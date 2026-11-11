"""Testes de carregamento da base bruta (load_data, RF01) — fixtures sintéticas."""
from pathlib import Path

import pytest

from load_data import load_raw

DATA = Path(__file__).resolve().parent / "data"


def test_load_raw_preserva_texto_sem_coercao():
    df = load_raw(DATA / "raw_sample.csv")
    assert len(df) == 3
    assert df.loc[0, "rodata"] == "01"
    assert df.loc[0, "mandante_Placar"] == "2"
    assert df.loc[1, "vencedor"] == "-"


def test_load_raw_arquivo_inexistente_instrui_fetch(tmp_path):
    with pytest.raises(FileNotFoundError, match="fetch_raw"):
        load_raw(tmp_path / "nao_existe.csv")


def test_load_raw_arquivo_vazio_rejeitado():
    with pytest.raises(ValueError, match="Arquivo vazio"):
        load_raw(DATA / "raw_empty.csv")


def test_load_raw_sem_linhas_rejeitado():
    with pytest.raises(ValueError, match="sem linhas de dados"):
        load_raw(DATA / "raw_header_only.csv")


def test_load_raw_colunas_obrigatorias_ausentes():
    with pytest.raises(ValueError) as exc:
        load_raw(DATA / "raw_missing_columns.csv")
    assert "mandante_Placar" in str(exc.value)
    assert "visitante_Placar" in str(exc.value)
    assert "(RF01)" in str(exc.value)
