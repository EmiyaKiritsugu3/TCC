#!/usr/bin/env python3
"""Gera data/processed/ a partir da base bruta (Fase 2)."""
from pathlib import Path

from clean_data import clean_matches, save_processed
from load_data import load_raw

RAIZ = Path(__file__).resolve().parent.parent
RAW = RAIZ / "data" / "raw" / "campeonato-brasileiro-full.csv"
OUT = RAIZ / "data" / "processed"


def main() -> None:
    df_raw = load_raw(RAW)
    clean, report = clean_matches(df_raw)
    save_processed(clean, report, OUT)
    print(f"lidas: {report['loaded']}  mantidas: {report['kept']}")
    print(f"excluídas: {report['excluded']}")
    print(f"cobertura: {report['coverage_per_season']}")
    print(f"abaixo do esperado: {report['seasons_below_expected']}")
    print(f"gravado em: {OUT / 'matches_processed.csv'}")


if __name__ == "__main__":
    main()
