"""Testes das funções de associação (bootstrap, grupos, equipe, nível)."""
import numpy as np
import pandas as pd
import pytest

from associations import (
    annual_pollard_ci,
    bootstrap_pollard_ci,
    change_point,
    cluster_bootstrap_diff,
    correlation_matrix,
    correlation_with,
    group_pollard,
    match_features,
    split_half_reliability,
    team_home_advantage,
    team_season_features,
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
    primeira = bootstrap_pollard_ci(d, n=200, seed=7)
    segunda = bootstrap_pollard_ci(d, n=200, seed=7)
    assert primeira == segunda


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
    assert r["n_clusters"] == [2, 2]


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


def test_team_season_home_advantage_indefinido_sem_um_lado():
    d = _df([(2019, "A", "B", 3, 0)])
    ts = team_season_home_advantage(d)
    a = ts[ts.team == "A"].iloc[0]
    assert pd.isna(a["away_ppg"])
    assert pd.isna(a["ha"])


def test_team_season_features_calcula_ha_e_rank():
    d = pd.DataFrame({
        "season": [2019, 2019, 2019, 2019],
        "home_team": ["A", "B", "A", "B"],
        "away_team": ["B", "A", "B", "A"],
        "home_goals": [3, 1, 2, 0],
        "away_goals": [0, 1, 0, 2],
        "result": ["H", "D", "H", "A"],
        "home_points": [3, 1, 3, 0],
        "away_points": [0, 1, 0, 3],
        "travel_km": [100.0, 100.0, 200.0, 200.0],
        "usual_stadium": [True, True, False, True],
    })
    ts = team_season_features(d).set_index("team")
    a, b = ts.loc["A"], ts.loc["B"]
    assert a["home_ppg"] == 3.0 and a["away_ppg"] == 2.0
    assert a["ha"] == 1.0 and b["ha"] == 0.5
    assert a["pts"] == 10 and b["pts"] == 1
    assert a["rank"] == 1 and b["rank"] == 2
    assert a["home_win_pct"] == 100.0 and a["away_win_pct"] == 50.0
    assert a["home_goals_pg"] == 2.5 and a["away_goals_pg"] == 1.5
    assert a["avg_away_km"] == 150.0 and b["avg_away_km"] == 150.0
    assert a["usual_stadium_share"] == 0.5 and b["usual_stadium_share"] == 1.0


def test_match_features_deriva_colunas():
    d = pd.DataFrame({
        "home_goals": [2, 0],
        "away_goals": [0, 1],
        "travel_km": [100.0, 200.0],
        "home_rest": [5.0, 3.0],
        "away_rest": [3.0, 5.0],
        "away_pos_before": [5, 2],
        "home_pos_before": [2, 5],
        "derby": [False, True],
        "usual_stadium": [True, False],
        "var_era": [True, True],
        "pandemia": [False, True],
    })
    mf = match_features(d)
    assert mf["goal_diff"].tolist() == [2, -1]
    assert mf["rest_diff"].tolist() == [2.0, -2.0]
    assert mf["rank_diff"].tolist() == [3, -3]
    assert mf["derby"].tolist() == [0, 1]
    assert mf["usual_stadium"].tolist() == [1, 0]
    assert mf["pandemia"].tolist() == [0, 1]


def test_correlation_matrix_simetrica_e_diagonal():
    d = pd.DataFrame({
        "a": [1, 2, 3, 4],
        "b": [2, 4, 6, 8],
        "c": [4, 3, 2, 1],
        "d": [1, 1, 1, 1],
    })
    m = correlation_matrix(d, min_periods=2)
    assert m.loc["a", "b"] == pytest.approx(1.0)
    assert m.loc["a", "c"] == pytest.approx(-1.0)
    assert np.isnan(m.loc["a", "d"])
    assert m.loc["a", "a"] == pytest.approx(1.0)
    assert m.loc["b", "a"] == m.loc["a", "b"]


def test_correlation_with_ha_retorna_rho_e_n():
    d = pd.DataFrame({
        "ha": [1, 2, 3, 4],
        "forca": [1, 2, 3, 4],
        "viagem": [4, 3, 2, 1],
    })
    out = correlation_with(d, "ha", min_periods=2).set_index("variavel")
    assert out.loc["forca", "rho"] == pytest.approx(1.0)
    assert out.loc["viagem", "rho"] == pytest.approx(-1.0)
    assert out.loc["forca", "n"] == 4


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
    ts = team_season_features(df)
    mf = match_features(df)
    assert len(ts) == 380 and len(mf) == 7219
    assert correlation_matrix(ts).shape == (12, 12)
    assert correlation_matrix(mf).shape == (8, 8)
    for variavel in ("Clássico", "Distância", "Mesmo estado", "Estádio",
                     "Força na tabela", "Era", "Pandemia"):
        assert tab5.loc[tab5["variavel"] == variavel, "n"].sum() == 7219
    assert tab5.loc[tab5["variavel"] == "Descanso", "n"].sum() == 7025
