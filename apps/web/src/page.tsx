"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { AudioLines, Bolt, Check, ChevronDown, CircleHelp, Headphones, Mic, Pause, Play, Upload, Volume2, Waves } from "lucide-react";
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import type { Analysis, Dataset } from "./types";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
type Mode = "trend" | "anomaly" | "comparison";

async function capturePcm(onStart: () => void): Promise<{ audioBase64: string; sampleRate: number }> {
  if (!navigator.mediaDevices?.getUserMedia) throw new Error("This browser cannot access a microphone. Try the typed question option.");
  let stream: MediaStream | undefined;
  let context: AudioContext | undefined;
  let source: MediaStreamAudioSourceNode | undefined;
  let processor: ScriptProcessorNode | undefined;
  let silent: GainNode | undefined;
  try {
    stream = await navigator.mediaDevices.getUserMedia({ audio: { channelCount: 1, echoCancellation: true, noiseSuppression: true, autoGainControl: true } });
    context = new AudioContext({ sampleRate: 16000 });
    if (context.state === "suspended") await context.resume();
    source = context.createMediaStreamSource(stream);
    processor = context.createScriptProcessor(4096, 1, 1);
    silent = context.createGain();
    silent.gain.value = 0;
    source.connect(processor);
    processor.connect(silent);
    silent.connect(context.destination);
    const chunks: Float32Array[] = [];
    const startedAt = performance.now();
    let lastSpeechAt = startedAt;
    let detectedSpeech = false;
    onStart();
    await new Promise<void>(resolve => {
      const finish = () => { processor!.onaudioprocess = null; resolve(); };
      processor!.onaudioprocess = event => {
        const samples = event.inputBuffer.getChannelData(0);
        const copy = new Float32Array(samples);
        chunks.push(copy);
        let power = 0;
        for (let i = 0; i < samples.length; i += 4) power += samples[i] * samples[i];
        const rms = Math.sqrt(power / Math.ceil(samples.length / 4));
        const now = performance.now();
        if (rms > 0.012) { detectedSpeech = true; lastSpeechAt = now; }
        if ((detectedSpeech && now - lastSpeechAt > 900) || now - startedAt > 10_000 || (!detectedSpeech && now - startedAt > 5_000)) finish();
      };
    });
    if (!detectedSpeech) throw new Error("I didn’t catch any speech. Check your microphone and try again.");
    const sampleCount = chunks.reduce((sum, chunk) => sum + chunk.length, 0);
    const pcm = new Uint8Array(sampleCount * 2);
    let at = 0;
    for (const chunk of chunks) for (const sample of chunk) {
      const clamped = Math.max(-1, Math.min(1, sample));
      const value = clamped < 0 ? clamped * 32768 : clamped * 32767;
      pcm[at++] = value & 255;
      pcm[at++] = (value >> 8) & 255;
    }
    let binary = "";
    for (let i = 0; i < pcm.length; i += 0x8000) binary += String.fromCharCode(...pcm.subarray(i, Math.min(i + 0x8000, pcm.length)));
    return { audioBase64: btoa(binary), sampleRate: 16000 };
  } finally {
    processor?.disconnect();
    source?.disconnect();
    silent?.disconnect();
    stream?.getTracks().forEach(track => track.stop());
    if (context && context.state !== "closed") await context.close();
  }
}

