def buscar_secuencial(sesiones, fecha_objetivo):
    resultado = []
    for sesion in sesiones:
        if sesion.fecha == fecha_objetivo:
            resultado.append(sesion)
    return resultado
