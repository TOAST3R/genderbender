## Context

Un paso suena si `256 − v < Density`, con el slider de Density entre 0 y 260 y 50 por defecto. El valor de un paso no es una probabilidad sino el umbral de Density a partir del cual entra.

- Los estilos antiguos de `drum_styles_v/` usan sobre todo 255/170/85, más algunos valores sueltos (128, 64, 191…).
- La escala actual del formato `.style` es `X=255 x=170 o=120 -=60`.
- `decode` emite `[n]` para todo valor que no esté en la escala, lo que garantiza el round-trip byte a byte.

## Goals / Non-Goals

**Goals:**
- Escala de 5 niveles equiespaciados para escribir estilos nuevos con escalones regulares de Density.
- `decode` produce una cuadrícula legible con solo símbolos de la escala.

**Non-Goals:**
- Reescribir ni recuantizar los `.txt` existentes.
- Cambiar el plugin o la semántica de Density.
- Probabilidad real (aleatoriedad por paso).

## Decisions

- **Escala `X=255 x=204 o=153 -=102 ,=51 .=0` (paso 51).**
  - Los umbrales de entrada quedan en Density >1, >52, >103, >154 y >205, repartidos por todo el recorrido del slider.
  - Se conservan los símbolos `X x o -` con nuevos valores en lugar de inventar cinco nuevos, para que la lectura "mayúscula = esencial, punto = silencio" siga igual.
  - `,` se lee como "casi nada", entre `-` y `.`.
- **El snap de `decode` es `round(v / 51) * 51`.**
  - Con niveles a distancia 51, ningún entero cae justo en el punto medio, así que no hay empates que resolver.
  - Alternativa descartada: mantener `[n]` para los valores fuera de escala. El usuario pidió snap.
- **Las cumbias se congelan con `[n]`.**
  - Sus fuentes usan `x/o/-` con los valores viejos (170/120/60). Se reescriben como `[170]/[120]/[60]` para que `build` siga generando sus `.txt` idénticos.
  - Alternativa descartada: dejar que se reconstruyan con la escala nueva, porque cambiaría cuándo entran sus adornos. Eso contradice la decisión de no tocar los estilos existentes.
- **`build` no cambia**, salvo por la escala. `[n]` sigue disponible para valores exactos.

## Risks / Trade-offs

- **[Riesgo]** `decode` deja de ser reversible: decodificar y reconstruir un estilo antiguo da otro `.txt`. Por ejemplo, 170 pasa a 153 y entra con Density ≥104 en lugar de ≥87.
  → Mitigación: los `.txt` existentes no se tocan; `decode` es solo un punto de partida para estilos nuevos. Si se reconstruye uno, debe guardarse con otro nombre.
- **[Riesgo]** Los valores de 1 a 25 se ajustan a `.` y desaparecen. Solo sonaban con Density ≥231.
  → Aceptado. Afecta a unas pocas decenas de pasos en total.
- **[Riesgo]** Una fuente `.style` antigua que use `x/o/-` cambia de significado sin aviso.
  → Las únicas fuentes que existen son las cinco cumbias, y se migran en este cambio.
