## ADDED Requirements

### Requirement: Kits sintetizados del preview
La página SHALL ofrecer nueve kits sintetizados para el preview (Actual, 808, 909, Acústico, Lo-fi, Hardcore, 80s / Linn, Percusión y Chiptune), cada uno con sus 7 voces, sin cargar recursos externos. Un selector de kit en la cabecera y otro en la vista ampliada, sincronizados, SHALL permitir elegir un kit o "Auto". El kit SHALL poder cambiarse en cualquier momento, también mientras suena, y el golpe siguiente SHALL usar el kit nuevo. El kit SHALL afectar solo al sonido de la página, no al MIDI exportado.

#### Scenario: Cambiar de kit mientras suena
- **WHEN** suena un estilo y se cambia el kit de 909 a 808
- **THEN** la reproducción sigue sin pararse y los golpes siguientes suenan con el 808

#### Scenario: El MIDI no cambia
- **WHEN** se exporta el MIDI de un estilo con dos kits distintos
- **THEN** los dos archivos son idénticos

### Requirement: Kit automático por familia
Con "Auto" (la opción por defecto), el kit SHALL ser el asignado a la familia del estilo que suena, según una tabla familia → kit, y SHALL cambiar cuando cambia la familia del estilo que suena, también en A/B. El selector SHALL mostrar qué kit está usando Auto.

#### Scenario: Familias distintas
- **WHEN** con Auto se pulsa Play en DETROIT TECHNO 128 y después en SALSA 180
- **THEN** primero suena el kit 909 y después el de Percusión, y el selector muestra "Auto (909)" y luego "Auto (Percusión)"

#### Scenario: A/B entre familias
- **WHEN** con Auto se toca A/B entre TRAP 140 y SAMBA 100
- **THEN** los compases de TRAP 140 suenan con el 808 y los de SAMBA 100 con Percusión

### Requirement: Kit recordado y en el permalink
El kit elegido SHALL guardarse en el navegador y en el parámetro `kit` del permalink; al cargar la página, el permalink SHALL tener prioridad sobre lo guardado.

#### Scenario: Permalink con kit
- **WHEN** se carga `fingerprints.html#kit=808`
- **THEN** el selector está en 808 aunque en el navegador estuviera guardado otro kit
