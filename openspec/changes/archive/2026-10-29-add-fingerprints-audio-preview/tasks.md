## 1. Tempo

- [x] 1.1 Añadir `(bpm)` a las 35 entradas sin BPM de la tabla "Included styles" del README, con los valores de `design.md`
- [x] 1.2 En `tools/view_styles.py`, calcular el BPM de cada estilo (nombre → entrada del README → 120) y guardarlo en `DATA`

## 2. Audio

- [x] 2.1 En la plantilla, sintetizar las 7 voces con Web Audio (una función por voz, sin recursos externos)
- [x] 2.2 Planificador con look-ahead: paso de `60 / BPM / 8` s, Density leída en cada paso y swing con la deformación de `groove-swing`
- [x] 2.3 Botón Play/Stop y BPM en cada tira; p4/p5 alternando a cada compás; borde de acento en el patrón que suena
- [x] 2.4 ▶ por patrón en la vista ampliada; un patrón vacío no suena
- [x] 2.5 Una sola reproducción a la vez; Stop, Play en otro y Esc (con la vista ampliada cerrada) la paran
- [x] 2.6 Slider de swing (50–75) en la cabecera y nota "preview sintetizado"
- [x] 2.7 Leer swing y amount por voz de la cabecera de `styles_src/*.style`; al pulsar Play, poner el slider en el swing del estilo y aplicar el amount de cada voz

## 3. Documentación y verificación

- [x] 3.1 Regenerar `docs/fingerprints.html` con `python3 tools/view_styles.py`
- [x] 3.2 `python3 tools/check_styles.py` imprime `ok`
- [x] 3.3 En un navegador (Playwright): Play crea el audio y programa notas; Play en otro deja uno solo; Stop y Esc paran; el BPM mostrado sale del nombre o del README
- [x] 3.4 Mencionar el preview en el README, junto al enlace a la página de huellas
- [ ] 3.5 Escuchar varios estilos y comprobar que el ritmo coincide con la tira (lo hace el usuario)
