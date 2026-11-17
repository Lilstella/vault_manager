from commands import normalizar_fechas as nf


def test_dia_mes():
    assert nf.convertir_fecha("11/05/2025") == "2025-05-11"


def test_mes_dia():
    assert nf.convertir_fecha("11/05/2025", dayfirst=False) == "2025-11-05"


def test_guiones_y_un_digito():
    assert nf.convertir_fecha("5-3-2025") == "2025-03-05"


def test_invalida():
    assert nf.convertir_fecha("31/02/2025") is None


def test_ya_iso():
    assert nf.convertir_fecha("2025-05-11") == "2025-05-11"


def test_encontrar_ignora_iso():
    assert nf.encontrar_fechas("hoy 2025-05-11 y 11/05/2025") == ["11/05/2025"]
