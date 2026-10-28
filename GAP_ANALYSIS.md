# SonicLens product gap analysis

**Direction:** The user supplied `SonicLens — Complete Codex Master Prompt` on 29 October 2026 and explicitly asked to follow it. Where it changes the older PRD, this voice-native live analyst direction takes precedence. This audit records the repository as it existed at commit `30721cd`.

## Product and interaction

| Requirement | Existing implementation | Status | Work needed |
|---|---|---|---|
| General conversational data intelligence product | Landing copy and page identify household energy as the product; telemetry is a dataset option | Partially implemented | Present voice-led analysis as the product; treat energy and telemetry as demos on one shared workspace |
| Voice is the primary analytical interface | AudioWorklet capture, live Prisma, typed fallback and Timbre response work | Implemented, partially verified | Make listening, transcription, investigation and narration explicit states; keep the microphone available to interrupt narration |
| Grounded deterministic analysis | Bounded phrase routing and deterministic analysis return evidence | Implemented and verified | Expand useful overview, evidence, follow-up and comparison intents without unsupported claims |
| Structured presentation scenes | Analysis is applied directly to the chart; no scene model or persisted scene history | Missing | Add validated Pydantic scene schema, session persistence, deterministic planner and typed frontend renderer |
| Agent-controlled visual updates | Mode and range update after a voice query; no scene navigation or exact-readings action | Partially implemented | Apply chart type, focus, annotation and evidence from validated scenes; support previous-scene navigation |
| Real investigation timeline | No investigation steps are displayed or persisted | Missing | Return and render only executed steps: dataset/metric validation, analysis, evidence attachment and scene preparation |
| Conversational goal and dataset-aware memory | Session stores dataset, metric, mode, focus, turns and last analysis | Partially implemented | Persist the current goal, analysis steps, scene list and selected scene; restore scenes against saved analysis |
| Push-to-interrupt | Mic works between answers; narration cannot be redirected with one action | Missing | Stop narration and sonification, invalidate stale requests, start capture, then render the new result |
| Two shared demo domains and CSV | Energy, telemetry and CSV share API, analysis and chart components | Implemented, partially verified | Demonstrate voice-led analysis on both seeded domains; expose multi-metric requests only when calculations support them |
| Sonification is supplementary | Audio review currently has a prominent peer card beside the chart | Partially implemented | Move sound mapping and playback into a secondary Audio Lab disclosure |

## Engineering and verification

| Requirement | Existing implementation | Status | Work needed |
|---|---|---|---|
| Real Gnani Prisma and Timbre | Authenticated PCM → Prisma → analysis → Timbre journey passed with generated speech input | Implemented and verified | Preserve server-side credentials and report live/failed states honestly |
| Typed scene contracts | Existing `Analysis`/`Dataset` TypeScript types; no scene schema | Missing | Define matching Pydantic and TypeScript scene contracts; validate dataset, analysis and evidence references |
| Bounded analytical agent | Deterministic intent parser invokes at most one analysis operation | Partially implemented | Keep execution bounded; persist actual steps and explicit clarification/incomplete outcomes |
| Request cancellation and stale-result protection | Audio cleanup exists; overlapping requests are not generation-guarded | Missing | Use abort controller and request generation; stop narration on interruption or dataset change |
| Persistent scene retrieval | Analyses persist in SQLite; sessions persist turns but not scenes | Partially implemented | Persist scenes in the existing session and add a validated restore endpoint |
| API and architecture docs | Existing docs cover data, voice and sonification | Implemented, out of date for new direction | Add scene and interruption contracts; document the voice-led analyst and supplementary Audio Lab |
| Browser and API checks | 28 API tests, production build, typecheck and browser flows passed at last checkpoint | Implemented and verified for prior flow | Add checks for scene persistence/restore, bounded steps, interruption and voice-to-scene UI |
| Real device and acoustic behavior | Generated speech loopback tested; no physical microphone/speaker check | Requires device verification | Keep clearly marked as requiring a user-device check |

## First complete product slice

1. A voice or typed instruction becomes a persisted session goal.
2. The deterministic router validates the active dataset and metric, runs bounded analysis, attaches saved evidence, and produces a validated scene.
3. The scene changes the central chart and focus, appears in the real investigation timeline, and can be revisited.
4. Gnani speech narrates the grounded result; pressing the microphone during narration stops it and starts the next instruction.
5. A generation ID prevents an obsolete response from replacing the new scene.

This is a deterministic, bounded analyst orchestration layer. It does not claim an unconfigured LLM or unrestricted autonomous planning.
