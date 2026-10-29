## Context

Las fuentes de los 73 estilos se escribieron con dos scripts de un solo uso: la BASE de cada estilo a mano, e INTRO, ENERGÍA, VARIACIÓN y FILL derivados con reglas comunes. El FILL no depende casi de la base (bombo en 1 y redoble de la voz de caja), por eso se repite.

## Goals / Non-Goals

**Goals:**
- Que no haya dos estilos con el mismo p6, p7 o p8.

**Non-Goals:**
- Escribir fills y variaciones nuevos para cada estilo (se puede hacer más adelante, estilo a estilo).
- Tocar los estilos anteriores a hoy, salvo borrar ESTAIL.

## Decisions

- **Comparación exacta** de cada patrón (las 7 voces y los 32 pasos, con sus valores) entre los 73 estilos generados.
- **Representante:** el primer estilo por orden alfabético de cada grupo conserva el patrón. Quedan con FILL: ACID HOUSE 124, BOSSA NOVA CHILL 100 y GABBER 180; con VARIACIÓN, FULL-ON 145 en lugar de GABBER 180 y GABBER ROLL 180.
- **Vaciar, no inventar:** el patrón se queda a 0 en la fuente (el bloque no se escribe). La página de huellas ya muestra "FILL vacío".
- **ESTAIL fuera, GQOM se queda:** GQOM tiene nombre de género y familia propia; ESTAIL estaba en "Other".

## Risks / Trade-offs

- [Silencio en el pad] Un patrón vacío no toca nada en su zona del pad. → Es lo que se ha pedido; se puede revertir regenerando las fuentes.

## Verificación

- Ningún p6, p7 ni p8 no vacío se repite entre los 73 estilos (script de un solo uso).
- `python3 tools/check_styles.py` imprime `ok`; la tabla del README y la carpeta coinciden.
- No hace falta REAPER: no cambia el plugin ni las bases.
