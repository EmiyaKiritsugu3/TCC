"""Regressões dos comentários de revisão sobre bootstrap/fetch_raw (PT-BR)."""
import subprocess
import sys
from pathlib import Path

import pytest

import bootstrap
import fetch_raw


def test_checar_lock_marca_divergencia_como_falha(monkeypatch):
    monkeypatch.setattr(bootstrap, "pins_do_lock", lambda: [("pandas", "3.1.0")])
    monkeypatch.setattr(
        bootstrap, "rodar",
        lambda *a, **k: subprocess.CompletedProcess([], 0, '{"pandas":"2.0.0"}', ""),
    )
    assert bootstrap.checar_lock(Path("python")) is False


def test_checar_coleta_desativa_cache_do_pytest(monkeypatch):
    visto = {}

    def fake(comando, env):
        visto["comando"] = comando
        return subprocess.CompletedProcess([], 0, "2 tests collected", "")

    monkeypatch.setattr(bootstrap, "rodar", fake)
    bootstrap.checar_coleta(Path("python"), {})
    assert "no:cacheprovider" in " ".join(visto["comando"])


def test_check_nao_cria_diretorio_raw(tmp_path, monkeypatch):
    destino = tmp_path / "raw"
    monkeypatch.setattr(fetch_raw, "DEST", destino)
    with pytest.raises(SystemExit):
        fetch_raw.main(["--check"])
    assert not destino.exists()


def test_bootstrap_instala_pacote_e_mostra_interpreter(monkeypatch, capsys):
    comandos = []

    def fake(comando, env):
        comandos.append(comando)
        return subprocess.CompletedProcess([], 0, "", "")

    monkeypatch.setattr(bootstrap, "rodar", fake)
    monkeypatch.setattr(bootstrap, "interpretador", lambda: Path("/tmp/.venv/bin/python"))
    monkeypatch.setattr(sys, "argv", ["bootstrap.py"])
    assert bootstrap.main() == 0
    assert any("install" in c and "-e" in c for c in comandos)
    assert "/tmp/.venv/bin/python" in capsys.readouterr().out
