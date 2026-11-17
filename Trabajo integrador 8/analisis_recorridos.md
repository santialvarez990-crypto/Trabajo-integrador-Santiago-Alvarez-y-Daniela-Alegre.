# Recorridos del grafo: BFS y DFS

## Qué hace cada uno
Los dos recorren la red de actividades empezando desde una actividad de
origen y visitan cada actividad alcanzable **una sola vez** (se anota cuáles
ya se visitaron, porque la red tiene ciclos y sin eso se daría vueltas
para siempre). Cambia el **orden** en que las visitan.

- **BFS (búsqueda en anchura):** visita primero todas las actividades que
  están a 1 paso del origen, después las que están a 2 pasos, después a 3, y
  así. Va por capas, de la más cercana a la más lejana. Usa una **cola**: la
  primera que entra es la primera que se atiende.
- **DFS (búsqueda en profundidad):** elige una actividad relacionada y sigue
  de una en una lo más lejos posible. Cuando llega a una de la que ya no se
  puede seguir, **vuelve atrás** y prueba por otro lado. Usa una **pila**: la
  última que entra es la primera que se atiende.

En los dos casos se anota de qué actividad se llegó a cada una
(`anterior`), y con eso se puede reconstruir el camino desde el origen
hasta cualquier actividad visitada.

## Cómo está implementado (`grafo.py`)
| Pieza | Qué hace |
|---|---|
| `Recorrido` | Guarda el resultado: `orden` (en qué orden se visitó), `distancia` (cuántos pasos hay desde el origen), `anterior` y `aristas_revisadas` |
| `Recorrido.camino_hasta` | Arma el camino desde el origen hasta una actividad, siguiendo los `anterior` hacia atrás |
| `bfs` | Recorrido con cola |
| `dfs` | Recorrido con pila |
| `mas_cercana_de_categoria` | Usa BFS para encontrar la actividad más cercana de una categoría (caso de uso 1) |
| `esta_conectado` | Usa DFS para saber si se llega a todas las actividades |

Detalles de la implementación:
- Los vecinos se recorren de **más cercanos a más lejanos** (por el peso de
  la arista), así el resultado siempre sale en el mismo orden.
- La cola de BFS es una lista con una posición que avanza, en vez de sacar
  siempre el primer elemento. Sacar el primero de una lista cuesta O(n) y
  haría que el BFS tardara más que O(V + E).
- El DFS usa una pila y no recursión, así que no tiene problemas con redes
  muy largas (se probó con una cadena de 20000 actividades).

## Caso de uso 1 (BFS): escalera hacia una categoría
**Pregunta:** desde lo que estoy haciendo ahora, ¿cuál es la actividad de una
categoría determinada que está más cerca, y cómo llego con la menor cantidad
de cambios?

**Por qué BFS:** como visita por capas, la primera actividad de esa categoría
que aparece es la que está a menos pasos. Es la misma idea del ejemplo de la
consigna ("la película relacionada más cercana"). Sirve para pasar de a poco
de algo fácil a algo más exigente, sin saltos grandes.

En la terminal: opción 8, inciso **d**.

```
Desde Meditar hacia Lectura -> 2 pasos:
    Meditar -> Escuchar música -> Leer 10 páginas
Desde Llamar a un amigo hacia Lectura -> 3 pasos:
    Llamar a un amigo -> Caminata -> Escuchar música -> Leer 10 páginas
Desde Limpiar un sitio inusual hacia Social -> 3 pasos:
    Limpiar un sitio inusual -> Escuchar música -> Caminata -> Llamar a un amigo
```

**Aclaración importante:** BFS cuenta **pasos**, no mira el peso (la
distancia) de las aristas. Garantiza el camino con menos actividades en el
medio, pero no que la suma de distancias sea la menor. Por ejemplo, el camino
de "Limpiar un sitio inusual" a "Llamar a un amigo" tiene 3 pasos y distancia total 8.
Buscar el camino de menor distancia total es otro problema (camino mínimo) y
no se resuelve con BFS.

## Caso de uso 2 (DFS): explorar en profundidad
**Pregunta:** a partir de una actividad, ¿qué cadenas de actividades
relacionadas se pueden armar, hasta dónde llega cada una y cuántas
actividades quedan al alcance?

**Por qué DFS:** la pregunta es sobre cadenas y ramas. DFS sigue una
cadena hasta el final antes de pasar a otra, y eso muestra las "rutinas
largas" posibles. BFS también visitaría todas, pero ordenadas por cercanía,
y eso esconde las cadenas.

En la terminal: opción 8, inciso **e** (se muestra con sangría según la
profundidad).

```
Llamar a un amigo (10 min)
  Escribirle a un familiar (10 min)
  Caminata (15 min)
    Estiramientos (5 min)
      Escuchar música (10 min)
        Meditar (3 min)
        Leer 10 páginas (15 min)
          Anotar 3 tareas del día (5 min)
            Armar la mochila para mañana (10 min)
              Escuchar un podcast (25 min)
                Ver un tutorial corto (15 min)
              Ordenar la pieza (20 min)
                Limpiar un sitio inusual (10 min)
Actividades alcanzadas: 13 - minutos si se hicieran todas: 153
```

Cuidado al leerlo: la sangría muestra la **profundidad en el recorrido**, no
la cercanía real. "Leer 10 páginas" aparece en el nivel 4, pero está a 3
pasos de "Llamar a un amigo" (lo muestra BFS).

