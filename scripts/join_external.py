#!/usr/bin/env python3
"""Junta a base do TCC às fontes externas de público e arbitragem.

Entradas:
  data/processed/matches_processed.csv
  data/external/basedosdados/brasileirao_serie_a_2006_2024.csv
  data/external/fbref/2024_serie_a.csv (opcional, validação)

Saída:
  data/external/joined_context.csv (local; não versionado)

A junção usa temporada + mandante + visitante + placar, porque as datas
das fontes divergem em jogos remarcados. Os nomes dos clubes passam por
um mapa de aliases; o caso Barueri/Grêmio Prudente (2010) é tratado.
"""
from __future__ import annotations

import argparse
import re
import unicodedata
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
BASE = RAIZ / "data" / "processed" / "matches_processed.csv"
BD = RAIZ / "data" / "external" / "basedosdados" / "brasileirao_serie_a_2006_2024.csv"
FBREF = RAIZ / "data" / "external" / "fbref" / "2024_serie_a.csv"
OUT = RAIZ / "data" / "external" / "joined_context.csv"

# Nome normalizado na fonte -> nome canônico da base do TCC.
ALIASES_BD = {
    "america mg": "America-MG", "america rn": "America-RN",
    "athletico pr": "Athletico-PR", "atletico pr": "Athletico-PR",
    "atletico go": "Atletico-GO", "atletico mg": "Atletico-MG",
    "avai fc": "Avai", "barueri": "Barueri", "botafogo": "Botafogo-RJ",
    "rb bragantino": "Bragantino", "bragantino": "Bragantino", "csa": "CSA",
    "ceara sc": "Ceara", "chapecoense": "Chapecoense",
    "corinthians": "Corinthians", "coritiba fc": "Coritiba",
    "criciuma ec": "Criciuma", "cruzeiro": "Cruzeiro",
    "cuiaba mt": "Cuiaba", "figueirense fc": "Figueirense",
    "flamengo": "Flamengo", "fluminense": "Fluminense",
    "fortaleza": "Fortaleza", "goias": "Goias", "goias ec": "Goias",
    "gremio": "Gremio", "guarani": "Guarani", "internacional": "Internacional",
    "ipatinga fc": "Ipatinga", "joinville sc": "Joinville",
    "juventude": "Juventude", "nautico": "Nautico", "palmeiras": "Palmeiras",
    "parana": "Parana", "ponte preta": "Ponte Preta",
    "portuguesa": "Portuguesa", "santa cruz": "Santa Cruz",
    "santo andre": "Santo Andre", "santos": "Santos", "santos fc": "Santos",
    "sao caetano": "Sao Caetano", "sao paulo": "Sao Paulo",
    "sport recife": "Sport", "vasco da gama": "Vasco",
    "vitoria": "Vitoria", "ec vitoria": "Vitoria", "ec bahia": "Bahia",
}

ALIASES_FBREF = {
    "athletico pr": "Athletico-PR", "atletico paranaense": "Athletico-PR",
    "atletico mineiro": "Atletico-MG", "atletico mg": "Atletico-MG",
    "atl goianiense": "Atletico-GO", "atletico goianiense": "Atletico-GO",
    "atletico go": "Atletico-GO", "botafogo": "Botafogo-RJ",
    "botafogo rj": "Botafogo-RJ", "rb bragantino": "Bragantino",
    "red bull bragantino": "Bragantino", "bragantino": "Bragantino",
    "vasco da gama": "Vasco", "sao paulo": "Sao Paulo",
    "gremio": "Gremio", "internacional": "Internacional",
    "corinthians": "Corinthians", "palmeiras": "Palmeiras",
    "santos": "Santos", "flamengo": "Flamengo", "fluminense": "Fluminense",
    "cruzeiro": "Cruzeiro", "fortaleza": "Fortaleza", "bahia": "Bahia",
    "juventude": "Juventude", "criciuma": "Criciuma", "cuiaba": "Cuiaba",
    "coritiba": "Coritiba", "mirassol": "Mirassol", "vitoria": "Vitoria",
    "sport recife": "Sport", "sport": "Sport",
}


def normalizar(nome: object) -> str:
    texto = (str(nome).replace("–", "-").replace("—", "-").replace("−", "-"))
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", texto).strip()


def canonico(nome: object, aliases: dict[str, str]) -> str | None:
    return aliases.get(normalizar(nome))


def carregar_base(caminho: Path = BASE) -> pd.DataFrame:
    base = pd.read_csv(caminho)
    base["date"] = pd.to_datetime(base["date"])
    return base


