"""Medias de gols, saldo e contrato de erro de summarize; esquema de by_season vazio.

Complementa test_metrics.py, que cobre n, pontos, Pollard e proporcoes.
"""
import pandas as pd
import pytest

from metrics import by_season, summarize


def _df(rows):
    d = pd.DataFrame(rows, columns=["home_goals", "away_goals"])
    d["result"] = "D"
    d.loc[d["home_goals"] > d["away_goals"], "result"] = "H"
    d.loc[d["home_goals"] < d["away_goals"], "result"] = "A"
    d["home_points"] = d["result"].map({"H": 3, "D": 1, "A": 0})
    d["away_points"] = d["result"].map({"H": 0, "D": 1, "A": 3})
    return d


def test_summarize_medias_de_gols_e_saldo():
    s = summarize(_df([(3, 1), (0, 1)]))
    assert s["avg_home_goals"] == 1.5
    assert s["avg_away_goals"] == 1.0
    assert s["goal_diff"] == 0.5


def test_summarize_exige_colunas_obrigatorias():
    d = _df([(1, 0)]).drop(columns=["home_goals"])
    with pytest.raises(ValueError, match="Coluna obrigatória"):
        summarize(d)


def test_by_season_vazio_tem_esquema_completo():
    t = by_season(pd.DataFrame())
    assert t.empty
    assert list(t.columns) == [
        "season", "n", "p_home", "p_draw", "p_away",
        "avg_home_goals", "avg_away_goals", "goal_diff",
        "home_points", "away_points", "pollard",
    ]
