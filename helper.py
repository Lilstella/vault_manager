"""
Helper functions for all vault_manager commands.
"""
from __future__ import annotations
import re
from datetime import date
from pathlib import Path

from yaml import safe_load, YAMLError

from config import get_config

FRONTMATTER_RE = re.compile(r"\A---[ \t]*\n(.*?)^---[ \t]*(?:\n|\Z)", re.DOTALL | re.MULTILINE)

def ignored(path: Path) -> bool:
    """
    Return True if `path` is inside any ignored folder (see config.Config.is_ignored).
    """
    return get_config().is_ignored(path)


def list_notes(include_ignored: bool = False) -> list[Path]:
    """
    Returns a sorted list of all notes in the vault, optionally including ignored notes.
    """
    vault = get_config().vault
    return sorted(note for note in vault.rglob("*.md") if include_ignored or not ignored(note))


def read_note(root: Path) -> str:
    """
    Read a note as text (¡encoding utf-8!).
    """
    with open(root, "r", encoding="utf-8") as f:
        return f.read()


def write_note(root: Path, text: str) -> None:
    """
    Write `text` to `root` (utf-8). Create intermediate folders if missing.
    """
    root.parent.mkdir(parents=True, exist_ok=True)
    with open(root, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def separate_frontmatter(text: str) -> tuple[dict, str]:
    """
    Separate the YAML frontmatter from the body of the note.

    Return (properties, body). If the note has no frontmatter -> ({}, text).
    Cases to consider:
        - the text starts with '---' on the first line
        - the frontmatter ends at the next line that is exactly '---'
        - empty or invalid YAML should not break the script (return {})
    Hint: yaml.safe_load(). Note: YAML automatically converts 2025-05-11 to
    datetime.date and `true` to bool.
    """
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    try:
        props = safe_load(match.group(1)) or {}
    except YAMLError:
        return {}, text
    if not isinstance(props, dict):
        return {}, text
    return props, text[match.end():]

def iso_date() -> str:
    """
    Today's date as 'YYYY-MM-DD'.
    """
    return date.today().isoformat()
