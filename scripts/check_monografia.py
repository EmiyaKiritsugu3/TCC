#!/usr/bin/env python3
"""Auditoria da monografia: confere cada número do texto contra a base e os CSVs.

Uso: .venv/bin/python scripts/check_monografia.py
Falha (exit 1) na primeira divergência, com mensagem objetiva.
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "src"))

import pandas as pd
from metrics import by_season, summarize, team_season
from context import add_era_flags, rest_days, table_snapshot, travel_km

ERROS = []


def confere(cond, msg):
    if not cond:
        ERROS.append(msg)
        print(f"DIVERGÊNCIA: {msg}")


T = (RAIZ / "docs" / "monografia_v2.md").read_text(encoding="utf-8")
df = pd.read_csv(RAIZ / "data" / "processed" / "matches_processed.csv")
s = summarize(df)
t = by_season(df).set_index("season")
tab1 = pd.read_csv(RAIZ / "figuras" / "tab1_indicadores_temporada.csv").sort_values("season")


def cel(season, col):
    return tab1.loc[tab1.season == season, col].iloc[0]


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
               "2.659 de 2.660", "99,96%", "19/19", "31 testes", "31 passed",
               "25/02/2021", "Flamengo 2019: 53/37/90/38"]:
    confere(pedaco in T, f"trecho ausente: {pedaco!r}")

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

# --- Tabela 1 do md == CSV ==
bloco = T.split("**Tabela 1", 1)[1].split("Fonte:", 1)[0]
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
    if vals != esp:
        ok = False
        print(f"DIVERGÊNCIA Tabela 1/{ano}: md={vals} csv={esp}")
confere(ok, "Tabela 1 diverge do CSV")

# --- Tabela 5 == bandas calculadas ---
d = df.copy()
d["travel"] = travel_km(d)
bandas = [("Curta", d[d.travel < 500], 63.37),
          ("Média", d[(d.travel >= 500) & (d.travel < 1500)], 63.80),
          ("Longa", d[d.travel >= 1500], 63.90)]
tot = 0
for nome, sub, esp in bandas:
    x = summarize(sub)
    confere(round(x["pollard"], 2) == esp, f"Tabela 5 {nome}: {x['pollard']:.2f} != {esp}")
    tot += x["n"]
    confere(f"{x['n']:,}".replace(",", ".") in T, f"n Tabela 5 {nome} ausente no texto")
confere(tot == 7219, "bandas somam 7219")

# --- contexto: descanso/força/era ---
r = rest_days(df)
confere(round(summarize(df[r.home_rest.fillna(99) >= r.away_rest.fillna(99)])["pollard"], 2) == 64.25, "descanso casa")
confere(round(summarize(df[r.home_rest.fillna(99) < r.away_rest.fillna(99)])["pollard"], 2) == 61.96, "descanso fora")
sb = table_snapshot(df)
confere(round(summarize(df[sb.home_pos_before < sb.away_pos_before])["pollard"], 2) == 70.55, "favorito")
confere(round(summarize(df[sb.home_pos_before > sb.away_pos_before])["pollard"], 2) == 56.84, "zebra")
f = add_era_flags(df)
confere(round(summarize(f[~f.var_era])["pollard"], 2) == 64.88, "pre-VAR")
confere(round(summarize(f[f.var_era])["pollard"], 2) == 61.01, "era VAR")
confere(round(summarize(f[f.pandemia])["pollard"], 2) == 61.00, "pandemia")

# --- figuras, tabelas, todos ---
corpo = T.split("# 1 INTRODUÇÃO", 1)[1]
nums, ordem = [], []
for n in re.findall(r"Figura (\d)", corpo):
    nums.append(int(n))
    if int(n) not in ordem:
        ordem.append(int(n))
confere(ordem == list(range(1, 9)), f"ordem figuras {ordem}")
for i in range(1, 6):
    confere(f"Tabela {i}" in T, f"Tabela {i} ausente")

# --- citações x referências ---
refs = T.split("# REFERÊNCIAS", 1)[1].split("## APÊNDICE", 1)[0]
for sobrenome in ["ALMEIDA", "DUQUE", "FEW", "GIL", "MATOS", "NEAVE", "NEVILL",
                  "OPENFOOTBALL", "POLLARD", "RIBEIRO", "SHARDA", "SILVA",
                  "STREAMLIT"]:
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
    sys.exit(1)
print("AUDITORIA NUMÉRICA: tudo confere")
