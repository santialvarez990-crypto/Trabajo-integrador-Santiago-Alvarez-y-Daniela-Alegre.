import os

from gestor_datos import GestorDatos
from repositorio import RepositorioActividades
from arbol_general import ArbolCategorias
from recomendador import Recomendador
from grafo import armar_grafo
from modelos import SesionUso, Usuario, Categoria

CANTIDAD_EN_RANKING = 5
CARPETA_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos")


def mostrar_menu():
    print("\n==================== PAUSE ====================")
    print(" 1) Ver tiempo en pantalla")
    print(" 2) Ver mis actividades")
    print(" 3) ¿Qué hago ahora?")
    print(" 4) Ver desafíos pendientes")
    print(" 5) Activar/Desactivar modo minimalista")
    print(" 6) Estadísticas de la semana")
    print(" 7) Explorar categorías")
    print(" 8) Actividades relacionadas")
    print(" 0) Salir")
    print("=================================================")


def pedir_entero_positivo(mensaje):
    try:
        valor = int(input(mensaje).strip())
    except ValueError:
        print("Ingresá un número válido.")
        return None
    if valor <= 0:
        print("Ingresá un número mayor que cero.")
        return None
    return valor


def mostrar_resultados(resultados):
    if not resultados:
        print("No se encontraron actividades.")
        return
    for i, a in enumerate(resultados, start=1):
        print(f"  {i}. {a}")


def submenu_actividades(repo, arbol):
    print("\n-- Ver mis actividades --")
    print(" a) Listar todas")
    print(" b) Buscar por nombre")
    print(" c) Filtrar por categoría")
    print(" d) Filtrar por duración máxima")
    print(" e) Listar de la más corta a la más larga")
    opcion = input("Elegí una opción: ").strip().lower()

    if opcion == "a":
        mostrar_resultados(repo.listar())
    elif opcion == "b":
        texto = input("¿Qué buscás?: ").strip()
        mostrar_resultados(repo.buscar(texto))
    elif opcion == "c":
        nombre = input("Categoría: ").strip()
        categoria = arbol.buscar(nombre)
        if categoria is None:
            print("No existe esa categoría.")
        else:
            mostrar_resultados(arbol.actividades_de(categoria))
    elif opcion == "d":
        minutos = pedir_entero_positivo("¿Cuántos minutos tenés?: ")
        if minutos is not None:
            mostrar_resultados(repo.filtrar(duracion_maxima=minutos))
    elif opcion == "e":
        mostrar_resultados(repo.listar_por_duracion())
    else:
        print("Opción inválida.")


def explorar_jerarquia(arbol):
    actual = arbol.raiz
    camino = [arbol.raiz]

    while True:
        nombres = []
        for categoria in camino:
            nombres.append(categoria.get_nombre())
        print("\nEstás en: " + " > ".join(nombres))

        subcategorias = actual.get_subcategorias()
        if len(subcategorias) > 0:
            print("Subcategorías:")
            for numero, subcategoria in enumerate(subcategorias, start=1):
                cantidad = len(arbol.actividades_de(subcategoria))
                print(f"  {numero}) {subcategoria.get_nombre()} (actividades: {cantidad})")
        else:
            print("Esta categoría no tiene subcategorías.")

        propias = actual.get_actividades()
        if len(propias) > 0:
            print("Actividades de esta categoría:")
            for actividad in propias:
                print(f"  - {actividad}")

        opcion = input("Elegí un número para entrar, v para volver, 0 para salir: ").strip().lower()
        if opcion == "0":
            return
        elif opcion == "v":
            if len(camino) > 1:
                camino.pop()
                actual = camino[len(camino) - 1]
            else:
                print("Ya estás en la raíz.")
        elif opcion.isdigit() and 1 <= int(opcion) <= len(subcategorias):
            actual = subcategorias[int(opcion) - 1]
            camino.append(actual)
        else:
            print("Opción inválida.")


