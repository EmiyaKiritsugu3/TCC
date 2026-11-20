#!/usr/bin/env python3
"""Análise descritiva das fontes externas de público e arbitragem.

Lê a base limpa `data/external/context_clean.csv` (gerada por
`scripts/build_external.py`) e produz:

  - cobertura por temporada;
  - público médio por temporada;
  - índice de Pollard por blocos (pré-2019, 2019, 2020, 2021, 2022–2024);
  - associação entre público e vantagem casa−fora, por equipe-temporada;
  - associação dentro de equipe-temporada, com e sem controle pela força
    pré-jogo do adversário;
  - comparação acima/abaixo da mediana de público da equipe-temporada;
  - descrição da arbitragem (cobertura e heterogeneidade bruta).

Nada aqui é causal. O objetivo é diagnosticar se as variáveis externas
acrescentam informação ou apenas repetem força do clube e contexto.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from associations import (
    bootstrap_pollard_ci,
    correlation_matrix,
    correlation_with,
    team_season_features,
)
from context import build_context_frame
from metrics import pollard

RAIZ = Path(__file__).resolve().parent.parent
BASE = RAIZ / "data" / "processed" / "matches_processed.csv"
LIMPO = RAIZ / "data" / "external" / "context_clean.csv"
SAIDA = RAIZ / "data" / "external" / "external_summary.json"


def spearman(a: pd.Series, b: pd.Series) -> float | None:
    par = pd.DataFrame({"a": a, "b": b}).dropna()
    if len(par) < 3:
        return None
    return float(par["a"].rank().corr(par["b"].rank()))


def partial_spearman(x: pd.Series, y: pd.Series, z: pd.Series) -> tuple[float | None, int]:
    """Spearman parcial: correlação dos resíduos de x e y em z (ranks)."""
    q = pd.DataFrame({"x": x, "y": y, "z": z}).dropna().rank()
    if len(q) < 3:
        return None, len(q)
    rx, ry, rz = q["x"] - q["x"].mean(), q["y"] - q["y"].mean(), q["z"] - q["z"].mean()
    denom = float((rz * rz).sum())
    if denom == 0:
        return None, len(q)
    bx = float((rx * rz).sum()) / denom
    by = float((ry * rz).sum()) / denom
    return float(np.corrcoef(rx - bx * rz, ry - by * rz)[0, 1]), len(q)


def _bloco(season: int) -> str:
    if 2007 <= season <= 2018:
        return "2007–2018"
    if season == 2019:
        return "2019"
    if season == 2020:
        return "2020 (portões fechados)"
    if season == 2021:
        return "2021 (retorno parcial)"
    if 2022 <= season <= 2024:
        return "2022–2024"
    return "2006 (sem público)"


def _resumo_blocos(d: pd.DataFrame) -> list[dict]:
    ordem = [
        "2006 (sem público)", "2007–2018", "2019",
        "2020 (portões fechados)", "2021 (retorno parcial)", "2022–2024",
    ]
    d = d.copy()
    d["bloco"] = d["season"].map(_bloco)
    linhas = []
    for nome in ordem:
        g = d[d["bloco"] == nome]
        if g.empty:
            continue
        lo, hi = bootstrap_pollard_ci(g, n=3000, seed=42)
        linhas.append({
            "bloco": nome,
            "n": int(len(g)),
            "publico_n": int(g["publico"].notna().sum()),
            "pollard": pollard(g["home_points"].sum(), g["away_points"].sum()),
            "lo": lo,
            "hi": hi,
            "saldo_medio": float((g["home_goals"] - g["away_goals"]).mean()),
            "pts_casa": float(g["home_points"].mean()),
            "vitoria_casa": float((g["home_goals"] > g["away_goals"]).mean()),
            "publico_medio": float(g["publico"].mean()) if g["publico"].notna().any() else None,
        })
    total = d[d["season"].between(2007, 2024)]
    lo, hi = bootstrap_pollard_ci(total, n=3000, seed=42)
    linhas.append({
        "bloco": "Total 2007–2024",
        "n": int(len(total)),
        "publico_n": int(total["publico"].notna().sum()),
        "pollard": pollard(total["home_points"].sum(), total["away_points"].sum()),
        "lo": lo,
        "hi": hi,
        "saldo_medio": float((total["home_goals"] - total["away_goals"]).mean()),
        "pts_casa": float(total["home_points"].mean()),
        "vitoria_casa": float((total["home_goals"] > total["away_goals"]).mean()),
        "publico_medio": float(total["publico"].mean()) if total["publico"].notna().any() else None,
    })
    return linhas


def _por_temporada(d: pd.DataFrame) -> list[dict]:
    linhas = []
    for season, g in d.groupby("season"):
        linhas.append({
            "season": int(season),
            "n": int(len(g)),
            "publico_n": int(g["publico"].notna().sum()),
            "publico_medio": float(g["publico"].mean()) if g["publico"].notna().any() else None,
            "publico_mediana": float(g["publico"].median()) if g["publico"].notna().any() else None,
            "publico_zero": int((g["publico"] == 0).sum()),
            "publico_zero_real": int(g["publico_zero_real"].sum()),
            "arbitro_n": int(g["arbitro"].notna().sum()),
            "faltas_n": int(g["faltas_mandante"].notna().sum()),
        })
    return linhas


def _equipe_temporada(base: pd.DataFrame, d: pd.DataFrame) -> dict:
    ts = team_season_features(base).set_index(["season", "team"])
    publico = (d.groupby(["season", "home_team"])["publico"]
               .agg(["mean", "std", "count"]).rename(
                   columns={"mean": "publico_medio", "std": "publico_sd", "count": "publico_n"}))
    publico.index = publico.index.set_names(["season", "team"])
    ts = ts.join(publico)
    ts["publico_cv"] = ts["publico_sd"] / ts["publico_medio"].replace(0, np.nan)

    def bloco(sub: pd.DataFrame) -> dict:
        return {
            "n": int(sub["publico_medio"].notna().sum()),
            "spearman_ha_publico": spearman(sub["ha"], sub["publico_medio"]),
            "spearman_pts_publico": spearman(sub["pts"], sub["publico_medio"]),
            "spearman_ha_publico_cv": spearman(sub["ha"], sub["publico_cv"]),
        }

    return {
        "todas": bloco(ts.reset_index()),
        "2007_2019": bloco(ts.loc[2007:2019].reset_index()),
        "2022_2024": bloco(ts.loc[2022:2024].reset_index()),
        "sem_2020_2021": bloco(ts.drop(index=[2020, 2021], level=0, errors="ignore").reset_index()),
        "matriz": correlation_matrix(
            ts.reset_index()[["ha", "home_ppg", "away_ppg", "pts", "rank",
                              "avg_away_km", "usual_stadium_share", "season",
                              "publico_medio", "publico_cv"]]
        ).round(4).to_dict(),
        "com_ha": correlation_with(
            ts.reset_index()[["ha", "home_ppg", "away_ppg", "pts", "rank",
                              "avg_away_km", "usual_stadium_share", "season",
                              "publico_medio", "publico_cv"]], "ha"
        ).round(4).to_dict(orient="records"),
    }


def _equipe_publico(d: pd.DataFrame) -> dict:
    """Quartis de público médio por equipe (mínimo de cinco temporadas)."""
    ts = team_season_features(d).set_index(["season", "team"])
    pub = d.groupby(["season", "home_team"])["publico"].mean().rename("publico_medio")
    pub.index = pub.index.set_names(["season", "team"])
    ts = ts.join(pub).reset_index()
    g = ts.dropna(subset=["publico_medio"]).groupby("team").agg(
        temporadas=("season", "nunique"),
        publico=("publico_medio", "mean"),
        ha=("ha", "mean"),
        pts=("pts", "mean"),
        home_ppg=("home_ppg", "mean"),
        away_ppg=("away_ppg", "mean"),
    ).reset_index()
    g = g[g["temporadas"] >= 5].copy()
    g["quartil"] = pd.qcut(
        g["publico"], 4, labels=["Q1 (menor)", "Q2", "Q3", "Q4 (maior)"]
    )
    quartis = []
    for nome, sub in g.groupby("quartil", observed=True):
        quartis.append({
            "quartil": str(nome),
            "times": int(len(sub)),
            "publico": float(sub["publico"].mean()),
            "pts": float(sub["pts"].mean()),
            "ha": float(sub["ha"].mean()),
            "home_ppg": float(sub["home_ppg"].mean()),
            "away_ppg": float(sub["away_ppg"].mean()),
        })
    return {
        "n_times": int(len(g)),
        "quartis": quartis,
        "correlacoes": {
            "publico_ha": spearman(g["publico"], g["ha"]),
            "publico_pts": spearman(g["publico"], g["pts"]),
            "publico_home_ppg": spearman(g["publico"], g["home_ppg"]),
            "publico_away_ppg": spearman(g["publico"], g["away_ppg"]),
        },
        "times": g.sort_values("publico", ascending=False)[
            ["team", "temporadas", "publico", "ha", "pts", "home_ppg", "away_ppg"]
        ].round(4).to_dict(orient="records"),
    }


def _partida(d: pd.DataFrame) -> dict:
    d = d.copy()
    d["goal_diff"] = d["home_goals"] - d["away_goals"]
    d["rank_diff"] = d["away_pos_before"] - d["home_pos_before"]
    d["publico_dev"] = d["publico"] - d.groupby(["season", "home_team"])["publico"].transform("mean")
    d["gd_dev"] = d["goal_diff"] - d.groupby(["season", "home_team"])["goal_diff"].transform("mean")

    def bloco(sub: pd.DataFrame) -> dict:
        rho = spearman(sub["goal_diff"], sub["publico"])
        parcial, n_parcial = partial_spearman(sub["publico_dev"], sub["gd_dev"], sub["rank_diff"])
        return {
            "n_publico": int(sub[["goal_diff", "publico"]].dropna().shape[0]),
            "spearman_gd_publico": rho,
            "n_parcial": n_parcial,
            "spearman_parcial_controle_rank": parcial,
        }

    # Acima/abaixo da mediana de público da própria equipe-temporada.
    d["mediana"] = d.groupby(["season", "home_team"])["publico"].transform("median")
    d["grupo"] = np.where(d["publico"] > d["mediana"], "acima",
                          np.where(d["publico"] < d["mediana"], "abaixo", "mediana"))
    g = d[d["grupo"] != "mediana"].groupby("grupo").agg(
        n=("goal_diff", "size"),
        publico=("publico", "mean"),
        opp_pos=("away_pos_before", "mean"),
        saldo=("goal_diff", "mean"),
        pts=("home_points", "mean"),
        vitoria=("home_points", lambda s: float((s == 3).mean())),
        rank_diff=("rank_diff", "mean"),
    ).reset_index()

    # Matriz de partida com as variáveis externas.
    matriz = d[["goal_diff", "publico", "publico_dev", "rank_diff",
                "travel_km", "derby", "usual_stadium", "var_era", "pandemia"]].copy()
    matriz["derby"] = matriz["derby"].astype(int)
    matriz["usual_stadium"] = matriz["usual_stadium"].astype(int)
    matriz["var_era"] = matriz["var_era"].astype(int)
    matriz["pandemia"] = matriz["pandemia"].astype(int)

    return {
        "todas": bloco(d),
        "2007_2019": bloco(d[d["season"].between(2007, 2019)]),
        "2022_2024": bloco(d[d["season"].between(2022, 2024)]),
        "sem_2020_2021": bloco(d[~d["season"].isin([2020, 2021])]),
        "acima_abaixo_mediana": g.round(3).to_dict(orient="records"),
        "matriz": correlation_matrix(matriz).round(4).to_dict(),
        "com_goal_diff": correlation_with(matriz, "goal_diff").round(4).to_dict(orient="records"),
    }


def _arbitragem(d: pd.DataFrame) -> dict:
    a = d.dropna(subset=["arbitro"]).copy()
    a["home_win"] = (a["home_goals"] > a["away_goals"]).astype(int)
    por_arbitro = a.groupby("arbitro").agg(
        n=("home_win", "size"),
        vitoria_casa=("home_win", "mean"),
        publico=("publico", "mean"),
    ).sort_values("n", ascending=False)
    com_amostra = por_arbitro[por_arbitro["n"] >= 40]
    return {
        "n_jogos": int(len(a)),
        "n_arbitros": int(por_arbitro.shape[0]),
        "jogos_por_arbitro_mediana": float(por_arbitro["n"].median()),
        "jogos_por_arbitro_max": int(por_arbitro["n"].max()),
        "taxa_vitoria_casa_geral": float(a["home_win"].mean()),
        "arbitros_com_40_jogos": int(len(com_amostra)),
        "taxa_vitoria_casa_min": float(com_amostra["vitoria_casa"].min()) if len(com_amostra) else None,
        "taxa_vitoria_casa_max": float(com_amostra["vitoria_casa"].max()) if len(com_amostra) else None,
        "top10_jogos": por_arbitro.head(10).round(3).reset_index().to_dict(orient="records"),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=BASE)
    parser.add_argument("--limpo", type=Path, default=LIMPO)
    parser.add_argument("--out", type=Path, default=SAIDA)
    args = parser.parse_args(argv)

    base = pd.read_csv(args.base)
    limpo = pd.read_csv(args.limpo)
    ctx = build_context_frame(base)
    d = ctx.merge(
        limpo[["match_id", "publico", "publico_zero_real", "publico_fonte",
               "arbitro", "arbitro_fonte", "faltas_mandante", "faltas_visitante"]],
        on="match_id", how="left",
    )
    if len(d) != len(ctx):
        raise SystemExit(f"junção alterou o número de linhas: {len(ctx)} -> {len(d)}")

    resumo = {
        "cobertura": _por_temporada(d),
        "blocos": _resumo_blocos(d),
        "equipe_temporada": _equipe_temporada(base, d),
        "equipe_publico": _equipe_publico(d),
        "partida": _partida(d),
        "arbitragem": _arbitragem(d),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(resumo, ensure_ascii=False, indent=2, default=str) + "\n",
                        encoding="utf-8")

    print(json.dumps({
        "blocos": resumo["blocos"],
        "equipe_temporada": {k: v for k, v in resumo["equipe_temporada"].items()
                             if k not in ("matriz", "com_ha")},
        "partida": {k: v for k, v in resumo["partida"].items()
                    if k not in ("matriz", "com_goal_diff")},
        "arbitragem": {k: v for k, v in resumo["arbitragem"].items()
                       if k != "top10_jogos"},
    }, ensure_ascii=False, indent=2, default=str))
    print(f"-> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
