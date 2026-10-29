#!/usr/bin/env python3
"""Genera docs/fingerprints.html: las huellas de todos los estilos de drum_styles_v/.

  python3 tools/view_styles.py

Cada estilo es una tira de 9 mapas de calor (p0-p8, 7 voces x 32 pasos), agrupada
por familia segun la tabla "Included styles" del README. La salida es determinista:
check_styles.py la compara con render() para saber si esta al dia.
"""
import glob
import json
import os
import re
import sys

from make_style import PATTERNS, ROOT, VOICES, StyleError, from_txt

OUT = os.path.join(ROOT, 'docs', 'fingerprints.html')


def families():
    # filas "| Familia | NOMBRE (bpm), ... |" de la tabla bajo "## Included styles"
    text = open(os.path.join(ROOT, 'README.md'), encoding='utf-8').read()
    section = text.split('## Included styles', 1)[-1].split('\n## ', 1)[0]
    table = []
    for line in section.splitlines():
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) != 2 or cells[0] in ('Family', '') or set(cells[0]) <= set('-'):
            continue
        entries = [re.match(r'^(.*?)(?: \((\d+)\))?$', e.strip()).groups()
                   for e in cells[1].split(',') if e.strip()]
        table.append((cells[0], entries))
    return table


def grooves():
    # receta de groove de la cabecera de cada fuente: nombre -> (swing, amount por voz)
    alias = {'kick': 0, 'snare': 1, 'clap': 2, 'hhc': 3, 'hho': 4, 'hitom': 5, 'lotom': 6}
    out = {}
    for path in glob.glob(os.path.join(ROOT, 'styles_src', '*.style')):
        text = open(path, encoding='utf-8').read()
        name = re.search(r'^name:\s*(.+?)\s*$', text, re.M)
        groove = re.search(r'^#\s*Groove:(.*)$', text, re.M)
        if not name or not groove:
            continue
        sw = re.search(r'swing(?: global)? (\d{2})', groove.group(1))
        amt = re.search(r'amount:([^·]*)', groove.group(1))
        pairs = dict(re.findall(r'(kick|snare|clap|hhc|hho|hitom|lotom|resto) (\d+)', amt.group(1))) if amt else {}
        rest = int(pairs.get('resto', 100))
        out[name.group(1)] = (int(sw.group(1)) if sw else 50,
                              [int(pairs[v]) if v in pairs else rest for v in alias],
                              os.path.basename(path)[:-6])
    return out


def bpm_of(name, readme_bpm):
    # BPM del preview: numero final del nombre (60-220) -> (bpm) de su entrada del README -> 120
    m = re.search(r'(\d{2,3})$', name)
    if m and 60 <= int(m.group(1)) <= 220:
        return int(m.group(1))
    return readme_bpm or 120


def render():
    styles = {}
    for path in sorted(glob.glob(os.path.join(ROOT, 'drum_styles_v', '*.txt'))):
        name = os.path.basename(path)[:-4]
        try:
            data = from_txt(open(path, encoding='utf-8', newline='').read())
        except StyleError as e:
            raise StyleError(f'{name}.txt: {e}')
        # un patron = 7 voces x 32 pasos en hex (2 caracteres por paso)
        styles[name] = [''.join(f'{v:02x}' for vi in range(len(VOICES)) for v in data[vi][p])
                        for p in range(PATTERNS)]
    groups, used, tempo = [], set(), {}
    for family, entries in families():
        names = []
        for base, bpm in entries:
            for n in styles:
                if n not in used and (n == base or (bpm and n == f'{base} {bpm}')):
                    names.append(n); used.add(n); tempo[n] = int(bpm) if bpm else None
        groups.append([family, names])
    rest = [n for n in styles if n not in used]
    other = next((g for g in groups if g[0] == 'Other'), None)
    if other is None and rest:
        other = ['Other', []]
        groups.append(other)
    if rest:
        other[1] += rest
    groove = grooves()
    page = [{'family': f, 'styles': [{'name': n, 'bpm': bpm_of(n, tempo.get(n)),
                                      'swing': groove.get(n, (50, None, None))[0], 'amt': groove.get(n, (50, None, None))[1],
                                      'src': groove.get(n, (50, None, None))[2],
                                      'p': styles[n]} for n in names]}
            for f, names in groups if names]
    payload = json.dumps({'voices': VOICES, 'groups': page}, ensure_ascii=False,
                         separators=(',', ':')).replace('</', '<\\/')
    return TEMPLATE.replace('/*DATA*/', payload)


