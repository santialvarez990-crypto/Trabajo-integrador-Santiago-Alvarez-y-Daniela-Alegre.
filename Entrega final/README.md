# Pause

Trabajo integrador de **Estructura de Datos** (Tecnicatura en Programación).

Pause es una aplicación de terminal que ayuda a usar menos el celular. Cuando
la persona está por abrir una red social (TikTok, YouTube, etc.), Pause le
propone actividades alternativas que entran en el tiempo libre que tiene.

**Usuario objetivo:** Franco, 12 años, estudiante de primer año del secundario, que pasa varias horas
por día en redes sociales y a quien le cuesta sostener la atención en una sola
cosa.

## Requisitos
- Python 3.8 o superior.
- No hace falta instalar nada más.

## Cómo ejecutar
```bash
python3 main.py
```
Se puede ejecutar desde cualquier carpeta: los datos se leen de la carpeta
`datos/`, que tiene que estar junto a `main.py`.

## Menú
```
==================== PAUSE ====================
 1) Ver tiempo en pantalla
 2) Ver mis actividades
 3) ¿Qué hago ahora?
 4) Ver desafíos pendientes
 5) Activar/Desactivar modo minimalista
 6) Estadísticas de la semana
 7) Explorar categorías
 8) Actividades relacionadas
 0) Salir
=================================================
```

| Opción | Qué hace |
|---|---|
| 2 | Submenú: **a)** listar todas, **b)** buscar por nombre, **c)** filtrar por categoría (incluye sus subcategorías), **d)** filtrar por duración máxima, **e)** listar de la más corta a la más larga |
| 3 | Pregunta qué se estaba por hacer y cuántos minutos hay libres, y muestra un **TOP 5** de actividades. La persona elige una (o ninguna) y se guarda en `datos/sesiones.json` |
| 6 | Muestra cuántas sesiones se registraron en la ejecución actual |
| 7 | Submenú: **a)** navegar por la jerarquía de categorías, **b)** ver el árbol completo, **c)** verlo por niveles, **d)** buscar una categoría y ver su ruta |
| 8 | Submenú: **a)** ver las actividades relacionadas con una, **b)** ver toda la red, **c)** ver datos de la red (cantidad, densidad, si está conectada), **d)** camino con menos pasos hacia una categoría (BFS), **e)** explorar en profundidad desde una actividad (DFS) |
| 1, 4, 5 | Reservadas para futuras actualizaciones (ver más abajo). Hoy muestran "no disponible en esta versión por falta de tiempo" |

### Ejemplo: opción 3
```
¿Qué estás por hacer?: abrir TikTok
¿Cuántos minutos tenés?: 15

TOP 5 PARA 15 MINUTOS
1. Caminata                         5.0  (15 min)
2. Leer 10 páginas                  5.0  (15 min)
3. Ver un tutorial corto            5.0  (15 min)
4. Llamar a un amigo                3.3  (10 min)
5. Armar la mochila para mañana     3.3  (10 min)
¿Cuál elegís? (0 si ninguna): 1
Racha actual de Franco: 1.
```
El ranking cambia según lo que la persona fue aceptando: lo que aceptó antes
suma puntos, y lo último que aceptó vale la mitad para que no se repita.

### Ejemplo: opción 7-b
```
Actividades (13)
    Cuerpo (4)
        Movimiento (2)
        Descanso (2)
    Mente (5)
        Lectura (1)
        Aprendizaje (2)
        Organización (2)
    Vida diaria (2)
        Hogar (2)
    Vínculos (2)
        Social (2)
```
Entre paréntesis está la cantidad de actividades de cada rama.

## Datos (`datos/`)
| Archivo | Contenido |
|---|---|
| `actividades.json` | Las actividades: nombre, categoría y duración estimada en minutos |
| `usuarios.json` | El usuario |
| `categorias.json` | La jerarquía de categorías (árbol general) |
| `puentes.json` | Relaciones entre actividades de grupos distintos (para el grafo) |
| `sesiones.json` | Se crea solo al usar la opción 3. Guarda el historial |

