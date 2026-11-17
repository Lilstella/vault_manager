from commands import limpiar_pdf


def test_une_palabras_cortadas():
    assert limpiar_pdf.unir_palabras_cortadas("una demon-\nstration clara") == "una demonstration clara"


def test_no_toca_guiones_dentro_de_la_linea():
    assert limpiar_pdf.unir_palabras_cortadas("bien-estar general") == "bien-estar general"


def test_une_lineas_de_un_parrafo():
    assert limpiar_pdf.unir_lineas_de_parrafo("esto es una\noración partida") == "esto es una oración partida"


def test_respeta_parrafos():
    assert limpiar_pdf.unir_lineas_de_parrafo("uno\n\ndos") == "uno\n\ndos"


def test_no_une_listas():
    texto = "- a\n- b"
    assert limpiar_pdf.unir_lineas_de_parrafo(texto) == texto


def test_normaliza_espacios():
    assert limpiar_pdf.normalizar_espacios("hola   mundo  \nchau") == "hola mundo\nchau"
