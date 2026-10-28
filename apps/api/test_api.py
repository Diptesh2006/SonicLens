import os
import tempfile
import base64
from datetime import datetime
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

_test_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_test_db.close()
os.environ["SONICLENS_DB_PATH"] = _test_db.name

from main import app

client = TestClient(app)


def test_seeded_datasets_and_health():
    assert client.get("/api/health").json()["datasets"] == 2
    assert {row["id"] for row in client.get("/api/datasets").json()} == {"energy-week", "api-telemetry"}


def test_energy_peak_and_cost_are_grounded():
    dataset = client.get("/api/datasets/energy-week").json()
    result = client.post("/api/analysis", json={"dataset_id": dataset["id"], "metric": "usage_kwh", "mode": "anomaly", "tariff": 8}).json()
    assert result["summary"]["max"] == 2.35
    assert result["summary"]["energy_cost"] == round(sum(s["values"]["usage_kwh"] for s in dataset["samples"])*8, 2)
    assert 114 in result["focus_indices"]


def test_csv_import_and_metric_validation():
    result = client.post("/api/datasets/import", files={"file": ("tiny.csv", b"timestamp,reading\n2026-01-01T00:00:00Z,2\n2026-01-01T01:00:00Z,4\n", "text/csv")})
    assert result.status_code == 200
    dataset = result.json()
    assert dataset["metrics"] == ["reading"] and len(dataset["samples"]) == 2
    bad = client.post("/api/analysis", json={"dataset_id": dataset["id"], "metric": "unknown"})
    assert bad.status_code == 422


def test_invalid_csv_is_actionable():
    result = client.post("/api/datasets/import", files={"file": ("bad.csv", b"x,y\na,1\n", "text/csv")})
    assert result.status_code == 400 and "time column" in result.json()["detail"]


def test_comparison_returns_aligned_difference():
    result = client.post("/api/analysis", json={"dataset_id": "energy-week", "metric": "usage_kwh", "mode": "comparison"}).json()
    assert result["comparison"]["aligned_points"] == 84
    assert result["comparison"]["period_a"]["end"] == result["comparison"]["period_b"]["start"]
    assert isinstance(result["comparison"]["mean_difference"], float)


def test_sessions_persist_and_query_updates_analysis():
    session = client.post("/api/sessions", params={"dataset_id": "energy-week", "metric": "usage_kwh"}).json()
    response = client.post("/api/voice/query", json={"session_id": session["id"], "dataset_id": "energy-week", "metric": "usage_kwh", "text": "Find unusual spikes"})
    assert response.status_code == 200
    body = response.json()
    assert body["analysis"]["mode"] == "anomaly"
    assert body["answer"] and body["analysis"]["analysis_id"]
    assert body["session"]["turns"][-1]["analysis_id"] == body["analysis"]["analysis_id"]
    assert client.get(f"/api/sessions/{session['id']}").json()["id"] == session["id"]


def test_comparison_pairs_same_offsets_and_exposes_differences():
    result = client.post("/api/analysis", json={"dataset_id": "energy-week", "metric": "usage_kwh", "mode": "comparison", "start": 12, "end": 60}).json()
    comparison = result["comparison"]
    assert comparison["aligned_points"] == len(comparison["differences"]) == 24
    assert comparison["period_a"] == {"start": 12, "end": 36}
    assert comparison["period_b"] == {"start": 36, "end": 60}


def test_focus_rejects_out_of_bounds_and_demo_reset_removes_uploads():
    session = client.post("/api/sessions", params={"dataset_id": "energy-week", "metric": "usage_kwh"}).json()
    invalid = client.post(f"/api/sessions/{session['id']}/focus", json={"start": 0, "end": 999})
    assert invalid.status_code == 422
    reset = client.post("/api/demo/reset").json()
    assert {dataset["id"] for dataset in reset["datasets"]} == {"energy-week", "api-telemetry"}
    assert len(client.get("/api/datasets").json()) == 2


