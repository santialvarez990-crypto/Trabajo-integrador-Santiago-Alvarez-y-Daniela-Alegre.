import os

from gestor_datos import GestorDatos
from repositorio import RepositorioActividades
from modelos import SesionUso, Usuario

CARPETA_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos")


def mostrar_menu():
    print("\n==================== PAUSE ====================")
    print(" 1) Ver tiempo en pantalla")
    print(" 2) Ver mis actividades")
    print(" 3) ¿Qué hago ahora?")
    print(" 4) Ver desafíos pendientes")
    print(" 5) Activar/Desactivar modo minimalista")
    print(" 6) Estadísticas de la semana")
    print(" 0) Salir")
    print("=================================================")


def pedir_entero_positivo(mensaje):
    try:
        valor = int(input(mensaje).strip())
    except ValueError:
        print("Ingresá un número válido.")
        return None
    if valor <= 0:
        print("Ingresá un número mayor a cero.")
        return None
    return valor


def mostrar_resultados(resultados):
    if not resultados:
        print("No hay actividades")
        return
    for i, a in enumerate(resultados, start=1):
        print(f"  {i}. {a}")


def submenu_actividades(repo):
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
        categoria = input("Categoría: ").strip()
        mostrar_resultados(repo.filtrar(categoria=categoria))
    elif opcion == "d":
        minutos = pedir_entero_positivo("¿Cuántos minutos tenés?: ")
        if minutos is not None:
            mostrar_resultados(repo.filtrar(duracion_maxima=minutos))
    elif opcion == "e":
        mostrar_resultados(repo.listar_por_duracion())
    else:
        print("Opción inválida.")


def que_hago_ahora(repo, usuario, gestor):
    impulso = input('¿Qué estás por hacer?: ').strip()
    minutos = pedir_entero_positivo("¿Cuántos minutos tenés?: ")
    if minutos is None:
        return

    sugerida = repo.sugerir_para_tiempo(minutos)
    alternativa = None

    if sugerida:
        print(f'Pause sugiere: "¿Y si hacés esto? -> {sugerida.get_nombre()} '
              f'({sugerida.get_duracion_estimada()} min)"')
        acepta = input("¿Aceptás?: ").strip().lower()
        if acepta == "s":
            alternativa = sugerida
    else:
        print(f"No tengo ninguna actividad que entre en {minutos} min. "
              "Probá con un poco más de tiempo.")

    sesion = SesionUso(app_o_impulso=impulso, actividad_alternativa=alternativa)
    usuario.registrar_sesion(sesion)
    gestor.guardar_sesion(sesion)

    if alternativa:
        usuario.actualizar_racha()
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
        usuarios = gestor.cargar_usuarios()
        usuario = usuarios[0] if usuarios else None
    except FileNotFoundError:
        usuario = None

    if usuario is None:
        print("No hay usuarios cargados. Iniciando como usuario de prueba.")
        usuario = Usuario(nombre="Invitado", edad=0)

    print(f"Bienvenido a Pause, {usuario.get_nombre()}.")

    while True:
        mostrar_menu()
        opcion = input("Elegí una opción: ").strip()

        if opcion == "1":
            print("Registro de tiempo en pantalla: ")
        elif opcion == "2":
            submenu_actividades(repo)
        elif opcion == "3":
            que_hago_ahora(repo, usuario, gestor)
        elif opcion == "4":
            print("Desafíos pendientes: ")
        elif opcion == "5":
            print("Modo minimalista: ")
        elif opcion == "6":
            print(f"Sesiones registradas: {len(usuario.get_historial_sesiones())}")
        elif opcion == "0":
            print("¡Adios!")
            break
        else:
            print("Opción inválida, probá de nuevo.")


if __name__ == "__main__":
    main()
