"""Testes das variáveis contextuais descritivas (Fase 1)."""
from pathlib import Path

import pandas as pd
import pytest

from context import (
    CLUB_COORDS,
    CLUB_STATE,
    add_era_flags,
    build_context_frame,
    haversine_km,
    region,
    rest_bucket,
    rest_days,
    same_state,
    table_bucket,
    table_snapshot,
    travel_km,
    usual_stadium,
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


@pytest.mark.integration
@pytest.mark.skipif(not PROCESSED.exists(), reason="rode scripts/build_processed.py")
def test_base_real_coberta_e_soma_confere():
    df = pd.read_csv(PROCESSED)
    falta = (set(df["home_team"]) | set(df["away_team"])) - set(CLUB_COORDS)
    assert falta == set()
    t = travel_km(df)
    assert len(t) == 7219 and (t >= 0).all()
    r = rest_days(df)
    assert (r["home_rest"].fillna(0) >= 0).all()


def test_travel_km_clube_nao_mapeado_falha():
    df = pd.DataFrame([{"home_team": "Flamengo", "away_team": "Clube Inexistente"}])
    with pytest.raises(ValueError, match="Clube Inexistente"):
        travel_km(df)


def test_estados_cobrem_todos_os_clubes_com_coordenadas():
    assert set(CLUB_STATE) == set(CLUB_COORDS)


def test_same_state_e_regiao():
    d = pd.DataFrame({
        "home_team": ["Flamengo", "Flamengo", "Bahia", "Gremio", "Cuiaba"],
        "away_team": ["Fluminense", "Corinthians", "Vitoria", "Internacional", "Goias"],
    })
    assert same_state(d).tolist() == [True, False, True, True, False]
    assert region(d, "home").tolist() == ["SE", "SE", "NE", "S", "CO"]
    assert region(d, "away").tolist() == ["SE", "SE", "NE", "S", "CO"]


def test_region_estado_desconhecido_falha():
    d = pd.DataFrame({"home_team": ["Paysandu"], "away_team": ["Flamengo"]})
    with pytest.raises(ValueError, match="Paysandu"):
        region(d, "home")


def test_usual_stadium_desempata_por_ordem_alfabetica():
    d = pd.DataFrame({
        "season": [2019, 2019, 2019, 2019, 2019],
        "home_team": ["A", "A", "A", "B", "B"],
        "stadium": ["X", "X", "Y", "Y", "X"],
    })
    assert usual_stadium(d).tolist() == [True, True, False, False, True]


def test_rest_bucket_cobre_as_faixas_e_ignora_ausente():
    d = pd.DataFrame({
        "home_rest": [5, 5, 1, 0, 0, 4, 5, None],
        "away_rest": [2, 2, 0, 1, 2, 5, 1, 2],
    })
    got = rest_bucket(d).tolist()
    assert got == ["casa +3", "casa +3", "casa +1-2", "fora +1-2",
                   "fora +1-2", "fora +1-2", "casa +3", None]


def test_table_bucket_usa_margem_de_tres_posicoes():
    d = pd.DataFrame({
        "home_pos_before": [1, 5, 10, 10, 6, 10, None],
        "away_pos_before": [10, 5, 1, 6, 10, 7, 2],
    })
    assert table_bucket(d).tolist() == [
        "favorito", "equilibrado", "zebra", "zebra", "favorito", "equilibrado", None,
    ]


def test_build_context_frame_monta_variaveis_derivadas():
    d = pd.DataFrame({
        "season": [2019, 2019],
        "date": pd.to_datetime(["2019-04-27", "2019-04-28"]),
        "round": [1, 1],
        "match_id": ["1", "2"],
        "home_team": ["Flamengo", "Corinthians"],
        "away_team": ["Fluminense", "Sao Paulo"],
        "home_goals": [2, 1],
        "away_goals": [0, 0],
        "home_points": [3, 1],
        "away_points": [0, 1],
        "stadium": ["Maracana", "Arena Corinthians"],
    })
    c = build_context_frame(d)
    assert c["derby"].tolist() == [True, True]
    assert c["same_state"].tolist() == [True, True]
    assert c["home_region"].tolist() == ["SE", "SE"]
    assert c["usual_stadium"].tolist() == [True, True]
    assert c["rest_bucket"].isna().all()
    assert c["table_bucket"].notna().all()
    assert c["var_era"].all()
