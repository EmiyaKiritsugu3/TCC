"""Associações descritivas entre contexto e vantagem de casa.

Funções puras: recebem a base limpa e devolvem tabelas ou intervalos de
bootstrap. Nada aqui afirma causalidade; o objetivo é quantificar
diferenças e incerteza.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from metrics import pollard

COLUNAS_GRUPO = ["grupo", "n", "pollard", "lo", "hi"]


def _pontos(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    return (
        np.asarray(df["home_points"], dtype=float),
        np.asarray(df["away_points"], dtype=float),
    )


def _pollard_draws(home: np.ndarray, away: np.ndarray, rng: np.random.Generator,
                   n: int) -> np.ndarray | None:
    if len(home) == 0:
        return None
    idx = rng.integers(0, len(home), size=(n, len(home)))
    h = home[idx].sum(axis=1)
    a = away[idx].sum(axis=1)
    total = h + a
    if not (total > 0).any():
        return None
    return h[total > 0] / total[total > 0] * 100


def bootstrap_pollard_ci(df: pd.DataFrame, n: int = 2000,
                         seed: int = 42) -> tuple[float | None, float | None]:
    """IC 95% do Pollard por bootstrap de partidas (reamostragem com reposição)."""
    if df.empty:
        return None, None
    home, away = _pontos(df)
    draws = _pollard_draws(home, away, np.random.default_rng(seed), n)
    if draws is None or len(draws) == 0:
        return None, None
    lo, hi = np.percentile(draws, [2.5, 97.5])
    return float(lo), float(hi)


def annual_pollard_ci(df: pd.DataFrame, n: int = 2000,
                      seed: int = 42) -> pd.DataFrame:
    """Pollard anual com n e IC 95% por temporada."""
    linhas = []
    for season, grupo in df.groupby("season"):
        lo, hi = bootstrap_pollard_ci(grupo, n=n, seed=seed)
        linhas.append({
            "season": int(season),
            "n": int(len(grupo)),
            "pollard": pollard(grupo["home_points"].sum(), grupo["away_points"].sum()),
            "lo": lo,
            "hi": hi,
        })
    return pd.DataFrame(linhas, columns=["season", "n", "pollard", "lo", "hi"]).sort_values(
        "season").reset_index(drop=True)


def _cluster_draws(sub: pd.DataFrame, n: int,
                   rng: np.random.Generator) -> np.ndarray | None:
    """Reamostra temporadas inteiras e devolve um Pollard por reamostragem."""
    somas = sub.groupby("season")[["home_points", "away_points"]].sum()
    if somas.empty:
        return None
    valores = somas.to_numpy(dtype=float)
    idx = rng.integers(0, len(valores), size=(n, len(valores)))
    h = valores[idx, 0].sum(axis=1)
    a = valores[idx, 1].sum(axis=1)
    total = h + a
    if not (total > 0).any():
        return None
    return h[total > 0] / total[total > 0] * 100


def cluster_bootstrap_diff(df: pd.DataFrame, mask_a: pd.Series,
                           mask_b: pd.Series, n: int = 3000,
                           seed: int = 42) -> dict:
    """Diferença de Pollard entre dois recortes, com temporada como cluster.

    Reamostra temporadas dentro de cada recorte, preservando a dependência
    entre partidas da mesma temporada.
    """
    a, b = df.loc[mask_a], df.loc[mask_b]
    if a.empty or b.empty:
        return {"a": None, "b": None, "diff": None, "lo": None, "hi": None}
    rng = np.random.default_rng(seed)
    da = _cluster_draws(a, n, rng)
    db = _cluster_draws(b, n, rng)
    if da is None or db is None:
        return {"a": None, "b": None, "diff": None, "lo": None, "hi": None}
    diff = da - db
    lo, hi = np.percentile(diff, [2.5, 97.5])
    a_p = pollard(a["home_points"].sum(), a["away_points"].sum())
    b_p = pollard(b["home_points"].sum(), b["away_points"].sum())
    return {"a": a_p, "b": b_p, "diff": a_p - b_p,
            "lo": float(lo), "hi": float(hi),
            "n_clusters": [int(a["season"].nunique()), int(b["season"].nunique())]}


def _annual_pollard(df: pd.DataFrame) -> pd.Series:
    return (df.groupby("season")[["home_points", "away_points"]].sum()
            .apply(lambda r: pollard(r["home_points"], r["away_points"]), axis=1))


def change_point(df: pd.DataFrame, minimo: int = 3) -> dict:
    """Ponto de quebra que minimiza a soma de quadrados dos dois segmentos."""
    y = _annual_pollard(df).dropna()
    if len(y) < 2 * minimo:
        return {"cut": None, "pre": None, "post": None, "diff": None, "sse": None}
    anos, valores = y.index.to_numpy(), y.to_numpy(dtype=float)

    def _sse(segmento: np.ndarray) -> float:
        return float(((segmento - segmento.mean()) ** 2).sum())

    melhor = None
    for i in range(minimo, len(valores) - minimo + 1):
        sse = _sse(valores[:i]) + _sse(valores[i:])
        if melhor is None or sse < melhor[0]:
            melhor = (sse, i)
    sse, i = melhor
    pre, post = float(valores[:i].mean()), float(valores[i:].mean())
    return {"cut": int(anos[i]), "pre": pre, "post": post,
            "diff": pre - post, "sse": sse}


def group_pollard(df: pd.DataFrame, groups: pd.Series, n: int = 2000,
                  seed: int = 42) -> pd.DataFrame:
    """Pollard, n e IC 95% para cada grupo de uma variável contextual."""
    grupos = pd.Series(groups, index=df.index)
    validos = grupos.notna()
    if not validos.any():
        return pd.DataFrame(columns=COLUNAS_GRUPO)
    linhas = []
    for nome in sorted(grupos[validos].unique()):
        sub = df.loc[validos & (grupos == nome)]
        lo, hi = bootstrap_pollard_ci(sub, n=n, seed=seed)
        linhas.append({"grupo": nome, "n": int(len(sub)),
                       "pollard": pollard(sub["home_points"].sum(),
                                          sub["away_points"].sum()),
                       "lo": lo, "hi": hi})
    return pd.DataFrame(linhas, columns=COLUNAS_GRUPO)


def team_season_home_advantage(df: pd.DataFrame) -> pd.DataFrame:
    """Pontos por jogo em casa e fora por equipe-temporada (mesmos adversários)."""
    casa = (df.groupby(["season", "home_team"])
            .agg(home_n=("home_points", "size"), home_ppg=("home_points", "mean")))
    fora = (df.groupby(["season", "away_team"])
            .agg(away_n=("away_points", "size"), away_ppg=("away_points", "mean")))
    casa.index = casa.index.set_names(["season", "team"])
    fora.index = fora.index.set_names(["season", "team"])
    out = casa.join(fora, how="outer").reset_index()
    out["home_n"] = out["home_n"].fillna(0).astype(int)
    out["away_n"] = out["away_n"].fillna(0).astype(int)
    # Sem um dos lados, a diferença casa−fora é indefinida (NaN), não zero.
    out["ha"] = out["home_ppg"] - out["away_ppg"]
    return out[["season", "team", "home_n", "away_n", "home_ppg", "away_ppg", "ha"]]


def team_home_advantage(df: pd.DataFrame, n: int = 2000,
                        seed: int = 42) -> pd.DataFrame:
    """Vantagem casa−fora por equipe, com IC 95% por bootstrap."""
    linhas = []
    rng = np.random.default_rng(seed)
    for team, grupo in df.groupby("home_team"):
        casa = grupo["home_points"].to_numpy(dtype=float)
        fora = df.loc[df["away_team"] == team, "away_points"].to_numpy(dtype=float)
        if len(casa) == 0 or len(fora) == 0:
            continue
        idx_c = rng.integers(0, len(casa), size=(n, len(casa)))
        idx_f = rng.integers(0, len(fora), size=(n, len(fora)))
        dif = casa[idx_c].mean(axis=1) - fora[idx_f].mean(axis=1)
        lo, hi = np.percentile(dif, [2.5, 97.5])
        linhas.append({
            "team": team,
            "n": int(len(casa) + len(fora)),
            "home_ppg": float(casa.mean()),
            "away_ppg": float(fora.mean()),
            "ha": float(casa.mean() - fora.mean()),
            "lo": float(lo), "hi": float(hi),
        })
    return (pd.DataFrame(linhas, columns=["team", "n", "home_ppg", "away_ppg",
                                          "ha", "lo", "hi"])
            .sort_values("ha", ascending=False).reset_index(drop=True))


def within_team_season(df: pd.DataFrame, groups: pd.Series,
                       outcome: str = "home_points") -> pd.DataFrame:
    """Desvio médio do resultado em relação à média da equipe-temporada.

    Controla a força da equipe na temporada: cada partida é comparada com a
    média do próprio clube naquela temporada.
    """
    d = df.copy()
    d["_grupo"] = pd.Series(groups, index=df.index)
    # A média da equipe-temporada usa TODAS as partidas do clube, inclusive
    # aquelas sem grupo (ex.: estreia sem descanso anterior).
    d["_media"] = d.groupby(["season", "home_team"])[outcome].transform("mean")
    d = d[d["_grupo"].notna()].copy()
    if d.empty:
        return pd.DataFrame(columns=["grupo", "n", "mean_deviation"])
    d["_desvio"] = d[outcome] - d["_media"]
    out = (d.groupby("_grupo")
           .agg(n=(outcome, "size"), mean_deviation=("_desvio", "mean"))
           .reset_index().rename(columns={"_grupo": "grupo"}))
    return out.sort_values("grupo").reset_index(drop=True)


COLUNAS_EQUIPE = [
    "ha", "home_ppg", "away_ppg", "pts", "rank", "home_win_pct",
    "away_win_pct", "home_goals_pg", "away_goals_pg", "avg_away_km",
    "usual_stadium_share", "season",
]

COLUNAS_PARTIDA = [
    "goal_diff", "travel_km", "rest_diff", "rank_diff", "derby",
    "usual_stadium", "var_era", "pandemia",
]


def team_season_features(df: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por equipe-temporada com desempenho e contexto.

    A vantagem casa−fora (`ha`) é a diferença entre pontos por jogo em casa
    e fora; `rank` usa pontos, vitórias e saldo, na mesma ordem da tabela.
    """
    obrigatorias = {"season", "home_team", "away_team", "home_goals",
                    "away_goals", "result", "home_points", "away_points"}
    faltam = sorted(obrigatorias - set(df.columns))
    if faltam:
        raise ValueError(f"Colunas obrigatórias ausentes: {faltam}")
    tem_travel = "travel_km" in df.columns
    tem_estadio = "usual_stadium" in df.columns
    linhas = []
    for (season, team), casa in df.groupby(["season", "home_team"]):
        fora = df[(df["season"] == season) & (df["away_team"] == team)]
        home_ppg = float(casa["home_points"].mean())
        away_ppg = float(fora["away_points"].mean())
        sg = float(
            (casa["home_goals"].sum() - casa["away_goals"].sum())
            + (fora["away_goals"].sum() - fora["home_goals"].sum())
        )
        linhas.append({
            "season": int(season),
            "team": team,
            "ha": home_ppg - away_ppg,
            "home_ppg": home_ppg,
            "away_ppg": away_ppg,
            "pts": int(casa["home_points"].sum() + fora["away_points"].sum()),
            "home_win_pct": float((casa["result"] == "H").mean() * 100),
            "away_win_pct": float((fora["result"] == "A").mean() * 100),
            "home_goals_pg": float(casa["home_goals"].mean()),
            "away_goals_pg": float(fora["away_goals"].mean()),
            "avg_away_km": float(fora["travel_km"].mean()) if tem_travel else np.nan,
            "usual_stadium_share": float(casa["usual_stadium"].mean()) if tem_estadio else np.nan,
            "wins": int((casa["result"] == "H").sum() + (fora["result"] == "A").sum()),
            "sg": sg,
        })
    out = pd.DataFrame(linhas)
    if out.empty:
        return pd.DataFrame(columns=["season", "team", *COLUNAS_EQUIPE])
    out["rank"] = 0
    for _, indices in out.groupby("season").groups.items():
        g = out.loc[indices]
        out.loc[indices, "rank"] = (
            g[["pts", "wins", "sg"]].apply(tuple, axis=1)
            .rank(method="min", ascending=False).astype(int)
        )
    colunas = ["season", "team", *[c for c in COLUNAS_EQUIPE if c != "season"]]
    return out[colunas].sort_values(["season", "rank"]).reset_index(drop=True)


