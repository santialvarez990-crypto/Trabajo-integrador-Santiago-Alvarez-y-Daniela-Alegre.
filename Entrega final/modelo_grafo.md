# Grafo de actividades de Pause

## Idea general
Las actividades que Pause recomienda no son independientes: algunas se
parecen, otras se complementan. Para poder responder preguntas como "¿qué
otra cosa puedo hacer que sea parecida a esto?", las relaciones se
representan como una red (un grafo). La red se arma desde los datos que ya
existen: las actividades (TP1), su categoría y la jerarquía de categorías
(TP5).

## Vértices
**Un vértice = una actividad** (por ejemplo "Caminata"). Se identifica
por su nombre. En esta versión hay 13 vértices, los mismos que cargan
`actividades.json` y el AVL de actividades.

## Aristas
**Una arista = dos actividades relacionadas**, es decir, que se pueden hacer
una en lugar de la otra o una a continuación de la otra. Se definen con tres
reglas, y cada una tiene su peso:

| Regla | Ejemplo | Peso (distancia) |
|---|---|---|
| Misma categoría | Caminata – Estiramientos (las dos son Movimiento) | 1 |
| Mismo grupo, distinta categoría | Caminata – Meditar (Movimiento y Descanso, ambas de Cuerpo) | 2 |
| Grupos distintos, pero se complementan (puente) | Caminata – Llamar a un amigo (se puede hablar caminando) | 3 |

Las dos primeras reglas se aplican solas, mirando la jerarquía de
categorías del TP5 (el "grupo" es la categoría del segundo nivel: Cuerpo,
Mente, Vida diaria o Vínculos). Los puentes están escritos a mano en
`datos/puentes.json`, porque no se pueden deducir de las categorías. Sirven
además para que **todas las actividades queden conectadas** con las demás:
sin ellos, los cuatro grupos serían islas separadas.

Resultado: 13 vértices y 24 aristas (6 de peso 1, 12 de peso 2 y 6 de peso 3).

## Tipo de grafo: no dirigido y pesado
- **No dirigido.** Que "Caminata" esté relacionada con "Estiramientos"
  es lo mismo que decir que "Estiramientos" está relacionada con "Caminata
  corta". La relación es simétrica, así que no hace falta una dirección. En
  el código, cada arista se guarda en las dos listas con el mismo peso.
- **Pesado.** No todas las relaciones valen lo mismo: dos actividades de la
  misma categoría son más parecidas que dos que solo se complementan. El peso
  es una **distancia**: cuanto más chico, más relacionadas. Permite ordenar lo
  relacionado de más a menos cercano y deja lista la red para buscar caminos
  de menor costo más adelante.

## Representación: lista de adyacencia
Cada actividad guarda la lista de sus aristas. En el código es un
diccionario `nombre -> lista de Arista`, y cada `Arista` tiene `origen`,
`destino` y `peso`:

```
Caminata -> Estiramientos (1), Escuchar música (2), Meditar (2),
                  Escuchar un podcast (3), Llamar a un amigo (3)
Estiramientos  -> Caminata (1), Escuchar música (2), Meditar (2)
...
```

### Por qué lista y no matriz
La matriz de adyacencia es una tabla de n × n donde cada celda dice si hay
arista entre dos vértices. Se elige entre las dos según la **densidad**
(qué fracción de todas las relaciones posibles existe).

- **Densidad actual: 0.31** (24 aristas de las 78 posibles). Si el catálogo
  crece con la misma regla, se mantiene en torno a **0.30** (medido con
  catálogos de 98 y 294 actividades repartidas en las mismas 7 categorías:
  0.299 y 0.304). Es una densidad moderada, no muy baja, porque las
  actividades de una misma categoría quedan todas conectadas entre sí.
- Con esa densidad, la lista guarda unas 0.30 entradas por cada celda de la
  matriz (por ejemplo 2842 entradas contra 9604 celdas con 98 actividades).
  Ahorra lugar, aunque no tanto como en un grafo muy ralo, y en Python cada
  entrada es un objeto más pesado que una celda de la matriz.
