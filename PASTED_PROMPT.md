# CODEX MASTER PROMPT — BUILD SONICLENS END TO END

## Role and Objective

You are acting as the **founding full-stack engineer, AI engineer, technical architect, and product designer** for SonicLens.

Your responsibility is to build a complete, polished, functional application—not merely create a project skeleton, write documentation, or produce a prototype with simulated buttons.

**Project:** SonicLens  
**Tagline:** Hear your data. Ask what matters.  
**Category:** Conversational AI, Data Sonification, Multimodal Analytics  
**Target:** Gnani.ai Voice AI Challenge  
**Deployment target:** Localhost initially  
**Primary stack:** Next.js, TypeScript, FastAPI, Python, SQLite, Web Audio API, Gnani Prisma, Gnani Timbre

### Your mission

Build a production-quality MVP that allows people to:

1. Upload or select numerical datasets.
2. Hear trends, anomalies, and relationships through meaningful sound representations.
3. Ask spoken questions about their data.
4. Receive accurate, natural spoken explanations.
5. Change the auditory representation through conversational commands.
6. Compare datasets, time periods, and individual metrics.
7. Investigate specific ranges through follow-up questions.
8. Maintain conversational context during an investigation.
9. Inspect the precise numerical evidence supporting every AI explanation.
10. Use the same application across different data domains without rebuilding the analytical engine.

The finished application must be demonstrable entirely through a local browser, laptop microphone, and speakers.

**Do not stop at planning. Implement, execute, test, diagnose, fix, and verify the actual application.**

---

# 1. READ THE EXISTING PRD FIRST

Before writing or modifying code:

1. Inspect the current repository.
2. Locate `PRD.md`, `SonicLens_End_to_End_PRD_Codex.md`, or another existing SonicLens requirements document.
3. Read the entire document, including architecture, API contracts, testing requirements, execution rules, and Definition of Done.
4. Treat that document as the detailed source of truth for requirements.
5. Treat this prompt as the implementation and execution directive.

If both this prompt and the PRD exist, follow both.

If there is a conflict:
- Preserve the latest confirmed product scope: a **domain-independent conversational data-sonification platform**, not an ML-only monitoring tool.
- Prefer explicit, measurable requirements over ambiguous statements.
- Preserve security and correctness.
- Record any significant decision in `DECISIONS.md`.

If the PRD does not exist, proceed using this prompt as the complete implementation contract. Do not block implementation unnecessarily.

Do not overwrite existing work without inspecting it.

---

# 2. UNDERSTAND THE ACTUAL PRODUCT

SonicLens is not a chatbot that describes charts.

SonicLens is not a tool that converts CSV values into random musical notes.

SonicLens is a **conversational auditory data-exploration platform**.

Its main innovation is *question-conditioned sonification*.

Traditional data sonification converts values into sound according to predefined mappings.

SonicLens allows users to change **what the data sounds like based on what they are trying to investigate**.

Consider the same energy-consumption dataset.

The user says:

"Play the overall electricity consumption trend."

The application generates an auditory representation of the consumption values.

The user then says:

"Only play the hours where consumption increased unusually."

The application performs numerical anomaly/change analysis, selects the relevant periods, and produces a different auditory representation.

The user then says:

"Compare those hours with yesterday."

The application aligns the time periods, calculates the differences, updates the visualizations, and generates comparison audio.

The user then says:

"Why was Tuesday's usage unusually high?"

The agent presents the actual measurements and possible interpretations, while refusing to invent a cause that is not supported by the dataset.

**The sound, visualization, analytical result, and AI explanation must all be derived from the same data.**

This consistency is a fundamental engineering requirement.

---

# 3. PRODUCT SCOPE

The SonicLens architecture must be independent of any individual data domain.

Do not hardcode the application around ML training.

Do not make ML epochs, training loss, validation loss, or model accuracy mandatory concepts in the main application.

The shared system should understand:

- Datasets.
- Time series.
- Numerical measurements.
- Metric units.
- Selected intervals.
- Anomalies and changes.
- Comparisons.
- Trends.
- Relationships.
- Sonification plans.
- Conversational context.

Implement two domain presets for the MVP.

## Domain A: Energy Explorer

The user explores household or building electricity consumption.

Example questions:

- "Play my electricity usage for the last week."
- "When was consumption unusually high?"
- "Compare Monday and Tuesday."
- "How much more did I consume in the evening?"
- "What would this usage cost at eight rupees per unit?"
- "Replay the highest-consumption period slowly."

The system must support accurate energy calculations based on dataset semantics.

For example, if the dataset represents energy consumed per hour in kWh, a period's total can be calculated by summing its values.

If it contains instantaneous power measurements in kW, total energy must be calculated using proper time integration.

