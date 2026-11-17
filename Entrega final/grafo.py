PESO_MISMA_CATEGORIA = 1
PESO_MISMO_GRUPO = 2


class Arista:
    def __init__(self, origen, destino, peso):
        self.origen = origen
        self.destino = destino
        self.peso = peso


class Recorrido:
    def __init__(self, origen):
        self.origen = origen
        self.orden = []
        self.distancia = {}
        self.anterior = {}
        self.aristas_revisadas = 0

    def visitado(self, nombre):
        return nombre in self.anterior

    def registrar(self, nombre, anterior, distancia):
        self.orden.append(nombre)
        self.anterior[nombre] = anterior
        self.distancia[nombre] = distancia

    def camino_hasta(self, destino):
        if not self.visitado(destino):
            return []
        camino = []
        actual = destino
        while actual is not None:
            camino.append(actual)
            actual = self.anterior[actual]
        camino.reverse()
        return camino


def clave_para_ordenar(arista):
    return (arista.peso, arista.destino)


class Grafo:
    def __init__(self):
        self.actividades = {}
        self.conexiones = {}
        self.cantidad_aristas = 0
        self.puentes_rechazados = 0

    def agregar_vertice(self, actividad):
        nombre = actividad.get_nombre()
        if nombre in self.actividades:
            return False
        self.actividades[nombre] = actividad
        self.conexiones[nombre] = []
        return True

    def agregar_arista(self, nombre_a, nombre_b, peso):
        if nombre_a == nombre_b:
            return False
        if not self.existe_vertice(nombre_a) or not self.existe_vertice(nombre_b):
            return False
        if self.existe_arista(nombre_a, nombre_b):
            return False
        self.conexiones[nombre_a].append(Arista(nombre_a, nombre_b, peso))
        self.conexiones[nombre_b].append(Arista(nombre_b, nombre_a, peso))
        self.cantidad_aristas += 1
        return True

    def existe_vertice(self, nombre):
        return nombre in self.actividades

    def existe_arista(self, nombre_a, nombre_b):
        if not self.existe_vertice(nombre_a):
            return False
        for arista in self.conexiones[nombre_a]:
            if arista.destino == nombre_b:
                return True
        return False

    def peso_de(self, nombre_a, nombre_b):
        if not self.existe_vertice(nombre_a):
            return None
        for arista in self.conexiones[nombre_a]:
            if arista.destino == nombre_b:
                return arista.peso
        return None

    def get_actividad(self, nombre):
        if self.existe_vertice(nombre):
            return self.actividades[nombre]
        return None

    def nombres(self):
        return list(self.actividades.keys())

    def cantidad_vertices(self):
        return len(self.actividades)

    def grado_de(self, nombre):
        if not self.existe_vertice(nombre):
            return 0
        return len(self.conexiones[nombre])

    def vecinos_de(self, nombre):
        if not self.existe_vertice(nombre):
            return []
        return sorted(self.conexiones[nombre], key=clave_para_ordenar)

    def relacionadas(self, nombre, peso_maximo):
        resultado = []
        for arista in self.vecinos_de(nombre):
            if arista.peso <= peso_maximo:
                resultado.append(arista)
        return resultado

    def mas_conectada(self):
        mejor = None
        for nombre in self.actividades:
            if mejor is None or self.grado_de(nombre) > self.grado_de(mejor):
                mejor = nombre
        return mejor

    def densidad(self):
        n = self.cantidad_vertices()
        if n < 2:
            return 0
        return 2 * self.cantidad_aristas / (n * (n - 1))

    def listar_aristas(self):
        resultado = []
        for nombre in self.actividades:
            for arista in self.conexiones[nombre]:
                if arista.origen < arista.destino:
                    resultado.append(arista)
        return resultado


    def bfs(self, origen):
        recorrido = Recorrido(origen)
        if not self.existe_vertice(origen):
            return recorrido
        recorrido.registrar(origen, None, 0)
        cola = [origen]
        posicion = 0
        while posicion < len(cola):
            actual = cola[posicion]
            posicion += 1
            for arista in self.vecinos_de(actual):
                recorrido.aristas_revisadas += 1
                if not recorrido.visitado(arista.destino):
                    recorrido.registrar(arista.destino, actual, recorrido.distancia[actual] + 1)
                    cola.append(arista.destino)
        return recorrido

    def dfs(self, origen):
        recorrido = Recorrido(origen)
        if not self.existe_vertice(origen):
            return recorrido
        pila = [(origen, None, 0)]
        while len(pila) > 0:
            nombre, anterior, profundidad = pila.pop()
            if recorrido.visitado(nombre):
                continue
            recorrido.registrar(nombre, anterior, profundidad)
            vecinos = self.vecinos_de(nombre)
            posicion = len(vecinos) - 1
            while posicion >= 0:
                recorrido.aristas_revisadas += 1
                destino = vecinos[posicion].destino
                if not recorrido.visitado(destino):
                    pila.append((destino, nombre, profundidad + 1))
                posicion -= 1
        return recorrido

    def mas_cercana_de_categoria(self, origen, categoria):
        recorrido = self.bfs(origen)
        buscada = categoria.strip().lower()
        for nombre in recorrido.orden:
            if nombre != origen and self.actividades[nombre].get_categoria().lower() == buscada:
                return recorrido.camino_hasta(nombre)
        return []

    def esta_conectado(self):
        if self.cantidad_vertices() == 0:
            return True
        primero = self.nombres()[0]
        return len(self.dfs(primero).orden) == self.cantidad_vertices()


def grupo_de(arbol, actividad):
    ruta = arbol.ruta_hasta(actividad.get_categoria())
    if len(ruta) > 1:
        return ruta[1]
    return None


def armar_grafo(actividades, arbol, puentes):
    grafo = Grafo()
    for actividad in actividades:
        grafo.agregar_vertice(actividad)

    cantidad = len(actividades)
    for i in range(cantidad):
        for j in range(i + 1, cantidad):
            una = actividades[i]
            otra = actividades[j]
            if una.get_categoria() == otra.get_categoria():
                grafo.agregar_arista(una.get_nombre(), otra.get_nombre(), PESO_MISMA_CATEGORIA)
            else:
                grupo_una = grupo_de(arbol, una)
                if grupo_una is not None and grupo_una == grupo_de(arbol, otra):
                    grafo.agregar_arista(una.get_nombre(), otra.get_nombre(), PESO_MISMO_GRUPO)

    for puente in puentes:
        agregada = grafo.agregar_arista(puente["actividad_a"], puente["actividad_b"], puente["peso"])
        if not agregada:
            grafo.puentes_rechazados += 1

    return grafo
