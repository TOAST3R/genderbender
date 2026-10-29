## ADDED Requirements

### Requirement: Cursor de paso y golpes por voz
Mientras suena un estilo en la vista ampliada, la página SHALL resaltar la columna del paso que suena en el patrón que suena, sincronizada con el audio (con el swing aplicado), y SHALL iluminar un instante el nombre de cada voz cuando golpea. Al parar, el cursor SHALL desaparecer.

#### Scenario: El cursor recorre el compás
- **WHEN** suena DETROIT TECHNO 128 en la vista ampliada
- **THEN** una columna resaltada recorre los 32 pasos del patrón que suena y vuelve al paso 0 en cada compás

#### Scenario: Golpe del bombo
- **WHEN** suena un paso con bombo
- **THEN** el nombre "kick" se ilumina un instante

### Requirement: Visualizador del sonido
Mientras suena el preview, la página SHALL mostrar un visualizador del sonido de salida (después del kit y de los efectos) con dos modos, Onda y Espectro, que se alternan con un clic; el modo SHALL recordarse en el navegador. El visualizador SHALL estar en la vista ampliada y, si suena desde la lista, en una barra fija al pie que desaparece al parar. Con `prefers-reduced-motion: reduce` el visualizador no SHALL animarse ni iluminar las voces; el cursor de paso sí se mantiene. El visualizador SHALL animarse solo mientras suena.

#### Scenario: Cambiar de modo
- **WHEN** suena un estilo y se hace clic en el visualizador en modo Onda
- **THEN** pasa a modo Espectro y, al recargar la página, sigue en Espectro

#### Scenario: Barra del pie
- **WHEN** se pulsa Play en un estilo de la lista y después Stop
- **THEN** la barra del visualizador aparece al pie mientras suena y desaparece al parar
