"""Guardas da auditoria numérica da monografia (PT-BR)."""
import os
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def _auditar_com_texto(tmp_path, texto):
    alvo = tmp_path / "monografia.md"
    alvo.write_text(texto, encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(RAIZ / "scripts" / "check_monografia.py"),
         "--monografia", str(alvo)],
        cwd=RAIZ, capture_output=True, text=True,
        env=dict(os.environ, PYTHONPATH="src"),
    )


def test_auditor_rejeita_numero_desatualizado(tmp_path):
    texto = (RAIZ / "docs" / "monografia_v2.md").read_text(encoding="utf-8")
    resultado = _auditar_com_texto(tmp_path, texto.replace("31 testes", "99 testes"))
    assert resultado.returncode == 1
    assert "DIVERGÊNCIA" in resultado.stdout
