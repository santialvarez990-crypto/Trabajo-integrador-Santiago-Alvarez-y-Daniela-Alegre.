import math
import random
import time

from modelos import Actividad
from heap import Elemento, HeapMaximo
from recomendador import Recomendador, clave_para_ordenar

TAMANOS_TOP = [100, 1000, 10000, 100000]
TAMANOS_DINAMICO = [100, 1000, 3000]
CANTIDAD_EN_TOP = 5
REPETICIONES = 5
MINUTOS_LIBRES = 120


def crear_elementos(cantidad, recomendador):
    azar = random.Random(42)
    actividades = []
    for numero in range(cantidad):
        actividades.append(Actividad("Actividad " + str(numero), "Prueba", azar.randint(1, 120)))

    aceptadas = []
    for _ in range(30):
        aceptadas.append("Actividad " + str(azar.randint(0, cantidad - 1)))

    elementos = []
    for orden in range(cantidad):
        prioridad = recomendador.calcular_prioridad(actividades[orden], MINUTOS_LIBRES, aceptadas)
        elementos.append(Elemento(prioridad, orden, actividades[orden]))
    return elementos


def promedio_en_ms(funcion, *datos):
    total = 0
    for _ in range(REPETICIONES):
        inicio = time.perf_counter()
        funcion(*datos)
        total += time.perf_counter() - inicio
    return total / REPETICIONES * 1000


def parte_top_n():
    recomendador = Recomendador(None)
    filas = []
    for n in TAMANOS_TOP:
        elementos = crear_elementos(n, recomendador)

        con_heap = recomendador.elegir_con_heap(elementos, CANTIDAD_EN_TOP)
        comparaciones_heap = recomendador.comparaciones
        ordenando = recomendador.elegir_ordenando(elementos, CANTIDAD_EN_TOP)
        for i in range(CANTIDAD_EN_TOP):
            assert con_heap[i].orden == ordenando[i].orden

        tiempo_heap = promedio_en_ms(recomendador.elegir_con_heap, elementos, CANTIDAD_EN_TOP)
        tiempo_ordenar = promedio_en_ms(recomendador.elegir_ordenando, elementos, CANTIDAD_EN_TOP)
        comparaciones_ordenar = n * math.log2(n)

        filas.append([n, tiempo_heap, tiempo_ordenar, comparaciones_heap, comparaciones_ordenar])

    print("TOP-5 DE UN CONJUNTO QUE YA ESTÁ ARMADO")
    print(f"{'N':>8}{'Heap ms':>11}{'Ordenar ms':>13}{'Comp. heap':>13}{'Comp. ordenar (aprox)':>24}{'Veces menos':>13}")
    print("-" * 82)
    for fila in filas:
        veces = fila[4] / fila[3]
        print(f"{fila[0]:>8}{fila[1]:>11.2f}{fila[2]:>13.2f}{fila[3]:>13}{fila[4]:>24.0f}{veces:>13.1f}")


def parte_dinamica():
    recomendador = Recomendador(None)
    filas = []
    for n in TAMANOS_DINAMICO:
        elementos = crear_elementos(n, recomendador)

        inicio = time.perf_counter()
        heap = HeapMaximo()
        mejores_heap = []
        for elemento in elementos:
            heap.insertar(elemento)
            mejores_heap.append(heap.ver_maximo().orden)
        tiempo_heap = (time.perf_counter() - inicio) * 1000

        inicio = time.perf_counter()
        lista = []
        mejores_ordenando = []
        comparaciones_ordenar = 0
        for elemento in elementos:
            lista.append(elemento)
            ordenada = sorted(lista, key=clave_para_ordenar)
            mejores_ordenando.append(ordenada[0].orden)
            if len(lista) > 1:
                comparaciones_ordenar += len(lista) * math.log2(len(lista))
        tiempo_ordenar = (time.perf_counter() - inicio) * 1000

        assert mejores_heap == mejores_ordenando

        filas.append([n, tiempo_heap, tiempo_ordenar, heap.comparaciones, comparaciones_ordenar])

    print()
    print("RANKING DINÁMICO: SE AGREGA UNA ACTIVIDAD Y SE PIDE LA MEJOR, N VECES")
    print(f"{'N':>8}{'Heap ms':>11}{'Ordenar ms':>13}{'Comp. heap':>13}{'Comp. ordenar (aprox)':>24}{'Veces menos':>13}")
    print("-" * 82)
    for fila in filas:
        veces = fila[4] / fila[3]
        print(f"{fila[0]:>8}{fila[1]:>11.2f}{fila[2]:>13.2f}{fila[3]:>13}{fila[4]:>24.0f}{veces:>13.1f}")


parte_top_n()
parte_dinamica()