Los nombres de `puentes.json` tienen que coincidir **exactamente** con los de
`actividades.json`. Si alguno no coincide, esa relación no se carga y la app
avisa al arrancar.

## Estructuras de datos usadas
| Estructura | Archivo | Para qué se usa | Complejidad |
|---|---|---|---|
| Árbol AVL | `arbol_avl.py` | Índice de las actividades por duración: sugerir, filtrar y listar ordenado | Buscar e insertar O(log n). Filtrar por duración O(log n + k). Listar ordenado Θ(n) |
| Árbol binario de búsqueda | `arbol_binario.py` | Es el árbol del TP3. Se conserva para comparar contra el AVL | O(log n) en promedio, O(n) si se desbalancea |
| Árbol general (n-ario) | `arbol_general.py` | Jerarquía de categorías: explorar, buscar y recorrer | Buscar una categoría O(C), con C = cantidad de categorías |
| Heap máxima | `heap.py` | Cola de prioridad para el Top-N de recomendaciones | Insertar y extraer O(log n). Construir O(n). Top-N: O(k + N log k) |
| Grafo (lista de adyacencia) | `grafo.py` | Red de actividades relacionadas (no dirigido y pesado) | Vecinos O(g log g). Existe arista O(g) |
| BFS y DFS | `grafo.py` | Camino con menos pasos y exploración en profundidad | O(V + E) los dos |
| Búsqueda secuencial | `repositorio.py` | Buscar por nombre | O(n) |

*n* = cantidad de actividades, *k* = actividades que entran en el tiempo libre,
*N* = tamaño del Top, *g* = relaciones de una actividad, *V* y *E* = vértices y
aristas del grafo.

### Cómo se conectan
- El **AVL** devuelve rápido las actividades que entran en el tiempo libre.
- El **heap** elige las 5 mejores entre esas, según la función de prioridad.
- El **grafo** se arma desde las categorías del árbol general: misma categoría
  (distancia 1), mismo grupo (distancia 2) y los puentes de `puentes.json`
  (distancia 3).

## Estructura del proyecto
```
.
├── main.py                    # Interfaz de terminal
├── modelos.py                 # Usuario, Actividad, Desafio, SesionUso, Categoria
├── repositorio.py             # Actividades + índice AVL por duración
├── gestor_datos.py            # Lectura y escritura de los JSON
├── arbol_avl.py               # Árbol AVL
├── arbol_binario.py           # Árbol binario de búsqueda
├── arbol_general.py           # Árbol de categorías
├── heap.py                    # Heap máxima
├── recomendador.py            # Función de prioridad y Top-N
├── grafo.py                   # Grafo, BFS y DFS
├── busqueda_secuencial.py     # TP2: búsqueda secuencial de sesiones por fecha
├── arbol.py                   # TP2: árbol de sesiones por fecha
├── sesion.py                  # TP2: datos de una sesión
├── generador_datos.py         # TP2: datos de prueba
├── experimento.py             # TP2: secuencial contra árbol
├── resultados.csv             # TP2: resultados medidos
├── Exp_Arbol.py               # TP3: árbol contra búsqueda secuencial
├── experimento_avl.py         # TP4: BST contra AVL
├── experimento_heap.py        # TP6: heap contra ordenar todo
├── ejemplos_recorridos.py     # TP5: recorridos del árbol general
├── ejemplos_grafo.py          # TP7: consultas sobre el grafo
├── ejemplos_bfs_dfs.py        # TP8: casos de uso de BFS y DFS
├── experimento_recorridos.py  # TP8: costo de BFS y DFS
├── datos/
│   ├── actividades.json
│   ├── usuarios.json
│   ├── categorias.json
│   └── puentes.json
├── tests/
│   ├── test_arbol.py
│   └── test_repositorio.py
├── analisis_complejidad.md    # TP2
├── comparacion_estrategias.md # TP3
├── comparacion_avl.md         # TP4
├── justificacion_heap.md      # TP6
├── modelo_grafo.md            # TP7
└── analisis_recorridos.md     # TP8
```