def submenu_categorias(arbol):
    print("\n-- Explorar categorías --")
    print(" a) Navegar por la jerarquía")
    print(" b) Ver el árbol completo")
    print(" c) Ver las categorías por niveles")
    print(" d) Buscar una categoría")
    opcion = input("Elegí una opción: ").strip().lower()

    if opcion == "a":
        explorar_jerarquia(arbol)
    elif opcion == "b":
        for categoria, nivel in arbol.preorder():
            cantidad = len(arbol.actividades_de(categoria))
            print("    " * nivel + categoria.get_nombre() + " (" + str(cantidad) + ")")
    elif opcion == "c":
        nivel_anterior = -1
        for categoria, nivel in arbol.por_niveles():
            if nivel != nivel_anterior:
                print("Nivel " + str(nivel) + ":")
                nivel_anterior = nivel
            print("    " + categoria.get_nombre())
    elif opcion == "d":
        nombre = input("Nombre de la categoría: ").strip()
        categoria = arbol.buscar(nombre)
        if categoria is None:
            print("No existe esa categoría.")
        else:
            print("Ruta: " + " > ".join(arbol.ruta_hasta(nombre)))
            print("Categorías revisadas para encontrarla: " + str(arbol.pasos))
            mostrar_resultados(arbol.actividades_de(categoria))
    else:
        print("Opción inválida.")


def elegir_actividad(repo):
    texto = input("¿Qué actividad?: ").strip()
    encontradas = repo.buscar(texto)
    if len(encontradas) == 0:
        print("No se encontró esa actividad.")
        return None
    if len(encontradas) == 1:
        return encontradas[0]
    for numero, actividad in enumerate(encontradas, start=1):
        print(f"  {numero}) {actividad.get_nombre()}")
    eleccion = input("¿Cuál?: ").strip()
    if eleccion.isdigit() and 1 <= int(eleccion) <= len(encontradas):
        return encontradas[int(eleccion) - 1]
    print("Opción inválida.")
    return None


def submenu_red(grafo, repo):
    print("\n-- Actividades relacionadas --")
    print(" a) Ver las relacionadas con una actividad")
    print(" b) Ver toda la red")
    print(" c) Ver datos de la red")
    print(" d) Camino con menos pasos hacia una categoría")
    print(" e) Explorar en profundidad desde una actividad")
    opcion = input("Elegí una opción: ").strip().lower()

    if opcion == "a":
        actividad = elegir_actividad(repo)
        if actividad is None:
            return
        nombre = actividad.get_nombre()
        vecinos = grafo.vecinos_de(nombre)
        print(f"\n{nombre} ({actividad.get_duracion_estimada()} min) está relacionada con {len(vecinos)} actividades:")
        numero = 1
        for arista in vecinos:
            otra = grafo.get_actividad(arista.destino)
            print(f"  {numero}. {otra.get_nombre():<32} {otra.get_duracion_estimada():>3} min   distancia {arista.peso}")
            numero += 1
    elif opcion == "b":
        for nombre in grafo.nombres():
            destinos = []
            for arista in grafo.vecinos_de(nombre):
                destinos.append(f"{arista.destino} ({arista.peso})")
            print(nombre + " -> " + ", ".join(destinos))
    elif opcion == "c":
        print("Actividades en la red: " + str(grafo.cantidad_vertices()))
        print("Relaciones: " + str(grafo.cantidad_aristas))
        print("Densidad: " + f"{grafo.densidad():.2f}")
        mas = grafo.mas_conectada()
        if mas is not None:
            print(f"La más conectada: {mas} ({grafo.grado_de(mas)} relaciones)")
        if grafo.esta_conectado():
            print("Todas las actividades están conectadas entre sí.")
        else:
            print("Hay actividades que quedaron separadas del resto.")
    elif opcion == "d":
        actividad = elegir_actividad(repo)
        if actividad is None:
            return
        categoria = input("¿A qué categoría querés llegar?: ").strip()
        camino = grafo.mas_cercana_de_categoria(actividad.get_nombre(), categoria)
        if len(camino) == 0:
            print("No hay una actividad de esa categoría para llegar desde ahí.")
        else:
            print(f"\nCamino con menos pasos ({len(camino) - 1}):")
            minutos = 0
            numero = 1
            for nombre in camino:
                otra = grafo.get_actividad(nombre)
                print(f"  {numero}. {nombre} ({otra.get_duracion_estimada()} min)")
                minutos += otra.get_duracion_estimada()
                numero += 1
            print(f"Total si hacés todas: {minutos} min")
    elif opcion == "e":
        actividad = elegir_actividad(repo)
        if actividad is None:
            return
        recorrido = grafo.dfs(actividad.get_nombre())
        print(f"\nExploración en profundidad desde {actividad.get_nombre()}:")
        minutos = 0
        profundidad_maxima = 0
        for nombre in recorrido.orden:
            otra = grafo.get_actividad(nombre)
            profundidad = recorrido.distancia[nombre]
            print("  " * profundidad + f"{nombre} ({otra.get_duracion_estimada()} min)")
            minutos += otra.get_duracion_estimada()
            if profundidad > profundidad_maxima:
                profundidad_maxima = profundidad
        print(f"Actividades alcanzadas: {len(recorrido.orden)}   Profundidad máxima: {profundidad_maxima}   Total: {minutos} min")
    else:
        print("Opción inválida.")


