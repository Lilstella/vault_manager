"""
Tests de helper.py.

Los tests de ignored/list_notes/read_note/write_note trabajan sobre un vault
temporal (tmp_path), así que nunca tocan tu vault real.
"""
import re
from datetime import date
from pathlib import Path

import pytest

import helper

IGNORED = {".obsidian", "90 - Plantillas", "91 - Scripts", "99 - Archivo"}


# El fixture `vault` (vault temporal + configuración) está en conftest.py.
def make_note(vault: Path, relative: str, content: str = "# nota\n") -> Path:
    path = vault / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


# --------------------------------------------------------------------------- #
# ignored
# --------------------------------------------------------------------------- #
def test_ignored_normal_folder_is_not_ignored(vault):
    note = make_note(vault, "01 - Universidad/Tareas/TP.md")
    assert helper.ignored(note) is False


@pytest.mark.parametrize("folder", sorted(IGNORED))
def test_ignored_each_ignored_folder(vault, folder):
    note = make_note(vault, f"{folder}/nota.md")
    assert helper.ignored(note) is True


def test_ignored_nested_inside_ignored_folder(vault):
    note = make_note(vault, "99 - Archivo/2025/Viejo/nota.md")
    assert helper.ignored(note) is True


def test_ignored_note_in_vault_root_is_not_ignored(vault):
    note = make_note(vault, "Dashboard.md")
    assert helper.ignored(note) is False


def test_ignored_vault_itself_is_not_ignored(vault):
    assert helper.ignored(vault) is False


def test_ignored_similar_name_is_not_ignored(vault):
    note = make_note(vault, "90 - Plantillas extra/nota.md")
    assert helper.ignored(note) is False


def test_ignored_ignored_name_deeper_in_path_does_not_count(vault):
    note = make_note(vault, "01 - Universidad/99 - Archivo/nota.md")
    assert helper.ignored(note) is False


def test_ignored_path_outside_vault_is_not_ignored(vault, tmp_path_factory):
    outside = tmp_path_factory.mktemp("otro") / "nota.md"
    assert helper.ignored(outside) is False


# --------------------------------------------------------------------------- #
# list_notes
# --------------------------------------------------------------------------- #
def test_list_notes_empty_vault(vault):
    assert helper.list_notes() == []


def test_list_notes_returns_paths(vault):
    make_note(vault, "Dashboard.md")
    notes = helper.list_notes()
    assert all(isinstance(n, Path) for n in notes)


def test_list_notes_only_markdown(vault):
    make_note(vault, "nota.md")
    make_note(vault, "datos.txt")
    make_note(vault, "script.py")
    (vault / "imagen.png").write_bytes(b"\x89PNG")
    assert helper.list_notes() == [vault / "nota.md"]


def test_list_notes_finds_nested_notes(vault):
    profunda = make_note(vault, "01 - Universidad/Apuntes/Fundamentos/clase1.md")
    assert profunda in helper.list_notes()


def test_list_notes_excludes_ignored_by_default(vault):
    visible = make_note(vault, "01 - Universidad/nota.md")
    make_note(vault, "90 - Plantillas/Tarea.md")
    make_note(vault, "99 - Archivo/vieja.md")
    make_note(vault, ".obsidian/README.md")
    assert helper.list_notes() == [visible]


def test_list_notes_includes_ignored_when_asked(vault):
    a = make_note(vault, "01 - Universidad/nota.md")
    b = make_note(vault, "90 - Plantillas/Tarea.md")
    c = make_note(vault, "99 - Archivo/vieja.md")
    assert helper.list_notes(True) == sorted([a, b, c])


def test_list_notes_is_sorted(vault):
    z = make_note(vault, "z.md")
    a = make_note(vault, "a.md")
    m = make_note(vault, "carpeta/m.md")
    assert helper.list_notes() == sorted([z, a, m])


# --------------------------------------------------------------------------- #
# read_note
# --------------------------------------------------------------------------- #
def test_read_note_returns_content(vault):
    note = make_note(vault, "nota.md", "hola\nmundo\n")
    assert helper.read_note(note) == "hola\nmundo\n"


def test_read_note_utf8(vault):
    texto = "Título con ñ, acentos áéíóú y emojis 🎓✔\n"
    note = make_note(vault, "nota.md", texto)
    assert helper.read_note(note) == texto


def test_read_note_empty_file(vault):
    note = make_note(vault, "vacia.md", "")
    assert helper.read_note(note) == ""


def test_read_note_missing_file_raises(vault):
    with pytest.raises(FileNotFoundError):
        helper.read_note(vault / "no_existe.md")


def test_read_note_normalizes_crlf(vault):
    note = vault / "windows.md"
    note.write_bytes(b"---\r\na: 1\r\n---\r\ncuerpo\r\n")
    assert helper.read_note(note) == "---\na: 1\n---\ncuerpo\n"


# --------------------------------------------------------------------------- #
# write_note
# --------------------------------------------------------------------------- #
def test_write_note_creates_file(vault):
    path = vault / "nueva.md"
    helper.write_note(path, "contenido")
    assert path.read_text(encoding="utf-8") == "contenido"