def test_csv_normalizes_order_and_rejects_duplicate_timestamps():
    result = client.post("/api/datasets/import", files={"file": ("ordered.csv", b"timestamp,reading\n2026-01-01T01:00:00Z,2\n2026-01-01T00:00:00Z,1\n", "text/csv")})
    assert result.status_code == 200
    times = [sample["timestamp"] for sample in result.json()["samples"]]
    assert times == sorted(times)
    duplicate = client.post("/api/datasets/import", files={"file": ("duplicate.csv", b"timestamp,reading\n2026-01-01T00:00:00Z,1\n2026-01-01T00:00:00Z,2\n", "text/csv")})
    assert duplicate.status_code == 400 and "Duplicate timestamps" in duplicate.json()["detail"]


def test_csv_rejects_infinite_values_instead_of_silently_dropping_series():
    result = client.post("/api/datasets/import", files={"file": ("infinite.csv", b"timestamp,reading\n2026-01-01T00:00:00Z,Infinity\n", "text/csv")})
    assert result.status_code == 400 and "Infinity" in result.json()["detail"]


def test_voice_route_surfaces_missing_gnani_credentials():
    session = client.post("/api/sessions", params={"dataset_id": "energy-week", "metric": "usage_kwh"}).json()
    audio = base64.b64encode(bytes(16000)).decode()
    with patch("main.gnani_key", return_value=None):
        response = client.post("/api/voice/speak", json={"session_id":session["id"],"dataset_id":"energy-week","metric":"usage_kwh","audio_base64":audio,"sample_rate":16000})
    assert response.status_code == 503 and "GNANI_API_KEY" in response.json()["detail"]


def test_voice_route_rejects_invalid_pcm_before_provider_call():
    session = client.post("/api/sessions", params={"dataset_id": "energy-week", "metric": "usage_kwh"}).json()
    with patch("main.prisma_transcribe", new_callable=AsyncMock) as transcribe:
        response = client.post("/api/voice/speak", json={"session_id":session["id"],"dataset_id":"energy-week","metric":"usage_kwh","audio_base64":"@@@","sample_rate":16000})
    assert response.status_code == 400
    transcribe.assert_not_awaited()


def test_voice_route_uses_provider_transcript_and_returns_valid_wav():
    session = client.post("/api/sessions", params={"dataset_id": "energy-week", "metric": "usage_kwh"}).json()
    audio = base64.b64encode(bytes(16000)).decode()
    wav = b"RIFF" + bytes(40)
    with patch("main.prisma_transcribe", new_callable=AsyncMock, return_value=("Find unusual spikes", "en-IN")), patch("main.timbre_synthesize", new_callable=AsyncMock, return_value=(wav, 321.4)):
        response = client.post("/api/voice/speak", json={"session_id":session["id"],"dataset_id":"energy-week","metric":"usage_kwh","audio_base64":audio,"sample_rate":16000})
    assert response.status_code == 200
    assert response.json()["transcript"] == "Find unusual spikes"
    assert response.json()["analysis"]["mode"] == "anomaly"
    assert base64.b64decode(response.json()["audio_base64"]) == wav
    assert response.json()["tts_latency_ms"] == 321.4


def test_analysis_returns_local_peaks_and_energy_semantics():
    result = client.post("/api/analysis", json={"dataset_id":"energy-week","metric":"usage_kwh","mode":"trend"}).json()
    assert result["peaks"]
    assert all(result["peaks"][i]["value"] >= result["peaks"][i-1]["value"] for i in range(1,len(result["peaks"]))) is False or len(result["peaks"]) > 1
    assert result["summary"]["energy_semantics"] == "interval kWh multiplied by supplied tariff"
    assert result["summary"]["tariff_per_kwh"] == 8


