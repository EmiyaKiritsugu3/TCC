#!/usr/bin/env python3
"""Constrói a tabela de cartões por partida e junta à base do TCC.

Entrada:
  data/processed/matches_processed.csv
  data/external/cards/Serie_A_<ano>_games.json (2013–2024)

Saída:
  data/external/cards/cards_2013_2024.csv (local, não versionado)
  data/external/cards/QUALITY.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from cards import parse_partida
from paths import caminho_no_projeto

RAIZ = Path(__file__).resolve().parent.parent
BASE = RAIZ / "data" / "processed" / "matches_processed.csv"
PASTA = RAIZ / "data" / "external" / "cards"
SAIDA = PASTA / "cards_2013_2024.csv"
QUALIDADE = PASTA / "QUALITY.json"


def _cartoes(anos: list[int]) -> pd.DataFrame:
    linhas = []
    for ano in anos:
        caminho = PASTA / f"Serie_A_{ano}_games.json"
        if not caminho.exists():
            raise SystemExit(f"arquivo ausente: {caminho}; rode fetch_cards.py")
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        for chave, jogo in dados.items():
            item = parse_partida(jogo)
            item["season"] = ano
            item["jogo_fonte"] = chave
            linhas.append(item)
    return pd.DataFrame(linhas)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=BASE)
    parser.add_argument("--out", type=Path, default=SAIDA)
    parser.add_argument("--qualidade", type=Path, default=QUALIDADE)
    args = parser.parse_args(argv)
    base_path = caminho_no_projeto(args.base)
    out = caminho_no_projeto(args.out)
    qualidade_path = caminho_no_projeto(args.qualidade)

    base = pd.read_csv(base_path)
    if base["match_id"].duplicated().any():
        raise SystemExit("matches_processed.csv tem match_id duplicado")
    base["date"] = pd.to_datetime(base["date"]).dt.strftime("%Y-%m-%d")
    anos = [a for a in sorted(base["season"].unique().tolist()) if 2013 <= a <= 2024]
    cartoes = _cartoes(anos)
    cartoes["date"] = pd.to_datetime(cartoes["date"]).dt.strftime("%Y-%m-%d")

    chave_data = ["season", "date", "home_team", "away_team", "home_goals", "away_goals"]
    chave_dia = ["season", "date", "home_team", "away_team"]
    chave_time = ["season", "home_team", "away_team", "home_goals", "away_goals"]
    base_data = base[chave_data + ["match_id"]].copy()
    junto = cartoes.merge(base_data, on=chave_data, how="left",
                          indicator=True, validate="many_to_one")
    # Fallback 1: mesmo dia e equipes, mas placar divergente entre as fontes.
    sem = junto[junto["_merge"] == "left_only"].drop(columns=["match_id", "_merge"])
    if not sem.empty:
        alt = sem.merge(
            base[chave_dia + ["match_id"]].drop_duplicates(chave_dia),
            on=chave_dia, how="left", validate="many_to_one",
        )
        junto = pd.concat([junto[junto["_merge"] == "both"].drop(columns=["_merge"]), alt],
                          ignore_index=True)
    # Fallback 2: mesmas equipes e placar, mas data remarcada.
    sem = junto[junto["match_id"].isna()].drop(columns=["match_id"])
    if not sem.empty:
        alt = sem.merge(
            base[chave_time + ["match_id"]].drop_duplicates(chave_time),
            on=chave_time, how="left", validate="many_to_one",
        )
        junto = pd.concat([junto[junto["match_id"].notna()], alt], ignore_index=True)

    junto = junto.dropna(subset=["match_id"]).copy()
    junto["match_id"] = junto["match_id"].astype(int)
    repetidos = junto.loc[junto["match_id"].duplicated(), "match_id"].unique()
    if len(repetidos):
        raise SystemExit(
            "junção de cartões duplicou match_id: "
            + ", ".join(str(x) for x in sorted(repetidos)[:10])
        )
    # A data canônica é sempre a da base; o fallback por equipes+placar pode
    # casar uma partida remarcada e não deve manter a data antiga da fonte.
    datas_base = base[["match_id", "date"]].rename(columns={"date": "date_base"})
    junto = junto.merge(datas_base, on="match_id", how="left", validate="many_to_one")
    junto["date"] = junto["date_base"]
    junto = junto.drop(columns=["date_base"])
    junto["placar_fonte"] = (junto["home_goals"].astype(int).astype(str)
                             + " X " + junto["away_goals"].astype(int).astype(str))
    base_placar = base[["match_id", "home_goals", "away_goals"]].rename(
        columns={"home_goals": "home_goals_base", "away_goals": "away_goals_base"})
    junto = junto.merge(base_placar, on="match_id", how="left", validate="many_to_one")
    divergencias = junto[
        (junto["home_goals"] != junto["home_goals_base"])
        | (junto["away_goals"] != junto["away_goals_base"])
    ][["match_id", "season", "date", "home_team", "away_team",
       "placar_fonte", "home_goals_base", "away_goals_base"]]
    junto["home_goals"] = junto["home_goals_base"]
    junto["away_goals"] = junto["away_goals_base"]
    junto = junto.sort_values(["season", "date", "home_team"]).reset_index(drop=True)
    colunas = ["match_id", "season", "date", "home_team", "away_team",
               "home_goals", "away_goals", "placar_fonte", "yellow_home",
               "yellow_away", "red_home", "red_away", "pen_home", "pen_away",
               "pen_nao_atribuidos", "nao_atribuidos", "cartoes_total",
               "jogo_fonte"]
    junto = junto[colunas]
    out.parent.mkdir(parents=True, exist_ok=True)
    junto.to_csv(out, index=False)
    cobertura = {}
    for season, grupo in junto.groupby("season"):
        base_n = int((base["season"] == season).sum())
        cobertura[str(int(season))] = {
            "base": base_n,
            "cartoes": int(len(grupo)),
            "cobertura": round(len(grupo) / base_n, 4) if base_n else None,
            "nao_atribuidos": int(grupo["nao_atribuidos"].sum()),
            "amarelos": int(grupo["yellow_home"].sum() + grupo["yellow_away"].sum()),
            "vermelhos": int(grupo["red_home"].sum() + grupo["red_away"].sum()),
            "penaltis": int(grupo["pen_home"].sum() + grupo["pen_away"].sum()),
        }
    elegiveis = base[base["season"].between(2013, 2024)]
    qualidade = {
        "fonte": "BrazilianFootball/Data",
        "partidas_base": int(len(base)),
        "partidas_elegiveis_2013_2024": int(len(elegiveis)),
        "partidas_com_cartoes": int(len(junto)),
        "cobertura": round(len(junto) / len(base), 4),
        "cobertura_2013_2024": round(len(junto) / len(elegiveis), 4),
        "anos_sem_fonte": [2006, 2007, 2008, 2009, 2010, 2011, 2012],
        "nao_atribuidos": int(junto["nao_atribuidos"].sum()),
        "penaltis_nao_atribuidos": int(junto["pen_nao_atribuidos"].sum()),
        "divergencias_placar": divergencias.to_dict(orient="records"),
        "por_temporada": cobertura,
    }
    qualidade_path.parent.mkdir(parents=True, exist_ok=True)
    qualidade_path.write_text(json.dumps(qualidade, ensure_ascii=False, indent=2) + "\n",
                              encoding="utf-8")
    print(f"ok: {len(junto)} partidas com cartões -> {out}")
    print(f"cobertura: {qualidade['cobertura']:.1%}; "
          f"não atribuídos: {qualidade['nao_atribuidos']}")
    print(pd.DataFrame(cobertura).T.to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
