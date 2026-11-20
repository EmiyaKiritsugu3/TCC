#!/usr/bin/env python3
"""Analisa os cartões por partida (2013–2024).

Saídas:
  figuras/fig13_cartoes.png
  figuras/tab_cartoes.csv
  data/external/cards/cards_summary.json
  docs/analise_cartoes.md (tabelas e leitura)
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from paths import caminho_no_projeto

RAIZ = Path(__file__).resolve().parent.parent
CARTOES = RAIZ / "data" / "external" / "cards" / "cards_2013_2024.csv"
BASE = RAIZ / "data" / "processed" / "matches_processed.csv"
CONTEXTO = RAIZ / "data" / "external" / "context_clean.csv"
FIG = RAIZ / "figuras"
RESUMO = RAIZ / "data" / "external" / "cards" / "cards_summary.json"
TABELA = FIG / "tab_cartoes.csv"
FIGURA = FIG / "fig13_cartoes.png"
RELATORIO = RAIZ / "docs" / "analise_cartoes.md"

AZUL, CINZA, VERMELHO = "#1f77b4", "#7f7f7f", "#d62728"


def _pt(x: float, n: int = 2, sinal: bool = False) -> str:
    fmt = f"{{:+.{n}f}}" if sinal else f"{{:.{n}f}}"
    return fmt.format(x).replace(".", ",")


def _bootstrap_media(valores: np.ndarray, n: int = 4000, seed: int = 42):
    if len(valores) == 0:
        return None, None, None
    rng = np.random.default_rng(seed)
    medias = np.array([
        rng.choice(valores, len(valores), replace=True).mean() for _ in range(n)
    ])
    return float(valores.mean()), float(np.percentile(medias, 2.5)), float(np.percentile(medias, 97.5))


def _ols_hc1(y: np.ndarray, X: np.ndarray, nomes: list[str]):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    n, k = X.shape
    xtx_inv = np.linalg.pinv(X.T @ X)
    cov = xtx_inv @ (X.T @ (X * (resid ** 2)[:, None])) @ xtx_inv
    cov *= n / max(n - k, 1)
    se = np.sqrt(np.diag(cov))
    return beta, se, nomes


def _did(df: pd.DataFrame) -> dict:
    """DiD 2019 vs 2020 com efeitos fixos de mandante e visitante."""
    d = df[df["season"].isin([2019, 2020])].copy()
    d["post"] = (d["season"] == 2020).astype(float)
    d["yellow_diff"] = d["yellow_home"] - d["yellow_away"]
    y = d["yellow_diff"].to_numpy(dtype=float)

    def matriz(sub: pd.DataFrame) -> tuple[np.ndarray, list[str]]:
        base = pd.DataFrame({
            "intercepto": 1.0,
            "post": sub["post"].to_numpy(dtype=float),
        }, index=sub.index)
        casa = pd.get_dummies(sub["home_team"], prefix="casa", drop_first=True, dtype=float)
        fora = pd.get_dummies(sub["away_team"], prefix="fora", drop_first=True, dtype=float)
        X = pd.concat([base, casa, fora], axis=1)
        return X.to_numpy(dtype=float), list(X.columns)

    X, nomes = matriz(d)
    beta, se, nomes = _ols_hc1(y, X, nomes)
    i = nomes.index("post")
    return {
        "n": int(len(d)),
        "coef": float(beta[i]),
        "se": float(se[i]),
        "lo": float(beta[i] - 1.96 * se[i]),
        "hi": float(beta[i] + 1.96 * se[i]),
        "modelo": "yellow_diff ~ post + C(home_team) + C(away_team)",
    }


def _did_comum(df: pd.DataFrame) -> dict:
    """DiD restrito às equipes presentes em 2019 e 2020 (amostra equilibrada)."""
    t19 = set(df.loc[df["season"] == 2019, "home_team"]) | set(df.loc[df["season"] == 2019, "away_team"])
    t20 = set(df.loc[df["season"] == 2020, "home_team"]) | set(df.loc[df["season"] == 2020, "away_team"])
    comuns = t19 & t20
    d = df[df["season"].isin([2019, 2020])].copy()
    d = d[d["home_team"].isin(comuns) & d["away_team"].isin(comuns)].copy()
    d = d.reset_index(drop=True)
    d["post"] = (d["season"] == 2020).astype(float)
    d["yellow_diff"] = d["yellow_home"] - d["yellow_away"]
    y = d["yellow_diff"].to_numpy(dtype=float)
    base = pd.DataFrame({"intercepto": 1.0, "post": d["post"].to_numpy(dtype=float)})
    casa = pd.get_dummies(d["home_team"], prefix="casa", drop_first=True, dtype=float)
    fora = pd.get_dummies(d["away_team"], prefix="fora", drop_first=True, dtype=float)
    X = pd.concat([base, casa, fora], axis=1).to_numpy(dtype=float)
    beta, se, _ = _ols_hc1(y, X, ["intercepto", "post"] + list(casa.columns) + list(fora.columns))
    return {
        "n": int(len(d)),
        "coef": float(beta[1]),
        "se": float(se[1]),
        "lo": float(beta[1] - 1.96 * se[1]),
        "hi": float(beta[1] + 1.96 * se[1]),
        "equipes_comuns": sorted(comuns),
    }


def _tabela_temporadas(df: pd.DataFrame) -> pd.DataFrame:
    linhas = []
    for season, g in df.groupby("season"):
        m, lo, hi = _bootstrap_media((g["yellow_home"] - g["yellow_away"]).to_numpy(dtype=float))
        mr, lor, hir = _bootstrap_media((g["red_home"] - g["red_away"]).to_numpy(dtype=float))
        linhas.append({
            "season": int(season),
            "n": int(len(g)),
            "amarelos_casa": float(g["yellow_home"].mean()),
            "amarelos_fora": float(g["yellow_away"].mean()),
            "amarelos_diff": m,
            "amarelos_lo": lo,
            "amarelos_hi": hi,
            "vermelhos_casa": float(g["red_home"].mean()),
            "vermelhos_fora": float(g["red_away"].mean()),
            "vermelhos_diff": mr,
            "vermelhos_lo": lor,
            "vermelhos_hi": hir,
            "cartoes_por_jogo": float((g["yellow_home"] + g["yellow_away"]
                                       + g["red_home"] + g["red_away"]).mean()),
        })
    return pd.DataFrame(linhas)


def _cartoes_por_falta(df: pd.DataFrame) -> pd.DataFrame:
    if not {"faltas_mandante", "faltas_visitante"}.issubset(df.columns):
        return pd.DataFrame()
    d = df.dropna(subset=["faltas_mandante", "faltas_visitante"]).copy()
    d = d[(d["faltas_mandante"] > 0) & (d["faltas_visitante"] > 0)]
    linhas = []
    for season, g in d.groupby("season"):
        linhas.append({
            "season": int(season),
            "n": int(len(g)),
            "amarelos_por_falta_casa": float(g["yellow_home"].sum() / g["faltas_mandante"].sum()),
            "amarelos_por_falta_fora": float(g["yellow_away"].sum() / g["faltas_visitante"].sum()),
        })
    return pd.DataFrame(linhas)


def _figura(tab: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    ax.axhline(0, color="black", linewidth=1)
    ax.fill_between(tab["season"], tab["amarelos_lo"], tab["amarelos_hi"],
                    color=AZUL, alpha=0.18, label="IC 95% (bootstrap)")
    ax.plot(tab["season"], tab["amarelos_diff"], marker="o", color=AZUL,
            label="Amarelos casa − fora")
    ax.axvspan(2019.5, 2020.5, color=VERMELHO, alpha=0.10)
    ax.text(2020, tab["amarelos_diff"].max() + 0.05, "2020\nsem torcida",
            ha="center", va="bottom", fontsize=9, color=VERMELHO)
    ax.set_xlabel("Temporada")
    ax.set_ylabel("Diferença média (cartões por jogo)")
    ax.set_xticks(range(2013, 2025, 2))
    ax.legend(loc="lower left", fontsize=9, frameon=False)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURA, dpi=150)
    plt.close(fig)


def _relatorio(tab: pd.DataFrame, did: dict, did_comum: dict,
               por_falta: pd.DataFrame) -> str:
    linhas = [
        "# Cartões e arbitragem — análise descritiva (2013–2024)",
        "",
        "Fonte: BrazilianFootball/Data (MIT), extraída dos borderôs da CBF.",
        "Cada cartão é contado para a equipe que o recebeu; cartões não atribuídos",
        "são registrados no controle de qualidade.",
        "",
        "## Cartões por temporada",
        "",
        "| Temporada | Jogos | Amarelos casa | Amarelos fora | Diferença (IC 95%) | Vermelhos casa | Vermelhos fora |",
        "|---|---:|---:|---:|---|---:|---:|",
    ]
    for r in tab.itertuples():
        linhas.append(
            f"| {r.season} | {r.n} | {_pt(r.amarelos_casa)} | {_pt(r.amarelos_fora)} | "
            f"{_pt(r.amarelos_diff, 2, True)} ({_pt(r.amarelos_lo, 2, True)} a "
            f"{_pt(r.amarelos_hi, 2, True)}) | {_pt(r.vermelhos_casa)} | "
            f"{_pt(r.vermelhos_fora)} |"
        )
    linhas += [
        "",
        "## Diferença-em-diferenças 2019 → 2020",
        "",
        f"- Amostra completa: **{_pt(did['coef'], 3, True)}** cartões por jogo "
        f"(EP {_pt(did['se'], 3)}; IC 95% {_pt(did['lo'], 3, True)} a "
        f"{_pt(did['hi'], 3, True)}; n={did['n']}).",
        f"- Equipes presentes nos dois anos: **{_pt(did_comum['coef'], 3, True)}** "
        f"(EP {_pt(did_comum['se'], 3)}; IC 95% {_pt(did_comum['lo'], 3, True)} a "
        f"{_pt(did_comum['hi'], 3, True)}; n={did_comum['n']}).",
        "",
        "Coeficiente positivo = a diferença casa−fora **aumentou** em 2020: o",
        "mandante deixou de receber relativamente menos cartões. Em 2019 a",
        "diferença era −0,19; em 2020, +0,11; a mudança bruta é +0,30 e a",
        f"estimativa com efeitos fixos de equipe é {_pt(did['coef'], 2, True)}.",
        "",
        "## Leitura",
        "",
        "- Com torcida (2013–2019), o mandante recebia, em média, cerca de",
        "  0,3 cartão amarelo a menos que o visitante por jogo.",
        "- Em 2020, sem torcida, a diferença ficou próxima de zero ou levemente",
        "  positiva.",
        "- Em 2021–2024, com o retorno do público, a diferença voltou a ser",
        "  negativa, embora com oscilação.",
        "- O padrão é compatível com pressão da torcida sobre decisões de",
        "  arbitragem, mas não identifica causalidade: VAR, calendário, protocolos",
        "  e comportamento dos jogadores também mudaram.",
        "",
    ]
    if not por_falta.empty:
        linhas += [
            "## Cartões por falta (2018+)",
            "",
            "| Temporada | Jogos com faltas | Amarelos/falta casa | Amarelos/falta fora |",
            "|---|---:|---:|---:|",
        ]
        for r in por_falta.itertuples():
            linhas.append(
                f"| {r.season} | {r.n} | {_pt(r.amarelos_por_falta_casa, 3)} | "
                f"{_pt(r.amarelos_por_falta_fora, 3)} |"
            )
        linhas += [
            "",
            "A cobertura de faltas é parcial em 2018–2019 e 2024; a comparação",
            "cartes-per-foul serve como robustez, não como teste definitivo.",
            "",
        ]
    linhas += [
        "## Limitações",
        "",
        "- Cartão é decisão do árbitro, mas também reflete comportamento do jogador.",
        "- 2020 tem pandemia, calendário atípico e protocolos; VAR já existia em 2019.",
        "- 2006–2012 não têm cartões nesta fonte.",
        "- A série 2013–2024 tem 1 cartão não atribuído em 2022 (formato quebrado).",
        "- Não há pênaltis nem cartões por arbítrio separados por tipo; o teste do",
        "  canal arbitral é indireto.",
        "",
        "## Reprodução",
        "",
        "```bash",
        "PYTHONPATH=src python3 scripts/fetch_cards.py",
        "PYTHONPATH=src python3 scripts/build_cards.py",
        "PYTHONPATH=src python3 scripts/analyze_cards.py",
        "```",
    ]
    return "\n".join(linhas) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cartoes", type=Path, default=CARTOES)
    parser.add_argument("--base", type=Path, default=BASE)
    parser.add_argument("--contexto", type=Path, default=CONTEXTO)
    args = parser.parse_args(argv)

    cartoes = pd.read_csv(caminho_no_projeto(args.cartoes))
    base = pd.read_csv(caminho_no_projeto(args.base))
    contexto = pd.read_csv(caminho_no_projeto(args.contexto))
    df = cartoes.merge(
        contexto[["match_id", "arbitro", "publico", "faltas_mandante", "faltas_visitante"]],
        on="match_id", how="left",
    )
    tab = _tabela_temporadas(df)
    did = _did(df)
    did_comum = _did_comum(df)
    por_falta = _cartoes_por_falta(df)

    FIG.mkdir(parents=True, exist_ok=True)
    tab.round(4).to_csv(TABELA, index=False)
    _figura(tab)
    resumo = {
        "fonte": "BrazilianFootball/Data (MIT)",
        "periodo": [int(tab.season.min()), int(tab.season.max())],
        "temporadas": tab.round(4).to_dict(orient="records"),
        "did_2019_2020": did,
        "did_2019_2020_equipes_comuns": did_comum,
        "cartoes_por_falta": por_falta.round(4).to_dict(orient="records"),
    }
    RESUMO.write_text(json.dumps(resumo, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    RELATORIO.write_text(_relatorio(tab, did, did_comum, por_falta), encoding="utf-8")
    print(tab.round(3).to_string(index=False))
    print("\nDiD:", json.dumps(did, ensure_ascii=False))
    print("DiD equipes comuns:", json.dumps(did_comum, ensure_ascii=False))
    print(f"-> {TABELA}")
    print(f"-> {FIGURA}")
    print(f"-> {RESUMO}")
    print(f"-> {RELATORIO}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