def test_write_note_creates_intermediate_folders(vault):
    path = vault / "01 - Universidad" / "Tareas" / "profunda" / "TP.md"
    helper.write_note(path, "x")
    assert path.exists()


def test_write_note_overwrites_existing(vault):
    path = make_note(vault, "nota.md", "viejo")
    helper.write_note(path, "nuevo")
    assert path.read_text(encoding="utf-8") == "nuevo"


def test_write_note_writes_utf8_bytes(vault):
    path = vault / "nota.md"
    helper.write_note(path, "Ñandú ✔")
    assert path.read_bytes() == "Ñandú ✔".encode("utf-8")


def test_write_then_read_roundtrip(vault):
    path = vault / "sub" / "nota.md"
    texto = "---\ntags: [a, b]\n---\n# Título ñ 🎓\n\nTexto.\n"
    helper.write_note(path, texto)
    assert helper.read_note(path) == texto


def test_write_note_keeps_lf_line_endings(vault):
    path = vault / "nota.md"
    helper.write_note(path, "a\nb\n")
    assert b"\r" not in path.read_bytes()


# --------------------------------------------------------------------------- #
# separate_frontmatter
# --------------------------------------------------------------------------- #
def test_no_frontmatter():
    props, body = helper.separate_frontmatter("# Hola\ntexto")
    assert props == {}
    assert body == "# Hola\ntexto"


def test_empty_string():
    assert helper.separate_frontmatter("") == ({}, "")


def test_with_frontmatter():
    texto = "---\nasignatura: Fundamentos\ncompletado: false\n---\n# Título\n"
    props, body = helper.separate_frontmatter(texto)
    assert props["asignatura"] == "Fundamentos"
    assert props["completado"] is False
    assert body.strip() == "# Título"


def test_body_is_returned_exactly():
    props, body = helper.separate_frontmatter("---\na: 1\n---\n# T\n\nTexto\n")
    assert props == {"a": 1}
    assert body == "# T\n\nTexto\n"


def test_empty_frontmatter_does_not_break():
    props, body = helper.separate_frontmatter("---\n---\ncuerpo")
    assert props == {}
    assert body == "cuerpo"


def test_yaml_types():
    texto = (
        "---\n"
        "fecha-entrega: 2025-05-11\n"
        "completado: true\n"
        "tags: [universidad/tarea, urgente]\n"
        "nota: 8.5\n"
        "---\n"
    )
    props, _ = helper.separate_frontmatter(texto)
    assert props["fecha-entrega"] == date(2025, 5, 11)
    assert props["completado"] is True
    assert props["tags"] == ["universidad/tarea", "urgente"]
    assert props["nota"] == 8.5


def test_non_iso_date_stays_a_string():
    props, _ = helper.separate_frontmatter("---\nfecha: 11/05/2025\n---\n")
    assert props["fecha"] == "11/05/2025"


def test_unicode_in_frontmatter():
    props, _ = helper.separate_frontmatter("---\ntítulo: Café ñandú\n---\n")
    assert props["título"] == "Café ñandú"


def test_horizontal_rule_in_body_stays_in_body():
    texto = "---\na: 1\n---\ntexto\n---\nmás texto\n"
    props, body = helper.separate_frontmatter(texto)
    assert props == {"a": 1}
    assert body == "texto\n---\nmás texto\n"


def test_dashes_not_on_first_line_is_not_frontmatter():
    texto = "\n---\na: 1\n---\ncuerpo"
    assert helper.separate_frontmatter(texto) == ({}, texto)


def test_invalid_yaml_returns_original_text():
    texto = "---\ntitulo: Hola: mundo\n---\nbody"
    assert helper.separate_frontmatter(texto) == ({}, texto)


def test_scalar_yaml_does_not_lose_text():
    texto = "---\nTexto que no es yaml\n\nmas\n---\nfin"
    assert helper.separate_frontmatter(texto) == ({}, texto)


def test_list_yaml_does_not_lose_text():
    texto = "---\n- a\n- b\n---\nbody"
    assert helper.separate_frontmatter(texto) == ({}, texto)


def test_frontmatter_at_end_of_file_without_newline():
    props, body = helper.separate_frontmatter("---\na: 1\n---")
    assert props == {"a": 1}
    assert body == ""


def test_closing_delimiter_with_trailing_spaces():
    props, body = helper.separate_frontmatter("---\na: 1\n--- \nbody")
    assert props == {"a": 1}
    assert body == "body"


# --------------------------------------------------------------------------- #
# iso_date
# --------------------------------------------------------------------------- #
def test_iso_date_format():
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", helper.iso_date())


def test_iso_date_is_today():
    assert helper.iso_date() == date.today().isoformat()


def test_iso_date_fixed_day_with_zero_padding(monkeypatch):
    class FakeDate(date):
        @classmethod
        def today(cls):
            return cls(2026, 1, 5)

    monkeypatch.setattr(helper, "date", FakeDate)
    assert helper.iso_date() == "2026-01-05"