def match_features(df: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por partida com desfecho e variáveis contextuais numéricas."""
    obrigatorias = {"home_goals", "away_goals", "travel_km", "home_rest",
                    "away_rest", "away_pos_before", "home_pos_before",
                    "derby", "usual_stadium", "var_era", "pandemia"}
    faltam = sorted(obrigatorias - set(df.columns))
    if faltam:
        raise ValueError(f"Colunas obrigatórias ausentes: {faltam}")
    return pd.DataFrame({
        "goal_diff": df["home_goals"] - df["away_goals"],
        "travel_km": df["travel_km"],
        "rest_diff": df["home_rest"] - df["away_rest"],
        "rank_diff": df["away_pos_before"] - df["home_pos_before"],
        "derby": df["derby"].astype(int),
        "usual_stadium": df["usual_stadium"].astype(int),
        "var_era": df["var_era"].astype(int),
        "pandemia": df["pandemia"].astype(int),
    })[COLUNAS_PARTIDA]


def correlation_matrix(df: pd.DataFrame, method: str = "spearman",
                       min_periods: int = 30) -> pd.DataFrame:
    """Matriz de correlação pairwise (Spearman por padrão)."""
    numericas = df.select_dtypes(include="number")
    if numericas.shape[1] < 2:
        raise ValueError("A matriz de correlação precisa de ao menos duas variáveis numéricas")
    if method == "spearman":
        # Spearman = Pearson sobre os ranks; evita depender de scipy.
        numericas = numericas.rank()
        method = "pearson"
    return numericas.corr(method=method, min_periods=min_periods)


def correlation_with(df: pd.DataFrame, target: str, method: str = "spearman",
                     min_periods: int = 30) -> pd.DataFrame:
    """Correlação de cada variável com um alvo, com n pairwise."""
    numericas = df.select_dtypes(include="number")
    if target not in numericas.columns:
        raise ValueError(f"Alvo ausente ou não numérico: {target!r}")
    linhas = []
    for coluna in numericas.columns:
        if coluna == target:
            continue
        par = numericas[[target, coluna]].dropna()
        n = int(len(par))
        if n >= min_periods and method == "spearman":
            par = par.rank()
        rho = (float(par[target].corr(par[coluna]))
               if n >= min_periods else None)
        linhas.append({"variavel": coluna, "rho": rho, "n": n})
    out = pd.DataFrame(linhas, columns=["variavel", "rho", "n"])
    out["rho"] = pd.to_numeric(out["rho"], errors="coerce")
    out["_abs"] = out["rho"].abs()
    return (out.sort_values("_abs", ascending=False, na_position="last")
            .drop(columns="_abs").reset_index(drop=True))


def split_half_reliability(team_season_df: pd.DataFrame) -> float | None:
    """Correlação ítem-par entre temporadas ímpares e pares (HA por equipe).

    Usa apenas equipes com pelo menos 10 temporadas, para reduzir ruído.
    """
    if not {"season", "team", "ha"}.issubset(team_season_df.columns):
        raise ValueError("team_season_df precisa de season, team e ha")
    piv = team_season_df.pivot(index="team", columns="season", values="ha")
    if piv.shape[0] < 2 or piv.shape[1] < 10:
        return None
    sub = piv.dropna(thresh=10)
    if len(sub) < 2:
        return None
    impares = [s for s in sub.columns if int(s) % 2 == 1]
    pares = [s for s in sub.columns if int(s) % 2 == 0]
    if not impares or not pares:
        return None
    return float(sub[impares].mean(axis=1).corr(sub[pares].mean(axis=1)))
