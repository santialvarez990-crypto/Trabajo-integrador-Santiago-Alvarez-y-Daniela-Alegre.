class NodoAVL:
    def __init__(self, actividad):
        self.actividad = actividad
        self.izquierda = None
        self.derecha = None
        self.altura = 1


class ArbolAVL:
    def __init__(self):
        self.raiz = None
        self.cantidad = 0
        self.rotaciones = 0
        self.pasos = 0

    def altura_de(self, nodo):
        if nodo is None:
            return 0
        return nodo.altura

    def altura_total(self):
        return self.altura_de(self.raiz)

    def actualizar_altura(self, nodo):
        altura_izquierda = self.altura_de(nodo.izquierda)
        altura_derecha = self.altura_de(nodo.derecha)
        nodo.altura = 1 + max(altura_izquierda, altura_derecha)

    def factor_balance(self, nodo):
        return self.altura_de(nodo.izquierda) - self.altura_de(nodo.derecha)

    def rotar_derecha(self, nodo_desbalanceado):
        nueva_raiz = nodo_desbalanceado.izquierda
        nodo_desbalanceado.izquierda = nueva_raiz.derecha
        nueva_raiz.derecha = nodo_desbalanceado
        self.actualizar_altura(nodo_desbalanceado)
        self.actualizar_altura(nueva_raiz)
        self.rotaciones += 1
        return nueva_raiz

    def rotar_izquierda(self, nodo_desbalanceado):
        nueva_raiz = nodo_desbalanceado.derecha
        nodo_desbalanceado.derecha = nueva_raiz.izquierda
        nueva_raiz.izquierda = nodo_desbalanceado
        self.actualizar_altura(nodo_desbalanceado)
        self.actualizar_altura(nueva_raiz)
        self.rotaciones += 1
        return nueva_raiz

    def balancear(self, nodo):
        self.actualizar_altura(nodo)
        factor = self.factor_balance(nodo)

        if factor > 1:
            if self.factor_balance(nodo.izquierda) < 0:
                nodo.izquierda = self.rotar_izquierda(nodo.izquierda)
            return self.rotar_derecha(nodo)

        if factor < -1:
            if self.factor_balance(nodo.derecha) > 0:
                nodo.derecha = self.rotar_derecha(nodo.derecha)
            return self.rotar_izquierda(nodo)

        return nodo

    def insertar(self, actividad):
        self.raiz = self.insertar_en(self.raiz, actividad)
        self.cantidad += 1

    def insertar_en(self, nodo, actividad):
        if nodo is None:
            return NodoAVL(actividad)

        if actividad.get_duracion_estimada() < nodo.actividad.get_duracion_estimada():
            nodo.izquierda = self.insertar_en(nodo.izquierda, actividad)
        else:
            nodo.derecha = self.insertar_en(nodo.derecha, actividad)

        return self.balancear(nodo)

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

    def inorder(self):
        resultado = []
        self.recorrer_inorder(self.raiz, resultado)
        return resultado

    def recorrer_inorder(self, nodo, resultado):
        if nodo is None:
            return
        self.recorrer_inorder(nodo.izquierda, resultado)
        resultado.append(nodo.actividad)
        self.recorrer_inorder(nodo.derecha, resultado)

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

    def preorder(self):
        resultado = []
        self.recorrer_preorder(self.raiz, resultado)
        return resultado

    def recorrer_preorder(self, nodo, resultado):
        if nodo is None:
            return
        resultado.append(nodo.actividad)
        self.recorrer_preorder(nodo.izquierda, resultado)
        self.recorrer_preorder(nodo.derecha, resultado)

    def postorder(self):
        resultado = []
        self.recorrer_postorder(self.raiz, resultado)
        return resultado

    def recorrer_postorder(self, nodo, resultado):
        if nodo is None:
            return
        self.recorrer_postorder(nodo.izquierda, resultado)
        self.recorrer_postorder(nodo.derecha, resultado)
        resultado.append(nodo.actividad)
