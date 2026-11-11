#!/usr/bin/env python3
"""Prepara o ambiente do projeto na primeira execução (ou apenas o verifica).

Uso:
  python3 scripts/bootstrap.py            # modo completo
  python3 scripts/bootstrap.py --check    # somente verificação (não altera nada)

Modo completo, nesta ordem:
  1. pip install -r requirements-lock.txt
  2. scripts/fetch_raw.py   (baixa a base bruta e confere o SHA-256)
  3. scripts/build_processed.py
  4. pytest tests/

Modo --check apenas informa o estado do ambiente: interpretador Python,
versões fixadas em requirements-lock.txt, integridade da base bruta,
presença da base processada e coleta dos testes.

A lógica de download e limpeza NÃO é reimplementada aqui: fetch_raw.py e
build_processed.py são executados como subprocessos.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SRC = RAIZ / "src"
LOCK = RAIZ / "requirements-lock.txt"
RAW_CSV = RAIZ / "data" / "raw" / "campeonato-brasileiro-full.csv"
PROCESSED = RAIZ / "data" / "processed" / "matches_processed.csv"
PYTHON_MINIMO = (3, 11)

CODIGO_VERSOES = """
import json, sys
import importlib.metadata as md
saida = {}
for nome in sys.argv[1:]:
    try:
        saida[nome] = md.version(nome)
    except md.PackageNotFoundError:
        saida[nome] = None
