"""Testes dos indicadores (seção 16.1 da spec)."""
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from metrics import by_season, pollard, summarize


def _df(rows):
    # rows: (hg, ag)
    d = pd.DataFrame(rows, columns=["home_goals", "away_goals"])
    d["result"] = "D"
    d.loc[d["home_goals"] > d["away_goals"], "result"] = "H"
    d.loc[d["home_goals"] < d["away_goals"], "result"] = "A"
    d["home_points"] = d["result"].map({"H": 3, "D": 1, "A": 0})
    d["away_points"] = d["result"].map({"H": 0, "D": 1, "A": 3})
    return d


def test_caso_referencia_tres_partidas():
    # Tabela da seção 16.1: Ph=4, Pv=4 -> Pollard exatamente 50%, 1/3 cada.
    s = summarize(_df([(2, 0), (1, 1), (0, 2)]))
    assert s["n"] == 3
    assert s["home_points"] == 4 and s["away_points"] == 4
    assert s["pollard"] == 50.0
    assert s["p_home"] == s["p_draw"] == s["p_away"] == pytest.approx(100 / 3)


def test_tudo_mandante_acima_50_e_tudo_visitante_abaixo():
    assert summarize(_df([(1, 0)] * 5))["pollard"] > 50
    assert summarize(_df([(0, 1)] * 5))["pollard"] < 50


def test_proporcoes_somam_100():
    s = summarize(_df([(2, 0), (1, 1), (0, 2), (3, 1)]))
    assert s["p_home"] + s["p_draw"] + s["p_away"] == 100.0


def test_pollard_indefinido_sem_pontos():
    assert pollard(0, 0) is None
    assert summarize(_df([]).iloc[0:0])["pollard"] is None


def test_recorte_vazio_nao_quebra():
    s = summarize(_df([]).iloc[0:0])
    assert s["n"] == 0 and s["p_home"] is None


def test_by_season_agrega():
    d = _df([(1, 0), (0, 0)])
    d["season"] = [2010, 2011]
    t = by_season(d)
    assert list(t["season"]) == [2010, 2011]
    assert t.loc[t["season"] == 2010, "pollard"].iloc[0] == 100.0