- **Lo que decide es el tiempo de las operaciones que Pause más va a usar:**
  pedir las actividades relacionadas con una (`vecinos_de`) y, más adelante,
  recorrer la red. Con lista, esto cuesta lo que vale el grado de la
  actividad; con matriz, hay que revisar toda una fila de n celdas aunque la
  actividad tenga solo 3 relaciones.

| Operación | Lista de adyacencia | Matriz de adyacencia |
|---|---|---|
| ¿Existe la arista A–B? | O(grado de A) | O(1) |
| Vecinos de una actividad | O(grado) | O(V) |
| Recorrer toda la red | O(V + E) | O(V²) |
| Memoria | O(V + E) | O(V²) |

La matriz le gana en una sola cosa, saber si dos actividades están
relacionadas, y es una consulta que se hace poco. Convendría pasar a una
matriz si la densidad subiera por encima de 0.5 o si esa consulta pasara a
ser la principal.

## Operaciones implementadas (`grafo.py`)
| Operación | Qué hace | Complejidad |
|---|---|---|
| `agregar_vertice` | Agrega una actividad a la red | O(1) |
| `agregar_arista` | Conecta dos actividades (en las dos direcciones) | O(grado) |
| `existe_arista`, `peso_de` | ¿Están conectadas? ¿con qué distancia? | O(grado) |
| `vecinos_de` | Las relacionadas con una, de más cercana a más lejana | O(g log g) |
| `relacionadas` | Solo las de distancia menor o igual a un máximo | O(g log g) |
| `grado_de` | Cantidad de relaciones de una actividad | O(1) |
| `mas_conectada` | La actividad con más relaciones | O(V) |
| `densidad` | Fracción de relaciones posibles que existen | O(1) |
| `listar_aristas` | Todas las relaciones, sin repetir | O(V + E) |
| `armar_grafo` | Arma la red desde actividades, categorías y puentes | revisa los n·(n−1)/2 pares |

*g* es el grado de la actividad consultada.

## Ejemplos de consultas
Salida de `ejemplos_grafo.py` (con los datos de prueba):

```
CONSULTA 1: ¿con qué está relacionada 'Caminata'?
    Estiramientos - distancia 1
    Escuchar música - distancia 2
    Meditar - distancia 2
    Escuchar un podcast - distancia 3
    Llamar a un amigo - distancia 3

CONSULTA 3: ¿están relacionadas estas dos?
    Caminata y Estiramientos : sí, distancia 1
    Caminata y Llamar a un amigo : sí, distancia 3
    Caminata y Limpiar un sitio inusual : no

CONSULTA 4: las muy parecidas a 'Leer 10 páginas' (distancia 2 o menos)
    Anotar 3 tareas del día - distancia 2
    Armar la mochila para mañana - distancia 2
    Escuchar un podcast - distancia 2
    Ver un tutorial corto - distancia 2

CONSULTA 5: ¿cuál es la actividad más conectada?
    Caminata con 5 relaciones
```

(Hay varias actividades empatadas con 5 relaciones; se informa la primera
que se cargó.)

## Funcionalidad integrada
En la terminal, la opción **8) Actividades relacionadas** permite:
- **a)** elegir una actividad y ver con cuáles está relacionada, con su
  duración y su distancia;
- **b)** ver toda la red (la lista de adyacencia completa);
- **c)** ver datos de la red: cantidad de actividades y relaciones, densidad
  y la actividad más conectada.

## Límites
- Los pesos 1, 2 y 3 son una decisión de diseño, no una medición: reflejan
  qué tan parecidas se consideran las actividades.
- Los puentes se cargan a mano. Si un puente nombra una actividad que no
  existe, se ignora y la app avisa.
- Esta versión solo consulta relaciones directas. Los recorridos de la red y
  la búsqueda de caminos quedan para el trabajo siguiente.
