"""Indicadores do TCC (seção 10 da spec). Funções puras sobre a base limpa."""
from __future__ import annotations

import pandas as pd

RESULT_HOME, RESULT_DRAW, RESULT_AWAY = "H", "D", "A"


def pollard(home_points: float, away_points: float) -> float | None:
    """Índice de Pollard: Ph/(Ph+Pv)*100. Denominador zero -> None (indefinido)."""
    total = home_points + away_points
    if total == 0:
        return None
    return home_points / total * 100


def summarize(df: pd.DataFrame) -> dict:
    """Indicadores agregados de um recorte. Recorte vazio -> n=0 e Nones (RF10)."""
    n = int(len(df))
    if n == 0:
        return {
            "n": 0, "p_home": None, "p_draw": None, "p_away": None,
            "avg_home_goals": None, "avg_away_goals": None,
            "goal_diff": None, "home_points": 0, "away_points": 0,
            "pollard": None,
        }
    for col in ("result", "home_goals", "away_goals", "home_points", "away_points"):
        if col not in df.columns:
            raise ValueError(f"Coluna obrigatória ausente: {col}")
    n_h = int((df["result"] == RESULT_HOME).sum())
    n_d = int((df["result"] == RESULT_DRAW).sum())
    n_a = int((df["result"] == RESULT_AWAY).sum())
    ph, pa = float(df["home_points"].sum()), float(df["away_points"].sum())
    return {
        "n": n,
        "p_home": n_h / n * 100,
        "p_draw": n_d / n * 100,
        "p_away": n_a / n * 100,
        "avg_home_goals": float(df["home_goals"].sum() / n),
        "avg_away_goals": float(df["away_goals"].sum() / n),
        "goal_diff": float((df["home_goals"] - df["away_goals"]).sum() / n),
        "home_points": ph,
        "away_points": pa,
        "pollard": pollard(ph, pa),
    }


def by_season(df: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por temporada com todos os indicadores + proporções."""
    if df.empty:
        return pd.DataFrame(columns=["season", "n", "p_home", "p_draw", "p_away",
                                      "avg_home_goals", "avg_away_goals", "goal_diff",
                                      "home_points", "away_points", "pollard"])
    rows = []
    for season, g in sorted(df.groupby("season"), key=lambda x: x[0]):
        s = summarize(g)
        s["season"] = int(season)
        rows.append(s)
    return pd.DataFrame(rows, columns=["season", "n", "p_home", "p_draw", "p_away",
                                       "avg_home_goals", "avg_away_goals", "goal_diff",
                                       "home_points", "away_points", "pollard"])


def team_season(df: pd.DataFrame, team: str, season: int) -> dict:
    """Desempenho de uma equipe numa temporada, separando casa e fora."""
    g = df[df["season"] == season]
    home = g[g["home_team"] == team]
    away = g[g["away_team"] == team]
    sh, sa = summarize(home), summarize(away)
    return {
        "team": team, "season": int(season),
        "home_n": sh["n"], "home_w": int((home["result"] == RESULT_HOME).sum()) if len(home) else 0,
        "home_d": int((home["result"] == RESULT_DRAW).sum()) if len(home) else 0,
        "home_l": int((home["result"] == RESULT_AWAY).sum()) if len(home) else 0,
        "home_points": int(sh["home_points"]),
        "away_n": sa["n"], "away_w": int((away["result"] == RESULT_AWAY).sum()) if len(away) else 0,
        "away_d": int((away["result"] == RESULT_DRAW).sum()) if len(away) else 0,
        "away_l": int((away["result"] == RESULT_HOME).sum()) if len(away) else 0,
        "away_points": int(sa["away_points"]),
    }