def test_followup_previous_day_compares_equal_active_window_and_slow_replay():
    session = client.post("/api/sessions", params={"dataset_id":"energy-week","metric":"usage_kwh"}).json()
    client.post(f"/api/sessions/{session['id']}/focus", json={"start":48,"end":72})
    response = client.post("/api/voice/query", json={"session_id":session["id"],"dataset_id":"energy-week","metric":"usage_kwh","text":"Compare that with the previous day"}).json()
    comparison = response["analysis"]["comparison"]
    assert comparison["aligned_points"] == 24
    assert comparison["period_a"] == {"start":24,"end":48}
    assert comparison["period_b"] == {"start":48,"end":72}
    replay = client.post("/api/voice/query", json={"session_id":session["id"],"dataset_id":"energy-week","metric":"usage_kwh","text":"Replay that interval slowly"}).json()
    assert replay["session"]["playback_speed"] == 0.5
    assert replay["analysis"]["range"] == {"start":24,"end":72}


def test_ambiguous_query_requests_clarification_without_fabricating_analysis():
    session = client.post("/api/sessions", params={"dataset_id":"energy-week","metric":"usage_kwh"}).json()
    response = client.post("/api/voice/query", json={"session_id":session["id"],"dataset_id":"energy-week","metric":"usage_kwh","text":"Why did it happen?"}).json()
    assert response["clarification"]["needed"] is True
    assert response["analysis"] is None
    assert len(response["clarification"]["choices"]) == 3


def test_demo_hinglish_transcript_routes_to_anomaly_tool():
    session = client.post("/api/sessions", params={"dataset_id":"energy-week","metric":"usage_kwh"}).json()
    response = client.post("/api/voice/query", json={"session_id":session["id"],"dataset_id":"energy-week","metric":"usage_kwh","text":"Sirf unusual consumption spikes sunao"}).json()
    assert response["analysis"]["mode"] == "anomaly"
    assert response["analysis"]["summary"]["max"] == 2.35


def test_metric_alias_and_cost_intent_use_validated_energy_tool():
    session = client.post("/api/sessions", params={"dataset_id":"api-telemetry","metric":"latency_ms"}).json()
    response = client.post("/api/voice/query", json={"session_id":session["id"],"dataset_id":"api-telemetry","metric":"latency_ms","text":"Show the latency trend"}).json()
    assert response["analysis"]["metric"] == "latency_ms"
    energy_session = client.post("/api/sessions", params={"dataset_id":"energy-week","metric":"usage_kwh"}).json()
    cost = client.post("/api/voice/query", json={"session_id":energy_session["id"],"dataset_id":"energy-week","metric":"usage_kwh","text":"What did this energy cost at my tariff?","tariff":10}).json()
    assert cost["analysis"]["summary"]["tariff_per_kwh"] == 10
    assert cost["analysis"]["summary"]["energy_cost"] is not None


def test_causal_why_question_does_not_invent_cause():
    session = client.post("/api/sessions", params={"dataset_id":"energy-week","metric":"usage_kwh"}).json()
    response = client.post("/api/voice/query", json={"session_id":session["id"],"dataset_id":"energy-week","metric":"usage_kwh","text":"Why was usage high?"}).json()
    assert response["analysis"] is None
    assert "do not identify why" in response["answer"]


def test_datasets_expose_correct_per_metric_units_and_sampling_kind():
    energy = client.get("/api/datasets/energy-week").json()
    telemetry = client.get("/api/datasets/api-telemetry").json()
    assert energy["sampling_kind"] == "interval_energy" and energy["metric_units"]["usage_kwh"] == "kWh"
    assert telemetry["metric_units"] == {"latency_ms":"ms","error_count":"count","request_count":"requests / interval"}


def test_csv_missing_values_and_unit_corrections_persist():
    imported = client.post("/api/datasets/import", files={"file": ("missing.csv", b"timestamp,reading\n2026-01-01T00:00:00Z,2\n2026-01-01T01:00:00Z,\n2026-01-01T02:00:00Z,4\n", "text/csv")})
    assert imported.status_code == 200
    dataset = imported.json()
    assert dataset["missing_counts"]["reading"] == 1
    assert dataset["samples"][1]["values"] == {}
    analysis = client.post("/api/analysis", json={"dataset_id":dataset["id"],"metric":"reading"}).json()
    assert analysis["summary"]["count"] == 2 and analysis["summary"]["missing_count"] == 1
    changed = client.patch(f"/api/datasets/{dataset['id']}/metrics/reading/unit", json={"unit":"widgets"})
    assert changed.json()["unit"] == "widgets"
    assert client.get(f"/api/datasets/{dataset['id']}").json()["metric_units"]["reading"] == "widgets"


