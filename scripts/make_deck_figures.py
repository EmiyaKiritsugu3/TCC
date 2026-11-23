#!/usr/bin/env python3
"""Gera versões dos gráficos com tipografia maior para o deck.

As figuras do artigo continuam em `figuras/artigo_serie_pollard.png` e
`figuras/fig13_cartoes.png`; estas versões são só para projeção.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
FIG = RAIZ / "figuras"

VERDE = "#0B3D2E"
VERDE_CLARO = "#6A994E"
TERRA = "#C8553D"
CINZA = "#5F655E"


def serie_pollard() -> None:
    t = pd.read_csv(FIG / "tab_artigo_temporadas.csv").sort_values("season")
    pre = t.loc[t.season.between(2013, 2018), "pollard"].mean()
    pos = t.loc[t.season.between(2019, 2024), "pollard"].mean()

    fig, ax = plt.subplots(figsize=(8.0, 4.4), dpi=220)
    ax.fill_between(t["season"], t["lo"], t["hi"], color="#1f77b4",
                    alpha=0.16, linewidth=0, label="IC 95% (bootstrap)")
    ax.plot(t["season"], t["pollard"], marker="o", color=VERDE,
            linewidth=2.2, markersize=5, label="Pollard")
    ax.axhline(50, color=CINZA, linestyle="--", linewidth=1.1)
    ax.hlines(pre, 2013, 2018.5, color=TERRA, linestyle="--", linewidth=1.6,
              label=f"Média 2013–2018 ({pre:.1f}%)".replace(".", ","))
    ax.hlines(pos, 2018.5, 2024, color=VERDE_CLARO, linestyle="--",
              linewidth=1.6, label=f"Média 2019–2024 ({pos:.1f}%)".replace(".", ","))
    ax.axvline(2018.5, color=CINZA, linestyle=":", linewidth=1.1)
    ax.annotate("quebra\n2019", xy=(2019, pos + 1.0), xytext=(2020.0, 71.2),
                fontsize=11, color=CINZA, ha="left", va="center",
                arrowprops=dict(arrowstyle="-", color=CINZA, lw=0.8))
    ax.set_xlim(2012.5, 2024.5)
    ax.set_xticks([2013, 2015, 2017, 2019, 2021, 2024])
    ax.set_ylim(48, 73)
    ax.set_xlabel("Temporada", fontsize=14)
    ax.set_ylabel("Índice de Pollard (%)", fontsize=14)
    ax.tick_params(axis="both", labelsize=12)
    ax.grid(alpha=0.25)
    ax.text(2012.7, 50.6, "50%", fontsize=9, color=CINZA, va="bottom")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.20), ncol=2,
              frameon=False, fontsize=11.2, handlelength=1.8,
              columnspacing=1.4)
    fig.tight_layout()
    fig.savefig(FIG / "deck_serie_pollard.png", bbox_inches="tight",
                facecolor="white")
    plt.close(fig)


def cartoes() -> None:
    t = pd.read_csv(FIG / "tab_cartoes.csv").sort_values("season")
    fig, ax = plt.subplots(figsize=(7.6, 4.2), dpi=220)
    ax.fill_between(t["season"], t["amarelos_lo"], t["amarelos_hi"],
                    color="#1f77b4", alpha=0.16, linewidth=0,
                    label="IC 95% (bootstrap)")
    ax.plot(t["season"], t["amarelos_diff"], marker="o", color=VERDE,
            linewidth=2.2, markersize=5, label="Diferença casa−fora")
    ax.axhline(0, color=CINZA, linestyle="--", linewidth=1.1)
    ax.axvspan(2019.5, 2020.5, color=TERRA, alpha=0.10, linewidth=0)
    ax.annotate("2020\nsem torcida", xy=(2020, 0.16), xytext=(2020.2, 0.26),
                fontsize=10, color=TERRA, ha="left", va="center")
    ax.set_xlim(2012.5, 2024.5)
    ax.set_xticks([2013, 2015, 2017, 2019, 2021, 2024])
    ax.set_xlabel("Temporada", fontsize=14)
    ax.set_ylabel("Cartões amarelos por jogo\n(casa − fora)", fontsize=12)
    ax.tick_params(axis="both", labelsize=12)
    ax.grid(alpha=0.25)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=2,
              frameon=False, fontsize=11.2, handlelength=1.8,
              columnspacing=1.4)
    fig.tight_layout()
    fig.savefig(FIG / "deck_cartoes.png", bbox_inches="tight",
                facecolor="white")
    plt.close(fig)


def main() -> None:
    serie_pollard()
    cartoes()
    print("figuras do deck geradas em figuras/deck_*.png")


if __name__ == "__main__":
    main()
