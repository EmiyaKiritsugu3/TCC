#!/usr/bin/env python3
"""Baixa a base bruta do commit pinado (plano B — o CSV não é versionado).

Uso:  python3 scripts/fetch_raw.py [--check]
Saída: data/raw/campeonato-brasileiro-full.csv (+ Legenda.txt)
"""
import sys
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

from integrity import verify_sha256

COMMIT = "15f027c3be337bb130d6ae94436b5cdca737377c"
BASE_URL = f"https://raw.githubusercontent.com/adaoduque/Brasileirao_Dataset/{COMMIT}"
ARQUIVOS = ["campeonato-brasileiro-full.csv", "Legenda.txt"]

DEST = RAIZ / "data" / "raw"

SHA256 = {
    "campeonato-brasileiro-full.csv": "c09d03d36debfd7d7aee71da9a9f0909b5e420fc80a1705f215efc93c76e83fc",
    "Legenda.txt": "dfedf5fb55d9d7b178bce0e0e0b639c380d42d27af76a7d3ef1f1d6db6d1de1f",
}


def main() -> None:
    check = "--check" in sys.argv[1:]
    DEST.mkdir(parents=True, exist_ok=True)
    for nome in ARQUIVOS:
        out = DEST / nome
        if check:
            if not out.exists():
                raise SystemExit(f"arquivo ausente: {out}")
            verify_sha256(out, SHA256[nome])
            print(f"  ok {out} ({out.stat().st_size} bytes)")
            continue
        url = f"{BASE_URL}/{nome}"
        tmp = out.with_name(out.name + ".tmp")
        print(f"baixando {url} ...")
        try:
            urllib.request.urlretrieve(url, tmp)
            verify_sha256(tmp, SHA256[nome])
            tmp.replace(out)
        except BaseException:
            tmp.unlink(missing_ok=True)
            raise
        print(f"  -> {out} ({out.stat().st_size} bytes)")
    if check:
        print("OK. Arquivos conferidos.")
    else:
        print("OK. Em seguida: python3 scripts/build_processed.py")


if __name__ == "__main__":
    main()
