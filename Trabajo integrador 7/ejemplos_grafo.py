import os

from gestor_datos import GestorDatos
from arbol_general import ArbolCategorias
from grafo import armar_grafo

carpeta_datos = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos")
gestor = GestorDatos(carpeta_datos)

actividades = gestor.cargar_actividades()
arbol = ArbolCategorias(gestor.cargar_categorias())
arbol.cargar_actividades(actividades)
grafo = armar_grafo(actividades, arbol, gestor.cargar_puentes())

print("DATOS DE LA RED")
print("Vértices(Act):", grafo.cantidad_vertices())
print("Aristas(Rel):", grafo.cantidad_aristas)
print("Densidad:", round(grafo.densidad(), 2))

print("\nLISTA DE ADYACENCIA (actividades relacionadas con su distancia)")
for nombre in grafo.nombres():
    destinos = []
    for arista in grafo.vecinos_de(nombre):
        destinos.append(arista.destino + " (" + str(arista.peso) + ")")
    print(nombre + " -> " + ", ".join(destinos))

print("\nCONSULTA 1: ¿con qué está relacionada 'Caminata'?")
for arista in grafo.vecinos_de("Caminata"):
    print("   ", arista.destino, "- distancia", arista.peso)

print("\nCONSULTA 2: ¿cuántas relaciones tiene cada actividad?")
for nombre in grafo.nombres():
    print("   ", nombre, "->", grafo.grado_de(nombre))

print("\nCONSULTA 3: ¿están relacionadas estas dos?")
pares = [
    ("Caminata", "Estiramientos"),
    ("Caminata", "Llamar a un amigo"),
    ("Caminata", "Limpiar un sitio inusual"),
]
for una, otra in pares:
    if grafo.existe_arista(una, otra):
        print("   ", una, "y", otra, ": sí, distancia", grafo.peso_de(una, otra))
    else:
        print("   ", una, "y", otra, ": no")

print("\nCONSULTA 4: las muy parecidas a 'Leer 10 páginas' (distancia 2 o menos)")
for arista in grafo.relacionadas("Leer 10 páginas", 2):
    print("   ", arista.destino, "- distancia", arista.peso)

print("\nCONSULTA 5: ¿cuál es la actividad más conectada?")
mas = grafo.mas_conectada()
print("   ", mas, "con", grafo.grado_de(mas), "relaciones")

print("\nCONSULTA 6: una actividad que no existe")
print("    vecinos:", grafo.vecinos_de("Bailar"))
print("    grado:", grafo.grado_de("Bailar"))
