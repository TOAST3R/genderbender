# Design

## Context

Ver proposal.md para la motivación y las specs `melo-*` para los requisitos.

Algunas partes de gb_18 (`GenderBender/genderbender.jsfx`) sirven de referencia:
- Lee cada estilo con `file_open` sobre un slider de archivo (`slider1:/drum_styles_v:none:`), y el nombre de la carpeta es el de `Data/`.
- Mezcla 4 esquinas de 9 patrones por cuadrante (`sector`, `Xmap`, `Ymap`). El código se repite a mano para cada una de las 7 voces.
- Tiene una cola de eventos de 128 entradas con emisión sample-accurate, swing y slide (specs `note-scheduling`, `groove-swing`, `voice-slide`).
- Usa `rand()` de EEL2, que no admite semilla.
- El formato compilado es una sola línea de texto que se parsea como cadena. Es frágil: un error lo deja en silencio.

El plugin melódico es un archivo nuevo y no comparte código en tiempo de ejecución con gb_18. Sí copia de él sus algoritmos ya verificados.

## Goals / Non-Goals

**Goals:**
- Un motor con voces parametrizadas por índice (arrays y bucles), sin código duplicado por voz.
- Determinismo: misma semilla, mismo estado y misma posición del transporte producen las mismas notas, también después de un seek.
- Un formato compilado que el plugin pueda leer sin parsear cadenas y que el validador pueda comprobar por completo.

**Non-Goals:**
- Sincronizarse con gb_18 por `gmem` (queda para un cambio posterior).
- Seguir acordes tocados por MIDI in.
- Ilustrar el fondo de la interfaz. La v1 dibuja la GUI con primitivas `gfx_*`.
- La página de fingerprints para estilos melódicos.

## Decisions

### D1. Archivo, carpetas y nombres
- Plugin en `GenderBenderMelo/genderbender_melo.jsfx`, con `desc: MIDI GenderBender Melo`.
- Fuentes en `styles_melo_src/*.mstyle` y compilados en `melo_styles/*.txt`. Se instalan en `Data/melo_styles/`.
- Alternativa descartada: meter los estilos melódicos en `drum_styles_v/`. Mezclaría formatos, y `countStyles()` de gb_18 los contaría.

### D2. Formato compilado: solo números
El compilado es una lista de números separados por comas, una sección por línea, que el plugin lee en secuencia con `file_var` en modo texto. Probado en REAPER 7.75: el modo texto separa valores con comas o saltos de línea, y un espacio, un tabulador o un punto y coma cortan el resto de la línea.

```
MAGIC VERSION
cabecera:  bpm  pasos_por_compás(32|24)  tónica(0-11)  máscara_escala(12 bits)
           compases_por_acorde  longitud_ciclo  forma_frase[3 voces × 4]
armonía:   n_acordes  [raíz_semitonos  máscara_intervalos]×n     # tabla de acordes del estilo
           n_progresiones  [longitud  idx_acorde×longitud]×n
           markov  n×n pesos (0-255)
           sustituciones  [idx_origen  idx_destino]×m
voces:     3 × 9 patrones × 32 pasos × (ritmo  altura  articulación)
FIN        MAGIC
```

- Los acordes van como raíz en semitonos más máscara de 12 bits de intervalos. El plugin no necesita saber de números romanos: el compilador traduce `bII7`, `V7` o `VII` según la escala.
- La altura se codifica por voz: bajo, 0 = R, 1 = 3, 2 = 5, 3 = 7, 4 = 8, 5 = a; acordes, tipo de voicing 0–5; melodía, 0 = `=`, 1 = `+`, 2 = `-`, 3 = `^`.
- El `MAGIC` final permite que el plugin detecte un archivo truncado y lo rechace: muestra "estilo inválido" en la GUI en lugar de quedarse en silencio.
- Alternativa descartada: reutilizar el formato de una línea de gb_18. Exige parsear cadenas en EEL2 y no tiene sitio para la armonía.

### D3. Compilador y validador en Python
- `tools/make_melo_style.py build|decode` sigue el estilo de `make_style.py`: niveles `X x o - , .`, `[n]`, grupos `[p0 p1]` y 16 → 32 pasos.
- `tools/check_melo_styles.py` recompila cada fuente, compara el resultado con el compilado, comprueba conteos y rangos e imprime `ok`.
- Las escalas y los grados romanos están definidos en un único módulo que comparten ambos scripts.

### D4. Compás ternario por resolución de rejilla
Un estilo ternario declara `pasos_por_compás = 24` (semicorcheas de tresillo: 4 negras × 6). El plugin calcula la duración del paso como `compás / pasos_por_compás` y usa solo los 24 primeros pasos. El swing global se sigue aplicando encima, pero un ternario ya no lo necesita.
- Alternativa descartada: depender del swing a 67 como en gb_18. Es la trampa que se quiere evitar.

### D5. Generador pseudoaleatorio propio con semilla
Se usa un xorshift de 32 bits implementado en EEL2, con funciones `rng(seed, a, b, c)` que derivan un valor de una combinación de claves (semilla, voz, índice de frase, paso). No hay estado global que avance: cada decisión se calcula a partir de sus claves. Por eso un seek reproduce lo mismo sin tener que recorrer la reproducción.
- Alternativa descartada: `rand()` de EEL2, que no tiene semilla.

