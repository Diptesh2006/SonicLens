from fastapi.testclient import TestClient

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
