"""Desempate de posicao e alinhamento de indice em context.py.

Complementa test_context.py, que cobre haversine, viagem, descanso basico,
snapshot simples e flags de era.
"""
import pandas as pd

from context import rest_days, table_snapshot


def test_table_snapshot_desempata_por_saldo_de_gols():
    d = pd.DataFrame({
        "season": [2010, 2010, 2010],
        "date": pd.to_datetime(["2010-05-01", "2010-05-01", "2010-05-08"]),
        "round": [1, 1, 2],
        "match_id": ["1", "2", "3"],
        "home_team": ["A", "C", "A"],
        "away_team": ["B", "D", "C"],
        "home_goals": [2, 1, 0],
        "away_goals": [0, 0, 0],
    })
    s = table_snapshot(d)
    # Antes da rodada 2: A e C empatam em pontos e vitorias; saldo decide
    # (A +2 x C +1).
    linha = s.loc[2]
    assert linha["home_pts_before"] == linha["away_pts_before"] == 3
    assert (linha["home_pos_before"], linha["away_pos_before"]) == (1, 2)


def test_table_snapshot_empate_compartilha_posicao():
    d = pd.DataFrame({
        "season": [2010, 2010, 2010],
        "date": pd.to_datetime(["2010-05-01", "2010-05-01", "2010-05-08"]),
        "round": [1, 1, 2],
        "match_id": ["1", "2", "3"],
        "home_team": ["A", "C", "A"],
        "away_team": ["B", "D", "C"],
        "home_goals": [1, 1, 0],
        "away_goals": [1, 1, 0],
    })
    s = table_snapshot(d)
    # Quatro clubes com 1 pt, 0 vitorias e saldo 0: mesma posicao (rank min).
    linha = s.loc[2]
    assert linha["home_pts_before"] == linha["away_pts_before"] == 1
    assert linha["home_pos_before"] == linha["away_pos_before"] == 1


def test_rest_days_preserva_ordem_original_do_indice():
    d = pd.DataFrame({
        "date": pd.to_datetime(["2020-08-12", "2020-08-09", "2020-08-15"]),
        "home_team": ["A", "B", "A"],
        "away_team": ["B", "C", "C"],
    })
    r = rest_days(d)
    assert list(r.index) == [0, 1, 2]
    assert r.loc[0, "away_rest"] == 3.0
    assert r.loc[2, "home_rest"] == 3.0
    assert r.loc[2, "away_rest"] == 6.0
