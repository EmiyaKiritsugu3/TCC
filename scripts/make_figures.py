#!/usr/bin/env python3
"""Figuras finais da monografia (Sprint 2). PNG 150 DPI, rótulos em PT-BR."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from analyze_context import build_outputs
from associations import team_season_features
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


def fig_serie_ic(anual: pd.DataFrame, nivel: dict):
    fig, ax = plt.subplots(figsize=(10, 5.4))
    ax.fill_between(anual["season"], anual["lo"], anual["hi"], color=AZUL,
                    alpha=0.18, label="IC 95% (bootstrap)")
    ax.plot(anual["season"], anual["pollard"], marker="o", color=AZUL)
    ax.axhline(50, color="black", linestyle="--", linewidth=1, label="50% (neutro)")
    ax.hlines(nivel["a"], 2006, 2018.5, color=VERMELHO, linestyles="--",
              label="Média 2006–2018")
    ax.hlines(nivel["b"], 2018.5, 2024, color=CINZA, linestyles="--",
              label="Média 2019–2024")
    ax.axvline(2018.5, color=CINZA, linestyle=":", linewidth=1)
    ax.text(2018.7, nivel["a"] + 0.8, "VAR 2019", color=CINZA, fontsize=9)
    ax.set_xlabel("Temporada")
    ax.set_xticks(range(2006, 2025, 2))
    ax.set_ylabel("Índice de Pollard (%)")
    ax.legend(loc="lower left", fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(FIG / "fig9_serie_ic.png", dpi=150)
    plt.close(fig)


def fig_contexto(tab5: pd.DataFrame):
    d = tab5[tab5["variavel"] != "Geral"].reset_index(drop=True)
    rotulos = [f"{r.variavel} — {r.grupo}" for r in d.itertuples()]
    y = list(range(len(d)))
    fig, ax = plt.subplots(figsize=(9.5, 9))
    cores = [AZUL if v >= 50 else VERMELHO for v in d["pollard"]]
    ax.barh(y, d["pollard"] - 50, left=50, color=cores, alpha=0.75, height=0.68)
    ax.errorbar(d["pollard"], y, xerr=[d["pollard"] - d["lo"], d["hi"] - d["pollard"]],
                fmt="none", ecolor="black", capsize=3, linewidth=1)
    ax.axvline(50, color="black", linestyle="--", linewidth=1)
    ax.set_yticks(y)
    ax.set_yticklabels(rotulos, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("Índice de Pollard (%)")
    ax.set_xlim(45, 80)
    ax.set_title("Pollard por contexto da partida (barra = ponto; haste = IC 95%)",
                 fontsize=11)
    fig.tight_layout()
    fig.savefig(FIG / "fig10_contexto.png", dpi=150)
    plt.close(fig)


def fig_correlacoes(mat: pd.DataFrame):
    rotulos = {
        "ha": "HA", "home_ppg": "Casa pts/jogo", "away_ppg": "Fora pts/jogo",
        "pts": "Pontos", "rank": "Posição", "home_win_pct": "% vit. casa",
        "away_win_pct": "% vit. fora", "home_goals_pg": "Gols casa/jogo",
        "away_goals_pg": "Gols fora/jogo", "avg_away_km": "Distância média",
        "usual_stadium_share": "% estádio habitual", "season": "Temporada",
    }
    d = mat.rename(index=rotulos, columns=rotulos)
    fig, ax = plt.subplots(figsize=(10, 9))
    im = ax.imshow(d.values, cmap="RdBu", vmin=-1, vmax=1)
    ax.set_xticks(range(len(d.columns)))
    ax.set_yticks(range(len(d.index)))
    ax.set_xticklabels(d.columns, rotation=45, ha="right", fontsize=8)
    ax.set_yticklabels(d.index, fontsize=8)
    for i in range(d.shape[0]):
        for j in range(d.shape[1]):
            valor = d.values[i, j]
            if pd.notna(valor):
                ax.text(j, i, f"{valor:.2f}", ha="center", va="center",
                        fontsize=6, color="black")
    fig.colorbar(im, ax=ax, shrink=0.8, label="rho de Spearman")
    ax.set_title("Matriz de correlação por equipe-temporada (Spearman)", fontsize=11)
    fig.tight_layout()
    fig.savefig(FIG / "fig11_correlacoes_equipe.png", dpi=150)
    plt.close(fig)


def fig_publico_ha():
    """Dispersão público × HA e público × pontos (base externa)."""
    caminho = RAIZ / "data" / "external" / "context_clean.csv"
    if not caminho.exists():
        print("fig12: context_clean.csv ausente; figura não regenerada")
        return
    ext = pd.read_csv(caminho)
    ts = team_season_features(ext).set_index(["season", "team"])
    pub = ext.groupby(["season", "home_team"])["publico"].mean().rename("publico_medio")
    pub.index = pub.index.set_names(["season", "team"])
    ts = ts.join(pub).reset_index()
    g = ts.dropna(subset=["publico_medio"]).groupby("team").agg(
        temporadas=("season", "nunique"),
        publico=("publico_medio", "mean"),
        ha=("ha", "mean"),
        pts=("pts", "mean"),
    ).reset_index()
    g = g[g["temporadas"] >= 5].copy()
    if g.empty:
        print("fig12: sem equipes com cinco temporadas; figura não regenerada")
        return

    fig, axes = plt.subplots(1, 2, figsize=(12, 5.2))
    paineis = [
        ("ha", "HA × público", "Vantagem casa−fora (pontos/jogo)"),
        ("pts", "Pontos médios × público", "Pontos médios por temporada"),
    ]
    for ax, (coluna, titulo, rotulo_y) in zip(axes, paineis):
        x = g["publico"] / 1000
        y = g[coluna]
        ax.scatter(x, y, color=AZUL, alpha=0.8, s=28)
        coef = np.polyfit(x, y, 1)
        xs = np.linspace(float(x.min()), float(x.max()), 50)
        ax.plot(xs, np.polyval(coef, xs), color=CINZA, linewidth=1.5)
        rho = float(x.rank().corr(y.rank()))
        ax.set_title(f"{titulo} (ρ = {rho:.2f})", fontsize=10)
        ax.set_xlabel("Público médio (mil)")
        ax.set_ylabel(rotulo_y)
        deslocamentos = {"Flamengo": (4, 4), "Santos": (4, 4), "Atletico-GO": (4, -12)}
        for _, row in g.iterrows():
            if row["team"] in deslocamentos:
                nome = "Atlético-GO" if row["team"] == "Atletico-GO" else row["team"]
                ax.annotate(nome, (row["publico"] / 1000, row[coluna]),
                            textcoords="offset points",
                            xytext=deslocamentos[row["team"]], fontsize=8)
    fig.suptitle("Público médio, HA e pontos médios por temporada (por equipe, 2007–2024)",
                 fontsize=12)
    fig.tight_layout()
    fig.savefig(FIG / "fig12_publico_ha.png", dpi=150)
    plt.close(fig)


def main():
    FIG.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(RAIZ / "data" / "processed" / "matches_processed.csv")
    s = summarize(df)
    t = by_season(df).sort_values("season")
    _, tab5, _, payload = build_outputs()
    anual = pd.DataFrame(payload["anual"])
    fig_distribuicao(s)
    fig_pollard(t)
    fig_resultados(t)
    fig_gols(t)
    fig_serie_ic(anual, payload["nivel_2019"])
    fig_contexto(tab5)
    fig_correlacoes(pd.DataFrame(payload["correlacoes"]["equipe"]["matriz"]))
    fig_publico_ha()
    tab1 = t.merge(anual[["season", "lo", "hi"]].rename(
        columns={"lo": "pollard_lo", "hi": "pollard_hi"}), on="season", how="left")
    tab1.round(2).to_csv(FIG / "tab1_indicadores_temporada.csv", index=False)
    print("figuras:", sorted(p.name for p in FIG.iterdir()))


if __name__ == "__main__":
    main()
