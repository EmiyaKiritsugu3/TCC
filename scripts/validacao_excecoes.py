"""Regra da exceção conhecida de data na validação cruzada (PT-BR).

Botafogo-RJ x Athletico-PR 1-1, 28ª rodada de 2023 — "jogo de dois dias":
iniciado em 21/10, interrompido por quedas de energia no Nilton Santos e
concluído em 22/10. A base primária registra 22/10; o OpenFootball, 21/10.
Fontes: ge.globo 22/10/2023 e globoplay.
"""
import pandas as pd

# Chave = exclusivo da base primária; valor = exclusivo esperado do OpenFootball.
KNOWN_DATE_EXCEPTIONS = {
    (2023, "2023-10-22", "Botafogo-RJ", "Athletico-PR"):
        ("2023-10-21", "Botafogo-RJ", "Athletico-PR"),
}


def excecao_conhecida(
    ano: int,
    so_na_base: pd.DataFrame,
    so_na_of: pd.DataFrame,
    placar_divergente: int,
) -> bool:
    """True somente para o par documentado: 1 exclusivo de cada lado, sem divergência de placar."""
    if len(so_na_base) != 1 or len(so_na_of) != 1 or placar_divergente != 0:
        return False
    b = so_na_base.iloc[0]
    o = so_na_of.iloc[0]
    chave_base = (ano, b["date"], b["home_team"], b["away_team"])
    chave_of = (o["date"], o["home_team"], o["away_team"])
    return KNOWN_DATE_EXCEPTIONS.get(chave_base) == chave_of
