"""Confinamento de caminhos para os scripts locais do TCC.

Os scripts de ingestão aceitam caminhos de entrada e saída pela linha de
comando. Como são ferramentas locais, o caminho é confinado ao repositório:
um argumento errado não deve gravar fora do projeto.
"""
from __future__ import annotations

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def caminho_no_projeto(caminho: Path) -> Path:
    """Resolve `caminho` e falha se ele sair do repositório do TCC."""
    resolvido = Path(caminho).expanduser().resolve()
    raiz = RAIZ.resolve()
    if resolvido != raiz and raiz not in resolvido.parents:
        raise SystemExit(f"caminho fora do projeto: {caminho}")
    return resolvido
