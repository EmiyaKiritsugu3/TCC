#!/usr/bin/env python3
"""Validação da integridade da base: o campeão calculado por temporada
confere com o campeão oficial? (Sprint 9)"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

ESPERADO = {
    2006: "Sao Paulo", 2007: "Sao Paulo", 2008: "Sao Paulo",
    2009: "Flamengo", 2010: "Fluminense", 2011: "Corinthians",
    2012: "Fluminense", 2013: "Cruzeiro", 2014: "Cruzeiro",
    2015: "Corinthians", 2016: "Palmeiras", 2017: "Corinthians",
    2018: "Palmeiras", 2019: "Flamengo", 2020: "Flamengo",
    2021: "Atletico-MG", 2022: "Palmeiras", 2023: "Palmeiras",
    2024: "Botafogo-RJ",
}

RAIZ = Path(__file__).resolve().parent.parent


def tabela(df):
    """Classificação: pontos, vitórias, saldo (critérios CBF, nesta ordem)."""
    h = df.groupby("home_team").agg(pts_h=("home_points", "sum"),
                                    v_h=("result", lambda s: (s == "H").sum()),
                                    gp_h=("home_goals", "sum"),
                                    gc_h=("away_goals", "sum"))
    a = df.groupby("away_team").agg(pts_a=("away_points", "sum"),
                                    v_a=("result", lambda s: (s == "A").sum()),
                                    gp_a=("away_goals", "sum"),
                                    gc_a=("home_goals", "sum"))
    t = pd.DataFrame({"pts": h["pts_h"].add(a["pts_a"], fill_value=0),
                      "vit": h["v_h"].add(a["v_a"], fill_value=0),
                      "sg": (h["gp_h"] + a["gp_a"]) - (h["gc_h"] + a["gc_a"])})
    return t.sort_values(["pts", "vit", "sg"], ascending=False)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base", type=Path,
        default=RAIZ / "data" / "processed" / "matches_processed.csv",
        help="CSV processado a validar (padrão: base 2006–2024)",
    )
    args = parser.parse_args(argv)
    base = args.base if args.base.is_absolute() else RAIZ / args.base
    df = pd.read_csv(base)
    temporadas = [ano for ano in sorted(df["season"].unique()) if ano in ESPERADO]
    if not temporadas:
        print(f"nenhuma temporada esperada em {base}")
        return 1
    erros = 0
    for ano in temporadas:
        esp = ESPERADO[ano]
        g = df[df["season"] == ano]
        t = tabela(g)
        camp, pts = t.index[0], int(t.iloc[0]["pts"])
        vice_pts = int(t.iloc[1]["pts"])
        flag = "OK" if camp == esp else "DIVERGE"
        if camp != esp:
            erros += 1
        print(f"{ano}: {camp} ({pts} pts, vice {vice_pts}) esperado {esp}  {flag}")
        if pts == vice_pts:
            print(f"  AVISO: empate em pontos no topo em {ano} — checar desempate manual.")
    total = len(temporadas)
    print("RESULTADO:", f"PASS — {total}/{total} campeões" if erros == 0
          else f"{erros} DIVERGÊNCIAS em {total} temporadas")
    return erros


if __name__ == "__main__":
    raise SystemExit(main())
