"""Regra da exceção conhecida de data na validação cruzada (PT-BR)."""
import pandas as pd

from validacao_excecoes import excecao_conhecida


def _jogo(date, casa, fora, sufixo):
    return pd.DataFrame([{
        "date": date, "home_team": casa, "away_team": fora,
        f"home_goals_{sufixo}": 1, f"away_goals_{sufixo}": 1,
    }])


def test_toleranca_excecao_aceita_caso_conhecido():
    base = _jogo("2023-10-22", "Botafogo-RJ", "Athletico-PR", "base")
    of = _jogo("2023-10-21", "Botafogo-RJ", "Athletico-PR", "of")
    assert excecao_conhecida(2023, base, of, 0) is True


def test_toleranca_excecao_rejeita_fora_do_caso_conhecido():
    base = _jogo("2022-05-10", "Flamengo", "Vasco", "base")
    of = _jogo("2022-05-09", "Flamengo", "Vasco", "of")
    assert excecao_conhecida(2022, base, of, 0) is False
