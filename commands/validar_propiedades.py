"""Valida las propiedades (frontmatter) de tareas y exámenes.

Es lo que rompía las tablas de Dataview: fechas mal escritas, completado como texto, etc.

Uso:
    python validar_propiedades.py
"""
from __future__ import annotations

import argparse
from pathlib import Path

import helper
from config import get_config

PRIORIDADES_VALIDAS = {"alta", "media", "baja"}
TIPOS_EXAMEN_VALIDOS = {"parcial", "final", "recuperatorio"}


def fecha_valida_iso(valor) -> bool:
    """True si `valor` es una fecha AAAA-MM-DD válida.

    Ojo: yaml.safe_load ya convierte 2025-05-11 en datetime.date, pero deja
    '11/05/2025' como str. Tenés que aceptar date/datetime y str con formato ISO,
    y rechazar todo lo demás (None, int, '2025-13-40', '11/05/2025').
    Pista: datetime.strptime(valor, "%Y-%m-%d") dentro de un try/except ValueError.
    """
    raise NotImplementedError("TODO: fecha_valida_iso")


def validar_tarea(props: dict) -> list[str]:
    """Lista de problemas encontrados en las propiedades de una tarea.

    Reglas:
      - `asignatura` presente y no vacía (las personales pueden estar vacías: decidí vos)
      - `fecha-entrega` presente y fecha ISO válida
      - `prioridad` dentro de PRIORIDADES_VALIDAS
      - `completado` es un bool real (no el texto "true")
    Devolvé mensajes legibles, p. ej. "fecha-entrega inválida: '11/05/2025'".
    Lista vacía = todo OK.
    """
    raise NotImplementedError("TODO: validar_tarea")


def validar_examen(props: dict) -> list[str]:
    """Reglas: `asignatura`, `fecha` ISO válida, `tipo` en TIPOS_EXAMEN_VALIDOS."""
    raise NotImplementedError("TODO: validar_examen")


def tipo_de_nota(props: dict) -> str | None:
    """Devuelve 'tarea', 'examen' o None según los tags de la nota.

    Los tags están en props['tags'] y pueden ser str o list. Buscá
    'universidad/tarea' y 'universidad/examen'.
    """
    raise NotImplementedError("TODO: tipo_de_nota")


def validar_todo() -> dict[Path, list[str]]:
    """Recorre el vault y devuelve {nota: [problemas]} solo de las notas con problemas."""
    raise NotImplementedError("TODO: validar_todo")


def main(argv: list[str] | None = None) -> int:
    argparse.ArgumentParser(description=__doc__).parse_args(argv)
    # TODO: imprimí los problemas agrupados por nota; devolvé 1 si hubo alguno, 0 si no.
    raise NotImplementedError("TODO: main")


if __name__ == "__main__":
    raise SystemExit(main())
