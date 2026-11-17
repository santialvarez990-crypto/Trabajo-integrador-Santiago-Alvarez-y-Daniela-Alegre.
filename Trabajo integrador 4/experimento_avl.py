import math
import random
import time

from modelos import Actividad
from arbol_binario import ArbolBinario
from arbol_avl import ArbolAVL

tamaños = [100, 1000, 10000]
cantidad_de_consultas = 200


def duraciones_ascendentes(n):
    return list(range(1, n + 1))


def duraciones_descendentes(n):
    return list(range(n, 0, -1))


def duraciones_alternadas(n):
    resultado = []
    menor = 1
    mayor = n
    while menor <= mayor:
        resultado.append(menor)
        menor += 1
        if menor <= mayor:
            resultado.append(mayor)
            mayor -= 1
    return resultado


def duraciones_random(n):
    azar = random.Random(42)
    resultado = list(range(1, n + 1))
    azar.shuffle(resultado)
    return resultado


def duraciones_repetidas(n):
    azar = random.Random(42)
    resultado = []
    for _ in range(n):
        resultado.append(azar.randint(1, 120))
    return resultado


casos = [
    ["Ordenados de menor a mayor", duraciones_ascendentes],
    ["Ordenados de mayor a menor", duraciones_descendentes],
    ["Alternados", duraciones_alternadas],
    ["Random", duraciones_random],
    ["Muchas repetidas", duraciones_repetidas],
]


def crear_actividades(duraciones):
    actividades = []
    for numero in range(len(duraciones)):
        actividades.append(Actividad("Actividad " + str(numero), "Prueba", duraciones[numero]))
    return actividades


def armar_arbol(arbol, actividades):
    inicio = time.perf_counter()
    for actividad in actividades:
        arbol.insertar(actividad)
    return (time.perf_counter() - inicio) * 1000


def tiempo_de_consultas(arbol, lista_de_minutos):
    inicio = time.perf_counter()
    for minutos in lista_de_minutos:
        arbol.mayor_hasta(minutos)
    return (time.perf_counter() - inicio) / len(lista_de_minutos) * 1000


def pasos_de_consultas(arbol, lista_de_minutos):
    total = 0
    for minutos in lista_de_minutos:
        arbol.mayor_hasta(minutos)
        total += arbol.pasos
    return total / len(lista_de_minutos)


def main():
    filas = []

    for nombre_caso, crear_duraciones in casos:
        for n in tamaños:
            duraciones = crear_duraciones(n)
            actividades = crear_actividades(duraciones)

            azar = random.Random(7)
            consultas = []
            for _ in range(cantidad_de_consultas):
                consultas.append(azar.randint(1, max(duraciones)))

            bst = ArbolBinario()
            avl = ArbolAVL()
            armar_bst = armar_arbol(bst, actividades)
            armar_avl = armar_arbol(avl, actividades)

            for minutos in consultas:
                respuesta_bst = bst.mayor_hasta(minutos)
                respuesta_avl = avl.mayor_hasta(minutos)
                if respuesta_bst is None:
                    assert respuesta_avl is None
                else:
                    assert respuesta_avl.get_duracion_estimada() == respuesta_bst.get_duracion_estimada()

            assert avl.altura_total() <= 1.45 * math.log2(n + 2)

            filas.append([
                nombre_caso, n,
                bst.altura, avl.altura_total(), avl.rotaciones,
                pasos_de_consultas(bst, consultas), pasos_de_consultas(avl, consultas),
                tiempo_de_consultas(bst, consultas), tiempo_de_consultas(avl, consultas),
                armar_bst, armar_avl,
            ])

    print("alturas, rotaciones y pasos por consulta")
    print(f"{'Caso':<38}{'N':>6}{'Alt.BST':>9}{'Alt.AVL':>9}{'Rotac.':>8}{'Pasos BST':>11}{'Pasos AVL':>11}")
    print("-" * 92)
    for f in filas:
        print(f"{f[0]:<38}{f[1]:>6}{f[2]:>9}{f[3]:>9}{f[4]:>8}{f[5]:>11.1f}{f[6]:>11.1f}")

    print()
    print("ms")
    print(f"{'Caso':<38}{'N':>6}{'Consulta BST':>14}{'Consulta AVL':>14}{'Armar BST':>11}{'Armar AVL':>11}")
    print("-" * 94)
    for f in filas:
        print(f"{f[0]:<38}{f[1]:>6}{f[7]:>14.4f}{f[8]:>14.4f}{f[9]:>11.1f}{f[10]:>11.1f}")

    print()
    print("Referencia: log2(n)")
    for n in tamaños:
        print(f"n = {n}: log2(n) = {math.log2(n):.1f}   1.44 * log2(n) = {1.44 * math.log2(n):.1f}")


main()
