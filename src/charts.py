"""Gráficos Plotly do dashboard (separados dos cálculos — RNF06)."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from formatting import pct

COR_HOME, COR_DRAW, COR_AWAY = "#1f77b4", "#7f7f7f", "#d62728"


def outcome_distribution(summary: dict, titulo="Resultados"):
    vals = [summary.get("p_home") or 0, summary.get("p_draw") or 0, summary.get("p_away") or 0]
    fig = go.Figure([go.Bar(
        x=["Vitória mandante", "Empate", "Vitória visitante"], y=vals,
        marker_color=[COR_HOME, COR_DRAW, COR_AWAY], text=[pct(v) for v in vals],
        textposition="outside",
    )])
    fig.update_layout(title=titulo, yaxis_title="% de partidas",
                      yaxis_range=[0, max(vals + [10]) * 1.2], separators=",.")
    return fig


def pollard_series(by_season_df: pd.DataFrame):
    fig = go.Figure()
    fig.add_hline(y=50, line_dash="dash", line_color="gray", annotation_text="50% (neutro)")
    fig.add_trace(go.Scatter(x=by_season_df["season"], y=by_season_df["pollard"],
                             mode="lines+markers", name="Pollard"))
    fig.update_layout(title="Índice de Pollard por temporada", xaxis_title="Temporada",
                      yaxis_title="VC (%)", separators=",.")
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
    fig.update_layout(xaxis_title="Temporada", yaxis_title="%", separators=",.")
    return fig


def goals_by_season(by_season_df: pd.DataFrame):
    m = by_season_df.melt(id_vars="season", value_vars=["avg_home_goals", "avg_away_goals"],
                          var_name="lado", value_name="media")
    m["lado"] = m["lado"].map({"avg_home_goals": "Mandante", "avg_away_goals": "Visitante"})
    fig = px.line(m, x="season", y="media", color="lado", markers=True,
                  color_discrete_map={"Mandante": COR_HOME, "Visitante": COR_AWAY},
                  title="Média de gols por temporada (casa × fora)")
    fig.update_layout(xaxis_title="Temporada", yaxis_title="Gols/partida", separators=",.")
    return fig


def pollard_by_group(effects: pd.DataFrame):
    """Barras horizontais de Pollard por grupo, com IC 95% e linha de 50%."""
    fig = go.Figure(go.Bar(
        x=effects["pollard"], y=effects["grupo"], orientation="h",
        marker_color=COR_HOME,
        error_x=dict(type="data", array=effects["hi"] - effects["pollard"],
                     arrayminus=effects["pollard"] - effects["lo"], color="black"),
    ))
    fig.add_vline(x=50, line_dash="dash", line_color="gray",
                  annotation_text="50% (neutro)")
    fig.update_layout(title="Pollard por contexto da partida",
                      xaxis_title="Índice de Pollard (%)",
                      yaxis_title="", separators=",.")
    return fig


def correlation_heatmap(matrix: pd.DataFrame, titulo="Matriz de correlação"):
    """Heatmap de uma matriz de correlação, com escala fixa em [-1, 1]."""
    fig = go.Figure(go.Heatmap(
        z=matrix.values, x=list(matrix.columns), y=list(matrix.index),
        zmin=-1, zmax=1, zmid=0, colorscale="RdBu",
        text=matrix.round(2).astype(str).values, texttemplate="%{text}",
        colorbar=dict(title="rho"),
    ))
    fig.update_layout(title=titulo, xaxis_tickangle=-40,
                      yaxis=dict(autorange="reversed"), separators=",.")
    return fig


def team_home_advantage_chart(team_df: pd.DataFrame):
    """Ranking de vantagem casa−fora (pontos/jogo), com IC 95%."""
    fig = go.Figure(go.Bar(
        x=team_df["ha"], y=team_df["team"], orientation="h",
        marker_color=COR_HOME,
        error_x=dict(type="data", array=team_df["hi"] - team_df["ha"],
                     arrayminus=team_df["ha"] - team_df["lo"], color="black"),
    ))
    fig.add_vline(x=0, line_dash="dash", line_color="gray",
                  annotation_text="0 (sem diferença)")
    fig.update_layout(title="Vantagem casa−fora por equipe (pontos por jogo)",
                      xaxis_title="Casa − fora (pontos/jogo)",
                      yaxis_title="", separators=",.")
    return fig
