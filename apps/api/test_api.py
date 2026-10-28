import os
import tempfile
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
