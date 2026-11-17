from dataclasses import dataclass
from datetime import date


@dataclass
class Sesion:
    fecha: date
    impulso: str