Do not confuse power and energy.

Tariff calculations must use the user-supplied tariff and clearly state the assumptions.

## Domain B: Generic Telemetry Explorer

The user explores application or system performance.

Example questions:

- "Play the API latency trend."
- "Highlight unusual latency spikes."
- "Compare error counts with response time."
- "Where did both metrics increase together?"
- "Replay only the last ten minutes."
- "What was the maximum latency?"

The same analytical and auditory engines must support this dataset.

Do not create an entirely separate backend for each domain.

## Future domain adapters

Design the architecture to accommodate:

- ML experiment monitoring.
- Scientific and environmental measurements.
- Research datasets.
- Educational mathematical functions.
- Accessibility-oriented data exploration.
- Financial and business metrics.
- Continuous operational monitoring.

These are future extensions, not mandatory implementations for the initial MVP.

---

# 4. USER EXPERIENCE — COMPLETE FLOW

The application should work as follows.

## User Journey 1: First launch

The user opens:

`http://localhost:3000`

A polished SonicLens dashboard appears.

A sample energy dataset is loaded automatically.

The user sees:

- Dataset name.
- Time coverage.
- Available metrics.
- Measurement units.
- Interactive chart.
- Voice assistant control.
- Audio visualization controls.
- Insight summary.
- A few suggested voice commands.

The interface must immediately explain what SonicLens does without requiring the user to read lengthy documentation.

The user clicks **Play Data**.

The browser generates actual data-driven sound.

The chart cursor moves in synchronization with audio playback.

The user can pause, stop, slow down, or select an interval.

## User Journey 2: Voice-driven exploration

The user presses the microphone button and speaks:

"Show me the days where electricity usage was unusually high."

The application:

1. Captures microphone audio.
2. Sends it securely through the backend to Gnani Prisma.
3. Displays the recognized transcript.
4. Interprets the request.
5. Selects an appropriate deterministic analytics tool.
6. Detects the requested events.
7. Highlights them in the chart.
8. Generates an appropriate sonification plan.
9. Produces actual nonverbal audio for those selected events.
10. Uses Gnani Timbre to speak a grounded explanation.

The response should include actual values and timestamps.

Do not hardcode an answer specifically for this sentence.

Equivalent requests with different phrasing should use the same underlying tools.

## User Journey 3: Conversational follow-up

The user asks:

"Compare that with the previous day."

The agent should understand what "that" refers to based on the active investigation.

It must reuse the previously selected metric and interval where appropriate.

The application then:

- Computes the comparison.
- Updates the chart.
- Generates comparison audio.
- Speaks the result.
- Shows the supporting calculations.

The user continues:

"Replay only the biggest difference, more slowly."

The system selects the correct interval and changes playback speed.

This must work without requiring the user to repeat the complete dataset name or selected metric.

## User Journey 4: Switch domains

The user selects a telemetry dataset.

The same workspace and voice agent continue working.

The user asks:

"Where did errors rise along with latency?"

SonicLens calculates the relationship, highlights the relevant interval, and produces corresponding sound.

This demonstrates that SonicLens is a reusable platform rather than a single-purpose energy application.

## User Journey 5: CSV import

The user imports a valid CSV.

The system must:

- Validate file type and size.
- Inspect headers.
- Identify or ask the user to select the time column.
- Identify numerical columns.
- Handle missing and invalid observations.
- Preserve correct units.
- Store the dataset.
- Render an interactive chart.
- Enable sonification.
- Support analytical queries.

Errors must be understandable and actionable.

---

# 5. FRONTEND DESIGN

Build a visually impressive but practical engineering application.

The frontend should look like a serious SaaS product, not a generic AI-generated dashboard.

## Design principles

- Dark-first interface.
- Clean, modern typography.
- Professional visual hierarchy.
- Restrained color palette.
- Large, readable charts.
- Clear microphone interaction.
- Excellent audio controls.
- Small but meaningful animations.
- Responsive layout.
- Consistent spacing and component styling.

Suggested visual palette:

- Background: deep charcoal/navy.
- Primary accent: cyan/teal.
- Secondary accent: muted violet.
- Warning: amber.
- Error: restrained red.
- Successful state: green.

Use professional fonts such as Geist or Inter.

Use Lucide icons.

Avoid excessive gradients, pointless glowing effects, and decorative cards that convey no information.

## Main layout

### Top navigation

Show:

- SonicLens branding.
- Active dataset.
- Import button.
- Gnani service status.
- Audio output status.
- Settings.

### Sidebar

Navigation sections:

- Explore.
- Datasets.
- Audio Lab.
- Compare.
- Sessions.
- Settings.

Keep future features disabled or hidden rather than creating nonfunctional navigation.

### Main workspace

The screen should contain:

