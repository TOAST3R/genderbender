## ADDED Requirements

### Requirement: Filtro por familia con recuentos
La cabecera de la página SHALL tener un selector de familia con la opción "Todos" seguida de una opción por familia, en el orden de la tabla "Included styles" y con el número de estilos de cada una entre paréntesis. Junto al selector, la página SHALL mostrar el recuento de estilos visibles y el total. Los recuentos SHALL calcularse a partir de los estilos de la página.

#### Scenario: Valor inicial
- **WHEN** se abre la página
- **THEN** el selector está en "Todos (N)", con N el número total de estilos, se ven todas las familias y el recuento dice `N estilos`

#### Scenario: Elegir una familia
- **WHEN** se elige la opción `Cumbia (6)`
- **THEN** solo se ven el encabezado y las 6 tiras de Cumbia, y el recuento dice `6 de N estilos`

#### Scenario: Volver a todos
- **WHEN** se elige "Todos" después de una familia
- **THEN** vuelven a verse todas las familias y el recuento dice `N estilos`
