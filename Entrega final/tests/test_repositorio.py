import os
import random
import sys
import unittest

CARPETA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, CARPETA_PROYECTO)

from gestor_datos import GestorDatos
from modelos import Actividad, Usuario
from repositorio import RepositorioActividades


def armar_repositorio():
    repo = RepositorioActividades()
    repo.cargar([
        Actividad("Caminata corta", "Movimiento", 15),
        Actividad("Estiramientos", "Movimiento", 5),
        Actividad("Llamar a un amigo", "Social", 10),
        Actividad("Leer 10 páginas", "Lectura", 15),
        Actividad("Podcast", "Aprendizaje", 25),
    ])
    return repo


def nombres_de(actividades):
    lista = []
    for actividad in actividades:
        lista.append(actividad.get_nombre())
    return lista


class TestRepositorio(unittest.TestCase):
    def setUp(self):
        self.repo = armar_repositorio()

    def test_listar_respeta_el_orden_de_carga(self):
        nombres = nombres_de(self.repo.listar())
        self.assertEqual(nombres[0], "Caminata corta")
        self.assertEqual(len(nombres), 5)

    def test_listar_por_duracion(self):
        duraciones = []
        for actividad in self.repo.listar_por_duracion():
            duraciones.append(actividad.get_duracion_estimada())
        self.assertEqual(duraciones, [5, 10, 15, 15, 25])

    def test_listar_por_duracion_mantiene_el_orden_de_los_empates(self):
        nombres = nombres_de(self.repo.listar_por_duracion())
        self.assertEqual(nombres.index("Caminata corta") < nombres.index("Leer 10 páginas"), True)

    def test_sugerir_para_tiempo(self):
        self.assertEqual(self.repo.sugerir_para_tiempo(12).get_nombre(), "Llamar a un amigo")
        self.assertEqual(self.repo.sugerir_para_tiempo(500).get_nombre(), "Podcast")

    def test_sugerir_con_empate_gana_la_ultima_cargada(self):
        self.assertEqual(self.repo.sugerir_para_tiempo(15).get_nombre(), "Leer 10 páginas")

    def test_sugerir_si_no_entra_ninguna(self):
        self.assertIsNone(self.repo.sugerir_para_tiempo(4))
        self.assertIsNone(self.repo.sugerir_para_tiempo(0))

    def test_sugerir_sin_actividades(self):
        self.assertIsNone(RepositorioActividades().sugerir_para_tiempo(30))

    def test_filtrar_por_duracion_maxima(self):
        nombres = nombres_de(self.repo.filtrar(duracion_maxima=10))
        self.assertEqual(nombres, ["Estiramientos", "Llamar a un amigo"])

    def test_filtrar_por_categoria_y_duracion(self):
        nombres = nombres_de(self.repo.filtrar(categoria="movimiento", duracion_maxima=10))
        self.assertEqual(nombres, ["Estiramientos"])

    def test_filtrar_solo_por_categoria(self):
        self.assertEqual(len(self.repo.filtrar(categoria="Movimiento")), 2)

    def test_buscar_por_nombre(self):
        self.assertEqual(nombres_de(self.repo.buscar("llamar")), ["Llamar a un amigo"])

    def test_agregar_actualiza_el_arbol(self):
        self.repo.agregar(Actividad("Respirar profundo", "Bienestar", 3))
        self.assertEqual(self.repo.sugerir_para_tiempo(4).get_nombre(), "Respirar profundo")
        self.assertEqual(self.repo.listar_por_duracion()[0].get_nombre(), "Respirar profundo")


class TestArbolContraSecuencial(unittest.TestCase):
    def test_con_datos_al_azar(self):
        azar = random.Random(3)
        actividades = []
        for numero in range(1000):
            categoria = azar.choice(["X", "Y", "Z"])
            duracion = azar.randint(1, 120)
            actividades.append(Actividad("A" + str(numero), categoria, duracion))
        repo = RepositorioActividades(actividades)

        for minutos in range(0, 130, 3):
            self.assertIs(repo.sugerir_para_tiempo(minutos),
                          repo.sugerir_para_tiempo_secuencial(minutos))

            con_arbol = sorted(nombres_de(repo.filtrar("X", minutos)))
            secuencial = sorted(nombres_de(repo.filtrar_secuencial("X", minutos)))
            self.assertEqual(con_arbol, secuencial)


class TestConDatosReales(unittest.TestCase):
    def test_cargar_json_y_sugerir(self):
        gestor = GestorDatos(carpeta_datos=os.path.join(CARPETA_PROYECTO, "datos"))
        repo = RepositorioActividades(gestor.cargar_actividades())
        self.assertEqual(len(repo.listar()), 13)
        self.assertEqual(repo.sugerir_para_tiempo(30).get_nombre(), "Escuchar un podcast")
        self.assertEqual(repo.sugerir_para_tiempo(12).get_duracion_estimada(), 10)
        self.assertIsNone(repo.sugerir_para_tiempo(2))

    def test_la_racha_se_actualiza_con_un_metodo(self):
        usuario = Usuario("Franco", 11)
        usuario.actualizar_racha()
        self.assertEqual(usuario.get_racha(), 1)


if __name__ == "__main__":
    unittest.main()
