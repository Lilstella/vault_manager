from commands import validar_vault


def test_extraer_enlaces():
    texto = "[[Nota]] [[Otra|alias]] [[Tercera#Sección]] [[ Con espacios ]]"
    assert validar_vault.extraer_enlaces(texto) == {"Nota", "Otra", "Tercera", "Con espacios"}


def test_sin_enlaces():
    assert validar_vault.extraer_enlaces("nada por acá") == set()
