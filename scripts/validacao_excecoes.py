"""Regra da exceção conhecida de data na validação cruzada (PT-BR).

Botafogo-RJ x Athletico-PR 1-1, 28ª rodada de 2023 — "jogo de dois dias":
iniciado em 21/10, interrompido por quedas de energia no Nilton Santos e
concluído em 22/10. A base primária registra 22/10; o OpenFootball, 21/10.
Fontes: ge.globo 22/10/2023 e globoplay.
"""
import pandas as pd

KNOWN_DATE_EXCEPTIONS = {
    (2023, "2023-10-22", "Botafogo-RJ", "Athletico-PR"),
}


def excecao_conhecida(
    ano: int,
    so_na_base: pd.DataFrame,
    so_na_of: pd.DataFrame,
    placar_divergente: int,
) -> bool:
    """True somente para o caso documentado: 1 exclusivo de cada lado, sem divergência de placar."""
    if len(so_na_base) != 1 or len(so_na_of) != 1 or placar_divergente != 0:
        return False
    linha_base = so_na_base.iloc[0]
    linha_of = so_na_of.iloc[0]
    return (ano, linha_base["date"], linha_base["home_team"], linha_base["away_team"]) in KNOWN_DATE_EXCEPTIONS
