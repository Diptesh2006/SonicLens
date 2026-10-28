# SonicLens progress

## Current checkpoint

Core data import, deterministic analysis, three sound modes, constrained text/voice adapters, evidence persistence, and the voice-first household energy workspace are implemented. On 29 October 2026, the production build and all 28 API tests passed; the production browser returned a grounded typed spike answer with evidence, and desktop and 390px mobile layouts rendered without horizontal overflow. Remaining user-device checks are physical microphone capture/output and a Hindi-English request; a repeatable demo recording also remains outstanding.

The API reads server configuration from the repository-root `.env` at startup. A nonempty key was detected without printing or logging its value. Explicit Prisma and Timbre endpoints are configured in the ignored `.env`; live provider calls now pass.

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

- 29 October 2026: production browser loaded seeded household energy with “VOICE READY”; typed “Find unusual spikes” returned the calculated 2.35 kWh peak with a persisted evidence ID.
- AudioWorklet browser simulation captured a Gnani-generated English utterance at 16 kHz; the real Prisma→analysis→Timbre route transcribed “Find unusual spikes,” returned the grounded 2.35 kWh answer, and exposed spoken replay. A code-mixed “Sirf unusual consumption spikes sunao” fixture was recognized as “Surf unusual consumption spikes soon” and routed to anomaly analysis. Silent input timed out with a retry message and sent no request. Browser console had no errors or deprecation warnings.
- The generated speech fixtures validate browser capture and the live provider chain, but do not replace testing with the user's physical microphone and speakers.
- Desktop browser at 1365×900 and mobile at 390×844: primary voice action, chart and energy summary were visible; document width matched viewport width; browser console had zero errors or warnings.
- The voice-first question, transcript, grounded answer and replay UI were reviewed in the mobile screenshot. Real-device microphone capture/output and the browser-to-live-Gnani round trip remain unverified.
- `python -m pytest test_api.py -q`: 28 passed.
- `npm run typecheck`: pass.
- `npm run build`: pass; routes prerendered, favicon included.
- Production app and API launched at localhost:3000/8000.
- Browser checked anomaly analysis, play/pause/resume/stop, comparison with 84 aligned pairs, moving cursor, 168-row evidence matching stored timestamps, range changes and Energy→Telemetry switching.
- Direct CSV upload: 3 rows with 1 missing reading; confirmed kWh interval semantics; evidence showed 2 observed readings, missing row, and ₹28.80 at ₹8/kWh.
- Mobile browser at 390×844: key controls and evidence visible; document width equaled viewport; screenshot reviewed.
- Browser set playback to 2× and volume to 0; cursor advanced and playback stopped cleanly.
- Final production browser console after rebuild: 0 errors and 0 warnings.
- Live Prisma transcription, grounded anomaly analysis, and Timbre WAV synthesis succeeded using a short local spoken PCM clip; the web app reports Gnani ready and enables its mic control.
- Physical microphone capture/output and a Hindi-English utterance were not independently verified.

## Next actions

1. Verify capture and playback with the user's physical microphone and speaker/headphones.
2. Capture a repeatable demo only if the environment can record browser audio faithfully.
