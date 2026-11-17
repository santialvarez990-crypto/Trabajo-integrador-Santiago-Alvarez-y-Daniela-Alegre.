import os

from gestor_datos import GestorDatos
from arbol_general import ArbolCategorias

carpeta_datos = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos")
gestor = GestorDatos(carpeta_datos)

arbol = ArbolCategorias(gestor.cargar_categorias())
arbol.cargar_actividades(gestor.cargar_actividades())

print("Categorías en total:", arbol.cantidad_categorias())
print("Altura del árbol:", arbol.altura())

print("\nPREORDER (primero la categoría, después sus subcategorías)")
for categoria, nivel in arbol.preorder():
    print("    " * nivel + categoria.get_nombre())

print("\nPOSTORDER (primero las subcategorías, al final la categoría)")
for categoria, nivel in arbol.postorder():
    cantidad = len(arbol.actividades_de(categoria))
    print("    " * nivel + categoria.get_nombre() + " -> total de actividades: " + str(cantidad))

print("\nPOR NIVELES (de arriba hacia abajo, nivel por nivel)")
nivel_anterior = -1
for categoria, nivel in arbol.por_niveles():
    if nivel != nivel_anterior:
        print("Nivel", nivel)
        nivel_anterior = nivel
    print("    " + categoria.get_nombre())

print("\nBUSCAR una categoría")
for nombre in ["Social", "Descanso", "Deportes"]:
    categoria = arbol.buscar(nombre)
    if categoria is None:
        print(nombre, "-> no existe (se revisaron", arbol.pasos, "categorías)")
    else:
        print(nombre, "-> encontrada, se revisaron", arbol.pasos, "categorías")
        print("    ruta:", " > ".join(arbol.ruta_hasta(nombre)))

print("\nACTIVIDADES de una rama completa: Mente")
mente = arbol.buscar("Mente")
for actividad in arbol.actividades_de(mente):
    print("    -", actividad)

print("\nAGREGAR una categoría nueva")
arbol.agregar_categoria("Descanso", "Respiración")
print("ruta:", " > ".join(arbol.ruta_hasta("Respiración")))
print("Categorías en total:", arbol.cantidad_categorias())
print("Altura del árbol:", arbol.altura())