export default function Home() {
  const [datasets, setDatasets] = useState<Dataset[]>([]), [activeId, setActiveId] = useState("energy-week"), [metric, setMetric] = useState("usage_kwh");
  const [mode, setMode] = useState<Mode>("trend"), [analysis, setAnalysis] = useState<Analysis | null>(null), [error, setError] = useState(""), [loading, setLoading] = useState(true);
  const [playing, setPlaying] = useState(false), [paused, setPaused] = useState(false), [cursor, setCursor] = useState(-1), [speed, setSpeed] = useState(1), [volume, setVolume] = useState(.45), [rangeStart, setRangeStart] = useState(0), [rangeEnd, setRangeEnd] = useState(100);
  const [question, setQuestion] = useState(""), [answer, setAnswer] = useState(""), [clarification, setClarification] = useState<string[]>([]), [sessionId, setSessionId] = useState(""), [tariff, setTariff] = useState(8), [voiceConfigured, setVoiceConfigured] = useState(false), [recording, setRecording] = useState(false), [processingVoice, setProcessingVoice] = useState(false), [transcript, setTranscript] = useState(""), [speechUrl, setSpeechUrl] = useState(""), [showTypedQuestion, setShowTypedQuestion] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null), timerRef = useRef<ReturnType<typeof setInterval> | null>(null), audioRef = useRef<AudioContext | null>(null), gainRef = useRef<GainNode | null>(null), spokenAudioRef = useRef<HTMLAudioElement | null>(null);
  const dataset = datasets.find(d => d.id === activeId);
  const selectDataset = (id: string) => { const next = datasets.find(item => item.id === id); if (next) setMetric(next.metrics[0]); setActiveId(id); };
  const loadDatasets = useCallback(async () => { try { const [r, h] = await Promise.all([fetch(`${API}/api/datasets`), fetch(`${API}/api/health`)]); if (!r.ok) throw new Error("API unavailable"); const list: Dataset[] = await r.json(), health=await h.json(); setVoiceConfigured(Boolean(health.voice?.configured)); setDatasets(list); if (!list.some(d => d.id === activeId)) setActiveId(list[0]?.id ?? ""); } catch { setError("Start the API to load the demonstration datasets."); } finally { setLoading(false); } }, [activeId]);
  useEffect(() => { void loadDatasets(); }, [loadDatasets]);
  useEffect(() => { if (!dataset) return; setMetric(dataset.metrics[0]); setAnalysis(null); setAnswer(""); setSessionId(""); setCursor(-1); setPlaying(false); setRangeStart(0); setRangeEnd(dataset.samples.length); }, [activeId, dataset]);
  useEffect(() => { if (!dataset || !metric) return; let cancelled = false; void fetch(`${API}/api/sessions?dataset_id=${encodeURIComponent(dataset.id)}&metric=${encodeURIComponent(metric)}`, { method: "POST" }).then(r => r.json()).then(s => { if (!cancelled) setSessionId(s.id); }).catch(() => undefined); return () => { cancelled = true; }; }, [dataset?.id, metric]);
  const runAnalysis = useCallback(async (nextMode = mode, end = rangeEnd) => { if (!dataset) return; setError(""); try { const r = await fetch(`${API}/api/analysis`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ dataset_id: dataset.id, metric, mode: nextMode, start: rangeStart, end, tariff }) }); const body = await r.json(); if (!r.ok) throw new Error(body.detail ?? "Analysis failed"); setAnalysis(body); } catch (e) { setError(e instanceof Error ? e.message : "Analysis failed"); } }, [dataset, metric, mode, rangeStart, rangeEnd, tariff]);
  useEffect(() => { void runAnalysis(); }, [runAnalysis]);
  useEffect(() => { if (!dataset || typeof window === "undefined") return; const ctx = new AudioContext(); const gain = ctx.createGain(); gain.gain.value = volume; gain.connect(ctx.destination); audioRef.current = ctx; gainRef.current = gain; return () => { void ctx.close(); }; }, [dataset?.id]);
  useEffect(() => { if (gainRef.current) gainRef.current.gain.value = volume; }, [volume]);
  useEffect(() => () => { spokenAudioRef.current?.pause(); if (speechUrl) URL.revokeObjectURL(speechUrl); }, [speechUrl]);
  const sound = useCallback((index: number) => { if (!dataset || volume <= 0) return; const sample = dataset.samples[index], value = sample?.values[metric]; const ctx = audioRef.current; if (value === undefined || !ctx || !gainRef.current) return; if (ctx.state === "suspended") void ctx.resume(); const values = dataset.samples.map(s => s.values[metric]).filter(Number.isFinite); const lo = Math.min(...values), hi = Math.max(...values); const osc = ctx.createOscillator(), env = ctx.createGain(); osc.type = mode === "anomaly" ? "triangle" : "sine"; let pitch = hi === lo ? .5 : (value-lo)/(hi-lo); if (mode === "comparison" && analysis?.comparison) { const pair = analysis.comparison.pairs.find(item => item.index_a === index || item.index_b === index); if (pair) { const span = Math.max(...analysis.comparison.pairs.map(item => Math.abs(item.delta)), 1e-9); pitch = .5 + .5 * pair.delta / span; osc.type = "triangle"; } } osc.frequency.value = 180 + pitch*760; env.gain.setValueAtTime(0.0001, ctx.currentTime); env.gain.exponentialRampToValueAtTime(volume*.13, ctx.currentTime+.025); env.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime+.14); osc.connect(env); env.connect(gainRef.current); osc.start(); osc.stop(ctx.currentTime+.15); osc.onended = () => { osc.disconnect(); env.disconnect(); }; }, [dataset, metric, mode, volume, analysis]);
  const stop = useCallback(() => { if (timerRef.current) clearInterval(timerRef.current); timerRef.current = null; setPlaying(false); setPaused(false); setCursor(-1); }, []);
  const playbackRef = useRef<{indices:number[];position:number}>({indices:[],position:0});
  const pause = useCallback(() => { setPlaying(false); setPaused(true); }, []);
  const play = useCallback(() => { if (!dataset) return; if(!paused || !playbackRef.current.indices.length){let indices=analysis?.plan.events.map(event=>event.index).filter(index=>index>=rangeStart&&index<rangeEnd)??Array.from({length:rangeEnd-rangeStart},(_,i)=>rangeStart+i); if (mode === "comparison" && analysis?.comparison) indices = [...new Set(analysis.comparison.pairs.flatMap(pair=>[pair.index_a,pair.index_b]))].filter(index=>index>=rangeStart&&index<rangeEnd); if(!indices.length)return; if(indices.length>150) indices=Array.from({length:150},(_,i)=>indices[Math.round(i*(indices.length-1)/149)]); playbackRef.current={indices,position:-1};}setPaused(false);setPlaying(true); }, [analysis,dataset,paused,rangeStart,rangeEnd,mode]);
  useEffect(() => { if(!playing||paused)return; const state=playbackRef.current; if(state.position<0){state.position=0;const first=state.indices[0];setCursor(first);sound(first);} timerRef.current=setInterval(()=>{state.position+=1;if(state.position>=state.indices.length){if(timerRef.current)clearInterval(timerRef.current);timerRef.current=null;setPlaying(false);setPaused(false);return;}const index=state.indices[state.position];setCursor(index);sound(index);},210/speed);return()=>{if(timerRef.current)clearInterval(timerRef.current);timerRef.current=null;}; }, [playing,paused,speed,sound]);
  useEffect(() => () => { if (timerRef.current) clearInterval(timerRef.current); }, []);
  const chartData = useMemo(() => (dataset?.samples.slice(rangeStart, rangeEnd) ?? []).map((s, offset) => { const i=rangeStart+offset; return { index: i, time: new Date(s.timestamp).toLocaleString([], { weekday: "short", hour: "2-digit", minute: "2-digit" }), value: s.values[metric], focus: analysis?.focus_indices.includes(i) ?? false, cursor: i === cursor }; }), [dataset, rangeStart, rangeEnd, metric, analysis, cursor]);
  const updateFocus = async (end: number) => { setRangeStart(0); setRangeEnd(end); if (dataset && sessionId) { try { const r = await fetch(`${API}/api/sessions/${sessionId}/focus`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ start: 0, end, metric }) }); if (!r.ok) throw new Error("Could not update selected range"); } catch (e) { setError(e instanceof Error ? e.message : "Could not update focus"); } } };
  const askQuestion = async (text = question) => { if (!dataset || !sessionId || !text.trim()) return; setError(""); setClarification([]); try { const r = await fetch(`${API}/api/voice/query`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ session_id: sessionId, dataset_id: dataset.id, metric, text, tariff }) }); const body = await r.json(); if (!r.ok) throw new Error(body.detail ?? "Could not analyze that request"); setSessionId(body.session.id); setQuestion(text); if(body.clarification?.needed){setClarification(body.clarification.choices);setAnswer(body.answer);return;} setAnalysis(body.analysis); setMode(body.analysis.mode); setAnswer(body.answer); setSpeed(body.session.playback_speed); setRangeStart(body.analysis.range.start); setRangeEnd(body.analysis.range.end); } catch (e) { setError(e instanceof Error ? e.message : "Query failed"); } };
  const askByVoice = async () => {
    if (!dataset || !sessionId || !voiceConfigured || recording || processingVoice) return;
    setError(""); setTranscript(""); setAnswer(""); setSpeechUrl(""); setRecording(true); stop(); spokenAudioRef.current?.pause();
    try {
      const captured = await capturePcm(() => { setRecording(false); setProcessingVoice(true); });
      const response = await fetch(`${API}/api/voice/speak`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ session_id: sessionId, dataset_id: dataset.id, metric, audio_base64: captured.audioBase64, sample_rate: captured.sampleRate, language_code: "indic-auto", tariff }) });
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail ?? "Voice analysis failed");
      setSessionId(body.session.id); setAnalysis(body.analysis); setMode(body.analysis.mode); setAnswer(body.answer); setTranscript(body.transcript); setQuestion(body.transcript); setRangeStart(body.analysis.range.start); setRangeEnd(body.analysis.range.end);
      const binary = atob(body.audio_base64), bytes = Uint8Array.from(binary, character => character.charCodeAt(0));
      const url = URL.createObjectURL(new Blob([bytes], { type: "audio/wav" }));
      setSpeechUrl(url);
      const spoken = new Audio(url); spokenAudioRef.current = spoken;
      try { await spoken.play(); } catch { /* Keep the replay button available if autoplay is blocked. */ }
    } catch (e) { setError(e instanceof Error ? e.message : "Voice request failed"); }
    finally { setRecording(false); setProcessingVoice(false); }
  };
  const replayAnswer = async () => { if (!speechUrl) return; const spoken = new Audio(speechUrl); spokenAudioRef.current = spoken; try { await spoken.play(); } catch { setError("Your browser blocked audio. Use the play control in the response card."); } };
  const handleUpload = async (file?: File) => { if (!file) return; const form = new FormData(); form.append("file", file); try { const r = await fetch(`${API}/api/datasets/import`, { method: "POST", body: form }); const body = await r.json(); if (!r.ok) throw new Error(body.detail ?? "Upload failed"); setMetric(body.metrics[0]); setActiveId(body.id); await loadDatasets(); setError(""); } catch (e) { setError(e instanceof Error ? e.message : "Upload failed"); } finally { if (fileRef.current) fileRef.current.value = ""; } };
  const changeMetricUnit = async (unit:string,samplingKind?:string) => { if(!dataset) return; const response=await fetch(`${API}/api/datasets/${dataset.id}/metrics/${encodeURIComponent(metric)}/unit`,{method:"PATCH",headers:{"Content-Type":"application/json"},body:JSON.stringify({unit,...(samplingKind?{sampling_kind:samplingKind}:{})})}); if(!response.ok){setError("Could not save metric unit.");return;} const refreshed=await fetch(`${API}/api/datasets/${dataset.id}`); const updated:Dataset=await refreshed.json(); setDatasets(current=>current.map(item=>item.id===updated.id?updated:item)); };
  const restoreAnalysis = async (id:string) => { try { const response=await fetch(`${API}/api/analysis/${encodeURIComponent(id)}`), saved=await response.json(); if(!response.ok) throw new Error(saved.detail??"Evidence was not found"); setAnalysis(saved); setMode(saved.mode); setRangeStart(saved.range.start); setRangeEnd(saved.range.end); setAnswer(`Restored saved analysis ${saved.analysis_id}.`); } catch(e){setError(e instanceof Error?e.message:"Could not restore evidence");} };
  const recent = dataset?.samples.at(-1);
  if (loading) return <main className="loading"><Waves size={22}/> Opening your energy workspace…</main>;
  const isEnergy = dataset?.domain === "energy";
  const spokenPeriod = dataset?.samples.length ? `${new Date(dataset.samples[0].timestamp).toLocaleDateString([], {month:"short",day:"numeric"})} — ${new Date(dataset.samples.at(-1)!.timestamp).toLocaleDateString([], {month:"short",day:"numeric"})}` : "No readings";

  return (
    <main className="app-shell">
      <header className="site-header">
        <a className="brand" href="#home" aria-label="SonicLens home"><span className="brand-mark"><Waves size={19}/></span><span>SonicLens</span></a>
        <label className="workspace-picker"><span>YOUR WORKSPACE</span><select aria-label="Dataset" value={activeId} onChange={event => selectDataset(event.target.value)}>{datasets.map(item => <option key={item.id} value={item.id}>{item.domain === "energy" ? "Home energy · 7 days" : item.name}</option>)}</select><ChevronDown size={14}/></label>
        <div className="header-actions"><span className={`connection-status ${voiceConfigured ? "connected" : "disconnected"}`}><i/>{voiceConfigured ? "VOICE READY" : "VOICE SETUP NEEDED"}</span><button className="quiet-button" onClick={async () => { await fetch(`${API}/api/demo/reset`, {method:"POST"}); await loadDatasets(); selectDataset("energy-week"); setQuestion(""); setAnswer(""); setTranscript(""); setError(""); }}>Reset demo</button><button className="upload-button" onClick={() => fileRef.current?.click()} aria-label="Import a CSV"><Upload size={16}/><span>Import</span></button></div>
        <input ref={fileRef} hidden type="file" accept=".csv,text/csv" onChange={event => void handleUpload(event.target.files?.[0])}/>
      </header>

      <div className="workspace" id="home">
        <section className="page-intro"><div><p className="eyebrow">HOUSEHOLD ENERGY · WEEKLY REVIEW</p><h1>Know what your home is using.</h1><p>Ask a question. Hear a grounded answer. See the readings behind it.</p></div><div className="period-note"><span className="period-dot"/><span>{spokenPeriod}</span><span className="period-divider">·</span><span>{dataset?.source === "Synthetic demonstration data" ? "Example household" : dataset?.name}</span></div></section>
        {error && <div className="error-banner" role="alert"><CircleHelp size={16}/><span>{error}</span></div>}

        <section className="voice-layout" aria-label="Voice-first household energy analysis">
          <div className="voice-card">
            <div className="voice-card-header"><span className="voice-label"><AudioLines size={16}/> YOUR ENERGY ASSISTANT</span><span className={`voice-live ${voiceConfigured ? "" : "offline"}`}><i/>{voiceConfigured ? "Gnani voice" : "Voice unavailable"}</span></div>
            <div className="voice-main">
              <div className="voice-prompt"><h2>What would you like to know?</h2><p>Ask about a spike, compare days, or estimate your bill. Answers are calculated from your readings and tariff.</p><div className="suggested-questions"><span>TRY SAYING</span><p>“When did I use the most electricity?”</p><p>“Compare usage with yesterday.”</p></div><button className="typed-toggle" onClick={() => setShowTypedQuestion(value => !value)}>{showTypedQuestion ? "Close typed question" : "Prefer to type?"}</button></div>
              <div className="record-column"><button className={`record-button ${recording ? "is-recording" : ""} ${processingVoice ? "is-processing" : ""}`} disabled={!voiceConfigured || recording || processingVoice} onClick={() => void askByVoice()} aria-label={recording ? "Recording, speak now" : processingVoice ? "Analyzing your question" : "Ask a voice question"}>{processingVoice ? <AudioLines size={26}/> : recording ? <AudioLines size={27}/> : <Mic size={28}/>}</button><strong>{recording ? "Listening" : processingVoice ? "Finding your answer" : voiceConfigured ? "Tap to ask" : "Set up voice"}</strong><span>{recording ? "Speak naturally. I’ll stop after your pause." : processingVoice ? "Transcribing and checking your readings…" : voiceConfigured ? "One tap · no need to hold" : "Add your Gnani key to the local .env"}</span></div>
            </div>
            {showTypedQuestion && <form className="typed-question" onSubmit={event => { event.preventDefault(); void askQuestion(); }}><label htmlFor="typed-question">Ask by text</label><div><input id="typed-question" value={question} onChange={event => setQuestion(event.target.value)} placeholder="Find unusual evening spikes"/><button type="submit" disabled={!sessionId || !question.trim()}>Ask <span>→</span></button></div></form>}
            {(transcript || answer) && <section className="voice-result" aria-live="polite" aria-label="Voice answer"><div className="transcript-row"><span className="result-label">{transcript ? "YOU ASKED" : "YOUR QUESTION"}</span><p>“{transcript || question}”</p></div><div className="answer-row"><div className="answer-avatar"><Waves size={15}/></div><div className="answer-copy"><span className="result-label">SONICLENS · GROUNDED ANSWER</span><p>{answer}</p></div>{speechUrl && <button className="listen-again" onClick={() => void replayAnswer()} aria-label="Listen to the spoken answer"><Play size={15} fill="currentColor"/><span>Listen</span></button>}</div>{analysis && <div className="result-foot"><span><Check size={13}/> Based on {analysis.summary.count} readings</span><span>Evidence {analysis.analysis_id}</span><button onClick={() => void play()} disabled={!analysis.plan.events.length}>Hear this pattern <Play size={12} fill="currentColor"/></button></div>}{clarification.length > 0 && <div className="clarification-options">{clarification.map(choice => <button key={choice} onClick={() => { setQuestion(choice); setShowTypedQuestion(true); }}>{choice}</button>)}</div>}</section>}
          </div>

          <aside className="week-card"><div className="week-card-heading"><span className="eyebrow">AT A GLANCE</span><Bolt size={18}/></div><h2>{isEnergy ? "This week" : "Selected period"}</h2><div className="week-stat"><span>Average use</span><strong>{analysis?.summary.mean.toLocaleString(undefined,{maximumFractionDigits:2}) ?? "—"}<small> {analysis?.summary.unit ?? "kWh"} / interval</small></strong></div><div className="week-stat"><span>Highest reading</span><strong>{analysis?.summary.max.toLocaleString(undefined,{maximumFractionDigits:2}) ?? "—"}<small> {analysis?.summary.unit ?? "kWh"}</small></strong></div><div className="week-stat cost-stat"><label htmlFor="tariff">Estimated energy cost</label><strong>{!isEnergy && dataset?.domain !== "csv" ? "Energy data only" : analysis?.summary.energy_cost == null ? "Confirm kWh units" : `₹${analysis.summary.energy_cost.toFixed(2)}`}</strong>{(isEnergy || dataset?.domain === "csv") && <div className="tariff-field"><span>Tariff</span><input id="tariff" aria-label="Tariff per kWh" type="number" min="0" step=".5" value={tariff} onChange={event => setTariff(Number(event.target.value))}/><span>₹/kWh</span></div>}</div>{dataset?.domain === "csv" && <details className="csv-settings"><summary>Confirm imported data units</summary><label>Metric unit<input aria-label="Metric unit" value={dataset.metric_units?.[metric] ?? "unspecified"} onChange={event => setDatasets(items => items.map(item => item.id === dataset.id ? {...item,metric_units:{...item.metric_units,[metric]:event.target.value}} : item))} onBlur={event => void changeMetricUnit(event.target.value,dataset.sampling_kind)}/></label><label>Readings represent<select aria-label="Sampling kind" value={dataset.sampling_kind ?? "unknown"} onChange={event => void changeMetricUnit(dataset.metric_units?.[metric] ?? "unspecified",event.target.value)}><option value="unknown">Unconfirmed</option><option value="interval_energy">Interval energy</option><option value="power_sample">Power samples</option><option value="sampled">Other sampled metric</option></select></label></details>}<p className="week-footnote">{dataset?.source === "Synthetic demonstration data" ? "Example data · not a live meter" : "Imported readings · confirm units before cost estimates"}</p></aside>
        </section>

        <section className="analysis-layout">
          <section className="chart-card" aria-labelledby="usage-title"><header className="chart-header"><div><p className="eyebrow">YOUR READINGS</p><h2 id="usage-title">{isEnergy ? "Electricity use" : metric.replaceAll("_"," ")} <span>over time</span></h2><p id="chart-description" className="chart-description">{dataset?.name}: {analysis?.summary.count ?? 0} readings. Average {analysis?.summary.mean ?? "—"} {analysis?.summary.unit ?? ""}; highest {analysis?.summary.max ?? "—"} {analysis?.summary.unit ?? ""}. Exact source values are listed below.</p></div><div className="analysis-modes" aria-label="Analysis view">{(["trend","anomaly","comparison"] as Mode[]).map(item => <button key={item} className={mode === item ? "active" : ""} onClick={() => { setMode(item); void runAnalysis(item); }}>{item === "trend" ? "All readings" : item === "anomaly" ? "Spikes" : "Compare"}</button>)}</div></header>
            <div className="chart-wrap" role="img" aria-describedby="chart-description" aria-label={`${metric.replaceAll("_"," ")} chart for ${dataset?.name}; ${chartData.length} readings`}><ResponsiveContainer width="100%" height="100%"><AreaChart data={chartData} margin={{top:12,right:14,left:-18,bottom:0}}><defs><linearGradient id="energy-fill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#668c69" stopOpacity={.24}/><stop offset="95%" stopColor="#668c69" stopOpacity={0}/></linearGradient></defs><CartesianGrid stroke="#e8e5dc" vertical={false}/><XAxis dataKey="time" tick={{fill:"#777a70",fontSize:10}} axisLine={false} tickLine={false} minTickGap={54}/><YAxis tick={{fill:"#777a70",fontSize:10}} axisLine={false} tickLine={false} width={48}/><Tooltip contentStyle={{background:"#fffdf8",border:"1px solid #ddd9ce",borderRadius:8,color:"#24352d"}}/><Area type="monotone" dataKey="value" stroke="#527c5b" strokeWidth={2.4} fill="url(#energy-fill)" dot={(props: {cx?:number;cy?:number;payload?:{focus?:boolean;cursor?:boolean}}) => props.payload?.focus || props.payload?.cursor ? <circle key={`reading-${props.cx}-${props.cy}`} cx={props.cx} cy={props.cy} r={props.payload.cursor ? 5 : 3.5} fill={props.payload.cursor ? "#c55e42" : "#d5a04e"} stroke="#fffdf8" strokeWidth={2}/> : <></>} activeDot={{r:4,fill:"#d5a04e",stroke:"#fffdf8"}}/></AreaChart></ResponsiveContainer></div>
            <div className="chart-controls"><label htmlFor="time-range">SHOW RANGE</label><input id="time-range" aria-label="Time range end" type="range" min="8" max={dataset?.samples.length ?? 168} value={rangeEnd} onChange={event => void updateFocus(Number(event.target.value))}/><span>{rangeEnd} / {dataset?.samples.length ?? 0}</span></div><div className="chart-legend"><span><i/> {metric.replaceAll("_"," ")} · {analysis?.summary.unit ?? dataset?.unit}</span><span className="legend-spike"><i/> Unusual reading</span></div>
          </section>
          <aside className="listen-card"><div className="listen-heading"><span className="eyebrow">AUDIO REVIEW</span><Headphones size={17}/></div><h2>Hear the readings</h2><p>{mode === "trend" ? "A note for each reading; pitch follows electricity use." : mode === "anomaly" ? "Listen to the unusual readings in your data." : "Compare aligned readings from two periods."}</p><div className="player-main"><button className={`play-button ${playing ? "is-playing" : ""}`} onClick={playing ? pause : play} aria-label={playing ? "Pause playback" : paused ? "Resume playback" : "Play sonification"}>{playing ? <Pause size={18} fill="currentColor"/> : <Play size={18} fill="currentColor"/>}</button><div className="timeline"><div className="timeline-track"><div className="timeline-progress" style={{width:`${Math.max(0,(cursor+1)/(rangeEnd||1)*100)}%`}}/></div><div className="timeline-labels"><span>{cursor >= 0 && dataset ? new Date(dataset.samples[cursor]?.timestamp ?? "").toLocaleTimeString([], {hour:"2-digit",minute:"2-digit"}) : paused ? "Paused" : "Ready"}</span><span>{dataset?.samples[rangeEnd-1] ? new Date(dataset.samples[rangeEnd-1].timestamp).toLocaleTimeString([], {hour:"2-digit",minute:"2-digit"}) : "—"}</span></div></div><button className="stop-button" onClick={stop} disabled={!playing && !paused} aria-label="Stop playback">Stop</button></div><div className="listen-options"><label>Speed<select aria-label="Playback speed" value={speed} onChange={event => setSpeed(Number(event.target.value))}><option value="0.5">0.5×</option><option value="1">1×</option><option value="1.5">1.5×</option><option value="2">2×</option></select></label><label className="listen-volume"><Volume2 size={15}/><input aria-label="Volume" type="range" min="0" max="1" step=".01" value={volume} onChange={event => setVolume(Number(event.target.value))}/></label></div></aside>
        </section>

        <section className="evidence-card"><header className="evidence-heading"><div><p className="eyebrow">SHOW YOUR WORK</p><h2>Readings behind this analysis</h2><p>{analysis?.analysis_id ?? "Analysis is loading"} · Calculated from the selected dataset</p></div>{analysis && <button className="restore-evidence" onClick={() => void restoreAnalysis(analysis.analysis_id)}>Reload saved analysis</button>}</header>{analysis?.comparison && <p className="evidence-summary">The second period differed by {analysis.comparison.mean_difference} {analysis.comparison.unit} across {analysis.comparison.aligned_points} aligned readings.</p>}<div className="evidence-metrics"><span><strong>{analysis?.summary.count ?? 0}</strong> readings analyzed</span><span><strong>{analysis?.summary.min ?? "—"}–{analysis?.summary.max ?? "—"}</strong> observed range · {analysis?.summary.unit ?? ""}{analysis?.summary.missing_count ? ` · ${analysis.summary.missing_count} missing` : ""}</span><span><strong>{analysis?.events.length ?? 0}</strong> unusual readings</span></div>{analysis?.evidence?.length ? <details className="evidence-table"><summary>Inspect timestamps and values ({analysis.evidence.length})</summary><div className="table-scroll"><table><caption>Source readings used for this answer</caption><thead><tr><th scope="col">Reading</th><th scope="col">Timestamp (UTC)</th><th scope="col">{metric.replaceAll("_"," ")} · {analysis.summary.unit}</th></tr></thead><tbody>{analysis.evidence.map((row,offset) => { const index = analysis.range.start + offset; return <tr key={`${row.timestamp}-${index}`}><th scope="row">{index+1}</th><td>{new Date(row.timestamp).toISOString()}</td><td>{row.values[metric] ?? "Missing"}</td></tr>; })}</tbody></table></div></details> : <p className="evidence-empty">Choose an analysis to inspect its source readings.</p>}</section>
        <footer className="site-footer"><span>Voice-led household energy review</span><span>Example data is synthetic. SonicLens is not connected to a physical meter.</span><a href={`${API}/docs`} target="_blank" rel="noreferrer">API details</a></footer>
      </div>
    </main>
  );
}
