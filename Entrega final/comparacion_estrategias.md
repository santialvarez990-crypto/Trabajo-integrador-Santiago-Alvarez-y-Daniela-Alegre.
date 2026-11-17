# Comparación: árbol vs búsqueda secuencial

## Para qué sirve el árbol en Pause
El árbol guarda las actividades **ordenadas por duración** y está dentro de
`RepositorioActividades` (`repositorio.py`). Se usa en tres lugares del menú:

| Opción del menú | Qué hace el árbol |
|---|---|
| 3) ¿Qué hago ahora? | `mayor_hasta(minutos)`: encuentra la actividad más larga que entra en el tiempo libre |
| 2-d) Filtrar por duración máxima | `hasta(minutos)`: junta todas las que entran, ya ordenadas |
| 2-e) Listar de la más corta a la más larga | recorrido `inorder` |

**Clave de ordenamiento: la duración.** La idea central de Pause es "tengo X
minutos, ¿qué hago en vez de abrir una red social?". Con las actividades
ordenadas por duración, esa pregunta se contesta sin mirar todas.

## Regla del árbol
- Si una actividad dura **menos** que el nodo, va a la **izquierda**.
- Si dura **igual o más**, va a la **derecha**.

## Las dos formas de resolver "¿Qué hago con X minutos?"
1. **Secuencial (TP1):** mira todas las actividades de la lista y se queda con
   la más larga que no pase de X minutos.
2. **Árbol:** empieza en la raíz. Si la actividad del nodo entra en X minutos,
   la anota como candidata y sigue por la derecha (puede haber una más larga).
   Si no entra, sigue por la izquierda. Así descarta muchas actividades de
   un solo paso.

Las dos dan siempre la misma actividad (hay una prueba que lo comprueba). Si
hay varias igual de largas, las dos devuelven la última que se cargó.

## Complejidad
*n* = cantidad de actividades. *h* = altura del árbol (cantidad de niveles).

| Operación | Mejor caso (Ω) | Caso promedio | Peor caso (O) |
|---|---|---|---|
| Secuencial: sugerir | Ω(n) | Θ(n) | O(n) |
| Árbol: sugerir (`mayor_hasta`) | Ω(1) | depende de h (ver abajo) | O(n) |
| Árbol: insertar / buscar | Ω(1) | depende de h | O(n) |
| Árbol: filtrar (`hasta`) | — | O(h + k) | O(n) |
| Árbol: recorridos (inorder, preorder, postorder) | Θ(n) | Θ(n) | Θ(n) |
| Árbol: armarlo con n inserciones | — | Θ(n · h) | O(n²) |

*k* = cantidad de actividades que devuelve `hasta`.

La búsqueda secuencial siempre es Ω(n): para estar seguro de que no hay una
actividad más larga que entre, tiene que mirarlas todas.

En el árbol, todo depende de la altura *h*:
- Si el árbol está "parejo", *h* es chico (parecido a log₂ n).
- Si las actividades llegan **ya ordenadas** por duración, cada una va a la
  derecha de la anterior y el árbol queda como una lista: *h* = *n* y pierde
  toda su ventaja.
- Si hay **muchas duraciones repetidas** (como en Pause, donde las duraciones
  son minutos entre 1 y 120), las repetidas se van encadenando hacia la
  derecha y *h* crece más o menos como *n* dividido la cantidad de
  duraciones distintas.

## Resultados medidos
Actividades inventadas con duraciones al azar entre 1 y 120 minutos, 200
consultas por tamaño, siempre los mismos datos (semilla fija). Se puede
repetir con `python3 Exp_Arbol.py`.

| N actividades | Secuencial (ms) | Árbol (ms) | Pasos secuencial | Pasos árbol | Altura del árbol | Armar el árbol (ms) | Consultas para recuperar ese tiempo |
|---|---|---|---|---|---|---|---|
| 100 | 0.0047 | 0.0006 | 100 | 8.4 | 12 | 0.1 | 15.6 |
| 1000 | 0.0459 | 0.0013 | 1000 | 17.9 | 25 | 0.9 | 20.2 |
| 10000 | 0.4745 | 0.0098 | 10000 | 90.7 | 117 | 32.9 | 70.7 |
| 100000 | 5.2944 | 0.2181 | 100000 | 847.4 | 935 | 6723.0 | 1324.4 |

