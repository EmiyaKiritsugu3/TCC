"""Parser Football.TXT do OpenFootball e comparacao com a base primaria."""
from pathlib import Path

import pandas as pd
import pytest

from openfootball import comparar, parse_arquivo

DATA = Path(__file__).resolve().parent / "data"


def test_parse_arquivo_mapeia_nomes_datas_rodadas_e_virada_de_ano():
    df = parse_arquivo(DATA / "openfootball_2020.txt", 2020)
    assert list(df.columns) == [
        "season", "date", "round", "home_team", "away_team",
        "home_goals", "away_goals",
    ]
    assert df.to_dict("records") == [
        {"season": 2020, "date": "2020-12-05", "round": 30, "home_team": "Flamengo",
         "away_team": "Santos", "home_goals": 2, "away_goals": 1},
        {"season": 2020, "date": "2020-12-05", "round": 30, "home_team": "Sao Paulo",
         "away_team": "Corinthians", "home_goals": 0, "away_goals": 0},
        {"season": 2020, "date": "2020-12-20", "round": 33, "home_team": "Vasco",
         "away_team": "Fluminense", "home_goals": 1, "away_goals": 3},
        {"season": 2020, "date": "2021-01-30", "round": 1, "home_team": "Gremio",
         "away_team": "Bahia", "home_goals": 2, "away_goals": 2},
    ]


def test_parse_arquivo_virada_de_ano_especial_2020():
    df = parse_arquivo(DATA / "openfootball_virada_2020.txt", 2020)
    assert df["date"].tolist() == ["2021-02-26"]
    assert df["round"].tolist() == [34]


def test_parse_arquivo_time_sem_mapeamento_rejeitado():
    with pytest.raises(ValueError, match="Time sem mapeamento") as exc:
        parse_arquivo(DATA / "openfootball_unmapped.txt", 2020)
    assert "Unknown FC" in str(exc.value)


def test_comparar_contabiliza_divergentes_e_exclusivos():
    base = pd.DataFrame([
        {"date": "2019-05-05", "home_team": "A", "away_team": "B",
         "home_goals": 1, "away_goals": 0},
        {"date": "2019-05-06", "home_team": "C", "away_team": "D",
         "home_goals": 2, "away_goals": 2},
    ])
    aberta = pd.DataFrame([
        {"date": "2019-05-05", "home_team": "A", "away_team": "B",
         "home_goals": 0, "away_goals": 0},
        {"date": "2019-05-07", "home_team": "E", "away_team": "F",
         "home_goals": 1, "away_goals": 1},
    ])
    r = comparar(base, aberta)
    assert (r["n_base"], r["n_of"], r["em_ambas"]) == (2, 2, 1)
    assert (r["placar_igual"], r["placar_divergente"]) == (0, 1)
    assert r["so_na_base"]["home_team"].tolist() == ["C"]
    assert r["so_na_of"]["home_team"].tolist() == ["E"]
    assert len(r["divergencias"]) == 1
