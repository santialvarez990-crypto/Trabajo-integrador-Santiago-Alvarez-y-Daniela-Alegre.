import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arbol_binario import ArbolBinario
from modelos import Actividad


def armar_arbol(duraciones):
    arbol = ArbolBinario()
    for numero, duracion in enumerate(duraciones):
        arbol.insertar(Actividad("Actividad " + str(numero), "Prueba", duracion))
    return arbol


def duraciones_de(actividades):
    lista = []
    for actividad in actividades:
        lista.append(actividad.get_duracion_estimada())
    return lista


class TestArbolVacio(unittest.TestCase):
    def test_arbol_vacio(self):
        arbol = ArbolBinario()
        self.assertIsNone(arbol.raiz)
        self.assertEqual(arbol.cantidad, 0)
        self.assertEqual(arbol.altura, 0)
        self.assertIsNone(arbol.buscar(10))
        self.assertIsNone(arbol.mayor_hasta(10))
        self.assertEqual(arbol.hasta(10), [])
        self.assertEqual(arbol.inorder(), [])
        self.assertEqual(arbol.preorder(), [])
        self.assertEqual(arbol.postorder(), [])


class TestInsertarYBuscar(unittest.TestCase):
    def setUp(self):
        self.arbol = armar_arbol([10, 5, 15, 3, 7, 12, 18])

    def test_cantidad_y_altura(self):
        self.assertEqual(self.arbol.cantidad, 7)
        self.assertEqual(self.arbol.altura, 3)

    def test_la_raiz_es_la_primera_actividad(self):
        self.assertEqual(self.arbol.raiz.actividad.get_duracion_estimada(), 10)

    def test_buscar_una_que_existe(self):
        self.assertEqual(self.arbol.buscar(7).get_duracion_estimada(), 7)

    def test_buscar_una_que_no_existe(self):
        self.assertIsNone(self.arbol.buscar(99))
        self.assertIsNone(self.arbol.buscar(1))

    def test_pasos_de_la_busqueda(self):
        self.arbol.buscar(10)
        self.assertEqual(self.arbol.pasos, 1)
        self.arbol.buscar(18)
        self.assertEqual(self.arbol.pasos, 3)


class TestRecorridos(unittest.TestCase):
    def setUp(self):
        self.arbol = armar_arbol([10, 5, 15, 3, 7, 12, 18])

    def test_inorder_queda_ordenado(self):
        self.assertEqual(duraciones_de(self.arbol.inorder()), [3, 5, 7, 10, 12, 15, 18])

    def test_preorder(self):
        self.assertEqual(duraciones_de(self.arbol.preorder()), [10, 5, 3, 7, 15, 12, 18])

    def test_postorder(self):
        self.assertEqual(duraciones_de(self.arbol.postorder()), [3, 7, 5, 12, 18, 15, 10])


class TestMayorHastaYHasta(unittest.TestCase):
    def setUp(self):
        self.arbol = armar_arbol([10, 5, 15, 3, 7, 12, 18])

    def test_mayor_hasta_justo(self):
        self.assertEqual(self.arbol.mayor_hasta(12).get_duracion_estimada(), 12)

    def test_mayor_hasta_entre_dos_duraciones(self):
        self.assertEqual(self.arbol.mayor_hasta(14).get_duracion_estimada(), 12)
        self.assertEqual(self.arbol.mayor_hasta(4).get_duracion_estimada(), 3)

    def test_mayor_hasta_con_mucho_tiempo(self):
        self.assertEqual(self.arbol.mayor_hasta(500).get_duracion_estimada(), 18)

    def test_mayor_hasta_si_ninguna_entra(self):
        self.assertIsNone(self.arbol.mayor_hasta(2))

    def test_hasta_devuelve_ordenado(self):
        self.assertEqual(duraciones_de(self.arbol.hasta(10)), [3, 5, 7, 10])
        self.assertEqual(duraciones_de(self.arbol.hasta(11)), [3, 5, 7, 10])
        self.assertEqual(duraciones_de(self.arbol.hasta(500)), [3, 5, 7, 10, 12, 15, 18])

    def test_hasta_si_ninguna_entra(self):
        self.assertEqual(self.arbol.hasta(2), [])


class TestDuracionesRepetidas(unittest.TestCase):
    def test_las_repetidas_van_a_la_derecha(self):
        arbol = armar_arbol([10, 10])
        self.assertIsNone(arbol.raiz.izquierda)
        self.assertEqual(arbol.raiz.derecha.actividad.get_duracion_estimada(), 10)
        self.assertEqual(arbol.altura, 2)

    def test_no_se_pierde_ninguna(self):
        arbol = armar_arbol([15, 5, 15, 15])
        self.assertEqual(arbol.cantidad, 4)
        self.assertEqual(duraciones_de(arbol.inorder()), [5, 15, 15, 15])

    def test_buscar_devuelve_la_primera_cargada(self):
        arbol = armar_arbol([15, 15])
        self.assertEqual(arbol.buscar(15).get_nombre(), "Actividad 0")

    def test_mayor_hasta_devuelve_la_ultima_cargada(self):
        arbol = armar_arbol([15, 15, 5])
        self.assertEqual(arbol.mayor_hasta(20).get_nombre(), "Actividad 1")


class TestDatosYaOrdenados(unittest.TestCase):
    def test_con_datos_ordenados_el_arbol_se_alarga(self):
        arbol = armar_arbol(list(range(1, 301)))
        self.assertEqual(arbol.cantidad, 300)
        self.assertEqual(arbol.altura, 300)

    def test_igual_funciona(self):
        arbol = armar_arbol(list(range(1, 301)))
        self.assertEqual(arbol.buscar(300).get_duracion_estimada(), 300)
        self.assertEqual(len(arbol.inorder()), 300)


if __name__ == "__main__":
    unittest.main()