**Dataset header**
- Dataset title.
- Domain.
- Time range.
- Available metrics.
- Selected analysis mode.

**Data overview**
- Current/average measurement.
- Maximum.
- Minimum.
- Biggest detected change.
- Data quality indicator.

**Primary visualization**
- Large interactive time-series chart.
- Multiple metric support.
- Clearly indicated units.
- Interval highlighting.
- Playback cursor.
- Tooltip values.
- Selected anomaly markers.

**Audio exploration panel**
- Play.
- Pause.
- Stop.
- Replay.
- Volume.
- Playback speed.
- Audio mode selector.
- Audio mapping explanation.
- Currently selected interval.

**Voice investigator**
- Microphone button.
- Listening state.
- Recognized speech.
- Agent response.
- Voice playback.
- Supporting evidence.
- Suggested follow-up questions.

**Analysis timeline**
- Detected anomalies.
- Selected events.
- Comparison events.
- Previous queries.

## Quality requirements

Every visible button must have meaningful behavior.

Avoid placeholder UI.

Provide proper loading, error, empty, and success states.

The UI must remain usable without Gnani credentials, with voice functionality honestly labeled unavailable.

---

# 6. TECHNOLOGY STACK

Use the following unless the existing repository already has an equivalent, well-functioning alternative.

## Frontend

- Next.js with App Router.
- TypeScript.
- Tailwind CSS.
- Recharts.
- Lucide React.
- Web Audio API, optionally Tone.js.
- Zod for frontend validation.
- TanStack Query where it adds value.

## Backend

- Python.
- FastAPI.
- Pydantic.
- SQLAlchemy or SQLModel.
- SQLite.
- Pandas.
- NumPy.
- SciPy where needed.
- WebSockets for live or replay streams.

## AI

- Gnani Prisma for speech recognition.
- Gnani Timbre for synthesized spoken explanations.
- A configurable reasoning model for intent interpretation and tool selection.
- Structured JSON outputs.
- Deterministic analytical tools.

## Testing

- Pytest for backend.
- Vitest or an equivalent frontend testing framework.
- Playwright for browser-level end-to-end tests.
- TypeScript type checking.
- ESLint.
- Build validation.

Do not introduce Redis, Kubernetes, Kafka, Celery, or other infrastructure that is unnecessary for a localhost MVP.

---

# 7. BACKEND ARCHITECTURE

Maintain these logical modules.

```text
SonicLens
│
├── Data Sources
│   ├── CSV uploads
│   ├── Seeded datasets
│   └── Optional metric streams
│
├── Data Ingestion
│   ├── Validation
│   ├── Time normalization
│   ├── Unit handling
│   └── Persistence
│
├── Analytics Engine
│   ├── Descriptive statistics
│   ├── Trend detection
│   ├── Anomaly detection
│   ├── Period comparison
│   └── Series relationship analysis
│
├── Sonification Planner
│   ├── Trend audio
│   ├── Anomaly-focused audio
│   ├── Difference/comparison audio
│   └── Audio metadata and synchronization
│
├── Domain Adapters
│   ├── Energy
│   ├── Generic telemetry
│   └── Future adapters
│
├── Conversational Voice Agent
│   ├── Gnani Prisma STT
│   ├── Intent understanding
│   ├── Tool execution
│   ├── Session memory
│   └── Gnani Timbre TTS
│
└── Frontend
    ├── Dashboard
    ├── Charts
    ├── Audio playback
    └── Voice investigator
```

Keep these concerns separate.

The reasoning model must not calculate statistics independently when deterministic tools can do so.

The sonification engine must not invent values.

The dashboard must not use fabricated metric values unrelated to the current dataset.

---

# 8. DATA MODEL AND PERSISTENCE

Implement persistent entities for:

- Dataset.
- Data series.
- Metric observation.
- Analysis result.
- Sonification plan.
- Conversation session.
- Session context.
- Voice interaction.
- Saved audio exploration state.

A dataset should include:

```json
{
  "id": "dataset_001",
  "name": "Household Electricity Usage",
  "domain": "energy",
  "time_column": "timestamp",
  "metrics": [
    {
      "name": "consumption",
      "unit": "kWh"
    }
  ],
  "source": "seeded",
  "created_at": "ISO-8601 timestamp"
}
```

Each observation should include:

```json
{
  "dataset_id": "dataset_001",
  "timestamp": "ISO-8601 timestamp",
  "values": {
    "consumption": 2.45
  }
}
```

Use actual timestamps and preserve the source timezone or the dataset's configured timezone.

Avoid mixing naive and timezone-aware timestamps.

Handle:

- Missing values.
- Duplicate timestamps.
- Unsorted rows.
- Unsupported units.
- Nonfinite values.
- Uneven sample intervals.
- Empty datasets.
- Misaligned comparison periods.

