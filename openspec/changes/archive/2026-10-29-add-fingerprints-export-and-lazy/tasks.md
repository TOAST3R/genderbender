## 1. Render perezoso

- [x] 1.1 Crear los canvas de cada tira al entrar en pantalla (`IntersectionObserver`, margen de 400 px) y que `redraw()` recorra solo los creados
- [x] 1.2 Comprobar que la vista ampliada, el filtro de género y el preview siguen funcionando

## 2. MIDI

- [x] 2.1 Generador de SMF tipo 0 en JS (cabecera, tempo, notas de 1/32 en el tiempo del swing, fin de pista)
- [x] 2.2 Botón ⬇ .mid en la vista ampliada: exporta la BASE o el patrón que suena, con Density y swing
- [x] 2.3 Interruptor "GM" (notas 36, 38, 39, 42, 46, 50, 45) frente a las del plugin (36 + voz)
- [x] 2.4 Asa ⠿ arrastrable con `DownloadURL` solo en navegadores que lo admitan

## 3. Fuentes y permalink

- [x] 3.1 En `view_styles.py`, pasar en `DATA` el archivo `.style` de cada estilo que lo tiene
- [x] 3.2 Enlaces al `.txt` y al `.style` en GitHub desde la vista ampliada
- [x] 3.3 Permalink: actualizar el hash con `history.replaceState` y aplicarlo al cargar (género, Density, estilo)

## 3b. Controles y maquetación

- [x] 3.4 Density y swing en la vista ampliada, sincronizados con los de la cabecera (también cuando Play pone el swing de la receta)
- [x] 3.5 Centrar el contenido de la página

## 4. Verificación

- [x] 4.1 Regenerar `docs/fingerprints.html` con `python3 tools/view_styles.py`; `python3 tools/check_styles.py` imprime `ok`
- [x] 4.2 En un navegador (Playwright): menos canvas al cargar y más al bajar; el `.mid` de TRAIN BEAT 110 tiene 32 notas de snare y 4 de kick a 110 BPM; "GM" cambia el snare a la 38; un permalink abre el estilo con su Density y su género
- [ ] 4.3 A mano: arrastrar el asa al escritorio y a una pista de REAPER, y anotar si REAPER lo acepta
