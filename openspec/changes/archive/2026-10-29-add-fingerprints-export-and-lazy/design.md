## Context

- `tools/view_styles.py` genera `docs/fingerprints.html`: los datos de todos los estilos van en JSON (`DATA.groups`, cada patrón en hex) y el script crea un `<canvas>` por patrón y los pinta todos al cargar (`pattern()` → `draw()`), además de los botones Play y el motor de audio del preview.
- El plugin envía cada voz en la nota `basenote + 7 × multiplicador + v` (slider 46 = 36 por defecto, `v` = 0…6 en el orden kick, snare, clap, hhc, hho, hitom, lotom).
- `check_styles.py` compara la página con lo que genera `view_styles.py`, así que cualquier cambio de plantilla obliga a regenerar.

## Goals / Non-Goals

**Goals:**
- Que la página cargue rápido aunque siga creciendo.
- Sacar a un DAW, como MIDI, lo que se oye en la página.
- Compartir un estilo con un enlace.

**Non-Goals:**
- El pad XY, la secuencia, mute/solo y A/B (van en `add-fingerprints-pad-and-sequence`).
- Velocidad por paso en el MIDI (el plugin usa velocidad fija por voz).
- Que el arrastre funcione en Firefox o Safari, que no tienen `DownloadURL`.

## Decisions

- **Render perezoso con `IntersectionObserver`**: cada tira guarda sus datos y un contenedor vacío; al entrar en pantalla (con un margen de 400 px) se crean y pintan sus 9 canvas. `redraw()` (Density, tema oscuro) recorre solo los canvas creados. La vista ampliada sigue pintándose entera al abrirse.
- **MIDI generado en JS**: SMF tipo 0, 480 ticks por negra, un evento de tempo con el BPM del estilo y dos compases de 4/4. Cada paso que suena (misma regla de Density que el preview) genera una nota de 1/32 de duración en el tiempo que le da el swing actual (`groove-swing`), con velocidad 100. Lo que se exporta es lo que suena: el par p4/p5 si se exporta la BASE, o el patrón elegido en la vista ampliada repetido dos compases.
- **Notas**: por defecto las del plugin, 36 + v (36 kick, 37 snare, 38 clap, 39 hhc, 40 hho, 41 hitom, 42 lotom), para que suene igual en el sampler que usa el plugin. Interruptor "GM": 36 kick, 38 snare, 39 clap, 42 hhc, 46 hho, 50 hitom, 45 lotom.
- **Descarga y arrastre**: el botón descarga un `Blob` como `<NOMBRE>.mid`. El asa es `draggable` y en `dragstart` pone `DownloadURL = audio/midi:<NOMBRE>.mid:<data URL>`. Si el navegador no lo admite (no es Chromium), el asa no se muestra.
- **Fuentes**: `view_styles.py` pasa en `DATA` el archivo `.style` de cada estilo que lo tiene (lo sabe por las cabeceras que ya lee para el swing). La vista ampliada enlaza a `https://github.com/TOAST3R/genderbender/blob/main/drum_styles_v/<NOMBRE>.txt` y, si hay fuente, a `…/styles_src/<archivo>.style`.
- **Permalink**: `history.replaceState` actualiza el hash al abrir o cerrar la vista ampliada y al cambiar Density o el género. Al cargar, se lee el hash y se aplica en ese orden: género, Density, estilo (abre su vista ampliada). Un estilo o género que no existe se ignora.

## Risks / Trade-offs

- [Arrastre al DAW sin probar] El archivo que suelta Chrome es una "promesa de archivo"; el escritorio y el Finder lo aceptan, pero no está comprobado que REAPER o Ableton lo acepten soltado directamente en una pista. → Se prueba en la verificación; el botón de descarga funciona siempre.
- [Búsqueda del navegador] Con el render perezoso, las tiras no pintadas no se ven al hacer scroll rápido hasta que se pintan (un instante). → Margen de 400 px.

## Verificación

No toca el plugin. En un navegador (Playwright): al cargar hay muchos menos canvas que 2.061 y al bajar aparecen más; el `.mid` descargado es un SMF válido con las notas esperadas para un estilo conocido (p. ej. TRAIN BEAT 110: 16 snare y 2 kick por compás con Density por defecto) y cambia de notas con "GM"; un permalink abre el estilo con su Density y su género. A mano: arrastrar el asa al escritorio y a una pista de REAPER.
