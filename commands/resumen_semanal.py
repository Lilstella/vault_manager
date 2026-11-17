"""Genera una nota con el resumen de la semana en 00 - Inbox.

Uso:
    python resumen_semanal.py
    python resumen_semanal.py --dias 14
"""
from __future__ import annotations

import argparse
from pathlib import Path

import helper
from config import get_config


def checkboxes_hechos(texto: str) -> list[str]:
    """Textos de los '- [x] algo' del cuerpo de una nota (sin el '- [x] ').

    Aceptá '[x]' y '[X]'. Ignorá los '- [ ]' (pendientes).
    Pista: regex r"^\\s*- \\[[xX]\\]\\s+(.+)$" con re.MULTILINE.
    """
    raise NotImplementedError("TODO: checkboxes_hechos")


def checkboxes_pendientes(texto: str) -> list[str]:
    """Igual que el anterior pero para '- [ ] algo'."""
    raise NotImplementedError("TODO: checkboxes_pendientes")


def tareas_completadas(dias: int = 7) -> list[Path]:
    """Notas de tareas con `completado: true` modificadas en los últimos `dias`."""
    raise NotImplementedError("TODO: tareas_completadas")


def notas_creadas(dias: int = 7) -> list[Path]:
    """Notas creadas en los últimos `dias`.

    Pista: st_ctime es la fecha de creación en Windows, pero en Linux/Mac no es
    confiable. Si te interesa lo multiplataforma, pensá en alternativas
    (st_birthtime en macOS, o guardar `fecha:` en el frontmatter).
    """
    raise NotImplementedError("TODO: notas_creadas")


def tareas_pendientes() -> list[tuple[Path, str]]:
    """[(nota, fecha-entrega)] de tareas con completado: false, por fecha ascendente."""
    raise NotImplementedError("TODO: tareas_pendientes")


def generar_markdown(dias: int) -> str:
    """Arma el texto de la nota resumen (con frontmatter, secciones y enlaces [[...]])."""
    raise NotImplementedError("TODO: generar_markdown")


def guardar_resumen(dias: int, simular: bool = False) -> Path:
    """Escribe 'Resumen AAAA-MM-DD.md' en get_config().inbox_dir."""
    raise NotImplementedError("TODO: guardar_resumen")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dias", type=int, default=7)
    parser.add_argument("--simular", action="store_true")
    args = parser.parse_args(argv)
    guardar_resumen(args.dias, simular=args.simular)


if __name__ == "__main__":
    main()