### D6. Frases calculadas desde el índice de frase
Un motivo dura 2 compases (el par de patrones de gb_18: p4 en el compás 1, p5 en el 2) y una frase 4 motivos (8 compases). El índice de frase es `floor(posición_en_compases / 8)`. El motivo de la frase k se obtiene aplicando la evolución a la frase k−1. Tras un seek se recalcula iterando desde la frase 0 hasta k, lo que cuesta poco: un motivo son como mucho 64 decisiones por voz. Las variaciones A' y B dentro de la frase se derivan del motivo con claves propias.
- Con lock, el motivo actual de la voz se copia a un buffer que se guarda en `@serialize` y que tiene prioridad sobre el cálculo.
- Los resultados de los dados (estilos, progresión, tónica, contador de motivo por voz) son estado guardado: los sliders o `@serialize`, no el azar en vivo.

### D7. Pipeline por paso

```
paso del transporte
  → acorde actual (director armónico: modo, tensión, markov con claves de ciclo)
  → por voz: ¿suena? (motivo de la frase ← ritmo mezclado por pad × densidad)
           → altura (sorteo ponderado por pad entre esquinas → símbolo)
           → nota(s) MIDI (bajo: grado sobre acorde · acordes: voicing + voice leading
                           · melodía: contorno sobre escala + gravedad + registro)
           → articulación → cola de eventos (swing, slide, strum)
  → emisión (canal o bus según destino)
```

El pad calcula los pesos bilineales de las 4 esquinas una vez por bloque, con la geometría de cuadrantes de gb_18 escrita como tabla, sin repetir código. Cada voz mezcla con `peso_pad`: la posición efectiva es la del pad multiplicada por `peso/100`.

### D8. Salida MIDI
- `ext_midi_bus = 1` en `@init`. Antes de cada `midisend`, `midi_bus` se fija al bus de destino (modo bus) o a 0 (modo canal).
- Cada entrada de la cola guarda nota, canal y bus. El "todo NoteOff" del transporte recorre una tabla de notas activas por destino (16 × 16 × 128 bits, unos 4 KB de memoria).
- Legato: el NoteOff de la nota anterior se programa justo después del NoteOn de la siguiente. Slide: CC 65 = 127 antes del NoteOn y CC 65 = 0 después del NoteOff.
- La cola crece a 256 entradas porque un acorde partido con strum genera hasta 5 eventos por paso.

### D9. Mapa de sliders
Es un plugin nuevo, así que el mapa se fija ahora y desde la v1 rige la regla de no renumerar.

| Sliders | Uso |
|---|---|
| 1–3 | Estilo de bajo, acordes y melodía (selector de archivo `/melo_styles`) |
| 4 | Uso interno: cuenta estilos (como el slider 8 de gb_18) |
| 5–6 | Pad X, Y |
| 7–15 | Global: voz maestra, tónica, modo de progresión, progresión fija, tensión, ritmo armónico, longitud de ciclo, modulación, swing |
| 16 | Semilla |
| 17–28 | Bajo: peso pad, densidad, octava, duración, velocidad, swing, slide, evolución, lock, destino, (2 de reserva) |
| 29–40 | Acordes: lo mismo que el bajo, más strum y partido |
| 41–52 | Melodía: lo mismo que el bajo, más salto máximo |
| 53 | Modo de salida (canal/bus) |

Los bloques por voz tienen el mismo tamaño para poder recorrerlos con `slider(base + 12·v + i)`.

### D10. Instalación
`tools/install.sh` crea además `Effects/GenderBenderMelo` y `Data/melo_styles` y copia ambos. La línea `ok -> …` no cambia.

## Risks / Trade-offs

- [Un estilo melódico cuesta mucho más de escribir que uno de batería] → solo 6 estilos en la v1, un `decode` para leer los existentes y el skill `adding-styles` como modelo para un futuro skill de estilos melódicos.
- [El sorteo de alturas por pad suena a azar en los puntos intermedios] → el motivo se fija por frase (D6), así que el sorteo solo cambia al cambiar de frase y no en cada compás.
- [Los buses MIDI solo funcionan en REAPER] → el modo canal es el predeterminado y funciona con ysfx.
- [Los cambios armónicos en vivo se aplican al cerrar el ciclo, con hasta 8 compases de espera] → el indicador de progresión muestra el cambio "pendiente".
- [El voice leading y la gravedad de la melodía pueden chocar con el contorno escrito] → los tiempos fuertes priorizan la nota del acorde y el resto del contorno manda. Se ajusta escuchando en REAPER.
- [Recalcular desde la frase 0 tras un seek muy lejano] → es una iteración barata. Si hiciera falta, se guarda en caché el último motivo calculado.

## Migration Plan

No hay migración: es un plugin nuevo. gb_18, sus estilos y sus presets no cambian. La reversión consiste en quitar `GenderBenderMelo/` y `melo_styles/` de la instalación.

## Open Questions

- El tiempo de portamento (CC 5) por defecto para el slide: se ajustará escuchando.
- La paleta de colores de la GUI dibujada.
