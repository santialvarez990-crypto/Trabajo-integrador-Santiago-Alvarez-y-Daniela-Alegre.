from modelos import Categoria


class ArbolCategorias:
    def __init__(self, raiz):
        self.raiz = raiz
        self.pasos = 0

    def agregar_categoria(self, nombre_padre, nombre_nueva):
        padre = self.buscar(nombre_padre)
        if padre is None:
            return False
        padre.agregar_subcategoria(Categoria(nombre_nueva))
        return True

    def cargar_actividades(self, actividades):
        sin_categoria = []
        for actividad in actividades:
            categoria = self.buscar(actividad.get_categoria())
            if categoria is None:
                self.raiz.agregar_actividad(actividad)
                sin_categoria.append(actividad)
            else:
                categoria.agregar_actividad(actividad)
        return sin_categoria

    def buscar(self, nombre):
        self.pasos = 0
        return self.buscar_desde(self.raiz, nombre.strip().lower())

    def buscar_desde(self, categoria, nombre):
        self.pasos += 1
        if categoria.get_nombre().lower() == nombre:
            return categoria
        for subcategoria in categoria.get_subcategorias():
            encontrada = self.buscar_desde(subcategoria, nombre)
            if encontrada is not None:
                return encontrada
        return None

    def ruta_hasta(self, nombre):
        return self.ruta_desde(self.raiz, nombre.strip().lower())

    def ruta_desde(self, categoria, nombre):
        if categoria.get_nombre().lower() == nombre:
            return [categoria.get_nombre()]
        for subcategoria in categoria.get_subcategorias():
            ruta = self.ruta_desde(subcategoria, nombre)
            if len(ruta) > 0:
                return [categoria.get_nombre()] + ruta
        return []

    def actividades_de(self, categoria):
        resultado = categoria.get_actividades()
        for subcategoria in categoria.get_subcategorias():
            resultado = resultado + self.actividades_de(subcategoria)
        return resultado

    def preorder(self):
        resultado = []
        self.recorrer_preorder(self.raiz, 0, resultado)
        return resultado

    def recorrer_preorder(self, categoria, nivel, resultado):
        resultado.append((categoria, nivel))
        for subcategoria in categoria.get_subcategorias():
            self.recorrer_preorder(subcategoria, nivel + 1, resultado)

    def postorder(self):
        resultado = []
        self.recorrer_postorder(self.raiz, 0, resultado)
        return resultado

    def recorrer_postorder(self, categoria, nivel, resultado):
        for subcategoria in categoria.get_subcategorias():
            self.recorrer_postorder(subcategoria, nivel + 1, resultado)
        resultado.append((categoria, nivel))

    def por_niveles(self):
        resultado = []
        cola = [(self.raiz, 0)]
        while len(cola) > 0:
            categoria, nivel = cola.pop(0)
            resultado.append((categoria, nivel))
            for subcategoria in categoria.get_subcategorias():
                cola.append((subcategoria, nivel + 1))
        return resultado

    def altura(self):
        return self.altura_desde(self.raiz)

    def altura_desde(self, categoria):
        mayor = 0
        for subcategoria in categoria.get_subcategorias():
            altura_hija = self.altura_desde(subcategoria)
            if altura_hija > mayor:
                mayor = altura_hija
        return 1 + mayor

    def cantidad_categorias(self):
        return len(self.preorder())
