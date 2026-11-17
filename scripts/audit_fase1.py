#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auditoria da Fase 1 — campeonato-brasileiro-full.csv (Brasileirao_Dataset).

Verifica, conforme a seção 8.2, 9.2 (etapa 3) e 15 da especificação do TCC:
  cobertura por temporada (referência: 380 partidas em 2006–2024),
  duplicatas, placares ausentes/inválidos, consistência do campo `vencedor`
  e nomes de clubes (insumo para a tabela de aliases).

Execução:  python3 scripts/audit_fase1.py [caminho_do_csv]
Saída:     relatório textual no stdout (sem alterar nenhum arquivo).

Este script não calcula indicadores (índice de Pollard etc.) — a Fase 3 cuida
deles, após a base estar validada (seção 21 da especificação).
"""
import argparse
import unicodedata
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent

REF_POR_TEMPORADA = 380          # 20 clubes, turno e returno (2006 em diante)
RECORTE = set(range(2006, 2025))  # temporadas 2006–2024
REF_ANTIGAS = {2003: 552, 2004: 552, 2005: 462}  # 24/24/22 clubes (referência de formato)

SEP = "=" * 72


def titulo(txt):
    print(f"\n{SEP}\n{txt}\n{SEP}")


def sem_acento(txt):
    if pd.isna(txt):
        return txt
    return "".join(c for c in unicodedata.normalize("NFKD", str(txt)) if not unicodedata.combining(c))


def _preparar(df: pd.DataFrame) -> pd.DataFrame:
    """Converte colunas-source em numéricas/datas e apara textos."""
    df["ID_num"] = pd.to_numeric(df["ID"], errors="coerce")
    df["rodada_n"] = pd.to_numeric(df["rodata"].str.strip(), errors="coerce")
    df["data_dt"] = pd.to_datetime(df["data"].str.strip(), format="%d/%m/%Y", errors="coerce")
    df["hg"] = pd.to_numeric(df["mandante_Placar"].str.strip(), errors="coerce")
    df["ag"] = pd.to_numeric(df["visitante_Placar"].str.strip(), errors="coerce")
    for c in ("mandante", "visitante", "vencedor"):
        df[c] = df[c].str.strip()
    return df


def _segmentar(df: pd.DataFrame) -> pd.DataFrame:
    """Segmenta temporadas por intervalo > 45 dias com rodada <= 5."""
    titulo("2. Temporadas detectadas (segmentação por intervalo entre rodadas)")
    d = df.sort_values(["data_dt", "ID_num"], na_position="last").reset_index(drop=True)
    seg = []
    atual = 0
    prev_dt = None
    for r, dt in zip(d["rodada_n"], d["data_dt"]):
        novo = atual == 0
        if not novo and prev_dt is not None and not pd.isna(r):
            if (dt - prev_dt).days > 45 and r <= 5:
                novo = True
        if novo:
            atual += 1
        seg.append(atual)
        prev_dt = dt
    d["segmento"] = seg

    pequenos = d.groupby("segmento").size()
    pequenos = pequenos[pequenos < 50].index.tolist()
    if pequenos:
        print(f"AVISO: segmentos com < 50 partidas mesclados no anterior: {pequenos}")
        for s in pequenos:
            d.loc[d["segmento"] == s, "segmento"] = s - 1
        d["segmento"] = d["segmento"].factorize()[0] + 1

    d["temporada"] = d.groupby("segmento")["data_dt"].transform(lambda x: x.iloc[0].year)
    return d


def _resumir_temporadas(d: pd.DataFrame) -> None:
    """Cobertura por temporada e contagem no recorte."""
    resumo = d.groupby("temporada").agg(
        partidas=("ID", "size"),
        inicio=("data_dt", "min"),
        fim=("data_dt", "max"),
        rodada_min=("rodada_n", "min"),
        rodada_max=("rodada_n", "max"),
        rodada_nula=("rodada_n", lambda x: x.isna().sum()),
        fora_do_ano=("data_dt", lambda x: 0),  # preenchido abaixo
    )
    fora = d.assign(ano=d["data_dt"].dt.year).groupby("temporada").apply(
        lambda g: (g["ano"] != g.name).sum(), include_groups=False
    )
    resumo["fora_do_ano"] = fora
    print(resumo.to_string())

    esperado_total = d["temporada"].isin(RECORTE).sum()
    print(f"\nPartidas no recorte 2006–2024: {esperado_total}")

    titulo("3. Recorte 2006–2024: observado vs esperado (380)")
    rec = d[d["temporada"].isin(RECORTE)]
    cont = rec.groupby("temporada").size()
    for t in sorted(RECORTE):
        obs = int(cont.get(t, 0))
        delta = obs - REF_POR_TEMPORADA
        flag = "ok" if delta == 0 else ("FALTA" if delta < 0 else "EXCESSO")
        print(f"  {t}: {obs:4d} (esperado {REF_POR_TEMPORADA})  delta {delta:+d}  {flag}")


def _checar_placares(d: pd.DataFrame) -> None:
    """Placares ausentes, negativos e máximos."""
    titulo("4. Placares")
    sem_placar = d["hg"].isna() | d["ag"].isna()
    print(f"Placar ausente (total na base): {sem_placar.sum()}")
    no_recorte = sem_placar & d["temporada"].isin(RECORTE)
    print(f"Placar ausente no recorte 2006–2024: {no_recorte.sum()}")
    if no_recorte.sum():
        cols = ["temporada", "data", "mandante", "visitante", "mandante_Placar", "visitante_Placar"]
        print(d.loc[no_recorte, cols].to_string())
    neg = ((d["hg"] < 0) | (d["ag"] < 0)).sum()
    print(f"Gols negativos: {neg}")
    print(f"Maior placar mandante: {d['hg'].max()} | Maior placar visitante: {d['ag'].max()}")


def _checar_duplicatas(d: pd.DataFrame) -> None:
    """Duplicatas por ID, linha, tripla e partidas espelhadas."""
    titulo("5. Duplicatas")
    dup_linha = d.duplicated().sum()
    dup_linha_sem_id = d.drop(columns=["ID", "ID_num"]).duplicated().sum()
    dup_id = d["ID_num"].duplicated(keep=False).sum()
    print(f"Linhas 100% duplicadas (com ID):    {dup_linha}")
    print(f"Linhas 100% duplicadas (sem ID):    {dup_linha_sem_id}")
    print(f"IDs repetidos (linhas envolvidas):  {dup_id}")

    chave = d.duplicated(subset=["data_dt", "mandante", "visitante"], keep=False)
    print(f"Triplas (data, mandante, visitante) repetidas: {chave.sum()}")
    if chave.sum():
        cols = ["temporada", "data", "mandante", "visitante", "mandante_Placar", "visitante_Placar", "ID"]
        print(d.loc[chave].sort_values(["data_dt", "mandante"])[cols].head(40).to_string())

    m = d.merge(d, on="ID", suffixes=("", "_y"))  # espelhadas: mesmo dia, times invertidos
    esp = m[
        (m["data_dt"] == m["data_dt_y"])
        & (m["mandante"] == m["visitante_y"])
        & (m["visitante"] == m["mandante_y"])
        & (m["ID_num"] != m["ID_num_y"])
    ]
    esp = esp[esp["ID_num"] < esp["ID_num_y"]]
    print(f"Partidas espelhadas no mesmo dia (possível inversão de mando): {len(esp)}")
    if len(esp):
        cols = ["data", "mandante", "visitante", "mandante_Placar", "visitante_Placar", "ID"]
        print(esp[cols].head(20).to_string())


def _checar_vencedor(rec: pd.DataFrame) -> None:
    """Confronta o campo `vencedor` com o resultado recalculado do placar."""
    titulo("7. Campo `vencedor` vs placar recalculado (2006–2024)")
    r = rec.copy()
    r["res_real"] = r["hg"].gt(r["ag"]).map({True: "H", False: None})
    r.loc[r["res_real"].isna() & r["hg"].notna() & r["ag"].notna(), "res_real"] = "A"
    r.loc[r["hg"] == r["ag"], "res_real"] = "E"

    ven_norm = r["vencedor"].map(lambda x: sem_acento(x).upper() if pd.notna(x) else x)
    mand_norm = r["mandante"].map(lambda x: sem_acento(x).upper())
    vis_norm = r["visitante"].map(lambda x: sem_acento(x).upper())

    esperado_h = ven_norm == mand_norm
    esperado_a = ven_norm == vis_norm
    esperado_e = ven_norm == "-"
    valido = r["hg"].notna() & r["ag"].notna()
    diverge = valido & (
        ((r["res_real"] == "H") & ~esperado_h)
        | ((r["res_real"] == "A") & ~esperado_a)
        | ((r["res_real"] == "E") & ~esperado_e)
    )
    print(f"Partidas avaliadas: {valido.sum()}")
    print(f"Divergências vencedor x placar: {diverge.sum()}")
    if diverge.sum():
        cols = ["temporada", "data", "mandante", "visitante", "mandante_Placar", "visitante_Placar", "vencedor"]
        print(r.loc[diverge, cols].head(15).to_string())


def _checar_clubes(rec: pd.DataFrame) -> None:
    """Nomes distintos e candidatos a variantes do mesmo clube."""
    titulo("8. Clubes distintos no recorte 2006–2024 (insumo p/ aliases)")
    casa = rec["mandante"].value_counts()
    fora = rec["visitante"].value_counts()
    clubes = pd.DataFrame({"mandante": casa, "visitante": fora}).fillna(0).astype(int)
    clubes["total"] = clubes["mandante"] + clubes["visitante"]
    print(f"Total de nomes distintos: {len(clubes)}")
    print(clubes.sort_index().to_string())

    titulo("8.1 Candidatos a variantes (normalizados sem acento, contendo um no outro)")
    idx_norm = {sem_acento(i).upper(): i for i in clubes.index}
    nomes = sorted(idx_norm)
    for a in nomes:
        for b in nomes:
            if a < b and (a in b or b in a):
                print(f"  '{idx_norm[a]}' <-> '{idx_norm[b]}'")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", nargs="?", help="caminho do CSV bruto")
    args = parser.parse_args()
    csv = Path(args.csv or RAIZ / "data/raw/campeonato-brasileiro-full.csv")

    df = pd.read_csv(csv, dtype=str, keep_default_na=False, na_values=[])
    print(f"Arquivo: {csv}")
    print(f"Linhas de dados: {len(df)}")
    print(f"Colunas: {list(df.columns)}")

    df = _preparar(df)

    titulo("1. Datas")
    sem_data = df["data_dt"].isna()
    print(f"Datas não interpretáveis: {sem_data.sum()}")
    if sem_data.sum():
        print(df.loc[sem_data, ["ID", "data", "mandante", "visitante"]].head(10).to_string())

    d = _segmentar(df)
    _resumir_temporadas(d)
    rec = d[d["temporada"].isin(RECORTE)]

    _checar_placares(d)
    _checar_duplicatas(d)

    titulo("6. Mandante igual a visitante")
    iguais = (d["mandante"] == d["visitante"]).sum()
    print(f"Linhas com mandante == visitante: {iguais}")
    if iguais:
        print(d.loc[d["mandante"] == d["visitante"], ["temporada", "data", "mandante", "ID"]].to_string())

    _checar_vencedor(rec)
    _checar_clubes(rec)


if __name__ == "__main__":
    main()
