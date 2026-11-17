# Comparación: BST común vs AVL

## Qué se hizo
Se armó un árbol AVL (`arbol_avl.py`) y se lo comparó contra el BST del TP3
(`arbol_binario.py`) cargando los dos con los mismos datos. Los datos se
generaron para que el BST se desbalancee y también hay casos normales de
control:

1. Duraciones ordenadas de menor a mayor.
2. Duraciones ordenadas de mayor a menor.
3. Duraciones alternadas (1, n, 2, n-1, 3...).
4. Duraciones al azar sin repetir (caso de control).
5. Muchas repetidas, de 1 a 120 minutos (el caso real de Pause).

Tamaños: 100, 1000 y 10000 actividades. La operación medida es `mayor_hasta`
(la de "¿Qué hago ahora?"), con 200 consultas por tamaño. Se corre con
`python3 experimento_avl.py`.

## Cómo funciona el AVL
Es un BST que, después de cada inserción, revisa cada nodo del camino por el
que bajó. A cada nodo le calcula el **factor de balance**: altura del lado
izquierdo menos altura del lado derecho. Si el resultado es -1, 0 o 1, está
bien. Si es mayor a 1 o menor a -1, el nodo está desbalanceado y se arregla
con una **rotación**:

| Caso | Qué pasó | Arreglo |
|---|---|---|
| Izquierda-izquierda | Se cargó de más el lado izquierdo del hijo izquierdo | Rotación a la derecha |
| Derecha-derecha | Se cargó de más el lado derecho del hijo derecho | Rotación a la izquierda |
| Izquierda-derecha | Se cargó de más el lado derecho del hijo izquierdo | Rotación a la izquierda del hijo y después a la derecha |
| Derecha-izquierda | Se cargó de más el lado izquierdo del hijo derecho | Rotación a la derecha del hijo y después a la izquierda |

Ejemplo: se insertan 1, 2 y 3 en ese orden. El BST común queda como una
escalera (1 → 2 → 3). El AVL, al insertar el 3, ve que la raíz tiene factor
-2 y rota a la izquierda: queda el 2 arriba con el 1 y el 3 como hijos.

## Resultados

**Alturas, rotaciones y pasos por consulta**

| Caso | N | Altura BST | Altura AVL | Rotaciones AVL | Pasos BST | Pasos AVL |
|---|---|---|---|---|---|---|
| Menor a mayor | 100 | 100 | 7 | 93 | 51.1 | 6.7 |
| Menor a mayor | 1000 | 1000 | 10 | 990 | 467.5 | 10.0 |
| Menor a mayor | 10000 | 10000 | 14 | 9986 | 5107.9 | 13.4 |
| Mayor a menor | 100 | 100 | 7 | 93 | 50.8 | 6.8 |
| Mayor a menor | 1000 | 1000 | 10 | 990 | 534.5 | 10.0 |
| Mayor a menor | 10000 | 10000 | 14 | 9986 | 4894.1 | 13.4 |
| Alternados | 100 | 100 | 8 | 149 | 52.5 | 7.0 |
| Alternados | 1000 | 1000 | 12 | 1605 | 525.1 | 10.2 |
| Alternados | 10000 | 10000 | 17 | 16221 | 4683.1 | 13.7 |
| Al azar | 100 | 11 | 8 | 65 | 8.1 | 6.8 |
| Al azar | 1000 | 21 | 12 | 689 | 13.5 | 10.2 |
| Al azar | 10000 | 32 | 16 | 6946 | 17.4 | 13.6 |
| Muchas repetidas | 100 | 14 | 8 | 67 | 8.6 | 7.1 |
| Muchas repetidas | 1000 | 26 | 12 | 872 | 16.9 | 10.7 |
| Muchas repetidas | 10000 | 115 | 15 | 10655 | 92.7 | 14.1 |

**Tiempos con 10000 actividades (en milisegundos)**

| Caso | Consulta BST | Consulta AVL | Armar BST | Armar AVL |
|---|---|---|---|---|
| Menor a mayor | 0.5543 | 0.0020 | 3882.3 | 113.2 |
| Mayor a menor | 0.4192 | 0.0018 | 4263.0 | 78.1 |
| Alternados | 0.4516 | 0.0028 | 4247.2 | 146.4 |
| Al azar | 0.0015 | 0.0011 | 16.3 | 86.1 |
| Muchas repetidas | 0.0104 | 0.0014 | 41.1 | 77.6 |

Referencia: con 10000 elementos, log₂(n) es 13.3 y el límite teórico del AVL
(1.44 · log₂(n)) es 19.1. En todos los casos la altura del AVL quedó por
debajo de ese límite (14, 14, 17, 16 y 15).

