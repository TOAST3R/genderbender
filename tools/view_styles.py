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
dialog::backdrop{background:rgba(0,0,0,.5)}
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
.mix{display:grid;grid-template-columns:auto auto auto;gap:2px 6px;align-items:center}
.play.on{background:var(--ink);color:var(--bg);border-color:var(--ink)}
</style>
</head>
<body>
<header>
<h1>GENDERBENDER · FINGERPRINTS</h1>
<a class="src" href="https://github.com/TOAST3R/genderbender">Código fuente ↗</a>
<label>Género <select id="fam"></select></label><output id="count"></output>
<label>Density <input id="dens" type="range" min="0" max="260" value="50"><output id="densv">50</output></label>
<label>Swing <input id="swing" type="range" min="50" max="75" value="50"><output id="swingv">50</output></label>
<span class="hint" style="margin:0">color = valor 0–255 · atenuado = no suena con esta Density · clic para ampliar · ▶ preview sintetizado (no es el sonido de tu sampler) · Esc para</span>
</header>
<main id="main"></main>
<dialog id="zoom"><h3 id="zname"></h3><div class="tools" id="ztools"></div><div class="zplay" id="zplay"></div><div class="big" id="zbody"></div><p class="hint">Esc o clic fuera para cerrar</p></dialog>
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
let ac = null, noiseBuf = null, openHat = null, play = null;
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
function tone(t, f0, f1, len, a) {
  const o = ac.createOscillator(), g = ac.createGain();
  o.frequency.setValueAtTime(f0, t); o.frequency.exponentialRampToValueAtTime(f1, t + len);
  env(g, t, a, len); o.connect(g).connect(ac.destination); o.start(t); o.stop(t + len);
}
function noise(t, type, freq, len, a) {
  const s = ac.createBufferSource(), f = ac.createBiquadFilter(), g = ac.createGain();
  s.buffer = noiseBuf; f.type = type; f.frequency.value = freq;
  env(g, t, a, len); s.connect(f).connect(g).connect(ac.destination); s.start(t); s.stop(t + len);
  return s;
}
const VOICE = [  // mismo orden que DATA.voices
  t => tone(t, 150, 45, 0.35, 1),
  t => { noise(t, 'highpass', 1000, 0.15, 0.5); tone(t, 180, 160, 0.1, 0.3); },
  t => { for (let k = 0; k < 3; k++) noise(t + k * 0.01, 'bandpass', 1200, k < 2 ? 0.02 : 0.12, 0.6); },
  t => { if (openHat) { openHat.stop(t); openHat = null; } noise(t, 'highpass', 7000, 0.05, 0.3); },
  t => { openHat = noise(t, 'highpass', 7000, 0.3, 0.25); },
  t => tone(t, 220, 160, 0.25, 0.6),
  t => tone(t, 140, 100, 0.3, 0.7),
];
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
        P.lastSt = P.cur.st; P.bpm = P.cur.st.bpm; P.amt = P.cur.st.amt || Array(NV).fill(100);
      }
      const t0 = Math.max(P.barStart, ac.currentTime), mark = P.cur.mark;
      setTimeout(() => { if (play === P) P.marks.forEach(m => m.classList.toggle('playing', m === mark)); }, (t0 - ac.currentTime) * 1000);
    }
    const d = +dens.value;
    for (let vi = 0; vi < NV; vi++) {
      if (!audible(vi)) continue;
      const v = P.cur.val(vi, P.step);
      // misma regla que el plugin; cada voz con su amount de swing
      if (v && 256 - v < d) VOICE[vi](Math.max(P.barStart + stepTime(P.step, P.bpm, P.amt[vi]), ac.currentTime));
    }
    if (++P.step === STEPS) { P.step = 0; P.bar++; P.barStart += 240 / P.bpm; }
  }
}
function stop() {
  if (!play) return;
  clearInterval(play.timer);
  play.btn.textContent = play.label; play.btn.setAttribute('aria-pressed', 'false');
  play.marks.forEach(m => m.classList.remove('playing'));
  play = null;
}
function start(btn, label, pats, marks, st, inZoom, getBar) {
  const same = play && play.btn === btn;
  stop();
  if (same) return;
  audio();
  swing.value = swingv.value = st.swing;  // la receta del estilo; se puede mover a mano mientras suena
  syncZoom();
  getBar = getBar || (b => barOf(st, pats[b % pats.length], marks[b % marks.length]));
  play = {btn, label, getBar, marks, st, bpm: st.bpm, amt: st.amt || Array(NV).fill(100), inZoom,
          bar: 0, step: 0, barStart: ac.currentTime + 0.05};
  btn.textContent = '■ Stop'; btn.setAttribute('aria-pressed', 'true');
  play.timer = setInterval(tick, 25); tick();
}
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
  st.p.forEach((hex, i) => {
    const f = document.createElement('figure'), cap = document.createElement('figcaption');
    figs.push(f);
    cap.textContent = 'p' + i + (i === 8 ? ' FILL' : '');
    cap.append(playButton('▶', b => start(b, '▶', [hex], [f], st, true)));
    const row = document.createElement('div'); row.className = 'row';
    const names = document.createElement('div'); names.className = 'voices';
    DATA.voices.forEach(v => { const e = document.createElement('span'); e.textContent = v; names.append(e); });
    row.append(names, pattern(hex, 10, zoomed)); f.append(cap, row); zbody.append(f);
  });
  zoomPlay(st, figs);
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
    mix.append(name, tg(mute, 'M'), tg(solo, 'S'));
  });
  z.append(box, col, mix);
}
zoom.addEventListener('click', e => { if (e.target === zoom) zoom.close(); });
zoom.addEventListener('close', () => { current = null; writeHash(); });

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
  const us = Math.round(60000000 / st.bpm), trk = [0, 0xff, 0x51, 3, us >> 16 & 255, us >> 8 & 255, us & 255];
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
  const link = (txt, href) => { const a = document.createElement('a'); a.href = href; a.textContent = txt; a.target = '_blank'; a.rel = 'noopener'; t.append(a); };
  link('.txt ↗', GH + 'drum_styles_v/' + encodeURIComponent(st.name) + '.txt');
  if (st.src) link('.style ↗', GH + 'styles_src/' + encodeURIComponent(st.src) + '.style');
}

