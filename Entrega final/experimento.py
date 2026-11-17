import time
import statistics
from datetime import date, timedelta

from generador_datos import generar_sesiones, DIA_BASE, RANGO_DIAS
from busqueda_secuencial import buscar_secuencial
from arbol import ArbolBusquedaFechas

TAMANOS = [100, 1_000, 10_000, 100_000]
REPETICIONES_POR_TAMANO = 200


def construir_estructuras(sesiones):
    arbol = ArbolBusquedaFechas()
    for s in sesiones:
        arbol.insertar(s)
    return sesiones, arbol


def medir(funcion, *args, repeticiones):
    tiempos = []
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        funcion(*args)
        fin = time.perf_counter()
        tiempos.append(fin - inicio)
    return statistics.mean(tiempos)


def main():
    print(f"{'N elementos':<15}{'Secuencial (ms)':<20}{'Árbol (ms)':<15}{'Altura del árbol':<18}")
    filas = []

    for n in TAMANOS:
        sesiones = generar_sesiones(n, semilla=42)
        lista, arbol = construir_estructuras(sesiones)

        rng_fechas = [DIA_BASE + timedelta(days=i) for i in range(RANGO_DIAS)]

        def buscar_seq():
            for _ in range(1):
                pass
            fecha = rng_fechas[hash(time.perf_counter_ns()) % RANGO_DIAS]
            buscar_secuencial(lista, fecha)

        def buscar_arbol():
            fecha = rng_fechas[hash(time.perf_counter_ns()) % RANGO_DIAS]
            arbol.buscar(fecha)

        t_secuencial = medir(buscar_seq, repeticiones=REPETICIONES_POR_TAMANO) * 1000
        t_arbol = medir(buscar_arbol, repeticiones=REPETICIONES_POR_TAMANO) * 1000
        altura = arbol.altura()

        print(f"{n:<15}{t_secuencial:<20.4f}{t_arbol:<15.4f}{altura:<18}")
        filas.append((n, t_secuencial, t_arbol, altura))

    with open("resultados.csv", "w", encoding="utf-8") as f:
        f.write("n_elementos,secuencial_ms,arbol_ms,altura_arbol\n")
        for n, ts, ta, alt in filas:
            f.write(f"{n},{ts:.4f},{ta:.4f},{alt}\n")


if __name__ == "__main__":
    main()
