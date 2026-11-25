#!/usr/bin/env python3
"""Gera o guia de estudo da banca em DOCX e PDF.

Entrada: docs/guia_estudo_banca.md
Saídas: docs/guia_estudo_banca.docx e .pdf
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

from docx import Document
from docx.shared import Cm, Pt

from docx_common import configurar, pagina, paragrafo, runs, tabela

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "docs" / "guia_estudo_banca.md"
SAIDA = RAIZ / "docs" / "guia_estudo_banca.docx"
VERDE = (0x0B, 0x3D, 0x2E)
CINZA = (0x5F, 0x65, 0x5E)


def _cor(rgb: tuple[int, int, int]):
    from docx.shared import RGBColor
    return RGBColor(*rgb)


def _heading(doc, texto: str, nivel: int) -> None:
    tamanhos = {1: 18, 2: 13.5, 3: 11.5}
    paragrafo(doc, texto, tamanho=tamanhos[nivel], negrito=True,
              cor=_cor(VERDE), antes=10 if nivel > 1 else 0, depois=4,
              recuo=False, alinhamento="left")


def _codigo(doc, linhas: list[str]) -> None:
    for linha in linhas:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.4)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        run = p.add_run(linha)
        run.font.name = "Consolas"
        run.font.size = Pt(8.5)
    doc.add_paragraph()


def _tabela_md(doc, bloco: list[str]) -> None:
    linhas = []
    for linha in bloco:
        partes = [p.strip() for p in linha.strip("|").split("|")]
        if all(set(p) <= set("-: ") for p in partes):
            continue
        linhas.append(partes)
    if linhas:
        tabela(doc, linhas, fonte=8.0)


def _paragrafo_md(doc, texto: str) -> None:
    if texto.startswith("- [ ] "):
        texto = "☐  " + texto[6:]
    elif texto.startswith("- "):
        texto = "•  " + texto[2:]
    paragrafo(doc, texto, tamanho=10.5, espaco=1.12, depois=4,
              recuo=False, alinhamento="justify")


def _quote(doc, texto: str) -> None:
    paragrafo(doc, texto, tamanho=10, italico=True, cor=_cor(CINZA),
              espaco=1.08, depois=4, recuo=False, alinhamento="justify")


def main() -> None:
    linhas = ENTRADA.read_text(encoding="utf-8").splitlines()
    doc = Document()
    configurar(doc, top=2.2, left=2.2, bottom=2.0, right=2.2, tamanho=10.5)
    doc.core_properties.title = "Guia de estudo para a banca — Artigo 2013–2024"
    doc.core_properties.author = "José Inamar de Medeiros Júnior"

    i = 0
    while i < len(linhas):
        s = linhas[i].strip()
        if not s or s == "---":
            i += 1
            continue
        if s.startswith("```"):
            i += 1
            bloco = []
            while i < len(linhas) and not linhas[i].strip().startswith("```"):
                bloco.append(linhas[i])
                i += 1
            i += 1
            _codigo(doc, bloco)
            continue
        if s.startswith("|"):
            bloco = []
            while i < len(linhas) and linhas[i].strip().startswith("|"):
                bloco.append(linhas[i].strip())
                i += 1
            _tabela_md(doc, bloco)
            continue
        if s.startswith("### "):
            _heading(doc, s[4:], 3)
            i += 1
            continue
        if s.startswith("## "):
            _heading(doc, s[3:], 2)
            i += 1
            continue
        if s.startswith("# "):
            _heading(doc, s[2:], 1)
            i += 1
            continue
        if s.startswith("> "):
            _quote(doc, s[2:])
            i += 1
            continue
        if s.startswith("- [ ] ") or s.startswith("- ") or re.match(r"^\d+\.\s", s):
            _paragrafo_md(doc, s)
            i += 1
            continue
        # parágrafo comum: junta linhas até um elemento especial
        bloco = [s]
        i += 1
        while i < len(linhas):
            t = linhas[i].strip()
            if not t or t.startswith(("#", "|", "```", "> ", "- ", "- [ ] ",
                                      "**Artigo:**", "**Aluno:**",
                                      "**Orientador:**")) \
                    or re.match(r"^\d+\.\s", t):
                break
            bloco.append(t)
            i += 1
        _paragrafo_md(doc, " ".join(bloco))

    pagina(doc)
    doc.save(SAIDA)
    print(f"gravado em: {SAIDA}")
    subprocess.run(
        ["libreoffice", "--headless", "--convert-to", "pdf",
         "--outdir", str(SAIDA.parent), str(SAIDA)],
        check=True,
    )


if __name__ == "__main__":
    main()
