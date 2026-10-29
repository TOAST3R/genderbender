## 1. Audio independiente del contexto

- [x] 1.1 `inContext(ctx, fn)`: cambia y restaura los globales del audio durante el render offline (ver design.md); efectos sin rampa offline; un solo choke de hats
- [x] 1.2 Comprobar que el render offline coloca los golpes donde dice `stepTime` y que el directo no cambia

## 2. Samples

- [x] 2.1 Carga por botón y por soltar sobre el nombre de la voz; `decodeAudioData`; aviso si no decodifica
- [x] 2.2 Golpe con sample (ganancia × velocity) y choke hhc/hho; ✕ vuelve al kit; ganancia −24 a +6 dB
- [x] 2.3 IndexedDB (`gb-samples`/`voices`), límite de 10 MB, aviso si no hay IndexedDB; aviso "samples propios" en la cabecera

## 3. Exportar WAV

- [x] 3.1 Render offline con la lógica de `tick` (getBar, Density, mute/solo, swing, BPM efectivo) y colas envueltas
- [x] 3.2 Codificador WAV 16 bits / 44,1 kHz con dither y ZIP *store* con CRC32
- [x] 3.3 Panel: compases 1/2/4/8, colas envueltas, ⬇ secuencia, ⬇ todas las partes .zip; ⬇ por parte
- [x] 3.4 Caché en segundo plano por parte (300 ms tras cambios) y asa ⠿ WAV con `DownloadURL` (URL `data:`)

## 4. Verificación

- [x] 4.1 Regenerar `docs/fingerprints.html`; `python3 tools/check_styles.py` imprime `ok`; la página no carga recursos externos
- [x] 4.2 En un navegador (Playwright): las comprobaciones de `design.md` (samples e IndexedDB, cabecera y duración del WAV, empalme, posición de los golpes, ZIP con `unzip -t`, asa de arrastre)
- [ ] 4.3 Arrastrar un WAV a REAPER y probar samples reales (lo hace el usuario)
