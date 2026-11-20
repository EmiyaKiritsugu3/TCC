#!/usr/bin/env python3
"""Gera o resumo de artigo para o orientador em DOCX e PDF.

Entrada: docs/resumo_artigo_orientador.md
Saídas: docs/resumo_artigo_orientador.docx e .pdf

O PDF depende do LibreOffice:
  libreoffice --headless --convert-to pdf --outdir docs \
      docs/resumo_artigo_orientador.docx
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "docs" / "resumo_artigo_orientador.md"
SAIDA = RAIZ / "docs" / "resumo_artigo_orientador.docx"
VERDE = RGBColor(0x14, 0x53, 0x2D)
CINZA = RGBColor(0x55, 0x55, 0x55)


def _runs(par, texto: str, tamanho: float = 10.5, negrito: bool = False) -> None:
    """Adiciona texto com **negrito** preservando o restante."""
    for parte in re.split(r"(\*\*.+?\*\*)", texto):
        if not parte:
            continue
        if parte.startswith("**") and parte.endswith("**"):
            run = par.add_run(parte[2:-2])
            run.bold = True
        else:
            run = par.add_run(parte)
            run.bold = negrito
        run.font.name = "Times New Roman"
        run.font.size = Pt(tamanho)


def _paragrafo(doc, texto: str, *, tamanho: float = 10.5, negrito: bool = False,
               espaco: float = 1.08, antes: int = 0, depois: int = 5,
               recuo: bool = False, cor: RGBColor | None = None) -> None:
    par = doc.add_paragraph()
    par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    par.paragraph_format.line_spacing = espaco
    par.paragraph_format.space_before = Pt(antes)
    par.paragraph_format.space_after = Pt(depois)
    if recuo:
        par.paragraph_format.left_indent = Cm(0.6)
        par.paragraph_format.first_line_indent = Cm(-0.4)
    _runs(par, texto, tamanho=tamanho, negrito=negrito)
    if cor is not None:
        for run in par.runs:
            run.font.color.rgb = cor


def _tabela(doc, linhas: list[list[str]]) -> None:
    tab = doc.add_table(rows=len(linhas), cols=len(linhas[0]))
    tab.style = "Table Grid"
    tab.autofit = True
    for i, linha in enumerate(linhas):
        for j, celula in enumerate(linha):
            cel = tab.cell(i, j)
            cel.text = ""
            _runs(cel.paragraphs[0], celula.strip(), tamanho=8.5,
                  negrito=(i == 0))
    doc.add_paragraph()


def _rodape(doc) -> None:
    par = doc.sections[0].footer.paragraphs[0]
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    run = OxmlElement("w:r")
    txt = OxmlElement("w:t")
    txt.text = "1"
    run.append(txt)
    fld.append(run)
    par._p.append(fld)


def _configurar(doc) -> None:
    for secao in doc.sections:
        secao.page_width, secao.page_height = Cm(21.0), Cm(29.7)
        secao.top_margin, secao.bottom_margin = Cm(2.2), Cm(2.0)
        secao.left_margin, secao.right_margin = Cm(2.5), Cm(2.5)
    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(11)


def _renderizar(doc, linhas: list[str]) -> None:
    i = 0
    while i < len(linhas):
        s = linhas[i].strip()
        if not s or s == "---":
            i += 1
            continue
        if s.startswith("# "):
            par = doc.add_paragraph()
            par.alignment = WD_ALIGN_PARAGRAPH.CENTER
            par.paragraph_format.space_after = Pt(2)
            _runs(par, s[2:], tamanho=16, negrito=True)
            for run in par.runs:
                run.font.color.rgb = VERDE
            i += 1
            continue
        if s.startswith("## "):
            _paragrafo(doc, s[3:], tamanho=12, negrito=True, antes=8,
                       depois=3, cor=VERDE)
            i += 1
            continue
        if s.startswith("|"):
            bloco = []
            while i < len(linhas) and linhas[i].strip().startswith("|"):
                bloco.append(linhas[i].strip())
                i += 1
            linhas_tab = []
            for linha in bloco:
                partes = [p.strip() for p in linha.strip("|").split("|")]
                if all(set(p) <= set("-: ") for p in partes):
                    continue
                linhas_tab.append(partes)
            if linhas_tab:
                _tabela(doc, linhas_tab)
            continue
        if re.match(r"^(\d+\.|-)\s", s):
            if s.startswith("- "):
                texto = "•  " + s[2:].strip()
            else:
                texto = s
            _paragrafo(doc, texto, recuo=True, depois=3)
            i += 1
            continue
        _paragrafo(doc, s)
        i += 1


def main() -> None:
    linhas = ENTRADA.read_text(encoding="utf-8").splitlines()
    doc = Document()
    _configurar(doc)
    doc.core_properties.title = "Resumo para o orientador — proposta de artigo"
    doc.core_properties.author = "José Inamar de Medeiros Júnior"
    _renderizar(doc, linhas)
    _rodape(doc)
    doc.save(SAIDA)
    print(f"gravado em: {SAIDA}")
    subprocess.run(
        ["libreoffice", "--headless", "--convert-to", "pdf",
         "--outdir", str(SAIDA.parent), str(SAIDA)],
        check=False,
    )


if __name__ == "__main__":
    main()
