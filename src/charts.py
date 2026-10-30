"""Gráficos Plotly do dashboard (separados dos cálculos — RNF06)."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

COR_HOME, COR_DRAW, COR_AWAY = "#1f77b4", "#7f7f7f", "#d62728"


def outcome_distribution(summary: dict, titulo="Resultados"):
    vals = [summary.get("p_home") or 0, summary.get("p_draw") or 0, summary.get("p_away") or 0]
    fig = go.Figure([go.Bar(
        x=["Vitória mandante", "Empate", "Vitória visitante"], y=vals,
        marker_color=[COR_HOME, COR_DRAW, COR_AWAY], text=[f"{v:.1f}%" for v in vals],
        textposition="outside",
    )])
    fig.update_layout(title=titulo, yaxis_title="% de partidas", yaxis_range=[0, max(vals + [10]) * 1.2])
    return fig


def pollard_series(by_season_df: pd.DataFrame):
    fig = go.Figure()
    fig.add_hline(y=50, line_dash="dash", line_color="gray", annotation_text="50% (neutro)")
    fig.add_trace(go.Scatter(x=by_season_df["season"], y=by_season_df["pollard"],
                             mode="lines+markers", name="Pollard"))
    fig.update_layout(title="Índice de Pollard por temporada", xaxis_title="Temporada",
                      yaxis_title="VC (%)")
    return fig


def outcomes_by_season(by_season_df: pd.DataFrame):
    m = by_season_df.melt(id_vars="season", value_vars=["p_home", "p_draw", "p_away"],
                          var_name="resultado", value_name="pct")
    nomes = {"p_home": "Vit. mandante", "p_draw": "Empate", "p_away": "Vit. visitante"}
    m["resultado"] = m["resultado"].map(nomes)
    fig = px.bar(m, x="season", y="pct", color="resultado", barmode="stack",
                 color_discrete_map={"Vit. mandante": COR_HOME, "Empate": COR_DRAW,
                                     "Vit. visitante": COR_AWAY},
                 title="Distribuição de resultados por temporada")
    fig.update_layout(xaxis_title="Temporada", yaxis_title="%")
    return fig


def goals_by_season(by_season_df: pd.DataFrame):
    m = by_season_df.melt(id_vars="season", value_vars=["avg_home_goals", "avg_away_goals"],
                          var_name="lado", value_name="media")
    m["lado"] = m["lado"].map({"avg_home_goals": "Mandante", "avg_away_goals": "Visitante"})
    fig = px.line(m, x="season", y="media", color="lado", markers=True,
                  color_discrete_map={"Mandante": COR_HOME, "Visitante": COR_AWAY},
                  title="Média de gols por temporada (casa × fora)")
    fig.update_layout(xaxis_title="Temporada", yaxis_title="Gols/partida")
    return fig