TEMPLATE = '''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GenderBender Fingerprints</title>
<style>
:root{--bg:#f6f4ef;--fg:#1d1b18;--muted:#6b665d;--cell:#ebe7de;--ink:#c2410c;--line:#d6d0c3}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#15130f;--fg:#ece7dc;--muted:#9a9384;--cell:#24211b;--ink:#fb923c;--line:#3a352c}}
:root[data-theme="dark"]{--bg:#15130f;--fg:#ece7dc;--muted:#9a9384;--cell:#24211b;--ink:#fb923c;--line:#3a352c}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.4 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
header{position:sticky;top:0;z-index:2;background:var(--bg);border-bottom:1px solid var(--line);padding:12px 16px;display:flex;flex-wrap:wrap;gap:8px 24px;align-items:center}
h1{font-size:16px;margin:0;letter-spacing:.08em}
label{display:flex;gap:8px;align-items:center;color:var(--muted)}
input[type=range]{width:180px;accent-color:var(--ink)}
select{font:inherit;color:var(--fg);background:var(--cell);border:1px solid var(--line);border-radius:4px;padding:2px 4px}
output{color:var(--fg);min-width:3ch}
main{padding:8px 16px 48px;max-width:1100px;margin:0 auto}
h2{font-size:13px;color:var(--muted);text-transform:uppercase;letter-spacing:.12em;margin:28px 0 8px;border-bottom:1px solid var(--line);padding-bottom:4px}
.style{padding:6px;margin:0 -6px 6px;border-radius:6px;cursor:pointer}
.style:hover,.style:focus-visible{background:var(--cell);outline:none}
.style:focus-visible{box-shadow:0 0 0 2px var(--ink)}
.name{font-size:13px;margin-bottom:4px}
.strip{display:flex;flex-wrap:wrap;gap:4px}
.pat{position:relative}
.pat canvas{display:block;image-rendering:pixelated}
.empty::after{content:"FILL vacío";position:absolute;inset:0;display:grid;place-items:center;font-size:10px;color:var(--muted);border:1px dashed var(--line)}
dialog{background:var(--bg);color:var(--fg);border:1px solid var(--line);border-radius:8px;padding:16px;max-width:calc(100vw - 32px);max-height:calc(100vh - 32px)}
dialog::backdrop{background:rgba(0,0,0,.3)}
dialog h3{margin:0 0 12px;font-size:15px}
.big{display:flex;flex-wrap:wrap;gap:12px 20px}
.big figure{margin:0}
.big figcaption{color:var(--muted);font-size:12px;margin-bottom:2px}
.big .row{display:flex;gap:6px}
.big .voices{display:flex;flex-direction:column;justify-content:space-around;font-size:10px;color:var(--muted);text-align:right}
.big canvas{max-width:calc(100vw - 120px);height:auto}
.hint{color:var(--muted);font-size:12px;margin:12px 0 0}
.src{color:var(--ink);font-size:12px;text-decoration:none}
.src:hover,.src:focus-visible{text-decoration:underline}
.play{font:inherit;font-size:12px;color:var(--fg);background:var(--cell);border:1px solid var(--line);border-radius:4px;padding:0 6px;margin-left:8px;cursor:pointer}
.play:hover,.play:focus-visible{border-color:var(--ink);outline:none}
.bpm{color:var(--muted);font-size:12px;margin-left:8px}
.playing{outline:2px solid var(--ink);outline-offset:1px}
.knob{position:relative}
.big .row{position:relative}
.cursor{position:absolute;background:var(--ink);opacity:.25;pointer-events:none}
.voices span{transition:color .15s}
.voices span.hit{color:var(--ink);transition:none}
.vis{display:none;width:100%;cursor:pointer}
.vis.on{display:block}
#zvis{height:64px;margin:0 0 12px}
#visbar{position:fixed;left:0;right:0;bottom:0;background:var(--bg);border-top:1px solid var(--line);padding:4px 16px;display:none}
#visbar.on{display:block}
body:has(#visbar.on){padding-bottom:60px}
#fvis{height:48px}
.knob input{position:absolute;opacity:0;width:1px;height:1px;pointer-events:none}
.disc{--v:0;width:20px;height:20px;border-radius:50%;border:1px solid var(--line);cursor:ns-resize;touch-action:none;background:conic-gradient(from 225deg,var(--ink) calc(var(--v)*2.7deg),var(--cell) 0 270deg,transparent 0)}
.knob input:focus-visible+.disc{outline:2px solid var(--ink);outline-offset:1px}
.knob output{min-width:2ch}
.pat{min-width:96px;min-height:21px}
.tools{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center;margin:0 0 12px;font-size:12px;color:var(--muted)}
.tools a{color:var(--ink)}
.drag{cursor:grab;user-select:none}
.tools input[type=range]{width:140px}
.zplay{display:flex;flex-wrap:wrap;gap:12px 24px;align-items:flex-start;margin:0 0 14px;font-size:12px;color:var(--muted)}
.pad{width:160px;height:160px;position:relative;background:var(--cell);border:1px solid var(--line);border-radius:4px;touch-action:none;cursor:crosshair}
.pad::before,.pad::after{content:'';position:absolute;background:var(--line)}
.pad::before{left:50%;top:0;bottom:0;width:1px}.pad::after{top:50%;left:0;right:0;height:1px}
.dot{position:absolute;width:12px;height:12px;margin:-6px 0 0 -6px;border-radius:50%;background:var(--ink);z-index:1}
.mix{display:grid;grid-template-columns:repeat(7,auto);gap:2px 6px;align-items:center}
.smp{max-width:140px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--muted)}
input.sgain{width:70px}
.drop{outline:2px dashed var(--ink);outline-offset:2px}
.play.on{background:var(--ink);color:var(--bg);border-color:var(--ink)}
#scene{position:fixed;inset:0;width:100vw;height:100vh;z-index:-1;pointer-events:none}
main section{background:color-mix(in srgb,var(--bg) 92%,transparent);border-radius:8px;padding:2px 12px 10px;margin:0 -12px 16px}
main section h2{margin-top:14px}
</style>
</head>
<body>
<canvas id="scene" aria-hidden="true"></canvas>
<header>
<h1>GENDERBENDER · FINGERPRINTS</h1>
<a class="src" href="https://github.com/TOAST3R/genderbender">Código fuente ↗</a>
<label>Género <select id="fam"></select></label><output id="count"></output>
<label>Density <input id="dens" type="range" min="0" max="260" value="50"><output id="densv">50</output></label>
<label>Swing <input id="swing" type="range" min="50" max="75" value="50"><output id="swingv">50</output></label>
<span><label style="display:inline-flex">BPM <input id="bpm" type="range" min="40" max="240" value="120"><output id="bpmv">120</output></label><button class="play" id="bpmreset" title="Volver al BPM del estilo">↺</button></span>
<label>Kit <select id="kit"></select></label>
<span id="snote" class="hint" style="margin:0" hidden></span>
<label class="knob">Distortion <input id="dist" type="range" min="0" max="100" value="0"><span class="disc"></span><output id="distv">0</output></label>
<label class="knob">Delay <input id="dly" type="range" min="0" max="100" value="0"><span class="disc"></span><output id="dlyv">0</output></label>
<label class="knob">Reverb <input id="rev" type="range" min="0" max="100" value="0"><span class="disc"></span><output id="revv">0</output></label>
<span class="hint" style="margin:0">color = valor 0–255 · atenuado = no suena con esta Density · clic para ampliar · ▶ preview sintetizado (no es el sonido de tu sampler) · Esc para</span>
</header>
<main id="main"></main>
<div id="visbar"><canvas id="fvis" class="vis on" title="Clic: onda / espectro"></canvas></div>
<dialog id="zoom"><h3 id="zname"></h3><div class="tools" id="ztools"></div><canvas id="zvis" class="vis" title="Clic: onda / espectro"></canvas><div class="zplay" id="zplay"></div><div class="big" id="zbody"></div><p class="hint">Esc o clic fuera para cerrar</p></dialog>
<script>
const DATA = /*DATA*/;
const STEPS = 32, NV = DATA.voices.length;
const dens = document.getElementById('dens'), densv = document.getElementById('densv');
const canvases = [];  // [canvas, hex, tamaño de celda]

function draw([c, hex, s]) {
  const cs = getComputedStyle(document.documentElement), g = c.getContext('2d'), d = +dens.value;
  g.fillStyle = cs.getPropertyValue('--cell'); g.fillRect(0, 0, c.width, c.height);
  g.fillStyle = cs.getPropertyValue('--ink');
  for (let vi = 0; vi < NV; vi++) for (let st = 0; st < STEPS; st++) {
    const v = parseInt(hex.substr((vi * STEPS + st) * 2, 2), 16);
    if (!v) continue;
    // misma regla que el plugin: suena si 256 - v < Density
    g.globalAlpha = (0.25 + 0.75 * v / 255) * (256 - v < d ? 1 : 0.18);
    g.fillRect(st * s, vi * s, s - (s > 4 ? 1 : 0), s - 1);
  }
  g.globalAlpha = 1;
  if (s > 4) {  // marca cada 8 pasos en la vista ampliada
    g.fillStyle = cs.getPropertyValue('--muted');
    for (let st = 8; st < STEPS; st += 8) g.fillRect(st * s - 1, 0, 1, c.height);
  }
}

function pattern(hex, s, list = canvases) {
  const c = document.createElement('canvas');
  c.width = STEPS * s; c.height = NV * s;
  const item = [c, hex, s]; list.push(item); draw(item);
  return c;
}

// ---- preview de audio: voces sintetizadas con Web Audio, sin recursos externos
const swing = document.getElementById('swing'), swingv = document.getElementById('swingv');
// BPM: el del estilo salvo que se mueva el slider; bpmFor = estilo al que pertenece el cambio
const bpmI = document.getElementById('bpm'), bpmv = document.getElementById('bpmv');
let bpmOverride = null, bpmFor = null;
const setBpmSlider = v => { bpmI.value = bpmv.value = v; syncZoom(); };
function setTempo(P, nb) {  // sin saltos: el siguiente paso por programar no se mueve
  if (nb === P.bpm) return;
  const tNext = P.barStart + stepTime(P.step, P.bpm);
  P.barStart = tNext - stepTime(P.step, nb); P.bpm = nb; delayBpm(nb);
}
bpmI.addEventListener('input', () => {
  bpmv.value = bpmI.value; bpmOverride = +bpmI.value; bpmFor = play ? play.st : (current || bpmFor);
  if (play) setTempo(play, bpmOverride);
  syncZoom(); writeHash();
});
function resetBpm() {
  bpmOverride = null;
  const st = play ? (play.cur ? play.cur.st : play.st) : (current || bpmFor);
  if (st) setBpmSlider(st.bpm);
  if (play && play.cur) setTempo(play, play.cur.st.bpm);
  writeHash();
}
document.getElementById('bpmreset').addEventListener('click', resetBpm);
let ac = null, noiseBuf = null, play = null;
function audio() {
  if (!ac) {
    ac = new AudioContext();
    noiseBuf = ac.createBuffer(1, ac.sampleRate, ac.sampleRate);
    const d = noiseBuf.getChannelData(0);
    for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
  }
  ac.resume();
}
function env(g, t, a, len) { g.gain.setValueAtTime(a, t); g.gain.exponentialRampToValueAtTime(0.001, t + len); }
function tone(t, f0, f1, len, a, out, type = 'sine') {
  const o = ac.createOscillator(), g = ac.createGain();
  o.type = type; o.frequency.setValueAtTime(f0, t); o.frequency.exponentialRampToValueAtTime(f1, t + len);
  env(g, t, a, len); o.connect(g).connect(out || bus()); o.start(t); o.stop(t + len);
}
function noise(t, type, freq, len, a, out, gate) {
  const s = ac.createBufferSource(), f = ac.createBiquadFilter(), g = ac.createGain();
  s.buffer = noiseBuf; f.type = type; f.frequency.value = freq;
  if (gate) { g.gain.setValueAtTime(a, t); g.gain.setValueAtTime(0, t + len); } else env(g, t, a, len);
  s.connect(f).connect(g).connect(out || bus()); s.start(t); s.stop(t + len + 0.01);
  return s;
}
// metal: seis cuadradas en las frecuencias del hat del 808, con paso banda y paso alto
function metal(t, len, a, out) {
  const bp = ac.createBiquadFilter(), hp = ac.createBiquadFilter(), g = ac.createGain();
  bp.type = 'bandpass'; bp.frequency.value = 10000; hp.type = 'highpass'; hp.frequency.value = 7000;
  env(g, t, a, len); bp.connect(hp).connect(g).connect(out || bus());
  const oscs = [205.3, 304.4, 369.6, 522.7, 540, 800].map(f => {
    const o = ac.createOscillator(); o.type = 'square'; o.frequency.value = f; o.connect(bp); o.start(t); o.stop(t + len); return o;
  });
  return {stop: when => oscs.forEach(o => o.stop(when))};
}
function cowbell(t, a, out) {
  const bp = ac.createBiquadFilter(), g = ac.createGain();
  bp.type = 'bandpass'; bp.frequency.value = 800; env(g, t, a, 0.3); bp.connect(g).connect(out || bus());
  [540, 800].forEach(f => { const o = ac.createOscillator(); o.type = 'square'; o.frequency.value = f; o.connect(bp); o.start(t); o.stop(t + 0.3); });
}
const click = (t, a, out) => noise(t, 'highpass', 2000, 0.006, a, out);
const clapBursts = (t, n, freq, a, out) => { for (let k = 0; k < n; k++) noise(t + k * 0.01, 'bandpass', freq, k < n - 1 ? 0.015 : 0.18, a, out); };

// salidas con efecto por kit: crush (bits + paso bajo), drive (distorsion); creadas una vez por contexto
const FX = {};
function fx(name) {
  if (FX[name]) return FX[name];
  const out = ac.createGain();
  if (name === 'lofi' || name === 'chip') {
    const levels = name === 'lofi' ? 32 : 3, ws = ac.createWaveShaper(), c = new Float32Array(1024);
    for (let i = 0; i < 1024; i++) { const x = i / 511.5 - 1; c[i] = Math.round(x * levels) / levels; }
    ws.curve = c; out.connect(ws);
    let last = ws;
    if (name === 'lofi') { const lp = ac.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 4000; ws.connect(lp); last = lp; }
    const g = ac.createGain(); g.gain.value = 0.9; last.connect(g).connect(bus());
  } else if (name === 'drive') {
    const ws = ac.createWaveShaper(), c = new Float32Array(1024), g = ac.createGain();
    for (let i = 0; i < 1024; i++) { const x = i / 511.5 - 1; c[i] = Math.tanh(8 * x); }
    ws.curve = c; g.gain.value = 0.45; out.connect(ws).connect(g).connect(bus());
  } else out.connect(bus());
  return (FX[name] = out);
}
// ---- efectos globales: master -> distortion -> seco + envio de delay + envio de reverb
const FXI = ['dist', 'dly', 'rev'].map(id => document.getElementById(id));
let FXB = null;
function bus() {
  if (FXB) return FXB.in;
  const inp = ac.createGain(), ws = ac.createWaveShaper(), mk = ac.createGain();
  const dsend = ac.createGain(), dl = ac.createDelay(2), lp = ac.createBiquadFilter(), fb = ac.createGain();
  const rsend = ac.createGain(), conv = ac.createConvolver();
  lp.type = 'lowpass'; lp.frequency.value = 3000; fb.gain.value = 0.35;  // realimentacion fija < 0.5: no crece sin fin
  const n = ac.sampleRate * 2, ir = ac.createBuffer(2, n, ac.sampleRate);  // respuesta de impulso de 2 s generada
  for (let ch = 0; ch < 2; ch++) {
    const d = ir.getChannelData(ch);
    for (let i = 0; i < n; i++) d[i] = (Math.random() * 2 - 1) * Math.exp(-6 * i / n);
  }
  conv.buffer = ir;
  dl.delayTime.value = 0.75 * 60 / (play ? play.bpm : 120);
  inp.connect(ws).connect(mk).connect(ac.destination);
  mk.connect(dsend).connect(dl).connect(lp).connect(ac.destination); lp.connect(fb).connect(dl);
  mk.connect(rsend).connect(conv).connect(ac.destination);
  dsend.gain.value = rsend.gain.value = 0;  // sin rampa desde 1 al crear
  const an = ac.createAnalyser(); an.fftSize = 2048;
  mk.connect(an); lp.connect(an); conv.connect(an);
  FXB = {in: inp, ws, mk, dsend, rsend, dl, an};
  applyFx();
  return inp;
}
function applyFx() {  // mueve parametros, no reconstruye nodos
  if (!FXB) return;
  const [dist, dly, rev] = FXI.map(r => +r.value / 100), t = ac.currentTime;
  if (dist) {
    const k = 1 + 19 * dist, c = new Float32Array(1024);
    for (let i = 0; i < 1024; i++) c[i] = Math.tanh(k * (i / 511.5 - 1)) / Math.tanh(k);
    FXB.ws.curve = c; FXB.ws.oversample = '2x';
  } else { FXB.ws.curve = null; FXB.ws.oversample = 'none'; }  // a 0, la señal pasa intacta
  const set = (prm, v) => ac instanceof OfflineAudioContext ? prm.value = v : prm.setTargetAtTime(v, t, 0.02);
  set(FXB.mk.gain, 1 - 0.5 * dist); set(FXB.dsend.gain, 0.6 * dly); set(FXB.rsend.gain, 0.8 * rev);
}
const delayBpm = bpm => { if (FXB) FXB.dl.delayTime.setTargetAtTime(0.75 * 60 / bpm, ac.currentTime, 0.02); };  // corchea con puntillo
function knob(r) {  // disco que se gira arrastrando en vertical o con la rueda; el range da el teclado
  const d = r.nextElementSibling, set = v => {
    v = Math.max(0, Math.min(100, Math.round(v)));
    if (v !== +r.value) { r.value = v; r.dispatchEvent(new Event('input')); }
  };
  r.addEventListener('input', () => d.style.setProperty('--v', r.value)); d.style.setProperty('--v', r.value);
  d.addEventListener('pointerdown', e => {
    e.preventDefault(); d.setPointerCapture(e.pointerId); r.focus();
    const y0 = e.clientY, v0 = +r.value, move = ev => set(v0 + (y0 - ev.clientY) / 2);
    d.addEventListener('pointermove', move);
    d.addEventListener('pointerup', () => d.removeEventListener('pointermove', move), {once: true});
  });
  d.addEventListener('wheel', e => { e.preventDefault(); set(+r.value + (e.deltaY < 0 ? 2 : -2)); }, {passive: false});
}
FXI.forEach(r => {
  knob(r);
  r.addEventListener('input', () => {
    document.getElementById(r.id + 'v').value = r.value;
    applyFx(); syncZoom(); writeHash();
    try { localStorage.setItem('gb-fx', JSON.stringify(FXI.map(x => +x.value))); } catch (e) {}
  });
});

const choke = {};  // el hho de cada kit, para que el hhc lo corte
const hh = (kit, t, open, make) => {
  if (choke.hh) { try { choke.hh.stop(t); } catch (e) {} choke.hh = null; }
  const n = make(); if (open) choke.hh = n;
};
// acustico: tambien lo usa el Lo-fi a traves de su salida con crush
const acoustic = o => [
  t => { tone(t, 90, 55, 0.25, 1, o()); noise(t, 'lowpass', 600, 0.05, 0.4, o()); },
  t => { noise(t, 'bandpass', 3000, 0.25, 0.55, o()); tone(t, 190, 170, 0.12, 0.35, o()); },
  t => clapBursts(t, 3, 1300, 0.45, o()),
  t => hh(o === fxLofi ? 'lofi' : 'acustico', t, false, () => noise(t, 'highpass', 6000, 0.06, 0.25, o())),
  t => hh(o === fxLofi ? 'lofi' : 'acustico', t, true, () => noise(t, 'highpass', 5000, 0.6, 0.14, o())),
  t => { tone(t, 220, 200, 0.3, 0.55, o()); noise(t, 'bandpass', 1500, 0.03, 0.2, o()); },
  t => { tone(t, 140, 125, 0.35, 0.65, o()); noise(t, 'bandpass', 900, 0.03, 0.2, o()); },
];
const dry = () => bus(), fxLofi = () => fx('lofi'), fxChip = () => fx('chip'), fxDrive = () => fx('drive');
const KITS = {
  actual: {label: 'Actual', v: [
    t => tone(t, 150, 45, 0.35, 1),
    t => { noise(t, 'highpass', 1000, 0.15, 0.5); tone(t, 180, 160, 0.1, 0.3); },
    t => { for (let k = 0; k < 3; k++) noise(t + k * 0.01, 'bandpass', 1200, k < 2 ? 0.02 : 0.12, 0.6); },
    t => hh('actual', t, false, () => noise(t, 'highpass', 7000, 0.05, 0.3)),
    t => hh('actual', t, true, () => noise(t, 'highpass', 7000, 0.3, 0.25)),
    t => tone(t, 220, 160, 0.25, 0.6),
    t => tone(t, 140, 100, 0.3, 0.7),
  ]},
  '808': {label: '808', v: [
    t => tone(t, 60, 45, 0.8, 1),
    t => { tone(t, 180, 170, 0.15, 0.3); tone(t, 330, 320, 0.12, 0.2); noise(t, 'highpass', 1500, 0.18, 0.4); },
    t => clapBursts(t, 4, 1100, 0.5),
    t => hh('808', t, false, () => metal(t, 0.05, 0.35)),
    t => hh('808', t, true, () => metal(t, 0.35, 0.3)),
    t => cowbell(t, 0.4),
    t => tone(t, 130, 90, 0.5, 0.7),
  ]},
  '909': {label: '909', v: [
    t => { tone(t, 160, 50, 0.3, 1); click(t, 0.5); },
    t => { noise(t, 'highpass', 2000, 0.2, 0.6); tone(t, 200, 180, 0.1, 0.35); },
    t => clapBursts(t, 3, 1500, 0.55),
    t => hh('909', t, false, () => noise(t, 'highpass', 8000, 0.04, 0.35)),
    t => hh('909', t, true, () => noise(t, 'highpass', 7000, 0.25, 0.28)),
    t => tone(t, 250, 180, 0.2, 0.6),
    t => tone(t, 160, 110, 0.25, 0.7),
  ]},
  acustico: {label: 'Acústico', v: acoustic(dry)},
  lofi: {label: 'Lo-fi', v: acoustic(fxLofi)},
  hardcore: {label: 'Hardcore', v: [
    t => tone(t, 200, 45, 0.5, 1, fxDrive()),
    t => { noise(t, 'highpass', 2000, 0.12, 0.6); tone(t, 220, 190, 0.08, 0.4); },
    t => clapBursts(t, 2, 1600, 0.6),
    t => hh('hardcore', t, false, () => noise(t, 'highpass', 9000, 0.03, 0.4)),
    t => hh('hardcore', t, true, () => noise(t, 'highpass', 7000, 0.15, 0.35)),
    t => tone(t, 250, 180, 0.2, 0.6),
    t => tone(t, 160, 110, 0.25, 0.7),
  ]},
  '80s': {label: '80s / Linn', v: [
    t => tone(t, 120, 55, 0.18, 1),
    t => { noise(t, 'bandpass', 1800, 0.18, 0.6, null, true); tone(t, 220, 180, 0.08, 0.35); },
    t => clapBursts(t, 3, 1200, 0.5),
    t => hh('80s', t, false, () => noise(t, 'highpass', 9000, 0.03, 0.3)),
    t => hh('80s', t, true, () => noise(t, 'highpass', 8000, 0.2, 0.25)),
    t => { tone(t, 300, 120, 0.25, 0.6); noise(t, 'bandpass', 2000, 0.02, 0.2); },
    t => { tone(t, 200, 80, 0.3, 0.7); noise(t, 'bandpass', 1500, 0.02, 0.2); },
  ]},
  percusion: {label: 'Percusión', v: [
    t => tone(t, 80, 70, 0.6, 0.9),
    t => tone(t, 2500, 2400, 0.04, 0.5),
    t => clapBursts(t, 3, 1200, 0.4),
    t => hh('percusion', t, false, () => {  // shaker: ataque suave
      const n = ac.createBufferSource(), f = ac.createBiquadFilter(), g = ac.createGain();
      n.buffer = noiseBuf; f.type = 'bandpass'; f.frequency.value = 6000;
      g.gain.setValueAtTime(0.001, t); g.gain.linearRampToValueAtTime(0.3, t + 0.02); g.gain.exponentialRampToValueAtTime(0.001, t + 0.09);
      n.connect(f).connect(g).connect(bus()); n.start(t); n.stop(t + 0.1); return n;
    }),
    t => hh('percusion', t, true, () => { for (let k = 0; k < 4; k++) noise(t + k * 0.03, 'bandpass', 3000, 0.025, 0.3); return {stop() {}}; }),
    t => cowbell(t, 0.35),
    t => { tone(t, 200, 190, 0.25, 0.7); noise(t, 'bandpass', 2500, 0.01, 0.3); },
  ]},
  chiptune: {label: 'Chiptune', v: [
    t => tone(t, 120, 40, 0.15, 0.8, null, 'square'),
    t => noise(t, 'highpass', 1000, 0.12, 0.5, fxChip()),
    t => noise(t, 'bandpass', 1500, 0.1, 0.5, fxChip()),
    t => hh('chiptune', t, false, () => noise(t, 'highpass', 8000, 0.03, 0.35, fxChip())),
    t => hh('chiptune', t, true, () => noise(t, 'highpass', 6000, 0.18, 0.3, fxChip())),
    t => tone(t, 440, 300, 0.12, 0.4, null, 'square'),
    t => tone(t, 220, 150, 0.15, 0.45, null, 'square'),
  ]},
};
// Auto: el kit de la familia del estilo que suena
const FAM_KIT = {
  'Techno': '909', 'House': '909', 'Hard house': '909', 'Psytrance': '909', 'Rave / oldskool': '909', 'UK garage': '909', 'Gqom': '909',
  'R&B / trap': '808', 'Electro': '808', 'Bass music': '808', 'Phonk': '808', 'Footwork / juke': '808', 'Reggaeton / funk carioca': '808',
  'Breaks': 'acustico', 'Drum & bass': 'acustico', 'Funk / New Orleans': 'acustico', 'Country / Americana': 'acustico', 'Reggae / dancehall': 'acustico',
  'Hip-hop': 'lofi', 'Downtempo / chill': 'lofi', 'Hardcore / hard dance': 'hardcore', 'Synth / disco': '80s', 'EBM / industrial': '80s',
  'Latin / Caribbean': 'percusion', 'Brazil': 'percusion', 'South America': 'percusion', 'Afro / Caribbean': 'percusion',
  'Afro / Latin club': 'percusion', 'Cumbia': 'percusion', 'Flamenco': 'percusion', 'Folk ibérico': 'percusion', 'Celtic': 'percusion',
  'World folk': 'percusion', 'IDM / experimental': 'chiptune', 'Other': 'actual',
};
const FAMILY = {};
DATA.groups.forEach(g => g.styles.forEach(st => { FAMILY[st.name] = g.family; }));
let kitChoice = 'auto';
const kitOf = st => kitChoice !== 'auto' ? kitChoice : (FAM_KIT[FAMILY[st.name]] || 'actual');
const SAMPLES = Array(NV).fill(null);  // {name, buf, gainDb, bytes} por voz
const playVoice = (st, vi, t, v = 255) => SAMPLES[vi] ? playSample(vi, t, v) : KITS[kitOf(st)].v[vi](t);
function playSample(vi, t, v) {
  const smp = SAMPLES[vi], make = () => {
    const src = ac.createBufferSource(), g = ac.createGain();
    src.buffer = smp.buf; g.gain.value = Math.pow(10, smp.gainDb / 20) * v / 255;
    src.connect(g).connect(bus()); src.start(t); return src;
  };
  vi === 3 || vi === 4 ? hh(null, t, vi === 4, make) : make();
}
function stepTime(i, bpm, amt = 100) {
  // deformacion de groove-swing: dentro de cada corchea, [0, 0.25) -> [0, p) y [0.25, 0.5) -> [p, 0.5)
  // con el swing de la voz: S_voz = 50 + (S - 50) * amount / 100
  const sv = 50 + (swing.value - 50) * amt / 100;
  const x = (i % 4) * 0.125, p = sv / 100 * 0.5;
  const w = x < 0.25 ? x * p / 0.25 : p + (x - 0.25) * (0.5 - p) / 0.25;
  return (Math.floor(i / 4) * 0.5 + w) * 60 / bpm;
}
// valores 0-255 de un patron (cache por hex)
const VALS = new Map();
function vals(hex) {
  let v = VALS.get(hex);
  if (!v) {
    v = Array.from({length: NV}, (_, vi) => Array.from({length: STEPS}, (_, i) => parseInt(hex.substr((vi * STEPS + i) * 2, 2), 16)));
    VALS.set(hex, v);
  }
  return v;
}
const isEmpty = hex => !/[^0]/.test(hex);
// mute / solo por voz: con algun solo activo suenan solo los solos
const mute = Array(NV).fill(false), solo = Array(NV).fill(false);
const audible = vi => solo.some(Boolean) ? solo[vi] : !mute[vi];

// ---- pad XY: la mezcla del plugin (genderbender.jsfx, lineas 766-772 y 501-504)
let padX = 0, padY = 0, padSector = 4;
function padValue(st, vi, i, sb) {
  const x = padX, y = padY;
  // mismo orden que el plugin: gana la ultima condicion que se cumple (en (0,0), el sector 4)
  if (x < 0 && y < 0) padSector = 1;
  if (x < 0 && y > 0) padSector = 2;
  if (x >= 0 && y >= 0) padSector = 3;
  if (x >= 0 && y <= 0) padSector = 4;
  const X = Math.abs(x) / 100, Y = Math.abs(y) / 100, P = n => vals(st.p[n])[vi][i];
  switch (padSector) {
    case 1: return (P(0 + sb) * X + P(2 + sb) * (1 - X)) * Y + (P(4 + sb) * X + P(6 + sb) * (1 - X)) * (1 - Y);
    case 2: return (P(0 + sb) * X + P(4 + sb) * (1 - X)) * Y + (P(6 + sb) * X + P(8) * (1 - X)) * (1 - Y);
    case 3: return (P(0 + sb) * (1 - X) + P(2 + sb) * X) * (1 - Y) + (P(8) * (1 - X) + P(6 + sb) * X) * Y;
    default: return (P(0 + sb) * (1 - X) + P(8) * X) * Y + (P(4 + sb) * (1 - X) + P(2 + sb) * X) * (1 - Y);
  }
}
const barOf = (st, hex, mark) => { const v = vals(hex); return {st, val: (vi, i) => v[vi][i], mark}; };

function tick() {
  const P = play;
  while (P.barStart + stepTime(P.step, P.bpm) < ac.currentTime + 0.1) {
    if (P.step === 0) {
      P.cur = P.getBar(P.bar);
      if (P.cur.st !== P.lastSt) {  // A/B: cada estilo con su BPM y su swing
        if (P.lastSt) { swing.value = swingv.value = P.cur.st.swing; syncZoom(); }
        P.lastSt = P.cur.st; P.bpm = bpmOverride ?? P.cur.st.bpm; P.amt = P.cur.st.amt || Array(NV).fill(100);
        if (bpmOverride == null) setBpmSlider(P.bpm);
        delayBpm(P.bpm);
      }
      showAuto(P.cur.st);
      const t0 = Math.max(P.barStart, ac.currentTime), mark = P.cur.mark;
      setTimeout(() => { if (play === P) P.marks.forEach(m => m.classList.toggle('playing', m === mark)); }, (t0 - ac.currentTime) * 1000);
    }
    const d = +dens.value, hits = [];
    for (let vi = 0; vi < NV; vi++) {
      if (!audible(vi)) continue;
      const v = P.cur.val(vi, P.step);
      // misma regla que el plugin; cada voz con su amount de swing
      if (v && 256 - v < d) { playVoice(P.cur.st, vi, Math.max(P.barStart + stepTime(P.step, P.bpm, P.amt[vi]), ac.currentTime), v); hits.push(vi); }
    }
    P.q.push({t: P.barStart + stepTime(P.step, P.bpm), mark: P.cur.mark, step: P.step, hits, st: P.cur.st});
    if (++P.step === STEPS) { P.step = 0; P.bar++; P.barStart += 240 / P.bpm; }
  }
}
function stop() {
  if (!play) return;
  clearInterval(play.timer);
  play.btn.textContent = play.label; play.btn.setAttribute('aria-pressed', 'false');
  play.marks.forEach(m => m.classList.remove('playing'));
  play = null;
  cursor.remove();
  S.last = null; drawScene(0, true);
  document.querySelectorAll('.vis, #visbar').forEach(e => e.classList.toggle('on', e.id === 'fvis'));
}
function start(btn, label, pats, marks, st, inZoom, getBar) {
  const same = play && play.btn === btn;
  stop();
  if (same) return;
  audio();
  swing.value = swingv.value = st.swing;  // la receta del estilo; se puede mover a mano mientras suena
  syncZoom();
  getBar = getBar || (b => barOf(st, pats[b % pats.length], marks[b % marks.length]));
  if (st !== bpmFor && bpmOverride != null) { bpmOverride = null; bpmFor = st; writeHash(); }  // otro estilo: vuelve a su BPM, como el Swing
  bpmFor = st; setBpmSlider(bpmOverride ?? st.bpm);
  play = {btn, label, getBar, marks, st, bpm: bpmOverride ?? st.bpm, amt: st.amt || Array(NV).fill(100), inZoom,
          bar: 0, step: 0, barStart: ac.currentTime + 0.05, q: []};
  btn.textContent = '■ Stop'; btn.setAttribute('aria-pressed', 'true');
  S.last = null; S.hitAt.fill(-1e9); S.ev.length = 0;
  play.timer = setInterval(tick, 25); tick();
  if (!raf) raf = requestAnimationFrame(frame);
}

// ---- visuales: cursor de paso, golpes por voz y onda / espectro, solo mientras suena
const cursor = document.createElement('div'); cursor.className = 'cursor';
const still = matchMedia('(prefers-reduced-motion: reduce)');
let raf = 0, visMode = 'onda';
try { if (localStorage.getItem('gb-vis') === 'espectro') visMode = 'espectro'; } catch (e) {}
document.querySelectorAll('.vis').forEach(c => c.addEventListener('click', () => {
  visMode = visMode === 'onda' ? 'espectro' : 'onda';
  try { localStorage.setItem('gb-vis', visMode); } catch (e) {}
}));
function showStep(e) {
  const row = e.mark && e.mark.querySelector && e.mark.querySelector('.row');
  if (!row) return;  // en la lista no hay cursor: solo se marca el patron
  const c = row.querySelector('canvas'), w = c.offsetWidth / STEPS;
  if (cursor.parentNode !== row) row.append(cursor);
  Object.assign(cursor.style, {left: c.offsetLeft + e.step * w + 'px', top: c.offsetTop + 'px', width: w + 'px', height: c.offsetHeight + 'px'});
  if (still.matches) return;
  const names = row.querySelectorAll('.voices span');
  e.hits.forEach(vi => { const n = names[vi]; n.classList.add('hit'); setTimeout(() => n.classList.remove('hit'), 80); });
}
function drawVis(c) {
  if (c.width !== c.offsetWidth) { c.width = c.offsetWidth; c.height = c.offsetHeight; }
  const g = c.getContext('2d'), W = c.width, H = c.height, an = FXB.an;
  g.clearRect(0, 0, W, H); g.fillStyle = g.strokeStyle = getComputedStyle(c).getPropertyValue('--ink') || '#c40';
  if (visMode === 'onda') {
    const d = new Float32Array(an.fftSize); an.getFloatTimeDomainData(d);
    g.beginPath();
    for (let x = 0; x < W; x++) { const y = H / 2 - d[Math.floor(x / W * d.length)] * H / 2; x ? g.lineTo(x, y) : g.moveTo(x, y); }
    g.stroke();
  } else {
    const d = new Uint8Array(an.frequencyBinCount), N = 48, bw = W / N; an.getByteFrequencyData(d);
    for (let i = 0; i < N; i++) {  // barras en escala logaritmica de 30 Hz a 16 kHz
      const f = 30 * Math.pow(16000 / 30, i / (N - 1)), v = d[Math.min(d.length - 1, Math.round(f / (ac.sampleRate / 2) * d.length))] / 255;
      g.fillRect(i * bw + 1, H - v * H, bw - 2, v * H);
    }
  }
}
function frame(ts) {
  if (!play) { raf = 0; return; }
  const now = ac.currentTime - (ac.outputLatency || 0);
  let e;
  while (play.q.length && play.q[0].t <= now) {
    e = play.q.shift(); S.last = e;
    e.hits.forEach(vi => { S.hitAt[vi] = e.t; S.ev.push({vi, t: e.t}); });
  }
  if (S.ev.length > 64) S.ev.splice(0, S.ev.length - 64);
  if (e) showStep(e);
  const vis = [document.getElementById('zvis')], bar = document.getElementById('visbar');
  vis[0].classList.toggle('on', !still.matches && zoom.open);
  bar.classList.toggle('on', !still.matches && !play.inZoom);
  if (!still.matches && FXB) { if (zoom.open) drawVis(vis[0]); if (!play.inZoom) drawVis(document.getElementById('fvis')); }
  drawScene(ts);
  raf = requestAnimationFrame(frame);
}

// ---- escenas de fondo: una por grupo de kit; se mueven al tempo y con los golpes
const sceneC = document.getElementById('scene'), sg = sceneC.getContext('2d'), snap = document.createElement('canvas');
const S = {id: null, fade0: 0, last: null, hitAt: Array(NV).fill(-1e9), ev: [], lastDraw: 0, w: 0, h: 0, pal: null, fbuf: null};
function sceneSize() {
  const dpr = Math.min(2, devicePixelRatio || 1);
  S.w = innerWidth; S.h = innerHeight;
  sceneC.width = snap.width = Math.round(S.w * dpr); sceneC.height = snap.height = Math.round(S.h * dpr);
  sg.setTransform(dpr, 0, 0, dpr, 0, 0);
}
function scenePal() {
  const cs = getComputedStyle(document.documentElement), v = n => cs.getPropertyValue(n).trim(), bg = v('--bg');
  S.pal = {bg, fg: v('--fg'), muted: v('--muted'), cell: v('--cell'), ink: v('--ink'), line: v('--line'), dark: parseInt(bg.slice(1, 3), 16) < 128};
}
function sceneId() {  // el estilo que suena; si no, el genero del filtro
  const f = play && S.last ? FAMILY[S.last.st.name] : fam.value;
  return (f && FAM_KIT[f]) || 'actual';
}
function sceneState(calm) {
  const s = {w: S.w, h: S.h, pal: S.pal, t: 0, pos: 0, beat: 0, bpm: 120, age: Array(NV).fill(Infinity),
             lo: 0, mid: 0, hi: 0, spec: Array(16).fill(0), ev: [], calm};
  if (calm || !play) return s;
  const now = ac.currentTime - (ac.outputLatency || 0);
  s.t = now; s.bpm = play.bpm;
  if (S.last) { s.pos = (S.last.step / 8 + Math.max(0, now - S.last.t) * play.bpm / 60) % 4; s.beat = s.pos % 1; }
  s.age = S.hitAt.map(t => now - t);
  s.ev = S.ev.filter(e => now - e.t < 1.5).map(e => ({vi: e.vi, age: now - e.t, seed: e.t + e.vi * 0.37}));
  if (FXB) {
    if (!S.fbuf) S.fbuf = new Uint8Array(FXB.an.frequencyBinCount);
    FXB.an.getByteFrequencyData(S.fbuf);
    const n = S.fbuf.length, bin = f => Math.min(n - 1, Math.round(f / (ac.sampleRate / 2) * n));
    const avg = (a, b) => { let x = 0, k = 0; for (let i = bin(a); i <= bin(b); i++) { x += S.fbuf[i]; k++; } return x / k / 255; };
    s.lo = avg(30, 150); s.mid = avg(300, 2000); s.hi = avg(5000, 12000);
    s.spec = s.spec.map((_, i) => avg(40 * Math.pow(300, i / 16), 40 * Math.pow(300, (i + 1) / 16)));
  }
  return s;
}
function drawScene(ts, force) {
  if (!S.pal) scenePal();
  const id = sceneId(), now = performance.now(), animate = play && !still.matches;
  if (id !== S.id) {
    if (S.id && animate) { const c = snap.getContext('2d'); c.clearRect(0, 0, snap.width, snap.height); c.drawImage(sceneC, 0, 0); S.fade0 = now; }
    else S.fade0 = 0;
    S.id = id; force = true;
  }
  const fade = animate && S.fade0 ? (now - S.fade0) / 400 : 1;  // fundido de 400 ms
  if (!force && (!animate || now - S.lastDraw < 33)) return;  // fondo a <= 30 fps; fijo sin reproduccion
  S.lastDraw = now;
  sg.save(); SCENES[S.id](sg, sceneState(!animate)); sg.restore();
  if (fade < 1) { sg.save(); sg.setTransform(1, 0, 0, 1, 0, 0); sg.globalAlpha = 1 - fade; sg.drawImage(snap, 0, 0); sg.restore(); }
  else S.fade0 = 0;
}
const dec = (age, tau) => age >= 0 ? Math.exp(-age / tau) : 0;  // envolvente de un golpe
const hash = i => { const x = Math.sin(i * 12.9898) * 43758.5453; return x - Math.floor(x); };
const back = (g, s) => { g.fillStyle = s.pal.bg; g.fillRect(0, 0, s.w, s.h); };
const grain = (g, s, n, a) => {
  g.fillStyle = s.pal.fg; g.globalAlpha = a;
  for (let i = 0; i < n; i++) g.fillRect(Math.random() * s.w, Math.random() * s.h, 1.5, 1.5);
  g.globalAlpha = 1;
};
const SCENES = {
  // 909: panel en perspectiva con potes y la tira de 16 pasos; el panel respira con el bombo
  '909'(g, s) {
    back(g, s);
    const {w, h, pal} = s, b = 1 + 0.03 * dec(s.age[0], 0.15), pw = Math.min(w * 0.9, 1300), ph = Math.min(h * 0.34, 320);
    g.translate(w / 2, h * 0.62); g.scale(b, b);
    g.globalAlpha = 0.55; g.fillStyle = pal.dark ? '#202020' : '#d4d0c8';
    g.beginPath(); g.moveTo(-pw * 0.4, -ph / 2); g.lineTo(pw * 0.4, -ph / 2); g.lineTo(pw / 2, ph / 2); g.lineTo(-pw / 2, ph / 2); g.fill();
    g.globalAlpha = 0.6; g.strokeStyle = pal.line; g.lineWidth = 2;
    for (let i = 0; i < 12; i++) {  // potes
      const x = (-0.5 + (i + 0.5) / 12) * pw * 0.78, y = -ph * 0.22, r = ph * 0.06;
      g.fillStyle = pal.cell; g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); g.stroke();
      const a = -2.4 + hash(i) * 4.8; g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.cos(a) * r, y + Math.sin(a) * r); g.stroke();
    }
    const lit = s.calm ? -1 : Math.floor(s.pos * 4) % 16, TR = ['#c0392b', '#e67e22', '#f1c40f', '#ecf0f1'];
    for (let i = 0; i < 16; i++) {
      const bw = pw * 0.92 / 16, x = -pw * 0.46 + i * bw, y = ph * 0.18;
      g.globalAlpha = i === lit ? 1 : 0.3; g.fillStyle = TR[i >> 2];
      g.shadowBlur = i === lit ? 18 : 0; g.shadowColor = TR[i >> 2];
      g.fillRect(x + bw * 0.12, y, bw * 0.76, ph * 0.16);
    }
  },
  // 808: tunel de anillos que avanzan al tempo; el bombo lanza una onda larga y los graves lo hacen ondular
  '808'(g, s) {
    back(g, s);
    const {w, h, pal} = s, cx = w / 2 + s.lo * 14 * Math.sin(s.t * 7), cy = h / 2 + s.lo * 14 * Math.cos(s.t * 5), R = Math.hypot(w, h) / 2;
    g.strokeStyle = '#8b5cf6';
    for (let i = 0; i < 16; i++) {
      const d = (i + s.beat) / 16;
      g.globalAlpha = 0.06 + 0.3 * d; g.lineWidth = 1 + 3 * d;
      g.beginPath(); g.arc(cx, cy, R * d * d, 0, 7); g.stroke();
    }
    const a = s.age[0];
    if (a < 1) { g.globalAlpha = 0.5 * (1 - a); g.strokeStyle = pal.ink; g.lineWidth = 14 * (1 - a); g.beginPath(); g.arc(cx, cy, R * Math.pow(a, 0.6), 0, 7); g.stroke(); }
  },
  // acustico: bateria vista desde arriba; el parche de cada voz ondula al golpear
  acustico(g, s) {
    back(g, s);
    const {w, h, pal} = s, m = Math.min(w, h), cx = w / 2;
    const kit = [[cx, h * 0.62, 0.2, 0], [cx - m * 0.3, h * 0.62, 0.11, 1], [cx + m * 0.5, h * 0.36, 0.15, 2], [cx - m * 0.5, h * 0.45, 0.1, 3],
                 [cx - m * 0.5, h * 0.45, 0.1, 4], [cx - m * 0.12, h * 0.36, 0.09, 5], [cx + m * 0.16, h * 0.36, 0.1, 6]];
    for (const [x, y, rr, vi] of kit) {
      const r = rr * m, cym = vi === 2 || vi >= 3 && vi <= 4, k = dec(s.age[vi], 0.3);
      g.globalAlpha = 0.45; g.fillStyle = cym ? '#ca8a04' : pal.cell; g.strokeStyle = '#a16207'; g.lineWidth = cym ? 1 : 4;
      g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); g.stroke();
      if (k > 0.01) {
        g.strokeStyle = pal.ink; g.lineWidth = 2;
        for (let j = 1; j <= 3; j++) {
          g.globalAlpha = 0.6 * k; g.beginPath();
          g.arc(x, y, r * (j / 4 + 0.03 * k * Math.sin(s.age[vi] * 50 + j)), 0, 7); g.stroke();
        }
      }
    }
  },
  // lo-fi: vinilo que gira a 33 rpm (escalado por el tempo), grano, polvo con los hats y vineta calida
  lofi(g, s) {
    back(g, s);
    const {w, h, pal} = s, cx = w / 2, cy = h * 0.55, R = Math.min(w, h) * 0.38, a = s.t * 2 * Math.PI * (33.333 / 60) * (s.bpm / 90);
    g.globalAlpha = 0.85; g.fillStyle = '#18181b'; g.beginPath(); g.arc(cx, cy, R, 0, 7); g.fill();
    g.strokeStyle = '#fff'; g.lineWidth = 1;
    for (let i = 0; i < 26; i++) { g.globalAlpha = 0.03 + 0.03 * (i % 3 === 0); g.beginPath(); g.arc(cx, cy, R * (0.36 + 0.62 * i / 26), 0, 7); g.stroke(); }
    g.globalAlpha = 0.07; g.fillStyle = '#fff'; g.beginPath(); g.moveTo(cx, cy); g.arc(cx, cy, R, a, a + 0.5); g.fill();
    g.globalAlpha = 0.9; g.fillStyle = pal.ink; g.beginPath(); g.arc(cx, cy, R * 0.32, 0, 7); g.fill();
    g.strokeStyle = pal.bg; g.lineWidth = 3; g.beginPath(); g.moveTo(cx, cy); g.lineTo(cx + Math.cos(a) * R * 0.3, cy + Math.sin(a) * R * 0.3); g.stroke();
    g.strokeStyle = pal.muted; g.lineWidth = 6; g.globalAlpha = 0.7;
    g.beginPath(); g.moveTo(cx + R * 1.05, cy - R * 0.95); g.lineTo(cx + R * 0.5, cy - R * 0.1); g.stroke();
    if (Math.min(s.age[3], s.age[4]) < 0.08) {
      g.fillStyle = '#fff'; g.globalAlpha = 0.7;
      for (let i = 0; i < 6; i++) { const r = R * Math.sqrt(Math.random()), t = Math.random() * 7; g.fillRect(cx + Math.cos(t) * r, cy + Math.sin(t) * r, 2, 2); }
    }
    g.globalAlpha = 1;
    const v = g.createRadialGradient(cx, cy, R * 0.6, cx, cy, Math.hypot(w, h) / 1.6);
    v.addColorStop(0, 'rgba(120,80,40,0)'); v.addColorStop(1, 'rgba(120,80,40,.28)'); g.fillStyle = v; g.fillRect(0, 0, w, h);
    grain(g, s, 400, 0.06);
  },
  // hardcore: franjas de aviso que pasan al tempo y suelo aspero; el bombo sacude la camara, sin destellos
  hardcore(g, s) {
    back(g, s);
    const {w, h} = s, a = s.age[0], k = dec(a, 0.1);
    g.translate(10 * k * Math.sin(a * 80), 6 * k * Math.cos(a * 70));
    g.fillStyle = 'rgba(127,29,29,.12)'; g.fillRect(-20, -20, w + 40, h + 40);
    g.strokeStyle = s.pal.muted; g.lineWidth = 1.5; g.globalAlpha = 0.35;
    for (let j = 0; j < 7; j++) {
      g.beginPath();
      for (let x = -20; x <= w + 20; x += 12) {
        const y = h * (0.3 + 0.07 * j) + Math.sin(x * 0.05 + j * 3 + s.pos * 2) * 6 + Math.sin(x * 0.13 + j) * 3;
        x < 0 ? g.moveTo(x, y) : g.lineTo(x, y);
      }
      g.stroke();
    }
    const sw = 40, off = (s.pos * 2 * sw) % (2 * sw);
    for (const [y0, y1] of [[-20, h * 0.1], [h * 0.9, h + 20]]) {
      g.save(); g.beginPath(); g.rect(-20, y0, w + 40, y1 - y0); g.clip();
      g.globalAlpha = 0.6; g.fillStyle = '#0a0a0a'; g.fillRect(-20, y0, w + 40, y1 - y0);
      g.globalAlpha = 0.55; g.fillStyle = '#eab308';
      for (let x = -h - 2 * sw + off; x < w + h; x += 2 * sw) {
        g.beginPath(); g.moveTo(x, y1); g.lineTo(x + sw, y1); g.lineTo(x + sw + (y1 - y0), y0); g.lineTo(x + (y1 - y0), y0); g.fill();
      }
      g.restore();
    }
  },
  // 80s: rejilla de neon que avanza al tempo, sol a franjas; la caja da brillo en el horizonte, los hats estrellas
  '80s'(g, s) {
    back(g, s);
    const {w, h, pal} = s, y0 = h * 0.55, R = Math.min(w, h) * 0.2;
    const sky = g.createLinearGradient(0, 0, 0, y0);
    sky.addColorStop(0, pal.dark ? '#1e0b3a' : '#f5d0fe'); sky.addColorStop(1, pal.dark ? '#5b1a5e' : '#fbcfe8');
    g.globalAlpha = 0.6; g.fillStyle = sky; g.fillRect(0, 0, w, y0);
    g.fillStyle = pal.dark ? '#fff' : '#7e22ce';
    for (let i = 0; i < 50; i++) {
      g.globalAlpha = 0.2 + (i % 3 === 0 ? 0.6 * dec(s.age[3], 0.15) : 0) + (i % 5 === 0 ? 0.6 * dec(s.age[4], 0.3) : 0);
      g.fillRect(hash(i) * w, hash(i + 99) * y0 * 0.85, 2, 2);
    }
    g.save(); g.beginPath(); g.rect(0, 0, w, y0); g.clip();
    const sun = g.createLinearGradient(0, y0 - R, 0, y0); sun.addColorStop(0, '#fde047'); sun.addColorStop(1, '#ec4899');
    g.globalAlpha = 0.85; g.fillStyle = sun; g.beginPath(); g.arc(w / 2, y0, R, 0, 7); g.fill();
    g.globalAlpha = 1; g.fillStyle = pal.dark ? '#5b1a5e' : '#fbcfe8';
    for (let k = 0; k < 6; k++) g.fillRect(w / 2 - R, y0 - R * (0.08 + 0.13 * k), 2 * R, 2 + k * 1.2);
    g.restore();
    g.globalAlpha = 0.35; g.fillStyle = pal.dark ? '#2e1065' : '#ede9fe'; g.fillRect(0, y0, w, h - y0);
    g.strokeStyle = '#e879f9'; g.lineWidth = 1.5; g.globalAlpha = 0.6;
    for (let i = -24; i <= 24; i++) { g.beginPath(); g.moveTo(w / 2, y0); g.lineTo(w / 2 + i * w * 0.09, h); g.stroke(); }
    const fr = s.pos % 1;
    for (let j = 0; j < 16; j++) { const z = j + 1 - fr, y = y0 + (h - y0) / z; g.beginPath(); g.moveTo(0, y); g.lineTo(w, y); g.stroke(); }
    const k = dec(s.age[1], 0.2);
    g.globalAlpha = 0.8; g.shadowColor = '#f0abfc'; g.shadowBlur = 24 * k; g.lineWidth = 2 + 6 * k;
    g.beginPath(); g.moveTo(0, y0); g.lineTo(w, y0); g.stroke();
  },
  // percusion: tejido de colores; cada golpe deja caer una piedra con ondas de un color por voz
  percusion(g, s) {
    back(g, s);
    const {w, h} = s, C = ['#b45309', '#dc2626', '#ca8a04', '#65a30d', '#16a34a', '#0891b2', '#9333ea'], T = 28;
    g.globalAlpha = 0.12;
    for (let y = 0, iy = 0; y < h; y += T, iy++) for (let x = 0, ix = 0; x < w; x += T, ix++) {
      g.fillStyle = C[(ix + 2 * iy) % 4];
      (ix + iy) % 2 ? g.fillRect(x, y + T * 0.3, T, T * 0.4) : g.fillRect(x + T * 0.3, y, T * 0.4, T);
    }
    g.lineWidth = 3;
    for (const e of s.ev) {
      const x = hash(e.seed * 91.7) * w, y = hash(e.seed * 47.3) * h, r = 20 + e.age * 260;
      g.strokeStyle = C[e.vi]; g.globalAlpha = 0.6 * (1 - e.age / 1.5);
      g.beginPath(); g.arc(x, y, r, 0, 7); g.stroke(); g.beginPath(); g.arc(x, y, r * 0.6, 0, 7); g.stroke();
    }
  },
  // chiptune: CRT de Game Boy con ecualizador de bloques y un sprite que salta con el bombo
  chiptune(g, s) {
    back(g, s);
    const {w, h, pal} = s, GB = ['#0f380f', '#306230', '#8bac0f', '#9bbc0f'], scr = pal.dark ? GB[0] : GB[3], px = pal.dark ? GB[2] : GB[0];
    const x0 = w * 0.08, y0 = h * 0.1, sw = w * 0.84, sh = h * 0.8, bs = sw / 16 / 1.25;
    g.globalAlpha = 0.85; g.fillStyle = scr; g.beginPath(); g.roundRect(x0, y0, sw, sh, 24); g.fill();
    g.strokeStyle = pal.line; g.lineWidth = 6; g.stroke();
    g.fillStyle = px; g.globalAlpha = 0.8;
    for (let i = 0; i < 16; i++) {
      const n = s.calm ? 1 + (i * 7 % 5) : Math.round(s.spec[i] * 12);
      for (let j = 0; j < n; j++) g.fillRect(x0 + sw * 0.04 + i * sw * 0.92 / 16, y0 + sh * 0.92 - (j + 1) * bs * 0.8, bs, bs * 0.65);
    }
    const SPR = ['00100100', '00011000', '00111100', '01011010', '11111111', '10111101', '10100101', '00011000'], ps = bs * 0.4;
    const sx = x0 + sw * (0.1 + 0.8 * s.pos / 4), sy = y0 + sh * 0.18 - bs * 3 * dec(s.age[0], 0.25);
    g.fillStyle = GB[1]; g.globalAlpha = 0.95;
    SPR.forEach((row, r) => [...row].forEach((c, k) => { if (c === '1') g.fillRect(sx + k * ps, sy + r * ps, ps, ps); }));
    g.fillStyle = '#000'; g.globalAlpha = 0.12;
    for (let y = y0; y < y0 + sh; y += 3) g.fillRect(x0, y, sw, 1);
  },
  // otros: grano suave
  actual(g, s) { back(g, s); grain(g, s, 300, 0.05); },
};
addEventListener('resize', () => { sceneSize(); drawScene(0, true); });
sceneSize();
function playButton(label, onClick) {
  const b = document.createElement('button');
  b.type = 'button'; b.className = 'play'; b.textContent = label; b.setAttribute('aria-pressed', 'false');
  b.addEventListener('click', e => { e.stopPropagation(); onClick(b); });
  b.addEventListener('keydown', e => e.stopPropagation());
  return b;
}
document.addEventListener('keydown', e => { if (e.key === 'Escape' && !zoom.open) stop(); });
swing.addEventListener('input', () => { swingv.value = swing.value; syncZoom(); });

const main = document.getElementById('main'), zoom = document.getElementById('zoom');
const zbody = document.getElementById('zbody');
let zoomed = [];

function openZoom(st) {
  if (play && play.inZoom) stop();
  zoomed.length = 0;
  zbody.textContent = '';
  document.getElementById('zname').textContent = st.name;
  zoomTools(st);
  current = st;
  mute.fill(false); solo.fill(false);
  const figs = [];
  wavCache = []; wavUI = [];
  st.p.forEach((hex, i) => {
    const f = document.createElement('figure'), cap = document.createElement('figcaption');
    figs.push(f);
    cap.textContent = 'p' + i + (i === 8 ? ' FILL' : '');
    cap.append(playButton('▶', b => start(b, '▶', [hex], [f], st, true)));
    if (!isEmpty(hex)) wavButtons(st, i, cap);
    const row = document.createElement('div'); row.className = 'row';
    const names = document.createElement('div'); names.className = 'voices';
    DATA.voices.forEach((v, vi) => { const e = document.createElement('span'); e.textContent = v; dropTarget(e, vi); names.append(e); });
    row.append(names, pattern(hex, 10, zoomed)); f.append(cap, row); zbody.append(f);
  });
  zoomPlay(st, figs);
  scheduleCache();
  if (!zoom.open) zoom.showModal();
  writeHash();
}

function zoomPlay(st, figs) {
  const z = document.getElementById('zplay'); z.textContent = '';
  // pad XY
  const box = document.createElement('div'), pad = document.createElement('div'), dot = document.createElement('div');
  const pos = document.createElement('output'), note = document.createElement('div');
  pad.className = 'pad'; dot.className = 'dot'; pad.append(dot);
  pad.title = 'Pad XY del plugin: arrastra mientras suena; doble clic para volver al centro';
  const place = () => { dot.style.left = (padX + 100) / 2 + '%'; dot.style.top = (100 - padY) / 2 + '%'; pos.value = 'x ' + padX + ' · y ' + padY; };
  const move = e => {
    const r = pad.getBoundingClientRect(), c = v => Math.max(-100, Math.min(100, Math.round(v)));
    padX = c(((e.clientX - r.left) / r.width * 2 - 1) * 100); padY = c((1 - (e.clientY - r.top) / r.height * 2) * 100); place();
  };
  pad.addEventListener('pointerdown', e => { pad.setPointerCapture(e.pointerId); move(e); });
  pad.addEventListener('pointermove', e => { if (e.buttons) move(e); });
  pad.addEventListener('dblclick', () => { padX = padY = 0; place(); });
  padX = padY = 0; place();
  note.textContent = 'como en el plugin: justo encima del centro cambia de sector';
  const padBtn = playButton('▶ pad', b => start(b, '▶ pad', null, [], st, true, n => ({st, val: (vi, i) => padValue(st, vi, i, n % 2), mark: null})));
  box.append(padBtn, ' ', pos, pad, note);
  // secuencia: INTRO -> BASE -> ENERGIA -> VARIACION -> FILL, sin partes vacias
  const seq = [0, 1, 4, 5, 2, 3, 6, 7, 8, 8].filter(k => !isEmpty(st.p[k]));
  const seqBtn = playButton('▶ secuencia', b => start(b, '▶ secuencia', null, figs, st, true, n => barOf(st, st.p[seq[n % seq.length]], figs[seq[n % seq.length]])));
  // A/B con otro estilo
  const all = DATA.groups.flatMap(g => g.styles), sel = document.createElement('select');
  all.forEach(o => { if (o !== st) sel.append(new Option(o.name, o.name)); });
  const abBtn = playButton('▶ A/B', b => {
    const other = all.find(o => o.name === sel.value);
    start(b, '▶ A/B', null, [], st, true, n => { const s2 = Math.floor(n / 2) % 2 ? other : st; return barOf(s2, s2.p[4 + n % 2], null); });
  });
  const col = document.createElement('div'); col.style.display = 'grid'; col.style.gap = '8px';
  const ab = document.createElement('label'); ab.append('B: ', sel);
  col.append(seqBtn, abBtn, ab);
  // mute / solo por voz
  const mix = document.createElement('div'); mix.className = 'mix';
  DATA.voices.forEach((v, vi) => {
    const tg = (arr, txt) => playButton(txt, b => { arr[vi] = !arr[vi]; b.classList.toggle('on', arr[vi]); b.textContent = txt; });
    const name = document.createElement('span'); name.textContent = v;
    dropTarget(name, vi);
    const lab = document.createElement('span'); lab.className = 'smp';
    const up = playButton('⇪', () => { pickFor = vi; picker.click(); }); up.title = 'Cargar un sample de tu equipo (o suéltalo sobre el nombre de la voz)';
    const x = playButton('✕', () => clearSample(vi)); x.title = 'Volver al kit';
    const gn = document.createElement('input'); gn.type = 'range'; gn.min = -24; gn.max = 6; gn.className = 'sgain'; gn.title = 'Ganancia del sample (dB)';
    gn.addEventListener('input', () => { if (SAMPLES[vi]) { SAMPLES[vi].gainDb = +gn.value; saveSample(vi); sampleVer++; } });
    sampleUI[vi] = {lab, gn};
    mix.append(name, tg(mute, 'M'), tg(solo, 'S'), lab, up, x, gn);
  });
  z.append(box, col, mix);
  refreshSamples();
}
zoom.addEventListener('click', e => { if (e.target === zoom) zoom.close(); });
zoom.addEventListener('close', () => { current = null; writeHash(); });

// ---- samples propios: archivo local -> AudioBuffer; se guardan en IndexedDB, nunca salen del navegador
const sampleUI = [], picker = Object.assign(document.createElement('input'), {type: 'file', accept: 'audio/*', hidden: true});
let pickFor = 0, sampleVer = 0;
document.body.append(picker);
picker.addEventListener('change', () => { if (picker.files[0]) loadSample(pickFor, picker.files[0]); picker.value = ''; });
addEventListener('dragover', e => e.preventDefault());  // soltar un archivo fuera de una voz no abre el archivo
addEventListener('drop', e => e.preventDefault());
function notice(msg) {
  const n = document.getElementById('snote'); n.hidden = false; n.textContent = msg;
  clearTimeout(notice.t); notice.t = setTimeout(refreshSamples, 5000);
}
function dropTarget(el, vi) {
  el.addEventListener('dragover', e => { if (e.dataTransfer.types.includes('Files')) { e.preventDefault(); el.classList.add('drop'); } });
  el.addEventListener('dragleave', () => el.classList.remove('drop'));
  el.addEventListener('drop', e => { e.preventDefault(); el.classList.remove('drop'); if (e.dataTransfer.files[0]) loadSample(vi, e.dataTransfer.files[0]); });
}
function idb(mode, fn) {
  return new Promise((ok, ko) => {
    const r = indexedDB.open('gb-samples', 1);
    r.onupgradeneeded = () => r.result.createObjectStore('voices');
    r.onerror = () => ko(r.error);
    r.onsuccess = () => {
      const tx = r.result.transaction('voices', mode), q = fn(tx.objectStore('voices'));
      tx.oncomplete = () => ok(q && q.result); tx.onerror = () => ko(tx.error);
    };
  });
}
const decode = bytes => new OfflineAudioContext(1, 1, 44100).decodeAudioData(bytes.slice(0));
async function loadSample(vi, file) {
  if (file.size > 10e6) return notice(file.name + ': más de 10 MB');  // shortcut: limite fijo, subirlo si hace falta
  const bytes = await file.arrayBuffer();
  let buf; try { buf = await decode(bytes); } catch (e) { return notice('No se puede leer ' + file.name + ' como audio'); }
  SAMPLES[vi] = {name: file.name, buf, bytes, gainDb: SAMPLES[vi] ? SAMPLES[vi].gainDb : 0};
  saveSample(vi); sampleVer++; refreshSamples(); scheduleCache();
}
function saveSample(vi) {
  const x = SAMPLES[vi];
  idb('readwrite', o => o.put({vi, name: x.name, bytes: x.bytes, gainDb: x.gainDb}, vi))
    .catch(() => notice('Sin IndexedDB: el sample no se guardará al recargar'));
}
function clearSample(vi) {
  SAMPLES[vi] = null; sampleVer++; refreshSamples(); scheduleCache();
  idb('readwrite', o => o.delete(vi)).catch(() => {});
}
function refreshSamples() {
  sampleUI.forEach(({lab, gn}, vi) => {
    const x = SAMPLES[vi];
    lab.textContent = x ? x.name : 'kit'; lab.title = x ? x.name : ''; gn.disabled = !x; gn.value = x ? x.gainDb : 0;
  });
  const n = document.getElementById('snote'), on = DATA.voices.filter((v, vi) => SAMPLES[vi]);
  n.hidden = !on.length; n.textContent = on.length ? 'samples propios: ' + on.join(', ') : '';
}
idb('readonly', o => o.getAll()).then(async rows => {
  for (const r of rows || []) { try { SAMPLES[r.vi] = {name: r.name, bytes: r.bytes, gainDb: r.gainDb, buf: await decode(r.bytes)}; } catch (e) {} }
  sampleVer++; refreshSamples();
}).catch(() => {});

// ---- exportar WAV: render offline con la misma logica que tick
const exp = {bars: 2, wrap: true}, PART = ['INTRO', 'INTRO', 'ENERGIA', 'ENERGIA', 'BASE', 'BASE', 'VARIACION', 'VARIACION', 'FILL'];
function inContext(ctx, fn) {
  // los ladrillos de sintesis usan los globales del contexto en directo; se cambian solo durante esta
  // llamada sincrona (el planificador en directo no puede ejecutarse en medio) y se restauran siempre
  const saved = [ac, noiseBuf, FXB], fx0 = {...FX}, ch0 = {...choke};
  for (const k in FX) delete FX[k]; for (const k in choke) delete choke[k];
  ac = ctx; FXB = null; noiseBuf = ctx.createBuffer(1, ctx.sampleRate, ctx.sampleRate);
  const d = noiseBuf.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
  try { fn(); } finally {
    [ac, noiseBuf, FXB] = saved;
    for (const k in FX) delete FX[k]; Object.assign(FX, fx0);
    for (const k in choke) delete choke[k]; Object.assign(choke, ch0);
  }
}
const bpmOf = (st, s) => bpmFor === st && bpmOverride || s.bpm;
async function renderWav(st, getBar, nBars, wrap) {
  const SR = 44100;
  let len = 0; for (let b = 0; b < nBars; b++) len += 240 / bpmOf(st, getBar(b).st);
  const frames = Math.round(len * SR), extra = wrap ? Math.round(240 / bpmOf(st, st) * SR) : 0;
  const off = new OfflineAudioContext(2, frames + extra, SR);
  inContext(off, () => {
    bus(); FXB.dl.delayTime.value = 0.75 * 60 / bpmOf(st, st);
    const d = +dens.value; let t0 = 0;
    for (let b = 0; b < nBars; b++) {
      const cur = getBar(b), bpm = bpmOf(st, cur.st), amt = cur.st.amt || Array(NV).fill(100);
      for (let i = 0; i < STEPS; i++) for (let vi = 0; vi < NV; vi++) {
        const v = cur.val(vi, i);
        if (audible(vi) && v && 256 - v < d) playVoice(cur.st, vi, t0 + stepTime(i, bpm, amt[vi]), v);
      }
      t0 += 240 / bpm;
    }
  });
  const buf = await off.startRendering();
  return [0, 1].map(c => {  // colas envueltas: lo que pasa del final se suma al principio
    const d = buf.getChannelData(c), o = d.slice(0, frames);
    for (let i = frames; i < d.length; i++) o[(i - frames) % frames] += d[i];
    return o;
  });
}
function wav(ch) {  // PCM 16 bits, 44,1 kHz, estereo, con dither triangular
  const n = ch[0].length, buf = new ArrayBuffer(44 + n * 4), v = new DataView(buf);
  const str = (o, x) => [...x].forEach((c, i) => v.setUint8(o + i, c.charCodeAt(0)));
  str(0, 'RIFF'); v.setUint32(4, 36 + n * 4, true); str(8, 'WAVE'); str(12, 'fmt '); v.setUint32(16, 16, true);
  v.setUint16(20, 1, true); v.setUint16(22, 2, true); v.setUint32(24, 44100, true); v.setUint32(28, 44100 * 4, true);
  v.setUint16(32, 4, true); v.setUint16(34, 16, true); str(36, 'data'); v.setUint32(40, n * 4, true);
  for (let i = 0, o = 44; i < n; i++) for (let c = 0; c < 2; c++, o += 2)
    v.setInt16(o, Math.max(-32768, Math.min(32767, Math.round(ch[c][i] * 32767 + Math.random() - Math.random()))), true);
  return new Uint8Array(buf);
}
const CRC = Uint32Array.from({length: 256}, (_, n) => { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; return c >>> 0; });
const crc32 = b => { let c = 0xffffffff; for (let i = 0; i < b.length; i++) c = CRC[(c ^ b[i]) & 255] ^ (c >>> 8); return (c ^ 0xffffffff) >>> 0; };
function zip(files) {  // ZIP sin compresion (store); nombres en UTF-8
  const enc = new TextEncoder(), out = [], cen = []; let off = 0;
  for (const f of files) {
    const nm = enc.encode(f.name), crc = crc32(f.data), n = f.data.length, h = new DataView(new ArrayBuffer(30)), c = new DataView(new ArrayBuffer(46));
    h.setUint32(0, 0x04034b50, true); h.setUint16(4, 20, true); h.setUint16(6, 0x0800, true); h.setUint16(12, 33, true);
    h.setUint32(14, crc, true); h.setUint32(18, n, true); h.setUint32(22, n, true); h.setUint16(26, nm.length, true);
    c.setUint32(0, 0x02014b50, true); c.setUint16(4, 20, true); c.setUint16(6, 20, true); c.setUint16(8, 0x0800, true); c.setUint16(14, 33, true);
    c.setUint32(16, crc, true); c.setUint32(20, n, true); c.setUint32(24, n, true); c.setUint16(28, nm.length, true); c.setUint32(42, off, true);
    out.push(new Uint8Array(h.buffer), nm, f.data); cen.push(new Uint8Array(c.buffer), nm);
    off += 30 + nm.length + n;
  }
  const size = cen.reduce((a, b) => a + b.length, 0), e = new DataView(new ArrayBuffer(22));
  e.setUint32(0, 0x06054b50, true); e.setUint16(8, files.length, true); e.setUint16(10, files.length, true); e.setUint32(12, size, true); e.setUint32(16, off, true);
  return new Blob([...out, ...cen, new Uint8Array(e.buffer)], {type: 'application/zip'});
}
const bpmTag = st => bpmFor === st && bpmOverride && bpmOverride !== st.bpm ? ' ' + bpmOverride + ' BPM' : '';
const wavName = (st, k) => st.name + ' p' + k + ' ' + PART[k] + bpmTag(st) + '.wav';
function save(blob, name) {
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name; a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}
// cache por parte: DownloadURL necesita los datos en dragstart y el render es asincrono, asi que se prepara antes
let wavCache = [], wavUI = [], cacheTimer = 0, filling = false, refill = false;
const settingsKey = (st, k) => JSON.stringify([st.name, k, exp.bars, exp.wrap, dens.value, swing.value, bpmFor === st && bpmOverride,
                                               kitOf(st), mute, solo, FXI.map(r => r.value), sampleVer]);
const partWav = async (st, k) => new Blob([wav(await renderWav(st, () => barOf(st, st.p[k], null), exp.bars, exp.wrap))], {type: 'audio/wav'});
const partBlob = (st, k) => wavCache[k] && wavCache[k].key === settingsKey(st, k) ? wavCache[k].blob : partWav(st, k);
function scheduleCache() {
  clearTimeout(cacheTimer); cacheTimer = setTimeout(fillCache, 300);
  if (current) wavUI.forEach((h, k) => { if (h && !(wavCache[k] && wavCache[k].key === settingsKey(current, k))) { h.textContent = '…'; h.draggable = false; } });
}
async function fillCache() {
  if (filling) { refill = true; return; }
  filling = true;
  try {
    for (let k = 0; k < 9; k++) {
      const st = current, ui = wavUI[k];
      if (!st || !zoom.open || !ui) continue;
      const key = settingsKey(st, k);
      if (wavCache[k] && wavCache[k].key === key) continue;
      ui.textContent = '…'; ui.draggable = false;
      const blob = await partWav(st, k);
      if (current !== st || settingsKey(st, k) !== key) { refill = true; break; }  // cambio mientras renderizaba
      const url = await new Promise(ok => { const fr = new FileReader(); fr.onload = () => ok(fr.result); fr.readAsDataURL(blob); });
      wavCache[k] = {key, blob, url}; ui.textContent = '⠿ WAV'; ui.draggable = true;
    }
  } finally { filling = false; if (refill) { refill = false; scheduleCache(); } }
}
function wavButtons(st, k, cap) {
  const dl = playButton('⬇', async () => save(await partBlob(st, k), wavName(st, k))); dl.title = 'Descargar el WAV de esta parte';
  const h = document.createElement('span'); h.className = 'play drag'; h.textContent = '…'; h.draggable = false;
  h.title = 'Arrastra el WAV de esta parte al escritorio o a tu DAW';
  h.addEventListener('dragstart', e => {
    const c = wavCache[k];
    if (!c || c.key !== settingsKey(st, k)) { e.preventDefault(); scheduleCache(); return; }
    e.dataTransfer.setData('DownloadURL', 'audio/wav:' + wavName(st, k) + ':' + c.url);
  });
  cap.append(dl);
  if (canDrag) { wavUI[k] = h; cap.append(h); }
}
for (const ev of ['input', 'change', 'click']) document.addEventListener(ev, () => { if (zoom.open) scheduleCache(); });
zoom.addEventListener('close', () => { wavCache = []; });

// ---- MIDI: dos compases de lo que se oye (Density y swing aplicados), SMF tipo 0
const GM = [36, 38, 39, 42, 46, 50, 45];
let useGM = false, current = null;
function vlq(n) { const b = [n & 127]; while ((n >>= 7)) b.unshift((n & 127) | 128); return b; }
function midiFile(st) {
  const getBar = play && play.st === st ? play.getBar : (b => barOf(st, st.p[4 + b % 2], null));
  const amt = st.amt || Array(NV).fill(100), d = +dens.value, PPQ = 480, ev = [];
  for (let bar = 0; bar < 2; bar++) {
    const cur = getBar(bar);
    for (let vi = 0; vi < NV; vi++) for (let i = 0; i < STEPS; i++) {
      const v = cur.val(vi, i);
      if (!audible(vi) || !v || 256 - v >= d) continue;
      const t = Math.round((bar * 4 + stepTime(i, 60, amt[vi])) * PPQ);  // stepTime a 60 BPM = negras
      const note = useGM ? GM[vi] : 36 + vi;
      ev.push([t, 0x99, note, 100], [t + PPQ / 8, 0x89, note, 0]);
    }
  }
  ev.sort((a, b) => a[0] - b[0] || (a[1] === 0x89 ? -1 : 1));
  const us = Math.round(60000000 / (bpmFor === st && bpmOverride || st.bpm)), trk = [0, 0xff, 0x51, 3, us >> 16 & 255, us >> 8 & 255, us & 255];
  let last = 0;
  for (const [t, s, n, vel] of ev) { trk.push(...vlq(t - last), s, n, vel); last = t; }
  trk.push(...vlq(Math.max(0, 8 * PPQ - last)), 0xff, 0x2f, 0);
  const len = trk.length;
  return new Uint8Array([0x4d, 0x54, 0x68, 0x64, 0, 0, 0, 6, 0, 0, 0, 1, PPQ >> 8, PPQ & 255,
                         0x4d, 0x54, 0x72, 0x6b, len >>> 24, len >> 16 & 255, len >> 8 & 255, len & 255, ...trk]);
}
const canDrag = /Chrome|Edg\\//.test(navigator.userAgent);  // DownloadURL solo existe en Chromium
const GH = 'https://github.com/TOAST3R/genderbender/blob/main/';
function zoomTools(st) {
  const t = document.getElementById('ztools'); t.textContent = '';
  const dl = playButton('⬇ .mid', () => {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([midiFile(st)], {type: 'audio/midi'}));
    a.download = st.name + '.mid'; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  });
  t.append(dl);
  if (canDrag) {
    const h = document.createElement('span'); h.className = 'play drag'; h.draggable = true;
    h.textContent = '⠿ arrastrar MIDI'; h.title = 'Arrastra el .mid al escritorio o a tu DAW';
    h.addEventListener('dragstart', e => {
      const bytes = midiFile(st); let bin = '';
      bytes.forEach(x => bin += String.fromCharCode(x));
      e.dataTransfer.setData('DownloadURL', 'audio/midi:' + st.name + '.mid:data:audio/midi;base64,' + btoa(bin));
    });
    t.append(h);
  }
  const gm = document.createElement('label'), cb = document.createElement('input');
  cb.type = 'checkbox'; cb.checked = useGM; cb.addEventListener('change', () => { useGM = cb.checked; });
  gm.append(cb, ' GM'); gm.title = 'Notas de General MIDI en lugar de las del plugin (36 + voz)'; t.append(gm);
  const slider = (label, id, src, min, max) => {
    const l = document.createElement('label'), r = document.createElement('input'), o = document.createElement('output');
    r.type = 'range'; r.id = id; r.min = min; r.max = max; r.value = src.value; o.id = id + 'v'; o.value = src.value;
    r.addEventListener('input', () => { src.value = r.value; src.dispatchEvent(new Event('input')); });
    l.append(label + ' ', r, o); t.append(l);
  };
  slider('Density', 'zdens', dens, 0, 260);
  slider('Swing', 'zswing', swing, 50, 75);
  if (!play && bpmFor !== st) setBpmSlider(st.bpm);
  slider('BPM', 'zbpm', bpmI, 40, 240);
  const rb = playButton('↺', resetBpm); rb.title = 'Volver al BPM del estilo'; t.lastChild.append(rb);
  for (const src of FXI) {
    const l = document.createElement('label'), r = document.createElement('input'), d = document.createElement('span'), o = document.createElement('output');
    l.className = 'knob'; d.className = 'disc';
    r.type = 'range'; r.id = 'z' + src.id; r.min = 0; r.max = 100; r.value = src.value; o.id = r.id + 'v'; o.value = src.value;
    r.addEventListener('input', () => { if (src.value !== r.value) { src.value = r.value; src.dispatchEvent(new Event('input')); } });
    l.append(src.parentNode.firstChild.textContent, r, d, o); t.append(l); knob(r);
  }
  const kl = document.createElement('label'), ks = document.createElement('select');
  ks.id = 'zkit'; fillKits(ks); kl.append('Kit ', ks); t.append(kl); showAuto(st);
  const bl = document.createElement('label'), bs = document.createElement('select');
  [1, 2, 4, 8].forEach(n => bs.append(new Option(n, n))); bs.value = exp.bars;
  bs.addEventListener('change', () => { exp.bars = +bs.value; });
  bl.append('WAV: compases ', bs); bl.title = 'Compases de cada parte al exportar WAV (16 bits, 44,1 kHz)'; t.append(bl);
  const wl = document.createElement('label'), wc = document.createElement('input');
  wc.type = 'checkbox'; wc.checked = exp.wrap; wc.addEventListener('change', () => { exp.wrap = wc.checked; });
  wl.append(wc, ' colas envueltas'); wl.title = 'Suma la cola de reverb y delay al principio para que el loop empalme'; t.append(wl);
  const busy = (b, fn) => async () => { const txt = b.textContent; b.textContent = '…'; b.disabled = true; try { await fn(); } finally { b.textContent = txt; b.disabled = false; } };
  const sq = playButton('⬇ secuencia .wav', () => {}); sq.onclick = busy(sq, async () => {
    const seq = [0, 1, 4, 5, 2, 3, 6, 7, 8, 8].filter(k => !isEmpty(st.p[k]));
    save(new Blob([wav(await renderWav(st, b => barOf(st, st.p[seq[b]], null), seq.length, exp.wrap))], {type: 'audio/wav'}), st.name + ' secuencia' + bpmTag(st) + '.wav');
  });
  const zp = playButton('⬇ partes .zip', () => {}); zp.onclick = busy(zp, async () => {
    const files = [];
    for (let k = 0; k < 9; k++) if (!isEmpty(st.p[k])) files.push({name: wavName(st, k), data: new Uint8Array(await (await partBlob(st, k)).arrayBuffer())});
    save(zip(files), st.name + bpmTag(st) + '.zip');
  });
  t.append(sq, zp);
  const link = (txt, href) => { const a = document.createElement('a'); a.href = href; a.textContent = txt; a.target = '_blank'; a.rel = 'noopener'; t.append(a); };
  link('.txt ↗', GH + 'drum_styles_v/' + encodeURIComponent(st.name) + '.txt');
  if (st.src) link('.style ↗', GH + 'styles_src/' + encodeURIComponent(st.src) + '.style');
}

// ---- permalink: #style=…&density=…&fam=…
function fillKits(sel) {
  sel.textContent = '';
  sel.append(new Option('Auto', 'auto'));
  for (const [id, k] of Object.entries(KITS)) sel.append(new Option(k.label, id));
  sel.value = kitChoice;
  sel.addEventListener('change', () => setKit(sel.value));
}
function setKit(v) {
  kitChoice = KITS[v] ? v : 'auto';
  try { localStorage.setItem('gb-kit', kitChoice); } catch (e) {}
  for (const id of ['kit', 'zkit']) { const s = document.getElementById(id); if (s) s.value = kitChoice; }
  showAuto(play ? play.cur && play.cur.st : current);
  writeHash();
}
function showAuto(st) {  // "Auto (909)": que kit esta usando Auto
  const k = st ? KITS[FAM_KIT[FAMILY[st.name]] || 'actual'].label : '';
  for (const id of ['kit', 'zkit']) {
    const s = document.getElementById(id);
    if (s && s.options.length) s.options[0].textContent = k ? 'Auto (' + k + ')' : 'Auto';
  }
}

function syncZoom() {  // los controles de la vista ampliada siguen a los de la cabecera
  for (const [id, src] of [['zdens', dens], ['zswing', swing], ['zbpm', bpmI], ...FXI.map(x => ['z' + x.id, x])]) {
    const r = document.getElementById(id);
    if (r) {
      r.value = src.value; document.getElementById(id + 'v').value = src.value;
      if (r.nextElementSibling.classList.contains('disc')) r.nextElementSibling.style.setProperty('--v', r.value);
    }
  }
}

function writeHash() {
  const q = new URLSearchParams();
  if (fam.value) q.set('fam', fam.value);
  if (+dens.value !== 50) q.set('density', dens.value);
  if (kitChoice !== 'auto') q.set('kit', kitChoice);
  if (bpmOverride != null && bpmFor) q.set('bpm', bpmOverride);
  FXI.forEach(r => { if (+r.value) q.set(r.id, r.value); });
  if (current) q.set('style', current.name);
  history.replaceState(null, '', q.toString() ? '#' + q.toString() : location.pathname + location.search);
}

const fam = document.getElementById('fam'), count = document.getElementById('count');
const lazy = new IntersectionObserver(entries => entries.forEach(e => {
  if (e.isIntersecting) { lazy.unobserve(e.target); e.target._paint(); }
}), {rootMargin: '400px'});
const total = DATA.groups.reduce((n, g) => n + g.styles.length, 0), sections = [];
fam.append(new Option('Todos (' + total + ')', ''));
for (const grp of DATA.groups) {
  fam.append(new Option(grp.family + ' (' + grp.styles.length + ')', grp.family));
  const sec = document.createElement('section'); sec.dataset.fam = grp.family; sections.push(sec);
  const h = document.createElement('h2'); h.textContent = grp.family; sec.append(h); main.append(sec);
  for (const st of grp.styles) {
    const el = document.createElement('div');
    el.className = 'style'; el.tabIndex = 0; el.setAttribute('role', 'button');
    el.setAttribute('aria-label', 'Ampliar ' + st.name);
    const n = document.createElement('div'); n.className = 'name'; n.textContent = st.name;
    const bpm = document.createElement('span'); bpm.className = 'bpm'; bpm.textContent = st.bpm + ' BPM';
    const strip = document.createElement('div'); strip.className = 'strip';
    const pats = [];
    st.p.forEach((hex, i) => {
      const w = document.createElement('div'); w.className = 'pat'; w.title = 'p' + i;
      if (i === 8 && !/[^0]/.test(hex)) w.classList.add('empty');
      strip.append(w); pats.push(w);
    });
    // los canvas se crean al acercarse a la pantalla (render perezoso)
    el._paint = () => st.p.forEach((hex, i) => pats[i].append(pattern(hex, 3)));
    lazy.observe(el);
    // la BASE: p4 en el compas 1 y p5 en el 2, como el plugin
    n.append(bpm, playButton('▶ Play', b => start(b, '▶ Play', [st.p[4], st.p[5]], [pats[4], pats[5]], st, false)));
    el.append(n, strip); sec.append(el);
    el.addEventListener('click', () => openZoom(st));
    el.addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); openZoom(st); } });
  }
}

function filter() {
  const f = fam.value;
  sections.forEach(sec => { sec.hidden = !!f && sec.dataset.fam !== f; });
  const shown = f ? DATA.groups.find(g => g.family === f).styles.length : total;
  count.value = f ? shown + ' de ' + total + ' estilos' : total + ' estilos';
}
fam.addEventListener('change', () => { filter(); writeHash(); drawScene(0, true); }); filter();

const redraw = () => { canvases.forEach(draw); zoomed.forEach(draw); };
dens.addEventListener('input', () => { densv.value = dens.value; redraw(); writeHash(); syncZoom(); });
{  // aplicar el permalink al cargar: genero, Density y estilo
  const q = new URLSearchParams(location.hash.slice(1));
  if (q.has('fam') && DATA.groups.some(g => g.family === q.get('fam'))) { fam.value = q.get('fam'); filter(); }
  let saved = null; try { saved = localStorage.getItem('gb-kit'); } catch (e) {}
  kitChoice = KITS[q.get('kit')] ? q.get('kit') : (KITS[saved] ? saved : 'auto');
  fillKits(document.getElementById('kit'));
  let fxv = null; try { fxv = JSON.parse(localStorage.getItem('gb-fx')); } catch (e) {}
  if (FXI.some(r => q.has(r.id))) fxv = FXI.map(r => parseInt(q.get(r.id), 10) || 0);  // el permalink manda entero
  if (Array.isArray(fxv)) FXI.forEach((r, i) => {
    const v = Math.max(0, Math.min(100, +fxv[i] || 0));
    r.value = document.getElementById(r.id + 'v').value = v; r.nextElementSibling.style.setProperty('--v', v);
  });
  const d = parseInt(q.get('density'), 10);
  if (d >= 0 && d <= 260) { dens.value = densv.value = d; redraw(); }
  const st = DATA.groups.flatMap(g => g.styles).find(s => s.name === q.get('style'));
  if (st) openZoom(st);
  const b = parseInt(q.get('bpm'), 10);
  if (st && b >= 40 && b <= 240) { bpmOverride = b; bpmFor = st; setBpmSlider(b); writeHash(); }
  drawScene(0, true);
}
matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => { redraw(); S.pal = null; drawScene(0, true); });
</script>
</body>
</html>
'''


if __name__ == '__main__':
    try:
        html = render()
    except StyleError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8', newline='') as f:
        f.write(html)
    print(os.path.relpath(OUT, ROOT))