**Otro uso de DFS:** `esta_conectado` recorre la red en profundidad desde la
primera actividad y compara cuántas visitó con el total. Con los puentes da
`True`, y sin ellos da `False` (los cuatro grupos quedan separados). Sirve
para detectar cuando un puente mal escrito deja actividades aisladas, y la
opción 8-c lo informa.

## Cuándo conviene cada uno
| Pregunta | Conviene |
|---|---|
| ¿Cuál es la actividad más cercana que cumple algo? | BFS |
| ¿Cuál es el camino con menos pasos entre dos actividades? | BFS |
| ¿Qué actividades hay a 1, 2 o 3 pasos? | BFS (porque ya van por capas) |
| ¿Qué cadenas largas se pueden armar desde una actividad? | DFS |
| Explorar toda una rama antes de pasar a otra | DFS |
| ¿Se puede llegar de una actividad a otra? ¿La red está conectada? | Cualquiera de los dos |

## Complejidad
*V* = cantidad de actividades (vértices), *E* = cantidad de relaciones
(aristas), con lista de adyacencia.

| | BFS | DFS |
|---|---|---|
| Tiempo (recorriendo todo) | O(V + E) | O(V + E) |
| Memoria extra | O(V): las visitadas y la cola | O(V + E) en esta implementación, porque la pila puede guardar una entrada por cada arista (con recursión sería O(V)) |
| Con matriz de adyacencia | O(V²) | O(V²) |

**Por qué O(V + E):** cada vértice se visita una vez (V) y cada lista de
adyacencia se lee una vez, y como la suma de los grados es 2E, se revisan
2E entradas. Con matriz habría que revisar una fila de V celdas por cada
vértice, y por eso sale O(V²) (es lo que se discutió en el TP7).

Dos precisiones:
- Si se corta apenas se encuentra lo buscado, el BFS puede terminar mucho
  antes. `mas_cercana_de_categoria` recorre todo y recién después busca, que
  es más simple y sigue siendo Θ(V + E).
- Cada vez que se pide los vecinos se los ordena por distancia, lo que suma
  O(g log g) por vértice (*g* es el grado). Con grados chicos, como en
  Pause (máximo 5), es despreciable.

### Mediciones
Redes al azar siempre conectadas, con unas 3 relaciones por actividad, y
recorridas desde la primera actividad (promedio de 3 repeticiones). Se corre
con `python3 experimento_recorridos.py`.

| V | E | V + E | BFS (ms) | DFS (ms) | Visitadas | Aristas revisadas |
|---|---|---|---|---|---|---|
| 1000 | 2994 | 3994 | 1.7 | 2.2 | 1000 | 5988 |
| 10000 | 29988 | 39988 | 36.2 | 36.6 | 10000 | 59976 |
| 100000 | 299987 | 399987 | 530.6 | 610.4 | 100000 | 599974 |

- Las **visitadas** son siempre exactamente V y las **aristas revisadas**
  son siempre exactamente 2E, como dice la teoría. Es el dato más confiable.
- El **tiempo** crece algo más que proporcional: por cada unidad de V + E
  pasa de 0.43 a 1.33 µs (BFS) cuando la red crece 100 veces. Es un
  crecimiento casi lineal; el aumento extra probablemente se deba a que con
  redes grandes los datos ya no entran en la memoria rápida del procesador,
  y no al algoritmo.
- BFS y DFS tardan parecido, porque hacen el mismo trabajo en distinto orden.

## Diferencias
| | BFS | DFS |
|---|---|---|
| Estructura | Cola (FIFO) | Pila (LIFO) |
| Orden | Por capas: primero lo más cercano en pasos | Por ramas: lo más profundo posible, y vuelve |
| Camino a una actividad | El de menos pasos | Uno cualquiera, que puede ser mucho más largo |
| Se queda con | Toda una capa a la vez (puede ser ancha) | Una rama a la vez (puede ser profunda) |
| Bueno para | Lo más cercano, niveles, caminos cortos | Explorar ramas, cadenas, conectividad |

Se midió la diferencia en el camino hacia la actividad de una categoría
(primera que encuentra cada uno):

| Red | Pasos BFS | Pasos DFS | Veces más largo |
|---|---|---|---|
| Pause: Meditar → Lectura | 2 | 7 | 3.5 |
| Pause: Llamar a un amigo → Lectura | 3 | 4 | 1.3 |
| Pause: Limpiar un sitio inusual → Social | 3 | 10 | 3.3 |
| Pause: Estiramientos → Hogar | 2 | 6 | 3.0 |
| Red al azar de 1000 actividades (promedio de 30 pedidos) | 2.3 | 40.0 | 17.1 |
| Red al azar de 10000 actividades (promedio de 30 pedidos) | 2.5 | 36.7 | 14.9 |

Por eso, para "lo más cercano", DFS no sirve: encuentra una, pero no
necesariamente la más cercana, y el camino puede ser mucho más largo.

## Límites
- BFS no tiene en cuenta los pesos: minimiza pasos, no distancia.
- El orden de los resultados depende de recorrer los vecinos del más
  cercano al más lejano; con otro criterio saldrían otros órdenes (aunque
  siempre las mismas actividades).
- Las redes al azar de las mediciones son sintéticas; la red real de Pause
  tiene solo 13 actividades, donde cualquier recorrido es instantáneo.
