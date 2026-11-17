from datetime import datetime


class Categoria:
    def __init__(self, nombre, subcategorias=None):
        self._nombre = nombre
        self._subcategorias = subcategorias if subcategorias else []
        self._actividades = []

    def get_nombre(self):
        return self._nombre

    def get_subcategorias(self):
        return list(self._subcategorias)

    def agregar_subcategoria(self, categoria):
        self._subcategorias.append(categoria)

    def get_actividades(self):
        return list(self._actividades)

    def agregar_actividad(self, actividad):
        self._actividades.append(actividad)

    def __repr__(self):
        return f"Categoria({self._nombre})"


class Actividad:
    def __init__(self, nombre, categoria, duracion_estimada):
        self._nombre = nombre
        self._categoria = categoria
        self._duracion_estimada = duracion_estimada

    def get_nombre(self):
        return self._nombre

    def get_categoria(self):
        return self._categoria

    def get_duracion_estimada(self):
        return self._duracion_estimada

    def __repr__(self):
        return f"{self._nombre} ({self._categoria}, {self._duracion_estimada} min)"


class Desafio:
    ESTADOS_VALIDOS = ("pendiente", "cumplido")

    def __init__(self, actividad, prioridad):
        self._actividad = actividad
        self._prioridad = prioridad
        self._estado = "pendiente"

    def get_actividad(self):
        return self._actividad

    def get_prioridad(self):
        return self._prioridad

    def get_estado(self):
        return self._estado

    def cumplir(self):
        self._estado = "cumplido"

    def __repr__(self):
        return f"Desafio[{self._estado}] {self._actividad.get_nombre()} (prio={self._prioridad})"


class SesionUso:
    def __init__(self, app_o_impulso, actividad_alternativa=None, timestamp=None):
        self._timestamp = timestamp or datetime.now()
        self._app_o_impulso = app_o_impulso
        self._actividad_alternativa = actividad_alternativa

    def get_timestamp(self):
        return self._timestamp

    def get_app_o_impulso(self):
        return self._app_o_impulso

    def get_actividad_alternativa(self):
        return self._actividad_alternativa

    def __repr__(self):
        alt = self._actividad_alternativa.get_nombre() if self._actividad_alternativa else "ninguna"
        return f"[{self._timestamp.strftime('%H:%M')}] impulso='{self._app_o_impulso}' -> alternativa={alt}"


class Usuario:
    def __init__(self, nombre, edad):
        self._nombre = nombre
        self._edad = edad
        self._racha = 0
        self._historial_sesiones = []
        self._desafios = []

    def get_nombre(self):
        return self._nombre

    def get_edad(self):
        return self._edad

    def get_racha(self):
        return self._racha

    def get_historial_sesiones(self):
        return list(self._historial_sesiones)

    def get_desafios(self):
        return list(self._desafios)

    def registrar_sesion(self, sesion):
        self._historial_sesiones.append(sesion)

    def asignar_desafio(self, desafio):
        self._desafios.append(desafio)

    def cumplir_desafio(self, desafio):
        desafio.cumplir()
        self.actualizar_racha()

    def actualizar_racha(self):
        self._racha += 1

    def __repr__(self):
        return f"Usuario({self._nombre}, {self._edad} años, racha={self._racha})"
