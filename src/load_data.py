"""Carregamento da base bruta (Fase 2).

Lê exclusivamente a cópia imutável em `data/raw/` e valida a presença
das colunas obrigatórias. Não transforma nada — a transformação vive
em `clean_data.py`.
"""
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = [
    "ID",
    "rodata",
    "data",
    "mandante",
    "visitante",
    "mandante_Placar",
    "visitante_Placar",
]

OPTIONAL_COLUMNS = ["hora", "vencedor", "arena"]


def load_raw(path: str | Path) -> pd.DataFrame:
    """Carrega o CSV bruto como texto (sem coerção prematura)."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"Base bruta não encontrada: {path}. "
            "Execute `python3 scripts/fetch_raw.py` para baixar do commit "
            "pinado (ver `data/raw/FONTE.md`). (RF01)"
        )
    try:
        df = pd.read_csv(path, dtype=str, keep_default_na=False, na_values=[])
    except pd.errors.EmptyDataError:
        raise ValueError(f"Arquivo vazio: {path}. (RF01)")
    if df.empty:
        raise ValueError(f"Arquivo sem linhas de dados: {path}. (RF01)")
    ausentes = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if ausentes:
        raise ValueError(
            f"Colunas obrigatórias ausentes em {path}: {ausentes}. (RF01)"
        )
    return df
