#!/usr/bin/env python3
"""Resumo exploratório da base externa (público/arbitragem).

Lê data/external/joined_context.csv (gerado por scripts/join_external.py)
e imprime:
  - cobertura por temporada;
  - correlação de Spearman entre público e vantagem casa−fora;
  - correlação entre público e saldo de gols;
  - diferença de faltas mandante−visitante e sua correlação com público.

Nada aqui é causal; é um diagnóstico para decidir se vale incorporar as
variáveis ao TCC.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from associations import team_season_features

RAIZ = Path(__file__).resolve().parent.parent
BASE = RAIZ / "data" / "processed" / "matches_processed.csv"
JUNTO = RAIZ / "data" / "external" / "joined_context.csv"
SAIDA = RAIZ / "data" / "external" / "external_summary.json"


def spearman(a: pd.Series, b: pd.Series) -> float | None:
    par = pd.DataFrame({"a": a, "b": b}).dropna()
    if len(par) < 3:
        return None
    return float(par["a"].rank().corr(par["b"].rank()))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=BASE)
    parser.add_argument("--junto", type=Path, default=JUNTO)
    parser.add_argument("--out", type=Path, default=SAIDA)
    args = parser.parse_args(argv)

    base = pd.read_csv(args.base)
    junto = pd.read_csv(args.junto)

    # Público médio por equipe-temporada (só jogos em casa).
    publico = junto.groupby(["season", "home_team"])["publico"].mean().rename("avg_publico")
    publico.index = publico.index.set_names(["season", "team"])
    ts = team_season_features(base).set_index(["season", "team"]).join(publico)

    junto["goal_diff"] = junto["home_goals"] - junto["away_goals"]
    junto["foul_diff"] = junto["faltas_mandante"] - junto["faltas_visitante"]

    resumo = {
        "cobertura": {
            str(int(s)): {
                "n": int(len(g)),
                "com_base_externa": int((g["_merge"] == "both").sum()),
                "publico": int(g["publico"].notna().sum()),
                "publico_zero": int((g["publico"] == 0).sum()),
                "arbitro": int(g["arbitro"].notna().sum()),
                "faltas": int(g["faltas_mandante"].notna().sum()),
            }
            for s, g in junto.groupby("season")
        },
        "equipe_temporada": {
            "n": int(len(ts)),
            "com_publico": int(ts["avg_publico"].notna().sum()),
            "spearman_ha_publico": spearman(ts["ha"], ts["avg_publico"]),
            "spearman_pts_publico": spearman(ts["pts"], ts["avg_publico"]),
        },
        "partida": {
            "n_publico": int(junto[["goal_diff", "publico"]].dropna().shape[0]),
            "spearman_gol_diff_publico": spearman(junto["goal_diff"], junto["publico"]),
            "n_faltas": int(junto[["foul_diff", "publico"]].dropna().shape[0]),
            "media_faltas_casa_menos_fora": float(junto["foul_diff"].mean()),
            "spearman_faltas_publico": spearman(junto["foul_diff"], junto["publico"]),
        },
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(resumo, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    print(json.dumps(resumo, ensure_ascii=False, indent=2))
    print(f"-> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
