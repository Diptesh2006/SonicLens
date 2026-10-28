from __future__ import annotations

import csv
import io
import math
import os
import re
import sqlite3
import statistics
import asyncio
import base64
import json
import time
from datetime import datetime, timedelta, timezone
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import httpx
import websockets

app = FastAPI(title="SonicLens API", version="0.1.0", description="Grounded time-series analysis and sonification plans")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_methods=["*"], allow_headers=["*"])


class Sample(BaseModel):
    timestamp: str
    values: dict[str, float]


class Dataset(BaseModel):
    id: str
    name: str
    domain: Literal["energy", "generic_telemetry", "csv"]
    source: str
    unit: str
    metrics: list[str]
    samples: list[Sample]


class AnalyzeRequest(BaseModel):
    dataset_id: str
    metric: str
    mode: Literal["trend", "anomaly", "comparison"] = "trend"
    start: int = 0
    end: int | None = None
    tariff: float = Field(default=8, ge=0)


class FocusRequest(BaseModel):
    start: int = Field(ge=0)
    end: int = Field(gt=0)
    metric: str | None = None


def seeds() -> dict[str, Dataset]:
    start = datetime(2026, 10, 19, tzinfo=timezone.utc)
    energy = []
    for i in range(168):
        hour = i % 24
        value = 0.32 + (0.62 if 17 <= hour <= 21 else 0.12 if 7 <= hour <= 9 else 0) + 0.07 * math.sin(i * 0.8)
        if i == 114:
            value = 2.35
        if i // 24 in (5, 6):
            value *= 0.82
        energy.append(Sample(timestamp=(start + timedelta(hours=i)).isoformat(), values={"usage_kwh": round(value, 3)}))
    telemetry = []
    start2 = datetime(2026, 10, 28, tzinfo=timezone.utc)
    for i in range(144):
        spike = 1 if 77 <= i <= 82 else 0
        telemetry.append(Sample(timestamp=(start2 + timedelta(minutes=10*i)).isoformat(), values={"latency_ms": round(105 + 15*math.sin(i/8) + 310*spike, 1), "error_count": (2 + i%3 + 16*spike)*1.0, "request_count": 48 + (i*7)%24}))
    return {
        "energy-week": Dataset(id="energy-week", name="Household energy · 7 days", domain="energy", source="Synthetic demonstration data", unit="kWh per hour", metrics=["usage_kwh"], samples=energy),
        "api-telemetry": Dataset(id="api-telemetry", name="API service · 24 hours", domain="generic_telemetry", source="Synthetic demonstration data", unit="ms / count", metrics=["latency_ms", "error_count", "request_count"], samples=telemetry),
    }


DB_PATH = os.environ.get("SONICLENS_DB_PATH", os.path.join(os.path.dirname(__file__), "soniclens.db"))


def connect_db() -> sqlite3.Connection:
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db


def init_db() -> None:
    with connect_db() as db:
        db.execute("CREATE TABLE IF NOT EXISTS datasets (id TEXT PRIMARY KEY, payload TEXT NOT NULL)")
        db.execute("CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, payload TEXT NOT NULL)")
        for dataset in seeds().values():
            db.execute("INSERT OR REPLACE INTO datasets(id,payload) VALUES(?,?)", (dataset.id, dataset.model_dump_json()))


init_db()


def load_datasets() -> dict[str, Dataset]:
    with connect_db() as db:
        return {row["id"]: Dataset.model_validate_json(row["payload"]) for row in db.execute("SELECT id,payload FROM datasets ORDER BY id")}


def reset_demo_data() -> dict[str, Dataset]:
    seeded = seeds()
    with connect_db() as db:
        db.execute("DELETE FROM datasets WHERE id NOT IN (?,?)", tuple(seeded))
        db.execute("DELETE FROM sessions")
        for dataset in seeded.values():
            db.execute("INSERT OR REPLACE INTO datasets(id,payload) VALUES(?,?)", (dataset.id, dataset.model_dump_json()))
    return seeded


def save_dataset(dataset: Dataset) -> None:
    with connect_db() as db:
        db.execute("INSERT OR REPLACE INTO datasets(id,payload) VALUES(?,?)", (dataset.id, dataset.model_dump_json()))


class SessionTurn(BaseModel):
    role: Literal["user", "assistant"]
    text: str
    analysis_id: str | None = None


