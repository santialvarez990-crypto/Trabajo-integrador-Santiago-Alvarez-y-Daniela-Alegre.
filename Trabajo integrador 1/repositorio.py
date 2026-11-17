"""
repositorio.py
Mantiene las actividades en memoria y expone las tres operaciones
requeridas: buscar, listar, filtrar. No sabe nada de archivos ni de terminal.
"""


class RepositorioActividades:
    def __init__(self, actividades=None):
        self._actividades = actividades if actividades else []

    def cargar(self, actividades):
        self._actividades = actividades

    def listar(self):
        """Devuelve todas las actividades."""
        return list(self._actividades)

    def buscar(self, texto):
        """Búsqueda por coincidencia parcial (case-insensitive) en el nombre."""
        texto = texto.lower()
        return [a for a in self._actividades if texto in a.get_nombre().lower()]

    def filtrar(self, categoria=None, duracion_maxima=None):
        """Filtra por categoría exacta y/o por duración máxima disponible."""
        resultado = self._actividades
        if categoria:
            resultado = [a for a in resultado if a.get_categoria().lower() == categoria.lower()]
        if duracion_maxima is not None:
            resultado = [a for a in resultado if a.get_duracion_estimada() <= duracion_maxima]
        return resultado
