#!/usr/bin/env python3
"""Converte a extração JSON do FBref em uma tabela de partidas.

O JSON de entrada é uma lista de objetos com as colunas da tabela
"Scores & Fixtures" do FBref:
round, day, date, time, home, score, away, attendance, venue, referee.

Como o FBref fica atrás de Cloudflare, a extração é feita no navegador
(ver docs/fontes_externas.md) e este script apenas normaliza o resultado.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd

from paths import caminho_no_projeto

RAIZ = Path(__file__).resolve().parent.parent
PADRAO_IN = RAIZ / ".playwright-mcp" / "fbref_2024.json"
PADRAO_OUT = RAIZ / "data" / "external" / "fbref" / "2024_serie_a.csv"


def _limpar(df: pd.DataFrame, season: int) -> pd.DataFrame:
    for coluna in ("home", "away", "score", "attendance", "venue", "referee"):
        if coluna not in df.columns:
            df[coluna] = ""
    jogos = df[df["score"].astype(str).str.contains("–", regex=False)].copy()
    placar = jogos["score"].str.replace("–", "-", regex=False).str.split("-", expand=True)
    jogos["home_goals"] = pd.to_numeric(placar[0], errors="coerce").astype("Int64")
    jogos["away_goals"] = pd.to_numeric(placar[1], errors="coerce").astype("Int64")
    jogos["attendance"] = pd.to_numeric(
        jogos["attendance"].astype(str).str.replace(",", "", regex=False),
        errors="coerce",
    ).astype("Int64")
    for coluna in ("home", "away", "venue", "referee"):
        jogos[coluna] = jogos[coluna].astype(str).str.strip().replace({"": None})
    jogos["season"] = season
    jogos["date"] = pd.to_datetime(jogos["date"], errors="coerce").dt.date
    jogos = jogos.dropna(subset=["date", "home", "away", "home_goals", "away_goals"])
    return jogos[[
        "season", "round", "date", "time", "home", "away",
        "home_goals", "away_goals", "attendance", "venue", "referee",
    ]].sort_values(["date", "time", "home"]).reset_index(drop=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=PADRAO_IN)
    parser.add_argument("--out", type=Path, default=PADRAO_OUT)
    parser.add_argument("--season", type=int, default=2024)
    args = parser.parse_args(argv)
    args.input = caminho_no_projeto(args.input)
    args.out = caminho_no_projeto(args.out)

    if not args.input.exists():
        raise SystemExit(f"JSON não encontrado: {args.input}")
    dados = json.loads(args.input.read_text(encoding="utf-8"))  # NOSONAR: caminho confinado
    df = _limpar(pd.DataFrame(dados), args.season)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out, index=False)  # NOSONAR: caminho confinado

    conteudo = args.out.read_bytes()  # NOSONAR: caminho confinado
    (args.out.parent / "FETCH_METADATA.json").write_text(  # NOSONAR: caminho confinado
        json.dumps({
            "fonte": "FBref / Sports Reference",
            "url": f"https://fbref.com/en/comps/24/{args.season}/schedule/{args.season}-Serie-A-Scores-and-Fixtures",
            "linhas": len(df),
            "publico_nao_nulo": int(df["attendance"].notna().sum()),
            "arbitro_nao_nulo": int(df["referee"].notna().sum()),
            "sha256": hashlib.sha256(conteudo).hexdigest(),
        }, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"ok: {len(df)} partidas -> {args.out}")
    print(f"público: {df['attendance'].notna().sum()}; árbitro: {df['referee'].notna().sum()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
