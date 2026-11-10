# Voice led demonstration

## Before the walkthrough

1. Start the API and web app with the README commands. Confirm `/api/health` reports voice configured and the header says **VOICE READY**.
2. Choose **Home energy · 7 days** or **API service · 24 hours**. Both are synthetic examples; imported CSV can be used instead.
3. Use **Reset demo** before recording a fresh walkthrough.

## Three minute walkthrough

1. Tap the microphone and say: “Find the biggest spike, compare it with the previous period, and explain what changed.” Watch the answer and three-scene plan: overview, highlighted spike, and aligned comparison.
2. While Timbre is narrating, tap the microphone and give a new instruction. Local playback stops immediately and stale scenes are invalidated; the revised transcript is analyzed against the active dataset and metric.
3. Repeat with both seeded datasets. The energy comparison aligns readings by clock time; API telemetry compares equal adjacent sample windows. Inspect each scene's persisted evidence ID and the highlighted chart interval.
4. Use **Scene history** to restore the overview or anomaly scene. Confirm its analysis and evidence return with it.
5. Ask: “Show exact readings.” Inspect the persisted timestamps and values.
6. Open **Optional Audio Lab** to hear the selected series as supplementary sonification.

For the seeded energy data, the anomaly includes the known synthetic 2.35 kWh peak. The API telemetry example uses the same flow for latency and errors. Narration is grounded in calculated observations and does not establish causality.

## Input and recovery

Voice requires the server side Gnani key and a browser microphone permission. The live Gnani Prisma and Timbre endpoints have been exercised with authenticated requests. If permission or provider setup is unavailable, use the typed question fallback. If the browser blocks autoplay, use **Listen** on the answer. A follow up during playback interrupts local narration; a provider request already submitted may finish server side.

## Verification status

API tests and frontend typecheck pass. The end-to-end localhost browser run completed a Prisma voice query and rendered the three scenes with Timbre playback. In the headless browser's synthetic microphone interruption check, Prisma closed the follow-up stream with `no speech segment received`; therefore the revised spoken-turn loop still needs confirmation with a physical microphone and speaker in a user-driven browser session. Do not treat the full interruption journey as verified until that succeeds.
