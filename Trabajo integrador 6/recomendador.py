from heap import Elemento, HeapMaximo

PUNTOS_POR_ENCAJE = 5
MAXIMO_DE_GUSTO = 3
FACTOR_SI_REPITE = 0.5


def clave_para_ordenar(elemento):
    return (-elemento.prioridad, elemento.orden)


class Recomendador:
    def __init__(self, repositorio):
        self.repositorio = repositorio
        self.comparaciones = 0

    def calcular_prioridad(self, actividad, minutos, aceptadas):
        encaje = actividad.get_duracion_estimada() / minutos * PUNTOS_POR_ENCAJE

        veces = aceptadas.count(actividad.get_nombre())
        if veces > MAXIMO_DE_GUSTO:
            veces = MAXIMO_DE_GUSTO

        prioridad = encaje + veces

        if len(aceptadas) > 0 and aceptadas[len(aceptadas) - 1] == actividad.get_nombre():
            prioridad = prioridad * FACTOR_SI_REPITE

        return prioridad

    def armar_elementos(self, minutos, aceptadas):
        elementos = []
        if minutos <= 0:
            return elementos
        candidatas = self.repositorio.filtrar(duracion_maxima=minutos)
        orden = 0
        for actividad in candidatas:
            prioridad = self.calcular_prioridad(actividad, minutos, aceptadas)
            elementos.append(Elemento(prioridad, orden, actividad))
            orden += 1
        return elementos

    def elegir_con_heap(self, elementos, n):
        heap = HeapMaximo()
        heap.construir(elementos)
        resultado = []
        while len(resultado) < n and not heap.esta_vacio():
            resultado.append(heap.extraer_maximo())
        self.comparaciones = heap.comparaciones
        return resultado

    def elegir_ordenando(self, elementos, n):
        ordenados = sorted(elementos, key=clave_para_ordenar)
        return ordenados[:n]

    def top_n(self, minutos, n, aceptadas):
        elementos = self.armar_elementos(minutos, aceptadas)
        return self.elegir_con_heap(elementos, n)

    def top_n_ordenando(self, minutos, n, aceptadas):
        elementos = self.armar_elementos(minutos, aceptadas)
        return self.elegir_ordenando(elementos, n)
