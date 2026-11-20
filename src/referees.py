"""Normalização de nomes de árbitros.

A Base dos Dados e o FBref grafam o mesmo árbitro de formas diferentes
(abreviações, acentos e espaços). Sem normalizar, o mesmo árbitro é contado
duas vezes e a heterogeneidade por árbitro fica inflada.
"""
from __future__ import annotations

import re
import unicodedata

import pandas as pd

# Chave normalizada -> nome canônico. Cobre variantes da Base dos Dados e
# abreviações do FBref observadas em 2024.
ALIASES: dict[str, str] = {
    "rodrigo d": "Rodrigo D'Alonso Ferreira",
    "rodrigo d alonso ferreira": "Rodrigo D'Alonso Ferreira",
    "denis ribeiro serafim": "Denis da Silva Ribeiro Serafim",
    "denis da silva ribeiro serafim": "Denis da Silva Ribeiro Serafim",
    "rodrigo jose pereira de lima": "Rodrigo José Pereira de Lima",
    "luiz flavio de oliveira": "Luiz Flávio de Oliveira",
    "braulio machado": "Braulio da Silva Machado",
    "braulio da silva machado": "Braulio da Silva Machado",
    "bruno arleu": "Bruno Arleu de Araújo",
    "bruno arleu de araujo": "Bruno Arleu de Araújo",
    "edina alves": "Edina Alves Batista",
    "edina alves batista": "Edina Alves Batista",
    "felipe fernandes de lima": "Felipe Fernandes",
    "felipe fernandes": "Felipe Fernandes",
    "kleber ariel goncalves silva": "Kleber Ariel Gonçalves da Silva",
    "kleber ariel goncalves da silva": "Kleber Ariel Gonçalves da Silva",
    "luciano da silva miranda": "Luciano da Silva Miranda Filho",
    "luciano da silva miranda filho": "Luciano da Silva Miranda Filho",
    "paulo zanovelli": "Paulo Cesar Zanovelli",
    "paulo cesar zanovelli": "Paulo Cesar Zanovelli",
    "rafael klein": "Rafael Rodrigo Klein",
    "rafael rodrigo klein": "Rafael Rodrigo Klein",
    "savio pereira": "Savio Pereira Sampaio",
    "savio pereira sampaio": "Savio Pereira Sampaio",
}


def normalizar(nome: object) -> str:
    """Chave ASCII, minúscula e sem pontuação para comparar nomes."""
    texto = unicodedata.normalize("NFKD", str(nome)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", texto.lower()).strip()


def mapa_canonico(nomes: pd.Series) -> dict[str, str]:
    """Mapa chave normalizada -> grafia mais frequente na fonte."""
    contagem = nomes.dropna().astype(str).str.strip()
    contagem = contagem[contagem != ""].value_counts()
    mapa: dict[str, str] = {}
    for nome in contagem.index:
        mapa.setdefault(normalizar(nome), nome)
    return mapa


def canonico(nome: object, mapa: dict[str, str] | None = None) -> str | None:
    """Devolve o nome canônico de um árbitro (ou None se vazio)."""
    if pd.isna(nome):
        return None
    texto = str(nome).strip()
    if not texto:
        return None
    chave = normalizar(texto)
    if chave in ALIASES:
        return ALIASES[chave]
    if mapa and chave in mapa:
        return mapa[chave]
    return texto
