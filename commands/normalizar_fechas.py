"""Convierte fechas como 11/05/2025 a formato ISO (2025-05-11) en las notas.

Por seguridad corre en modo simulación a menos que pases --aplicar.

Uso:
    python normalizar_fechas.py                  # solo muestra qué cambiaría
    python normalizar_fechas.py --aplicar        # modifica (con copia de seguridad)
    python normalizar_fechas.py --mdy            # interpreta 11/05 como mes/día
"""
from __future__ import annotations

import argparse
from pathlib import Path

import helper
from config import get_config


def convertir_fecha(texto: str, dayfirst: bool = True) -> str | None:
    """Convierte 'DD/MM/AAAA' (o 'DD-MM-AAAA', 'D/M/AAAA') a 'AAAA-MM-DD'.

    - Con dayfirst=False interpreta 'MM/DD/AAAA'.
    - Devuelve None si no es una fecha válida (p. ej. '31/02/2025').
    - Si ya está en ISO, devolvela igual.
    Pista: datetime.strptime en un try/except, probando varios formatos.
    """
    raise NotImplementedError("TODO: convertir_fecha")


def encontrar_fechas(texto: str) -> list[str]:
    """Todos los candidatos a fecha no-ISO que aparecen en el texto.

    Pista: regex r"\\b\\d{1,2}[/-]\\d{1,2}[/-]\\d{4}\\b".
    Ojo: 2025-05-11 (ya ISO) no debería aparecer como candidato.
    """
    raise NotImplementedError("TODO: encontrar_fechas")


def normalizar_texto(texto: str, dayfirst: bool = True) -> tuple[str, int]:
    """Reemplaza todas las fechas convertibles. Devuelve (texto_nuevo, cantidad_cambios).

    Consejo: limitá el reemplazo al FRONTMATTER para no tocar fechas dentro del cuerpo
    (código, citas). Usá helper.separate_frontmatter o trabajá sobre el texto crudo
    entre los dos '---'.
    """
    raise NotImplementedError("TODO: normalizar_texto")


def procesar_nota(ruta: Path, aplicar: bool, dayfirst: bool) -> int:
    """Procesa una nota. Si aplicar=True, guarda 'ruta.bak' y reescribe. Devuelve cambios."""
    raise NotImplementedError("TODO: procesar_nota")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--aplicar", action="store_true")
    parser.add_argument("--mdy", action="store_true", help="interpretar mes/día")
    args = parser.parse_args(argv)
    # TODO: recorrer helper.list_notes(), llamar procesar_nota y mostrar un resumen.
    raise NotImplementedError("TODO: main")


if __name__ == "__main__":
    main()
