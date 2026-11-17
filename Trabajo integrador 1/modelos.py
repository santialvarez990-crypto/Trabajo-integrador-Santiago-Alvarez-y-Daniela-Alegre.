"""
modelos.py
Clases principales del dominio de "Pause".

Convención de encapsulamiento:
- Atributos "privados" con prefijo simple "_" (privado por convención en Python).
- Getters explícitos donde el dato debe poder consultarse desde afuera.
- No se exponen setters genéricos: los cambios de estado se hacen a través
  de métodos con intención clara (ej. cumplir_desafio(), actualizar_racha()).
"""

from datetime import datetime


class Categoria:
    """Representa una categoría de actividades. Puede tener subcategorías
    (esto es la base sobre la que más adelante se va a construir el árbol)."""

    def __init__(self, nombre, subcategorias=None):
        self._nombre = nombre
        self._subcategorias = subcategorias if subcategorias else []

    def get_nombre(self):
        return self._nombre

    def get_subcategorias(self):
        return list(self._subcategorias)  # copia, para no exponer la lista interna

    def agregar_subcategoria(self, categoria):
        self._subcategorias.append(categoria)

    def __repr__(self):
        return f"Categoria({self._nombre})"


class Actividad:
    """Una actividad alternativa que Pause puede sugerir."""

    def __init__(self, nombre, categoria, duracion_estimada):
        self._nombre = nombre
        self._categoria = categoria  # string simple en esta v1
        self._duracion_estimada = duracion_estimada  # en minutos

    def get_nombre(self):
        return self._nombre

    def get_categoria(self):
        return self._categoria

    def get_duracion_estimada(self):
        return self._duracion_estimada

    def __repr__(self):
        return f"{self._nombre} ({self._categoria}, {self._duracion_estimada} min)"


class Desafio:
    """Un desafío pendiente asociado a una actividad.
    La prioridad numérica es la base para el futuro heap."""

    ESTADOS_VALIDOS = ("pendiente", "cumplido")

    def __init__(self, actividad, prioridad):
        self._actividad = actividad
        self._prioridad = prioridad  # menor número = mayor prioridad
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
    """Un registro de impulso/sesión: el usuario quiso abrir una app
    y el sistema le ofreció (o no) una alternativa."""

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
    """Usuario de la aplicación."""

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

    def registrar_sesion(self, sesion: SesionUso):
        self._historial_sesiones.append(sesion)

    def asignar_desafio(self, desafio: Desafio):
        self._desafios.append(desafio)

    def cumplir_desafio(self, desafio: Desafio):
        desafio.cumplir()
        self._racha += 1

    def __repr__(self):
        return f"Usuario({self._nombre}, {self._edad} años, racha={self._racha})"
