#!/usr/bin/env python3
"""Constrói a base 2013–2024 a partir do BrazilianFootball/Data (MIT).

Saídas:
  data/processed/matches_processed_2013_2024.csv
  data/processed/quality_report_2013_2024.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from mit_data import build_base, quality_report, validar_base
from paths import caminho_no_projeto

RAIZ = Path(__file__).resolve().parent.parent


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inicio", type=int, default=2013)
    parser.add_argument("--fim", type=int, default=2024)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--qualidade", type=Path, default=None)
    args = parser.parse_args(argv)

    anos = list(range(args.inicio, args.fim + 1))
    sufixo = f"{args.inicio}_{args.fim}"
    out = caminho_no_projeto(args.out) if args.out else (
        RAIZ / "data" / "processed" / f"matches_processed_{sufixo}.csv")
    qualidade_path = caminho_no_projeto(args.qualidade) if args.qualidade else (
        RAIZ / "data" / "processed" / f"quality_report_{sufixo}.json")
    df = build_base(anos)
    validar_base(df)

    out.parent.mkdir(parents=True, exist_ok=True)
    qualidade_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    relatorio = quality_report(df)
    qualidade_path.write_text(
        json.dumps(relatorio, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"ok: {len(df)} partidas ({args.inicio}–{args.fim}) -> {out}")
    print(pd.DataFrame(relatorio["coverage_per_season"], index=["jogos"]).T.to_string())
    print(f"ok: qualidade -> {qualidade_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