## Por qué importa el balance
Buscar, insertar y `mayor_hasta` cuestan tantos pasos como la **altura** del
árbol, porque en cada paso se baja un nivel.

- **Árbol parejo:** la altura es parecida a log₂(n). Con 10000 elementos son
  unos 14 niveles, o sea unos 14 pasos.
- **Árbol degenerado:** si los datos llegan ordenados, cada nodo va a la
  derecha del anterior y el árbol queda como una lista enlazada. La altura
  es n y hay que hacer del orden de n pasos. En el experimento, el BST con
  10000 duraciones ordenadas necesitó en promedio 5107.9 pasos por consulta
  contra 13.4 del AVL (unas 380 veces más).

En notación:

| Operación | BST común | AVL |
|---|---|---|
| Buscar / `mayor_hasta` | Mejor Ω(1), promedio Θ(log n) con datos al azar, peor O(n) | O(log n) siempre |
| Insertar | Mejor Ω(1), promedio Θ(log n) con datos al azar, peor O(n) | O(log n) siempre |
| Armar con n inserciones | Peor caso O(n²) | O(n log n) |

El AVL garantiza que en cada nodo la diferencia de alturas sea 1 como máximo.
Con esa regla la altura nunca pasa de 1.44 · log₂(n+2), y por eso el peor
caso también es O(log n). Cada rotación cambia solo unos pocos enlaces, así
que cuesta O(1), y cada inserción necesita como máximo una rotación simple o
una doble.

La diferencia más clara está en armar el árbol: con 10000 duraciones
ordenadas el BST tardó entre 3882 y 4263 ms, y el AVL entre 78 y 146 ms (de
29 a 55 veces menos).

## El precio del AVL
- **Con datos al azar no gana mucho.** El BST ya queda casi parejo (altura
  32 contra 16 del AVL con 10000) y las consultas son parecidas (17.4 pasos
  contra 13.6). Armar el AVL tarda más (86.1 ms contra 16.3 ms) porque en cada
  inserción recalcula alturas y rota.
- Cada nodo guarda un número más (su altura) y el código es más largo.

## Caso de Pause: duraciones repetidas
Es el problema que apareció en el TP3. Como las duraciones son minutos de 1
a 120, las repetidas se encadenan hacia la derecha en el BST. Con 10000
actividades el BST llega a 115 niveles y hace 92.7 pasos por consulta. El
AVL se queda en 15 niveles y 14.1 pasos, y la consulta es unas 7 veces más
rápida (0.0104 ms contra 0.0014 ms).

## Límites
- Los tiempos por consulta son fracciones de milisegundo y tienen ruido. La
  **altura** y los **pasos** son los datos más confiables.
- El AVL implementado solo inserta y busca (no borra), que es lo que Pause
  necesita por ahora.
- Con duraciones repetidas, las rotaciones pueden mover una actividad hacia
  el lado izquierdo, pero el orden del árbol se mantiene (primero por
  duración y, si duran lo mismo, por orden de carga). Por eso `mayor_hasta`
  devuelve la misma actividad que el BST también ante empates (se comprobó
  con 1050 consultas). Lo único que puede cambiar es `buscar(duracion)`, que
  devuelve alguna de las actividades con esa duración y no necesariamente la
  primera cargada; la app no usa ese método.
- Desde esta versión la app usa el AVL: `repositorio.py` pasó de `ArbolBinario`
  a `ArbolAVL`, y al AVL se le agregaron `hasta`, `preorder` y `postorder` para
  que tenga las mismas operaciones que el BST. Las sugerencias y los listados
  son los mismos de antes. El BST (`arbol_binario.py`) se conserva para poder
  comparar, y `Exp_Arbol.py` del TP3 ahora mide el AVL: los números de
  `comparacion_estrategias.md` son los del BST.

## Conclusión técnica
El BST común solo es rápido si los datos llegan en un orden favorable. Si
llegan ordenados, alternados o con muchas repetidas, se desbalancea y pasa de
O(log n) a O(n): con 10000 datos ordenados hizo más de 5000 pasos por
consulta y tardó unos 4 segundos en armarse. El AVL mantiene la altura
siempre por debajo de 1.44 · log₂(n+2) con rotaciones, y a cambio tiene un
costo extra de construcción cuando los datos ya venían bien. Para Pause
conviene el AVL, porque no controlamos el orden en que llegan las
actividades (por ejemplo, un archivo JSON ya ordenado o el historial de
sesiones, que siempre se carga en orden cronológico), y garantizar O(log n)
vale más que ahorrar unos milisegundos al armar el árbol.