Provide explicit warnings when interpolation or resampling is necessary.

---

# 9. DETERMINISTIC ANALYTICS ENGINE

Implement the following analytical operations.

## Descriptive analysis

- Minimum.
- Maximum.
- Mean.
- Median.
- Standard deviation.
- Start and end values.
- Absolute change.
- Percentage change where valid.
- Top peaks.
- Lowest points.

## Trend analysis

- Rolling mean.
- Positive/negative trend.
- Basic slope calculation.
- Relevant trend reversals.

## Anomaly and change detection

Implement configurable methods such as:

- Robust z-score.
- Median absolute deviation.
- Relative change thresholds.
- Rolling change detection.

The selected algorithm and thresholds must be visible or inspectable.

Do not equate anomaly detection with causation.

## Period comparison

Support:

- Date-to-date comparison.
- Selected-range comparison.
- Current period vs previous period.
- Metric-to-metric comparison.
- Aligned difference calculations.

Only compare aligned observations or explicitly document the chosen resampling method.

## Energy adapter

Support:

- Peak usage intervals.
- Total energy consumed.
- Day-to-day consumption comparison.
- High-usage periods.
- Cost calculation from a supplied tariff.

Handle kW versus kWh correctly.

## Telemetry adapter

Support:

- Latency spikes.
- Error count spikes.
- Period comparisons.
- Joint increase detection.
- Simple aligned-series relationships.

Do not imply correlation proves causality.

All results must include machine-readable numerical evidence.

---

# 10. SONIFICATION ENGINE

This is the defining technical feature of SonicLens.

The sonification engine must produce actual audio derived from numerical values.

Do not generate arbitrary sound effects and pretend they represent the dataset.

Use browser-side audio synthesis for nonverbal data sound.

## Mode A — Trend Listening

Map selected numerical values into a predictable audio sequence.

Requirements:

- Consistent mapping of normalized values to pitch.
- Time progresses through the sequence.
- Higher or lower values produce an audible change.
- The chart cursor tracks audio playback.
- Playback speed is configurable.
- The mapping is explained to the user.

For the same metric and shared scale, identical values must map to the same pitch.

## Mode B — Anomaly Listening

Identify unusual intervals using deterministic analysis.

Produce short, distinguishable audio cues corresponding to the selected anomalies.

The user must be able to:

- Play all anomalies.
- Select one anomaly.
- Replay its context.
- Slow down playback.
- Inspect the exact numerical evidence.

Do not generate a generic alarm disconnected from the data.

## Mode C — Comparison Listening

Support comparison of two aligned series or time periods.

Implement at least one understandable method:

- Sequential playback with a shared numerical scale.
- Alternating equal-duration segments.
- Sonification of the numerical difference.

Avoid dense simultaneous sound layers that make comparisons confusing.

## Audio safety and usability

- Reasonable bounded frequencies.
- Conservative default volume.
- No abrupt loud sounds.
- Short envelopes to prevent clicks.
- Pause and stop work immediately.
- No autoplay without user interaction.
- Proper cleanup of audio nodes.
- Handle browser audio permission restrictions.
- Avoid uncontrolled overlap between data audio and agent speech.

## Question-conditioned sonification

The voice agent must be able to alter the audio plan.

Examples:

"Play the overall trend."

"Only play the unusual spikes."

"Compare these two measurements."

"Replay that interval."

"Slow down the selected part."

"Play only the difference."

Represent audio instructions as typed JSON.

Example:

```json
{
  "mode": "comparison",
  "dataset_id": "dataset_001",
  "metrics": ["consumption"],
  "range": {
    "start": "ISO-8601 timestamp",
    "end": "ISO-8601 timestamp"
  },
  "comparison": {
    "strategy": "previous_period"
  },
  "playback_speed": 0.75,
  "normalization": "shared_scale"
}
```

Validate this plan before execution.

The backend decides **what should be sonified**.

The frontend audio engine decides **how to synthesize the specified sound**.

The LLM should not directly write arbitrary audio-generation code.

---

# 11. GNANI.AI INTEGRATION

Gnani is a mandatory, meaningful part of the application.

Implement two actual integrations:

## Gnani Prisma — Speech-to-Text

The browser records the user's voice.

The backend sends audio to the documented Gnani Prisma API.

The application receives the transcript and uses it to understand the requested analytical operation.

Support:

- English.
- Hindi-English code switching where supported by the selected API configuration.
- Conversational follow-ups.
- Visible recognized transcript.
- Clear error handling.
- Microphone permission handling.

Use the current official Gnani documentation.

Do not invent API paths, codecs, model names, or response fields.

Prefer a reliable push-to-talk implementation before adding complex real-time streaming.