// ---- permalink: #style=…&density=…&fam=…
function syncZoom() {  // los controles de la vista ampliada siguen a los de la cabecera
  for (const [id, src] of [['zdens', dens], ['zswing', swing]]) {
    const r = document.getElementById(id);
    if (r) { r.value = src.value; document.getElementById(id + 'v').value = src.value; }
  }
}

function writeHash() {
  const q = new URLSearchParams();
  if (fam.value) q.set('fam', fam.value);
  if (+dens.value !== 50) q.set('density', dens.value);
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
fam.addEventListener('change', () => { filter(); writeHash(); }); filter();

const redraw = () => { canvases.forEach(draw); zoomed.forEach(draw); };
dens.addEventListener('input', () => { densv.value = dens.value; redraw(); writeHash(); syncZoom(); });
{  // aplicar el permalink al cargar: genero, Density y estilo
  const q = new URLSearchParams(location.hash.slice(1));
  if (q.has('fam') && DATA.groups.some(g => g.family === q.get('fam'))) { fam.value = q.get('fam'); filter(); }
  const d = parseInt(q.get('density'), 10);
  if (d >= 0 && d <= 260) { dens.value = densv.value = d; redraw(); }
  const st = DATA.groups.flatMap(g => g.styles).find(s => s.name === q.get('style'));
  if (st) openZoom(st);
}
matchMedia('(prefers-color-scheme: dark)').addEventListener('change', redraw);
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
