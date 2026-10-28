# SonicLens

SonicLens is a voice-first time-series explorer for one practical question: **when is a home using the most electricity, and what changed?** Ask aloud about spikes, compare days, or estimate a bill; SonicLens calculates the answer from the selected readings, speaks it back, and shows the chart and source observations behind it. The household dataset is synthetic, so no utility or physical meter is connected. A secondary API telemetry dataset demonstrates that the same analysis and sonification engine can handle other time series.

## Requirements

- Python 3.11 or newer
- Node.js 20 or newer and npm

## Run locally

From the repository root, use two PowerShell terminals.

Before starting the API, open the repository-root `.env` file and paste your Gnani key after `GNANI_API_KEY=`. That file is ignored by Git. The API loads it automatically; do not commit it or paste the key into chat. The checked-in `.env.example` is a safe template.

Terminal 1 — API:

```powershell
cd apps/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Terminal 2 — web app:

```powershell
cd apps/web
npm ci
npm run dev
```

Open <http://localhost:3000>. API health is at <http://localhost:8000/api/health>, with interactive docs at <http://localhost:8000/docs>.

## Verify

```powershell
cd apps/api
python -m pytest test_api.py -q
cd ../web
npm run typecheck
npm run build
```

## Product behavior

- Primary use case: investigate a week of household electricity readings, find unusually high usage, compare time periods and estimate cost at a user-entered tariff.
- Secondary use case: explore API latency and error telemetry with the same analysis and sound controls.
- CSV upload supports up to 10 MB and 50,000 rows. Timestamps must include a timezone; duplicate timestamps and non-finite values are rejected; missing metric values remain visible in evidence.
- Deterministic summaries, peaks, outliers, abrupt changes, aligned period comparisons and persisted source evidence.
- Energy cost appears only for data explicitly labeled as interval kWh and uses the entered ₹/kWh tariff. Raw kW is never treated as kWh.
- Trend, anomaly and signed comparison sonification use Web Audio after a user gesture. Previews schedule at most 150 evenly spaced points. Playback has range, cursor, pause/resume, stop, speed and volume controls.
- Each analysis exposes a stable evidence ID and exact timestamped source observations. Demo reset removes uploaded datasets and clears sessions.
- Voice is the primary interaction: one tap records until a short pause, then sends speech to server-side Gnani Prisma; deterministic analysis grounds the answer and Gnani Timbre speaks it back. A typed question remains available as a fallback. Voice is disabled until the API reports a key configured.

## Gnani configuration

Add `GNANI_API_KEY` to the repository-root `.env`; the API loads it when it starts. Optional model and endpoint settings are documented in [docs/GNANI_SETUP.md](docs/GNANI_SETUP.md). Live STT/TTS calls must be verified with your account; provider mocks are not live-integration evidence.

## Known limitations

- Live Prisma and Timbre provider calls were verified using a short local spoken test clip; the browser now reports Gnani ready. A physical microphone interaction and Hindi-English utterance still need a user-device check.
- Browser audio scheduling and cursor behavior were exercised, but audibility on a physical speaker/headphone output was not independently evaluated.
- The blinded listening protocol is a proposed formative test, not a completed participant study; SonicLens makes no efficacy or accessibility-validation claims.
- A recorded end-to-end demo artifact has not yet been captured.

See [PRD.md](PRD.md), [GOALS.md](GOALS.md), [PROGRESS.md](PROGRESS.md), [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), [docs/API.md](docs/API.md), [docs/SONIFICATION.md](docs/SONIFICATION.md), [docs/DEMO.md](docs/DEMO.md), and [docs/SOUND_EVALUATION.md](docs/SOUND_EVALUATION.md).
