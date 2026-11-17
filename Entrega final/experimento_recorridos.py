import random
import time

from modelos import Actividad
from grafo import Grafo

TAMAÑOS = [1000, 10000, 100000]
REPETICIONES = 3
ARISTAS_EXTRA_POR_VERTICE = 2
CANTIDAD_DE_CATEGORIAS = 50
CANTIDAD_DE_ORIGENES = 30


def crear_grafo(cantidad):
    azar = random.Random(42)
    grafo = Grafo()
    for i in range(cantidad):
        categoria = "Categoria " + str(azar.randint(1, CANTIDAD_DE_CATEGORIAS))
        grafo.agregar_vertice(Actividad("v" + str(i), categoria, 10))
    for i in range(1, cantidad):
        anterior = azar.randint(0, i - 1)
        grafo.agregar_arista("v" + str(i), "v" + str(anterior), azar.randint(1, 3))
    for _ in range(ARISTAS_EXTRA_POR_VERTICE * cantidad):
        una = azar.randint(0, cantidad - 1)
        otra = azar.randint(0, cantidad - 1)
        grafo.agregar_arista("v" + str(una), "v" + str(otra), azar.randint(1, 3))
    return grafo


def promedio_en_ms(funcion, origen):
    total = 0
    for _ in range(REPETICIONES):
        inicio = time.perf_counter()
        funcion(origen)
        total += time.perf_counter() - inicio
    return total / REPETICIONES * 1000


def camino_con_dfs(grafo, origen, categoria):
    recorrido = grafo.dfs(origen)
    for nombre in recorrido.orden:
        if nombre != origen and grafo.get_actividad(nombre).get_categoria() == categoria:
            return recorrido.camino_hasta(nombre)
    return []


def parte_complejidad():
    print("COSTO DE RECORRER TODA LA RED")
    print(f"{'V':>8}{'E':>9}{'V+E':>9}{'BFS ms':>10}{'DFS ms':>10}{'Visitados':>11}{'Aristas rev.':>14}{'BFS µs/(V+E)':>14}{'DFS µs/(V+E)':>14}")
    print("-" * 99)
    for n in TAMAÑOS:
        grafo = crear_grafo(n)
        aristas = grafo.cantidad_aristas
        bfs = grafo.bfs("v0")
        dfs = grafo.dfs("v0")
        assert len(bfs.orden) == n and len(dfs.orden) == n
        assert bfs.aristas_revisadas == 2 * aristas and dfs.aristas_revisadas == 2 * aristas

        tiempo_bfs = promedio_en_ms(grafo.bfs, "v0")
        tiempo_dfs = promedio_en_ms(grafo.dfs, "v0")
        por_bfs = tiempo_bfs * 1000 / (n + aristas)
        por_dfs = tiempo_dfs * 1000 / (n + aristas)
        print(f"{n:>8}{aristas:>9}{n + aristas:>9}{tiempo_bfs:>10.1f}{tiempo_dfs:>10.1f}{len(bfs.orden):>11}{bfs.aristas_revisadas:>14}{por_bfs:>14.2f}{por_dfs:>14.2f}")


def parte_cercana():
    print()
    print("BFS vs DFS")
    print(f"{'V':>8}{'Pasos BFS':>12}{'Pasos DFS':>12}{'Veces más':>12}")
    print("-" * 44)
    for n in [1000, 10000]:
        grafo = crear_grafo(n)
        azar = random.Random(7)
        suma_bfs = 0
        suma_dfs = 0
        for _ in range(CANTIDAD_DE_ORIGENES):
            origen = "v" + str(azar.randint(0, n - 1))
            categoria = "Categoria " + str(azar.randint(1, CANTIDAD_DE_CATEGORIAS))
            con_bfs = grafo.mas_cercana_de_categoria(origen, categoria)
            con_dfs = camino_con_dfs(grafo, origen, categoria)
            assert len(con_bfs) > 0 and len(con_dfs) > 0
            assert len(con_bfs) <= len(con_dfs)
            suma_bfs += len(con_bfs) - 1
            suma_dfs += len(con_dfs) - 1
        promedio_bfs = suma_bfs / CANTIDAD_DE_ORIGENES
        promedio_dfs = suma_dfs / CANTIDAD_DE_ORIGENES
        print(f"{n:>8}{promedio_bfs:>12.1f}{promedio_dfs:>12.1f}{promedio_dfs / promedio_bfs:>12.1f}")


parte_complejidad()
parte_cercana()