class VoiceSession(BaseModel):
    id: str
    dataset_id: str
    metric: str
    mode: Literal["trend", "anomaly", "comparison"]
    focus_start: int = 0
    focus_end: int | None = None
    playback_speed: float = 1
    turns: list[SessionTurn] = []


class QueryRequest(BaseModel):
    session_id: str
    dataset_id: str
    metric: str
    text: str = Field(min_length=1, max_length=1000)
    tariff: float = Field(default=8, ge=0)


class SpeakRequest(BaseModel):
    session_id: str
    dataset_id: str
    metric: str
    audio_base64: str = Field(min_length=1, max_length=16_000_000)
    sample_rate: Literal[16000, 44100, 48000] = 16000
    language_code: str = "indic-auto"
    tariff: float = Field(default=8, ge=0)


class SynthesizeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=3000)
    language: str = "auto"


def gnani_key() -> str | None:
    return os.getenv("GNANI_API_KEY")


def gnani_ready() -> bool:
    return bool(gnani_key())


async def prisma_transcribe(pcm: bytes, sample_rate: int, language_code: str) -> tuple[str, str | None]:
    key = gnani_key()
    if not key:
        raise HTTPException(503, "Gnani Prisma is not configured. Set GNANI_API_KEY on the API server.")
    headers = {"x-api-key-id": key, "x-model": os.getenv("GNANI_PRISMA_MODEL", "prisma-v3.0"), "lang_code": language_code, "x-sample-rate": str(sample_rate), "x-format": "transcribe", "x-idle-timeout-sec": "10"}
    transcript = ""
    detected = None
    try:
        async with websockets.connect(os.getenv("GNANI_PRISMA_URL", "wss://api.vachana.ai/stt/v3/stream"), additional_headers=headers, open_timeout=10, close_timeout=3, max_size=2_000_000) as ws:
            async def send_audio():
                # 100 ms PCM frames paced at source cadence, as Prisma expects for VAD.
                chunk_size = sample_rate * 2 // 10
                for offset in range(0, len(pcm), chunk_size):
                    chunk = pcm[offset:offset + chunk_size]
                    await ws.send(chunk)
                    await asyncio.sleep(len(chunk) / (sample_rate * 2))
                await ws.send(json.dumps({"type": "commit"}))
            async def receive_transcript():
                nonlocal transcript, detected
                async for message in ws:
                    frame = json.loads(message)
                    if frame.get("type") == "transcript":
                        transcript = (transcript + " " + frame.get("text", "")).strip()
                        detected = frame.get("detected_language_code", detected)
                    elif frame.get("type") == "error":
                        raise HTTPException(502, f"Gnani Prisma error: {frame.get('message', 'transcription failed')}")
                    if transcript:
                        break
            await asyncio.wait_for(asyncio.gather(send_audio(), receive_transcript()), timeout=30)
    except HTTPException:
        raise
    except (TimeoutError, asyncio.TimeoutError) as exc:
        raise HTTPException(504, "Gnani Prisma transcription timed out") from exc
    except Exception as exc:
        raise HTTPException(502, f"Gnani Prisma connection failed: {type(exc).__name__}") from exc
    if not transcript:
        raise HTTPException(422, "Prisma returned an empty transcript; please try again")
    return transcript, detected


async def timbre_synthesize(text: str, language: str = "auto") -> tuple[bytes, float]:
    key = gnani_key()
    if not key:
        raise HTTPException(503, "Gnani Timbre is not configured. Set GNANI_API_KEY on the API server.")
    payload = {"text": text[:3000], "model": os.getenv("GNANI_TIMBRE_MODEL", "timbre-v2.5"), "voice": os.getenv("GNANI_TIMBRE_VOICE", "Nalini"), "language": language, "speed": 1.0, "audio_config": {"encoding": "linear_pcm", "container": "wav", "num_channels": 1, "sample_rate": 48000, "sample_width": 2}}
    started = time.perf_counter()
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(os.getenv("GNANI_TIMBRE_URL", "https://api.vachana.ai/api/v1/tts/inference"), headers={"X-API-Key-ID": key}, json=payload)
        response.raise_for_status()
        audio = response.content
        if not audio.startswith(b"RIFF") or len(audio) < 44:
            raise HTTPException(502, "Gnani Timbre response was not a valid WAV audio file")
        return audio, round((time.perf_counter()-started)*1000, 1)
    except HTTPException:
        raise
    except httpx.TimeoutException as exc:
        raise HTTPException(504, "Gnani Timbre synthesis timed out") from exc
    except httpx.HTTPStatusError as exc:
        raise HTTPException(502, f"Gnani Timbre returned HTTP {exc.response.status_code}") from exc
    except httpx.HTTPError as exc:
        raise HTTPException(502, "Gnani Timbre connection failed") from exc


