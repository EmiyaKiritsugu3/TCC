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

import numpy as np
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


def _num_pt(texto: str) -> float:
    return float(texto.replace("−", "-").replace(",", "."))


def _ic(texto: str) -> tuple[float, float, float]:
    """Lê '58,23 (53,99–62,45)' e devolve (ponto, lo, hi)."""
    m = re.fullmatch(r"(-?[\d,]+) \((-?[\d,]+)–(-?[\d,]+)\)", texto)
    if not m:
        raise ValueError(f"IC em formato inesperado: {texto!r}")
    return tuple(float(v.replace(",", ".")) for v in m.groups())  # type: ignore[return-value]


def conferir(texto: str, df: pd.DataFrame, tab1: pd.DataFrame,
             tab5: pd.DataFrame, tab6: pd.DataFrame, tab7: pd.DataFrame,
             mat_eq: pd.DataFrame, mat_part: pd.DataFrame,
             contexto: dict, externo: dict, qualidade: dict) -> list[str]:
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
                   "2.659 de 2.660", "99,96%", "19/19", "104 testes", "104 passed",
                   "25/02/2021", "Flamengo 2019: 53/37/90/38",
                   "64,9% em 2006–2018", "61,0% em 2019–2024", "3,9 p.p.",
                   "2,1–5,6", "4,5 p.p.", "3,0–6,0", "53,4–62,6",
                   "63,4%", "63,8%", "63,9%", "58,2% (IC 53,99–62,45)",
                   "4,7 p.p.", "0,13 ponto", "55,6%", "5,6 p.p.", "73,3%",
                   "17,7 p.p.", "0,46", "5.388", "12.554 vs. 7.166",
                   "Tabela 6", "Tabela 7", "Tabela 8", "Tabela 9",
                   "Tabela 10", "Figura 9", "Figura 10", "Figura 11",
                   "Figura 12", "6.618", "6.821", "64,94", "60,17", "60,55",
                   "0,068", "0,461", "−0,042", "0,786", "0,043",
                   "43,1", "59,4", "185 árbitros", "48,9%",
                   "65,1%", "60,6%", "4,5 p.p.", "3,0–6,0",
                   "−1,1", "0,57", "−0,46", "−0,01", "0,10", "0,19",
                   "380 equipe-temporadas"]:
        confere(pedaco in T, f"trecho ausente: {pedaco!r}")
    confere("12.554 × 7.166" not in T, "comparação de pontos ainda usa ×")
    confere("`tests/test_context.py` (20)" in T, "contagem de test_context no Apendice D")
    confere("`tests/test_associations.py` (19)" in T, "contagem de test_associations no Apendice D")

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

    n06 = contexto["nivel_2006_2016_vs_2022_2024"]
    confere(round(n06["a"], 2) == 65.07 and round(n06["b"], 2) == 60.55,
            "médias 2006–2016 vs. 2022–2024")
    confere(round(n06["diff"], 2) == 4.51, "diferença 2006–2016 vs. 2022–2024")
    confere(round(n06["lo"], 2) == 3.02 and round(n06["hi"], 2) == 6.03,
            "IC 2006–2016 vs. 2022–2024")

    for chave, valor in [
        ("derby_vs_nao", -5.79), ("estadio_vs_outro", 4.70),
        ("favorito_vs_zebra", 17.69), ("pandemia_vs_demais", -2.97),
        ("mesmo_estado_vs_diferente", -1.77),
    ]:
        confere(round(contexto["contrastes"][chave]["diff"], 2) == valor,
                f"contraste {chave}")

    for grupo, valor in {
        x["grupo"]: x["mean_deviation"]
        for x in contexto["dentro_equipe_temporada"]["descanso"]
    }.items():
        confere(f"{abs(valor):.3f}".replace(".", ",") in T,
                f"desvio de descanso ausente: {grupo}")
    est = {x["grupo"]: x["mean_deviation"]
           for x in contexto["dentro_equipe_temporada"]["estadio"]}
    confere(abs((est["Estádio habitual"] - est["Outro estádio"]) - 0.128) < 0.001,
            "diferença dentro de equipe-temporada do estádio")

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

    # --- Tabela 7 == correlações com HA ---
    mapa7 = {
        "Casa pts/jogo": "home_ppg", "% vitórias casa": "home_win_pct",
        "Fora pts/jogo": "away_ppg", "% vitórias fora": "away_win_pct",
        "Gols casa/jogo": "home_goals_pg", "Gols fora/jogo": "away_goals_pg",
        "Temporada": "season", "% estádio habitual": "usual_stadium_share",
        "Posição final": "rank", "Pontos": "pts", "Distância média": "avg_away_km",
    }
    bloco7 = secao("**Tabela 7").split("Fonte:", 1)[0]
    linhas7 = _linhas_tabela(bloco7, 3, "Variável")
    confere(len(linhas7) == len(tab7),
            f"Tabela 7 tem {len(linhas7)} linhas, esperado {len(tab7)}")
    idx7 = {r.variavel: r for _, r in tab7.iterrows()}
    for rotulo, rho_txt, n_txt in linhas7:
        variavel = mapa7.get(rotulo)
        confere(variavel is not None, f"Tabela 7 rótulo desconhecido: {rotulo}")
        if variavel is None or variavel not in idx7:
            continue
        r = idx7[variavel]
        confere(n_txt == _num(r["n"]), f"Tabela 7 n {rotulo}")
        confere(abs(_num_pt(rho_txt) - r["rho"]) < 0.006,
                f"Tabela 7 rho {rotulo}")
        confere(abs(mat_eq.loc["ha", variavel] - r["rho"]) < 1e-4,
                f"matriz_equipe HA x {variavel}")

    # --- Tabela 8 == base externa (público e Pollard por bloco) ---
    confere(qualidade["n"] == 7219, "qualidade externa: n total")
    confere(qualidade["publico"] == 6618, "qualidade externa: público")
    confere(qualidade["arbitro"] == 6821, "qualidade externa: árbitro")
    blocos = {b["bloco"]: b for b in externo["blocos"]
              if b["bloco"] != "2006 (sem público)"}
    bloco8 = secao("**Tabela 8").split("Fonte:", 1)[0]
    linhas8 = _linhas_tabela(bloco8, 5, "Bloco")
    confere(len(linhas8) == len(blocos),
            f"Tabela 8 tem {len(linhas8)} linhas, esperado {len(blocos)}")
    for nome, jogos, com_publico, publico_medio, ic in linhas8:
        confere(nome in blocos, f"Tabela 8 bloco desconhecido: {nome}")
        if nome not in blocos:
            continue
        r = blocos[nome]
        confere(jogos == _num(r["n"]), f"Tabela 8 n {nome}")
        confere(com_publico == _num(r["publico_n"]), f"Tabela 8 público n {nome}")
        confere(publico_medio == _num(round(r["publico_medio"])),
                f"Tabela 8 público médio {nome}")
        try:
            ponto, lo, hi = _ic(ic)
        except ValueError as exc:
            confere(False, str(exc))
            continue
        confere(round(ponto, 2) == round(r["pollard"], 2), f"Tabela 8 Pollard {nome}")
        confere(round(lo, 2) == round(r["lo"], 2), f"Tabela 8 IC inferior {nome}")
        confere(round(hi, 2) == round(r["hi"], 2), f"Tabela 8 IC superior {nome}")
    confere(set(blocos) == {linha[0] for linha in linhas8},
            "Tabela 8 não cobre todos os blocos")

    # --- Tabela 9 == correlações externas ---
    mapa9 = {
        "HA × público médio": ("equipe_temporada", "todas", "spearman_ha_publico", "n"),
        "HA × público médio, sem 2020–2021": ("equipe_temporada", "sem_2020_2021", "spearman_ha_publico", "n"),
        "Pontos × público médio": ("equipe_temporada", "todas", "spearman_pts_publico", "n"),
        "Saldo de gols × público (bruto)": ("partida", "todas", "spearman_gd_publico", "n_publico"),
        "Saldo × público, controlando equipe-temporada e rank pré-jogo":
            ("partida", "todas", "spearman_parcial_controle_rank", "n_parcial"),
    }
    bloco9 = secao("**Tabela 9").split("Fonte:", 1)[0]
    linhas9 = _linhas_tabela(bloco9, 4, "Nível")
    confere(len(linhas9) == len(mapa9),
            f"Tabela 9 tem {len(linhas9)} linhas, esperado {len(mapa9)}")
    for nivel, relacao, rho_txt, n_txt in linhas9:
        chave = mapa9.get(relacao)
        confere(chave is not None, f"Tabela 9 relação desconhecida: {relacao}")
        if chave is None:
            continue
        grupo, recorte, campo, campo_n = chave
        r = externo[grupo][recorte]
        confere(n_txt == _num(r[campo_n]), f"Tabela 9 n {relacao}")
        confere(abs(_num_pt(rho_txt) - r[campo]) < 0.006, f"Tabela 9 rho {relacao}")

    # --- Tabela 10 == quartis de público por equipe ---
    quartis = {q["quartil"]: q for q in externo["equipe_publico"]["quartis"]}
    bloco10 = secao("**Tabela 10").split("Fonte:", 1)[0]
    linhas10 = _linhas_tabela(bloco10, 7, "Quartil")
    confere(len(linhas10) == len(quartis),
            f"Tabela 10 tem {len(linhas10)} linhas, esperado {len(quartis)}")
    for nome, times, publico, pts, ha, casa, fora in linhas10:
        confere(nome in quartis, f"Tabela 10 quartil desconhecido: {nome}")
        if nome not in quartis:
            continue
        r = quartis[nome]
        confere(times == _num(r["times"]), f"Tabela 10 times {nome}")
        confere(publico == _num(round(r["publico"])), f"Tabela 10 público {nome}")
        confere(abs(_num_pt(pts) - r["pts"]) < 0.06, f"Tabela 10 pontos {nome}")
        confere(abs(_num_pt(ha) - r["ha"]) < 0.006, f"Tabela 10 HA {nome}")
        confere(abs(_num_pt(casa) - r["home_ppg"]) < 0.006, f"Tabela 10 casa {nome}")
        confere(abs(_num_pt(fora) - r["away_ppg"]) < 0.006, f"Tabela 10 fora {nome}")
    confere(set(quartis) == {linha[0] for linha in linhas10},
            "Tabela 10 não cobre todos os quartis")
    corr_equipe = externo["equipe_publico"]["correlacoes"]
    confere(abs(corr_equipe["publico_ha"] - 0.043) < 0.001,
            "correlação público × HA por equipe")
    confere(abs(corr_equipe["publico_pts"] - 0.786) < 0.001,
            "correlação público × pontos por equipe")

    confere(mat_eq.shape == (12, 12), f"matriz_equipe {mat_eq.shape} != (12, 12)")
    confere(mat_part.shape == (8, 8), f"matriz_partida {mat_part.shape} != (8, 8)")
    for nome, matriz in (("equipe", mat_eq), ("partida", mat_part)):
        confere(np.allclose(np.diag(matriz), 1.0), f"diagonal da matriz {nome}")
        confere(np.allclose(matriz.values, matriz.values.T, equal_nan=True),
                f"matriz {nome} não simétrica")

    # --- descanso: ausentes não são imputados ---
    d = df.copy()
    d["rest_bucket"] = rest_bucket(d)
    confere(int(d["rest_bucket"].isna().sum()) == 194,
            f"descanso ausente: {int(d['rest_bucket'].isna().sum())} != 194")
    confere(len(d) - int(d["rest_bucket"].isna().sum()) == 7025,
            "partidas com descanso != 7025")

    # --- figuras, tabelas, todos ---
    corpo = secao("# 1 INTRODUÇÃO")
    nums, ordem = [], []
    for n in re.findall(r"Figura (\d+)", corpo):
        nums.append(int(n))
        if int(n) not in ordem:
            ordem.append(int(n))
    confere(ordem == list(range(1, 13)), f"ordem figuras {ordem}")
    confere((RAIZ / "figuras" / "fig12_publico_ha.png").exists(),
            "figura 12 ausente")
    for i in range(1, 11):
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
                 "tab6_equipes.csv", "tab7_correlacoes_equipe.csv",
                 "matriz_equipe.csv", "matriz_partida.csv", "contexto.json"):
        if not (figuras / nome).exists():
            p.error(f"artefato ausente: figuras/{nome}; rode scripts/analyze_context.py")
    tab1 = pd.read_csv(figuras / "tab1_indicadores_temporada.csv").sort_values("season")
    tab5 = pd.read_csv(figuras / "tab5_contexto.csv")
    tab6 = pd.read_csv(figuras / "tab6_equipes.csv")
    tab7 = pd.read_csv(figuras / "tab7_correlacoes_equipe.csv")
    mat_eq = pd.read_csv(figuras / "matriz_equipe.csv", index_col=0)
    mat_part = pd.read_csv(figuras / "matriz_partida.csv", index_col=0)
    contexto = json.loads((figuras / "contexto.json").read_text(encoding="utf-8"))
    for nome in ("external_summary.json", "quality_external.json"):
        if not (RAIZ / "data" / "external" / nome).exists():
            p.error(f"artefato externo ausente: data/external/{nome}; "
                    "rode scripts/build_external.py e scripts/analyze_external.py")
    externo = json.loads(
        (RAIZ / "data" / "external" / "external_summary.json").read_text(encoding="utf-8"))
    qualidade = json.loads(
        (RAIZ / "data" / "external" / "quality_external.json").read_text(encoding="utf-8"))
    erros = conferir(texto, df, tab1, tab5, tab6, tab7, mat_eq, mat_part,
                     contexto, externo, qualidade)
    return 1 if erros else 0


if __name__ == "__main__":
    raise SystemExit(main())
