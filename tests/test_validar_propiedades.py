from datetime import date

from commands import validar_propiedades as vp


def test_fecha_valida():
    assert vp.fecha_valida_iso(date(2025, 5, 11))
    assert vp.fecha_valida_iso("2025-05-11")


def test_fecha_invalida():
    assert not vp.fecha_valida_iso("11/05/2025")
    assert not vp.fecha_valida_iso("2025-13-40")
    assert not vp.fecha_valida_iso(None)
    assert not vp.fecha_valida_iso(20250511)


def test_tarea_correcta():
    props = {"asignatura": "Fundamentos", "fecha-entrega": date(2025, 5, 11),
             "prioridad": "alta", "completado": False}
    assert vp.validar_tarea(props) == []


def test_tarea_con_errores():
    props = {"asignatura": "", "fecha-entrega": "11/05/2025",
             "prioridad": "urgente", "completado": "true"}
    problemas = vp.validar_tarea(props)
    assert len(problemas) >= 3


def test_tipo_de_nota():
    assert vp.tipo_de_nota({"tags": "universidad/tarea"}) == "tarea"
    assert vp.tipo_de_nota({"tags": ["universidad/examen"]}) == "examen"
    assert vp.tipo_de_nota({}) is None