def get_session(session_id: str) -> VoiceSession:
    with connect_db() as db:
        row = db.execute("SELECT payload FROM sessions WHERE id=?", (session_id,)).fetchone()
    if not row:
        raise HTTPException(404, "Session not found; start a new exploration")
    return VoiceSession.model_validate_json(row["payload"])


def save_session(session: VoiceSession) -> None:
    with connect_db() as db:
        db.execute("INSERT OR REPLACE INTO sessions(id,payload) VALUES(?,?)", (session.id, session.model_dump_json()))


@app.get("/api/health")
def health():
    return {"status": "ok", "datasets": len(load_datasets()), "storage": "sqlite", "voice": {"provider": "Gnani", "configured": gnani_ready(), "stt_model": os.getenv("GNANI_PRISMA_MODEL", "prisma-v3.0"), "tts_model": os.getenv("GNANI_TIMBRE_MODEL", "timbre-v2.5")}}


@app.get("/api/datasets")
def list_datasets():
    return list(load_datasets().values())


@app.post("/api/demo/reset")
def reset_demo():
    datasets = reset_demo_data()
    return {"status": "reset", "datasets": list(datasets.values())}


@app.get("/api/datasets/{dataset_id}")
def get_dataset(dataset_id: str):
    datasets = load_datasets()
    if dataset_id not in datasets:
        raise HTTPException(404, "Dataset not found")
    return datasets[dataset_id]


