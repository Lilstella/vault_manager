"""Estadísticas rápidas del vault: notas por carpeta, tags, actividad reciente.

Uso:
    python estadisticas.py
    python estadisticas.py --dias 14 --top 10
"""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

import helper
from config import get_config


def contar_notas_por_carpeta() -> Counter:
    """Counter {carpeta_de_primer_nivel: cantidad_de_notas}.

    Las notas de la raíz del vault podés agruparlas bajo "(raíz)".
    """
    raise NotImplementedError("TODO: contar_notas_por_carpeta")


def extraer_tags(texto: str) -> set[str]:
    """Todos los tags de una nota: los del frontmatter (`tags:`) y los inline (#tag).

    Cuidado:
      - `tags` puede ser una lista, un string o no existir.
      - Los tags inline no deben confundirse con encabezados ('# Título') ni con
        código. Pista: regex r"(?<!\\S)#([\\w/-]+)".
      - Devolvé los tags SIN el '#'.
    """
    raise NotImplementedError("TODO: extraer_tags")


def tags_mas_usados(n: int = 10) -> list[tuple[str, int]]:
    """Los n tags más frecuentes. Pista: Counter.most_common(n)."""
    raise NotImplementedError("TODO: tags_mas_usados")


def notas_modificadas(dias: int = 7) -> list[Path]:
    """Notas modificadas en los últimos `dias`, más recientes primero.

    Pista: ruta.stat().st_mtime y time.time() (o datetime.fromtimestamp).
    """
    raise NotImplementedError("TODO: notas_modificadas")


def imprimir_reporte(dias: int, top: int) -> None:
    """Arma e imprime el reporte (formato libre, pero que se lea bien)."""
    raise NotImplementedError("TODO: imprimir_reporte")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dias", type=int, default=7)
    parser.add_argument("--top", type=int, default=10)
    args = parser.parse_args(argv)
    imprimir_reporte(args.dias, args.top)


if __name__ == "__main__":
    main()
