class Nodo:
    def __init__(self, actividad):
        self.actividad = actividad
        self.izquierda = None
        self.derecha = None


class ArbolBinario:
    def __init__(self):
        self.raiz = None
        self.cantidad = 0
        self.altura = 0
        self.pasos = 0

    def insertar(self, actividad):
        nuevo = Nodo(actividad)
        self.cantidad += 1

        if self.raiz is None:
            self.raiz = nuevo
            self.altura = 1
            return

        duracion = actividad.get_duracion_estimada()
        actual = self.raiz
        nivel = 1
        while True:
            nivel += 1
            if duracion < actual.actividad.get_duracion_estimada():
                if actual.izquierda is None:
                    actual.izquierda = nuevo
                    break
                actual = actual.izquierda
            else:
                if actual.derecha is None:
                    actual.derecha = nuevo
                    break
                actual = actual.derecha

        if nivel > self.altura:
            self.altura = nivel

    def buscar(self, duracion):
        actual = self.raiz
        self.pasos = 0
        while actual is not None:
            self.pasos += 1
            duracion_actual = actual.actividad.get_duracion_estimada()
            if duracion == duracion_actual:
                return actual.actividad
            elif duracion < duracion_actual:
                actual = actual.izquierda
            else:
                actual = actual.derecha
        return None

    def mayor_hasta(self, minutos):
        actual = self.raiz
        mejor = None
        self.pasos = 0
        while actual is not None:
            self.pasos += 1
            if actual.actividad.get_duracion_estimada() <= minutos:
                mejor = actual.actividad
                actual = actual.derecha
            else:
                actual = actual.izquierda
        return mejor

    def hasta(self, minutos):
        resultado = []
        self.juntar_hasta(self.raiz, minutos, resultado)
        return resultado

    def juntar_hasta(self, nodo, minutos, resultado):
        if nodo is None:
            return
        self.juntar_hasta(nodo.izquierda, minutos, resultado)
        if nodo.actividad.get_duracion_estimada() <= minutos:
            resultado.append(nodo.actividad)
            self.juntar_hasta(nodo.derecha, minutos, resultado)

    def inorder(self):
        resultado = []
        self._inorder(self.raiz, resultado)
        return resultado

    def _inorder(self, nodo, resultado):
        if nodo is None:
            return
        self._inorder(nodo.izquierda, resultado)
        resultado.append(nodo.actividad)
        self._inorder(nodo.derecha, resultado)

    def preorder(self):
        resultado = []
        self._preorder(self.raiz, resultado)
        return resultado

    def _preorder(self, nodo, resultado):
        if nodo is None:
            return
        resultado.append(nodo.actividad)
        self._preorder(nodo.izquierda, resultado)
        self._preorder(nodo.derecha, resultado)

    def postorder(self):
        resultado = []
        self._postorder(self.raiz, resultado)
        return resultado

    def _postorder(self, nodo, resultado):
        if nodo is None:
            return
        self._postorder(nodo.izquierda, resultado)
        self._postorder(nodo.derecha, resultado)
        resultado.append(nodo.actividad)
