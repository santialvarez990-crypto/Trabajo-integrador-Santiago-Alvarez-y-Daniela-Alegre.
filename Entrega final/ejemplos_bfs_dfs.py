import os

from gestor_datos import GestorDatos
from arbol_general import ArbolCategorias
from grafo import armar_grafo

carpeta_datos = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos")
gestor = GestorDatos(carpeta_datos)

actividades = gestor.cargar_actividades()
arbol = ArbolCategorias(gestor.cargar_categorias())
arbol.cargar_actividades(actividades)
puentes = gestor.cargar_puentes()
grafo = armar_grafo(actividades, arbol, puentes)


def camino_con_dfs(origen, categoria):
    recorrido = grafo.dfs(origen)
    for nombre in recorrido.orden:
        if nombre != origen and grafo.get_actividad(nombre).get_categoria() == categoria:
            return recorrido.camino_hasta(nombre)
    return []


print("BFS desde Caminata:")
recorrido = grafo.bfs("Caminata")
paso_anterior = -1
for nombre in recorrido.orden:
    paso = recorrido.distancia[nombre]
    if paso != paso_anterior:
        print("A", paso, "pasos:")
        paso_anterior = paso
    print("    " + nombre)

print("\nDFS desde Caminata:")
recorrido = grafo.dfs("Caminata")
for nombre in recorrido.orden:
    print("  " * recorrido.distancia[nombre] + nombre)

print("\nBFS: escalera hacia una categoría")
print("¿cuál es la actividad de otra categoría más cercana?")
pares = [
    ("Meditar", "Lectura"),
    ("Llamar a un amigo", "Lectura"),
    ("Limpiar un sitio inusual", "Social"),
    ("Estiramientos", "Hogar"),
]
for origen, categoria in pares:
    camino = grafo.mas_cercana_de_categoria(origen, categoria)
    print("  Desde", origen, "hacia", categoria, "->", len(camino) - 1, "pasos:")
    print("      " + " -> ".join(camino))

print("\nComparacion:")
print("  Desde", "hacia", "pasos BFS", "pasos DFS", sep=" | ")
for origen, categoria in pares:
    con_bfs = grafo.mas_cercana_de_categoria(origen, categoria)
    con_dfs = camino_con_dfs(origen, categoria)
    print("  ", origen, "|", categoria, "|", len(con_bfs) - 1, "|", len(con_dfs) - 1)

print("\nDFS: explorar en profundidad todo lo relacionado con 'Llamar a un amigo'")
recorrido = grafo.dfs("Llamar a un amigo")
minutos = 0
for nombre in recorrido.orden:
    duracion = grafo.get_actividad(nombre).get_duracion_estimada()
    minutos += duracion
    print("  " * recorrido.distancia[nombre] + nombre + " (" + str(duracion) + " min)")
print("Actividades alcanzadas:", len(recorrido.orden), "- minutos si se hicieran todas:", minutos)

