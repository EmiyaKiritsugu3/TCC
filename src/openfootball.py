"""Parser do formato Football.TXT do OpenFootball + mapa p/ nomes canônicos.

Fonte CC0-1.0: https://github.com/openfootball/south-america (pasta brazil).
Uso neste TCC: validação cruzada 2018–2024 da base primária (adaoduque).
"""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import pandas as pd

MESES = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
         "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}

RE_DATA = re.compile(r"^\s*(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+(\w{3})\s+(\d{1,2})(?:\s+(\d{4}))?\s*$")
RE_JOGO = re.compile(r"^\s*(?:\d{1,2}:\d{2}\s+)?(.+?)\s+[vV]\s+(.+?)\s+(\d+)\s*-\s*(\d+)(?:\s+\(.*\))?\s*$")
RE_RODADA = re.compile(r"Matchday\s+(\d+)", re.IGNORECASE)


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip()


# Chave = nome normalizado (sem acento) -> nome canônico da base primária.
MAPA_TIMES = {
    "America MG": "America-MG", "America Mineiro": "America-MG",
    "Athletico Paranaense": "Athletico-PR", "CA Paranaense": "Athletico-PR",
    "Atletico Goianiense": "Atletico-GO", "AC Goianiense": "Atletico-GO",
    "Atletico Mineiro": "Atletico-MG", "CA Mineiro": "Atletico-MG",
    "Avai SC": "Avai",
    "EC Bahia": "Bahia", "Bahia BA": "Bahia",
    "Botafogo FR": "Botafogo-RJ", "Botafogo RJ": "Botafogo-RJ",
    "RB Bragantino": "Bragantino", "Red Bull Bragantino": "Bragantino",
    "CSA AL": "CSA",
    "Ceara CE": "Ceara",
    "Chapecoense": "Chapecoense",
    "SC Corinthians Paulista": "Corinthians", "Corinthians SP": "Corinthians",
    "Coritiba FBC": "Coritiba", "Coritiba PR": "Coritiba",
    "Criciuma EC": "Criciuma",
    "Cruzeiro": "Cruzeiro", "Cruzeiro EC": "Cruzeiro",
    "Cuiaba EC": "Cuiaba", "Cuiaba MT": "Cuiaba",
    "CR Flamengo": "Flamengo", "Flamengo RJ": "Flamengo",
    "Fluminense FC": "Fluminense", "Fluminense RJ": "Fluminense",
    "Fortaleza CE": "Fortaleza", "Fortaleza EC": "Fortaleza",
    "Goias EC": "Goias", "Goias GO": "Goias",
    "Gremio FBPA": "Gremio", "Gremio Porto Alegre": "Gremio",
    "SC Internacional": "Internacional", "Internacional": "Internacional",
    "EC Juventude": "Juventude", "Juventude RS": "Juventude",
    "SE Palmeiras": "Palmeiras", "Palmeiras": "Palmeiras",
    "Parana Clube": "Parana",
    "Santos FC": "Santos",
    "Sao Paulo FC": "Sao Paulo",
    "Sport Recife PE": "Sport",
    "CR Vasco da Gama": "Vasco", "Vasco da Gama RJ": "Vasco",
    "EC Vitoria": "Vitoria", "Vitoria BA": "Vitoria",
}


def parse_arquivo(path: str | Path, temporada: int) -> pd.DataFrame:
    """Lê um `AAAA_br1.txt` e devolve (date, home_team, away_team, hg, ag, round)."""
    linhas = Path(path).read_text(encoding="utf-8").splitlines()
    jogos: list[dict] = []
    rodada: int | None = None
    ano_corrente = temporada
    mes_atual: int | None = None

    for ln in linhas:
        m_rod = RE_RODADA.search(ln)
        if m_rod and "Matchday" in ln:
            rodada = int(m_rod.group(1))
            continue
        m_dt = RE_DATA.match(ln)
        if m_dt:
            mon, dia, ano = m_dt.group(1), int(m_dt.group(2)), m_dt.group(3)
            mes = MESES[mon]
            if ano is not None:
                ano_corrente = int(ano)
            else:
                # Janeiro/fevereiro após dezembro = virada de ano (caso 2020→2021).
                if mes_atual == 12 and mes in (1, 2, 3):
                    ano_corrente += 1
                elif mes in (1, 2) and temporada == 2020:
                    ano_corrente = 2021
                else:
                    ano_corrente = temporada
            mes_atual = mes
            data_iso = f"{ano_corrente:04d}-{mes:02d}-{dia:02d}"
            continue
        m_jg = RE_JOGO.match(ln)
        if m_jg and "Matchday" not in ln and "v" in ln.lower():
            casa_raw, fora_raw = _norm(m_jg.group(1)), _norm(m_jg.group(2))
            if casa_raw not in MAPA_TIMES or fora_raw not in MAPA_TIMES:
                raise ValueError(f"Time sem mapeamento em {path}: {casa_raw!r} x {fora_raw!r}")
            jogos.append({
                "date": data_iso,
                "home_team": MAPA_TIMES[casa_raw],
                "away_team": MAPA_TIMES[fora_raw],
                "home_goals": int(m_jg.group(3)),
                "away_goals": int(m_jg.group(4)),
                "round": rodada,
            })

    df = pd.DataFrame(jogos)
    df["season"] = temporada
    return df[["season", "date", "round", "home_team", "away_team", "home_goals", "away_goals"]]


def comparar(base: pd.DataFrame, aberta: pd.DataFrame) -> dict:
    """Compara por (date, home_team, away_team); placares confrontados em seguida."""
    chave = ["date", "home_team", "away_team"]
    b = base.copy()
    a = aberta.copy()
    m = b.merge(a, on=chave, how="outer", suffixes=("_base", "_of"), indicator=True)
    ambos = m[m["_merge"] == "both"]
    placar_ok = ((ambos["home_goals_base"] == ambos["home_goals_of"])
                 & (ambos["away_goals_base"] == ambos["away_goals_of"])).sum()
    div = ambos[(ambos["home_goals_base"] != ambos["home_goals_of"])
                | (ambos["away_goals_base"] != ambos["away_goals_of"])]
    return {
        "n_base": int((m["_merge"] != "right_only").sum()),
        "n_of": int((m["_merge"] != "left_only").sum()),
        "em_ambas": int(len(ambos)),
        "placar_igual": int(placar_ok),
        "placar_divergente": int(len(div)),
        "so_na_base": m[m["_merge"] == "left_only"][chave + ["home_goals_base", "away_goals_base"]],
        "so_na_of": m[m["_merge"] == "right_only"][chave + ["home_goals_of", "away_goals_of"]],
        "divergencias": div[chave + ["home_goals_base", "away_goals_base",
                                     "home_goals_of", "away_goals_of"]],
    }
