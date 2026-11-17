class Elemento:
    def __init__(self, prioridad, orden, actividad):
        self.prioridad = prioridad
        self.orden = orden
        self.actividad = actividad


class HeapMaximo:
    def __init__(self):
        self.datos = []
        self.comparaciones = 0

    def esta_vacio(self):
        return len(self.datos) == 0

    def tamano(self):
        return len(self.datos)

    def es_mejor(self, uno, otro):
        self.comparaciones += 1
        if uno.prioridad != otro.prioridad:
            return uno.prioridad > otro.prioridad
        return uno.orden < otro.orden

    def intercambiar(self, i, j):
        auxiliar = self.datos[i]
        self.datos[i] = self.datos[j]
        self.datos[j] = auxiliar

    def subir(self, posicion):
        while posicion > 0:
            padre = (posicion - 1) // 2
            if self.es_mejor(self.datos[posicion], self.datos[padre]):
                self.intercambiar(posicion, padre)
                posicion = padre
            else:
                break

    def bajar(self, posicion):
        cantidad = len(self.datos)
        while True:
            izquierda = 2 * posicion + 1
            derecha = 2 * posicion + 2
            mejor = posicion
            if izquierda < cantidad and self.es_mejor(self.datos[izquierda], self.datos[mejor]):
                mejor = izquierda
            if derecha < cantidad and self.es_mejor(self.datos[derecha], self.datos[mejor]):
                mejor = derecha
            if mejor == posicion:
                break
            self.intercambiar(posicion, mejor)
            posicion = mejor

    def insertar(self, elemento):
        self.datos.append(elemento)
        self.subir(len(self.datos) - 1)

    def ver_maximo(self):
        if self.esta_vacio():
            return None
        return self.datos[0]

    def extraer_maximo(self):
        if self.esta_vacio():
            return None
        maximo = self.datos[0]
        ultimo = self.datos.pop()
        if not self.esta_vacio():
            self.datos[0] = ultimo
            self.bajar(0)
        return maximo

    def construir(self, elementos):
        self.datos = list(elementos)
        posicion = len(self.datos) // 2 - 1
        while posicion >= 0:
            self.bajar(posicion)
            posicion -= 1
