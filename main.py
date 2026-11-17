"""vault_manager: command-line tools for your Obsidian vault.

Usage:
    python main.py [--vault PATH] <command> [command options]

Commands:
    new        create a note from a template        (main.py new tarea "TP Final")
    validate   check links and properties
    backup     zip the vault
    stats      vault statistics
    summary    generate the weekly summary
    clean      clean text copied from a PDF
    dates      normalize dates to ISO
    watch      watch the Inbox and move notes
    config     show the active settings and check them

Each command has its own help:  python main.py new --help
"""
from __future__ import annotations

import argparse
import sys
from importlib import import_module
from pathlib import Path

from config import get_config, load_config, set_config, validate

# command -> (module with a main(argv) function, help text).
# When you rename or finish a module, this is the only place to update.
COMMANDS: dict[str, tuple[str, str]] = {
    "new": ("commands.create_note", "create a note from a template"),
    "validate": ("commands.validar_vault", "check links and properties"),
    "backup": ("commands.backup", "zip the vault"),
    "stats": ("commands.estadisticas", "vault statistics"),
    "summary": ("commands.resumen_semanal", "generate the weekly summary"),
    "clean": ("commands.limpiar_pdf", "clean text copied from a PDF"),
    "dates": ("commands.normalizar_fechas", "normalize dates to ISO"),
    "watch": ("commands.vigilante", "watch the Inbox and move notes"),
}


def show_config() -> int:
    """`config` command: print the active settings and any problems."""
    cfg = get_config()
    print(f"Vault:      {cfg.vault}")
    print(f"Inbox:      {cfg.inbox}")
    print(f"Templates:  {cfg.templates}")
    print(f"Archive:    {cfg.archive}")
    ignored = [p.relative_to(cfg.vault) if p.is_relative_to(cfg.vault) else p for p in cfg.ignored_dirs]
    print(f"Ignored:    {', '.join(str(p) for p in ignored)}")
    print("Types:")
    for name, note_type in sorted(cfg.types.items()):
        print(f"  {name:<12} {note_type.template}  ->  {note_type.folder}")
    problems = validate(cfg)
    if problems:
        print("\nProblems found:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print("\nEverything looks fine.")
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else list(argv)

    # Global options can appear anywhere; everything else goes to the command.
    global_parser = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    global_parser.add_argument("--vault", type=Path)
    known, remaining = global_parser.parse_known_args(argv)

    if not remaining or remaining[0] in ("-h", "--help"):
        print(__doc__)
        return 0

    command, rest = remaining[0], remaining[1:]
    if command != "config" and command not in COMMANDS:
        print(f"Unknown command: {command!r}. Valid commands: "
              f"{', '.join([*COMMANDS, 'config'])}", file=sys.stderr)
        return 2

    try:
        set_config(load_config(known.vault))
    except (FileNotFoundError, ValueError) as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        return 2

    if command == "config":
        return show_config()

    module = import_module(COMMANDS[command][0])
    return module.main(rest) or 0


if __name__ == "__main__":
    sys.exit(main())
