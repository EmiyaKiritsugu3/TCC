#!/usr/bin/env python3
"""Baixa a base bruta do commit pinado (plano B — o CSV não é versionado).

Uso:  python3 scripts/fetch_raw.py
Saída: data/raw/campeonato-brasileiro-full.csv (+ Legenda.txt)
"""
import urllib.request
from pathlib import Path

COMMIT = "15f027c3be337bb130d6ae94436b5cdca737377c"
BASE_URL = f"https://raw.githubusercontent.com/adaoduque/Brasileirao_Dataset/{COMMIT}"
ARQUIVOS = ["campeonato-brasileiro-full.csv", "Legenda.txt"]

RAIZ = Path(__file__).resolve().parent.parent
DEST = RAIZ / "data" / "raw"


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    for nome in ARQUIVOS:
        url = f"{BASE_URL}/{nome}"
        out = DEST / nome
        print(f"baixando {url} ...")
        urllib.request.urlretrieve(url, out)
        print(f"  -> {out} ({out.stat().st_size} bytes)")
    print("OK. Em seguida: python3 scripts/build_processed.py")


if __name__ == "__main__":
    main()
