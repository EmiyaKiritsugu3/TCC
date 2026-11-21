"""Testes do parser de cartões (BrazilianFootball/Data)."""
from __future__ import annotations

import pytest

from cards import (
    candidatos_time,
    normalizar,
    parse_data,
    parse_partida,
    parse_resultado,
    time_canonico,
)


def test_normalizar_e_time_canonico():
    assert normalizar("São Paulo / SP") == "sao paulo sp"
    assert time_canonico("Bahia / BA") == "Bahia"
    assert time_canonico("Atlético/MG") == "Atletico-MG"
    assert time_canonico("Atlético/GO") == "Atletico-GO"
    assert time_canonico("Athletico/PR") == "Athletico-PR"
    assert time_canonico("América/MG") == "America-MG"
    assert time_canonico("Vasco da Gama S.a.f./RJ") == "Vasco"


def test_candidatos_time_inclui_variantes():
    assert "atletico" in candidatos_time("Atlético Mineiro / MG")
    assert "atletico" in candidatos_time("Athletico Paranaense / PR")
    assert "america" in candidatos_time("América / MG")
    assert "bragantino" in candidatos_time("Red Bull Bragantino / SP")


def test_parse_resultado_e_data():
    assert parse_resultado("2 X 1") == (2, 1)
    assert parse_resultado("1 x 2") == (1, 2)
    assert parse_data("13/04/2024") == "2024-04-13"
    with pytest.raises(ValueError):
        parse_resultado("sem placar")


def test_parse_partida_separa_cartoes_por_equipe():
    jogo = {
        "Date": "13/04/2024",
        "Home": "Palmeiras / SP",
        "Away": "Santos / SP",
        "Result": "2 X 1",
        "Yellow cards": [
            "10:00 1T10Ramires Santos do Nascimento Palmeiras/SP",
            "20:00 1T11Joao Silva Santos/SP",
            "30:00 1T12Pedro Souza Palmeiras/SP",
        ],
        "Red cards": ["40:00 2T9Jogador Santos/SP"],
        "Goals": [
            "10:00 1T9PNJogador Um Palmeiras/SP",
            "20:00 1T10PNJogador Dois Santos/SP",
        ],
    }
    item = parse_partida(jogo)
    assert item["home_team"] == "Palmeiras"
    assert item["away_team"] == "Santos"
    assert item["yellow_home"] == 2
    assert item["yellow_away"] == 1
    assert item["red_home"] == 0
    assert item["red_away"] == 1
    assert item["pen_home"] == 1
    assert item["pen_away"] == 1
    assert item["pen_nao_atribuidos"] == 0
    assert item["nao_atribuidos"] == 0
    assert item["cartoes_total"] == 4


def test_parse_partida_com_sufixo_empresarial_e_cartao_quebrado():
    jogo = {
        "Date": "01/05/2024",
        "Home": "Atlético Mineiro / MG",
        "Away": "Cruzeiro / MG",
        "Result": "1 X 0",
        "Yellow cards": [
            "10:00 1T9Jogador Clube Atletico Mineiro/MG",
            "20:00 1T10Jogador Cruzeiro Esporte Clube/MG",
            "30:00 1T11",
        ],
        "Red cards": [],
    }
    item = parse_partida(jogo)
    assert item["yellow_home"] == 1
    assert item["yellow_away"] == 1
    assert item["nao_atribuidos"] == 1


def test_time_canonico_ausente_ou_sem_uf():
    assert time_canonico(float("nan")) is None
    assert time_canonico("   ") is None
    assert time_canonico("Bahia") == "Bahia"


def test_desempate_por_uf_quando_os_dois_times_aparecem():
    jogo = {
        "Date": "02/06/2024",
        "Home": "Atlético Mineiro / MG",
        "Away": "Athletico Paranaense / PR",
        "Result": "1 X 1",
        "Yellow cards": ["10:00 1T9Jogador Atletico/MG"],
        "Red cards": [],
    }
    item = parse_partida(jogo)
    assert item["yellow_home"] == 1
    assert item["yellow_away"] == 0


def test_cartao_vermelho_sem_time_entra_como_nao_atribuido():
    jogo = {
        "Date": "02/06/2024",
        "Home": "Bahia / BA",
        "Away": "Vitória / BA",
        "Result": "0 X 0",
        "Yellow cards": [],
        "Red cards": ["80:00 2T9"],
    }
    item = parse_partida(jogo)
    assert item["red_home"] == 0
    assert item["red_away"] == 0
    assert item["nao_atribuidos"] == 1


def test_nome_mais_longo_desempata_sufixo_comum():
    jogo = {
        "Date": "10/06/2024",
        "Home": "América Mineiro / MG",
        "Away": "Atlético Mineiro / MG",
        "Result": "0 X 1",
        "Yellow cards": ["30:00 1T9Jogador America Mineiro/MG"],
        "Red cards": [],
    }
    item = parse_partida(jogo)
    assert item["yellow_home"] == 1
    assert item["yellow_away"] == 0