def que_hago_ahora(recomendador, usuario, gestor, aceptadas):
    impulso = input('¿Qué estás por hacer?: ').strip()
    minutos = pedir_entero_positivo("¿Cuántos minutos tenés?: ")
    if minutos is None:
        return

    ranking = recomendador.top_n(minutos, CANTIDAD_EN_RANKING, aceptadas)
    alternativa = None

    if len(ranking) > 0:
        print(f"\nTOP {len(ranking)} PARA {minutos} MINUTOS")
        puesto = 1
        for elemento in ranking:
            actividad = elemento.actividad
            print(f"{puesto}. {actividad.get_nombre():<32} {elemento.prioridad:.1f}  ({actividad.get_duracion_estimada()} min)")
            puesto += 1
        eleccion = input("¿Cuál elegís? (0 si ninguna): ").strip()
        if eleccion.isdigit() and 1 <= int(eleccion) <= len(ranking):
            alternativa = ranking[int(eleccion) - 1].actividad
    else:
        print(f"No tengo ninguna actividad que entre en {minutos} min. "
              "Probá con un poco más de tiempo.")

    sesion = SesionUso(app_o_impulso=impulso, actividad_alternativa=alternativa)
    usuario.registrar_sesion(sesion)
    gestor.guardar_sesion(sesion)

    if alternativa:
        usuario.actualizar_racha()
        aceptadas.append(alternativa.get_nombre())
        print(f"Racha actual de {usuario.get_nombre()}: {usuario.get_racha()}.")
    else:
        print("Sesión registrada.")


def main():
    gestor = GestorDatos(carpeta_datos=CARPETA_DATOS)
    repo = RepositorioActividades()

    try:
        repo.cargar(gestor.cargar_actividades())
    except FileNotFoundError:
        print("No se encontró el archivo de actividades. Iniciando sin datos.")

    try:
        raiz = gestor.cargar_categorias()
    except FileNotFoundError:
        print("No se encontró el archivo de categorías. Se usa una sola categoría.")
        raiz = Categoria("Actividades")
    recomendador = Recomendador(repo)
    aceptadas = gestor.cargar_aceptadas()
    arbol = ArbolCategorias(raiz)
    sin_categoria = arbol.cargar_actividades(repo.listar())
    if len(sin_categoria) > 0:
        print(f"Aviso: {len(sin_categoria)} actividades no tienen una categoría válida.")

    try:
        puentes = gestor.cargar_puentes()
    except FileNotFoundError:
        print("No se encontró el archivo de relaciones. La red usa solo las categorías.")
        puentes = []
    grafo = armar_grafo(repo.listar(), arbol, puentes)
    if grafo.puentes_rechazados > 0:
        print(f"Aviso: {grafo.puentes_rechazados} relaciones no se pudieron cargar.")

    try:
        usuarios = gestor.cargar_usuarios()
        usuario = usuarios[0] if usuarios else None
    except FileNotFoundError:
        usuario = None

    if usuario is None:
        print("No hay usuarios cargados. Creando usuario de prueba.")
        usuario = Usuario(nombre="Invitado", edad=0)

    print(f"Bienvenido/a a Pause, {usuario.get_nombre()}.")

    while True:
        mostrar_menu()
        opcion = input("Elegí una opción: ").strip()

        if opcion == "1":
            print("Registro de tiempo en pantalla: no disponible en esta versión por falta de tiempo.")
        elif opcion == "2":
            submenu_actividades(repo, arbol)
        elif opcion == "3":
            que_hago_ahora(recomendador, usuario, gestor, aceptadas)
        elif opcion == "4":
            print("Desafíos pendientes: no disponible en esta versión por falta de tiempo.")
        elif opcion == "5":
            print("Modo minimalista: no disponible en esta versión por falta de tiempo.")
        elif opcion == "6":
            print(f"Sesiones registradas: {len(usuario.get_historial_sesiones())}")
        elif opcion == "7":
            submenu_categorias(arbol)
        elif opcion == "8":
            submenu_red(grafo, repo)
        elif opcion == "0":
            print("¡Adios!")
            break
        else:
            print("Opción inválida, probá de nuevo.")


if __name__ == "__main__":
    main()
