# Architecture

The product uses a Next.js/TypeScript client and FastAPI/Python service. Its primary interface is spoken goal setting and narrated analysis. The API resolves voice or typed requests to bounded deterministic tools, persists evidence and builds a validated presentation scene; the client updates the chart, investigation steps, scene history and evidence from that same result. Optional Web Audio sonification lives in the Audio Lab.

FastAPI validates uploads and operation arguments, owns metric/unit semantics and computes numeric facts. Analysis results, datasets and voice sessions are persisted in SQLite. Each analysis includes its selected source observations and sonification plan and can be reloaded by analysis ID. Reset restores the synthetic energy and telemetry datasets and removes imported CSVs and sessions.

The local intent parser routes a bounded set of analytical requests to deterministic analysis. It does not execute model-generated code or SQL and does not invent values. Gnani Prisma STT and Timbre TTS provide the central voice interaction; keys remain in the API environment and can be loaded from the repository-root `.env`. Typed analysis remains available when voice is not configured.

## Data path

```text
CSV or seeded fixture
  → FastAPI validation and SQLite
  → deterministic analysis and persisted evidence
  → validated presentation scene and narration
  → Next.js scene driven chart, investigation steps and history
  → optional Web Audio sonification
```

For voice, microphone PCM travels from the browser to the local API, then to Prisma. The recognized request selects a constrained analysis operation; Timbre receives the resulting grounded explanation. Starting another capture interrupts local narration and prevents stale responses from replacing newer ones. See [PRESENTATION_ENGINE.md](PRESENTATION_ENGINE.md) for scene validation and session state.

## Boundaries

- Energy and telemetry share the same dataset and analysis path; domain-specific units and sampling semantics prevent invalid cost calculations.
- CSV upload is limited to 10 MB and 50,000 rows. Time values must include timezone information; duplicate timestamps and non-finite values are rejected.
- Sonification previews play at most 150 evenly spaced selected points. Analytical summaries and evidence still use every selected row.
- SQLite is local demo storage; this is not a multi-user or production monitoring deployment.
