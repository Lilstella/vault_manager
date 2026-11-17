"""Comprime el vault en un .zip con fecha.

Uso:
    python backup.py                     # crea ../../backups/cerebro_2026-10-24.zip
    python backup.py --destino D:/Backups --conservar 5
"""
from __future__ import annotations

import argparse
from pathlib import Path

import helper
from config import get_config

# Rutas (relativas al vault) que no vale la pena respaldar.
EXCLUIR = {".obsidian/plugins", ".obsidian/themes", "__pycache__", ".git"}


def debe_excluirse(ruta: Path) -> bool:
    """True si la ruta (absoluta, dentro del vault) cae en EXCLUIR.

    Pista: pasá la ruta a relativa con relative_to(get_config().vault) y comparalo
    con cada elemento de EXCLUIR usando as_posix() y startswith / partes.
    """
    raise NotImplementedError("TODO: debe_excluirse")


def nombre_backup(hoy: str) -> str:
    """'cerebro_AAAA-MM-DD.zip'."""
    raise NotImplementedError("TODO: nombre_backup")


def crear_backup(destino_dir: Path, simular: bool = False) -> Path:
    """Crea el zip con todos los archivos no excluidos.

    Pista: zipfile.ZipFile(ruta, "w", zipfile.ZIP_DEFLATED) y zf.write(archivo, arcname=...).
    El arcname debe ser relativo al vault para que al descomprimir quede ordenado.
    """
    raise NotImplementedError("TODO: crear_backup")


def rotar_backups(destino_dir: Path, conservar: int = 5, simular: bool = False) -> list[Path]:
    """Borra los backups más viejos y deja solo los últimos `conservar`.

    Devuelve la lista de archivos borrados. Ordená por nombre (la fecha ISO ordena sola).
    """
    raise NotImplementedError("TODO: rotar_backups")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destino", type=Path, default=None, help="carpeta de destino (por defecto: <vault>/../backups)")
    parser.add_argument("--conservar", type=int, default=5)
    parser.add_argument("--simular", action="store_true")
    args = parser.parse_args(argv)
    crear_backup(args.destino, simular=args.simular)
    rotar_backups(args.destino, args.conservar, simular=args.simular)


if __name__ == "__main__":
    main()
