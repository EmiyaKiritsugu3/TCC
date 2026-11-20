#!/usr/bin/env python3
"""Baixa os cartões por partida do BrazilianFootball/Data.

Fonte: https://github.com/BrazilianFootball/Data (MIT), extraída dos borderôs
da CBF. O commit é fixado para reprodutibilidade.

Uso:
  python3 scripts/fetch_cards.py            # baixa 2013–2024 e grava metadados
  python3 scripts/fetch_cards.py --check    # confere os arquivos locais
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import requests

from paths import caminho_no_projeto

REPO = "BrazilianFootball/Data"
COMMIT = "0dd1bc5f7da20130df460b9876e0bbbfebcbfa03"
DOI = "10.5281/zenodo.15207727"
ANOS = list(range(2013, 2025))
RAIZ = Path(__file__).resolve().parent.parent
PASTA = RAIZ / "data" / "external" / "cards"
URL = "https://raw.githubusercontent.com/{repo}/{commit}/results/processed/Serie_A_{ano}_games.json"


def _sha256(caminho: Path) -> str:
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


def _baixar(ano: int, destino: Path) -> dict:
    url = URL.format(repo=REPO, commit=COMMIT, ano=ano)
    resposta = requests.get(url, timeout=120)
    if resposta.status_code != 200:
        raise SystemExit(f"{ano}: HTTP {resposta.status_code} em {url}")
    destino.write_bytes(resposta.content)
    dados = json.loads(resposta.content)
    return {
        "ano": ano,
        "arquivo": destino.name,
        "url": url,
        "bytes": destino.stat().st_size,
        "partidas": len(dados),
        "sha256": _sha256(destino),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="apenas confere os arquivos e o metadata")
    args = parser.parse_args(argv)
    pasta = caminho_no_projeto(PASTA)
    metadata_path = pasta / "FETCH_METADATA.json"
    if args.check:
        if not metadata_path.exists():
            raise SystemExit(f"metadata ausente: {metadata_path}")
        meta = json.loads(metadata_path.read_text(encoding="utf-8"))
        falhas = []
        for item in meta["arquivos"]:
            caminho = pasta / item["arquivo"]
            if not caminho.exists():
                falhas.append(f"ausente: {caminho.name}")
            elif _sha256(caminho) != item["sha256"]:
                falhas.append(f"hash divergente: {caminho.name}")
        if falhas:
            raise SystemExit("\n".join(falhas))
        print(f"ok: {len(meta['arquivos'])} arquivos conferidos")
        return 0

    pasta.mkdir(parents=True, exist_ok=True)
    arquivos = []
    for ano in ANOS:
        destino = pasta / f"Serie_A_{ano}_games.json"
        arquivos.append(_baixar(ano, destino))
        print(f"ok: {ano} ({arquivos[-1]['partidas']} partidas)")
    metadata = {
        "fonte": "BrazilianFootball/Data",
        "repositorio": f"https://github.com/{REPO}",
        "commit": COMMIT,
        "doi": DOI,
        "licenca": "MIT",
        "acesso_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "anos": ANOS,
        "arquivos": arquivos,
    }
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")
    print(f"ok: {len(arquivos)} arquivos -> {pasta}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
