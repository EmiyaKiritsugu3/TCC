"""Esquema de saída, relatório de qualidade e segmentação de temporada.

Cobre caminhos de clean_matches não assertados pelos testes existentes
(test_data_validation.py trata das exclusões básicas e do resultado).
"""
from pathlib import Path

from clean_data import SOURCE_LABEL, clean_matches
from load_data import load_raw

DATA = Path(__file__).resolve().parent / "data"


def test_esquema_de_saida_relatorio_e_metadados():
    df, rep = clean_matches(load_raw(DATA / "raw_sample.csv"))
    assert list(df.columns) == [
        "match_id", "season", "date", "round", "home_team", "away_team",
        "home_goals", "away_goals", "result", "home_points", "away_points",
        "stadium", "source",
    ]
    assert df["match_id"].tolist() == ["1", "2", "3"]
    assert df["date"].tolist() == ["2010-05-10", "2010-05-11", "2010-05-17"]
    assert df["round"].tolist() == [1, 1, 2]
    assert df["home_goals"].tolist() == [2, 0, 1]
    assert df["away_goals"].tolist() == [1, 0, 3]
    assert df["stadium"].tolist() == ["Maracana", "Arena", "Vila Belmiro"]
    assert set(df["source"]) == {SOURCE_LABEL}
    assert rep["loaded"] == 3
    assert rep["kept"] == 3
    assert rep["coverage_per_season"] == {2010: 3}
    assert rep["seasons_below_expected"] == {2010: 377}


def test_temporada_por_intervalo_rollover_e_reinicio():
    df, rep = clean_matches(load_raw(DATA / "raw_seasons.csv"))
    # 20/12/2020 -> 28/02/2021: 70 dias de intervalo, mas rodada 36 mantém o
    # mesmo segmento (temporada 2020 vai ate fev/2021); 17/04/2021 com rodada 1
    # apos 48 dias reinicia o segmento em 2021.
    temporadas = {mid: int(s) for mid, s in zip(df["match_id"], df["season"])}
    assert temporadas == {"1": 2020, "2": 2020, "3": 2020, "4": 2021, "5": 2021}
    assert rep["coverage_per_season"] == {2020: 3, 2021: 2}
    assert rep["seasons_below_expected"] == {2020: 377, 2021: 378}


def test_exclusoes_data_invalida_fracionaria_e_tripla():
    df, rep = clean_matches(load_raw(DATA / "raw_exclusions.csv"))
    # "31/02/2010" -> data_invalida; placar "1.5" -> placar_invalido (o total
    # excluido ancora o caminho fracionario sem repetir a assercao de contagem
    # ja existente em test_data_validation.py); linhas 4 e 5 repetem a tripla
    # (data, mandante, visitante) e a primeira (ID 4) permanece.
    assert set(df["match_id"]) == {"1", "4", "6"}
    assert rep["excluded"]["data_invalida"] == 1
    assert rep["excluded"]["tripla_data_mandante_visitante_repetida"] == 1
    assert sum(rep["excluded"].values()) == 3
