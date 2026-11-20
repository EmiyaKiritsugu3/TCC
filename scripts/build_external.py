#!/usr/bin/env python3
"""Constrói a base externa limpa de público e arbitragem.

Combina:
  - data/processed/matches_processed.csv (base do TCC)
  - data/external/basedosdados/brasileirao_serie_a_2006_2024.csv
  - data/external/fbref/2024_serie_a.csv (completa 2024)

Regras:
  - `publico = 0` em 2008 vira ausente: os zeros estão espalhados por todo o
    campeonato e por todos os clubes, e a média dos jogos não-zero é compatível
    com 2007/2009; é falha de registro, não portão fechado.
  - `publico = 0` em 2020–2021 é mantido: são portões fechados/restrições reais.
  - 2024: a Base dos Dados tem 286 jogos; o FBref completa o público dos demais.
  - `publico_max` é capacidade, não público do jogo; fica apenas como referência.

Saída:
  data/external/context_clean.csv (local, não versionado)
  data/external/quality_external.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from join_external import (
    ALIASES_FBREF,
    carregar_base,
    carregar_bd,
    canonico,
)

RAIZ = Path(__file__).resolve().parent.parent
FBREF = RAIZ / "data" / "external" / "fbref" / "2024_serie_a.csv"
OUT = RAIZ / "data" / "external" / "context_clean.csv"
QUALIDADE = RAIZ / "data" / "external" / "quality_external.json"


def _fbref(caminho: Path) -> pd.DataFrame:
    fb = pd.read_csv(caminho)
    fb["home_fb"] = fb["home"].map(lambda x: canonico(x, ALIASES_FBREF))
    fb["away_fb"] = fb["away"].map(lambda x: canonico(x, ALIASES_FBREF))
    fb["season"] = fb["season"].astype(int)
    fb["attendance"] = pd.to_numeric(fb["attendance"], errors="coerce")
    fb["referee"] = fb["referee"].astype(str).str.strip().replace({"": None, "nan": None})
    return fb


def _juntar(base: pd.DataFrame, bd: pd.DataFrame, fb: pd.DataFrame) -> pd.DataFrame:
    chaves = ["season", "home_team", "away_team", "home_goals", "away_goals"]
    bd_unico = bd.drop_duplicates(
        subset=["season", "home_bd", "away_bd", "gols_mandante", "gols_visitante"]
    )
    junto = base.merge(
        bd_unico[[
            "season", "home_bd", "away_bd", "gols_mandante", "gols_visitante",
            "publico", "publico_max", "arbitro",
            "faltas_mandante", "faltas_visitante",
        ]],
        left_on=chaves,
        right_on=["season", "home_bd", "away_bd", "gols_mandante", "gols_visitante"],
        how="left",
    )
    fb_unico = fb.drop_duplicates(subset=["season", "home_fb", "away_fb", "home_goals", "away_goals"])
    junto = junto.merge(
        fb_unico[["season", "home_fb", "away_fb", "home_goals", "away_goals",
                  "attendance", "referee"]],
        left_on=chaves,
        right_on=["season", "home_fb", "away_fb", "home_goals", "away_goals"],
        how="left",
        suffixes=("", "_fb"),
    )
    return junto


def _limpar(junto: pd.DataFrame) -> pd.DataFrame:
    d = junto.copy()

    # Público: Base dos Dados primeiro; FBref completa 2024.
    d["publico_bd"] = pd.to_numeric(d["publico"], errors="coerce")
    d["publico_fb"] = pd.to_numeric(d["attendance"], errors="coerce")
    d["publico"] = d["publico_bd"]
    usar_fb = d["publico"].isna() & d["publico_fb"].notna()
    d.loc[usar_fb, "publico"] = d.loc[usar_fb, "publico_fb"]
    d["publico_fonte"] = np.where(
        d["publico_bd"].notna(), "Base dos Dados",
        np.where(usar_fb, "FBref", "ausente"),
    )

    # 2008: zeros são falha de registro, não portão fechado.
    zerar_2008 = (d["season"] == 2008) & (d["publico"] == 0)
    d.loc[zerar_2008, "publico"] = np.nan
    d.loc[zerar_2008, "publico_fonte"] = "ausente (zero de 2008)"

    # 2020–2021: zeros reais (portões fechados/restrições).
    d["publico_zero_real"] = (d["publico"] == 0) & d["season"].isin([2020, 2021])

    # Árbitro: Base dos Dados primeiro; FBref como complemento.
    d["arbitro_bd"] = d["arbitro"].astype(str).str.strip().replace({"": None, "nan": None})
    d["arbitro_fb"] = d["referee"]
    d["arbitro"] = d["arbitro_bd"].where(d["arbitro_bd"].notna(), d["arbitro_fb"])
    d["arbitro_fonte"] = np.where(
        d["arbitro_bd"].notna(), "Base dos Dados",
        np.where(d["arbitro_fb"].notna(), "FBref", "ausente"),
    )

    d["publico_max"] = pd.to_numeric(d["publico_max"], errors="coerce")
    d["faltas_mandante"] = pd.to_numeric(d["faltas_mandante"], errors="coerce")
    d["faltas_visitante"] = pd.to_numeric(d["faltas_visitante"], errors="coerce")
    return d


def _qualidade(d: pd.DataFrame) -> dict:
    por_temporada = {}
    for season, g in d.groupby("season"):
        por_temporada[str(int(season))] = {
            "n": int(len(g)),
            "publico": int(g["publico"].notna().sum()),
            "publico_zero": int((g["publico"] == 0).sum()),
            "publico_zero_real": int(g["publico_zero_real"].sum()),
            "publico_bd": int((g["publico_fonte"] == "Base dos Dados").sum()),
            "publico_fbref": int((g["publico_fonte"] == "FBref").sum()),
            "arbitro": int(g["arbitro"].notna().sum()),
            "faltas": int(g["faltas_mandante"].notna().sum()),
        }
    return {
        "fonte": "Base dos Dados/Transfermarkt + FBref 2024",
        "n": int(len(d)),
        "publico": int(d["publico"].notna().sum()),
        "publico_zero": int((d["publico"] == 0).sum()),
        "arbitro": int(d["arbitro"].notna().sum()),
        "por_temporada": por_temporada,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=None)
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--qualidade", type=Path, default=QUALIDADE)
    args = parser.parse_args(argv)

    base = carregar_base() if args.base is None else carregar_base(args.base)
    bd = carregar_bd()
    fb = _fbref(FBREF)
    d = _limpar(_juntar(base, bd, fb))

    colunas = [
        "match_id", "season", "date", "home_team", "away_team",
        "home_goals", "away_goals", "result", "home_points", "away_points",
        "publico", "publico_max", "publico_zero_real", "publico_fonte",
        "arbitro", "arbitro_fonte", "faltas_mandante", "faltas_visitante",
    ]
    d[colunas].to_csv(args.out, index=False)

    q = _qualidade(d)
    args.qualidade.write_text(json.dumps(q, ensure_ascii=False, indent=2) + "\n",
                              encoding="utf-8")
    print(f"ok: {len(d)} partidas -> {args.out}")
    print(f"público: {q['publico']} ({q['publico']/len(d):.1%}); "
          f"zero real: {q['publico_zero']}; árbitro: {q['arbitro']}")
    print(pd.DataFrame(q["por_temporada"]).T.to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
