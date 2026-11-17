"""Detecta enlaces rotos, notas huérfanas y notas olvidadas en el Inbox.

Uso:
    python validar_vault.py
    python validar_vault.py --dias-inbox 3
"""
from __future__ import annotations

import argparse
from pathlib import Path

import helper
from config import get_config


def extraer_enlaces(texto: str) -> set[str]:
    """Nombres de nota enlazados con [[...]] en el texto.

    Hay que quedarse solo con el nombre:
      [[Nota]]            -> "Nota"
      [[Nota|alias]]      -> "Nota"
      [[Nota#Sección]]    -> "Nota"
      [[Nota#^bloque]]    -> "Nota"
    Pista: regex r"\\[\\[([^\\]|#]+)" y .strip().
    Desafío: ignorá los enlaces que están dentro de bloques de código.
    """
    raise NotImplementedError("TODO: extraer_enlaces")


def nombres_de_notas() -> set[str]:
    """Nombres (sin .md) de todas las notas del vault. Pista: Path.stem."""
    raise NotImplementedError("TODO: nombres_de_notas")


def encontrar_enlaces_rotos() -> dict[Path, set[str]]:
    """{nota: {enlaces que no apuntan a ninguna nota existente}}.

    Solo incluí las notas que tengan al menos un enlace roto.
    """
    raise NotImplementedError("TODO: encontrar_enlaces_rotos")


def encontrar_huerfanas() -> list[Path]:
    """Notas que NINGUNA otra nota enlaza y que tampoco enlazan a nadie.

    Pista: armá primero un conjunto con todos los nombres enlazados en el vault.
    Los hubs (Dashboard, Mapa Universitario...) probablemente querrás excluirlos.
    """
    raise NotImplementedError("TODO: encontrar_huerfanas")


def inbox_estancado(dias: int = 7) -> list[tuple[Path, int]]:
    """Notas del Inbox con más de `dias` días sin tocarse: [(ruta, antigüedad_en_días)].

    Ordená de la más vieja a la más nueva.
    """
    raise NotImplementedError("TODO: inbox_estancado")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dias-inbox", type=int, default=7)
    args = parser.parse_args(argv)
    # TODO: imprimí un reporte con las tres secciones.
    # Devolvé 1 si hay problemas y 0 si todo está bien (sirve para automatizarlo).
    raise NotImplementedError("TODO: main")


if __name__ == "__main__":
    raise SystemExit(main())