def carregar_bd(caminho: Path = BD) -> pd.DataFrame:
    bd = pd.read_csv(caminho)
    bd["season"] = bd["ano_campeonato"].astype(int)
    bd["home_bd"] = bd["time_mandante"].map(lambda x: canonico(x, ALIASES_BD))
    bd["away_bd"] = bd["time_visitante"].map(lambda x: canonico(x, ALIASES_BD))
    # Barueri (2009) e Grêmio Prudente (2010) são a mesma franquia renomeada.
    em_2010 = bd["season"] == 2010
    bd.loc[em_2010, "home_bd"] = bd.loc[em_2010, "home_bd"].replace({"Barueri": "Gremio Prudente"})
    bd.loc[em_2010, "away_bd"] = bd.loc[em_2010, "away_bd"].replace({"Barueri": "Gremio Prudente"})
    bd["data_bd"] = pd.to_datetime(bd["data"], errors="coerce")
    return bd


def juntar(base: pd.DataFrame, bd: pd.DataFrame) -> pd.DataFrame:
    chaves = ["season", "home_team", "away_team", "home_goals", "away_goals"]
    bd_unico = bd.drop_duplicates(
        subset=["season", "home_bd", "away_bd", "gols_mandante", "gols_visitante"]
    )
    saida = base.merge(
        bd_unico[[
            "season", "home_bd", "away_bd", "gols_mandante", "gols_visitante",
            "data_bd", "publico", "publico_max", "arbitro",
            "faltas_mandante", "faltas_visitante",
        ]],
        left_on=chaves,
        right_on=["season", "home_bd", "away_bd", "gols_mandante", "gols_visitante"],
        how="left",
        indicator=True,
        validate="many_to_one",
    )
    return saida


def relatorio_cobertura(junto: pd.DataFrame) -> pd.DataFrame:
    linhas = []
    for season, grupo in junto.groupby("season"):
        linhas.append({
            "season": int(season),
            "n": len(grupo),
            "com_bd": int((grupo["_merge"] == "both").sum()),
            "publico": int(grupo["publico"].notna().sum()),
            "publico_zero": int((grupo["publico"] == 0).sum()),
            "arbitro": int(grupo["arbitro"].notna().sum()),
            "faltas": int(grupo["faltas_mandante"].notna().sum()),
        })
    return pd.DataFrame(linhas)


def validar_fbref(junto: pd.DataFrame, fbref: pd.DataFrame) -> dict:
    fb = fbref.copy()
    fb["home_fb"] = fb["home"].map(lambda x: canonico(x, ALIASES_FBREF))
    fb["away_fb"] = fb["away"].map(lambda x: canonico(x, ALIASES_FBREF))
    pares = junto.merge(
        fb[["season", "home_fb", "away_fb", "home_goals", "away_goals",
            "attendance", "referee"]],
        left_on=["season", "home_team", "away_team", "home_goals", "away_goals"],
        right_on=["season", "home_fb", "away_fb", "home_goals", "away_goals"],
        how="inner",
        suffixes=("", "_fb"),
        validate="many_to_one",
    )
    ambos = pares.dropna(subset=["publico", "attendance"])
    diferenca = (ambos["publico"] - ambos["attendance"]).abs()
    return {
        "jogos_fbref": len(fb),
        "overlap": len(pares),
        "pares_publico": len(ambos),
        "iguais": int((diferenca == 0).sum()),
        "ate_100": int((diferenca <= 100).sum()),
        "ate_1000": int((diferenca <= 1000).sum()),
        "media_diferenca": float(diferenca.mean()) if len(diferenca) else None,
        "referee_fbref": int(pares["referee"].notna().sum()),
        "referee_bd": int(pares["arbitro"].notna().sum()),
        "pares": pares,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=BASE)
    parser.add_argument("--bd", type=Path, default=BD)
    parser.add_argument("--fbref", type=Path, default=FBREF)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args(argv)

    base = carregar_base(args.base)
    bd = carregar_bd(args.bd)
    junto = juntar(base, bd)
    cobertura = relatorio_cobertura(junto)

    colunas = [
        "match_id", "season", "date", "home_team", "away_team",
        "home_goals", "away_goals", "publico", "publico_max", "arbitro",
        "faltas_mandante", "faltas_visitante", "_merge",
    ]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    junto[colunas].to_csv(args.out, index=False)

    print(f"partidas: {len(junto)}; com BD: {(junto['_merge'] == 'both').sum()}")
    print(cobertura.to_string(index=False))
    print(f"-> {args.out}")

    if args.fbref.exists():
        fbref = pd.read_csv(args.fbref)
        validacao = validar_fbref(junto, fbref)
        print("\nValidação FBref:")
        for chave in ("jogos_fbref", "overlap", "pares_publico", "iguais",
                      "ate_100", "ate_1000", "media_diferenca"):
            print(f"  {chave}: {validacao[chave]}")
        print(f"  árbitro FBref/BD: {validacao['referee_fbref']}/{validacao['referee_bd']}")
    else:
        print("\nFBref ausente; validação de público não executada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
