# Presentation engine

## Purpose

The presentation engine turns a user's analytical goal into a validated, inspectable visual scene. It sits between deterministic analysis and the client: narration, chart mode, focus interval and evidence references all describe the same saved result. The voice path uses this engine on every successful analysis.

## Data contract

A `PresentationScene` contains a stable scene ID, scene kind, title, dataset and metric, saved analysis ID, chart type, selected interval, highlighted sample indices, evidence IDs, narration, suggested follow ups and creation time. The API validates that the saved analysis belongs to the same dataset and that its metric and focus indices are valid before storing the scene in its `VoiceSession`.

Scene kinds cover dataset overview, trend inspection, anomaly spotlight, period comparison, numerical evidence and finding summary. Area charts show trends and anomalies; bar charts show comparisons and exact readings. Each scene references its persisted deterministic analysis as evidence. The client renders scene history and can restore any prior scene through the session route.

## Request flow

1. Capture speech in the browser and send bounded PCM to the API; Prisma transcribes it. Typed input uses the same query route and intent handling.
2. The API resolves only supported goals to validated deterministic analysis. Ambiguous or causal requests receive a clarification instead of a fabricated result.
3. It persists the analysis, appends investigation steps, validates and saves the presentation scene, and updates session goal/current scene.
4. Timbre narrates the grounded explanation. The browser updates transcript, scene, chart and evidence from the same response.
5. A follow up reuses the session context. A new spoken turn stops current audio; scene history restores a prior result.

## State and limits

Sessions persist goal, analysis turns, up to 20 scenes, current scene, metric, mode and focus interval in SQLite. Investigation steps describe dataset inspection, calculation, evidence attachment and scene preparation. The implementation is synchronous and local; it does not claim hidden background agent work. Analysis is deterministic and bounded; narration does not infer causality. SQLite and the local app are not multi-user production infrastructure.

## Voice interruption

While a narration is playing, the microphone remains available. Starting a new capture pauses the current narration and sonification. A request generation token prevents stale browser responses from replacing a newer interaction. The user can also restore a saved scene through scene history. Browser/server speech synthesis is request-response rather than streamed TTS, so interruption stops local playback immediately; it does not cancel a provider request already in flight.
