#!/usr/bin/env python3
"""Auditoria independente dos dados do TCC (base, externos, junção e métricas)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "scripts"))

from associations import team_season_features  # noqa: E402
from join_external import carregar_bd, juntar, validar_fbref  # noqa: E402
from metrics import by_season, summarize  # noqa: E402

FALHAS: list[str] = []
OK = 0


def check(nome: str, cond: bool, detalhe: str = "") -> None:
    global OK
    if cond:
        OK += 1
        print(f"[ok] {nome}")
    else:
        FALHAS.append(f"{nome}: {detalhe}")
        print(f"[FALHA] {nome}: {detalhe}")


for rel in [
    "data/processed/matches_processed.csv",
    "data/external/basedosdados/brasileirao_serie_a_2006_2024.csv",
    "data/external/fbref/2024_serie_a.csv",
    "data/external/context_clean.csv",
    "data/external/quality_external.json",
    "data/external/external_summary.json",
]:
    if not (RAIZ / rel).exists():
        raise SystemExit(f"arquivo ausente: {rel}; rode o pipeline externo primeiro")

base = pd.read_csv(RAIZ / "data/processed/matches_processed.csv")
bd = pd.read_csv(RAIZ / "data/external/basedosdados/brasileirao_serie_a_2006_2024.csv")
fb = pd.read_csv(RAIZ / "data/external/fbref/2024_serie_a.csv")
ext = pd.read_csv(RAIZ / "data/external/context_clean.csv")
qual = json.loads((RAIZ / "data/external/quality_external.json").read_text())
resumo = json.loads((RAIZ / "data/external/external_summary.json").read_text())

# ---------------------------------------------------------------- base TCC
check("base: 7.219 linhas", len(base) == 7219, str(len(base)))
check("base: match_id único", base.match_id.is_unique, f"{base.match_id.duplicated().sum()} duplicados")
check("base: sem linha integral duplicada", base.duplicated().sum() == 0, str(base.duplicated().sum()))
check("base: sem tripla data/mandante/visitante duplicada",
      base.duplicated(["date", "home_team", "away_team"]).sum() == 0)
check("base: colunas obrigatórias sem nulos",
      base[["season", "home_team", "away_team", "home_goals", "away_goals",
            "result", "home_points", "away_points"]].notna().all().all())
check("base: gols inteiros e não negativos",
      (base.home_goals >= 0).all() and (base.away_goals >= 0).all()
      and np.allclose(base.home_goals, base.home_goals.astype(int))
      and np.allclose(base.away_goals, base.away_goals.astype(int)))
check("base: mandante != visitante", (base.home_team != base.away_team).all())
check("base: temporadas 2006–2024", sorted(base.season.unique()) == list(range(2006, 2025)))
check("base: contagem por temporada",
      base.groupby("season").size().to_dict() == {
          2006: 380, 2007: 380, 2008: 380, 2009: 380, 2010: 380, 2011: 380,
          2012: 380, 2013: 380, 2014: 380, 2015: 380, 2016: 379, 2017: 380,
          2018: 380, 2019: 380, 2020: 380, 2021: 380, 2022: 380, 2023: 380,
          2024: 380,
      })
check("base: 2020 termina em 2021-02-25",
      base.loc[base.season == 2020, "date"].max() == "2021-02-25")
check("base: 2016 tem 379 e falta Chapecoense×Atlético-MG",
      len(base[base.season == 2016]) == 379
      and len(base[(base.season == 2016) & (base.home_team == "Chapecoense")
                   & (base.away_team == "Atletico-MG")]) == 0)
check("base: estádio sempre presente", base.stadium.notna().all())
check("base: rodadas entre 1 e 38", base["round"].between(1, 38).all())
check("base: source único", base.source.nunique() == 1)

s = summarize(base)
check("métrica: n=7.219", s["n"] == 7219)
check("métrica: mandante 49,0%", round(s["p_home"], 1) == 49.0)
check("métrica: empate 26,8%", round(s["p_draw"], 1) == 26.8)
check("métrica: visitante 24,1%", round(s["p_away"], 1) == 24.1)
check("métrica: gols casa 1,49", round(s["avg_home_goals"], 2) == 1.49)
check("métrica: gols fora 1,00", round(s["avg_away_goals"], 2) == 1.00)
check("métrica: Pollard 63,66", round(s["pollard"], 2) == 63.66)
check("métrica: pontos casa 12.554", s["home_points"] == 12554)
check("métrica: pontos fora 7.166", s["away_points"] == 7166)

t = by_season(base).set_index("season")
for ano, valor in [(2017, 58.24), (2018, 69.51), (2019, 62.38),
                   (2020, 60.17), (2021, 61.83)]:
    check(f"métrica: Pollard {ano} = {valor}", round(t.loc[ano, "pollard"], 2) == valor,
          str(round(t.loc[ano, "pollard"], 2)))

fla = base[(base.season == 2019) & (base.home_team == "Flamengo")]
fla_fora = base[(base.season == 2019) & (base.away_team == "Flamengo")]
check("Flamengo 2019: 53 pontos em casa", fla.home_points.sum() == 53,
      str(fla.home_points.sum()))
check("Flamengo 2019: 37 pontos fora", fla_fora.away_points.sum() == 37,
      str(fla_fora.away_points.sum()))
check("Flamengo 2019: 38 jogos", len(fla) + len(fla_fora) == 38)
check("Flamengo 2019: casa 17-2-0",
      (fla.result.value_counts().get("H", 0),
       fla.result.value_counts().get("D", 0),
       fla.result.value_counts().get("A", 0)) == (17, 2, 0))
check("Flamengo 2019: fora 11-4-4",
      (fla_fora.result.value_counts().get("A", 0),
       fla_fora.result.value_counts().get("D", 0),
       fla_fora.result.value_counts().get("H", 0)) == (11, 4, 4))

# ---------------------------------------------------------------- raw/build
raw_check = subprocess.run(
    [sys.executable, "scripts/fetch_raw.py", "--check"],
    cwd=RAIZ, capture_output=True, text=True,
)
check("raw: SHA-256 do arquivo bruto confere",
      raw_check.returncode == 0, raw_check.stderr[-300:])
sha_antes = __import__("hashlib").sha256(
    (RAIZ / "data/processed/matches_processed.csv").read_bytes()).hexdigest()
build = subprocess.run(
    [sys.executable, "scripts/build_processed.py"],
    cwd=RAIZ, capture_output=True, text=True,
)
sha_depois = __import__("hashlib").sha256(
    (RAIZ / "data/processed/matches_processed.csv").read_bytes()).hexdigest()
check("build: reproduz a base byte a byte", sha_antes == sha_depois,
      f"{sha_antes} != {sha_depois}")
check("build: quality_report carregado=8.785 / mantidas=7.219",
      json.loads((RAIZ / "data/processed/quality_report.json").read_text())["loaded"] == 8785
      and json.loads((RAIZ / "data/processed/quality_report.json").read_text())["kept"] == 7219)

# ---------------------------------------------------------------- Base dos Dados
check("BD: 7.126 linhas", len(bd) == 7126, str(len(bd)))
check("BD: temporadas 2006–2024", sorted(bd.ano_campeonato.unique()) == list(range(2006, 2025)))
check("BD: 2024 tem 286 jogos", len(bd[bd.ano_campeonato == 2024]) == 286)
chave_bd = ["ano_campeonato", "time_mandante", "time_visitante",
            "gols_mandante", "gols_visitante"]
check("BD: chave (temporada, mandante, visitante, placar) única",
      bd.duplicated(chave_bd).sum() == 0, str(bd.duplicated(chave_bd).sum()))
check("BD: público não negativo", (bd.publico.dropna() >= 0).all())
check("BD: público máximo não negativo", (bd.publico_max.dropna() >= 0).all())
check("BD: público <= público_max quando ambos presentes",
      (bd.dropna(subset=["publico", "publico_max"]).eval("publico <= publico_max")).all())
check("BD: 2008 tem 217 zeros", int((bd[bd.ano_campeonato == 2008].publico == 0).sum()) == 217)
check("BD: 2008 não-zero = 163", int(bd[bd.ano_campeonato == 2008].publico.gt(0).sum()) == 163)
check("BD: 2020 tem 380 zeros", int((bd[bd.ano_campeonato == 2020].publico == 0).sum()) == 380)
check("BD: 2021 tem 218 zeros", int((bd[bd.ano_campeonato == 2021].publico == 0).sum()) == 218)
check("BD: 2008 média dos não-zero 18.287",
      round(bd[(bd.ano_campeonato == 2008) & bd.publico.gt(0)].publico.mean(), 0) == 18287)
check("BD: 2007 média 17.659",
      round(bd[bd.ano_campeonato == 2007].publico.mean(), 0) == 17659)
check("BD: 2009 média 17.712",
      round(bd[bd.ano_campeonato == 2009].publico.mean(), 0) == 17712)
max_bd = bd.publico.max()
check("BD: público máximo plausível (< 200 mil)", max_bd < 200000, str(max_bd))
check("BD: público de 2024 começa em 2024-04-13",
      bd[bd.ano_campeonato == 2024].data.min() == "2024-04-13")
check("BD: público de 2024 termina em 2024-10-27",
      bd[bd.ano_campeonato == 2024].data.max() == "2024-10-27")
check("BD: 2024 sem zeros", int((bd[bd.ano_campeonato == 2024].publico == 0).sum()) == 0)

# 2008: zeros espalhados por clubes/meses (evidência de missing)
z08 = bd[(bd.ano_campeonato == 2008) & (bd.publico == 0)]
check("BD: zeros de 2008 em >= 15 clubes", z08.time_mandante.nunique() >= 15,
      str(z08.time_mandante.nunique()))
check("BD: zeros de 2008 em >= 6 meses", z08.data.str[5:7].nunique() >= 6,
      str(z08.data.str[5:7].nunique()))

# 2021: zeros concentrados no início (retorno gradual)
z21 = bd[(bd.ano_campeonato == 2021) & (bd.publico == 0)]
check("BD: 2021 zeros antes de outubro",
      (z21.data < "2021-10-01").mean() > 0.95,
      f"{(z21.data < '2021-10-01').mean():.3f}")

# árbitros: contar nomes exatos e normalizados
def norm(s):
    import unicodedata, re
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()

arb = bd.arbitro.dropna().astype(str).str.strip()
check("BD: árbitros sem vazio", (arb != "").all())
check("BD: 178 nomes exatos de árbitro", arb.nunique() == 178, str(arb.nunique()))
check("BD: 177 nomes normalizados de árbitro", arb.map(norm).nunique() == 177,
      str(arb.map(norm).nunique()))

# ---------------------------------------------------------------- FBref
check("FBref: 380 jogos", len(fb) == 380, str(len(fb)))
check("FBref: 376 públicos", int(fb.attendance.notna().sum()) == 376,
      str(fb.attendance.notna().sum()))
check("FBref: 253 árbitros", int(fb.referee.notna().sum()) == 253,
      str(fb.referee.notna().sum()))
check("FBref: sem chave duplicada",
      fb.duplicated(["home", "away", "home_goals", "away_goals"]).sum() == 0)
check("FBref: público não negativo", (fb.attendance.dropna() >= 0).all())
check("FBref: público máximo plausível (< 200 mil)", fb.attendance.max() < 200000,
      str(fb.attendance.max()))

# ---------------------------------------------------------------- junção
junto = juntar(base, carregar_bd())
check("junção: 7.219 linhas", len(junto) == 7219, str(len(junto)))
check("junção: match_id único", junto.match_id.is_unique)
cobertura = junto.groupby("season")._merge.apply(lambda x: (x == "both").sum()).to_dict()
check("junção: 7.121 partidas com BD", int((junto._merge == "both").sum()) == 7121,
      str((junto._merge == "both").sum()))
check("junção: 2024 = 286", cobertura[2024] == 286, str(cobertura[2024]))
check("junção: 2006 = 376", cobertura[2006] == 376, str(cobertura[2006]))
check("junção: 2010 = 380", cobertura[2010] == 380, str(cobertura[2010]))
check("junção: 2016 = 379", cobertura[2016] == 379, str(cobertura[2016]))
check("junção: 2023 = 380", cobertura[2023] == 380, str(cobertura[2023]))

# 2006: partidas sem correspondência
sem06 = junto[(junto.season == 2006) & (junto._merge == "left_only")]
check("junção: 2006 tem 4 sem correspondência", len(sem06) == 4, str(len(sem06)))
print("  2006 sem correspondência:")
for r in sem06.itertuples():
    print(f"    {r.date} {r.home_team} {r.home_goals}x{r.away_goals} {r.away_team}")

# 2024: cobertura por mês da BD
bd24 = bd[bd.ano_campeonato == 2024].copy()
bd24["mes"] = bd24.data.str[:7]
print("  BD 2024 por mês:", bd24.groupby("mes").size().to_dict())
base24 = base[base.season == 2024].copy()
base24["mes"] = base24.date.str[:7]
print("  base 2024 por mês:", base24.groupby("mes").size().to_dict())

# validação FBref x BD
val = validar_fbref(junto, fb)
check("validação: 286 pares de público", val["pares_publico"] == 286,
      str(val["pares_publico"]))
check("validação: 243 públicos idênticos", val["iguais"] == 243, str(val["iguais"]))
check("validação: 248 diferenças <= 100", val["ate_100"] == 248, str(val["ate_100"]))
check("validação: 271 diferenças <= 1.000", val["ate_1000"] == 271, str(val["ate_1000"]))
check("validação: diferença média 316,3", round(val["media_diferenca"], 1) == 316.3,
      str(round(val["media_diferenca"], 1)))
pares = val["pares"].dropna(subset=["publico", "attendance"]).copy()
pares["dif"] = (pares.publico - pares.attendance).abs()
print("  maiores diferenças FBref x BD (2024):")
print(pares.nlargest(8, "dif")[["date", "home_team", "away_team", "publico",
                                "attendance", "dif"]].to_string(index=False))

# ---------------------------------------------------------------- base externa
check("externa: 7.219 linhas", len(ext) == 7219, str(len(ext)))
check("externa: match_id único", ext.match_id.is_unique)
check("externa: 6.618 registros de público", int(ext.publico.notna().sum()) == 6618,
      str(ext.publico.notna().sum()))
check("externa: 641 zeros totais", int((ext.publico == 0).sum()) == 641,
      str((ext.publico == 0).sum()))
check("externa: 598 zeros reais (2020+2021)", int(ext.publico_zero_real.sum()) == 598,
      str(ext.publico_zero_real.sum()))
check("externa: 6.821 árbitros", int(ext.arbitro.notna().sum()) == 6821,
      str(ext.arbitro.notna().sum()))
check("externa: 2.090 faltas", int(ext.faltas_mandante.notna().sum()) == 2090,
      str(ext.faltas_mandante.notna().sum()))
check("externa: público não negativo", (ext.publico.dropna() >= 0).all())
check("externa: público <= público_max quando ambos",
      (ext.dropna(subset=["publico", "publico_max"]).eval("publico <= publico_max")).all())
check("externa: 2008 sem zeros", int((ext[ext.season == 2008].publico == 0).sum()) == 0)
check("externa: 2020 com 380 zeros", int((ext[ext.season == 2020].publico == 0).sum()) == 380)
check("externa: 2021 com 218 zeros", int((ext[ext.season == 2021].publico == 0).sum()) == 218)
check("externa: 2024 com 376 registros", int(ext[ext.season == 2024].publico.notna().sum()) == 376)
check("externa: 2024 média 27.330,9",
      round(ext[ext.season == 2024].publico.mean(), 1) == 27330.9,
      str(round(ext[ext.season == 2024].publico.mean(), 1)))
check("externa: 2024 mediana 26.582",
      round(ext[ext.season == 2024].publico.median(), 1) == 26582.0,
      str(round(ext[ext.season == 2024].publico.median(), 1)))
check("externa: 2024 sem zeros", int((ext[ext.season == 2024].publico == 0).sum()) == 0)
check("externa: fontes de público 6.528 BD + 90 FBref",
      (ext.publico_fonte == "Base dos Dados").sum() == 6528
      and (ext.publico_fonte == "FBref").sum() == 90,
      f"{(ext.publico_fonte == 'Base dos Dados').sum()} / {(ext.publico_fonte == 'FBref').sum()}")
check("externa: 601 partidas sem registro de público",
      int(ext.publico.isna().sum()) == 601, str(ext.publico.isna().sum()))

# ---------------------------------------------------------------- métricas externas
# blocos
for bloco, esperado in [
    ("2007–2018", 64.94), ("2019", 62.38), ("2020 (portões fechados)", 60.17),
    ("2021 (retorno parcial)", 61.83), ("2022–2024", 60.55),
    ("Total 2007–2024", 63.63),
]:
    b = next(x for x in resumo["blocos"] if x["bloco"] == bloco)
    check(f"resumo: bloco {bloco} Pollard {esperado}",
          round(b["pollard"], 2) == esperado, str(round(b["pollard"], 2)))

# equipe-temporada: HA x público
ts = team_season_features(ext).set_index(["season", "team"])
pub = ext.groupby(["season", "home_team"]).publico.mean().rename("publico_medio")
pub.index = pub.index.set_names(["season", "team"])
ts = ts.join(pub)
p = ts[["ha", "publico_medio"]].dropna()
rho_ha = float(p["ha"].rank().corr(p["publico_medio"].rank()))
check("resumo: HA x público equipe-temporada 0,068",
      round(rho_ha, 3) == 0.068, str(round(rho_ha, 3)))
p2 = ts.loc[~ts.index.get_level_values("season").isin([2020, 2021]),
            ["ha", "publico_medio"]].dropna()
rho_ha2 = float(p2["ha"].rank().corr(p2["publico_medio"].rank()))
check("resumo: HA x público sem 2020–2021 −0,010",
      round(rho_ha2, 3) == -0.010, str(round(rho_ha2, 3)))
p3 = ts[["pts", "publico_medio"]].dropna()
rho_pts = float(p3["pts"].rank().corr(p3["publico_medio"].rank()))
check("resumo: pontos x público equipe-temporada 0,461",
      round(rho_pts, 3) == 0.461, str(round(rho_pts, 3)))

# partida: saldo x público bruto
d = ext.copy()
d["goal_diff"] = d.home_goals - d.away_goals
p4 = d[["goal_diff", "publico"]].dropna()
rho_gd = float(p4["goal_diff"].rank().corr(p4["publico"].rank()))
check("resumo: saldo x público bruto 0,079",
      round(rho_gd, 3) == 0.079, str(round(rho_gd, 3)))

# quartis de público por equipe
g = ts.reset_index().dropna(subset=["publico_medio"]).groupby("team").agg(
    temporadas=("season", "nunique"),
    publico=("publico_medio", "mean"),
    ha=("ha", "mean"),
    pts=("pts", "mean"),
).reset_index()
g = g[g.temporadas >= 5].copy()
g["quartil"] = pd.qcut(g.publico, 4, labels=["Q1 (menor)", "Q2", "Q3", "Q4 (maior)"])
q = g.groupby("quartil", observed=True).agg(
    times=("team", "size"), publico=("publico", "mean"),
    pts=("pts", "mean"), ha=("ha", "mean"),
).reset_index()
print("  quartis recalculados:")
print(q.round(3).to_string(index=False))
for _, r in q.iterrows():
    item = next(x for x in resumo["equipe_publico"]["quartis"]
                if x["quartil"] == r["quartil"])
    check(f"quartil {r['quartil']}: times {int(r['times'])}",
          int(r["times"]) == item["times"])
    check(f"quartil {r['quartil']}: público {round(r['publico'])}",
          round(r["publico"]) == round(item["publico"]))
    check(f"quartil {r['quartil']}: pontos {round(r['pts'], 1)}",
          round(r["pts"], 1) == round(item["pts"], 1))
    check(f"quartil {r['quartil']}: HA {round(r['ha'], 3)}",
          round(r["ha"], 3) == round(item["ha"], 3))

# árbitros
a = ext.dropna(subset=["arbitro"]).copy()
a["home_win"] = (a.home_goals > a.away_goals).astype(int)
por_arb = a.groupby("arbitro").agg(n=("home_win", "size"), hw=("home_win", "mean"))
com40 = por_arb[por_arb.n >= 40]
check("arbitragem: 6.821 jogos", len(a) == 6821, str(len(a)))
check("arbitragem: 177 árbitros", por_arb.shape[0] == 177, str(por_arb.shape[0]))
check("arbitragem: 50 árbitros com 40+ jogos", len(com40) == 50, str(len(com40)))
check("arbitragem: taxa de vitória do mandante 48,9%",
      round(a.home_win.mean() * 100, 1) == 48.9, str(round(a.home_win.mean() * 100, 1)))
check("arbitragem: faixa 40,8%–67,4%",
      round(com40.hw.min() * 100, 1) == 40.8
      and round(com40.hw.max() * 100, 1) == 67.4,
      f"{round(com40.hw.min()*100,1)}–{round(com40.hw.max()*100,1)}")
# z-scores
p0 = a.home_win.mean()
z = (com40.hw - p0) / np.sqrt(p0 * (1 - p0) / com40.n)
check("arbitragem: 1 árbitro fora de ±2 DP", int((z.abs() > 2).sum()) == 1,
      str(int((z.abs() > 2).sum())))

# ---------------------------------------------------------------- documentação
report = (RAIZ / "docs/analise_publico_arbitragem.md").read_text()
for trecho in ["27.331", "26.582", "6.618", "6.821", "177", "50", "598",
               "43,1", "59,4", "0,786", "0,043", "60,2", "60,6"]:
    check(f"relatório contém {trecho}", trecho in report)
mono = (RAIZ / "docs/monografia_v2.md").read_text()
for trecho in ["Com registro", "6.618 partidas com registro",
               "177 árbitros", "Tabela 10", "Figura 12", "0,786", "0,043"]:
    check(f"monografia contém {trecho}", trecho in mono)

print()
print(f"checks OK: {OK}; falhas: {len(FALHAS)}")
if FALHAS:
    print("\nFALHAS:")
    for f in FALHAS:
        print(" -", f)
    raise SystemExit(1)
print("AUDITORIA DE DADOS: tudo confere")
