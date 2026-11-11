#!/usr/bin/env python3
"""Validação da integridade da base: o campeão calculado por temporada
confere com o campeão oficial? (Sprint 9)"""
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


def main():
    df = pd.read_csv(RAIZ / "data" / "processed" / "matches_processed.csv")
    erros = 0
    for ano, esp in ESPERADO.items():
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
    print("RESULTADO:", "PASS — 19/19 campeões" if erros == 0 else f"{erros} DIVERGÊNCIAS")
    return erros


if __name__ == "__main__":
    raise SystemExit(main())
