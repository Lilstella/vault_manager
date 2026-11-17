"""Limpia texto copiado de un PDF (palabras cortadas, saltos de línea en medio de frases).

Uso:
    python limpiar_pdf.py nota.md --simular
    python limpiar_pdf.py nota.md            # sobreescribe (¡hace copia .bak!)
    pegar texto | python limpiar_pdf.py -    # lee de stdin y escribe a stdout
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def unir_palabras_cortadas(texto: str) -> str:
    """'demon-\\nstration' -> 'demonstration'.

    Cuidado: no rompas guiones legítimos ('bien-estar' en medio de una línea).
    Solo unís cuando el guion está al FINAL de la línea y sigue una minúscula.
    Pista: re.sub(r"(\\w)-\\n(\\w)", ...) y evaluá el caso de la mayúscula.
    """
    raise NotImplementedError("TODO: unir_palabras_cortadas")


def unir_lineas_de_parrafo(texto: str) -> str:
    """Une líneas partidas dentro de un mismo párrafo, respetando párrafos reales.

    - Una línea en blanco separa párrafos: se conserva.
    - Un salto simple en medio de una oración se convierte en un espacio.
    - No toques listas ('- ', '1. '), encabezados ('# ') ni bloques de código (```).
    Pista: re.sub(r"(?<!\\n)\\n(?!\\n)", " ", texto) es un buen punto de partida,
    pero fallará con las listas: pensá cómo protegerlas.
    """
    raise NotImplementedError("TODO: unir_lineas_de_parrafo")


def normalizar_espacios(texto: str) -> str:
    """Colapsa espacios múltiples y quita espacios al final de cada línea."""
    raise NotImplementedError("TODO: normalizar_espacios")


def limpiar(texto: str) -> str:
    """Aplica todas las limpiezas en un orden sensato.

    ¿Importa el orden? Probá: ¿qué pasa si unís líneas antes que palabras cortadas?
    """
    raise NotImplementedError("TODO: limpiar")


def limpiar_archivo(ruta: Path, simular: bool = False) -> None:
    """Lee el archivo, limpia, y (si no es simulación) guarda una copia .bak y sobreescribe.

    Con simular=True imprimí un 'antes/después' corto en vez de escribir.
    """
    raise NotImplementedError("TODO: limpiar_archivo")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archivo", help="ruta a la nota, o '-' para stdin")
    parser.add_argument("--simular", action="store_true")
    args = parser.parse_args(argv)
    if args.archivo == "-":
        sys.stdout.write(limpiar(sys.stdin.read()))
    else:
        limpiar_archivo(Path(args.archivo), simular=args.simular)


if __name__ == "__main__":
    main()
