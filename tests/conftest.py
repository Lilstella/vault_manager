"""Fixtures compartidos. Ningún test toca tu vault real."""
import pytest

from config import ENV_VAULT, Config, NoteType, set_config


@pytest.fixture(autouse=True)
def _isolate_config(tmp_path, monkeypatch):
    """Evita que un test cargue por accidente la configuración de tu vault real."""
    monkeypatch.setenv(ENV_VAULT, str(tmp_path / "vault_sin_configurar"))
    set_config(None)
    yield
    set_config(None)


@pytest.fixture
def vault(tmp_path):
    """Vault temporal con su configuración activa."""
    root = tmp_path / "vault"
    (root / ".obsidian").mkdir(parents=True)
    set_config(Config(
        vault=root,
        inbox="00 - Inbox",
        templates="90 - Plantillas",
        archive="99 - Archivo",
        ignored=("91 - Scripts",),
        types={
            "tarea": NoteType("Tarea.md", "01 - Universidad/Tareas"),
            "apunte": NoteType("Apunte.md", "01 - Universidad/Apuntes"),
        },
    ))
    return root
