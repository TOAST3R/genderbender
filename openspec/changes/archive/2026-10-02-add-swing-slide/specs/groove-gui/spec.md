## ADDED Requirements

### Requirement: Sliders automatizables
El plugin SHALL exponer 15 sliders nuevos y automatizables: 52 swing global (50–75, por defecto 50), 53–59 swing amount de kick, snare, clap, hh cerrado, hh abierto, tom alto y tom bajo (0–100, por defecto 100), y 60–66 slide de las mismas voces (−30 a 30 ms, por defecto 0).

#### Scenario: Automatización
- **WHEN** se automatiza el slider de swing global desde REAPER
- **THEN** el swing de las voces cambia durante la reproducción y el knob de la GUI refleja el valor

### Requirement: Compatibilidad de presets
Los valores nuevos SHALL persistir en presets y proyectos, y los presets o proyectos anteriores SHALL cargar con los valores por defecto de los parámetros nuevos.

#### Scenario: Preset antiguo
- **WHEN** se carga un `.preset` creado antes de este cambio
- **THEN** el swing global vale 50, los amounts valen 100, los slides valen 0 y los demás parámetros conservan sus valores

#### Scenario: Guardar y recargar
- **WHEN** se guarda un proyecto con swing 60 y slide del snare +10 ms y luego se vuelve a abrir
- **THEN** los valores se restauran

### Requirement: Tira GROOVE en la interfaz
La GUI SHALL ampliarse a 686×486 con una tira inferior GROOVE que contiene un knob SWING global y, para cada una de las 7 voces, un knob AMT y un knob SLIDE con su etiqueta y su valor. La parte superior de la interfaz SHALL quedar idéntica.

#### Scenario: Interfaz abierta
- **WHEN** se abre la GUI del plugin
- **THEN** se ven la interfaz original intacta arriba y la tira GROOVE abajo con 15 controles etiquetados

#### Scenario: Reset con modificador
- **WHEN** se hace la acción de reset del knob (mismo gesto que los knobs existentes) sobre un control GROOVE
- **THEN** el control vuelve a su valor por defecto
