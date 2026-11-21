#!/usr/bin/env python3
"""Modelos do artigo 2013–2024: Poisson ataque/defesa e decomposição de variância.

O modelo de gols separa ataque e defesa por equipe, efeitos de temporada e
vantagem de casa. A mudança pós-2019 entra como interação `home × post`.

Saídas:
  data/processed/poisson_summary.json
  figuras/tab_poisson.csv
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from associations import team_season_features
from paths import caminho_no_projeto

RAIZ = Path(__file__).resolve().parent.parent
BASE = RAIZ / "data" / "processed" / "matches_processed_2013_2024.csv"
RESUMO = RAIZ / "data" / "processed" / "poisson_summary.json"
TABELA = RAIZ / "figuras" / "tab_poisson.csv"


def _desenho(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, list[str], np.ndarray]:
    """Matriz de desenho para os dois gols de cada partida.

    Uma linha para o mandante e outra para o visitante. A equipe de referência
    (primeira em ordem alfabética) tem ataque e defesa iguais a zero; a
    temporada de referência é a primeira.
    """
    times = sorted(set(df["home_team"]) | set(df["away_team"]))
    temporadas = sorted(df["season"].unique())
    ref_time, ref_temp = times[0], temporadas[0]
    times_sem = [t for t in times if t != ref_time]
    temps_sem = [t for t in temporadas if t != ref_temp]
    idx_time = {t: i for i, t in enumerate(times_sem)}
    idx_temp = {t: i for i, t in enumerate(temps_sem)}
    n_t, n_s = len(idx_time), len(idx_temp)
    nomes = (["intercepto", "casa", "casa_pos2019"]
             + [f"ataque_{t}" for t in idx_time]
             + [f"defesa_{t}" for t in idx_time]
             + [f"temporada_{t}" for t in idx_temp])
    X = np.zeros((2 * len(df), len(nomes)))
    y = np.zeros(2 * len(df))
    partidas = np.zeros(2 * len(df), dtype=int)

    for i, linha in enumerate(df.itertuples()):
        h, a = i * 2, i * 2 + 1
        y[h], y[a] = linha.home_goals, linha.away_goals
        partidas[h] = partidas[a] = int(linha.match_id)
        post = 1.0 if linha.season >= 2019 else 0.0
        # mandante
        X[h, 0] = 1.0
        X[h, 1] = 1.0
        X[h, 2] = post
        if linha.home_team in idx_time:
            X[h, 3 + idx_time[linha.home_team]] = 1.0
        if linha.away_team in idx_time:
            X[h, 3 + n_t + idx_time[linha.away_team]] = -1.0
        # visitante
        X[a, 0] = 1.0
        if linha.away_team in idx_time:
            X[a, 3 + idx_time[linha.away_team]] = 1.0
        if linha.home_team in idx_time:
            X[a, 3 + n_t + idx_time[linha.home_team]] = -1.0
        if linha.season != ref_temp:
            X[h, 3 + 2 * n_t + idx_temp[linha.season]] = 1.0
            X[a, 3 + 2 * n_t + idx_temp[linha.season]] = 1.0
    return X, y, nomes, partidas


def _irls(X: np.ndarray, y: np.ndarray, n_iter: int = 60) -> tuple[np.ndarray, np.ndarray]:
    """Poisson GLM por mínimos quadrados reponderados (IRLS)."""
    beta = np.zeros(X.shape[1])
    beta[0] = np.log(max(y.mean(), 1e-6))
    for _ in range(n_iter):
        eta = np.clip(X @ beta, -20, 20)
        lam = np.exp(eta)
        w = np.maximum(lam, 1e-9)
        z = eta + (y - lam) / w
        xtwx = X.T @ (w[:, None] * X)
        xtwz = X.T @ (w * z)
        novo = np.linalg.lstsq(xtwx, xtwz, rcond=None)[0]
        if np.max(np.abs(novo - beta)) < 1e-9:
            beta = novo
            break
        beta = novo
    eta = np.clip(X @ beta, -20, 20)
    lam = np.exp(eta)
    return beta, lam


def _cov_cluster(X: np.ndarray, y: np.ndarray, lam: np.ndarray,
                 partidas: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Covariância robusta por partida e fator de superdispersão."""
    w = np.maximum(lam, 1e-9)
    xtwx_inv = np.linalg.pinv(X.T @ (w[:, None] * X))
    resid = y - lam
    meat = np.zeros((X.shape[1], X.shape[1]))
    for grupo in np.unique(partidas):
        idx = partidas == grupo
        escore = X[idx].T @ resid[idx]
        meat += np.outer(escore, escore)
    n, p = X.shape
    g = len(np.unique(partidas))
    cov = xtwx_inv @ meat @ xtwx_inv
    cov *= (g / max(g - 1, 1)) * ((n - 1) / max(n - p, 1))
    pearson = float(np.sum(resid ** 2 / w))
    phi = pearson / max(n - p, 1)
    return cov, np.array([phi])


