"""Base de partidas da Série A a partir do BrazilianFootball/Data (MIT).

O repositório `BrazilianFootball/Data` publica um JSON por temporada com
resultado, data, estádio, gols e cartões extraídos dos borderôs eletrônicos da
CBF. Este módulo converte esses arquivos no esquema da base do TCC, sem
depender da fonte primária sem licença usada em 2006–2012.

Recorte: 2013–2024 (o borderô eletrônico da CBF começa em 2013).
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from cards import parse_partida, time_canonico
from context import CLUB_COORDS

REPO = "BrazilianFootball/Data"
COMMIT = "0dd1bc5f7da20130df460b9876e0bbbfebcbfa03"
LICENCA = "MIT"
PASTA = Path(__file__).resolve().parent.parent / "data" / "external" / "cards"

COLUNAS = [
    "match_id", "season", "date", "round", "home_team", "away_team",
    "home_goals", "away_goals", "result", "home_points", "away_points",
    "stadium", "source",
]


def parse_jogo(jogo: dict, season: int, jogo_id: str | int) -> dict:
    """Converte um jogo do JSON no esquema limpo do TCC."""
    base = parse_partida(jogo)
    if base["home_team"] is None or base["away_team"] is None:
        raise ValueError(
            f"time não mapeado em {season}/{jogo_id}: "
            f"{jogo.get('Home')!r} x {jogo.get('Away')!r}"
        )
    hg, ag = int(base["home_goals"]), int(base["away_goals"])
    if hg > ag:
        resultado, ph, pa = "H", 3, 0
    elif hg < ag:
        resultado, ph, pa = "A", 0, 3
    else:
        resultado, ph, pa = "D", 1, 1
    try:
        numero = int(jogo_id)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"jogo_id não numérico: {jogo_id!r}") from exc
    estadio = str(jogo.get("Stadium") or "").strip() or None
    return {
        "match_id": season * 1000 + numero,
        "season": int(season),
        "date": base["date"],
        "round": 0,
        "home_team": base["home_team"],
        "away_team": base["away_team"],
        "home_goals": hg,
        "away_goals": ag,
        "result": resultado,
        "home_points": ph,
        "away_points": pa,
        "stadium": estadio,
        "source": f"{REPO} commit {COMMIT[:7]} ({LICENCA})",
    }


def build_base(anos: range | list[int], pasta: Path = PASTA) -> pd.DataFrame:
    """Lê os JSONs das temporadas e devolve a base ordenada."""
    linhas = []
    for ano in anos:
        caminho = pasta / f"Serie_A_{ano}_games.json"
        if not caminho.exists():
            raise FileNotFoundError(
                f"arquivo ausente: {caminho}; rode scripts/fetch_cards.py"
            )
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        for jogo_id, jogo in dados.items():
            linhas.append(parse_jogo(jogo, ano, jogo_id))
    df = pd.DataFrame(linhas, columns=COLUNAS)
    return df.sort_values(["season", "date", "match_id"]).reset_index(drop=True)


def validar_base(df: pd.DataFrame) -> None:
    """Falha cedo se a base não servir ao dashboard/à análise."""
    faltantes = [c for c in COLUNAS if c not in df.columns]
    if faltantes:
        raise ValueError(f"colunas ausentes: {faltantes}")
    if df.empty:
        raise ValueError("base vazia")
    if df["match_id"].duplicated().any():
        raise ValueError("match_id duplicado")
    if df[["season", "date", "home_team", "away_team"]].isna().any().any():
        raise ValueError("campos obrigatórios ausentes")
    if (df["home_goals"] < 0).any() or (df["away_goals"] < 0).any():
        raise ValueError("gol negativo")
    if (df["home_team"] == df["away_team"]).any():
        raise ValueError("mandante igual ao visitante")
    for linha in df.itertuples():
        esperado = "H" if linha.home_goals > linha.away_goals else (
            "A" if linha.home_goals < linha.away_goals else "D"
        )
        if linha.result != esperado:
            raise ValueError(f"resultado inconsistente em {linha.match_id}")
    times = set(df["home_team"]) | set(df["away_team"])
    sem_coordenada = sorted(t for t in times if t not in CLUB_COORDS)
    if sem_coordenada:
        raise ValueError(f"times sem coordenada: {sem_coordenada}")


def quality_report(df: pd.DataFrame) -> dict:
    """Resumo no formato esperado pela aba Metodologia do dashboard."""
    cobertura = {str(int(ano)): int(n) for ano, n in
                 df.groupby("season").size().items()}
    esperado = {ano: 379 if ano == 2016 else 380 for ano in range(2013, 2025)}
    abaixo = {str(ano): esperado[ano] - cobertura.get(str(ano), 0)
              for ano in esperado
              if cobertura.get(str(ano), 0) < esperado[ano]}
    return {
        "fonte": f"{REPO} ({LICENCA})",
        "commit": COMMIT,
        "recorte": [int(df["season"].min()), int(df["season"].max())],
        "loaded": int(len(df)),
        "kept": int(len(df)),
        "excluded": {},
        "coverage_per_season": cobertura,
        "seasons_below_expected": abaixo,
        "times": int(len(set(df["home_team"]) | set(df["away_team"]))),
        "estadios_ausentes": int(df["stadium"].isna().sum()),
        "notes": [
            "Borderô eletrônico da CBF disponível a partir de 2013.",
            "2016 tem 379 partidas: Chapecoense x Atletico-MG (rodada 38) cancelada.",
            "Temporada 2020 vai de 2020-08-08 a 2021-02-25 (COVID-19).",
            "Sem rodada na fonte JSON; round=0 e a ordem usa data e match_id.",
        ],
    }
