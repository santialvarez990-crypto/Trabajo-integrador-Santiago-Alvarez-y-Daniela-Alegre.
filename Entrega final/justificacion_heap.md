# Cola de prioridad (heap): ranking de recomendaciones

## Dónde está integrado
En la opción **3) ¿Qué hago ahora?**. El usuario dice cuántos minutos tiene
y Pause le muestra un **TOP 5** de actividades ordenado por prioridad. El
usuario elige una (o ninguna) y la elección se guarda en `sesiones.json`.
Como el ranking usa ese historial, **cambia cada vez que el usuario acepta
algo**.

```
TOP 5 PARA 15 MINUTOS
1. Caminata                         5.0  (15 min)
2. Leer 10 páginas                  5.0  (15 min)
3. Ver un tutorial corto            5.0  (15 min)
4. Llamar a un amigo                3.3  (10 min)
5. Armar la mochila para mañana     3.3  (10 min)
¿Cuál elegís? (0 si ninguna):
```

Las estructuras trabajan juntas: el **AVL** (ordenado por duración) devuelve
rápido las actividades que entran en el tiempo libre, y el **heap** elige
cuáles son las 5 mejores entre ellas.

## Función de prioridad
Se calcula en `calcular_prioridad` (`recomendador.py`) con tres factores:

| Factor | Cómo se calcula | Puntos |
|---|---|---|
| Encaje | `duración / minutos libres × 5` | de 0 a 5 |
| Gusto | veces que el usuario aceptó esa actividad (máximo 3) | de 0 a 3 |
| Repetición | si fue la última que aceptó, el total se multiplica por 0.5 | ×0.5 |

`prioridad = (encaje + gusto)`, y se multiplica por 0.5 si fue la última
aceptada. El máximo posible es 8.0.

Ejemplos con 15 minutos libres:
- Caminata (15 min), sin historial: 15/15 × 5 = **5.0**.
- Llamar a un amigo (10 min), sin historial: 10/15 × 5 = **3.3**.
- Llamar a un amigo, aceptada 3 veces antes: 3.3 + 3 = **6.3**.
- Caminata si fue la última aceptada: (5.0 + 1) × 0.5 = **3.0**.

¿Por qué una combinación y no un solo factor? Si solo contara el encaje,
siempre se recomendaría lo mismo. Si solo contara el gusto, nunca se
descubrirían actividades nuevas. El factor de repetición evita que Pause
proponga dos veces seguidas lo mismo.

Si dos actividades tienen la misma prioridad, gana la que está primero en la
lista de candidatas (la de menor duración y, si duran lo mismo, la que se
cargó antes). Así el resultado siempre es el mismo.

## La heap
Es una **heap máxima**: cada padre tiene prioridad mayor o igual que sus
hijos, así que lo mejor siempre está arriba (posición 0). Se implementó a
mano (`heap.py`) sobre una lista, sin usar `heapq`. Para la posición `i`:

- hijo izquierdo: `2i + 1`
- hijo derecho: `2i + 2`
- padre: `(i - 1) // 2`

| Operación | Qué hace | Complejidad |
|---|---|---|
| `insertar` | Agrega al final y lo hace **subir** mientras sea mejor que su padre | O(log n) |
| `ver_maximo` | Mira la posición 0 | O(1) |
| `extraer_maximo` | Saca la raíz, pone el último en su lugar y lo hace **bajar** | O(log n) |
| `construir` | Arma la heap desde una lista haciendo bajar a la mitad de los elementos | O(n) |

## Cómo se obtiene el Top-N (`top_n`)
1. El AVL devuelve las actividades que entran en el tiempo libre: O(log n + k).
2. Se calcula la prioridad de cada una: O(k).
3. Se arma la heap con todas: O(k).
4. Se extrae el máximo N veces: O(N log k).

Total: **O(k + N log k)**, donde *k* es la cantidad de candidatas. Como N
es chico y fijo (5), en la práctica es O(k).