def test_csv_cost_requires_explicit_kwh_unit_semantics():
    imported = client.post("/api/datasets/import", files={"file": ("usage.csv", b"timestamp,usage_kwh\n2026-01-01T00:00:00Z,2\n2026-01-01T01:00:00Z,3\n", "text/csv")}).json()
    request = {"dataset_id":imported["id"],"metric":"usage_kwh","tariff":8}
    before = client.post("/api/analysis", json=request).json()
    assert before["summary"]["energy_cost"] is None
    client.patch(f"/api/datasets/{imported['id']}/metrics/usage_kwh/unit", json={"unit":"kWh"})
    after = client.post("/api/analysis", json=request).json()
    assert after["summary"]["energy_cost"] == 40


def test_power_samples_never_receive_interval_energy_cost():
    imported = client.post("/api/datasets/import", files={"file": ("power.csv", b"timestamp,power\n2026-01-01T00:00:00Z,2\n2026-01-01T01:00:00Z,3\n", "text/csv")}).json()
    client.patch(f"/api/datasets/{imported['id']}/metrics/power/unit", json={"unit":"kW","sampling_kind":"power_sample"})
    result = client.post("/api/analysis", json={"dataset_id":imported["id"],"metric":"power","tariff":8}).json()
    assert result["summary"]["energy_cost"] is None
    assert result["summary"]["energy_semantics"] is None


def test_csv_rejects_timezone_naive_timestamps_and_analysis_rejects_empty_range():
    naive = client.post("/api/datasets/import", files={"file": ("naive.csv", b"timestamp,value\n2026-01-01 00:00:00,1\n", "text/csv")})
    assert naive.status_code == 400 and "has no timezone" in naive.json()["detail"]
    empty = client.post("/api/analysis", json={"dataset_id":"energy-week","metric":"usage_kwh","start":0,"end":0})
    assert empty.status_code == 422


def test_prisma_languages_are_validated_before_network_call():
    session = client.post("/api/sessions", params={"dataset_id":"energy-week","metric":"usage_kwh"}).json()
    audio = base64.b64encode(bytes(16000)).decode()
    invalid = client.post("/api/voice/speak", json={"session_id":session["id"],"dataset_id":"energy-week","metric":"usage_kwh","audio_base64":audio,"language_code":"xx-XX"})
    assert invalid.status_code == 422
    with patch("main.gnani_key", return_value="test-key"), patch.dict("os.environ", {"GNANI_PRISMA_MODEL":"gnani-prisma-v2.5"}), patch("main.websockets.connect") as connect:
        mixed = client.post("/api/voice/speak", json={"session_id":session["id"],"dataset_id":"energy-week","metric":"usage_kwh","audio_base64":audio,"language_code":"hi-IN,en-IN"})
    assert mixed.status_code == 422 and "one language" in mixed.json()["detail"]
    connect.assert_not_called()


def test_energy_comparison_aligns_clock_time_and_returns_pair_evidence():
    result = client.post("/api/analysis", json={"dataset_id":"energy-week","metric":"usage_kwh","mode":"comparison","start":10,"end":58}).json()
    samples = client.get("/api/datasets/energy-week").json()["samples"]
    comparison = result["comparison"]
    assert comparison["aligned_by"] == "time_of_day"
    assert comparison["aligned_points"] == 24
    assert all(datetime.fromisoformat(samples[p["index_a"]]["timestamp"]).hour == datetime.fromisoformat(samples[p["index_b"]]["timestamp"]).hour for p in comparison["pairs"])
    assert result["focus_indices"] == sorted({index for pair in comparison["pairs"] for index in (pair["index_a"],pair["index_b"])})
