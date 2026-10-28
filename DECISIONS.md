# Decisions

- **Backend persistence:** datasets, analysis evidence and voice sessions use SQLite in the local API. The database defaults to `apps/api/soniclens.db`; `SONICLENS_DB_PATH` can override it for isolated runs and tests.
- **Custom Web Audio:** numeric values and analysis plans map to oscillator tones after a user gesture. Trend uses sine tones, event-focused playback uses triangle tones, and comparison uses signed aligned differences. No speech or external audio is described as sonification.
- **Synthetic seeds are explicit:** energy and telemetry series are deterministic fixtures and labeled synthetic in the API/UI.
- **Voice is optional and authentic:** no browser speech synthesis or fixture is represented as Gnani. Prisma STT and Timbre TTS use server-side credentials loaded from the environment or repository-root `.env`; live service calls have been verified with a local spoken test clip.
- **Energy seed stores interval kWh:** the editable ₹/kWh tariff multiplies interval quantities directly; raw kW is not treated as energy.
- **Comparison uses aligned windows:** energy compares matching times of day; other series compare sequence positions. Returned pairs preserve exact source indices and differences; they do not imply causation.
- **Local intent is constrained deterministic routing:** bounded phrase-to-tool handling provides inspectable analysis without arbitrary code execution or fabricated values. Live voice requires configured Gnani credentials.
