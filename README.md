# SonicLens

SonicLens is a voice led time series analyst. Speak an analytical goal and it investigates a selected dataset, updates a presentation scene, shows the supporting readings, and narrates the grounded result. Energy usage and service telemetry are demonstration datasets that share the same analysis engine; CSV import lets you explore your own timestamped data.

## Run locally

Requirements: Python 3.11+, Node.js 20+ and npm. Use two PowerShell terminals from the repository root.

Add your Gnani key to the ignored root `.env` as `GNANI_API_KEY=...`. The API reads it on startup; never commit it. A safe template is in `.env.example`.

API terminal:

```powershell
cd apps/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Web terminal:

```powershell
cd apps/web
npm ci
npm run dev
```

Open <http://localhost:3000>. API health is <http://localhost:8000/api/health> and API docs are at <http://localhost:8000/docs>.

## Voice led walkthrough

1. Select the energy or API telemetry dataset, or import a CSV with a timezone aware timestamp and numeric columns.
2. Tap the microphone and ask: “Give me an overview”, “Find unusual spikes”, or “Compare with the previous period”.
3. Watch the narration, investigation steps, chart scene and evidence update together. Speak again while narration is playing to interrupt and redirect it.
4. Use scene history to restore an earlier presentation. Expand **Optional Audio Lab** to hear supplementary sonification.

Voice uses server side Gnani Prisma transcription and Timbre narration. A typed query is available when voice is unavailable. Analysis uses bounded deterministic tools; explanations do not claim causes unsupported by the measurements. Seeded datasets are synthetic. Energy cost requires confirmed interval kWh and a supplied tariff.

## Verify

```powershell
cd apps/api
python -m pytest test_api.py -q
cd ../web
npm run typecheck
npm run build
```

Technical reference: [API](docs/API.md), [architecture](docs/ARCHITECTURE.md), [voice setup](docs/GNANI_SETUP.md), [presentation engine](docs/PRESENTATION_ENGINE.md) and [demo guide](docs/DEMO.md).
