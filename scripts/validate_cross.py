#!/usr/bin/env python3
"""Validação cruzada 2018–2024: base primária x OpenFootball (CC0)."""
from pathlib import Path

import pandas as pd

from openfootball import comparar, parse_arquivo
from validacao_excecoes import excecao_conhecida

RAIZ = Path(__file__).resolve().parent.parent
OF_DIR = RAIZ / "data" / "external" / "openfootball"
ANOS = list(range(2018, 2025))

# A exceção conhecida de data (jogo de dois dias de 2023) está documentada
# e testada em `validacao_excecoes.py`.


def main() -> int:
    base = pd.read_csv(RAIZ / "data" / "processed" / "matches_processed.csv")
    print(f"{'ano':>4} | {'base':>4} {'OF':>4} {'ambas':>5} {'placar_ok':>9} {'div':>3} {'só_base':>7} {'só_OF':>5}")
    ok = True
    for ano in ANOS:
        b = base[base["season"] == ano][["date", "home_team", "away_team", "home_goals", "away_goals"]]
        of = parse_arquivo(OF_DIR / f"{ano}_br1.txt", ano)
        of = of[["date", "home_team", "away_team", "home_goals", "away_goals"]]
        r = comparar(b, of)
        # Desconta a exceção conhecida de data (jogo de dois dias, 2023).
        so_base = r["so_na_base"]
        so_of = r["so_na_of"]
        if excecao_conhecida(ano, so_base, so_of, r["placar_divergente"]):
            print(f"{ano:>4} | {r['n_base']:>4} {r['n_of']:>4} {r['em_ambas']:>5} "
                  f"{r['placar_igual']:>9} {r['placar_divergente']:>3} "
                  f"{len(so_base):>7} {len(so_of):>5}  <- exceção conhecida (jogo de dois dias)")
            continue
        print(f"{ano:>4} | {r['n_base']:>4} {r['n_of']:>4} {r['em_ambas']:>5} "
              f"{r['placar_igual']:>9} {r['placar_divergente']:>3} "
              f"{len(r['so_na_base']):>7} {len(r['so_na_of']):>5}")
        for nome, tab in (("só_base", r["so_na_base"]), ("só_OF", r["so_na_of"]),
                          ("diverg", r["divergencias"])):
            if len(tab):
                ok = False
                print(f"  -- {nome} ({len(tab)}):")
                print(tab.to_string(index=False))
    print("RESULTADO:", "PASS — bases idênticas" if ok else "DIVERGÊNCIAS ACIMA — investigar")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
