"""Testes das funções de associação (bootstrap, grupos, equipe, nível)."""
import numpy as np
import pandas as pd
import pytest

from associations import (
    annual_pollard_ci,
    bootstrap_pollard_ci,
    change_point,
    cluster_bootstrap_diff,
    group_pollard,
    split_half_reliability,
    team_home_advantage,
    team_season_home_advantage,
    within_team_season,
)


def _df(rows):
    return pd.DataFrame(
        rows, columns=["season", "home_team", "away_team", "home_points", "away_points"]
    )


def test_bootstrap_pollard_ci_todos_vitorias_casa():
    d = _df([(2019, "A", "B", 3, 0)] * 10)
    lo, hi = bootstrap_pollard_ci(d, n=200, seed=1)
    assert (lo, hi) == (100.0, 100.0)


def test_bootstrap_pollard_ci_vazio():
    assert bootstrap_pollard_ci(_df([]), n=10, seed=1) == (None, None)


def test_bootstrap_pollard_ci_reprodutivel():
    d = _df([(2019, "A", "B", 3, 0), (2019, "C", "D", 0, 3), (2019, "E", "F", 1, 1)])
    assert bootstrap_pollard_ci(d, n=200, seed=7) == bootstrap_pollard_ci(d, n=200, seed=7)


def test_annual_pollard_ci_duas_temporadas():
    d = _df([(2006, "A", "B", 3, 0)] * 5 + [(2007, "A", "B", 0, 3)] * 5)
    out = annual_pollard_ci(d, n=100, seed=1).set_index("season")
    assert list(out.columns) == ["n", "pollard", "lo", "hi"]
    assert out.loc[2006, "pollard"] == 100.0
    assert out.loc[2007, "pollard"] == 0.0
    assert out.loc[2006, "n"] == 5


def test_cluster_bootstrap_diff_pre_pos():
    d = _df(
        [(2006, "A", "B", 3, 0)] * 5
        + [(2007, "A", "B", 3, 0)] * 5
        + [(2010, "A", "B", 0, 3)] * 5
        + [(2011, "A", "B", 0, 3)] * 5
    )
    r = cluster_bootstrap_diff(d, d.season < 2009, d.season >= 2010, n=100, seed=1)
    assert (r["a"], r["b"], r["diff"]) == (100.0, 0.0, 100.0)
    assert (r["lo"], r["hi"]) == (100.0, 100.0)


def test_change_point_encontra_quebra():
    d = _df(
        [(2006, "A", "B", 3, 0)]
        + [(2007, "A", "B", 3, 0)]
        + [(2008, "A", "B", 3, 0)]
        + [(2009, "A", "B", 3, 0)]
        + [(2010, "A", "B", 0, 3)]
        + [(2011, "A", "B", 0, 3)]
        + [(2012, "A", "B", 0, 3)]
    )
    r = change_point(d)
    assert r["cut"] == 2010
    assert (r["pre"], r["post"], r["diff"]) == (100.0, 0.0, 100.0)
    assert r["sse"] == pytest.approx(0.0)


def test_group_pollard_conta_e_calcula():
    d = _df([(2019, "A", "B", 3, 0)] * 3 + [(2019, "A", "B", 0, 3)] * 3)
    grupos = pd.Series(["A"] * 3 + ["B"] * 3, index=d.index)
    out = group_pollard(d, grupos, n=100, seed=1).set_index("grupo")
    assert out.loc["A", "n"] == 3 and out.loc["A", "pollard"] == 100.0
    assert out.loc["B", "n"] == 3 and out.loc["B", "pollard"] == 0.0


def test_group_pollard_ignora_ausente_e_vazio():
    d = _df([(2019, "A", "B", 3, 0)] * 2)
    grupos = pd.Series([None, None], index=d.index)
    out = group_pollard(d, grupos, n=20, seed=1)
    assert out.empty
    assert list(out.columns) == ["grupo", "n", "pollard", "lo", "hi"]


def test_team_home_advantage_separa_casa_e_fora():
    d = _df([
        (2019, "A", "B", 3, 0),
        (2019, "A", "C", 3, 0),
        (2019, "B", "A", 1, 1),
        (2019, "C", "A", 1, 1),
    ])
    out = team_home_advantage(d, n=100, seed=1).set_index("team")
    assert out.loc["A", "home_ppg"] == 3.0
    assert out.loc["A", "away_ppg"] == 1.0
    assert out.loc["A", "ha"] == 2.0
    assert out.loc["A", "n"] == 4
    assert out.loc["B", "ha"] == 1.0


def test_within_team_season_desvio_da_media():
    d = _df([(2019, "A", "B", 3, 0), (2019, "A", "C", 0, 3)])
    grupos = pd.Series(["X", "Y"], index=d.index)
    out = within_team_season(d, grupos).set_index("grupo")
    assert out.loc["X", "mean_deviation"] == pytest.approx(1.5)
    assert out.loc["Y", "mean_deviation"] == pytest.approx(-1.5)
    assert out.loc["X", "n"] == 1


def test_within_team_season_media_inclui_partidas_sem_grupo():
    d = _df([
        (2019, "A", "B", 3, 0),
        (2019, "A", "C", 0, 3),
        (2019, "A", "D", 3, 0),
    ])
    grupos = pd.Series(["X", None, "X"], index=d.index)
    out = within_team_season(d, grupos).set_index("grupo")
    # média da equipe-temporada = (3 + 0 + 3) / 3 = 2; X = 3 -> desvio +1
    assert out.loc["X", "mean_deviation"] == pytest.approx(1.0)
    assert out.loc["X", "n"] == 2


def test_team_season_home_advantage_e_split_half():
    rows = []
    for i, team in enumerate(["A", "B", "C", "D"]):
        base = i * 0.5
        for season in range(2006, 2016):
            rows.append((season, team, base + 0.1 * (season - 2006)))
    ts = pd.DataFrame(rows, columns=["season", "team", "ha"])
    r = split_half_reliability(ts)
    assert r == pytest.approx(1.0)


def test_team_season_home_advantage_usa_pontos():
    d = _df([
        (2019, "A", "B", 3, 0),
        (2019, "B", "A", 1, 1),
    ])
    ts = team_season_home_advantage(d)
    a = ts[ts.team == "A"].iloc[0]
    assert a["home_ppg"] == 3.0
    assert a["away_ppg"] == 1.0
    assert a["ha"] == 2.0


@pytest.mark.integration
def test_build_outputs_cobre_a_base_real():
    from pathlib import Path

    from analyze_context import build_outputs

    base = Path(__file__).resolve().parent.parent / "data" / "processed" / "matches_processed.csv"
    if not base.exists():
        pytest.skip("rode scripts/build_processed.py")
    df, tab5, tab6, payload = build_outputs()
    assert len(df) == 7219
    assert payload["geral"]["n"] == 7219
    assert payload["quebra"]["cut"] == 2019
    assert len(tab6) == 43
    for variavel in ("Clássico", "Distância", "Mesmo estado", "Estádio",
                     "Força na tabela", "Era", "Pandemia"):
        assert tab5.loc[tab5["variavel"] == variavel, "n"].sum() == 7219
    assert tab5.loc[tab5["variavel"] == "Descanso", "n"].sum() == 7188
