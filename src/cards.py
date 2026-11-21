"""Leitura dos cartões por partida do BrazilianFootball/Data.

Fonte: https://github.com/BrazilianFootball/Data (MIT), extraída dos borderôs
da CBF. O JSON de cada temporada tem, por jogo, as listas `Yellow cards` e
`Red cards` com minuto, jogador e equipe.
"""
from __future__ import annotations

import re
import unicodedata
from datetime import datetime

import pandas as pd

# Nome normalizado (sem estado, sem sufixo empresarial) -> nome da base do TCC.
ALIASES: dict[str, str] = {
    "athletico paranaense": "Athletico-PR", "athletico": "Athletico-PR",
    "atletico paranaense": "Athletico-PR",
    "atletico mineiro": "Atletico-MG",
    "atletico goianiense": "Atletico-GO",
    "america mineiro": "America-MG", "america natal": "America-RN",
    "avai": "Avai", "bahia": "Bahia", "barueri": "Barueri", "botafogo": "Botafogo-RJ",
    "bragantino": "Bragantino", "red bull bragantino": "Bragantino",
    "ceara": "Ceara", "chapecoense": "Chapecoense",
    "corinthians": "Corinthians", "coritiba": "Coritiba",
    "criciuma": "Criciuma", "cruzeiro": "Cruzeiro", "csa": "CSA",
    "cuiaba": "Cuiaba", "figueirense": "Figueirense",
    "flamengo": "Flamengo", "fluminense": "Fluminense",
    "fortaleza": "Fortaleza", "goias": "Goias", "gremio": "Gremio",
    "guarani": "Guarani", "internacional": "Internacional",
    "ipatinga": "Ipatinga", "joinville": "Joinville",
    "juventude": "Juventude", "nautico": "Nautico",
    "palmeiras": "Palmeiras", "parana": "Parana",
    "ponte preta": "Ponte Preta", "portuguesa": "Portuguesa",
    "santa cruz": "Santa Cruz", "santo andre": "Santo Andre",
    "santos": "Santos", "sao caetano": "Sao Caetano",
    "sao paulo": "Sao Paulo", "sport": "Sport", "sport recife": "Sport",
    "vasco": "Vasco", "vasco da gama": "Vasco", "vitoria": "Vitoria",
}

# Times ambíguos: a UF resolve.
AMBIGUOS = {
    ("atletico", "MG"): "Atletico-MG",
    ("atletico", "GO"): "Atletico-GO",
    ("atletico", "PR"): "Athletico-PR",
    ("america", "MG"): "America-MG",
    ("america", "RN"): "America-RN",
}


def normalizar(texto: object) -> str:
    """ASCII, minúsculo e sem pontuação."""
    s = unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def _limpar_time(nome: str) -> str:
    """Remove sufixos empresariais e de estado do nome do time."""
    nome = nome.split("/")[0]
    texto = normalizar(nome)
    texto = re.sub(r"\b(saf|s a f|futebol|clube)\b.*$", "", texto).strip()
    return texto


def time_canonico(nome: object, uf: str | None = None) -> str | None:
    """Converte o nome do BrazilianFootball/Data no nome da base do TCC."""
    if pd.isna(nome):
        return None
    bruto = str(nome).strip()
    if not bruto:
        return None
    if "/" in bruto:
        antes, depois = bruto.rsplit("/", 1)
        uf = uf or depois.strip()
    else:
        antes = bruto
    chave = _limpar_time(antes)
    if uf and (chave, uf) in AMBIGUOS:
        return AMBIGUOS[(chave, uf)]
    return ALIASES.get(chave)


def candidatos_time(nome: str) -> set[str]:
    """Formas curtas que podem aparecer no sufixo de um cartão."""
    base = _limpar_time(nome)
    palavras = base.split()
    out = {base}
    if palavras:
        out.add(palavras[0])
        out.add(palavras[-1])
    canon = time_canonico(nome)
    extras = {
        "Athletico-PR": {"athletico", "atletico", "athletico pr", "atletico pr"},
        "Atletico-MG": {"atletico", "atletico mg"},
        "Atletico-GO": {"atletico", "atletico go"},
        "America-MG": {"america", "america mg"},
        "America-RN": {"america", "america rn"},
        "Bragantino": {"bragantino", "red bull bragantino"},
        "Vasco": {"vasco", "vasco da gama"},
        "Sport": {"sport", "sport recife"},
    }
    out |= extras.get(canon, set())
    return out


