#!/usr/bin/env python3
"""Figuras e indicadores do recorte 2013–2024 (artigo).

Saídas:
  figuras/artigo_serie_pollard.png
  figuras/artigo_publico_ha.png
  figuras/artigo_indicadores.csv
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from associations import (annual_pollard_ci, change_point, cluster_bootstrap_diff,
                          team_season_features)
from metrics import by_season, summarize

RAIZ = Path(__file__).resolve().parent.parent
BASE = RAIZ / "data" / "processed" / "matches_processed_2013_2024.csv"
CONTEXTO = RAIZ / "data" / "external" / "context_clean.csv"
FIG = RAIZ / "figuras"
AZUL, CINZA, VERMELHO = "#1f77b4", "#7f7f7f", "#d62728"

plt.rcParams.update({"font.size": 11, "axes.grid": True, "grid.alpha": 0.3,
                     "figure.figsize": (10, 5.2)})


def _serie(df: pd.DataFrame) -> dict:
    anual = annual_pollard_ci(df, n=4000)
    corte = change_point(df)
    diff = cluster_bootstrap_diff(df, df["season"].between(2013, 2018),
                                  df["season"].between(2019, 2024), n=5000)
    fig, ax = plt.subplots(figsize=(10, 5.4))
    ax.fill_between(anual["season"], anual["lo"], anual["hi"], color=AZUL,
                    alpha=0.18, label="IC 95% (bootstrap de partidas)")
    ax.plot(anual["season"], anual["pollard"], marker="o", color=AZUL)
    ax.axhline(50, color="black", linestyle="--", linewidth=1, label="50% (neutro)")
    ax.hlines(diff["a"], 2013, 2018.5, color=VERMELHO, linestyles="--",
              label="Média 2013–2018")
    ax.hlines(diff["b"], 2018.5, 2024, color=CINZA, linestyles="--",
              label="Média 2019–2024")
    ax.axvline(2018.5, color=CINZA, linestyle=":", linewidth=1)
    ax.text(2018.7, diff["a"] + 0.8, "VAR 2019", color=CINZA, fontsize=9)
    ax.set_xlabel("Temporada")
    ax.set_xticks(range(2013, 2025, 2))
    ax.set_ylabel("Índice de Pollard (%)")
    ax.legend(loc="lower left", fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(FIG / "artigo_serie_pollard.png", dpi=150)
    plt.close(fig)
    return {"anual": anual, "corte": corte, "nivel": diff}


def _publico() -> None:
    if not CONTEXTO.exists():
        print("context_clean.csv ausente; figura pública não gerada")
        return
    ext = pd.read_csv(CONTEXTO)
    ext = ext[ext["season"].between(2013, 2024)].copy()
    ts = team_season_features(ext)
    pub = ext.groupby(["season", "home_team"])["publico"].mean().rename("publico_medio")
    pub.index = pub.index.set_names(["season", "team"])
    ts = ts.join(pub, on=["season", "team"]).reset_index()
    d = ts.dropna(subset=["publico_medio"]).copy()
    if d.empty:
        print("sem público no recorte")
        return
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.2))
    paineis = [
        ("ha", "HA × público", "Vantagem casa−fora (pontos/jogo)"),
        ("pts", "Pontos médios × público", "Pontos médios por temporada"),
    ]
    for ax, (coluna, titulo, rotulo_y) in zip(axes, paineis):
        x = d["publico_medio"] / 1000
        y = d[coluna]
        ax.scatter(x, y, color=AZUL, alpha=0.55, s=18)
        coef = np.polyfit(x, y, 1)
        xs = np.linspace(float(x.min()), float(x.max()), 50)
        ax.plot(xs, np.polyval(coef, xs), color=CINZA, linewidth=1.5)
        rho = float(x.rank().corr(y.rank()))
        ax.set_title(f"{titulo} (ρ = {rho:.2f})", fontsize=10)
        ax.set_xlabel("Público médio (mil)")
        ax.set_ylabel(rotulo_y)
    fig.suptitle("Público médio, HA e pontos por equipe-temporada (2013–2024)",
                 fontsize=12)
    fig.tight_layout()
    fig.savefig(FIG / "artigo_publico_ha.png", dpi=150)
    plt.close(fig)


def _contexto(df: pd.DataFrame) -> None:
    from context import build_context_frame, grupos_contexto
    from associations import group_pollard
    ctx = build_context_frame(df)
    linhas = []
    for dim in ["Distância", "Clássico", "Estádio", "Força na tabela"]:
        g = group_pollard(ctx, grupos_contexto(ctx, dim), n=2000, seed=42)
        for r in g.itertuples():
            linhas.append({"dimensao": dim, "grupo": str(r.grupo), "n": int(r.n),
                           "pollard": float(r.pollard), "lo": float(r.lo),
                           "hi": float(r.hi)})
    pd.DataFrame(linhas).round(4).to_csv(FIG / "tab_artigo_contexto.csv", index=False)


def main() -> None:
    df = pd.read_csv(BASE)
    s = summarize(df)
    t = by_season(df).sort_values("season")
    dados = _serie(df)
    t = t.merge(dados["anual"][["season", "lo", "hi"]], on="season")
    t.to_csv(FIG / "tab_artigo_temporadas.csv", index=False)
    _publico()
    _contexto(df)
    print(f"n={len(df)}; pollard={s['pollard']:.2f}%")
    print("mudança de nível:", {k: (round(v, 3) if isinstance(v, float) else v)
                                for k, v in dados["nivel"].items()})
    print("ponto de quebra:", dados["corte"])


if __name__ == "__main__":
    main()