@app.post("/api/datasets/import")
async def import_csv(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(400, "Upload a .csv file")
    raw = await file.read(10 * 1024 * 1024 + 1)
    if len(raw) > 10 * 1024 * 1024:
        raise HTTPException(413, "CSV must be 10 MB or smaller")
    try:
        rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
        if not rows or len(rows) > 50_000:
            raise ValueError("CSV must contain 1–50,000 data rows")
        headers = list(rows[0])
        time_key = next((h for h in headers if h and h.lower() in {"timestamp", "time", "date", "datetime"}), None)
        if not time_key:
            raise ValueError("Add a time column named timestamp, time, date, or datetime")
        metric_keys = []
        for header in headers:
            if not header or header == time_key:
                continue
            try:
                for row in rows:
                    if row[header]:
                        number = float(row[header])
                        if not math.isfinite(number):
                            raise ValueError(f"Metric '{header}' contains NaN or Infinity")
                metric_keys.append(header)
            except ValueError as exc:
                if "NaN" in str(exc) or "Infinity" in str(exc):
                    raise
        if not metric_keys:
            raise ValueError("Add at least one numeric metric column")
        samples = [Sample(timestamp=datetime.fromisoformat(row[time_key].replace("Z", "+00:00")).astimezone(timezone.utc).isoformat(), values={key: float(row[key]) for key in metric_keys if row[key]}) for row in rows]
        if any(not sample.values for sample in samples):
            raise ValueError("Every row must have at least one numeric value")
        samples.sort(key=lambda sample: sample.timestamp)
        if len({sample.timestamp for sample in samples}) != len(samples):
            raise ValueError("Duplicate timestamps are not supported; combine duplicate rows before importing")
    except (UnicodeDecodeError, csv.Error, ValueError, TypeError, AttributeError) as exc:
        raise HTTPException(400, f"Could not import CSV: {exc}") from exc
    dataset_id = f"upload-{uuid4().hex[:8]}"
    dataset = Dataset(id=dataset_id, name=file.filename, domain="csv", source="Uploaded CSV", unit="user supplied", metrics=metric_keys, samples=samples)
    save_dataset(dataset)
    return dataset


@app.post("/api/analysis")
def analyze(request: AnalyzeRequest):
    dataset = load_datasets().get(request.dataset_id)
    if not dataset:
        raise HTTPException(404, "Dataset not found")
    if request.metric not in dataset.metrics:
        raise HTTPException(422, "Metric is not present in this dataset")
    end = min(request.end or len(dataset.samples), len(dataset.samples))
    start = max(request.start, 0)
    selected = dataset.samples[start:end]
    values = [s.values[request.metric] for s in selected if request.metric in s.values]
    if not values:
        raise HTTPException(422, "Selected range has no values for this metric")
    median = statistics.median(values)
    deviations = [abs(v-median) for v in values]
    mad = statistics.median(deviations) or 1e-9
    threshold = median + 3 * 1.4826 * mad
    events = [{"index": start+i, "timestamp": selected[i].timestamp, "value": v} for i, v in enumerate(values) if v > threshold]
    changes = [{"index": start+i, "timestamp": selected[i].timestamp, "value": v, "delta": round(v-values[i-1], 4)} for i, v in enumerate(values) if i and abs(v-values[i-1]) >= max(mad*3, abs(median)*0.5)]
    peak_index = max(range(len(values)), key=values.__getitem__)
    focus = set(e["index"] for e in events)
    peaks = [{"index": start+i, "timestamp": selected[i].timestamp, "value": values[i]} for i in range(1, len(values)-1) if values[i] >= values[i-1] and values[i] > values[i+1] and values[i] >= median + mad*1.5]
    comparison = None
    if request.mode == "anomaly":
        focus.update(e["index"] for e in changes)
        if not focus:
            focus.add(start+peak_index)
    elif request.mode == "comparison":
        if len(values) >= 2:
            half = len(values)//2
            first, second = values[:half], values[-half:]
            aligned = half
            diffs = [second[i]-first[i] for i in range(aligned)]
            midpoint = start + half
            comparison = {"split_index": midpoint, "aligned_points": aligned, "mean_difference": round(statistics.mean(diffs), 4), "absolute_difference": round(abs(statistics.mean(diffs)), 4), "unit": dataset.unit, "period_a": {"start": start, "end": start+half}, "period_b": {"start": end-half, "end": end}, "differences": [round(value, 4) for value in diffs]}
            focus.update(range(start, start+half))
            focus.update(range(end-half, end))
    else:
        focus.update(range(start, end))
    cost = round(sum(values)*request.tariff, 2) if dataset.domain == "energy" and request.metric == "usage_kwh" else None
    plan_events = [{"index": index, "timestamp": dataset.samples[index].timestamp, "value": dataset.samples[index].values[request.metric]} for index in sorted(focus) if index < len(dataset.samples)]
    return {"analysis_id": f"ana-{uuid4().hex[:10]}", "dataset_id": dataset.id, "metric": request.metric, "mode": request.mode, "range": {"start": start, "end": end}, "summary": {"count": len(values), "mean": round(statistics.mean(values), 4), "median": round(median, 4), "min": min(values), "max": max(values), "peak_index": start+peak_index, "unit": dataset.unit, "energy_cost": cost, "tariff_per_kwh": request.tariff if cost is not None else None, "energy_semantics": "interval kWh multiplied by supplied tariff" if cost is not None else None}, "peaks": peaks, "comparison": comparison, "events": events, "abrupt_changes": changes, "focus_indices": sorted(focus), "plan": {"mode": request.mode, "metric": request.metric, "events": plan_events, "duration_ms": len(plan_events)*210}, "evidence": selected}


@app.post("/api/sessions", response_model=VoiceSession)
def create_session(dataset_id: str, metric: str):
    dataset = load_datasets().get(dataset_id)
    if not dataset:
        raise HTTPException(404, "Dataset not found")
    if metric not in dataset.metrics:
        raise HTTPException(422, "Metric is not present in this dataset")
    session = VoiceSession(id=f"ses-{uuid4().hex[:10]}", dataset_id=dataset_id, metric=metric, mode="trend", focus_end=len(dataset.samples))
    save_session(session)
    return session


@app.post("/api/sessions/{session_id}/focus", response_model=VoiceSession)
def select_focus(session_id: str, request: FocusRequest):
    session = get_session(session_id)
    dataset = load_datasets().get(session.dataset_id)
    if not dataset:
        raise HTTPException(404, "Dataset not found")
    if request.metric and request.metric not in dataset.metrics:
        raise HTTPException(422, "Metric is not present in this dataset")
    if request.start >= len(dataset.samples) or request.end > len(dataset.samples) or request.start >= request.end:
        raise HTTPException(422, "Focus range must select existing observations")
    session.focus_start, session.focus_end = request.start, request.end
    if request.metric:
        session.metric = request.metric
    save_session(session)
    return session


@app.get("/api/sessions/{session_id}", response_model=VoiceSession)
def read_session(session_id: str):
    return get_session(session_id)


@app.post("/api/voice/query")
def query_session(request: QueryRequest):
    session = get_session(request.session_id)
    if session.dataset_id != request.dataset_id:
        # A dataset switch clears old referents and binds subsequent turns to the active source.
        session.dataset_id, session.metric, session.mode = request.dataset_id, request.metric, "trend"
        session.focus_start, session.focus_end = 0, None
    dataset = load_datasets().get(session.dataset_id)
    if not dataset:
        raise HTTPException(404, "Dataset not found")
    if request.metric not in dataset.metrics:
        raise HTTPException(422, "Metric is not present in this dataset")
    text = request.text.strip()
    normalized = text.casefold()
    if any(word in normalized for word in ("compare", "difference", "previous day", "yesterday", "compare that")):
        session.mode = "comparison"
    elif any(word in normalized for word in ("anomal", "spike", "unusual", "increase sharply", "increased sharply")):
        session.mode = "anomaly"
    elif any(word in normalized for word in ("trend", "overall", "everything")):
        session.mode = "trend"
    speed_match = re.search(r"(?:at |speed )?(0\.5|1|1\.5|2)\s*x|slow(?:er|ly)", normalized)
    if speed_match:
        session.playback_speed = 0.5 if "slow" in normalized else float(speed_match.group(1) or 0.5)
    if "previous day" in normalized or "yesterday" in normalized:
        session.focus_start = max(0, session.focus_start - 24)
    end = session.focus_end or len(dataset.samples)
    result = analyze(AnalyzeRequest(dataset_id=dataset.id, metric=request.metric, mode=session.mode, start=session.focus_start, end=end, tariff=request.tariff))
    session.metric = request.metric
    session.focus_end = result["range"]["end"]
    if result["events"]:
        session.focus_start = result["events"][0]["index"]
    session.turns.extend([SessionTurn(role="user", text=text), SessionTurn(role="assistant", text=explain_result(result), analysis_id=result["analysis_id"])])
    session.turns = session.turns[-40:]
    save_session(session)
    return {"session": session, "analysis": result, "answer": explain_result(result), "provider": "deterministic_local_tools", "voice_status": "unconfigured"}


@app.post("/api/voice/speak")
async def speak_query(request: SpeakRequest):
    try:
        pcm = base64.b64decode(request.audio_base64, validate=True)
    except (ValueError, base64.binascii.Error) as exc:
        raise HTTPException(400, "Audio must be valid base64 PCM") from exc
    if len(pcm) < request.sample_rate // 4 or len(pcm) > 8_000_000 or len(pcm) % 2:
        raise HTTPException(400, "PCM audio must be 0.25–250 seconds of 16-bit mono audio")
    transcript, language = await prisma_transcribe(pcm, request.sample_rate, request.language_code)
    query = QueryRequest(session_id=request.session_id, dataset_id=request.dataset_id, metric=request.metric, text=transcript, tariff=request.tariff)
    result = query_session(query)
    audio, latency_ms = await timbre_synthesize(result["answer"], language or "auto")
    return {**result, "provider": "gnani_live", "transcript": transcript, "detected_language": language, "audio_base64": base64.b64encode(audio).decode("ascii"), "tts_latency_ms": latency_ms}


@app.post("/api/voice/synthesize")
async def speak_text(request: SynthesizeRequest):
    audio, latency_ms = await timbre_synthesize(request.text, request.language)
    return {"audio_base64": base64.b64encode(audio).decode("ascii"), "latency_ms": latency_ms, "provider": "gnani_live"}


def explain_result(result: dict) -> str:
    summary = result["summary"]
    if result["mode"] == "anomaly":
        if result["events"]:
            event = max(result["events"], key=lambda item: item["value"])
            return f"The selected range has {len(result['events'])} robust outlier event(s). The largest is observation {event['index']}, at {event['value']} {summary['unit']}."
        return f"No robust outliers were detected in {summary['count']} observations. The peak is {summary['max']} {summary['unit']}."
    if result["mode"] == "comparison" and result["comparison"]:
        comparison = result["comparison"]
        return f"Comparing two equal aligned portions across {comparison['aligned_points']} observations, the second period averaged {comparison['mean_difference']} {summary['unit']} different from the first."
    cost_text = f" At the supplied tariff, the interval energy cost is ₹{summary['energy_cost']:.2f}." if summary["energy_cost"] is not None else ""
    return f"Across {summary['count']} observations, the mean was {summary['mean']} {summary['unit']} and the peak was {summary['max']} {summary['unit']}.{cost_text}"