**Peor caso (duraciones cargadas ya ordenadas de menor a mayor):**

| N actividades | Altura del árbol |
|---|---|
| 100 | 100 |
| 1000 | 1000 |

### Qué se ve en la tabla
- **La búsqueda secuencial crece en línea recta:** los pasos son siempre *n*.
- **El árbol hace muchos menos pasos**, pero ya no son casi fijos: pasan de
  8 a 847 cuando *n* pasa de 100 a 100.000. Es por las duraciones repetidas
  (a 100.000 actividades les tocan unas 830 por cada duración posible).
- **En tiempo, el árbol gana entre 8 y 48 veces** según el tamaño. Con
  100.000 actividades la ventaja baja a unas 24 veces aunque en pasos sea
  unas 118 veces menor: cada paso del árbol cuesta más que un paso de la
  lista (hay que ir saltando de nodo en nodo).
- **Armar el árbol tiene un costo:** se paga una vez, al cargar las
  actividades. Con 1.000 actividades se recupera en unas 20 consultas. Con
  100.000 tarda 6,7 segundos y hacen falta unas 1.300 consultas para
  recuperarlo.
- Los tiempos son muy chicos, así que tienen algo de ruido. Los **pasos**
  son el dato más confiable.

## Relación con el TP2
En el TP2 se comparó la búsqueda secuencial contra un árbol para otra
operación: buscar las sesiones de una fecha (`busqueda_secuencial.py` y
`arbol.py`). Acá se repite la misma comparación con la operación que
realmente usa la app (sugerir una actividad según el tiempo libre) y con un
árbol que ahora forma parte de Pause.

| N | TP2: secuencial (ms) | TP2: árbol (ms) | TP3: secuencial (ms) | TP3: árbol (ms) |
|---|---|---|---|---|
| 100 | 0.0025 | 0.0007 | 0.0047 | 0.0006 |
| 1000 | 0.0173 | 0.0008 | 0.0459 | 0.0013 |
| 10000 | 0.1714 | 0.0012 | 0.4745 | 0.0098 |
| 100000 | 1.8438 | 0.0030 | 5.2944 | 0.2181 |

La conclusión es la misma: el árbol es mucho más rápido que recorrer toda la
lista. Hay una diferencia: en el TP2 el árbol casi no crece con N (altura 23
con 100000 elementos), mientras que acá el tiempo del árbol sube (altura 935
con 100000). Es porque en el TP2 cada nodo guardaba una lista con todas las
sesiones de la misma fecha, y en este TP, para simplificar, cada actividad con
la misma duración va a un nodo propio, así que con muchas repetidas el árbol se
alarga. Eso se corrige en el TP4 con el AVL.

## Conclusión
Conviene el árbol para el uso real de Pause: un catálogo de decenas,
cientos o pocos miles de actividades. Ahí la consulta es entre 8 y 48 veces
más rápida y armarlo se recupera con pocas decenas de consultas. Además,
da gratis cosas que la lista no da: filtrar por duración y listar ordenado
sin tener que ordenar cada vez.

Con catálogos muy chicos (como las 8 actividades de prueba) la diferencia
no se nota y daría lo mismo usar cualquiera de las dos.

## Límites de esta versión
1. **Datos ya ordenados:** el árbol se convierte en una lista (altura = *n*).
   Pasa si el archivo JSON tuviera las actividades ordenadas por duración.
2. **Duraciones repetidas:** hacen crecer la altura (se ve en la tabla).
3. **Recursión de Python:** los recorridos y `hasta` usan recursión, y Python
   permite alrededor de 1.000 llamadas anidadas. Un árbol de más de ~900
   niveles podría dar `RecursionError`. Con un catálogo normal no pasa.
4. **Buscar por nombre** sigue siendo secuencial: es una búsqueda de texto
   ("contiene") y un árbol ordenado por duración no puede ayudar.

## Cómo se podría mejorar (para más adelante)
- Que cada nodo guarde una **lista** con todas las actividades de la misma
  duración. Así no hay repetidas encadenadas y la altura nunca pasa de 120.
- Usar un árbol que se **balancea solo** (AVL), que mantiene la altura chica
  sin importar el orden en que lleguen los datos.
