"""Composicao dos graficos por temporada.

Complementa test_formatting.py, que cobre apenas o separador pt-BR de
outcome_distribution e a formatacao numerica.
"""
from pathlib import Path

import pandas as pd

from charts import goals_by_season, outcomes_by_season, pollard_series
from metrics import by_season

DATA = Path(__file__).resolve().parent / "data"


def _series():
    return by_season(pd.read_csv(DATA / "processed_sample.csv"))


def test_pollard_series_plota_valores_e_referencia_50():
    fig = pollard_series(_series())
    traco = fig.data[0]
    assert traco.name == "Pollard"
    assert list(traco.y) == [80.0, 0.0]
    assert fig.layout.shapes[0].y0 == 50
    assert fig.layout.shapes[0].y1 == 50


def test_outcomes_by_season_usa_rotulos_pt_br():
    fig = outcomes_by_season(_series())
    assert {t.name for t in fig.data} == {"Vit. mandante", "Empate", "Vit. visitante"}


def test_goals_by_season_separa_mandante_e_visitante():
    fig = goals_by_season(_series())
    valores = {t.name: list(t.y) for t in fig.data}
    assert valores == {"Mandante": [1.5, 0.0], "Visitante": [0.5, 2.0]}