## Pruebas
```bash
python3 -m unittest discover -s tests
```
Son 36 pruebas: el árbol binario (inserción, búsqueda, recorridos, rangos,
duraciones repetidas y datos ordenados) y el repositorio, que ahora usa el
AVL (listar, filtrar, sugerir, y que el resultado coincida con la búsqueda
secuencial).

## Experimentos y ejemplos
Todos se ejecutan con `python3 nombre.py`. Los de medición pueden tardar
unos segundos.

| Archivo | Qué muestra | Documento |
|---|---|---|
| `experimento.py` | Secuencial contra árbol para buscar sesiones por fecha | `analisis_complejidad.md` |
| `Exp_Arbol.py` | Secuencial contra árbol para sugerir según el tiempo libre | `comparacion_estrategias.md` |
| `experimento_avl.py` | BST contra AVL con datos que desbalancean | `comparacion_avl.md` |
| `ejemplos_recorridos.py` | Preorder, postorder y por niveles del árbol de categorías | |
| `experimento_heap.py` | Heap contra ordenar todo, para un Top-5 | `justificacion_heap.md` |
| `ejemplos_grafo.py` | Consultas sobre el grafo (vecinos, grado, densidad) | `modelo_grafo.md` |
| `ejemplos_bfs_dfs.py` | Los dos casos de uso de BFS y DFS | `analisis_recorridos.md` |
| `experimento_recorridos.py` | Costo de BFS y DFS al crecer la red | `analisis_recorridos.md` |

## Versiones
| Versión | Trabajo | Qué se agregó |
|---|---|---|
| v1 | TP1 | Clases del dominio, carga de datos, terminal, buscar, listar y filtrar |
| v2 | TP3 | Árbol binario de búsqueda integrado (sugerir y filtrar por duración) |
| — | TP4 | AVL, que pasa a ser el índice de la app |
| v3 | TP5 | Árbol general de categorías y opción 7 |
| v4 | TP6 | Heap y Top-5 en la opción 3 |
| v5 | TP7 | Grafo de actividades relacionadas y opción 8 |
| v6 | TP8 | BFS y DFS en la opción 8 |

## Limitaciones conocidas
- Las opciones 1, 4 y 5 del menú no están disponibles en esta versión por
  falta de tiempo, y la opción 6 solo cuenta las sesiones de la ejecución actual.
- Hay que escribir los nombres de categorías y actividades tal cual, con
  tildes (por ejemplo `Organización`).
- La prioridad del Top-5 depende de los minutos libres, por eso se arma un
  heap nuevo en cada consulta.
- BFS cuenta pasos y no mira el peso (la distancia) de las relaciones.
- Los pesos 1, 2 y 3 del grafo son una decisión de diseño, no una medición.
- Las pruebas automáticas cubren los árboles y el repositorio. No hay todavía
  pruebas para el heap, el grafo y el árbol general (se comprobaron con
  los scripts de ejemplos).

## Futuras actualizaciones
Quedaron fuera de esta entrega porque la cátedra canceló los puntos 9 y 10
por falta de tiempo. Se dejan planteados para una próxima versión:

- **Camino mínimo en el grafo** (por ejemplo con Dijkstra), usando los pesos
  que ya están definidos en las relaciones.
- **Funcionalidades del plan inicial:** registro de tiempo en pantalla,
  recordatorios de pausas, informes (diario, semanal, mensual y anual),
  desafíos pendientes ordenados con el heap, modo minimalista y estadísticas
  semanales reales.
- **Pruebas** para el heap, el grafo, BFS/DFS y el árbol general.
- **Documentación ampliada** del proyecto.