Ordenar todo y quedarse con las primeras N cuesta **O(k log k)**.

## Mediciones
Actividades inventadas con duraciones de 1 a 120 minutos, 120 minutos
libres (todas son candidatas), Top-5, promedio de 5 repeticiones. Se corre
con `python3 experimento_heap.py`. En las comparaciones de ordenar, el
valor es una estimación (n · log₂ n); en las del heap, son las medidas.

**1) Top-5 de un conjunto ya armado**

| N | Heap (ms) | Ordenar (ms) | Comparaciones heap | Comparaciones ordenar | Veces menos |
|---|---|---|---|---|---|
| 100 | 0.06 | 0.02 | 240 | 664 | 2.8 |
| 1000 | 0.38 | 0.24 | 1983 | 9966 | 5.0 |
| 10000 | 3.88 | 4.20 | 18892 | 132877 | 7.0 |
| 100000 | 48.42 | 56.39 | 188109 | 1660964 | 8.8 |

**2) Ranking dinámico:** se agrega una actividad nueva y se pide la mejor,
N veces seguidas. El heap queda armado y recibe cada actividad con
`insertar`. La otra forma vuelve a ordenar toda la lista cada vez.

| N | Heap (ms) | Ordenar de nuevo (ms) | Comparaciones heap | Comparaciones ordenar | Veces menos |
|---|---|---|---|---|---|
| 100 | 0.10 | 1.35 | 217 | 29946 | 138.0 |
| 1000 | 0.66 | 155.39 | 2277 | 4627202 | 2032.1 |
| 3000 | 3.22 | 1567.43 | 6723 | 48749624 | 7251.2 |

## Por qué un heap y no ordenar todo cada vez
1. **Se hace menos trabajo.** Para un Top-5 no hace falta tener todo
   ordenado: el heap solo asegura que lo mejor esté arriba y deja el resto
   desordenado. Hace entre 2.8 y 8.8 veces menos comparaciones, y la ventaja
   crece con N porque O(n) crece más lento que O(n log n).
2. **El ranking cambia todo el tiempo.** Cada vez que se agrega o cambia
   algo, el heap lo acomoda en O(log n) y la mejor sigue disponible en O(1).
   Volver a ordenar cuesta O(n log n) cada vez. Con 3000 elementos, el heap
   necesitó 7251 veces menos comparaciones y 3.22 ms contra 1567 ms.

## Lo que hay que decir con honestidad
- En el caso 1, en **tiempo real** el heap no gana siempre: con pocos
  elementos es más lento (0.06 ms contra 0.02 ms con 100) y con 100000 gana
  por poco (48 ms contra 56 ms). Pasa porque el `sorted` de Python está
  escrito en C y nuestro heap está escrito en Python. Donde sí se ve la
  ventaja es en las comparaciones, que es lo que mide la complejidad, y en el
  caso dinámico.
- Con las 13 actividades actuales de Pause la diferencia no se nota. La
  justificación es cómo se comporta cuando el catálogo crece o cuando el
  ranking se actualiza seguido.
- La prioridad depende de los minutos libres que dice el usuario, así que en
  la app se arma un heap nuevo en cada consulta y no uno permanente. El caso
  dinámico muestra qué pasaría con un ranking que se mantiene armado.
- El gusto se cuenta por nombre exacto de la actividad y se lee de
  `sesiones.json`.

## Conclusión
El heap conviene cuando solo se necesitan los mejores N y cuando el ranking
se actualiza: hace menos comparaciones que ordenar todo (O(k + N log k) contra
O(k log k)) y permite agregar elementos en O(log n). En Pause lo usamos para
elegir las 5 mejores recomendaciones entre las actividades que entran en el
tiempo libre, con una prioridad que combina cuánto aprovecha el tiempo, lo que
al usuario le gustó antes y que no se repita lo último que hizo.
