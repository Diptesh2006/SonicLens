# SonicLens progress

## Current checkpoint

Core data import, deterministic analysis, three sound modes, constrained text/voice adapters, evidence persistence, and browser workspace are implemented. Production build, CSV upload, explicit unit/cost flow, 390px layout, and browser journeys pass from the actual OneDrive checkout. Remaining work is final documentation/demo review and audio capture verification; authenticated live Gnani access is unavailable in the current environment.

The API now reads server configuration from the repository-root `.env` at startup. The local `.env` contains no key yet; the owner can add it without exposing the value in chat.

## Recent product slices

- Fixed dataset provenance labels and added branded favicon.
- Comparison sonification now plays only aligned pairs and maps signed deltas to a shared bounded pitch range.
- Added an expandable UTC source-observation table tied to persisted analysis evidence.
- Added a text description adjacent to the chart for selected coverage, mean, peak, and source-value location.
- Fixed dataset switching and CSV upload to select a valid metric immediately.
- CSV browser flow preserves missing rows and computes cost only after explicit kWh interval semantics are confirmed.
- Preview sonification is capped at 150 evenly distributed points; zero volume is silent; audio nodes disconnect on completion; spoken narration stops sonification first.
- Added a blinded formative listening protocol with no efficacy claims.

## Implemented

- FastAPI health, dataset listing/detail, analysis, CSV import, session/query, evidence retrieval, reset and voice routes.
- Seeded energy and telemetry datasets; SQLite datasets, sessions, plans, analysis payloads and evidence.
- Bounded CSV import (10 MB/50k rows), strict timestamp ordering/uniqueness, non-finite rejection and missingness counts.
- Deterministic statistics, peaks, robust outliers, changes, aligned comparisons, energy tariff semantics, evidence source samples.
- Web Audio trend, anomaly and signed aligned-comparison sonification with chart cursor, playback rate, pause, stop, volume and range.
- Constrained text intent, session followups, clarification and server-side Gnani Prisma/Timbre adapters with credentials surfaced honestly.
- Responsive Next.js UI, data provenance, metric/unit selection, chart description, evidence table and saved evidence reload.

## Verification evidence

- `python -m pytest test_api.py -q`: 28 passed.
- `npm run typecheck`: pass.
- `npm run build`: pass; routes prerendered, favicon included.
- Production app and API launched at localhost:3000/8000.
- Browser checked anomaly analysis, play/pause/resume/stop, comparison with 84 aligned pairs, moving cursor, 168-row evidence matching stored timestamps, range changes and Energy→Telemetry switching.
- Direct CSV upload: 3 rows with 1 missing reading; confirmed kWh interval semantics; evidence showed 2 observed readings, missing row, and ₹28.80 at ₹8/kWh.
- Mobile browser at 390×844: key controls and evidence visible; document width equaled viewport; screenshot reviewed.
- Browser set playback to 2× and volume to 0; cursor advanced and playback stopped cleanly.
- Final production browser console after rebuild: 0 errors and 0 warnings.
- Live Gnani calls and physical audio-output audibility were not independently verified.

## Next actions

1. Final review README, architecture and Gnani setup docs for current commands and payloads.
2. Capture a repeatable demo only if the environment can record browser audio faithfully.
3. Reconcile goals and evidence; keep live Gnani criteria blocked unless valid credentials are configured.