print(json.dumps(saida))
"""


# ---------------------------------------------------------------- utilidades


def ok(mensagem: str) -> None:
    print(f"  [ok] {mensagem}")


def aviso(mensagem: str) -> None:
    print(f"  [aviso] {mensagem}")


def falha(mensagem: str) -> None:
    print(f"  [falha] {mensagem}")


def ambiente() -> dict[str, str]:
    """Ambiente com src/ no PYTHONPATH (os scripts usam imports de topo)."""
    env = dict(os.environ)
    partes = [str(SRC)]
    if env.get("PYTHONPATH"):
        partes.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(partes)
    return env


def interpretador() -> Path:
    """Usa o virtualenv do projeto quando existe; senão, o interpretador atual."""
    if os.name == "nt":
        candidato = RAIZ / ".venv" / "Scripts" / "python.exe"
    else:
        candidato = RAIZ / ".venv" / "bin" / "python"
    return candidato if candidato.exists() else Path(sys.executable)


def rodar(comando: list[str], env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        comando,
        cwd=str(RAIZ),
        env=env,
        capture_output=True,
        text=True,
    )


def mostrar(proc: subprocess.CompletedProcess[str], linhas: int = 25) -> None:
    texto = (proc.stdout or "") + (proc.stderr or "")
    for linha in texto.strip().splitlines()[-linhas:]:
        print(f"       {linha}")


# ------------------------------------------------------------- verificações


def checar_python(py: Path) -> bool:
    proc = rodar([str(py), "-c", "import sys; print('%d.%d.%d' % sys.version_info[:3])"], ambiente())
    if proc.returncode != 0:
        falha(f"não foi possível executar o interpretador {py}")
        return False
    versao = proc.stdout.strip()
    partes = tuple(int(n) for n in versao.split(".")[:3])
    if partes < PYTHON_MINIMO:
        falha(f"Python {versao} abaixo do mínimo {PYTHON_MINIMO[0]}.{PYTHON_MINIMO[1]}")
        return False
    ok(f"Python {versao} ({py})")
    return True


def pins_do_lock() -> list[tuple[str, str]]:
    if not LOCK.exists():
        return []
    itens = []
    for linha in LOCK.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#"):
            continue
        nome, _, versao = linha.partition("==")
        itens.append((nome.strip(), versao.strip()))
    return itens


def checar_lock(py: Path) -> bool:
    if not LOCK.exists():
        falha("requirements-lock.txt não encontrado")
        return False
    pins = pins_do_lock()
    if not pins:
        falha("requirements-lock.txt sem requisitos")
        return False

    proc = rodar([str(py), "-c", CODIGO_VERSOES, *[nome for nome, _ in pins]], ambiente())
    if proc.returncode != 0:
        falha("não foi possível consultar as versões instaladas")
        mostrar(proc)
        return False
    instaladas = json.loads(proc.stdout.strip() or "{}")

    estado = True
    for nome, pin in pins:
        atual = instaladas.get(nome)
        if atual is None:
            falha(f"{nome}: não instalado (pin {pin})")
            estado = False
        elif atual == pin:
            ok(f"{nome} {atual} (pin {pin})")
        else:
            aviso(f"{nome} {atual} diverge do pin {pin}; rode `python3 scripts/bootstrap.py` para realinhar")
    return estado


def checar_raw(py: Path, env: dict[str, str]) -> bool:
    proc = rodar([str(py), str(RAIZ / "scripts" / "fetch_raw.py"), "--check"], env)
    if proc.returncode != 0:
        falha("base bruta ausente ou com SHA-256 divergente")
        mostrar(proc)
        return False
    ok("base bruta presente e SHA-256 conferido (scripts/fetch_raw.py --check)")
    for linha in proc.stdout.strip().splitlines():
        print(f"       {linha}")
    return True


def checar_processed() -> bool:
    if not PROCESSED.exists():
        falha(f"base processada ausente: {PROCESSED}")
        return False
    tamanho = PROCESSED.stat().st_size
    if tamanho == 0:
        falha(f"base processada vazia: {PROCESSED}")
        return False
    ok(f"base processada presente: {PROCESSED.relative_to(RAIZ)} ({tamanho} bytes)")
    return True


def checar_coleta(py: Path, env: dict[str, str]) -> bool:
    proc = rodar([str(py), "-m", "pytest", "--collect-only", "-q"], env)
    if proc.returncode != 0:
        falha("pytest não conseguiu coletar os testes")
        mostrar(proc)
        return False
    caso = re.search(r"(\d+) tests? collected", proc.stdout)
    coletados = int(caso.group(1)) if caso else 0
    if coletados == 0:
        falha("pytest coletou 0 testes")
        mostrar(proc)
        return False
    ok(f"pytest coletou {coletados} testes")
    return True


# ------------------------------------------------------------------ modos


def verificar(py: Path, env: dict[str, str]) -> int:
    print("[verificação] python3 scripts/bootstrap.py --check")
    resultados = [
        ("Python >= 3.11", checar_python(py)),
        ("requirements-lock.txt instalado", checar_lock(py)),
        ("base bruta íntegra (SHA-256)", checar_raw(py, env)),
        ("base processada presente", checar_processed()),
        ("coleta do pytest", checar_coleta(py, env)),
    ]
    print()
    falhas = [nome for nome, passou in resultados if not passou]
    if falhas:
        print(f"FALHOU: {len(falhas)} de {len(resultados)} verificações ({', '.join(falhas)})")
        return 1
    print(f"OK: {len(resultados)} verificações passaram.")
    return 0


def instalar_lock(py: Path, env: dict[str, str]) -> bool:
    proc = rodar([str(py), "-m", "pip", "install", "-r", str(LOCK)], env)
    if proc.returncode != 0:
        falha("pip install -r requirements-lock.txt falhou")
        mostrar(proc, linhas=40)
        return False
    ok("dependências instaladas conforme requirements-lock.txt")
    return True


def garantir_raw(py: Path, env: dict[str, str]) -> bool:
    proc = rodar([str(py), str(RAIZ / "scripts" / "fetch_raw.py"), "--check"], env)
    if proc.returncode == 0:
        ok("base bruta já presente e íntegra")
        return True

    print("  baixando a base bruta...")
    proc = rodar([str(py), str(RAIZ / "scripts" / "fetch_raw.py")], env)
    if proc.returncode != 0:
        falha("scripts/fetch_raw.py falhou")
        mostrar(proc, linhas=40)
        return False
    proc = rodar([str(py), str(RAIZ / "scripts" / "fetch_raw.py"), "--check"], env)
    if proc.returncode != 0:
        falha("SHA-256 da base bruta não confere após o download")
        mostrar(proc)
        return False
    ok("base bruta baixada e SHA-256 conferido")
    return True


def construir_processed(py: Path, env: dict[str, str]) -> bool:
    proc = rodar([str(py), str(RAIZ / "scripts" / "build_processed.py")], env)
    if proc.returncode != 0:
        falha("scripts/build_processed.py falhou")
        mostrar(proc, linhas=40)
        return False
    for linha in proc.stdout.strip().splitlines():
        print(f"       {linha}")
    ok("base processada gerada")
    return True


def rodar_testes(py: Path, env: dict[str, str]) -> bool:
    proc = rodar([str(py), "-m", "pytest", "tests/", "-q"], env)
    if proc.returncode != 0:
        falha("pytest falhou")
        mostrar(proc, linhas=40)
        return False
    for linha in proc.stdout.strip().splitlines()[-5:]:
        print(f"       {linha}")
    ok("pytest passou")
    return True


def preparar(py: Path, env: dict[str, str]) -> int:
    print("[bootstrap] python3 scripts/bootstrap.py")
    etapas = [
        ("instalar dependências", lambda: instalar_lock(py, env)),
        ("obter base bruta", lambda: garantir_raw(py, env)),
        ("gerar base processada", lambda: construir_processed(py, env)),
        ("rodar testes", lambda: rodar_testes(py, env)),
    ]
    for nome, etapa in etapas:
        print(f"\n[{nome}]")
        if not etapa():
            print()
            print(f"FALHOU em: {nome}")
            return 1
    print()
    print("OK: ambiente pronto. Rode `python3 -m streamlit run app.py`.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepara ou verifica o ambiente do projeto.")
    parser.add_argument("--check", action="store_true", help="apenas verifica o estado atual")
    args = parser.parse_args()

    py = interpretador()
    env = ambiente()
    if args.check:
        return verificar(py, env)
    return preparar(py, env)


if __name__ == "__main__":
    raise SystemExit(main())
