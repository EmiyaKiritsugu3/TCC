#!/usr/bin/env python3
"""Auditoria da monografia: confere cada número do texto contra a base e os CSVs.

Uso: .venv/bin/python scripts/check_monografia.py [--monografia CAMINHO]
Acumula as divergências com mensagens objetivas e falha (exit 1) ao final.
"""
import argparse
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

import pandas as pd
from metrics import by_season, summarize, team_season
from context import rest_bucket

ERROS = []


def confere(cond, msg):
    if not cond:
        ERROS.append(msg)
        print(f"DIVERGÊNCIA: {msg}")


def _num(n: int) -> str:
    return f"{int(n):,}".replace(",", ".")


def _rotulo_grupo(variavel: str, grupo: str) -> str:
    """Rótulo de apresentação usado na Tabela 5 (o CSV mantém o nome curto)."""
    mapa = {
        "casa +1-2": "Casa +1–2 dias",
        "casa +3": "Casa +3 dias",
        "fora +1-2": "Fora +1–2 dias",
        "fora +3": "Fora +3 dias",
        "igual": "Igual",
        "favorito": "Favorito",
        "equilibrado": "Equilibrado",
        "zebra": "Zebra",
    }
    return mapa.get(grupo, grupo)


def _linhas_tabela(bloco: str, ncols: int, cabecalho: str) -> list[list[str]]:
    """Extrai linhas de uma tabela Markdown, ignorando cabeçalho e separador."""
    linhas = []
    for linha in bloco.splitlines():
        if not linha.startswith("|"):
            continue
        partes = [p.strip() for p in linha.strip("|").split("|")]
        if len(partes) != ncols or partes[0] == cabecalho:
            continue
        if all(set(p) <= set("-: ") for p in partes):
            continue
        linhas.append(partes)
    return linhas


def _ic(texto: str) -> tuple[float, float, float]:
    """Lê '58,23 (53,99–62,45)' e devolve (ponto, lo, hi)."""
    m = re.fullmatch(r"([\d,]+) \(([\d,]+)–([\d,]+)\)", texto)
    if not m:
        raise ValueError(f"IC em formato inesperado: {texto!r}")
    return tuple(float(v.replace(",", ".")) for v in m.groups())  # type: ignore[return-value]


