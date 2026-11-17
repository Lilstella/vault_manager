from datetime import datetime

import pytest

from commands import create_note

NOW = datetime(2026, 1, 5, 9, 7)


@pytest.fixture
def templates(vault):
    folder = vault / "90 - Plantillas"
    folder.mkdir()
    (folder / "Tarea.md").write_text(
        "---\nfecha: {{date:YYYY-MM-DD}}\n---\n# {{title}}\nhora {{time}}\n", encoding="utf-8")
    return folder


# --- replace_variables ------------------------------------------------------
def test_replace_title_and_dates():
    texto = "# {{title}}\nfecha: {{date}}\nfecha2: {{date:YYYY-MM-DD}}"
    salida = create_note.replace_variables(texto, "TP Final", NOW)
    assert salida == "# TP Final\nfecha: 2026-01-05\nfecha2: 2026-01-05"


def test_replace_time():
    assert create_note.replace_variables("{{time}}", "x", NOW) == "09:07"


def test_replace_moment_formats():
    assert create_note.replace_variables("{{date:DD/MM/YY}}", "x", NOW) == "05/01/26"
    assert create_note.replace_variables("{{date:MMMM}}", "x", NOW) == "January"


def test_replace_tolerates_spaces_inside_braces():
    assert create_note.replace_variables("{{ title }} {{date:YYYY }}", "T", NOW) == "T 2026"


def test_unknown_variables_are_left_alone():
    assert create_note.replace_variables("{{foo}}", "x", NOW) == "{{foo}}"


def test_title_is_inserted_literally():
    # El título nunca se interpreta como patrón (ni como variable)
    assert create_note.replace_variables("{{title}}", r"a\1 {{date}}", NOW) == r"a\1 {{date}}"


# --- load_template ----------------------------------------------------------
def test_load_template(templates):
    assert "{{title}}" in create_note.load_template("tarea")


def test_unknown_type_lists_valid_types(vault):
    with pytest.raises(ValueError, match="apunte, tarea"):
        create_note.load_template("inexistente")


def test_missing_template_file(vault):
    with pytest.raises(FileNotFoundError, match="Tarea.md"):
        create_note.load_template("tarea")


# --- destination_path -------------------------------------------------------
def test_destination_is_inside_the_vault(vault):
    path = create_note.destination_path("tarea", "TP Final")
    assert path == vault / "01 - Universidad" / "Tareas" / "TP Final.md"


def test_destination_replaces_invalid_characters(vault):
    path = create_note.destination_path("tarea", "TP: 1/2 [x] #3")
    assert path.name == "TP_ 1_2 _x_ _3.md"


def test_destination_rejects_empty_title(vault):
    with pytest.raises(ValueError):
        create_note.destination_path("tarea", "   ")


def test_destination_existing_note(vault):
    existente = vault / "01 - Universidad" / "Tareas" / "TP Final.md"
    existente.parent.mkdir(parents=True)
    existente.write_text("x", encoding="utf-8")
    with pytest.raises(FileExistsError, match="TP Final.md"):
        create_note.destination_path("tarea", "TP Final")


# --- create_note / main -----------------------------------------------------
def test_create_note_writes_file(vault, templates):
    path, text = create_note.create_note("tarea", "TP Final", now=NOW)
    assert path.read_text(encoding="utf-8") == text
    assert "# TP Final" in text and "fecha: 2026-01-05" in text


def test_create_note_simulate_does_not_write(vault, templates):
    path, _ = create_note.create_note("tarea", "TP Final", simulate=True, now=NOW)
    assert not path.exists()


def test_main_creates_and_reports(vault, templates, capsys):
    assert create_note.main(["tarea", "TP Final"]) == 0
    assert "Created:" in capsys.readouterr().out


def test_main_existing_note_returns_1(vault, templates, capsys):
    create_note.main(["tarea", "TP Final"])
    assert create_note.main(["tarea", "TP Final"]) == 1
    assert "already exists" in capsys.readouterr().err
