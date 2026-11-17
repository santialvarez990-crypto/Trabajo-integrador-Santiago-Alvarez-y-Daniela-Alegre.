# Pause

Aplicación de terminal que ayuda a regular el uso del celular, sugiriendo
actividades alternativas ante impulsos de abrir apps de scroll infinito.

Trabajo integrador — Estructura de Datos.

## Requisitos

- Python 3.8 o superior (no requiere librerías externas).

## Cómo ejecutar

```bash
cd pause
python3 main.py
```

## Estructura del proyecto

```
pause/
├── main.py            # Interfaz de terminal (entrada/salida)
├── modelos.py          # Clases del dominio: Usuario, Actividad, Desafio, SesionUso, Categoria
├── repositorio.py       # Operaciones Buscar, Listar, Filtrar sobre las actividades
├── gestor_datos.py      # Carga/guardado de datos en JSON
├── datos/
│   ├── actividades.json # Actividades de prueba
│   ├── usuarios.json    # Usuario de prueba
│   └── sesiones.json    # Se genera automáticamente al usar la app (historial de sesiones)
└── README.md
```

## Funcionalidades de esta v1 (TP1)

- Carga de actividades y usuario desde archivos JSON.
- **Buscar** actividades por nombre (coincidencia parcial).
- **Listar** todas las actividades disponibles.
- **Filtrar** actividades por categoría y/o por duración máxima disponible.
- Flujo de "¿Qué hago ahora?": registra el impulso del usuario, sugiere una
  actividad alternativa y guarda la sesión en `datos/sesiones.json`.

Las opciones de "registro de tiempo en pantalla", "desafíos pendientes" y
"modo minimalista" aparecen en el menú, pero todavía no están implementadas
en esta versión.

## Demo rápida

```
$ python3 main.py
Bienvenido/a a Pause, Franco.

==================== PAUSE ====================
 1) Ver registro de tiempo en pantalla
 2) Ver mis actividades (buscar / categorías)
 3) ¿Qué hago ahora? (Desafíos nuevos)
 4) Ver desafíos pendientes
 5) Activar/Desactivar modo minimalista
 6) Estadísticas de la semana
 0) Salir
=================================================
Elegí una opción: 3
¿Qué estás por hacer? (ej: "abrir TikTok"): abrir TikTok
Pause sugiere: "¿Y si hacés esto? -> Estiramientos (5 min)"
¿Aceptás la sugerencia? (s/n): s
¡Listo! Racha actual de Franco: 1 días.
```