## Gnani Timbre — Text-to-Speech

After deterministic analysis, the AI agent generates a concise explanation.

Gnani Timbre synthesizes it into natural speech.

The application plays the result through the browser.

Requirements:

- Actual audio output.
- Text transcript of the spoken answer.
- Playback cancellation.
- Sensible language configuration.
- Error states.
- Audio focus management.

Sonification should pause or duck while the voice agent is speaking.

## Gnani API security

Use server-side environment variables.

Example:

```env
GNANI_API_KEY=
GNANI_STT_MODEL=
GNANI_TTS_MODEL=
GNANI_TTS_VOICE=
```

Use only variables actually needed by the verified API implementation.

Never expose API secrets in client-side code.

Never commit credentials.

## Provider adapters

Define explicit interfaces for STT and TTS.

Implement:

- A real Gnani provider.
- A clearly labeled fixture provider for deterministic testing.

If credentials are missing, the application must still support datasets, analytics, charts, and sonification.

However, it must clearly indicate that the live voice integration is unavailable.

Never present fixture-generated transcripts or audio as genuine Gnani inference.

Before declaring voice integration complete, verify it using a real authenticated API request.

If the current API requires different parameters, follow official documentation and record the details in the setup guide.

---

# 12. VOICE AGENT

The voice agent should be a constrained analytical assistant with tool-calling capability.

It must not function as a generic chatbot.

Its main purpose is to interpret spoken analytical requests and update the SonicLens workspace.

## Agent tools

Implement tools equivalent to:

```python
list_datasets()
select_dataset(dataset_id)
list_metrics(dataset_id)
get_dataset_summary(dataset_id)
get_metric_statistics(dataset_id, metric, range)
detect_anomalies(dataset_id, metric, range)
compare_periods(dataset_id, metric, first_range, second_range)
compare_metrics(dataset_id, metric_a, metric_b, range)
focus_interval(start, end)
set_audio_mode(mode, options)
set_playback_speed(speed)
play_audio()
pause_audio()
explain_analysis(result_id)
```

Use typed request and response schemas.

Validate arguments.

Do not allow arbitrary shell access or unrestricted Python execution.

## Conversation memory

Store the current investigation context:

- Dataset.
- Selected metric.
- Selected interval.
- Last anomaly.
- Last comparison.
- Active audio mode.
- Recent tool results.
- Recent user questions.

Example:

User: "Show me the biggest spike."

Agent: Selects the largest anomaly.

User: "What about the previous day?"

Agent: Compares the selected anomaly interval with the corresponding previous-day interval.

User: "Play that slowly."

Agent: Replays the currently relevant comparison interval.

The agent must correctly resolve references such as:

- That.
- Those hours.
- The same period.
- The previous day.
- The other metric.
- Replay it.

If reference resolution is genuinely ambiguous, ask a short clarification rather than guessing.

This is session memory, not a broad personal-memory platform.

## Agent execution pattern

Use:

**Understand → Plan tool operation → Execute deterministic tool → Validate result → Update UI/audio → Explain through Timbre.**

Do not create an uncontrolled autonomous reasoning loop.

For straightforward commands, execute one or two tools and return promptly.

For compound requests, support bounded multistep tool execution.

Use structured outputs wherever possible.

---

# 13. API CONTRACTS

Build a documented FastAPI API.

Suggested endpoints:

```text
GET    /api/health

GET    /api/datasets
GET    /api/datasets/{dataset_id}
POST   /api/datasets/import
DELETE /api/datasets/{dataset_id}

GET    /api/datasets/{dataset_id}/metrics

POST   /api/analysis/summary
POST   /api/analysis/anomalies
POST   /api/analysis/compare
POST   /api/analysis/trends

POST   /api/sonification/plan

POST   /api/voice/transcribe
POST   /api/voice/query
POST   /api/voice/synthesize

POST   /api/sessions
GET    /api/sessions/{session_id}

POST   /api/demo/reset

WS     /ws/datasets/{dataset_id}
```

Change endpoint naming if necessary for a coherent API, but preserve all required capabilities.

## API quality

- Typed Pydantic schemas.
- Correct status codes.
- Validation errors.
- Bounded file uploads.
- Safe CSV handling.
- Clear backend error responses.
- Timeouts on external calls.
- WebSocket reconnection where applicable.
- No leaked API keys.
- Deterministic analysis.
- Proper database persistence.

Provide OpenAPI documentation automatically through FastAPI.

---

# 14. DEMONSTRATION DATASETS

Create deterministic, reproducible sample datasets.

## Dataset 1: Household Energy Consumption

Generate hourly consumption data with:

- A normal daily pattern.
- Higher evening consumption.
- A deliberately injected unusual spike.
- A weekend variation.
- Enough history for day-to-day comparisons.

