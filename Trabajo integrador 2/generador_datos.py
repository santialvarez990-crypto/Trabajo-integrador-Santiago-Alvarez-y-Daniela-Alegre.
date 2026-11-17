import random
from datetime import date, timedelta
from sesion import Sesion

IMPULSOS = ["abrir TikTok", "abrir Instagram", "abrir YouTube", "revisar notificaciones"]
DIA_BASE = date(2026, 1, 1)
RANGO_DIAS = 365


def generar_sesiones(n, semilla=None):
    rng = random.Random(semilla)
    sesiones = []
    for _ in range(n):
        offset = rng.randint(0, RANGO_DIAS - 1)
        fecha = DIA_BASE + timedelta(days=offset)
        impulso = rng.choice(IMPULSOS)
        sesiones.append(Sesion(fecha=fecha, impulso=impulso))
    return sesiones
