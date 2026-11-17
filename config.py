"""Settings for vault_manager.

Where the vault is (first match wins):
    1. the `vault` argument (for example from the --vault flag)
    2. the VAULT_MANAGER_VAULT environment variable
    3. the nearest parent folder of the current directory that contains `.obsidian`

Everything else is read from `vault_manager.toml` in the vault root. Anything
missing falls back to the defaults below. Requires Python 3.11+ (tomllib).

Usage from the rest of the code:
    from config import get_config
    cfg = get_config()           # loaded once, on first use
    cfg.vault, cfg.inbox_dir, cfg.types["tarea"].folder, cfg.is_ignored(path)

Tests (or main.py with --vault) replace it with set_config(...).
"""
from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

CONFIG_FILENAME = "vault_manager.toml"
ENV_VAULT = "VAULT_MANAGER_VAULT"
PROJECT_DIR = Path(__file__).resolve().parent  # where this project lives


@dataclass(frozen=True)
class NoteType:
    template: str  # file name inside the templates folder
    folder: str    # destination folder, relative to the vault


DEFAULT_TYPES = {"note": NoteType("Note.md", "Notes")}


@dataclass(frozen=True)
class Config:
    vault: Path
    inbox: str = "Inbox"
    templates: str = "Templates"
    archive: str = "Archive"
    ignored: tuple[str, ...] = ()
    types: dict[str, NoteType] = field(default_factory=dict)

    # --- absolute paths -------------------------------------------------
    @property
    def inbox_dir(self) -> Path:
        return self.vault / self.inbox

    @property
    def templates_dir(self) -> Path:
        return self.vault / self.templates

    @property
    def archive_dir(self) -> Path:
        return self.vault / self.archive

    # --- ignoring -------------------------------------------------------
    @property
    def ignored_dirs(self) -> list[Path]:
        """Folders (absolute) that are never treated as real notes."""
        dirs = [self.vault / ".obsidian", self.templates_dir, self.archive_dir]
        dirs += [self.vault / name for name in self.ignored]
        if PROJECT_DIR.is_relative_to(self.vault) and PROJECT_DIR != self.vault:
            dirs.append(PROJECT_DIR)  # the project folder ignores itself
        return dirs

    def is_ignored(self, path: Path) -> bool:
        return any(path.is_relative_to(folder) for folder in self.ignored_dirs)


# --------------------------------------------------------------------------- #
# Finding the vault and loading the file
# --------------------------------------------------------------------------- #
def find_vault(start: Path | None = None) -> Path:
    """Walk up from `start` (default: cwd) until a folder containing `.obsidian`."""
    start = (start or Path.cwd()).resolve()
    for folder in (start, *start.parents):
        if (folder / ".obsidian").is_dir():
            return folder
    raise FileNotFoundError(
        f"No Obsidian vault found from {start}. Run inside your vault, "
        f"pass --vault, or set {ENV_VAULT}."
    )


def resolve_vault(vault: Path | None = None) -> Path:
    if vault is not None:
        return Path(vault).expanduser().resolve()
    if os.environ.get(ENV_VAULT):
        return Path(os.environ[ENV_VAULT]).expanduser().resolve()
    return find_vault()


def load_config(vault: Path | None = None) -> Config:
    vault = resolve_vault(vault)
    data: dict = {}
    config_file = vault / CONFIG_FILENAME
    if config_file.exists():
        with open(config_file, "rb") as f:
            data = tomllib.load(f)

    folders = data.get("folders", {})
    types: dict[str, NoteType] = {}
    for name, spec in data.get("types", {}).items():
        if "template" not in spec or "folder" not in spec:
            raise ValueError(f"[types.{name}] in {CONFIG_FILENAME} needs 'template' and 'folder'")
        types[name] = NoteType(spec["template"], spec["folder"])

    defaults = Config(vault=vault)
    return Config(
        vault=vault,
        inbox=folders.get("inbox", defaults.inbox),
        templates=folders.get("templates", defaults.templates),
        archive=folders.get("archive", defaults.archive),
        ignored=tuple(folders.get("ignored", ())),
        types=types or dict(DEFAULT_TYPES),
    )


def validate(config: Config) -> list[str]:
    """Human-readable problems with the configuration (empty list = OK)."""
    problems = []
    if not config.vault.is_dir():
        return [f"Vault folder does not exist: {config.vault}"]
    if not config.templates_dir.is_dir():
        problems.append(f"Templates folder not found: {config.templates_dir}")
    for name, note_type in config.types.items():
        if not (config.templates_dir / note_type.template).is_file():
            problems.append(f"Type '{name}': template not found: {note_type.template}")
        if not (config.vault / note_type.folder).is_dir():
            problems.append(f"Type '{name}': destination folder not found: {note_type.folder}")
    return problems


# --------------------------------------------------------------------------- #
# The active configuration (loaded lazily, replaceable)
# --------------------------------------------------------------------------- #
_current: Config | None = None


def get_config() -> Config:
    """The active configuration. Loaded on first use."""
    global _current
    if _current is None:
        _current = load_config()
    return _current


def set_config(config: Config | None) -> None:
    """Replace the active configuration (None = reload on next get_config())."""
    global _current
    _current = config
