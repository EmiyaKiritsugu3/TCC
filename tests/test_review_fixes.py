"""Testes de regressão dos achados da revisão final do branch (PT-BR)."""
import io
from pathlib import Path

import pandas as pd
import pytest

import fetch_raw
from validacao_excecoes import excecao_conhecida

RAIZ = Path(__file__).resolve().parent.parent


class _Resp(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def test_baixar_usa_timeout_e_grava_arquivo(tmp_path, monkeypatch):
    visto = {}

    def fake_urlopen(url, timeout=None):
        visto["url"], visto["timeout"] = url, timeout
        return _Resp(b"conteudo")

    monkeypatch.setattr(fetch_raw.urllib.request, "urlopen", fake_urlopen)
    destino = tmp_path / "arquivo.csv"
    fetch_raw.baixar("https://example.org/arquivo.csv", destino)
    assert visto["timeout"] == 60
    assert destino.read_bytes() == b"conteudo"


def test_excecao_rejeita_of_nao_relacionado():
    base = pd.DataFrame([{"date": "2023-10-22", "home_team": "Botafogo-RJ", "away_team": "Athletico-PR",
                          "home_goals_base": 1, "away_goals_base": 1}])
    of = pd.DataFrame([{"date": "2023-10-21", "home_team": "Flamengo", "away_team": "Vasco",
                        "home_goals_of": 1, "away_goals_of": 1}])
    assert excecao_conhecida(2023, base, of, 0) is False


def test_excecao_rejeita_base_fora_do_caso():
    base = pd.DataFrame([{"date": "2022-05-10", "home_team": "Flamengo", "away_team": "Vasco",
                          "home_goals_base": 1, "away_goals_base": 1}])
    of = pd.DataFrame([{"date": "2022-05-09", "home_team": "Flamengo", "away_team": "Vasco",
                        "home_goals_of": 1, "away_goals_of": 1}])
    assert excecao_conhecida(2022, base, of, 0) is False


def test_excecao_rejeita_placares_diferentes():
    base = pd.DataFrame([{"date": "2023-10-22", "home_team": "Botafogo-RJ",
                          "away_team": "Athletico-PR", "home_goals_base": 2, "away_goals_base": 1}])
    of = pd.DataFrame([{"date": "2023-10-21", "home_team": "Botafogo-RJ",
                        "away_team": "Athletico-PR", "home_goals_of": 1, "away_goals_of": 1}])
    assert excecao_conhecida(2023, base, of, 0) is False


def test_ci_mede_cobertura_e_invalida_cache_do_lock():
    ci = (RAIZ / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "--cov=src" in ci
    assert "requirements-lock.txt" in ci


def test_ci_valida_import_do_pacote_sem_pythonpath():
    ci = (RAIZ / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "env -u PYTHONPATH python3 -c \"import metrics, context, openfootball\"" in ci


def test_auditor_rejeita_caminho_fora_do_projeto(capsys):
    import check_monografia
    with pytest.raises(SystemExit) as exc:
        check_monografia.main(["--monografia", "/etc/passwd"])
    assert exc.value.code == 2
    assert "fora do projeto" in capsys.readouterr().err


def test_guardas_da_auditoria_sao_integracao():
    import test_check_monografia_guard as guardas
    marcas = [getattr(m, "name", str(m)) for m in getattr(guardas, "pytestmark", [])]
    assert "integration" in marcas


@pytest.mark.integration
@pytest.mark.skipif(not (RAIZ / "data" / "processed" / "matches_processed.csv").exists(),
                    reason="requer a base processada de build_processed.py")
def test_auditor_rejeita_contagem_desatualizada_no_apendice(tmp_path):
    from test_check_monografia_guard import _auditar_com_texto
    texto = (RAIZ / "docs" / "monografia_v2.md").read_text(encoding="utf-8")
    alterado = texto.replace("`tests/test_context.py` (10)", "`tests/test_context.py` (9)")
    resultado = _auditar_com_texto(tmp_path, alterado)
    assert resultado.returncode == 1
    assert "contagem de test_context" in resultado.stdout
