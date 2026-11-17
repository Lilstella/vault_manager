"""Vigila 00 - Inbox y mueve las notas nuevas según sus tags.

Requiere: pip install watchdog
Uso:
    python vigilante.py            # queda corriendo; Ctrl+C para salir
    python vigilante.py --simular  # solo avisa, no mueve nada
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

import helper
from config import get_config

# tag -> carpeta destino (relativa al vault)
REGLAS_TAGS: dict[str, str] = {
    "universidad/apunte": "01 - Universidad/Apuntes",
    "universidad/tarea": "01 - Universidad/Tareas",
    "universidad/examen": "01 - Universidad/Examenes",
    "conocimiento/lectura": "03 - Conocimiento/Lecturas",
    # TODO: agregá más reglas
}


def destino_segun_tags(tags: set[str]) -> Path | None:
    """Carpeta destino para una nota con esos tags, o None si ninguna regla aplica.

    ¿Qué hacés si una nota matchea dos reglas? Decidí (la primera, un aviso, ...).
    """
    raise NotImplementedError("TODO: destino_segun_tags")


def mover_nota(ruta: Path, simular: bool = False) -> Path | None:
    """Lee la nota, decide el destino y la mueve. Devuelve la nueva ruta o None.

    Pista: usá estadisticas.extraer_tags y shutil.move.
    Cuidado con colisiones: si ya existe una nota con ese nombre en el destino.
    """
    raise NotImplementedError("TODO: mover_nota")


class ManejadorInbox(FileSystemEventHandler):
    """Reacciona a archivos nuevos en el Inbox."""

    def __init__(self, simular: bool = False) -> None:
        super().__init__()
        self.simular = simular

    def on_created(self, event: FileSystemEvent) -> None:
        """Se llama cuando aparece un archivo/carpeta.

        - Ignorá directorios y archivos que no sean .md.
        - Esperá un momento (time.sleep) a que Obsidian termine de escribir el archivo.
        - Una nota recién creada suele estar vacía y sin tags: pensá cuándo conviene
          moverla (¿en on_modified? ¿al cerrarla?). Este es el problema interesante.
        """
        raise NotImplementedError("TODO: on_created")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--simular", action="store_true")
    args = parser.parse_args(argv)

    observador = Observer()
    observador.schedule(ManejadorInbox(args.simular), str(get_config().inbox_dir), recursive=False)
    observador.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observador.stop()
    observador.join()


if __name__ == "__main__":
    main()