The dataset must have believable units and timestamps.

Mark it as synthetic.

## Dataset 2: Server Telemetry

Generate timestamped metrics including:

- API latency.
- Request count.
- Error count.

Include:

- Normal performance.
- A latency spike.
- A period with jointly increasing latency and errors.
- Recovery to baseline.

Mark it as synthetic.

## Optional Dataset 3: ML Training

Only after the primary system works, add an example ML experiment dataset.

Do not let this optional dataset dictate core architecture.

## Demo reset

Create a deterministic reset mechanism.

The developer should be able to start a demonstration from exactly the same initial state repeatedly.

---

# 15. TESTING AND EVALUATION

Testing must cover actual application behavior, not merely successful imports.

## Backend unit tests

Test:

- CSV parsing.
- Timestamp normalization.
- Unit handling.
- Missing values.
- Duplicate timestamps.
- Statistical calculations.
- Anomaly detection.
- Period comparisons.
- Energy cost estimates.
- Telemetry comparisons.
- Sonification plan validation.
- Session-context resolution.

## Frontend tests

Test:

- Dataset selection.
- Metric selection.
- Audio mode switching.
- Playback state.
- Selected intervals.
- Voice loading/error states.
- Evidence display.
- Responsive layout where practical.

## Audio engine tests

Verify:

- Deterministic mapping.
- Correct audio duration relative to selected data.
- Consistent normalization.
- Correct cursor alignment.
- Pause/stop behavior.
- No accidental autoplay.
- No overlapping audio contexts.
- Proper cleanup.

## Voice agent tests

Use deterministic fixture transcripts for automated tests.

Test at least:

- Select metric.
- Find anomaly.
- Compare previous day.
- Replay last selected interval.
- Change playback speed.
- Ask an ambiguous follow-up.
- Switch dataset.
- Prevent stale context from leaking into the next dataset.

## Gnani integration verification

When credentials are available:

- Test an authenticated Prisma transcription.
- Test an authenticated Timbre synthesis.
- Verify response audio playback.
- Record actual request latency.
- Verify browser microphone flow.

Do not fabricate test results.

## Browser end-to-end tests

Using Playwright or an equivalent tool, verify that:

1. The app starts.
2. The energy dataset loads.
3. The chart renders.
4. Audio playback begins after a user gesture.
5. The user can select an interval.
6. The selected interval is reflected in analysis.
7. A fixture voice request invokes the correct tool.
8. The dashboard updates.
9. Dataset switching works.
10. Error states are handled.

---

# 16. PRODUCT DEMO — 60 SECONDS

Build a reliable live demo around the following sequence.

### 0–10 seconds: Introduce the product

Open SonicLens with household electricity data.

Explain:

"This is SonicLens. Instead of only visualizing data, you can hear it and ask questions about the patterns."

### 10–20 seconds: Hear the dataset

Start trend sonification.

The chart cursor progresses with the sound.

### 20–32 seconds: Speak an analytical request

Say:

"Sirf unusual consumption spikes sunao."

Gnani Prisma transcribes it.

The application isolates unusual periods and changes the audio accordingly.

### 32–43 seconds: Investigate

Ask:

"Which day had the biggest increase?"

Gnani Timbre speaks the exact date and numerical result.

The chart highlights the supporting evidence.

### 43–52 seconds: Conversational context

Ask:

"Compare that with the previous day."

The agent understands the reference and performs a real comparison.

### 52–60 seconds: Demonstrate generality

Switch to server telemetry.

Ask:

"Play the period where latency and errors increased together."

The same platform works without changing its core architecture.

Build the interface so that this flow is straightforward to execute.

Do not hardcode responses or fake an API call merely to make the recording appear successful.

---

# 17. IMPLEMENTATION PLAN

Execute work in meaningful vertical slices.

## Phase 1 — Project foundation

Deliver:

- Monorepo structure.
- Next.js frontend.
- FastAPI backend.
- SQLite database.
- Shared schemas.
- Environment setup.
- Health endpoint.
- Basic tests.

Verify that the frontend can communicate with the backend.

## Phase 2 — Data ingestion and analysis

Deliver:

- CSV import.
- Seeded datasets.
- Dataset selection.
- Statistics.
- Anomaly detection.
- Period comparison.
- Domain adapters.

Verify numerical correctness.

## Phase 3 — Functional dashboard

Deliver:

- Complete visual layout.
- Data charts.
- Metric controls.
- Range selection.
- Analysis panel.
- Evidence display.

Verify actual backend data is rendered.

## Phase 4 — Sonification

Deliver:

- Trend audio.
- Anomaly audio.
- Comparison audio.
- Synchronization with charts.
- Audio legend.
- Playback controls.

