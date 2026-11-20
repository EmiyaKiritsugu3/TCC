#!/usr/bin/env python3
"""Exporta a tabela histórica da Base dos Dados via BigQuery.

A consulta usa a tabela pública:
  basedosdados.mundo_transfermarkt_competicoes.brasileirao_serie_a

Requisitos:
  - `gcloud auth application-default login` (uma vez)
  - um projeto de billing no BigQuery (free tier cobre poucos GB)
  - `requests` e `pandas` instalados

Uso:
  python3 scripts/fetch_basedosdados.py --project SEU_PROJETO
  python3 scripts/fetch_basedosdados.py --project SEU_PROJETO --out data/external/basedosdados/brasileirao_serie_a_2006_2024.csv
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

from paths import caminho_no_projeto

RAIZ = Path(__file__).resolve().parent.parent
PADRAO = RAIZ / "data" / "external" / "basedosdados" / "brasileirao_serie_a_2006_2024.csv"
URL = "https://bigquery.googleapis.com/bigquery/v2/projects/{project}/queries"

COLUNAS = [
    "ano_campeonato", "data", "rodada", "estadio", "arbitro", "publico",
    "publico_max", "time_mandante", "time_visitante", "tecnico_mandante",
    "tecnico_visitante", "colocacao_mandante", "colocacao_visitante",
    "valor_equipe_titular_mandante", "valor_equipe_titular_visitante",
    "idade_media_titular_mandante", "idade_media_titular_visitante",
    "gols_mandante", "gols_visitante", "gols_1_tempo_mandante",
    "gols_1_tempo_visitante", "escanteios_mandante", "escanteios_visitante",
    "faltas_mandante", "faltas_visitante", "chutes_bola_parada_mandante",
    "chutes_bola_parada_visitante", "defesas_mandante", "defesas_visitante",
    "impedimentos_mandante", "impedimentos_visitante", "chutes_mandante",
    "chutes_visitante", "chutes_fora_mandante", "chutes_fora_visitante",
]


def _projeto(explicito: str | None) -> str:
    if explicito:
        return explicito
    for chave in ("BIGQUERY_PROJECT", "GOOGLE_CLOUD_PROJECT"):
        if os.environ.get(chave):
            return os.environ[chave]
    try:
        saida = subprocess.check_output(
            ["gcloud", "config", "get-value", "billing/quota_project"],
            text=True, stderr=subprocess.DEVNULL,
        ).strip()
        if saida and saida != "(unset)":
            return saida
    except (OSError, subprocess.CalledProcessError):
        pass
    raise SystemExit(
        "Informe o projeto de billing com --project ou defina BIGQUERY_PROJECT.\n"
        "Exemplo: python3 scripts/fetch_basedosdados.py --project meu-projeto"
    )


def _token() -> str:
    try:
        return subprocess.check_output(
            ["gcloud", "auth", "application-default", "print-access-token"],
            text=True, stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise SystemExit(
            "Não foi possível obter o token do Google Cloud. Rode:\n"
            "  gcloud auth application-default login\n"
        ) from exc


def _sql(inicio: int, fim: int) -> str:
    colunas = ",\n  ".join(COLUNAS)
    return f"""
SELECT
  {colunas}
FROM `basedosdados.mundo_transfermarkt_competicoes.brasileirao_serie_a`
WHERE ano_campeonato BETWEEN {inicio} AND {fim}
ORDER BY ano_campeonato, data, time_mandante
""".strip()


def _consultar(project: str, token: str, sql: str) -> pd.DataFrame:
    """Executa a consulta e pagina via jobs.getQueryResults.

    `jobs.query` devolve no máximo `maxResults` linhas e um `jobReference`;
    as páginas seguintes precisam ser buscadas no job, não reenviando a
    consulta com `pageToken`.
    """
    if not re.fullmatch(r"[a-z0-9][a-z0-9:.-]{4,62}", project):
        raise SystemExit(f"projeto BigQuery inválido: {project}")
    headers = {"Authorization": f"Bearer {token}"}
    resposta = requests.post(
        URL.format(project=project),
        headers=headers,
        json={"query": sql, "useLegacySql": False, "maxResults": 10000},
        timeout=180,
    )
    if resposta.status_code != 200:
        raise SystemExit(f"BigQuery retornou HTTP {resposta.status_code}: "
                         f"{resposta.text[:800]}")
    dados = resposta.json()
    job = dados.get("jobReference", {})
    job_id = job.get("jobId")
    if not job_id or not re.fullmatch(r"[A-Za-z0-9_-]+", job_id):
        raise SystemExit("BigQuery não retornou jobId válido")
    location = job.get("location")
    url_resultados = (
        "https://bigquery.googleapis.com/bigquery/v2/projects/"
        f"{project}/queries/{job_id}"
    )
    parametros = {"timeoutMs": 10000}
    if location:
        parametros["location"] = location
    while not dados.get("jobComplete", True):
        resposta = requests.get(url_resultados, headers=headers,
                                params=parametros, timeout=180)
        if resposta.status_code != 200:
            raise SystemExit(f"BigQuery retornou HTTP {resposta.status_code}: "
                             f"{resposta.text[:800]}")
        dados = resposta.json()

    linhas: list[list[str | None]] = []
    pagina = dados.get("pageToken")
    while True:
        for linha in dados.get("rows", []):
            linhas.append([campo.get("v") for campo in linha["f"]])
        if not pagina:
            break
        parametros = {"pageToken": pagina, "maxResults": 10000}
        if location:
            parametros["location"] = location
        resposta = requests.get(url_resultados, headers=headers,
                                params=parametros, timeout=180)
        if resposta.status_code != 200:
            raise SystemExit(f"BigQuery retornou HTTP {resposta.status_code}: "
                             f"{resposta.text[:800]}")
        dados = resposta.json()
        pagina = dados.get("pageToken")
    return pd.DataFrame(linhas, columns=COLUNAS)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", help="projeto de billing do BigQuery")
    parser.add_argument("--start", type=int, default=2006)
    parser.add_argument("--end", type=int, default=2024)
    parser.add_argument("--out", type=Path, default=PADRAO)
    args = parser.parse_args(argv)
    if args.start > args.end:
        raise SystemExit("--start não pode ser maior que --end")
    args.out = caminho_no_projeto(args.out)

    project = _projeto(args.project)
    token = _token()
    df = _consultar(project, token, _sql(args.start, args.end))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out, index=False)  # NOSONAR: caminho confinado

    conteudo = args.out.read_bytes()  # NOSONAR: caminho confinado
    metadata = {
        "fonte": "Base dos Dados / Transfermarkt",
        "tabela": "basedosdados.mundo_transfermarkt_competicoes.brasileirao_serie_a",
        "consulta": _sql(args.start, args.end),
        "acesso_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "linhas": len(df),
        "sha256": hashlib.sha256(conteudo).hexdigest(),
    }
    (args.out.parent / "FETCH_METADATA.json").write_text(  # NOSONAR
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )  # NOSONAR

    print(f"ok: {len(df)} linhas -> {args.out}")
    print(df.groupby("ano_campeonato").size().to_string())
    print(f"publico não nulo: {df['publico'].notna().sum()}")
    print(f"arbitro não nulo: {df['arbitro'].notna().sum()}")
    print(f"faltas não nulas: {df['faltas_mandante'].notna().sum()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