def conferir(texto: str, df: pd.DataFrame, tab1: pd.DataFrame,
             tab5: pd.DataFrame, tab6: pd.DataFrame, contexto: dict) -> list[str]:
    """Executa todas as conferências e devolve as mensagens de divergência."""
    ERROS.clear()
    T = texto
    s = summarize(df)
    t = by_season(df).set_index("season")

    def secao(marcador: str) -> str:
        """Texto após um cabeçalho; falta vira divergência, não traceback."""
        if marcador not in T:
            confere(False, f"cabeçalho ausente: {marcador!r}")
            return ""
        return T.split(marcador, 1)[1]

    # --- agregados do período ---
    confere(s["n"] == 7219, "n total")
    confere(round(s["p_home"], 1) == 49.0, "p_home")
    confere(round(s["p_draw"], 1) == 26.8, "p_draw")
    confere(round(s["p_away"], 1) == 24.1, "p_away")
    confere(round(s["avg_home_goals"], 2) == 1.49, "gols casa")
    confere(round(s["avg_away_goals"], 2) == 1.00, "gols fora")
    confere(round(s["pollard"], 2) == 63.66, "pollard geral")
    confere(s["home_points"] == 12554, f"pontos casa {s['home_points']}")
    confere(s["away_points"] == 7166, f"pontos fora {s['away_points']}")

    # --- números citados no texto existem ---
    for pedaco in ["7.219", "49,0%", "26,8%", "24,1%", "1,49", "1,00", "+0,49",
                   "63,7%", "12.554", "7.166", "58,2% (2017)", "69,5% (2018)",
                   "28,9%", "17,9%", "60,2%", "n = 379", "379 jogos",
                   "62,4% em 2019", "61,8% em 2021", "11,3 p.p",
                   "2.659 de 2.660", "99,96%", "19/19", "94 testes", "94 passed",
                   "25/02/2021", "Flamengo 2019: 53/37/90/38",
                   "64,9% em 2006–2018", "61,0% em 2019–2024", "3,9 p.p.",
                   "2,1–5,6", "4,5 p.p.", "3,0–6,0", "53,4–62,6",
                   "63,4%", "63,8%", "63,9%", "58,2% (IC 53,99–62,45)",
                   "4,7 p.p.", "0,13 ponto", "55,7%", "73,3%", "17,7 p.p.",
                   "0,46", "5.388", "12.554 vs. 7.166", "Tabela 6",
                   "Figura 9", "Figura 10"]:
        confere(pedaco in T, f"trecho ausente: {pedaco!r}")
    confere("12.554 × 7.166" not in T, "comparação de pontos ainda usa ×")
    confere("`tests/test_context.py` (17)" in T, "contagem de test_context no Apendice D")
    confere("`tests/test_associations.py` (13)" in T, "contagem de test_associations no Apendice D")

    # --- extremos anuais ---
    confere(round(t.loc[2017, "pollard"], 2) == 58.24, "pollard 2017")
    confere(round(t.loc[2018, "pollard"], 2) == 69.51, "pollard 2018")
    confere(round(t.loc[2017, "p_away"], 2) == 28.95, "visitantes 2017")
    confere(round(t.loc[2018, "p_away"], 2) == 17.89, "visitantes 2018")
    confere(round(t.loc[2019, "pollard"], 2) == 62.38, "pollard 2019")
    confere(round(t.loc[2020, "pollard"], 2) == 60.17, "pollard 2020")
    confere(round(t.loc[2021, "pollard"], 2) == 61.83, "pollard 2021")
    confere(round(t.loc[2019, "p_home"], 2) == 48.42, "mandante 2019")
    confere(round(t.loc[2020, "p_home"], 2) == 45.00, "mandante 2020")
    confere(round(t.loc[2021, "p_home"], 2) == 45.79, "mandante 2021")
    confere(round(t.loc[2018, "pollard"] - t.loc[2017, "pollard"], 1) == 11.3, "amplitude")
    confere(len(t) == 19 and (t["n"].sum()) == 7219, "19 temporadas somam 7219")

    # --- Flamengo 2019 ---
    ts = team_season(df, "Flamengo", 2019)
    confere((ts["home_points"], ts["away_points"]) == (53, 37), "fla pontos")
    confere(ts["home_points"] + ts["away_points"] == 90, "fla total")
    confere(ts["home_n"] + ts["away_n"] == 38, "fla jogos")
    confere((ts["home_w"], ts["home_d"], ts["home_l"]) == (17, 2, 0), "fla casa VED")
    confere((ts["away_w"], ts["away_d"], ts["away_l"]) == (11, 4, 4), "fla fora VED")

    # --- Tabela 1 do md == CSV ---
    bloco = secao("**Tabela 1").split("Fonte:", 1)[0]
    linhas = [l for l in bloco.splitlines() if re.match(r"^\| 20\d\d \|", l)]
    confere(len(linhas) == 19, f"Tabela 1 tem {len(linhas)} linhas, esperado 19")
    ok = True
    for l in linhas:
        ano = int(l.split("|")[1])
        vals = [c.strip() for c in l.split("|")[2:-1]]
        ref = tab1[tab1.season == ano].iloc[0]
        cols = ["n", "p_home", "p_draw", "p_away", "avg_home_goals",
                "avg_away_goals", "goal_diff", "home_points", "away_points", "pollard"]
        esp = [str(int(ref[c])) if c == "n" else f"{ref[c]:.2f}".replace(".", ",") for c in cols]
        esp.append(f"{ref['pollard_lo']:.2f}–{ref['pollard_hi']:.2f}".replace(".", ","))
        if vals != esp:
            ok = False
            print(f"DIVERGÊNCIA Tabela 1/{ano}: md={vals} csv={esp}")
    confere(ok, "Tabela 1 diverge do CSV")

    # --- Tabela 1 (CSV) == base recalculada (por construção, tolera arredondamento) ---
    base = by_season(df).sort_values("season").reset_index(drop=True)
    for c in ["p_home", "p_draw", "p_away", "avg_home_goals", "avg_away_goals",
              "goal_diff", "home_points", "away_points", "pollard"]:
        a = tab1[c].round(2).tolist()
        b = base[c].round(2).tolist()
        confere(a == b, f"coluna {c} do CSV diverge da base")
    confere((tab1["n"] == base["n"]).all(), "coluna n diverge da base")
    confere((tab1["season"] == base["season"]).all(), "temporadas divergem")

    anual = pd.DataFrame(contexto["anual"]).set_index("season")
    tab1_idx = tab1.set_index("season")
    confere((tab1_idx["pollard_lo"].round(2) == anual["lo"].round(2)).all(),
            "pollard_lo do CSV diverge do contexto.json")
    confere((tab1_idx["pollard_hi"].round(2) == anual["hi"].round(2)).all(),
            "pollard_hi do CSV diverge do contexto.json")

    # --- mudança de nível e ponto de quebra ---
    n19 = contexto["nivel_2019"]
    confere(round(n19["a"], 2) == 64.88, "pré-2019 do contexto")
    confere(round(n19["b"], 2) == 61.01, "pós-2019 do contexto")
    confere(round(n19["diff"], 2) == 3.87, "diferença pré/pós-2019")
    confere(round(n19["lo"], 2) == 2.15 and round(n19["hi"], 2) == 5.58,
            "IC pré/pós-2019")
    confere(contexto["quebra"]["cut"] == 2019, "ponto de quebra")
    confere(round(contexto["quebra"]["pre"], 2) == 64.88 and
            round(contexto["quebra"]["post"], 2) == 61.01,
            "médias do ponto de quebra")

    # --- citações novas com ano casando com a referência ---
    for cit in ["Gil (2008)", "Nevill, Balmer e Williams (2002)", "Neave e Wolfson (2003)",
                "Pollard, Silva e Medeiros (2008)"]:
        confere(cit in T, f"citação ausente: {cit}")

    # --- Tabela 5 == CSV/contexto ---
    bloco5 = secao("**Tabela 5").split("Fonte:", 1)[0]
    linhas5 = _linhas_tabela(bloco5, 4, "Dimensão")
    confere(len(linhas5) == len(tab5),
            f"Tabela 5 tem {len(linhas5)} linhas, esperado {len(tab5)}")
    idx5 = {(r.variavel, _rotulo_grupo(r.variavel, r.grupo)): r
            for _, r in tab5.iterrows()}
    for dim, grupo, n, ic in linhas5:
        chave = (dim, grupo)
        confere(chave in idx5, f"Tabela 5 linha desconhecida: {chave}")
        if chave not in idx5:
            continue
        r = idx5[chave]
        confere(n == _num(r["n"]), f"Tabela 5 n {chave}: {n} != {_num(r['n'])}")
        try:
            ponto, lo, hi = _ic(ic)
        except ValueError as exc:
            confere(False, str(exc))
            continue
        confere(round(ponto, 2) == round(r["pollard"], 2),
                f"Tabela 5 Pollard {chave}")
        confere(round(lo, 2) == round(r["lo"], 2), f"Tabela 5 IC inferior {chave}")
        confere(round(hi, 2) == round(r["hi"], 2), f"Tabela 5 IC superior {chave}")
    confere({(d, g) for d, g, _, _ in linhas5} == set(idx5),
            "Tabela 5 não cobre todas as linhas do CSV")

    # --- Tabela 6 == JSON (top5 + bottom5 longevas) ---
    bloco6 = secao("**Tabela 6").split("Fonte:", 1)[0]
    linhas6 = _linhas_tabela(bloco6, 3, "Equipe")
    esperadas = {x["team"]: x for x in
                 contexto["equipes"]["top5_longevas"] + contexto["equipes"]["bottom5_longevas"]}
    confere(len(linhas6) == len(esperadas),
            f"Tabela 6 tem {len(linhas6)} linhas, esperado {len(esperadas)}")
    for time, n, ha_ic in linhas6:
        confere(time in esperadas, f"Tabela 6 equipe desconhecida: {time}")
        if time not in esperadas:
            continue
        r = esperadas[time]
        confere(n == _num(r["n"]), f"Tabela 6 n {time}: {n} != {_num(r['n'])}")
        try:
            ponto, lo, hi = _ic(ha_ic)
        except ValueError as exc:
            confere(False, str(exc))
            continue
        confere(round(ponto, 2) == round(r["ha"], 2), f"Tabela 6 HA {time}")
        confere(round(lo, 2) == round(r["lo"], 2), f"Tabela 6 IC inferior {time}")
        confere(round(hi, 2) == round(r["hi"], 2), f"Tabela 6 IC superior {time}")

    # --- descanso: ausentes não são imputados ---
    d = df.copy()
    d["rest_bucket"] = rest_bucket(d)
    confere(int(d["rest_bucket"].isna().sum()) == 31,
            f"descanso ausente: {int(d['rest_bucket'].isna().sum())} != 31")
    confere(len(d) - int(d["rest_bucket"].isna().sum()) == 7188,
            "partidas com descanso != 7188")

    # --- figuras, tabelas, todos ---
    corpo = secao("# 1 INTRODUÇÃO")
    nums, ordem = [], []
    for n in re.findall(r"Figura (\d+)", corpo):
        nums.append(int(n))
        if int(n) not in ordem:
            ordem.append(int(n))
    confere(ordem == list(range(1, 11)), f"ordem figuras {ordem}")
    for i in range(1, 7):
        confere(f"Tabela {i}" in T, f"Tabela {i} ausente")

    # --- citações x referências ---
    refs = secao("# REFERÊNCIAS").split("## APÊNDICE", 1)[0]
    for sobrenome in ["ALMEIDA", "DUQUE", "EFRON", "FEW", "GIL", "MATOS", "NEAVE",
                      "NEVILL", "OPENFOOTBALL", "POLLARD", "RIBEIRO", "SHARDA",
                      "SILVA", "STREAMLIT"]:
        confere(sobrenome in refs, f"referência ausente: {sobrenome}")
        confere(sobrenome in corpo or sobrenome in T.split("## RESUMO")[0], f"citação órfã: {sobrenome}")
    confere(re.search(r"(?m)^NEVILL, A\. M\.; BALMER", refs) is not None,
            "entrada NEVILL 2002 ausente")
    confere("NEVILL; HOLDER, 1999" in corpo, "apud 1999 sumiu")

    # --- siglas usadas no texto ---
    for sigla in ["BDM", "BSI", "CBF", "CC0", "CERES", "CSV", "DCT", "DOI", "HA",
                  "JSON", "NBR", "RF", "RNF", "SHA", "SISBI", "UFRN", "VAR", "VC"]:
        confere(re.search(rf"\b{sigla}\b", T) is not None, f"sigla sem uso: {sigla}")
    confere("TODO-SIGLAS" not in T, "TODO-SIGLAS resolvido mas ainda citado")
    confere("sete cartões" not in T, "contagem de cartões desatualizada")
    confere("oito cartões" in T, "oito cartões ausente")
    confere("Disponível em: https://github.com/adaoduque/Brasileirao_Dataset" in T,
            "DUQUE sem Disponível em/Acesso em")
    confere("Disponível em: https://github.com/openfootball/south-america" in T,
            "OPENFOOTBALL sem Disponível em/Acesso em")

    # --- corpo mínimo ---
    n_pal = len(re.findall(r"\b\w+\b", corpo.split("# REFERÊNCIAS", 1)[0]))
    confere(n_pal >= 5500, f"corpo com {n_pal} palavras (<5500)")

    print(f"\ncorpo: {n_pal} palavras; figuras: {ordem}")
    if ERROS:
        print(f"\n{len(ERROS)} DIVERGÊNCIA(S)")
    else:
        print("AUDITORIA NUMÉRICA: tudo confere")
    return list(ERROS)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--monografia", type=Path,
                   default=RAIZ / "docs" / "monografia_v2.md",
                   help="caminho do texto a auditar")
    args = p.parse_args(argv)
    caminho = args.monografia.resolve()
    if RAIZ.resolve() not in caminho.parents:
        p.error(f"--monografia fora do projeto: {args.monografia}")
    if not caminho.exists():
        p.error(f"arquivo não encontrado: {args.monografia}")
    texto = caminho.read_text(encoding="utf-8")
    df = pd.read_csv(RAIZ / "data" / "processed" / "matches_processed.csv")
    figuras = RAIZ / "figuras"
    for nome in ("tab1_indicadores_temporada.csv", "tab5_contexto.csv",
                 "tab6_equipes.csv", "contexto.json"):
        if not (figuras / nome).exists():
            p.error(f"artefato ausente: figuras/{nome}; rode scripts/analyze_context.py")
    tab1 = pd.read_csv(figuras / "tab1_indicadores_temporada.csv").sort_values("season")
    tab5 = pd.read_csv(figuras / "tab5_contexto.csv")
    tab6 = pd.read_csv(figuras / "tab6_equipes.csv")
    contexto = json.loads((figuras / "contexto.json").read_text(encoding="utf-8"))
    erros = conferir(texto, df, tab1, tab5, tab6, contexto)
    return 1 if erros else 0


if __name__ == "__main__":
    raise SystemExit(main())
