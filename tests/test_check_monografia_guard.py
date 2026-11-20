"""Guardas da auditoria numérica da monografia (PT-BR)."""
import os
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
PROCESSED = RAIZ / "data" / "processed" / "matches_processed.csv"

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(not PROCESSED.exists(), reason="requer a base processada de build_processed.py"),
]


def _auditar_com_texto(tmp_path, texto):
    # O auditor aceita apenas arquivos dentro do projeto (mitigação S8707).
    diretorio = RAIZ / ".monografia_teste"
    diretorio.mkdir(exist_ok=True)
    alvo = diretorio / f"{tmp_path.name}.md"
    alvo.write_text(texto, encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(RAIZ / "scripts" / "check_monografia.py"),
         "--monografia", str(alvo)],
        cwd=RAIZ, capture_output=True, text=True,
        env=dict(os.environ, PYTHONPATH="src"),
    )


def test_auditor_rejeita_numero_desatualizado(tmp_path):
    texto = (RAIZ / "docs" / "monografia_v2.md").read_text(encoding="utf-8")
    resultado = _auditar_com_texto(tmp_path, texto.replace("96 testes", "99 testes"))
    assert resultado.returncode == 1
    assert "DIVERGÊNCIA" in resultado.stdout


def test_auditor_rejeita_cabecalho_ausente(tmp_path):
    texto = (RAIZ / "docs" / "monografia_v2.md").read_text(encoding="utf-8")
    sem_referencias = texto.replace("# REFERÊNCIAS", "# REFERENCIAS")
    resultado = _auditar_com_texto(tmp_path, sem_referencias)
    assert resultado.returncode == 1
    assert "DIVERGÊNCIA" in resultado.stdout
    assert "Traceback" not in resultado.stderr
