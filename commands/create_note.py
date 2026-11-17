"""
Create a new note from a vault template.

Usage:
    python main.py new tarea "TP Final"
    python main.py new apunte "Punteros en C" --simulate

(The valid types are the ones defined in vault_manager.toml.)
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

from config import get_config
from helper import read_note, write_note

# {{title}}, {{date}}, {{time}} and {{date:FORMAT}}
TEMPLATE_RE = re.compile(r"\{\{\s*(title|date|time)(?::([^}]*?))?\s*\}\}")

# Characters that break file names (Windows) or wikilinks (Obsidian: # ^ [ ])
INVALID_FILENAME_CHARS = re.compile(r'[/\\:*?"<>|#^\[\]]')

# Moment.js token -> strftime directive (longest tokens first in the regex)
MOMENT_TO_STRFTIME = {
    "YYYY": "%Y", "YY": "%y",
    "MMMM": "%B", "MMM": "%b", "MM": "%m",
    "DD": "%d",
    "HH": "%H", "mm": "%M", "ss": "%S",
}
MOMENT_TOKENS = re.compile("|".join(MOMENT_TO_STRFTIME))


def _get_type(note_type: str):
    """Return the NoteType from the config or raise a clear ValueError."""
    types = get_config().types
    if note_type not in types:
        raise ValueError(f"Unknown type: {note_type!r}. Valid types: {', '.join(sorted(types))}")
    return types[note_type]


def load_template(note_type: str) -> str:
    """Read and return the template text for `note_type`."""
    template_path = get_config().templates_dir / _get_type(note_type).template
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    return read_note(template_path)


def replace_variables(text: str, title: str, now: datetime | None = None) -> str:
    """Replace {{title}}, {{date}}, {{date:FORMAT}} and {{time}}."""
    now = now or datetime.now()

    def replacer(match: re.Match) -> str:
        key, fmt = match.group(1), match.group(2)
        if key == "title":
            return title
        if key == "date":
            if fmt:
                fmt = MOMENT_TOKENS.sub(lambda m: MOMENT_TO_STRFTIME[m.group()], fmt)
                return now.strftime(fmt)
            return now.strftime("%Y-%m-%d")
        return now.strftime("%H:%M")  # key == "time"

    return TEMPLATE_RE.sub(replacer, text)


def destination_path(note_type: str, title: str) -> Path:
    """Absolute path (inside the vault) where the note will be saved."""
    folder = get_config().vault / _get_type(note_type).folder
    safe_title = INVALID_FILENAME_CHARS.sub("_", title).strip()
    if not safe_title:
        raise ValueError("The title is empty after removing invalid characters.")
    path = folder / f"{safe_title}.md"
    if path.exists():
        raise FileExistsError(f"Note already exists: {path}")
    return path


def create_note(note_type: str, title: str, simulate: bool = False,
                now: datetime | None = None) -> tuple[Path, str]:
    """Template -> variables -> path -> write. Returns (path, text).

    With simulate=True nothing is written. No printing here: main() does the I/O.
    """
    text = replace_variables(load_template(note_type), title, now)
    path = destination_path(note_type, title)
    if not simulate:
        write_note(path, text)
    return path, text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="new", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("type", choices=sorted(get_config().types))
    parser.add_argument("title")
    parser.add_argument("--simulate", action="store_true")
    args = parser.parse_args(argv)

    try:
        path, text = create_note(args.type, args.title, simulate=args.simulate)
    except (ValueError, FileNotFoundError, FileExistsError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    if args.simulate:
        print(f"[simulate] would create: {path}\n\n{text}")
    else:
        print(f"Created: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