def _ic(beta: float, se: float) -> dict:
    return {"coef": float(beta), "se": float(se),
            "lo": float(beta - 1.96 * se), "hi": float(beta + 1.96 * se)}


def _multiplicativo(beta: float, se: float) -> dict:
    return {"efeito": float(np.exp(beta) - 1),
            "lo": float(np.exp(beta - 1.96 * se) - 1),
            "hi": float(np.exp(beta + 1.96 * se) - 1)}


def decomposicao_variancia(df: pd.DataFrame) -> dict:
    """Decomposição one-way da HA por equipe-temporada (entre vs dentro)."""
    ts = team_season_features(df)
    ts = ts.dropna(subset=["ha"])
    grande = float(ts["ha"].mean())
    grupos = ts.groupby("team")["ha"]
    k, n = grupos.ngroups, len(ts)
    ss_entre = float(sum(len(g) * (g.mean() - grande) ** 2 for _, g in grupos))
    ss_dentro = float(sum(((g - g.mean()) ** 2).sum() for _, g in grupos))
    ms_entre = ss_entre / max(k - 1, 1)
    ms_dentro = ss_dentro / max(n - k, 1)
    n0 = (n - sum(len(g) ** 2 for _, g in grupos) / n) / max(k - 1, 1)
    var_entre = max(0.0, (ms_entre - ms_dentro) / n0) if n0 else 0.0
    var_dentro = ms_dentro
    total = var_entre + var_dentro
    estimavel = k > 1 and n > k and total > 0
    return {"n": int(n), "times": int(k), "media": grande,
            "ss_entre": ss_entre, "ss_dentro": ss_dentro,
            "ms_entre": ms_entre, "ms_dentro": ms_dentro,
            "n0": n0, "var_entre": var_entre, "var_dentro": var_dentro,
            "icc": var_entre / total if estimavel else None,
            "share_entre": var_entre / total if estimavel else None,
            "icc_estimavel": bool(estimavel)}


def main() -> None:
    df = pd.read_csv(BASE)
    X, y, nomes, partidas = _desenho(df)
    beta, lam = _irls(X, y)
    cov, phi = _cov_cluster(X, y, lam, partidas)
    se = np.sqrt(np.maximum(np.diag(cov), 0))
    i_casa, i_pos = nomes.index("casa"), nomes.index("casa_pos2019")
    gama, delta = beta[i_casa], beta[i_pos]
    se_gama, se_delta = se[i_casa], se[i_pos]
    resumo = {
        "modelo": "gols ~ Poisson(mu + ataque_i - defesa_j + casa + casa:pos2019 + temporada)",
        "n_partidas": int(len(df)),
        "n_observacoes": int(len(y)),
        "parametros": int(X.shape[1]),
        "superdispersao": float(phi[0]),
        "casa": _ic(gama, se_gama),
        "casa_multiplicativo": _multiplicativo(gama, se_gama),
        "interacao_pos2019": _ic(delta, se_delta),
        "interacao_multiplicativo": _multiplicativo(delta, se_delta),
        "casa_pos2019": _ic(gama + delta, float(np.sqrt(
            cov[i_casa, i_casa] + cov[i_pos, i_pos] + 2 * cov[i_casa, i_pos]))),
        "casa_pos2019_multiplicativo": _multiplicativo(
            gama + delta, float(np.sqrt(
                cov[i_casa, i_casa] + cov[i_pos, i_pos] + 2 * cov[i_casa, i_pos]))),
        "variancia_ha": decomposicao_variancia(df),
    }
    RESUMO.write_text(json.dumps(resumo, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    linhas = [
        {"parametro": "vantagem de casa (log)", **_ic(gama, se_gama)},
        {"parametro": "interação casa × pós-2019", **_ic(delta, se_delta)},
        {"parametro": "vantagem de casa pós-2019 (log)",
         **resumo["casa_pos2019"]},
    ]
    pd.DataFrame(linhas).round(6).to_csv(TABELA, index=False)
    print(json.dumps(resumo, ensure_ascii=False, indent=2))
    print(f"-> {RESUMO}")
    print(f"-> {TABELA}")


if __name__ == "__main__":
    main()
