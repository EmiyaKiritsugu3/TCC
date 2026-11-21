"""Dashboard — vantagem de jogar em casa, Brasileirão Série A."""
import os
from pathlib import Path

import pandas as pd
import streamlit as st

from associations import (
    correlation_matrix,
    correlation_with,
    group_pollard,
    match_features,
    team_home_advantage,
    team_season_features,
)
from charts import (
    correlation_heatmap,
    goals_by_season,
    outcome_distribution,
    outcomes_by_season,
    pollard_by_group,
    pollard_series,
    team_home_advantage_chart,
)
from context import DIMENSOES_CONTEXTO, build_context_frame, grupos_contexto
from formatting import num, pct, signed
from metrics import by_season, summarize, team_season, teams_in_season

BASE = Path(__file__).resolve().parent
PROCESSED = Path(os.environ.get(
    "TCC_PROCESSED", BASE / "data" / "processed" / "matches_processed.csv"))
QUALITY = Path(os.environ.get(
    "TCC_QUALITY", BASE / "data" / "processed" / "quality_report.json"))

st.set_page_config(page_title="Vantagem de jogar em casa — Brasileirão", layout="wide")


@st.cache_data
def carregar():
    try:
        df = pd.read_csv(PROCESSED)
    except FileNotFoundError:
        st.error(
            f"Base processada não encontrada em `{PROCESSED}`. "
            "Rode `scripts/build_mit_base.py` (2013–2024) ou "
            "`scripts/build_processed.py` (2006–2024) e aponte "
            "`TCC_PROCESSED` para o CSV gerado. (RF01)"
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


@st.cache_data
def carregar_contexto():
    """Calcula as variáveis contextuais uma vez por processo (aba Contexto)."""
    return build_context_frame(carregar())


@st.cache_data(show_spinner=False)
def contexto_efeitos(temporadas: tuple[int, ...], dimensao: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Pollard por grupo, cacheado por temporadas e dimensão."""
    ctx = carregar_contexto()
    ctx = ctx[ctx["season"].isin(temporadas)].copy()
    return ctx, group_pollard(ctx, grupos_contexto(ctx, dimensao), n=1000, seed=42)


@st.cache_data(show_spinner=False)
def contexto_equipes(temporadas: tuple[int, ...]) -> pd.DataFrame:
    """Ranking por equipe, cacheado por temporadas."""
    ctx = carregar_contexto()
    ctx = ctx[ctx["season"].isin(temporadas)].copy()
    return team_home_advantage(ctx, n=500, seed=42)


df = carregar()
temporadas = sorted(df["season"].unique().tolist())

st.title(f"Vantagem de jogar em casa — Brasileirão Série A "
         f"({int(df['season'].min())}–{int(df['season'].max())})")
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

t1, t2, t3, t4, t5 = st.tabs([
    "Visão geral", "Evolução histórica", "Equipes e partidas",
    "Metodologia e dados", "Contexto",
])

with t1:  # RF03 + RF08
    c = st.columns(4)
    c[0].metric("Partidas", f"{resumo['n']:,}".replace(",", "."))
    c[1].metric("Vit. mandante", pct(resumo["p_home"]))
    c[2].metric("Empates", pct(resumo["p_draw"]))
    c[3].metric("Vit. visitante", pct(resumo["p_away"]))
    c = st.columns(4)
    c[0].metric("Gols/partida (casa)", num(resumo["avg_home_goals"]))
    c[1].metric("Gols/partida (fora)", num(resumo["avg_away_goals"]))
    c[2].metric("Diferença média", signed(resumo["goal_diff"]))
    c[3].metric("Pollard", pct(resumo["pollard"], 2),
                help="VC = Pm/(Pm+Pv)×100. Pm/Pv = pontos de mandantes/visitantes no recorte. 50% = neutro.")
    st.plotly_chart(outcome_distribution(resumo), width="stretch")
    st.info("Índice de Pollard: acima de 50% = mandantes somaram mais pontos no recorte. "
            "É uma descrição agregada, não uma causa. (RF08)")

with t2:  # RF04 + RF05
    st.plotly_chart(pollard_series(por_temp), width="stretch")
    st.plotly_chart(outcomes_by_season(por_temp), width="stretch")
    st.plotly_chart(goals_by_season(por_temp), width="stretch")
    st.dataframe(por_temp.round(2), width="stretch", hide_index=True)

with t3:  # RF06 + RF07 + RF10
    col1, col2 = st.columns(2)
    temp = col1.selectbox(
        "Temporada", sorted(base["season"].unique().tolist()), key="temporada"
    )
    equipes = teams_in_season(base, int(temp))
    if not equipes:
        st.warning("Nenhuma equipe para a temporada selecionada. (RF10)")
        st.stop()
    if st.session_state.get("equipe") not in equipes:
        st.session_state["equipe"] = equipes[0]
    equipe = col2.selectbox("Equipe", equipes, key="equipe")

    ts = team_season(base, equipe, int(temp))
    if ts["home_n"] + ts["away_n"] == 0:
        st.warning(
            f"{equipe} não disputou a Série A em {temp}. "
            "Selecione outra temporada ou equipe. (RF10)"
        )
    else:
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
                            "away_team", "result"]], width="stretch", hide_index=True)
        st.download_button("Baixar recorte filtrado (CSV)",  # RF11
                           base.to_csv(index=False).encode("utf-8"),
                           file_name="recorte_filtrado.csv", mime="text/csv")

with t4:  # RF09
    fontes = sorted(set(df["source"].dropna())) if "source" in df.columns else []
    fonte = fontes[0] if fontes else "fonte não informada"
    if "BrazilianFootball" in fonte:
        nota_fonte = (f"**Fonte:** {fonte}. Licença MIT; base derivada com "
                      "atribuição. CSV bruto não redistribuído.")
    else:
        nota_fonte = (f"**Fonte:** {fonte}. Sem arquivo LICENSE no repositório — "
                      "uso acadêmico pendente de autorização; CSV bruto não redistribuído.")
    periodo = f"{int(df['season'].min())}–{int(df['season'].max())}"
    partidas = f"{len(df):,}".replace(",", ".")
    temporadas = set(df["season"].unique().tolist())
    casos = []
    if 2016 in temporadas:
        casos.append("2016 com 379 — Chapecoense × Atlético-MG cancelada")
    if 2020 in temporadas:
        casos.append("2020 disputada até 25/02/2021 por causa da pandemia")
    nota_casos = (" " + "; ".join(casos) + ".") if casos else ""
    st.markdown(f"""{nota_fonte}

**Período:** {periodo} · **Partidas válidas no recorte:** {partidas}.{nota_casos}

**Fórmulas:** resultado do placar; pontos 3/1/0; proporções sobre o recorte;
Pollard `VC = Pm/(Pm+Pv)×100` (indefinido se Pm+Pv = 0).

**Limitações:** a base tem placar e mando; a aba Contexto acrescenta distância,
clássico, estádio, descanso e força. Torcida, arbitragem, elenco e clima não são
medidos, e nenhuma associação é causal.
Detalhes em `docs/data_dictionary.md` e `docs/auditoria_fase1.md`.""")
    try:
        import json
        q = json.loads(QUALITY.read_text(encoding="utf-8"))
        st.json({"excluídas": q["excluded"], "abaixo_do_esperado": q["seasons_below_expected"]})
    except FileNotFoundError:
        st.caption("quality_report.json não encontrado.")

with t5:  # RF12: contexto descritivo (viagem, clássico, estádio, descanso, força, era)
    st.subheader("Contexto da partida")
    st.caption("Associações descritivas com o recorte selecionado. Não implicam causalidade.")
    try:
        ctx = carregar_contexto()
    except (ValueError, KeyError) as exc:
        st.warning(f"Não foi possível calcular o contexto desta base: {exc}")
        ctx = None
    if ctx is not None:
        ctx = ctx[ctx["season"].isin(sel)].copy()
        if ctx.empty:
            st.warning("Nenhuma partida para os filtros aplicados. (RF10)")
        else:
            dimensao = st.selectbox("Dimensão do contexto", DIMENSOES_CONTEXTO,
                                    key="contexto_dimensao")
            temporadas_sel = tuple(sorted(sel))
            ctx, efeitos = contexto_efeitos(temporadas_sel, dimensao)
            efeitos = efeitos.dropna(subset=["pollard", "lo", "hi"])
            resumo_ctx = summarize(ctx)
            c = st.columns(3)
            c[0].metric("Partidas no contexto", f"{resumo_ctx['n']:,}".replace(",", "."))
            c[1].metric("Pollard do recorte", pct(resumo_ctx["pollard"], 2))
            c[2].metric("Grupos", len(efeitos))
            st.plotly_chart(pollard_by_group(efeitos), width="stretch")
            st.dataframe(efeitos.round(2), width="stretch", hide_index=True)
            st.info(
                "A distância é entre cidades-sede (haversine), não o deslocamento real. "
                "Clássicos na mesma cidade têm distância zero. O descanso conta apenas "
                "partidas da Série A. (RF12)"
            )
            with st.expander("Ranking por equipe (casa − fora)"):
                equipes = contexto_equipes(temporadas_sel)
                st.plotly_chart(team_home_advantage_chart(equipes), width="stretch")
                st.caption(
                    "Equipes com poucas partidas têm intervalo de confiança amplo; "
                    "o ranking é exploratório."
                )
            st.divider()
            st.subheader("Matriz de correlação")
            nivel_matriz = st.radio(
                "Nível", ["Equipe-temporada", "Partida"], horizontal=True,
                key="matriz_nivel",
            )
            if nivel_matriz == "Equipe-temporada":
                features = team_season_features(ctx)
                if len(features) < 30:
                    st.warning(
                        "Com menos de 30 equipe-temporadas, a matriz de correlação "
                        "não é estimável. Selecione mais temporadas. (RF12)"
                    )
                else:
                    matriz = correlation_matrix(features)
                    st.plotly_chart(
                        correlation_heatmap(matriz, "Correlações por equipe-temporada (Spearman)"),
                        width="stretch",
                    )
                    st.dataframe(correlation_with(features, "ha").round(2),
                                 width="stretch", hide_index=True)
                    st.caption(
                        "HA = pontos/jogo em casa − fora. home_ppg e away_ppg são "
                        "componentes do HA; a leitura substantiva está nas variáveis "
                        "de contexto (distância, estádio, temporada)."
                    )
            else:
                features = match_features(ctx)
                if len(features) < 30:
                    st.warning(
                        "Com menos de 30 partidas, a matriz de correlação não é "
                        "estimável. Selecione mais temporadas. (RF12)"
                    )
                else:
                    matriz = correlation_matrix(features)
                    st.plotly_chart(
                        correlation_heatmap(matriz, "Correlações por partida (Spearman)"),
                        width="stretch",
                    )
                    st.dataframe(correlation_with(features, "goal_diff").round(2),
                                 width="stretch", hide_index=True)
                    st.caption(
                        "Partidas não são independentes; a matriz é descritiva e "
                        "não deve ser lida como efeito causal."
                    )
