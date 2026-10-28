# API

- `GET /api/health`: readiness and seeded dataset count.
- `GET /api/datasets`: energy and telemetry datasets with samples, units and synthetic provenance.
- `GET /api/datasets/{dataset_id}`: one dataset.
- `POST /api/datasets/import`: multipart CSV (`timestamp`/`time`/`date`/`datetime` plus numeric metrics), maximum 10 MB and 50,000 rows.
- `POST /api/analysis`: JSON `{dataset_id, metric, mode, start, end, tariff}`. Returns summary, robust outlier/change events, source evidence and focus indices.
- `POST /api/demo/reset`: restore the two deterministic synthetic datasets, remove imported CSV data, and clear conversation sessions.
- `POST /api/sessions?dataset_id=…&metric=…`: create a persistent exploration session.
- `GET /api/sessions/{session_id}` and `POST /api/sessions/{session_id}/focus`: inspect session context and set a validated selected range.
- `POST /api/voice/query`: constrained local text intent; returns the deterministic analysis and answer. This is not Gnani STT/TTS and does not speak.

Interactive schema: `/docs`. Datasets currently live in API process memory. API validation errors use standard FastAPI status/detail responses.
