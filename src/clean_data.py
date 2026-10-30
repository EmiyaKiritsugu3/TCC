"""Limpeza e padronização da base (Fase 2, seção 15 da spec)."""
from pathlib import Path

import pandas as pd

SOURCE_LABEL = "Brasileirao_Dataset commit 15f027c (acesso 2026-10-28)"

# Tabela de aliases: normalização ortográfica -> nome canônico.
# A auditoria (Fase 1) não encontrou variantes dentro do recorte 2006–2024
# (Barueri/2009 e Grêmio Prudente/2010 são a mesma franquia renomeada ENTRE
# temporadas — mantidas separadas por temporada, com nota na monografia).
ALIASES: dict[str, str] = {}

SEASON_MIN, SEASON_MAX = 2006, 2024
EXPECTED_PER_SEASON = 380


def _strip(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for c in df.columns:
        if df[c].dtype == object:
            df[c] = df[c].astype(str).str.strip()
    return df


def assign_seasons(dates: pd.Series, rounds: pd.Series) -> pd.Series:
    """Atribui a temporada por intervalo entre partidas.

    Jogos reagendados carregam a rodada ORIGINAL (caso 2020/COVID), logo
    segmentar por "rodada reinicia em 1" quebra. Regra: ordena por data;
    um novo segmento começa quando o intervalo desde a partida anterior é
    > 45 dias E a rodada é pequena (<= 5). A temporada é o ano da primeira
    partida do segmento.
    """
    order = dates.sort_values(kind="mergesort").index
    seg = pd.Series(0, index=dates.index, dtype=int)
    cur, prev_dt, prev_r = 0, None, None
    for i in order:
        dt, r = dates.loc[i], rounds.loc[i]
        novo = cur == 0
        if not novo and pd.notna(dt) and prev_dt is not None and pd.notna(r):
            if (dt - prev_dt).days > 45 and r <= 5:
                novo = True
        if novo:
            cur += 1
        seg.loc[i] = cur
        if pd.notna(dt):
            prev_dt = dt
        prev_r = r
    first_year = dates.groupby(seg).transform("min").dt.year
    return first_year


def clean_matches(df_raw: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Padroniza a base bruta. Retorna (base_limpa, relatório)."""
    report: dict = {"loaded": int(len(df_raw)), "excluded": {}}

    def drop(mask, reason: str, df: pd.DataFrame) -> pd.DataFrame:
        n = int(mask.sum())
        if n:
            report["excluded"][reason] = report["excluded"].get(reason, 0) + n
        return df.loc[~mask].copy()

    df = _strip(df_raw)

    df["match_id"] = df["ID"].astype(str)
    df["round"] = pd.to_numeric(df["rodata"], errors="coerce")
    df["date_dt"] = pd.to_datetime(df["data"], format="%d/%m/%Y", errors="coerce")
    df["home_team"] = df["mandante"].map(lambda x: ALIASES.get(x, x))
    df["away_team"] = df["visitante"].map(lambda x: ALIASES.get(x, x))
    df["home_goals"] = pd.to_numeric(df["mandante_Placar"], errors="coerce")
    df["away_goals"] = pd.to_numeric(df["visitante_Placar"], errors="coerce")
    df["stadium"] = df["arena"] if "arena" in df.columns else ""
    df["winner_raw"] = df["vencedor"] if "vencedor" in df.columns else ""

    df = drop(df["date_dt"].isna(), "data_invalida", df)
    # Placar ausente ou não-numérico: nunca vira 0 (seção 15, item 4).
    df = drop(df["home_goals"].isna() | df["away_goals"].isna(), "placar_ausente", df)
    # Negativos ou fracionários são inválidos.
    bad_goal = (
        (df["home_goals"] < 0)
        | (df["away_goals"] < 0)
        | (df["home_goals"] % 1 != 0)
        | (df["away_goals"] % 1 != 0)
    )
    df = drop(bad_goal, "placar_invalido", df)
    df = drop(df["home_team"] == df["away_team"], "mandante_igual_visitante", df)
    df = drop(df["home_team"].eq("") | df["away_team"].eq(""), "clube_ausente", df)

    # Duplicatas: mantém a primeira ocorrência, registra o resto.
    df = df.sort_values(["date_dt", "match_id"]).reset_index(drop=True)
    dup_id = df.duplicated(subset=["match_id"], keep="first")
    df = drop(dup_id, "match_id_duplicado", df)
    dup_full = df.duplicated(keep="first")
    df = drop(dup_full, "linha_duplicada", df)
    dup_key = df.duplicated(subset=["date_dt", "home_team", "away_team"], keep="first")
    n_key = int(dup_key.sum())
    if n_key:
        report["excluded"]["tripla_data_mandante_visitante_repetida"] = n_key
        df = df.loc[~dup_key].copy()

    # Temporada por intervalo (robusto a reagendamentos) + filtro do recorte.
    df["season"] = assign_seasons(df["date_dt"], df["round"]).astype(int)
    fora = ~df["season"].between(SEASON_MIN, SEASON_MAX)
    df = drop(fora, f"fora_do_recorde_{SEASON_MIN}_{SEASON_MAX}", df)

    # Resultado e pontos recalculados do placar (seção 10.2); `vencedor`
    # serve só para auditoria, nunca para o cálculo.
    df["home_goals"] = df["home_goals"].astype(int)
    df["away_goals"] = df["away_goals"].astype(int)
    df["result"] = "D"
    df.loc[df["home_goals"] > df["away_goals"], "result"] = "H"
    df.loc[df["home_goals"] < df["away_goals"], "result"] = "A"
    df["home_points"] = df["result"].map({"H": 3, "D": 1, "A": 0}).astype(int)
    df["away_points"] = df["result"].map({"H": 0, "D": 1, "A": 3}).astype(int)

    clean = pd.DataFrame(
        {
            "match_id": df["match_id"].astype(str),
            "season": df["season"].astype(int),
            "date": df["date_dt"].dt.strftime("%Y-%m-%d"),
            "round": df["round"].astype("Int64"),
            "home_team": df["home_team"],
            "away_team": df["away_team"],
            "home_goals": df["home_goals"],
            "away_goals": df["away_goals"],
            "result": df["result"],
            "home_points": df["home_points"],
            "away_points": df["away_points"],
            "stadium": df["stadium"].astype(str),
            "source": SOURCE_LABEL,
        }
    ).sort_values(["season", "date", "match_id"]).reset_index(drop=True)

    coverage = clean.groupby("season").size().to_dict()
    report.update(
        {
            "kept": int(len(clean)),
            "coverage_per_season": {int(k): int(v) for k, v in coverage.items()},
            "seasons_below_expected": {
                int(s): int(EXPECTED_PER_SEASON - c)
                for s, c in coverage.items()
                if c < EXPECTED_PER_SEASON
            },
            "notes": [
                "2016 tem 379 partidas: Chapecoense x Atletico-MG (rodada 38) cancelada.",
                "Temporada 2020 vai de 2020-08-08 a 2021-02-25 (COVID-19); temporada atribuída por intervalo, não por ano civil.",
                "Barueri (2009) e Gremio Prudente (2010): mesma franquia renomeada; mantidas separadas por temporada.",
            ],
        }
    )
    return clean, report


def save_processed(clean: pd.DataFrame, report: dict, out_dir: str | Path) -> None:
    """Grava matches_processed.csv + quality_report.json."""
    import json

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    clean.to_csv(out / "matches_processed.csv", index=False)
    with open(out / "quality_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
