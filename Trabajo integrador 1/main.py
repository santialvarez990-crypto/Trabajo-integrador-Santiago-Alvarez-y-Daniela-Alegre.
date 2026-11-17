"""
main.py
Interfaz de terminal de Pause.
Solo maneja entrada/salida: la lógica vive en repositorio.py y gestor_datos.py.
"""

from gestor_datos import GestorDatos
from repositorio import RepositorioActividades
from modelos import SesionUso


def mostrar_menu():
    print("\n==================== PAUSE ====================")
    print(" 1) Ver registro de tiempo en pantalla")
    print(" 2) Ver mis actividades (buscar / categorías)")
    print(" 3) ¿Qué hago ahora? (Desafíos nuevos)")
    print(" 4) Ver desafíos pendientes")
    print(" 5) Activar/Desactivar modo minimalista")
    print(" 6) Estadísticas de la semana")
    print(" 0) Salir")
    print("=================================================")


def listar_actividades(repo):
    actividades = repo.listar()
    if not actividades:
        print("No hay actividades cargadas.")
        return
    for i, a in enumerate(actividades, start=1):
        print(f"  {i}. {a}")


def submenu_actividades(repo):
    print("\n-- Ver mis actividades --")
    print(" a) Listar todas")
    print(" b) Buscar por nombre")
    print(" c) Filtrar por categoría")
    print(" d) Filtrar por duración máxima")
    opcion = input("Elegí una opción: ").strip().lower()

    if opcion == "a":
        listar_actividades(repo)
    elif opcion == "b":
        texto = input("¿Qué buscás?: ").strip()
        resultados = repo.buscar(texto)
        mostrar_resultados(resultados)
    elif opcion == "c":
        categoria = input("Categoría (ej: Movimiento, Social, Hogar): ").strip()
        resultados = repo.filtrar(categoria=categoria)
        mostrar_resultados(resultados)
    elif opcion == "d":
        try:
            minutos = int(input("¿Cuántos minutos tenés disponibles?: ").strip())
        except ValueError:
            print("Ingresá un número válido.")
            return
        resultados = repo.filtrar(duracion_maxima=minutos)
        mostrar_resultados(resultados)
    else:
        print("Opción inválida.")


def mostrar_resultados(resultados):
    if not resultados:
        print("No se encontraron actividades.")
        return
    for a in resultados:
        print(f"  - {a}")


def que_hago_ahora(repo, usuario, gestor):
    impulso = input('¿Qué estás por hacer? (ej: "abrir TikTok"): ').strip()

    # v1 simple: sugiere la actividad de menor duración disponible como alternativa
    actividades = repo.listar()
    sugerida = min(actividades, key=lambda a: a.get_duracion_estimada()) if actividades else None

    if sugerida:
        print(f'Pause sugiere: "¿Y si hacés esto? -> {sugerida.get_nombre()} '
              f'({sugerida.get_duracion_estimada()} min)"')
        acepta = input("¿Aceptás la sugerencia? (s/n): ").strip().lower()
        alternativa = sugerida if acepta == "s" else None
    else:
        print("No hay actividades cargadas para sugerir.")
        alternativa = None

    sesion = SesionUso(app_o_impulso=impulso, actividad_alternativa=alternativa)
    usuario.registrar_sesion(sesion)
    gestor.guardar_sesion(sesion)

    if alternativa:
        usuario._racha += 1  # en v1 sumamos racha directo; en v2 se puede mover a un método dedicado
        print(f"¡Listo! Racha actual de {usuario.get_nombre()}: {usuario.get_racha()} días.")
    else:
        print("Sesión registrada.")


def main():
    gestor = GestorDatos(carpeta_datos="datos")
    repo = RepositorioActividades()

    try:
        actividades = gestor.cargar_actividades()
        repo.cargar(actividades)
    except FileNotFoundError:
        print("No se encontró el archivo de actividades. Iniciando sin datos.")

    try:
        usuarios = gestor.cargar_usuarios()
        usuario = usuarios[0] if usuarios else None
    except FileNotFoundError:
        usuario = None

    if usuario is None:
        print("No hay usuarios cargados. Creando usuario de prueba.")
        from modelos import Usuario
        usuario = Usuario(nombre="Invitado", edad=0)

    print(f"Bienvenido/a a Pause, {usuario.get_nombre()}.")

    while True:
        mostrar_menu()
        opcion = input("Elegí una opción: ").strip()

        if opcion == "1":
            print("Registro de tiempo en pantalla: (funcionalidad prevista para v2)")
        elif opcion == "2":
            submenu_actividades(repo)
        elif opcion == "3":
            que_hago_ahora(repo, usuario, gestor)
        elif opcion == "4":
            print("Desafíos pendientes: (funcionalidad prevista para v2, cuando se sume el heap)")
        elif opcion == "5":
            print("Modo minimalista: (funcionalidad prevista para v2)")
        elif opcion == "6":
            print(f"Sesiones registradas en esta ejecución: {len(usuario.get_historial_sesiones())}")
        elif opcion == "0":
            print("¡Hasta la próxima!")
            break
        else:
            print("Opción inválida, probá de nuevo.")


if __name__ == "__main__":
    main()
