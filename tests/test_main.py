import main


def test_no_arguments_prints_help(vault, capsys):
    assert main.main([]) == 0
    assert "Commands:" in capsys.readouterr().out


def test_unknown_command(vault, capsys):
    assert main.main(["inventado"]) == 2
    assert "Unknown command" in capsys.readouterr().err


def test_missing_vault_is_reported(tmp_path, capsys, monkeypatch):
    monkeypatch.delenv("VAULT_MANAGER_VAULT")
    monkeypatch.chdir(tmp_path)
    assert main.main(["config"]) == 2
    assert "Configuration error" in capsys.readouterr().err


def test_config_command_reports_problems(vault, capsys):
    # el vault de prueba no tiene plantillas -> hay problemas
    assert main.main(["--vault", str(vault), "config"]) == 1
    assert "Problems found" in capsys.readouterr().out


def test_vault_flag_can_go_anywhere(vault, capsys):
    assert main.main(["config", "--vault", str(vault)]) == 1


def test_new_command_goes_through_to_the_module(vault, capsys):
    (vault / "vault_manager.toml").write_text(
        '[folders]\ntemplates = "T"\n[types.nota]\ntemplate = "N.md"\nfolder = "Notas"\n',
        encoding="utf-8")
    (vault / "T").mkdir()
    (vault / "T" / "N.md").write_text("# {{title}}\n", encoding="utf-8")
    assert main.main(["--vault", str(vault), "new", "nota", "Hola", "--simulate"]) == 0
    assert "would create" in capsys.readouterr().out
