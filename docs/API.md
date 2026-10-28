# API

- `GET /api/health`: readiness and seeded dataset count.
- `GET /api/datasets`: energy and telemetry datasets with samples, units and synthetic provenance.
- `GET /api/datasets/{dataset_id}`: one dataset.
- `POST /api/datasets/import`: multipart CSV (`timestamp`/`time`/`date`/`datetime` plus numeric metrics), maximum 10 MB and 50,000 rows.
- `POST /api/analysis`: JSON `{dataset_id, metric, mode, start, end, tariff}`. Returns summary, robust outlier/change events, source evidence and focus indices.

Interactive schema: `/docs`. Datasets currently live in API process memory. API validation errors use standard FastAPI status/detail responses.
