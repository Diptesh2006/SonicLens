# Voice led demonstration

## Before the walkthrough

1. Start the API and web app with the README commands. Confirm `/api/health` reports voice configured and the header says **VOICE READY**.
2. Choose **Home energy · 7 days** or **API service · 24 hours**. Both are synthetic examples; imported CSV can be used instead.
3. Use **Reset demo** before recording a fresh walkthrough.

## Three minute walkthrough

1. Tap the microphone and say: “Give me an overview of this dataset.” Watch the answer, four investigation steps, overview scene, chart and evidence update together.
2. While Timbre is narrating, tap the microphone and say: “Find unusual spikes.” The first narration stops; the chart moves to the anomaly scene and highlights the calculated readings.
3. Ask: “Compare that with the previous period.” The session keeps its dataset and metric context, and the scene switches to a comparison view.
4. Use **Scene history** to restore the overview or anomaly scene. Confirm its analysis and evidence return with it.
5. Ask: “Show exact readings.” Inspect the persisted timestamps and values.
6. Open **Optional Audio Lab** to hear the selected series as supplementary sonification.

For the seeded energy data, the anomaly includes the known synthetic 2.35 kWh peak. The API telemetry example uses the same flow for latency and errors. Narration is grounded in calculated observations and does not establish causality.

## Input and recovery

Voice requires the server side Gnani key and a browser microphone permission. If permission or provider setup is unavailable, use the typed question fallback. If the browser blocks autoplay, use **Listen** on the answer. A follow up during playback interrupts local narration; a provider request already submitted may finish server side.
