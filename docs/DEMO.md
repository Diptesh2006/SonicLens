# Voice led demonstration

## Before the walkthrough

1. Start the API and web app with the README commands. Confirm `/api/health` reports voice configured and the header says **VOICE READY**.
2. Choose **Home energy · 7 days** or **API service · 24 hours**. Both are synthetic examples; imported CSV can be used instead.
3. Use **Reset demo** before recording a fresh walkthrough.

## 60 second walkthrough

1. **0–12s:** “Every day, we generate huge amounts of data. But understanding it still means staring at dashboards, manually comparing graphs, and searching for patterns. What if we could simply talk to our data?”
2. **12–20s:** “That's why I built SonicLens, a voice-powered AI data analyst that explains your data while highlighting the actual evidence.”
3. **20–35s:** Tap the microphone and say: “Find the strongest upward growth in my electricity usage.” Let Timbre narrate while the chart focuses the calculated interval.
4. **35–45s:** Interrupt with: “Now show me the strongest decline.” Confirm the prior narration stops, the transcript is recognized, and the chart and spoken explanation update.
5. **45–52s:** Expand **Inspect timestamps and values** to show the exact evidence behind the analysis.
6. **52–60s:** “Powered by Gnani Prisma for speech recognition and Timbre for natural voice responses, SonicLens makes data analysis conversational. SonicLens — Don't just see your data. Talk to it.”

For the seeded energy data, the anomaly includes the known synthetic 2.35 kWh peak. The API telemetry example uses the same flow for latency and errors. Narration is grounded in calculated observations and does not establish causality.

## Input and recovery

Voice requires the server side Gnani key and a browser microphone permission. The live Gnani Prisma and Timbre endpoints have been exercised with authenticated requests. If permission or provider setup is unavailable, use the typed question fallback. If the browser blocks autoplay, use **Listen** on the answer. A follow up during playback interrupts local narration; a provider request already submitted may finish server side.

## Verification status

API tests and frontend typecheck pass. The end-to-end localhost browser run completed a Prisma voice query and rendered the three scenes with Timbre playback. In the headless browser's synthetic microphone interruption check, Prisma closed the follow-up stream with `no speech segment received`; therefore the revised spoken-turn loop still needs confirmation with a physical microphone and speaker in a user-driven browser session. Do not treat the full interruption journey as verified until that succeeds.
