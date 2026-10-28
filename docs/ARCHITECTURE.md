# Architecture

The product uses a Next.js/TypeScript client and FastAPI/Python service. The client selects a dataset, metric, range and analysis mode; it renders backend observations in Recharts and requests analysis and a typed sonification plan. Browser Web Audio maps the selected plan to tones after explicit user interaction, while one playback index sequence drives the chart cursor.

FastAPI validates uploads and operation arguments, owns metric/unit semantics and computes numeric facts. Analysis results, datasets and voice sessions are persisted in SQLite. Each analysis includes its selected source observations and sonification plan and can be reloaded by analysis ID. Reset restores the synthetic energy and telemetry datasets and removes imported CSVs and sessions.

The local text intent parser routes a bounded set of analytical requests to deterministic analysis. It does not execute model-generated code or SQL and does not invent values. Gnani Prisma STT and Timbre TTS are optional server-side providers; keys remain in the API environment and can be loaded from the repository-root `.env`. Without credentials, voice is reported unavailable and local text analysis remains usable.

## Data path

```text
CSV or seeded fixture
  → FastAPI validation and SQLite
  → deterministic analysis and evidence
  → typed analysis/sonification plan
  → Next.js chart, evidence table and Web Audio
```

For voice, microphone PCM travels from the browser to the local API, then to Prisma. The recognized request selects a constrained analysis operation; Timbre receives the resulting grounded explanation. Spoken playback stops sonification first. Missing credentials and provider errors are surfaced by the API.

## Boundaries

- Energy and telemetry share the same dataset and analysis path; domain-specific units and sampling semantics prevent invalid cost calculations.
- CSV upload is limited to 10 MB and 50,000 rows. Time values must include timezone information; duplicate timestamps and non-finite values are rejected.
- Sonification previews play at most 150 evenly spaced selected points. Analytical summaries and evidence still use every selected row.
- SQLite is local demo storage; this is not a multi-user or production monitoring deployment.
