# melo-harmony Specification

## Purpose
Fija de dónde sale la armonía que siguen las tres voces (tónica, escala y progresión) y cómo el usuario la elige o la randomiza sin que las voces dejen de encajar entre sí.

## Requirements

### Requirement: Voz maestra de armonía
Un selector SHALL elegir qué voz (bajo, acordes o melodía) aporta la escala, el banco de progresiones, la tabla de Markov y las sustituciones. Las tres voces SHALL usar en todo momento la misma tónica, escala y acorde actual.

#### Scenario: Géneros cruzados
- **WHEN** el bajo es ROOTS REGGAE, los acordes son BULERIA y la voz maestra son los acordes
- **THEN** las tres voces siguen la frigia dominante y la progresión de BULERIA, y el bajo conserva el ritmo de ROOTS REGGAE

#### Scenario: Cambio de voz maestra
- **WHEN** el usuario cambia la voz maestra durante la reproducción
- **THEN** la armonía nueva entra al comienzo del siguiente ciclo de progresión

### Requirement: Tónica seleccionable
El usuario SHALL poder elegir la tónica (las 12 notas). Por defecto SHALL usarse la tónica que declara el estilo maestro. Al cambiar la tónica, el ritmo y los grados de las tres voces SHALL conservarse; los acordes y la melodía MAY elegir otra inversión u octava para seguir en su registro (no es una transposición literal).

#### Scenario: Transposición
- **WHEN** se cambia la tónica de A a C
- **THEN** las tres voces tocan en los mismos pasos, cada acorde pasa a su equivalente sobre C (Am → Cm, Dm → Fm) y todas las notas pertenecen al acorde o la escala de la nueva tónica
- **AND** el bajo sube 3 semitonos y los acordes y la melodía quedan dentro de su registro, aunque cambien de inversión u octava

### Requirement: Modos de progresión
Un selector SHALL elegir entre cinco modos: fija (una progresión del banco), ciclo del banco, aleatoria del banco, banco con sustituciones y Markov. En modo fija, el usuario SHALL poder elegir la progresión del banco.

#### Scenario: Modo fija
- **WHEN** el modo es fija y se elige la progresión 2 del banco
- **THEN** esa progresión se repite en todos los ciclos

#### Scenario: Modo ciclo
- **WHEN** el modo es ciclo del banco
- **THEN** al terminar cada progresión empieza la siguiente del banco, en orden

#### Scenario: Modo Markov
- **WHEN** el modo es Markov
- **THEN** cada acorde se elige a partir del anterior según la tabla del estilo maestro, y la progresión resuelve a la tónica al cerrar el ciclo

### Requirement: Tensión
En modo banco con sustituciones, un control de tensión (0–100) SHALL fijar la probabilidad de reemplazar cada acorde por una de las sustituciones que el estilo declara para él.

#### Scenario: Tensión cero
- **WHEN** la tensión vale 0
- **THEN** la progresión suena igual que en modo fija

#### Scenario: Tensión máxima
- **WHEN** la tensión vale 100 y el acorde tiene sustituciones declaradas
- **THEN** ese acorde siempre se reemplaza por una de ellas

### Requirement: Ritmo armónico y longitud
El usuario SHALL poder elegir la duración de cada acorde (½, 1 o 2 compases) y la longitud del ciclo de progresión (2, 4 u 8 compases). Por defecto SHALL usarse lo que declara el estilo.

#### Scenario: Dos acordes por compás
- **WHEN** el ritmo armónico vale ½ compás
- **THEN** el acorde cambia en el primer tiempo y en la mitad de cada compás

### Requirement: Cambios de armonía en el límite del ciclo
Cualquier cambio de progresión, tónica, estilo maestro o modo SHALL aplicarse al comienzo del siguiente ciclo de progresión, nunca a mitad de ciclo.

#### Scenario: Dado de progresión a mitad de ciclo
- **WHEN** se pulsa el dado de progresión en el compás 2 de un ciclo de 4
- **THEN** la progresión actual termina y la nueva empieza en el compás 1 del siguiente ciclo

### Requirement: Cambio de tónica automático
Un control opcional SHALL modular la tónica cada N ciclos (desactivado por defecto), subiendo o bajando una cuarta o una quinta, o yendo al relativo.

#### Scenario: Modulación cada 2 ciclos
- **WHEN** la modulación está activa cada 2 ciclos
- **THEN** la tónica cambia al empezar el ciclo 3, el 5 y así sucesivamente

### Requirement: Indicador de progresión
La interfaz SHALL mostrar la progresión del ciclo actual y marcar el acorde que está sonando.

#### Scenario: Reproducción
- **WHEN** el transporte avanza al segundo acorde de la progresión
- **THEN** el indicador marca el segundo acorde
