## Context

- El preview de `docs/fingerprints.html` tiene un array `VOICE` con una función por voz (kick, snare, clap, hhc, hho, hitom, lotom) que recibe el tiempo y programa nodos de Web Audio: `tone()` (seno con caída de tono), `noise()` (ruido filtrado) y un hho que corta el hhc.
- El planificador (`tick`) llama a `VOICE[vi](t)` por cada paso que suena; cada compás lo da `getBar()`, que también dice de qué estilo es (A/B).
- La spec exige que la página sea un solo archivo sin recursos externos.

## Goals / Non-Goals

**Goals:**
- Que cada familia suene con un timbre que la represente, y poder probar cualquier estilo con cualquier kit.
- Cambiar de kit sin parar la reproducción.

**Non-Goals:**
- Samples reales o cargados de fuera (Freesound, CDN): rompen la regla de recursos externos.
- Kit por voz (mezclar voces de kits): más adelante.
- Afectar al MIDI exportado o al plugin.

## Decisions

- **`KITS[nombre]` = 7 funciones de voz**, construidas con ladrillos comunes: `tone()`, `noise()`, `metal()` (suma de 6 cuadradas en las frecuencias del 808 con paso banda, para hats y platos), `click()` (ataque corto), y una salida por kit con efectos opcionales: `crush` (reducción de bits con `WaveShaper` y paso bajo, para Lo-fi y Chiptune), `drive` (distorsión con `WaveShaper`, para Hardcore) y `gate` (cola de ruido cortada en seco, para la caja de 80s).
- **Recetas** (orientativas; se ajustan de oído durante la implementación):

  | Kit | Kick | Snare / clap | Hats | Toms |
  |---|---|---|---|---|
  | Actual | el de hoy | el de hoy | el de hoy | el de hoy |
  | 808 | seno 60→45 Hz, cola de 0,8 s | dos tonos 180/330 Hz + ruido; clap de 4 ráfagas | `metal()` corto (hhc) y largo (hho) | senos con caída larga; hitom = cencerro (cuadradas 540/800 Hz) |
  | 909 | seno 160→50 Hz con `click()` | ruido brillante + tono 200 Hz | ruido metálico con paso alto a 8 kHz | senos cortos |
  | Acústico | seno 90→55 Hz corto + ruido sordo | ruido largo con paso banda (bordonera) + tono 190 Hz | ruido a 6 kHz; hho como ride (más largo) | senos afinados 220/140 Hz con algo de ruido |
  | Lo-fi | el Acústico | ídem | ídem | ídem, todo por `crush` (8 bits, paso bajo a 4 kHz) |
  | Hardcore | seno 200→45 Hz por `drive` fuerte, cola de 0,5 s | clap seco | hats duros y cortos | — (como 909) |
  | 80s / Linn | seno corto y seco | ruido + tono con `gate` (corte a 0,18 s) | hats cortos | toms electrónicos (Simmons: seno con caída rápida y algo de ruido) |
  | Percusión | surdo (seno 80 Hz, largo) | claves (seno 2,5 kHz muy corto) y palmas | shaker (ruido con paso banda, ataque suave) y güiro | congas (senos 300/200 Hz con ataque de ruido); hitom = cencerro |
  | Chiptune | cuadrada 120→40 Hz | ruido de 1 bit (`crush` a 1 bit) | ruido corto de 1 bit | cuadradas |

- **Auto por familia**: una tabla `familia → kit` en la plantilla. Con "Auto", el kit es el de la familia del estilo del compás que suena (así A/B cambia de kit con el estilo). Tabla:
  - **909**: Techno, House, Hard house, Psytrance, Rave / oldskool, UK garage, Gqom.
  - **808**: R&B / trap, Electro, Bass music, Phonk, Footwork / juke, Reggaeton / funk carioca.
  - **Acústico**: Breaks, Drum & bass, Funk / New Orleans, Country / Americana, Reggae / dancehall.
  - **Lo-fi**: Hip-hop, Downtempo / chill.
  - **Hardcore**: Hardcore / hard dance.
  - **80s / Linn**: Synth / disco, EBM / industrial.
  - **Percusión**: Latin / Caribbean, Brazil, South America, Afro / Caribbean, Afro / Latin club, Cumbia, Flamenco, Folk ibérico, Celtic, World folk.
  - **Chiptune**: IDM / experimental.
  - **Actual**: Other.
- **Cambio en cualquier momento**: el planificador busca el kit en cada golpe (`kitFor(estilo)[vi](t)`), así que cambiar el selector afecta al golpe siguiente sin parar nada. El hho que corta el hhc se guarda por kit.
- **Selector** en la cabecera y en la vista ampliada (mismo patrón que Density y Swing: sincronizados); muestra "Auto (909)" cuando Auto está activo, para saber qué suena.
- **Persistencia**: `localStorage['gb-kit']` y el parámetro `kit` del permalink (el permalink manda si está).

## Risks / Trade-offs

- [CPU] El hat del 808 son 6 osciladores por golpe. → A 200 BPM con hats en semicorcheas son ~13 golpes por segundo; se mide en el navegador y, si hace falta, se comparte un único banco de osciladores.
- [Calidad] Acústico y Percusión sonarán a "batería sintetizada", no a grabación. → Es el precio de no cargar recursos; el texto de la cabecera ya dice "preview sintetizado".
- [Volumen] Los kits con `drive` suenan más fuerte. → Ganancia de salida por kit para igualar el nivel.

## Verificación

No toca el plugin. En un navegador (Playwright): los 9 kits existen y cada voz programa nodos; con Auto, un estilo de Techno usa 909 y uno de Latin / Caribbean usa Percusión; en A/B entre dos familias el kit cambia con el estilo; cambiar el selector mientras suena cambia el kit del golpe siguiente sin parar; el kit se guarda en `localStorage` y en el permalink; el MIDI exportado no cambia con el kit. A mano: escuchar los 9 kits.