Verify actual sound is generated from dataset values.

## Phase 5 — Gnani integration

Deliver:

- Prisma adapter.
- Timbre adapter.
- Browser microphone interface.
- Voice responses.
- Service-status indicators.
- Error handling.

Verify live authenticated requests when credentials permit.

## Phase 6 — Voice agent

Deliver:

- Structured tool-calling.
- Session memory.
- Follow-up handling.
- Workspace updates.
- Evidence-linked explanations.
- Audio plan generation.

Verify the full speech → tool → data → sound → speech loop.

## Phase 7 — Product polish

Deliver:

- Responsive UI.
- Loading and error states.
- Accessibility basics.
- Consistent visual design.
- Improved playback UX.
- Demo reset.
- Documentation.

## Phase 8 — Final testing

Deliver:

- Passing backend tests.
- Passing frontend checks.
- Passing production build.
- Successful browser-level user journeys.
- Verified audio playback.
- Verified Gnani integration or clearly documented external blocker.
- Reproducible demonstration.

Do not skip verification to move to the next phase faster.

---

# 18. GOAL-DRIVEN CODEX EXECUTION

Your implementation process must be goal-driven.

Create these files:

- `GOALS.md`
- `PROGRESS.md`
- `DECISIONS.md`
- `TEST_RESULTS.md`

## GOALS.md

Create a list of measurable product and engineering acceptance criteria.

Every goal must include:

- Goal identifier.
- Expected behavior.
- Implementation status.
- Verification method.
- Evidence of completion.
- Any blocker.

## PROGRESS.md

Record:

- Current phase.
- Completed work.
- Pending work.
- Tests executed.
- Remaining failures.
- Next recommended action.

## DECISIONS.md

Record meaningful architectural decisions, particularly decisions that deviate from the PRD.

## TEST_RESULTS.md

Record:

- Test command.
- Execution outcome.
- Relevant failures.
- Evidence.
- Whether the issue was fixed.

## Required execution loop

Follow this loop throughout development:

1. Read the PRD and current goals.
2. Identify the highest-priority incomplete acceptance criterion.
3. Implement the smallest coherent functionality required.
4. Run relevant tests.
5. Inspect application behavior.
6. Diagnose failures.
7. Fix the implementation.
8. Rerun verification.
9. Record evidence.
10. Continue to the next criterion.

Do not interpret the completion of a coding phase as proof the product works.

Do not declare a goal complete without verification evidence.

Do not repeatedly rewrite the architecture instead of implementing working functionality.

Do not stop after creating the initial plan.

Continue through all feasible milestones within the current execution session.

If the execution session ends before completion, make the repository resumable through the progress files.

You cannot continue after the agent session ends unless the environment explicitly provides that capability. Do not claim otherwise.

---

# 19. DEFINITION OF DONE

The MVP is complete only when the following conditions are satisfied.

## A. Application

- [ ] Frontend runs on localhost.
- [ ] Backend runs on localhost.
- [ ] Frontend communicates with backend.
- [ ] SQLite persistence works.
- [ ] Project setup is documented.
- [ ] No committed secrets.

## B. Datasets

- [ ] Seeded energy dataset loads.
- [ ] Seeded telemetry dataset loads.
- [ ] CSV upload works.
- [ ] Data validation works.
- [ ] Timestamps and units are preserved.
- [ ] Dataset switching works.

## C. Analytics

- [ ] Descriptive statistics are numerically correct.
- [ ] Trend analysis works.
- [ ] Anomaly detection works.
- [ ] Period comparison works.
- [ ] Energy calculations respect units.
- [ ] Telemetry comparison works.
- [ ] Analytical evidence is available for every result.

## D. Sonification

- [ ] Trend mode generates actual audio.
- [ ] Anomaly mode generates actual audio.
- [ ] Comparison mode generates actual audio.
- [ ] Sound is derived deterministically from real dataset values.
- [ ] Chart cursor synchronizes with playback.
- [ ] Pause and stop work.
- [ ] Speed and volume controls work.
- [ ] Selected intervals can be replayed.
- [ ] Audio mappings are documented.
- [ ] Browser sound restrictions are handled.
- [ ] Voice and sonification do not overlap uncontrollably.

## E. Voice AI

- [ ] Gnani Prisma provider is implemented against official API documentation.
- [ ] Gnani Timbre provider is implemented against official API documentation.
- [ ] Microphone capture works.
- [ ] Transcribed text is displayed.
- [ ] Spoken explanations can be played.
- [ ] Voice errors are handled.
- [ ] Missing credentials are surfaced honestly.
- [ ] Live integration is verified if credentials are provided.

## F. Agent

