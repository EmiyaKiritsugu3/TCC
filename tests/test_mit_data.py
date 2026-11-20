"""Testes do parser da base 2013–2024 (BrazilianFootball/Data, MIT)."""
from __future__ import annotations

from pathlib import Path

import pytest

from mit_data import build_base, parse_jogo, quality_report, validar_base

RAIZ = Path(__file__).resolve().parent.parent
PASTA = RAIZ / "data" / "external" / "cards"
JOGO = {
    "Date": "13/04/2024",
    "Home": "Internacional / RS",
    "Away": "Bahia / BA",
    "Result": "2 X 1",
    "Stadium": "José Pinheiro Borda / Porto Alegre",
}


def test_parse_jogo_deriva_resultado_pontos_e_estadio():
    item = parse_jogo(JOGO, 2024, "1")
    assert item["match_id"] == 2024001
    assert item["home_team"] == "Internacional"
    assert item["away_team"] == "Bahia"
    assert (item["home_goals"], item["away_goals"]) == (2, 1)
    assert (item["result"], item["home_points"], item["away_points"]) == ("H", 3, 0)
    assert item["stadium"].startswith("José Pinheiro Borda")
    assert item["source"].startswith("BrazilianFootball/Data")


def test_parse_jogo_rejeita_time_nao_mapeado():
    jogo = dict(JOGO, Home="Time Inventado / XX")
    with pytest.raises(ValueError, match="time não mapeado"):
        parse_jogo(jogo, 2024, "1")


@pytest.mark.integration
@pytest.mark.skipif(
    not (PASTA / "Serie_A_2024_games.json").exists(),
    reason="rode scripts/fetch_cards.py",
)
def test_build_base_2013_2024():
    df = build_base(range(2013, 2025))
    validar_base(df)
    assert len(df) == 4559
    assert df["season"].nunique() == 12
    assert df["match_id"].is_unique
    assert set(df["season"]) == set(range(2013, 2025))
    q = quality_report(df)
    assert q["recorte"] == [2013, 2024]
    assert q["coverage_per_season"]["2016"] == 379
    assert q["seasons_below_expected"] == {}
