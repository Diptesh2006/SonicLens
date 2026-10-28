from __future__ import annotations

import csv
import io
import math
import statistics
from datetime import datetime, timedelta, timezone
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

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


DATASETS = seeds()


@app.get("/api/health")
def health():
    return {"status": "ok", "datasets": len(DATASETS)}


@app.get("/api/datasets")
def list_datasets():
    return list(DATASETS.values())


@app.get("/api/datasets/{dataset_id}")
def get_dataset(dataset_id: str):
    if dataset_id not in DATASETS:
        raise HTTPException(404, "Dataset not found")
    return DATASETS[dataset_id]


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
        metric_keys = [h for h in headers if h and h != time_key and all(not row[h] or math.isfinite(float(row[h])) for row in rows)]
        if not metric_keys:
            raise ValueError("Add at least one numeric metric column")
        samples = [Sample(timestamp=datetime.fromisoformat(row[time_key].replace("Z", "+00:00")).astimezone(timezone.utc).isoformat(), values={key: float(row[key]) for key in metric_keys if row[key]}) for row in rows]
        if any(not sample.values for sample in samples):
            raise ValueError("Every row must have at least one numeric value")
    except (UnicodeDecodeError, csv.Error, ValueError, TypeError) as exc:
        raise HTTPException(400, f"Could not import CSV: {exc}") from exc
    dataset_id = f"upload-{uuid4().hex[:8]}"
    dataset = Dataset(id=dataset_id, name=file.filename, domain="csv", source="Uploaded CSV", unit="user supplied", metrics=metric_keys, samples=samples)
    DATASETS[dataset_id] = dataset
    return dataset


@app.post("/api/analysis")
def analyze(request: AnalyzeRequest):
    dataset = DATASETS.get(request.dataset_id)
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
    if request.mode == "anomaly":
        focus.update(e["index"] for e in changes)
        if not focus:
            focus.add(start+peak_index)
    elif request.mode == "comparison":
        midpoint = start + len(values)//2
        focus.update(range(start, min(midpoint, end)))
        focus.update(range(midpoint, end))
    else:
        focus.update(range(start, end))
    cost = round(sum(values)*request.tariff, 2) if dataset.domain == "energy" and request.metric == "usage_kwh" else None
    return {"analysis_id": f"ana-{uuid4().hex[:10]}", "dataset_id": dataset.id, "metric": request.metric, "mode": request.mode, "range": {"start": start, "end": end}, "summary": {"count": len(values), "mean": round(statistics.mean(values), 4), "median": round(median, 4), "min": min(values), "max": max(values), "peak_index": start+peak_index, "unit": dataset.unit, "energy_cost": cost, "tariff_per_kwh": request.tariff if cost is not None else None}, "events": events, "abrupt_changes": changes, "focus_indices": sorted(focus), "evidence": selected}
