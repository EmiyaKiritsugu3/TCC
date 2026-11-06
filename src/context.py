"""Variáveis contextuais descritivas (Fase 1). Funções puras sobre a base limpa.

Nada aqui altera placar, mando ou resultado: apenas descreve o contexto de
cada partida (viagem, descanso, força na tabela, era). Coordenadas aproximadas
de cidade (~0,1 grau); a análise usa faixas de distância, robustas a isso.
"""
from __future__ import annotations

import math

import pandas as pd

# Clube -> (latitude, longitude) da cidade-sede. Aproximadas; suficientes
# para faixas de distância (<500, 500–1500, >1500 km).
CLUB_COORDS: dict[str, tuple[float, float]] = {
    "America-MG": (-19.92, -43.94),
    "America-RN": (-5.79, -35.21),
    "Athletico-PR": (-25.43, -49.27),
    "Atletico-GO": (-16.68, -49.25),
    "Atletico-MG": (-19.92, -43.94),
    "Avai": (-27.60, -48.55),
    "Bahia": (-12.97, -38.50),
    "Barueri": (-23.51, -46.88),
    "Botafogo-RJ": (-22.91, -43.17),
    "Bragantino": (-22.95, -46.54),
    "CSA": (-9.67, -35.74),
    "Ceara": (-3.73, -38.52),
    "Chapecoense": (-27.10, -52.62),
    "Corinthians": (-23.55, -46.63),
    "Coritiba": (-25.43, -49.27),
    "Criciuma": (-28.68, -49.38),
    "Cruzeiro": (-19.92, -43.94),
    "Cuiaba": (-15.60, -56.10),
    "Figueirense": (-27.60, -48.55),
    "Flamengo": (-22.91, -43.17),
    "Fluminense": (-22.91, -43.17),
    "Fortaleza": (-3.73, -38.52),
    "Goias": (-16.68, -49.25),
    "Gremio": (-30.03, -51.23),
    "Gremio Prudente": (-22.12, -51.39),
    "Guarani": (-22.91, -47.06),
    "Internacional": (-30.03, -51.23),
    "Ipatinga": (-19.47, -42.54),
    "Joinville": (-26.30, -48.84),
    "Juventude": (-29.17, -51.18),
    "Nautico": (-8.05, -34.88),
    "Palmeiras": (-23.55, -46.63),
    "Parana": (-25.43, -49.27),
    "Ponte Preta": (-22.91, -47.06),
    "Portuguesa": (-23.55, -46.63),
    "Santa Cruz": (-8.05, -34.88),
    "Santo Andre": (-23.66, -46.53),
    "Santos": (-23.96, -46.33),
    "Sao Caetano": (-23.62, -46.55),
    "Sao Paulo": (-23.55, -46.63),
    "Sport": (-8.05, -34.88),
    "Vasco": (-22.91, -43.17),
    "Vitoria": (-12.97, -38.50),
}


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distância ortodrômica em km. Mesmo ponto -> 0.0."""
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def travel_km(df: pd.DataFrame) -> pd.Series:
    """Distância da cidade do visitante à do mandante, em km.

    Clássicos na mesma cidade -> 0.0 (deslocamento interurbano nulo).
    """
    out = []
    for h, a in zip(df["home_team"], df["away_team"]):
        hla, hlo = CLUB_COORDS[h]
        ala, alo = CLUB_COORDS[a]
        out.append(0.0 if (hla, hlo) == (ala, alo) else haversine_km(hla, hlo, ala, alo))
    return pd.Series(out, index=df.index, dtype=float)


def rest_days(df: pd.DataFrame) -> pd.DataFrame:
    """Dias desde a partida anterior de cada clube (qualquer mando).

    Primeira aparição do clube na base -> NaN. Mesmo dia -> 0.
    """
    d = df.copy()
    d["date"] = pd.to_datetime(d["date"])
    d = d.sort_values("date", kind="mergesort")
    ultimo: dict[str, pd.Timestamp] = {}
    hr, ar = [], []
    for _, linha in d.iterrows():
        for clube, lista in ((linha["home_team"], hr), (linha["away_team"], ar)):
            prev = ultimo.get(clube)
            lista.append(float((linha["date"] - prev).days) if prev is not None else math.nan)
        ultimo[linha["home_team"]] = linha["date"]
        ultimo[linha["away_team"]] = linha["date"]
    d["home_rest"] = pd.Series(hr, index=d.index, dtype=float)
    d["away_rest"] = pd.Series(ar, index=d.index, dtype=float)
    return d.loc[df.index, ["home_rest", "away_rest"]]


def table_snapshot(df: pd.DataFrame) -> pd.DataFrame:
    """Pontos e posição de cada lado ANTES da partida, por temporada.

    Ordena por (data, rodada, match_id); desempate de posição por
    pontos, vitórias e saldo, nesta ordem; empates dividem a posição
    (`method="min"`). Estreantes na temporada partem de zero.
    """
    d = df.copy()
    d["date"] = pd.to_datetime(d["date"])
    ordem = d.sort_values(["season", "date", "round", "match_id"],
                         kind="mergesort").index
    pts: dict[tuple, dict[str, list]] = {}
    hp, ap, hpos, apos = [], [], [], []
    for i in ordem:
        lin = d.loc[i]
        s = lin["season"]
        if s not in pts:
            pts[s] = {}
        tab = pts[s]
        for clube in (lin["home_team"], lin["away_team"]):
            tab.setdefault(clube, [0, 0, 0])
        hp.append(tab[lin["home_team"]][0])
        ap.append(tab[lin["away_team"]][0])
        quadro = pd.DataFrame(
            [(c, v[0], v[1], v[2]) for c, v in tab.items()],
            columns=["clube", "p", "v", "sg"],
        ).sort_values(["p", "v", "sg"], ascending=False, kind="mergesort")
        quadro["pos"] = quadro[["p", "v", "sg"]].apply(tuple, axis=1).rank(
            method="min", ascending=False).astype(int)
        pos = dict(zip(quadro["clube"], quadro["pos"]))
        hpos.append(pos[lin["home_team"]])
        apos.append(pos[lin["away_team"]])
        hg, ag = lin["home_goals"], lin["away_goals"]
        if hg > ag:
            tab[lin["home_team"]][0] += 3
            tab[lin["home_team"]][1] += 1
        elif hg < ag:
            tab[lin["away_team"]][0] += 3
            tab[lin["away_team"]][1] += 1
        else:
            tab[lin["home_team"]][0] += 1
            tab[lin["away_team"]][0] += 1
        tab[lin["home_team"]][2] += hg - ag
        tab[lin["away_team"]][2] += ag - hg
    out = pd.DataFrame({
        "home_pts_before": pd.Series(hp, index=ordem, dtype=int),
        "away_pts_before": pd.Series(ap, index=ordem, dtype=int),
        "home_pos_before": pd.Series(hpos, index=ordem, dtype=int),
        "away_pos_before": pd.Series(apos, index=ordem, dtype=int),
    })
    return out.loc[df.index]


def add_era_flags(df: pd.DataFrame) -> pd.DataFrame:
    """Marcadores descritivos de era (sem leitura causal).

    `var_era`: temporada >= 2019 (estreia do VAR na Série A).
    `pandemia`: temporadas 2020–2021 (portões fechados/parciais, calendário atípico).
    """
    d = df.copy()
    d["var_era"] = d["season"] >= 2019
    d["pandemia"] = d["season"].isin([2020, 2021])
    return d
