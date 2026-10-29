## Why

La página de huellas pinta al cargar 2.061 canvas (229 estilos × 9 patrones) y pesa 940 KB: en un portátil tarda y en un móvil se nota mucho. Además, lo que se oye en la página no se puede llevar a ningún sitio: no hay forma de sacar un patrón a un DAW, ni de bajar su fuente, ni de compartir un estilo concreto con un enlace.

## What Changes

- **Render perezoso**: cada tira se pinta cuando entra en pantalla (`IntersectionObserver`), y Density solo repinta lo ya pintado.
- **MIDI**: en la vista ampliada, un botón **⬇ .mid** y un asa **⠿ arrastrar** que generan un archivo MIDI (SMF tipo 0) con dos compases de lo que se está oyendo: la BASE o el patrón elegido, con Density y swing aplicados. Las notas son las del plugin (nota base 36 + voz) y un interruptor cambia a General MIDI. El asa arrastra el archivo con `DownloadURL` (Chrome y Edge); en el resto de navegadores solo aparece el botón.
- **Fuentes**: en la vista ampliada, enlaces al `.txt` y, si existe, al `.style` del estilo en GitHub.
- **Density y swing en la vista ampliada**, sincronizados con los de la cabecera (que el diálogo tapa), y el contenido de la página centrado.
- **Permalink**: el hash de la URL guarda el estilo abierto, la Density y el género (`#style=SALSA 180&density=120&fam=Latin / Caribbean`); abrir ese enlace deja la página en ese estado.

## Capabilities

### New Capabilities

### Modified Capabilities
- `style-fingerprints`: render perezoso, exportación MIDI, enlaces a las fuentes y permalink.

## Impact

- `tools/view_styles.py` (plantilla y script; también pasa a la página qué estilos tienen fuente) y `docs/fingerprints.html` regenerado.
- Sin cambios en el plugin ni en los estilos. La página sigue siendo un solo archivo sin recursos externos: los enlaces a GitHub son enlaces, no se cargan.
- Prepara `add-fingerprints-pad-and-sequence`, que exportará también la mezcla del pad.