- [ ] Agent can select the active dataset.
- [ ] Agent can select a metric.
- [ ] Agent can request trend analysis.
- [ ] Agent can request anomalies.
- [ ] Agent can compare periods.
- [ ] Agent can change sonification mode.
- [ ] Agent can change playback range.
- [ ] Agent can answer follow-up questions.
- [ ] Session context persists appropriately.
- [ ] Answers use actual analytical evidence.
- [ ] Agent cannot execute arbitrary code or shell commands.

## G. UI Quality

- [ ] Dashboard is visually polished.
- [ ] Navigation works.
- [ ] Charts display actual backend data.
- [ ] All visible primary controls function.
- [ ] Loading states exist.
- [ ] Error states exist.
- [ ] Audio controls are clear.
- [ ] Responsive layout is acceptable.
- [ ] The user can distinguish demo/fixture behavior from real inference.

## H. Testing

- [ ] Backend tests pass.
- [ ] Frontend type checks pass.
- [ ] Frontend build passes.
- [ ] Sonification tests pass.
- [ ] Agent tool tests pass.
- [ ] Browser end-to-end smoke tests pass.
- [ ] No blocking console errors remain.
- [ ] Test outcomes are recorded honestly.

## I. Final Demo

- [ ] One complete energy-analysis interaction works.
- [ ] One complete telemetry-analysis interaction works.
- [ ] Voice request changes the analytical operation.
- [ ] The sound changes based on the question.
- [ ] The chart reflects the selected data.
- [ ] The spoken answer matches the numerical evidence.
- [ ] A conversational follow-up works.
- [ ] The demo can be reset and repeated.

Do not mark any item complete based solely on code existing.

Verification must establish actual functionality.

---

# 20. DOCUMENTATION DELIVERABLES

Create:

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/API.md`
- `docs/SONIFICATION.md`
- `docs/GNANI_SETUP.md`
- `docs/DEMO.md`
- `GOALS.md`
- `PROGRESS.md`
- `DECISIONS.md`
- `TEST_RESULTS.md`

The README must include:

- What SonicLens does.
- Features.
- Architecture overview.
- Prerequisites.
- Environment variables.
- Local installation.
- Backend startup.
- Frontend startup.
- Gnani configuration.
- Sample datasets.
- Running tests.
- Demo instructions.
- Known limitations.

Provide commands that work in the actual implementation.

---

# 21. IMPORTANT ENGINEERING RULES

1. Do not invent Gnani API responses.
2. Do not fabricate performance metrics.
3. Do not fabricate user-study findings.
4. Do not claim sonification is universally better than visualization.
5. Do not claim the product is the first sonification platform.
6. Do not substitute text-to-speech for actual numerical sonification.
7. Do not generate audio unrelated to the selected metric.
8. Do not make the system ML-specific.
9. Do not build unnecessary infrastructure.
10. Do not silently expose credentials.
11. Do not execute arbitrary code generated by the LLM.
12. Do not leave primary buttons nonfunctional.
13. Do not display hardcoded dashboard metrics presented as live backend data.
14. Do not silently substitute fixture inference for real Gnani calls.
15. Do not mark a test as passing unless executed successfully.
16. Do not claim visual verification unless browser or screenshot inspection was actually performed.
17. Do not call a feature complete merely because it has an API route.
18. Do not leave disconnected frontend and backend implementations.
19. Do not overcomplicate the MVP with future adapters.
20. Do not ask the user routine implementation questions when a reasonable decision can be made independently.

---

# 22. FINAL HANDOFF

When all feasible implementation work is complete, provide:

### A. What was built

A concise breakdown of the working frontend, backend, analytics, sonification, voice agent, and integrations.

### B. Verification

List the exact tests and commands executed, together with their results.

### C. Live Gnani status

State whether authenticated Prisma and Timbre calls were actually verified.

If not, identify the precise reason.

### D. Definition of Done

Provide the number of passed, failed, and blocked acceptance criteria.

Do not mark externally blocked integration tests as passed.

### E. Local execution commands

Provide exact startup instructions.

### F. Demonstration instructions

Explain how to reproduce the complete 60-second challenge demo.

### G. Remaining limitations

Identify any incomplete features or known issues plainly.

---

# FINAL INSTRUCTION

Start now.

Inspect the repository, locate and read the SonicLens PRD, establish the goal tracker, and implement the application.

Work in functional vertical slices.

Run the application regularly.

Test actual user journeys.

Fix failures before moving on.

Prioritize the complete data → analytics → sonification → voice interaction loop over secondary features.

Your objective is not to maximize the amount of generated code.

**Your objective is to deliver a fully working, technically credible, visually polished SonicLens MVP whose behavior can be demonstrated and independently verified.**

Continue until every feasible Definition of Done item has evidence of completion, or an external dependency or execution limit prevents further progress.

