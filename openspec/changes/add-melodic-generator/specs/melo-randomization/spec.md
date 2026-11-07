# Spec Delta

## Purpose

Define qué cambia y qué se respeta en cada botón de azar, para que randomizar sea predecible y nunca rompa la tonalidad común.

## ADDED Requirements

### Requirement: ALL RND
ALL RND SHALL asignar el mismo estilo aleatorio a las tres voces y elegir una progresión aleatoria de su banco. SHALL respetar la tónica fijada por el usuario, las densidades y los locks.

#### Scenario: Voces sin lock
- **WHEN** se pulsa ALL RND sin ninguna voz bloqueada
- **THEN** las tres voces pasan a un mismo estilo y la progresión cambia en el siguiente ciclo

#### Scenario: Voz bloqueada
- **WHEN** se pulsa ALL RND con el bajo bloqueado
- **THEN** el bajo conserva su estilo y su frase, y los acordes y la melodía cambian

### Requirement: EACH RND
EACH RND SHALL asignar un estilo aleatorio independiente a cada voz sin lock. La armonía SHALL seguir saliendo de la voz maestra.

#### Scenario: Cruces de género
- **WHEN** se pulsa EACH RND
- **THEN** cada voz sin lock puede quedar con un estilo distinto y las tres siguen la misma tónica y la misma progresión

### Requirement: Dado de progresión
El dado de progresión SHALL elegir otra progresión del banco del estilo maestro, distinta de la actual si el banco tiene más de una. Los motivos SHALL conservarse y re-armonizarse.

#### Scenario: Cambio de progresión
- **WHEN** se pulsa el dado de progresión
- **THEN** en el siguiente ciclo suena otra progresión y las voces mantienen sus motivos

### Requirement: Dado de motivo por voz
Cada voz SHALL tener un dado que genera un motivo nuevo para esa voz al empezar la siguiente frase, sin cambiar su estilo ni la progresión. Con la voz bloqueada SHALL no tener efecto.

#### Scenario: Motivo nuevo de la melodía
- **WHEN** se pulsa el dado de la melodía
- **THEN** la siguiente frase de la melodía usa un motivo nuevo y el bajo y los acordes no cambian

### Requirement: Dado de tónica
El dado de tónica SHALL elegir una tónica aleatoria, aplicada en el siguiente ciclo. SHALL conservar estilos, progresión y motivos.

#### Scenario: Tónica nueva
- **WHEN** se pulsa el dado de tónica
- **THEN** en el siguiente ciclo las tres voces suenan transpuestas a la nueva tónica, con la misma progresión y los mismos motivos

### Requirement: Azar reproducible
Todos los dados SHALL usar el generador con semilla del plugin. El resultado de cada pulsación SHALL guardarse en el estado del plugin (estilos, progresión, tónica, motivos), de modo que el proyecto suene igual al reabrirlo.

#### Scenario: Reapertura después de randomizar
- **WHEN** se pulsa EACH RND, se guarda el proyecto y se vuelve a abrir
- **THEN** cada voz conserva el estilo que le tocó
