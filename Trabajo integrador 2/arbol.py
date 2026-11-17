class _NodoFecha:
    __slots__ = ("fecha", "sesiones", "izquierda", "derecha")

    def __init__(self, fecha, sesion):
        self.fecha = fecha
        self.sesiones = [sesion]
        self.izquierda = None
        self.derecha = None


class ArbolBusquedaFechas:
    def __init__(self):
        self._raiz = None

    def insertar(self, sesion):
        if self._raiz is None:
            self._raiz = _NodoFecha(sesion.fecha, sesion)
            return
        actual = self._raiz
        while True:
            if sesion.fecha == actual.fecha:
                actual.sesiones.append(sesion)
                return
            elif sesion.fecha < actual.fecha:
                if actual.izquierda is None:
                    actual.izquierda = _NodoFecha(sesion.fecha, sesion)
                    return
                actual = actual.izquierda
            else:
                if actual.derecha is None:
                    actual.derecha = _NodoFecha(sesion.fecha, sesion)
                    return
                actual = actual.derecha

    def buscar(self, fecha_objetivo):
        actual = self._raiz
        while actual is not None:
            if fecha_objetivo == actual.fecha:
                return list(actual.sesiones)
            elif fecha_objetivo < actual.fecha:
                actual = actual.izquierda
            else:
                actual = actual.derecha
        return []

    def altura(self):
        """altura real del árbol construido
        sirve para verificar si esta balanceado"""
        def _altura(nodo):
            if nodo is None:
                return 0
            return 1 + max(_altura(nodo.izquierda), _altura(nodo.derecha))
        return _altura(self._raiz)
