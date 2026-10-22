## Context

Los estilos son `.txt` de una línea que `tools/make_style.py` ya sabe leer (`from_txt` devuelve `data[voz][patrón][paso]`, 7 × 9 × 32, valores 0–255). En el plugin un paso suena si `256 − v < Density` (Density por voz, 0–260, por defecto 50), así que un patrón es un mapa de alturas y no una lista de golpes. El repo no tiene web ni `docs/`. GitHub no ejecuta HTML dentro del repo, así que la página se publica con GitHub Pages desde `main /docs`.

## Goals / Non-Goals

**Goals:**
- Ver todos los estilos y sus 9 patrones en una sola página, agrupados por familia.
- Ver qué sonaría con un valor de Density dado.
- Que la página publicada no pueda quedarse desfasada sin que `check_styles.py` lo diga.

**Non-Goals:**
- Audio, pad XY y morph entre patrones (la geometría de sectores de `kdrumFunc` sigue sin aclarar).
- Swing, slide, break, división y duración.
- Editar estilos desde la página.
- Leer `presets/` o `styles_src/`: solo cuenta lo que carga el plugin.

## Decisions

**Un script Python que escribe un HTML estático con los datos incrustados.** Reutiliza `from_txt` y `ROOT` de `make_style.py`, como hace `check_styles.py`. Los datos van como JSON en un `<script>` y la página los pinta con JS en `<canvas>` (un canvas por patrón, 7 × 32 celdas). Alternativas: SVG generado en Python (pesado: 31 × 9 × 224 rectángulos y el slider tendría que tocar miles de nodos) o una página que lea los `.txt` con `fetch` (en Pages funcionaría, pero no abriendo el archivo en local y obliga a publicar `drum_styles_v/`).

**Salida determinista.** `view_styles.py` expone una función `render()` que devuelve el HTML como cadena: estilos en orden alfabético, sin fecha ni rutas absolutas. `check_styles.py` compara `render()` con `docs/fingerprints.html` y, si no coincide, da el error "docs/fingerprints.html desfasado (ejecuta tools/view_styles.py)". Alternativa descartada: un workflow de GitHub Actions que la regenere al hacer push; añade infraestructura para algo que un comando local ya resuelve.

**Familias leídas del README.** Se parsean las filas de la tabla bajo `## Included styles` (`| Familia | nombre (bpm), … |`). Un `.txt` pertenece a una entrada si su nombre es igual al de la entrada sin el `(bpm)` final, o a ese nombre más `" <bpm>"` (el README escribe `CUMBIA COLOMBIANA (95)` y el archivo es `CUMBIA COLOMBIANA 95`). Los estilos sin entrada van a "Other". Así la tabla del README sigue siendo la única lista de familias. Alternativa: un diccionario en el script, que habría que mantener junto al README.

**Color y Density.** Cada celda usa una rampa de un solo tono según `v / 255` (0 = fondo). El slider (0–260, valor inicial 50, como el plugin) no cambia el color: las celdas con `256 − v ≥ Density` bajan de opacidad. Una celda con valor 0 nunca suena (`256 ≥ Density` siempre que Density ≤ 256). Se respetan los temas claro y oscuro con `prefers-color-scheme`.

**Ampliar.** Clic (o Enter con foco) en una tira abre un panel con los 9 patrones a tamaño grande, con nombres de voz y marcas de compás cada 8 pasos; Escape o clic fuera lo cierra. Sin rutas ni historial.

**p8 vacío.** Si las 7 voces del p8 son 0, la miniatura muestra la etiqueta "FILL vacío" en lugar de un cuadro negro.

## Risks / Trade-offs

- [El HTML versionado se queda desfasado al cambiar estilos] → `check_styles.py` falla hasta que se regenere, y AGENTS.md ya exige ejecutarlo tras cualquier cambio de estilos.
- [El parseo del README se rompe si cambia el formato de la tabla] → los estilos caen en "Other" en vez de fallar; la página sigue siendo válida. Se nota a simple vista.
- [Tamaño] 31 estilos × 2016 valores ≈ 62 000 números, unos 250 KB de JSON. Aceptable para Pages; si crece mucho, se puede codificar cada patrón en hex.
- [Pages no está activado] → la página no se publica hasta que el usuario lo active y haga push. Hasta entonces se puede abrir `docs/fingerprints.html` en local.

## Migration Plan

1. Generar `docs/fingerprints.html` y comprobar con `check_styles.py`.
2. El usuario hace push y activa Pages (`main`, `/docs`). URL: `https://toast3r.github.io/genderbender/fingerprints.html`.
3. Revertir es borrar `docs/`, `tools/view_styles.py` y la comprobación.

Sin cambios en el plugin, así que no hay nada que verificar en REAPER.

## Open Questions

- ¿`docs/index.html` en vez de `fingerprints.html`, para que la raíz del sitio no dé 404? Por ahora se sigue el nombre pedido.
