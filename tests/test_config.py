from pathlib import Path

import pytest

import config
from config import Config, NoteType, find_vault, get_config, load_config, set_config, validate

TOML = """
[folders]
inbox = "00 - Inbox"
templates = "90 - Plantillas"
archive = "99 - Archivo"
ignored = ["91 - Scripts", "Meta/Viejo"]

[types.tarea]
template = "Tarea.md"
folder = "01 - Universidad/Tareas"
"""


@pytest.fixture
def real_vault(tmp_path):
    root = tmp_path / "mi_vault"
    (root / ".obsidian").mkdir(parents=True)
    return root


# --- finding the vault ------------------------------------------------------
def test_find_vault_walks_up(real_vault):
    profunda = real_vault / "a" / "b"
    profunda.mkdir(parents=True)
    assert find_vault(profunda) == real_vault.resolve()


def test_find_vault_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        find_vault(tmp_path)


def test_explicit_vault_wins_over_env(real_vault, tmp_path, monkeypatch):
    monkeypatch.setenv(config.ENV_VAULT, str(tmp_path / "otro"))
    assert load_config(real_vault).vault == real_vault.resolve()


def test_env_var_is_used(real_vault, monkeypatch):
    monkeypatch.setenv(config.ENV_VAULT, str(real_vault))
    assert load_config().vault == real_vault.resolve()


# --- loading ----------------------------------------------------------------
def test_defaults_without_toml(real_vault):
    cfg = load_config(real_vault)
    assert cfg.templates == "Templates"
    assert "note" in cfg.types


def test_toml_overrides_defaults(real_vault):
    (real_vault / config.CONFIG_FILENAME).write_text(TOML, encoding="utf-8")
    cfg = load_config(real_vault)
    assert cfg.templates == "90 - Plantillas"
    assert cfg.types == {"tarea": NoteType("Tarea.md", "01 - Universidad/Tareas")}
    assert cfg.ignored == ("91 - Scripts", "Meta/Viejo")


def test_incomplete_type_is_a_clear_error(real_vault):
    (real_vault / config.CONFIG_FILENAME).write_text("[types.tarea]\ntemplate = 'T.md'\n", encoding="utf-8")
    with pytest.raises(ValueError, match="types.tarea"):
        load_config(real_vault)


# --- ignoring ---------------------------------------------------------------
@pytest.fixture
def cfg(real_vault):
    (real_vault / config.CONFIG_FILENAME).write_text(TOML, encoding="utf-8")
    return load_config(real_vault)


@pytest.mark.parametrize("relative", [
    ".obsidian/app.json", "90 - Plantillas/Tarea.md", "99 - Archivo/a/b.md",
    "91 - Scripts/x.md", "Meta/Viejo/nota.md",
])
def test_ignored(cfg, relative):
    assert cfg.is_ignored(cfg.vault / relative)


@pytest.mark.parametrize("relative", [
    "Dashboard.md", "01 - Universidad/Tareas/t.md", "90 - Plantillas extra/t.md",
    "Meta/Nuevo/nota.md", "01 - Universidad/99 - Archivo/n.md",
])
def test_not_ignored(cfg, relative):
    assert not cfg.is_ignored(cfg.vault / relative)


# --- validate ---------------------------------------------------------------
def test_validate_reports_missing_things(cfg):
    problems = validate(cfg)
    assert any("Templates folder" in p for p in problems)
    assert any("Tarea.md" in p for p in problems)
    assert any("destination folder" in p for p in problems)


def test_validate_ok(cfg):
    (cfg.vault / "90 - Plantillas").mkdir()
    (cfg.vault / "90 - Plantillas" / "Tarea.md").write_text("x", encoding="utf-8")
    (cfg.vault / "01 - Universidad" / "Tareas").mkdir(parents=True)
    assert validate(cfg) == []


# --- active configuration ---------------------------------------------------
def test_set_and_get_config(real_vault):
    custom = Config(vault=real_vault, inbox="Entrada")
    set_config(custom)
    assert get_config() is custom


def test_get_config_loads_lazily_and_caches(real_vault, monkeypatch):
    monkeypatch.setenv(config.ENV_VAULT, str(real_vault))
    set_config(None)
    assert get_config() is get_config()
