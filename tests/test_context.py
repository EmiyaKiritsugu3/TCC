"""Testes das variáveis contextuais descritivas (Fase 1)."""
from pathlib import Path

import pandas as pd
import pytest

from context import (
    CLUB_COORDS,
    add_era_flags,
    haversine_km,
    rest_days,
    table_snapshot,
    travel_km,
)

PROCESSED = Path(__file__).resolve().parent.parent / "data" / "processed" / "matches_processed.csv"


def test_haversine_sao_paulo_rio():
    d = haversine_km(-23.55, -46.63, -22.91, -43.17)
    assert 340 < d < 380


def test_haversine_zero_mesma_cidade():
    assert haversine_km(-23.55, -46.63, -23.55, -46.63) == 0.0


def test_coordenadas_cobrem_todos_os_clubes():
    d = pd.DataFrame({
        "home_team": ["Flamengo", "Corinthians"],
        "away_team": ["Fluminense", "Palmeiras"],
    })
    for t in set(d["home_team"]) | set(d["away_team"]):
        assert t in CLUB_COORDS


def test_d_classico_mesma_cidade_zero():
    d = pd.DataFrame({
        "home_team": ["Flamengo", "Corinthians"],
        "away_team": ["Fluminense", "Sao Paulo"],
    })
    t = travel_km(d)
    assert (t == 0.0).all()


def test_distancia_interestadual_na_faixa_esperada():
    d = pd.DataFrame({"home_team": ["Sao Paulo"], "away_team": ["Flamengo"]})
    t = travel_km(d).iloc[0]
    assert 340 < t < 380


def test_descanso_em_dias():
    d = pd.DataFrame({
        "date": pd.to_datetime(["2020-08-08", "2020-08-12", "2020-08-12"]),
        "home_team": ["A", "A", "B"],
        "away_team": ["B", "C", "C"],
    })
    r = rest_days(d)
    assert pd.isna(r["home_rest"].iloc[0])  # estreia de A: sem anterior
    assert r["home_rest"].iloc[1] == 4      # A jogou 4 dias antes
    assert r["away_rest"].iloc[2] == 0      # C jogou no mesmo dia


def test_posicao_na_tabela_antes_da_partida():
    d = pd.DataFrame({
        "season": [2019, 2019, 2019],
        "date": pd.to_datetime(["2019-04-27", "2019-04-28", "2019-05-01"]),
        "round": [1, 1, 2],
        "match_id": ["1", "2", "3"],
        "home_team": ["A", "C", "A"],
        "away_team": ["B", "D", "C"],
        "home_goals": [2, 1, 0],
        "away_goals": [0, 1, 1],
    })
    s = table_snapshot(d)
    # rodada 2: A tem 3 pts (líder isolado entre os 4), C tem 1 pt
    assert s["home_pts_before"].iloc[2] == 3
    assert s["away_pts_before"].iloc[2] == 1
    assert s["home_pos_before"].iloc[2] == 1
    assert s["away_pos_before"].iloc[2] > 1


def test_flags_de_era():
    d = pd.DataFrame({"season": [2018, 2019, 2020, 2021, 2022]})
    f = add_era_flags(d)
    assert f["var_era"].tolist() == [False, True, True, True, True]
    assert f["pandemia"].tolist() == [False, False, True, True, False]


@pytest.mark.skipif(not PROCESSED.exists(), reason="rode scripts/build_processed.py")
def test_base_real_coberta_e_soma_confere():
    df = pd.read_csv(PROCESSED)
    falta = (set(df["home_team"]) | set(df["away_team"])) - set(CLUB_COORDS)
    assert falta == set()
    t = travel_km(df)
    assert len(t) == 7219 and (t >= 0).all()
    r = rest_days(df)
    assert (r["home_rest"].fillna(0) >= 0).all()
