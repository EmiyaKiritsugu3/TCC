#!/usr/bin/env python3
"""Figuras finais da monografia (Sprint 2). PNG 150 DPI, rótulos em PT-BR."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from metrics import by_season, summarize

RAIZ = Path(__file__).resolve().parent.parent
FIG = RAIZ / "figuras"
plt.rcParams.update({"font.size": 11, "axes.grid": True, "grid.alpha": 0.3,
                     "figure.figsize": (10, 5.2)})

AZUL, CINZA, VERMELHO = "#1f77b4", "#7f7f7f", "#d62728"


def fig_distribuicao(s):
    fig, ax = plt.subplots()
    cats = ["Vitória mandante", "Empate", "Vitória visitante"]
    vals = [s["p_home"], s["p_draw"], s["p_away"]]
    bars = ax.bar(cats, vals, color=[AZUL, CINZA, VERMELHO])
    ax.set_ylabel("% de partidas")
    ax.set_ylim(0, max(vals) * 1.25)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 1, f"{v:.1f}%", ha="center")
    fig.tight_layout()
    fig.savefig(FIG / "fig1_distribuicao_geral.png", dpi=150)
    plt.close(fig)


def fig_pollard(t):
    fig, ax = plt.subplots()
    ax.axhline(50, color="black", linestyle="--", linewidth=1, label="50% (neutro)")
    ax.plot(t["season"], t["pollard"], marker="o", color=AZUL)
    ax.set_xlabel("Temporada")
    ax.set_xticks(range(2006, 2025, 2))
    ax.set_ylabel("Índice de Pollard (%)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIG / "fig2_pollard_temporadas.png", dpi=150)
    plt.close(fig)


def fig_resultados(t):
    fig, ax = plt.subplots()
    n = len(t)
    ax.bar(t["season"], t["p_home"], width=0.62, color=AZUL, label="Vit. mandante")
    ax.bar(t["season"], t["p_draw"], bottom=t["p_home"], width=0.62,
           color=CINZA, label="Empate")
    ax.bar(t["season"], t["p_away"], bottom=t["p_home"] + t["p_draw"], width=0.62,
           color=VERMELHO, label="Vit. visitante")
    ax.set_xlabel("Temporada")
    ax.set_xticks(range(2006, 2025, 2))
    ax.set_ylabel("% de partidas")
    ax.set_xlim(2005.4, 2024.6)
    ax.set_ylim(0, 100)
    # legenda FORA do plot (abaixo, 3 colunas) — não sobrepõe as barras
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), ncols=3, frameon=False)
    fig.tight_layout()
    fig.savefig(FIG / "fig3_resultados_temporadas.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def fig_gols(t):
    fig, ax = plt.subplots()
    ax.plot(t["season"], t["avg_home_goals"], marker="o", color=AZUL, label="Mandante")
    ax.plot(t["season"], t["avg_away_goals"], marker="o", color=VERMELHO, label="Visitante")
    ax.set_xlabel("Temporada")
    ax.set_xticks(range(2006, 2025, 2))
    ax.set_ylabel("Gols por partida (média)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIG / "fig4_gols_temporadas.png", dpi=150)
    plt.close(fig)


def main():
    FIG.mkdir(exist_ok=True)
    df = pd.read_csv(RAIZ / "data" / "processed" / "matches_processed.csv")
    s = summarize(df)
    t = by_season(df).sort_values("season")
    fig_distribuicao(s)
    fig_pollard(t)
    fig_resultados(t)
    fig_gols(t)
    t.round(2).to_csv(FIG / "tab1_indicadores_temporada.csv", index=False)
    print("figuras:", sorted(p.name for p in FIG.iterdir()))


if __name__ == "__main__":
    main()
