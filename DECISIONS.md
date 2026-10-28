# SonicLens decisions

## Product identity — 2026-10-29

SonicLens is a voice led, goal oriented time series analyst. Speech is the primary control and response channel; validated visual scenes and inspectable evidence are central outputs. Energy and telemetry are example datasets. Sonification stays available as a supplementary inspection tool.

## Analysis and trust boundaries

- Analytical facts come from bounded deterministic operations; model generated code or SQL is not executed.
- A scene references a saved analysis from the same dataset and metric; evidence IDs point to that analysis.
- Narration describes calculated evidence and does not infer causality.
- Voice uses server side Gnani Prisma and Timbre adapters; secrets remain in the API environment.
- User interruption stops current browser narration immediately. Provider work already submitted is not guaranteed cancellable.
- Session state is local SQLite and is not a production multi user architecture.

## Product scope

The first complete slice supports overview, trend, anomaly, comparison and numerical evidence scenes; scene history; and contextual voice follow ups. Imported CSV, energy cost semantics and telemetry remain reusable demonstrations. Further domains and streamed narration remain later work.
