#!/usr/bin/env python3
"""Exporta a Tabela 1 (indicadores por temporada) em Markdown."""
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
TAB = RAIZ / "figuras" / "tab1_indicadores_temporada.csv"

COLUNAS = {
    "season": "Temporada",
    "n": "n",
    "p_home": "% V mandante",
    "p_draw": "% Empates",
    "p_away": "% V visitante",
    "avg_home_goals": "Gols casa",
    "avg_away_goals": "Gols fora",
    "goal_diff": "Dif. gols",
    "home_points": "Pontos casa",
    "away_points": "Pontos fora",
    "pollard": "Pollard",
}


def main() -> None:
    df = pd.read_csv(TAB).sort_values("season")
    cabecalho = list(COLUNAS.values())
    print("| " + " | ".join(cabecalho) + " |")
    print("|" + "|".join(["---"] + ["---:"] * (len(cabecalho) - 1)) + "|")
    for _, linha in df.iterrows():
        valores = [str(int(linha["season"])), str(int(linha["n"]))]
        for c in ("p_home", "p_draw", "p_away", "avg_home_goals", "avg_away_goals",
                  "goal_diff", "home_points", "away_points", "pollard"):
            valores.append(f"{linha[c]:.2f}".replace(".", ","))
        print("| " + " | ".join(valores) + " |")


if __name__ == "__main__":
    main()
