# SonicLens goals

Statuses: `NOT_STARTED`, `IN_PROGRESS`, `PASS`, `FAIL`, `BLOCKED_EXTERNAL`.

| ID | Acceptance criterion | Status | Verification / evidence |
|---|---|---|---|
| DOD-01 | Documented local frontend and API startup | PASS | README startup commands used to launch API on 8000 and production web app on 3000 |
| DOD-02 | Bounded CSV import, UTC normalization, ordering, duplicate/non-finite validation, missing-value and editable unit handling | PASS | 28 API tests pass, including CSV ordering, duplicate timestamps, Infinity, missing rows, and persistent unit edits; limits 10 MB/50k rows |
| DOD-03 | Synthetic energy and telemetry datasets | PASS | Browser loaded 168 energy and 144 telemetry observations after deterministic reset |
| DOD-04 | Chart shows backend observations and selected metric/range | PASS | Browser range changed energy coverage 168→48; dataset switch showed telemetry latency and its range-specific values |
| DOD-05 | Summary, local peaks, outlier, abrupt-change and aligned period comparison | PASS | API tests verify computed values; browser comparison returned 84 aligned time-of-day pairs |
| DOD-06 | Energy cost uses labeled tariff and confirmed interval kWh; never treats kW as kWh | PASS | API tests cover seed tariff, explicit CSV kWh confirmation and no estimate for kW power samples |
| DOD-07 | Browser generates data-mapped trend audio | IN_PROGRESS | Web Audio is gesture-started and cursor advances; audio device output has not been independently heard |
| DOD-08 | Anomaly mode focuses detected intervals | PASS | Browser selected anomaly mode; persisted analysis returned event focus; playback controls operated |
| DOD-09 | Comparison mode uses aligned series observations and reports differences | PASS | 84 aligned energy pairs verified in browser; comparison playback cursor advances over paired indices and uses signed difference pitch mapping |
| DOD-10 | Playback controls, focus range, rate, volume | PASS | Browser verified play, pause, resume, stop and range; speed set to 2×, volume set to 0 and cursor still advanced silently |
| DOD-11 | Chart cursor tracks scheduled notes | PASS | Browser timeline timestamp advanced during playback in trend/comparison flows |
| DOD-12 | Constrained natural-language intent routes analysis | PASS | 28 API tests cover English/Hinglish intents, aliases, cost and clarification |
| DOD-13 | Follow-up context resolution | PASS | API tests verify previous-period alignment, replay speed, persisted turns and unsupported-cause refusal |
| DOD-14 | Results have inspectable, persistent evidence IDs and source samples | PASS | API verifies storage/retrieval; browser expanded table with 168 source rows matching first/last persisted UTC timestamps |
| DOD-15 | Authentic server-side Gnani Prisma adapter | PASS | Authenticated live Prisma call transcribed a spoken test clip as “Find unusual spikes” and detected `en-IN` |
| DOD-16 | Authentic server-side Gnani Timbre adapter | PASS | Two authenticated live calls returned RIFF WAV audio; response latency was reported by the service |
| DOD-17 | Live Gnani microphone-to-spoken-answer journey | IN_PROGRESS | Live PCM→Prisma→anomaly analysis→Timbre path returned the grounded 2.35 kWh result and WAV; production browser voice UI is ready, but physical microphone capture/output has not been exercised |
| DOD-18 | Hindi-English spoken request verified | IN_PROGRESS | Credentials and endpoints configured; English provider round-trip passed, Hindi-English live utterance remains unverified |
| DOD-19 | Actionable upload and API errors | PASS | 28 API tests cover invalid schema, duplicates, non-finite values, invalid metrics/ranges and voice errors |
| DOD-20 | Synthetic data and local audio labels are honest | PASS | Browser confirmed synthetic fixture labels, unconfigured voice label and no synthetic badge on CSV uploads by implementation |
| DOD-21 | Responsive desktop and mobile layout | PASS | Production browser at 1365×900 and 390×844 showed the voice prompt, chart and energy summary; document width matched viewport; mobile screenshot visually reviewed |
| DOD-22 | Server-side keys, bounded uploads, constrained operations | PASS | API tests confirm missing credentials and limits; voice keys are read server-side and operation routing is bounded |
| DOD-23 | Backend tests, frontend typecheck and production build | PASS | 29 Oct 2026: `python -m pytest test_api.py -q` 28 passed; TypeScript `--noEmit --incremental false` and `next build` exit 0 |
| DOD-24 | Browser end-to-end seeded exploration | PASS | 29 Oct 2026 production browser loaded seeded energy, typed “Find unusual spikes” returned the calculated 2.35 kWh peak with an evidence ID; desktop/mobile widths checked; console had 0 errors and warnings |
| DOD-25 | Repeatable demo recording flow | IN_PROGRESS | Resettable browser walkthrough works; audio capture recording was not produced in this environment |
| DOD-26 | Setup, architecture, API, voice, audio and demo docs | PASS | README, architecture, API, Gnani setup, sonification, demo and sound evaluation docs reviewed and updated against current implementation |
| DOD-27 | Energy and telemetry share engine | PASS | Browser switched energy→telemetry and analysis updated to the telemetry metric without errors |
| DOD-28 | Blinded sound-value evaluation exists without efficacy claims | PASS | `docs/SOUND_EVALUATION.md` specifies randomized clips, blinded answer key and cautious reporting; no results are claimed |
