import json
import os
from modelos import Actividad, Usuario, Categoria


class GestorDatos:
    def __init__(self, carpeta_datos="datos"):
        self._carpeta_datos = carpeta_datos

    def _ruta(self, nombre_archivo):
        return os.path.join(self._carpeta_datos, nombre_archivo)

    def cargar_actividades(self, archivo="actividades.json"):
        ruta = self._ruta(archivo)
        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)

        actividades = []
        for item in data.get("actividades", []):
            actividades.append(
                Actividad(
                    nombre=item["nombre"],
                    categoria=item["categoria"],
                    duracion_estimada=item["duracion_estimada"],
                )
            )
        return actividades

    def cargar_usuarios(self, archivo="usuarios.json"):
        ruta = self._ruta(archivo)
        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)

        usuarios = []
        for item in data.get("usuarios", []):
            usuarios.append(Usuario(nombre=item["nombre"], edad=item["edad"]))
        return usuarios

    def cargar_categorias(self, archivo="categorias.json"):
        ruta = self._ruta(archivo)
        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
        return self._armar_categoria(data)

    def _armar_categoria(self, datos):
        categoria = Categoria(datos["nombre"])
        for datos_hija in datos.get("subcategorias", []):
            categoria.agregar_subcategoria(self._armar_categoria(datos_hija))
        return categoria

    def cargar_aceptadas(self, archivo="sesiones.json"):
        ruta = self._ruta(archivo)
        aceptadas = []
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as f:
                registros = json.load(f)
            for registro in registros:
                if registro["alternativa"] is not None:
                    aceptadas.append(registro["alternativa"])
        return aceptadas

    def cargar_puentes(self, archivo="puentes.json"):
        ruta = self._ruta(archivo)
        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("puentes", [])

    def guardar_sesion(self, sesion, archivo="sesiones.json"):
        ruta = self._ruta(archivo)
        registros = []
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as f:
                registros = json.load(f)

        registros.append(
            {
                "timestamp": sesion.get_timestamp().isoformat(),
                "impulso": sesion.get_app_o_impulso(),
                "alternativa": (
                    sesion.get_actividad_alternativa().get_nombre()
                    if sesion.get_actividad_alternativa()
                    else None
                ),
            }
        )

        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(registros, f, ensure_ascii=False, indent=2)
