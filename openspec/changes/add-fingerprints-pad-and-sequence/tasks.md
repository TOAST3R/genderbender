## 1. Pad

- [ ] 1.1 `padMix()` con el orden de condiciones del sector y las cuatro fórmulas del plugin, y una prueba en el navegador contra p4/p5, p2/p3, p0/p1 y p8
- [ ] 1.2 Control del pad en la vista ampliada (arrastrable, de −100 a 100), leído en cada paso del planificador, con la nota "como en el plugin"

## 2. Secuencia, mute/solo y A/B

- [ ] 2.1 Botón de secuencia: INTRO → BASE → ENERGÍA → VARIACIÓN → FILL, saltando las partes vacías y marcando la que suena
- [ ] 2.2 Mute y solo por voz, aplicados al preview y al MIDI
- [ ] 2.3 A/B: selector de segundo estilo y alternancia cada dos compases con su BPM y su swing
- [ ] 2.4 Que el MIDI exporte la mezcla del pad y respete mute/solo

## 3. Verificación

- [ ] 3.1 Regenerar `docs/fingerprints.html`; `python3 tools/check_styles.py` imprime `ok`
- [ ] 3.2 En un navegador (Playwright): notas programadas en el centro, en los bordes y en (0, 1); secuencia sin partes vacías; solo de una voz; A/B con dos BPM
- [ ] 3.3 A mano: mover el pad de la página y el del plugin al mismo punto y comparar
