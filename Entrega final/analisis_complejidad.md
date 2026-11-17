# Análisis de complejidad — Búsqueda de sesiones por fecha

## Operación crítica elegida
Buscar todas las sesiones registradas en una fecha determinada dentro del
historial de sesiones de un usuario. Es una operación de uso frecuente:
cualquier informe (diario/semanal/mensual) de Pause depende de poder
recuperar rápido las sesiones de un rango de fechas.

## Estrategia 1 — Búsqueda secuencial
Recorre la lista completa de sesiones comparando la fecha de cada una
contra la fecha buscada.

- **Peor caso (O):** O(n) — la fecha no está, o está al final; hay que
  recorrer todos los elementos.
- **Mejor caso (Ω):** Ω(1) — la primera sesión de la lista coincide.
- **Caso promedio (Θ):** Θ(n) — en promedio hay que recorrer una
  fracción constante de la lista, que sigue creciendo linealmente con n.

## Estrategia 2 — Árbol binario de búsqueda (BST) por fecha
Cada nodo almacena la fecha y todas las sesiones de esa fecha. La
búsqueda desciende por el árbol comparando fechas, descartando en cada
paso una de las dos mitades restantes (si el árbol está razonablemente
balanceado).

- **Peor caso (O):** O(n) — si el árbol degenera en una lista
  encadenada (ver más abajo, es un caso real y no solo teórico).
- **Mejor caso (Ω):** Ω(1) — la fecha buscada está en la raíz.
- **Caso promedio (Θ):** Θ(log n) — **solo si el árbol se mantiene
  razonablemente balanceado.**

## Resultados medidos

### Caso promedio (fechas insertadas en orden aleatorio)
Simula cómo se vería el historial si se cargan sesiones de prueba sin
ningún orden particular (dataset típico de laboratorio).

| N elementos | Secuencial (ms) | Árbol (ms) | Altura del árbol |
|---|---|---|---|
| 100 | 0.0025 | 0.0007 | 15 |
| 1.000 | 0.0173 | 0.0008 | 22 |
| 10.000 | 0.1714 | 0.0012 | 23 |
| 100.000 | 1.8438 | 0.0030 | 23 |

La altura del árbol crece de forma logarítmica (15 → 22 → 23 → 23 al
multiplicar n por 1000), tal como predice la teoría: log₂(100.000) ≈ 17.
El tiempo de búsqueda secuencial crece de forma aproximadamente lineal
con n (multiplicar n por 10 multiplica el tiempo por ~10), mientras
que el árbol apenas se mueve.

### Caso patológico (fechas insertadas en orden cronológico estricto)
Simula el escenario **real** de Pause: las sesiones se registran a
medida que pasan los días, es decir, se insertan siempre en orden
creciente de fecha.

| N elementos | Altura del árbol | Pasos para encontrar el último elemento | Tiempo (ms) |
|---|---|---|---|
| 100 | 100 | 100 | 0.0057 |
| 1.000 | 1.000 | 1.000 | 0.0437 |
| 10.000 | 10.000 | 10.000 | 0.4523 |

Acá el árbol se convierte literalmente en una lista encadenada
(altura = n). De hecho, al intentar calcular la altura con una función
recursiva simple, Python **arrojó `RecursionError`** al llegar a 1.000
elementos insertados en orden — una demostración muy concreta de que
el peor caso no es solo un tecnicismo de la notación O(), sino algo
que puede romper el programa en la práctica.

## Comparación y conclusión técnica

- Cuando los datos llegan en un orden que no favorece a ningún lado del
  árbol (caso promedio), el BST es claramente superior: crece en
  Θ(log n) contra Θ(n) de la búsqueda secuencial, y la diferencia se
  vuelve dramática a partir de unos pocos miles de elementos (con
  100.000 sesiones, el árbol es ~600 veces más rápido).
- Sin embargo, un BST simple **no es una solución mágica**: si los
  datos se insertan en un orden ya ordenado (que es exactamente lo que
  pasa con un historial cronológico como el de Pause), el árbol
  degenera y pierde toda su ventaja, quedando tan malo como la
  búsqueda secuencial (o peor, por el overhead de manejar nodos).
- **Conclusión:** para esta operación conviene el árbol, pero no en su
  versión más simple. Para integrarlo de forma robusta en el proyecto
  final habría que usar una variante auto-balanceada (AVL o
  rojo-negro), que garantiza Θ(log n) también en el peor caso,
  independientemente del orden de inserción. Lo dejamos anotado como
  mejora para cuando integremos el árbol definitivo en la entrega
  final.
