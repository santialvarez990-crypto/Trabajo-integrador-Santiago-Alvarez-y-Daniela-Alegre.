from arbol_avl import ArbolAVL

class RepositorioActividades:
    def __init__(self, actividades=None):
        self._actividades = []
        self._arbol = ArbolAVL()
        if actividades:
            self.cargar(actividades)

    def cargar(self, actividades):
        self._actividades = list(actividades)
        self._arbol = ArbolAVL()
        for actividad in self._actividades:
            self._arbol.insertar(actividad)

    def agregar(self, actividad):
        self._actividades.append(actividad)
        self._arbol.insertar(actividad)

    def listar(self):
        return list(self._actividades)

    def listar_por_duracion(self):
        return self._arbol.inorder()

    def buscar(self, texto):
        texto = texto.lower()
        resultado = []
        for actividad in self._actividades:
            if texto in actividad.get_nombre().lower():
                resultado.append(actividad)
        return resultado

    def filtrar(self, categoria=None, duracion_maxima=None):
        if duracion_maxima is not None:
            resultado = self._arbol.hasta(duracion_maxima)
        else:
            resultado = list(self._actividades)

        if categoria:
            solo_categoria = []
            for actividad in resultado:
                if actividad.get_categoria().lower() == categoria.lower():
                    solo_categoria.append(actividad)
            resultado = solo_categoria
        return resultado

    def filtrar_secuencial(self, categoria=None, duracion_maxima=None):
        resultado = []
        for actividad in self._actividades:
            if categoria and actividad.get_categoria().lower() != categoria.lower():
                continue
            if duracion_maxima is not None and actividad.get_duracion_estimada() > duracion_maxima:
                continue
            resultado.append(actividad)
        return resultado

    def sugerir_para_tiempo(self, minutos):
        return self._arbol.mayor_hasta(minutos)

    def sugerir_para_tiempo_secuencial(self, minutos):
        mejor = None
        for actividad in self._actividades:
            duracion = actividad.get_duracion_estimada()
            if duracion <= minutos:
                if mejor is None or duracion >= mejor.get_duracion_estimada():
                    mejor = actividad
        return mejor

    def altura(self):
        return self._arbol.altura_total()

    def pasos_ultima_busqueda(self):
        return self._arbol.pasos
