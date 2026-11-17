from commands import estadisticas


def test_tags_frontmatter_lista_e_inline():
    texto = "---\ntags: [uni, conocimiento/lectura]\n---\nhola #idea y # Título"
    assert estadisticas.extraer_tags(texto) == {"uni", "conocimiento/lectura", "idea"}


def test_tags_frontmatter_string():
    assert estadisticas.extraer_tags("---\ntags: universidad/tarea\n---\n") == {"universidad/tarea"}


def test_sin_tags():
    assert estadisticas.extraer_tags("solo texto") == set()
