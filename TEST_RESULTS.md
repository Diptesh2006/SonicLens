# Test results

Results updated 2026-10-29. Commands ran from this Windows/OneDrive checkout.

## Latest verification

- `python -m pytest test_api.py -q` in `apps/api`: **PASS**, 28 passed.
- `npm run typecheck` in `apps/web`: **PASS**.
- `npm run build` in `apps/web`: **PASS**, production routes `/`, `/_not-found`, and `/icon.svg` generated.
- Production API and web app started at `http://localhost:8000` and `http://localhost:3000`.
- Browser verified energy/telemetry switch, trend/anomaly/comparison selection, aligned comparison evidence, chart cursor and play/pause/resume/stop, 2× playback rate, silent zero-volume playback, range updates and evidence retrieval.
- CSV browser journey imported 3 rows with one missing value. The source table showed that missing row; setting `kWh` and `interval_energy` enabled the correct ₹28.80 estimate for the two observed values at ₹8/kWh.
- Mobile viewport 390×844: main controls/evidence remained visible, document width matched the viewport, screenshot visually reviewed.
- Final production browser console: **0 errors, 0 warnings**.

## Limitations

- Authenticated provider path was subsequently verified: local spoken PCM → Prisma transcript (“Find unusual spikes”, `en-IN`) → anomaly analysis (largest observation 114, 2.35 kWh) → Timbre WAV (`RIFF`). `/api/health` reports the providers configured, the browser enables its microphone button, and the browser console has no errors/warnings.
- Physical speaker/headphone audibility was not independently assessed.
- Physical microphone capture/output and a recorded demo artifact have not been independently verified.

Earlier development notes recorded build and browser failures caused by the incomplete dependency tree and stale temporary server. Those were resolved: the production build and browser checks above ran successfully against the current checkout.
