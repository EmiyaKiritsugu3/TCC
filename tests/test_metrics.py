"""Testes dos indicadores (seção 16.1 da spec)."""
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from metrics import by_season, pollard, summarize, team_season

PROCESSED = Path(__file__).resolve().parent.parent / "data" / "processed" / "matches_processed.csv"


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


def test_team_season_separa_pontos_de_casa_e_fora():
    casa = _df([(2, 0), (1, 1), (0, 2), (3, 0)])
    casa["season"] = 2019
    casa["home_team"] = "Flamengo"
    casa["away_team"] = ["A", "B", "C", "D"]

    fora = _df([(0, 2), (1, 1), (2, 0)])
    fora["season"] = 2019
    fora["home_team"] = ["A", "B", "C"]
    fora["away_team"] = "Flamengo"

    d = pd.concat([casa, fora], ignore_index=True)
    ts = team_season(d, "Flamengo", 2019)

    assert (ts["home_w"], ts["home_d"], ts["home_l"]) == (2, 1, 1)
    assert ts["home_points"] == 7          # 3 + 1 + 0 + 3
    assert (ts["away_w"], ts["away_d"], ts["away_l"]) == (1, 1, 1)
    assert ts["away_points"] == 4          # 3 + 1 + 0
    assert isinstance(ts["home_points"], int)
    assert isinstance(ts["away_points"], int)


@pytest.mark.skipif(not PROCESSED.exists(), reason="rode scripts/build_processed.py")
def test_flamengo_2019_pontuacao_oficial():
    df = pd.read_csv(PROCESSED)
    ts = team_season(df, "Flamengo", 2019)
    assert (ts["home_points"], ts["away_points"]) == (53, 37)
    assert ts["home_points"] + ts["away_points"] == 90
    assert ts["home_n"] + ts["away_n"] == 38
