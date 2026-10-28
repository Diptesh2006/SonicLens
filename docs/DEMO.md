# Current demo walkthrough

1. Start FastAPI and Next.js using the README commands; use **Reset demo** to restore the deterministic state.
2. Open the Energy Explorer and inspect the synthetic provenance label and chart description.
3. Press Play to hear the energy trend; switch to Anomalies and press Play again.
4. Adjust the selected observation range, playback rate and volume.
5. Switch to API telemetry, choose latency or errors, and replay.
6. Upload a CSV with ISO timestamps and numeric columns.
7. Ask “Find unusual spikes” or “Compare the periods”; inspect the deterministic answer, analysis ID, aligned evidence and expandable timestamped source-observation table. Comparison playback sonifies paired signed differences.
8. For imported CSV files, set the unit and sampling semantics explicitly. Energy cost remains unavailable for unconfirmed units or power samples.

The built-in audio preview schedules no more than 150 evenly spaced observations per play action; summaries and source evidence continue to use every selected observation. Set volume to zero for silence. Spoken audio stops the sonification player before narration begins.

The microphone flow requires `GNANI_API_KEY` in the API server environment. Without it, the UI labels the provider unconfigured and keeps microphone capture disabled; text prompts use deterministic local analysis tools.
