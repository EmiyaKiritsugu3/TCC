"""Dashboard — vantagem de jogar em casa, Brasileirão Série A 2006–2024 (RF01–RF11)."""
from pathlib import Path

import pandas as pd
import streamlit as st

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from charts import goals_by_season, outcome_distribution, outcomes_by_season, pollard_series
from metrics import by_season, summarize, team_season

BASE = Path(__file__).resolve().parent
PROCESSED = BASE / "data" / "processed" / "matches_processed.csv"
QUALITY = BASE / "data" / "processed" / "quality_report.json"

st.set_page_config(page_title="Vantagem de jogar em casa — Brasileirão", layout="wide")


@st.cache_data
def carregar():
    try:
        df = pd.read_csv(PROCESSED)
    except FileNotFoundError:
        st.error(
            "Base processada não encontrada (`data/processed/matches_processed.csv`). "
            "Execute `python3 scripts/build_processed.py` primeiro. (RF01)"
        )
        st.stop()
    if df.empty:
        st.error("Base processada vazia. Reconstrua com `scripts/build_processed.py`. (RF01)")
        st.stop()
    faltam = [c for c in ("season", "home_team", "away_team", "home_goals",
                          "away_goals", "result", "home_points", "away_points")
              if c not in df.columns]
    if faltam:
        st.error(f"Colunas obrigatórias ausentes na base: {faltam}. (RF01)")
        st.stop()
    return df


df = carregar()
temporadas = sorted(df["season"].unique().tolist())

st.title("Vantagem de jogar em casa — Brasileirão Série A (2006–2024)")
st.caption("Análise descritiva de resultados históricos. Não prevê jogos nem afirma causalidade.")

# ---- filtros globais (RF02, RNF03: um único recorte alimenta tudo) ----
st.sidebar.header("Filtros")
sel = st.sidebar.multiselect("Temporadas", temporadas, default=temporadas)
if not sel:
    st.warning("Selecione ao menos uma temporada. (RF10)")
    st.stop()
base = df[df["season"].isin(sel)].copy()
if base.empty:  # RF10
    st.warning("Nenhuma partida para os filtros aplicados. Ajuste a seleção. (RF10)")
    st.stop()

resumo = summarize(base)
por_temp = by_season(base)

t1, t2, t3, t4 = st.tabs(["Visão geral", "Evolução histórica", "Equipes e partidas", "Metodologia e dados"])

with t1:  # RF03 + RF08
    c = st.columns(4)
    c[0].metric("Partidas", f"{resumo['n']:,}".replace(",", "."))
    c[1].metric("Vit. mandante", f"{resumo['p_home']:.1f}%")
    c[2].metric("Empates", f"{resumo['p_draw']:.1f}%")
    c[3].metric("Vit. visitante", f"{resumo['p_away']:.1f}%")
    c = st.columns(4)
    c[0].metric("Gols/partida (casa)", f"{resumo['avg_home_goals']:.2f}")
    c[1].metric("Gols/partida (fora)", f"{resumo['avg_away_goals']:.2f}")
    c[2].metric("Diferença média", f"{resumo['goal_diff']:+.2f}")
    c[3].metric("Pollard", f"{resumo['pollard']:.2f}%",
                help="VC = Pm/(Pm+Pv)×100. Pm/Pv = pontos de mandantes/visitantes no recorte. 50% = neutro.")
    st.plotly_chart(outcome_distribution(resumo), use_container_width=True)
    st.info("Índice de Pollard: acima de 50% = mandantes somaram mais pontos no recorte. "
            "É uma descrição agregada, não uma causa. (RF08)")

with t2:  # RF04 + RF05
    st.plotly_chart(pollard_series(por_temp), use_container_width=True)
    st.plotly_chart(outcomes_by_season(por_temp), use_container_width=True)
    st.plotly_chart(goals_by_season(por_temp), use_container_width=True)
    st.dataframe(por_temp.round(2), use_container_width=True, hide_index=True)

with t3:  # RF06 + RF07
    equipes = sorted(set(base["home_team"]) | set(base["away_team"]))
    col1, col2 = st.columns(2)
    equipe = col1.selectbox("Equipe", equipes)
    temp = col2.selectbox("Temporada", sorted(base["season"].unique().tolist()))
    ts = team_season(df, equipe, int(temp))
    c = st.columns(4)
    c[0].metric(f"{equipe} em casa", f"{ts['home_points']} pts",
                f"{ts['home_w']}V {ts['home_d']}E {ts['home_l']}D em {ts['home_n']} jogos")
    c[1].metric(f"{equipe} fora", f"{ts['away_points']} pts",
                f"{ts['away_w']}V {ts['away_d']}E {ts['away_l']}D em {ts['away_n']} jogos")
    c[2].metric("Total", f"{ts['home_points'] + ts['away_points']} pts")
    c[3].metric("Jogos", f"{ts['home_n'] + ts['away_n']}")
    jogos = base[((base["home_team"] == equipe) | (base["away_team"] == equipe))
                 & (base["season"] == int(temp))].sort_values("date")
    st.dataframe(jogos[["date", "round", "home_team", "home_goals", "away_goals",
                        "away_team", "result"]], use_container_width=True, hide_index=True)
    st.download_button("Baixar recorte filtrado (CSV)",  # RF11
                       base.to_csv(index=False).encode("utf-8"),
                       file_name="recorte_filtrado.csv", mime="text/csv")

with t4:  # RF09
    st.markdown(f"""**Fonte:** Brasileirão_Dataset (`adaoduque`), commit `15f027c`, acesso 2026-10-28.
Sem arquivo LICENSE no repositório — uso acadêmico pendente de autorização; CSV bruto não redistribuído.

**Período:** 2006–2024 · **Partidas válidas no recorte:** 7.219 (2016 com 379 — Chapecoense × Atlético-MG cancelada;
2020 disputada até 25/02/2021 por causa da pandemia).

**Fórmulas:** resultado do placar; pontos 3/1/0; proporções sobre o recorte;
Pollard `VC = Pm/(Pm+Pv)×100` (indefinido se Pm+Pv = 0).

**Limitações:** só placar e mando; sem torcida, arbitragem, elenco, viagens ou causalidade.
Detalhes em `docs/data_dictionary.md` e `docs/auditoria_fase1.md`.""")
    try:
        import json
        q = json.loads(QUALITY.read_text(encoding="utf-8"))
        st.json({"excluídas": q["excluded"], "abaixo_do_esperado": q["seasons_below_expected"]})
    except FileNotFoundError:
        st.caption("quality_report.json não encontrado.")