def _limpar_cartao(texto: str) -> str:
    antes = texto.rsplit("/", 1)[0] if "/" in texto else texto
    limpo = normalizar(antes)
    limpo = re.sub(r"\b(saf|s a f|futebol|foot ?ball|regatas|clube|fc|ec|sc)\s*$",
                   "", limpo).strip()
    return re.sub(r"\b(de|da|do)\s*$", "", limpo).strip()


def _lado_cartao(cartao: str, casa: set[str], fora: set[str],
                 uf_casa: str, uf_fora: str) -> str | None:
    antes = cartao.rsplit("/", 1)[0] if "/" in cartao else cartao
    uf = cartao.rsplit("/", 1)[1].strip() if "/" in cartao else ""
    texto = _limpar_cartao(antes)
    lados: list[tuple[str, tuple[int, int], bool]] = []
    for lado, candidatos, uf_time in (("H", casa, uf_casa), ("A", fora, uf_fora)):
        ocorrencias = [
            (m.end(), len(c))
            for c in candidatos
            for m in re.finditer(rf"(?<![a-z0-9]){re.escape(c)}(?![a-z0-9])", texto)
        ]
        if ocorrencias:
            lados.append((lado, max(ocorrencias), uf_time == uf))
    if not lados:
        return None
    # A equipe do cartão é a menção mais ao final do texto; nomes de jogadores
    # podem conter o nome de outro clube (ex.: "Ramires Santos ... Palmeiras/SP").
    # Em empate de posição, o nome mais longo é o mais específico
    # ("America Mineiro" vence "Mineiro").
    ultima = max(score for _, score, _ in lados)
    melhores = [x for x in lados if x[1] == ultima]
    if len(melhores) == 1:
        return melhores[0][0]
    por_uf = [lado for lado, _, ok in melhores if ok]
    return por_uf[0] if len(por_uf) == 1 else None


def parse_resultado(resultado: str) -> tuple[int, int]:
    """Converte '2 X 1' em (2, 1)."""
    partes = [p.strip() for p in str(resultado).strip().upper().split("X", 1)]
    if len(partes) != 2:
        raise ValueError(f"placar inesperado: {resultado!r}")
    return int(partes[0]), int(partes[1])


def parse_data(data: str) -> str:
    """Converte DD/MM/AAAA em AAAA-MM-DD."""
    return datetime.strptime(str(data).strip(), "%d/%m/%Y").strftime("%Y-%m-%d")


def parse_partida(jogo: dict) -> dict:
    """Extrai cartões de um jogo do JSON, separando casa e fora."""
    casa_raw, fora_raw = jogo["Home"], jogo["Away"]
    uf_casa = casa_raw.rsplit("/", 1)[1].strip() if "/" in casa_raw else ""
    uf_fora = fora_raw.rsplit("/", 1)[1].strip() if "/" in fora_raw else ""
    casa = candidatos_time(casa_raw)
    fora = candidatos_time(fora_raw)
    casa_time = time_canonico(casa_raw)
    fora_time = time_canonico(fora_raw)
    hg, ag = parse_resultado(jogo["Result"])

    amarelos = {"H": 0, "A": 0}
    vermelhos = {"H": 0, "A": 0}
    penaltis = {"H": 0, "A": 0}
    nao_atribuidos: list[str] = []
    pen_nao_atribuidos = 0
    for cartao in jogo.get("Yellow cards", []) or []:
        lado = _lado_cartao(cartao, casa, fora, uf_casa, uf_fora)
        if lado is None:
            nao_atribuidos.append(cartao)
        else:
            amarelos[lado] += 1
    for cartao in jogo.get("Red cards", []) or []:
        lado = _lado_cartao(cartao, casa, fora, uf_casa, uf_fora)
        if lado is None:
            nao_atribuidos.append(cartao)
        else:
            vermelhos[lado] += 1
    for gol in jogo.get("Goals", []) or []:
        if not re.search(r"\dPN", gol):
            continue
        lado = _lado_cartao(gol, casa, fora, uf_casa, uf_fora)
        if lado is None:
            pen_nao_atribuidos += 1
        else:
            penaltis[lado] += 1

    return {
        "date": parse_data(jogo["Date"]),
        "home_team": casa_time,
        "away_team": fora_time,
        "home_goals": hg,
        "away_goals": ag,
        "yellow_home": amarelos["H"],
        "yellow_away": amarelos["A"],
        "red_home": vermelhos["H"],
        "red_away": vermelhos["A"],
        "pen_home": penaltis["H"],
        "pen_away": penaltis["A"],
        "pen_nao_atribuidos": pen_nao_atribuidos,
        "nao_atribuidos": len(nao_atribuidos),
        "cartoes_total": len(jogo.get("Yellow cards", []) or [])
        + len(jogo.get("Red cards", []) or []),
    }
