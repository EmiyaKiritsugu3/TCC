#!/usr/bin/env python3
"""Gera as tabelas e o JSON da análise de contexto (caminho B do TCC).

Uso: .venv/bin/python scripts/analyze_context.py
Saídas: figuras/tab5_contexto.csv, figuras/tab6_equipes.csv,
figuras/tab7_correlacoes_equipe.csv, figuras/matriz_equipe.csv,
figuras/matriz_partida.csv e figuras/contexto.json.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

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
from context import build_context_frame
from metrics import pollard

RAIZ = Path(__file__).resolve().parent.parent
FIG = RAIZ / "figuras"
BASE = RAIZ / "data" / "processed" / "matches_processed.csv"


def _jsonable(obj):
    """Converte tipos numpy/pandas para JSON puro."""
    if isinstance(obj, dict):
        return {str(k): _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonable(v) for v in obj]
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    if obj is None:
        return None
    if isinstance(obj, float) and np.isnan(obj):
        return None
    return obj


def _grupo(df: pd.DataFrame, variavel: str, grupos: pd.Series,
           geral: float) -> pd.DataFrame:
    out = group_pollard(df, grupos, n=2000, seed=42)
    out.insert(0, "variavel", variavel)
    out["delta_geral"] = out["pollard"].apply(
        lambda valor: None if pd.isna(valor) else valor - geral
    )
    return out[["variavel", "grupo", "n", "pollard", "lo", "hi", "delta_geral"]]


def _distancia(df: pd.DataFrame) -> pd.Series:
    return pd.cut(
        df["travel_km"],
        bins=[-0.001, 500, 1500, float("inf")],
        labels=["Curta (<500 km)", "Média (500–1.499 km)", "Longa (≥1.500 km)"],
        right=False,
    )


def build_outputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    """Calcula a base contextual, as tabelas e o payload JSON."""
    bruto = pd.read_csv(BASE)
    df = build_context_frame(bruto)

    geral = pollard(df["home_points"].sum(), df["away_points"].sum())
    lo_geral, hi_geral = bootstrap_pollard_ci(df, n=3000, seed=42)

    anual = annual_pollard_ci(df, n=2000, seed=42)
    nivel_2019 = cluster_bootstrap_diff(df, df["season"] < 2019, df["season"] >= 2019,
                                        n=4000, seed=42)
    nivel_2006_16 = cluster_bootstrap_diff(
        df, df["season"] <= 2016, df["season"] >= 2022, n=4000, seed=42
    )
    quebra = change_point(df)

    grupos = {
        "derby": _grupo(df, "Clássico", np.where(
            df["derby"], "Clássico (mesma cidade)", "Não clássico"), geral),
        "distancia": _grupo(df, "Distância", _distancia(df), geral),
        "same_state": _grupo(df, "Mesmo estado", np.where(
            df["same_state"], "Mesmo estado", "Estado diferente"), geral),
        "estadio": _grupo(df, "Estádio", np.where(
            df["usual_stadium"], "Estádio habitual", "Outro estádio"), geral),
        "descanso": _grupo(df, "Descanso", df["rest_bucket"], geral),
        "forca": _grupo(df, "Força na tabela", df["table_bucket"], geral),
        "era": _grupo(df, "Era", np.where(
            df["season"] < 2019, "Pré-2019", "2019+"), geral),
        "pandemia": _grupo(df, "Pandemia", np.where(
            df["pandemia"], "Pandemia (2020–2021)", "Demais temporadas"), geral),
    }

    dentro = {
        "estadio": within_team_season(
            df, np.where(df["usual_stadium"], "Estádio habitual", "Outro estádio")
        ),
        "descanso": within_team_season(df, df["rest_bucket"]),
        "forca": within_team_season(df, df["table_bucket"]),
    }

    contrastes = {
        "derby_vs_nao": cluster_bootstrap_diff(df, df["derby"], ~df["derby"],
                                               n=4000, seed=42),
        "estadio_vs_outro": cluster_bootstrap_diff(
            df, df["usual_stadium"], ~df["usual_stadium"], n=4000, seed=42),
        "mesmo_estado_vs_diferente": cluster_bootstrap_diff(
            df, df["same_state"], ~df["same_state"], n=4000, seed=42),
        "favorito_vs_zebra": cluster_bootstrap_diff(
            df, df["table_bucket"].eq("favorito"), df["table_bucket"].eq("zebra"),
            n=4000, seed=42),
        "pandemia_vs_demais": cluster_bootstrap_diff(
            df, df["pandemia"], ~df["pandemia"], n=4000, seed=42),
    }

    equipe_temporada = team_season_home_advantage(df)
    equipes = team_home_advantage(df)
    longevas = equipes[equipes["n"] >= 190]
    confiabilidade = split_half_reliability(equipe_temporada)

    ts = team_season_features(df)
    mf = match_features(df)
    matriz_equipe = correlation_matrix(ts)
    matriz_partida = correlation_matrix(mf)
    com_ha = correlation_with(ts, "ha")
    com_gol_diff = correlation_with(mf, "goal_diff")

    tabela5 = pd.concat(
        [pd.DataFrame([{
            "variavel": "Geral", "grupo": "Período 2006–2024", "n": len(df),
            "pollard": geral, "lo": lo_geral, "hi": hi_geral, "delta_geral": 0.0,
        }])] + list(grupos.values()),
        ignore_index=True,
    )
    tabela6 = equipes.copy()

    payload = {
        "geral": {"n": int(len(df)), "pollard": geral, "lo": lo_geral, "hi": hi_geral},
        "anual": anual.to_dict(orient="records"),
        "nivel_2019": nivel_2019,
        "nivel_2006_2016_vs_2022_2024": nivel_2006_16,
        "quebra": quebra,
        "grupos": {k: v.to_dict(orient="records") for k, v in grupos.items()},
        "contrastes": contrastes,
        "dentro_equipe_temporada": {k: v.to_dict(orient="records") for k, v in dentro.items()},
        "equipes": {
            "confiabilidade_split_half": confiabilidade,
            "top5": equipes.head(5).to_dict(orient="records"),
            "bottom5": equipes.tail(5).to_dict(orient="records"),
            "top5_longevas": longevas.head(5).to_dict(orient="records"),
            "bottom5_longevas": longevas.tail(5).to_dict(orient="records"),
            "n_equipes": int(len(equipes)),
        },
        "correlacoes": {
            "metodo": "spearman",
            "equipe": {
                "n": int(len(ts)),
                "matriz": matriz_equipe.round(4).to_dict(),
                "com_ha": com_ha.round(4).to_dict(orient="records"),
            },
            "partida": {
                "n": int(len(mf)),
                "matriz": matriz_partida.round(4).to_dict(),
                "com_goal_diff": com_gol_diff.round(4).to_dict(orient="records"),
            },
        },
        "contagens": {
            "classicos": int(df["derby"].sum()),
            "estadio_habitual": int(df["usual_stadium"].sum()),
            "mesmo_estado": int(df["same_state"].sum()),
            "descanso_ausente": int(df["rest_bucket"].isna().sum()),
            "tabela_ausente": int(df["table_bucket"].isna().sum()),
        },
    }
    return df, tabela5, tabela6, payload


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    df, tabela5, tabela6, payload = build_outputs()
    tabela5.to_csv(FIG / "tab5_contexto.csv", index=False)
    tabela6.to_csv(FIG / "tab6_equipes.csv", index=False)
    pd.DataFrame(payload["correlacoes"]["equipe"]["com_ha"]).to_csv(
        FIG / "tab7_correlacoes_equipe.csv", index=False)
    pd.DataFrame(payload["correlacoes"]["equipe"]["matriz"]).to_csv(
        FIG / "matriz_equipe.csv")
    pd.DataFrame(payload["correlacoes"]["partida"]["matriz"]).to_csv(
        FIG / "matriz_partida.csv")
    (FIG / "contexto.json").write_text(
        json.dumps(_jsonable(payload), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    geral = payload["geral"]
    quebra = payload["quebra"]
    nivel_2019 = payload["nivel_2019"]
    print(f"partidas: {geral['n']}")
    print(f"geral: {geral['pollard']:.2f}% (IC 95%: {geral['lo']:.2f}–{geral['hi']:.2f})")
    print(f"quebra: {quebra['cut']} ({quebra['pre']:.2f}% -> {quebra['post']:.2f}%; "
          f"diferença {quebra['diff']:.2f} p.p.)")
    print(f"2019: {nivel_2019['a']:.2f}% vs {nivel_2019['b']:.2f}% "
          f"(diferença {nivel_2019['diff']:.2f} p.p.; "
          f"IC {nivel_2019['lo']:.2f}–{nivel_2019['hi']:.2f})")
    print(f"equipes: {payload['equipes']['n_equipes']}; "
          f"confiabilidade split-half: {payload['equipes']['confiabilidade_split_half']:.3f}")
    print(f"correlações: {payload['correlacoes']['equipe']['n']} equipe-temporada; "
          f"{payload['correlacoes']['partida']['n']} partidas")
    print("arquivos: tab5, tab6, tab7, matrizes e contexto.json")


if __name__ == "__main__":
    main()
