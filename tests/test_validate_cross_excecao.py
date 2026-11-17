"""Regra da exceção conhecida de data na validação cruzada (PT-BR)."""
import pandas as pd

from validacao_excecoes import excecao_conhecida


def test_toleranca_excecao_aceita_caso_conhecido():
    base = pd.DataFrame([{"date": "2023-10-22", "home_team": "Botafogo-RJ", "away_team": "Athletico-PR"}])
    of = pd.DataFrame([{"date": "2023-10-21", "home_team": "Botafogo-RJ", "away_team": "Athletico-PR"}])
    assert excecao_conhecida(2023, base, of, 0) is True


def test_toleranca_excecao_rejeita_fora_do_caso_conhecido():
    base = pd.DataFrame([{"date": "2022-05-10", "home_team": "Flamengo", "away_team": "Vasco"}])
    of = pd.DataFrame([{"date": "2022-05-09", "home_team": "Flamengo", "away_team": "Vasco"}])
    assert excecao_conhecida(2022, base, of, 0) is False
