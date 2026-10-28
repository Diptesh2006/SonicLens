# API

- `GET /api/health`: readiness and seeded dataset count.
- `GET /api/datasets`: energy and telemetry datasets with samples, units and synthetic provenance.
- `GET /api/datasets/{dataset_id}`: one dataset.
- `POST /api/datasets/import`: multipart CSV (`timestamp`/`time`/`date`/`datetime` plus numeric metrics), maximum 10 MB and 50,000 rows.
- `PATCH /api/datasets/{dataset_id}/metrics/{metric}/unit`: `{unit, sampling_kind}` lets the user correct imported metric units and declare `interval_energy`, `power_sample`, `sampled`, or `unknown`. Cost is returned only for explicitly declared interval energy in kWh; kW is never multiplied directly by tariff.
- `POST /api/analysis`: JSON `{dataset_id, metric, mode, start, end, tariff}`. Returns summary, robust outlier/change events, source evidence and focus indices.
- `GET /api/analysis/{analysis_id}`: retrieve a persisted analysis, source samples and sonification plan by its evidence ID.
- `POST /api/demo/reset`: restore the two deterministic synthetic datasets, remove imported CSV data, and clear conversation sessions.
- `POST /api/sessions?dataset_id=…&metric=…`: create a persistent exploration session.
- `GET /api/sessions/{session_id}` and `POST /api/sessions/{session_id}/focus`: inspect session context and set a validated selected range.
- `POST /api/voice/query`: constrained local text intent; returns the deterministic analysis and answer. This is not Gnani STT/TTS and does not speak.
- `POST /api/voice/speak`: bounded base64 mono PCM plus active dataset/session; uses real Prisma, deterministic analysis, then real Timbre WAV when server credentials are configured. It returns HTTP 503 when credentials are absent.
- `POST /api/voice/synthesize`: `{text, language}`; returns provider audio only when configured.

Interactive schema: `/docs`. Datasets and sessions are stored in SQLite. API validation errors use standard FastAPI status/detail responses.
