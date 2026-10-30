"""Testes de validação da limpeza (seção 16.1, parte de dados)."""
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from clean_data import clean_matches


def _raw(rows):
    base = {
        "ID": [], "rodata": [], "data": [], "hora": [],
        "mandante": [], "visitante": [], "mandante_Placar": [],
        "visitante_Placar": [], "vencedor": [], "arena": [],
    }
    for i, r in enumerate(rows, start=1):
        base["ID"].append(str(i))
        base["rodata"].append(str(r.get("rodada", 1)))
        base["data"].append(r.get("data", "10/05/2010"))
        base["hora"].append("16:00")
        base["mandante"].append(r["mandante"])
        base["visitante"].append(r["visitante"])
        base["mandante_Placar"].append(r.get("hg", ""))
        base["visitante_Placar"].append(r.get("ag", ""))
        base["vencedor"].append("-")
        base["arena"].append("Arena")
    return pd.DataFrame(base)


def test_placar_ausente_nao_vira_zero():
    df, rep = clean_matches(_raw([{"mandante": "A", "visitante": "B", "hg": "", "ag": ""}]))
    assert len(df) == 0
    assert rep["excluded"].get("placar_ausente", 0) == 1


def test_gols_negativos_rejeitados():
    df, rep = clean_matches(_raw([{"mandante": "A", "visitante": "B", "hg": "-1", "ag": "2"}]))
    assert len(df) == 0
    assert rep["excluded"].get("placar_invalido", 0) == 1


def test_mandante_igual_visitante_rejeitado():
    df, rep = clean_matches(_raw([{"mandante": "A", "visitante": "A", "hg": "1", "ag": "0"}]))
    assert len(df) == 0
    assert rep["excluded"].get("mandante_igual_visitante", 0) == 1


def test_fora_do_recorde_excluido():
    df, _ = clean_matches(_raw([{"mandante": "A", "visitante": "B", "hg": "1", "ag": "0", "data": "10/05/2005"}]))
    assert len(df) == 0


def test_match_id_duplicado_mantem_primeiro():
    rows = [
        {"mandante": "A", "visitante": "B", "hg": "1", "ag": "0"},
        {"mandante": "C", "visitante": "D", "hg": "2", "ag": "2"},
    ]
    raw = _raw(rows)
    raw.loc[1, "ID"] = "1"  # duplica o ID
    df, rep = clean_matches(raw)
    assert len(df) == 1
    assert rep["excluded"].get("match_id_duplicado", 0) == 1


def test_resultado_recalculado_do_placar():
    df, _ = clean_matches(_raw([
        {"mandante": "A", "visitante": "B", "hg": "2", "ag": "0"},
        {"mandante": "C", "visitante": "D", "hg": "1", "ag": "1"},
        {"mandante": "E", "visitante": "F", "hg": "0", "ag": "2"},
    ]))
    assert df["result"].tolist() == ["H", "D", "A"]
    assert df["home_points"].tolist() == [3, 1, 0]
    assert df["away_points"].tolist() == [0, 1, 3]
