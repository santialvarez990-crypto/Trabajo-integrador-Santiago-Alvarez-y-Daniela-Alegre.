import random
import time

from modelos import Actividad
from repositorio import RepositorioActividades

TAMAÑOS = [100, 1000, 10000, 100000]
CANTIDAD_DE_CONSULTAS = 200
DURACION_MINIMA = 1
DURACION_MAXIMA = 120


def crear_actividades(cantidad, azar):
    categorias = ["Movimiento", "Social", "Hogar", "Lectura", "Organización", "Aprendizaje"]
    actividades = []
    for numero in range(cantidad):
        categoria = azar.choice(categorias)
        duracion = azar.randint(DURACION_MINIMA, DURACION_MAXIMA)
        actividades.append(Actividad("Actividad " + str(numero), categoria, duracion))
    return actividades


def promedio_en_ms(funcion, lista_de_minutos):
    total = 0
    for minutos in lista_de_minutos:
        inicio = time.perf_counter()
        funcion(minutos)
        total += time.perf_counter() - inicio
    return total / len(lista_de_minutos) * 1000


def main():
    azar = random.Random(42)
    filas = []

    for n in TAMAÑOS:
        actividades = crear_actividades(n, azar)
        consultas = []
        for _ in range(CANTIDAD_DE_CONSULTAS):
            consultas.append(azar.randint(DURACION_MINIMA, DURACION_MAXIMA))

        inicio = time.perf_counter()
        repo = RepositorioActividades(actividades)
        tiempo_armado = (time.perf_counter() - inicio) * 1000

        for minutos in consultas:
            assert repo.sugerir_para_tiempo(minutos) is repo.sugerir_para_tiempo_secuencial(minutos)

        tiempo_secuencial = promedio_en_ms(repo.sugerir_para_tiempo_secuencial, consultas)
        tiempo_arbol = promedio_en_ms(repo.sugerir_para_tiempo, consultas)

        suma_pasos = 0
        for minutos in consultas:
            repo.sugerir_para_tiempo(minutos)
            suma_pasos += repo.pasos_ultima_busqueda()
        pasos_arbol = suma_pasos / len(consultas)

        ahorro_por_consulta = tiempo_secuencial - tiempo_arbol
        if ahorro_por_consulta > 0:
            consultas_para_amortizar = tiempo_armado / ahorro_por_consulta
        else:
            consultas_para_amortizar = 0

        filas.append([n, tiempo_secuencial, tiempo_arbol, n, pasos_arbol,
                      repo.altura(), tiempo_armado, consultas_para_amortizar])

    print("N        | Secuencial ms | Arbol ms | Pasos sec. | Pasos arbol | Altura | Armar arbol ms | Consultas p/ amortizar")
    print("-" * 112)
    for fila in filas:
        print(f"{fila[0]:<8} | {fila[1]:<13.4f} | {fila[2]:<8.4f} | {fila[3]:<10} | "
              f"{fila[4]:<11.1f} | {fila[5]:<6} | {fila[6]:<14.1f} | {fila[7]:.1f}")

    print()
    print("Peor caso: duraciones cargadas ya ordenadas de menor a mayor")
    print("N        | Altura del arbol")
    for n in [100, 1000]:
        repo = RepositorioActividades()
        for numero in range(n):
            repo.agregar(Actividad("Actividad " + str(numero), "Prueba", numero + 1))
        print(f"{n:<8} | {repo.altura()}")


if __name__ == "__main__":
    main()
