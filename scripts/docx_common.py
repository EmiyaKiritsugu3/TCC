"""Funções compartilhadas de layout DOCX para os artigos."""
from __future__ import annotations

import re

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

FONTE = "Times New Roman"


def runs(par, texto: str, tamanho: float = 11, negrito: bool = False,
         italico: bool = False) -> None:
    """Adiciona texto com **negrito**, *itálico* e `código`."""
    for parte in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)", texto):
        if not parte:
            continue
        if parte.startswith("**") and parte.endswith("**"):
            run = par.add_run(parte[2:-2])
            run.bold = True
            run.italic = italico
        elif parte.startswith("`") and parte.endswith("`"):
            run = par.add_run(parte[1:-1])
            run.italic = True
        elif parte.startswith("*") and parte.endswith("*"):
            run = par.add_run(parte[1:-1])
            run.italic = True
        else:
            run = par.add_run(parte)
            run.bold = negrito
            run.italic = italico
        run.font.name = FONTE
        run.font.size = Pt(tamanho)


def paragrafo(doc, texto: str, *, tamanho: float = 11, negrito: bool = False,
              italico: bool = False, central: bool = False,
              espaco: float = 1.12, antes: int = 0, depois: int = 0,
              recuo: bool = False, indent: float = 0.6,
              hanging: bool = False, alinhamento: str = "justify",
              cor: RGBColor | None = None) -> None:
    par = doc.add_paragraph()
    if alinhamento == "left":
        par.alignment = WD_ALIGN_PARAGRAPH.LEFT
    elif central:
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    else:
        par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    fmt = par.paragraph_format
    fmt.line_spacing = espaco
    fmt.space_before = Pt(antes)
    fmt.space_after = Pt(depois)
    if hanging:
        fmt.left_indent = Cm(indent)
        fmt.first_line_indent = Cm(-indent)
    elif recuo and not central:
        fmt.first_line_indent = Cm(indent)
    runs(par, texto, tamanho=tamanho, negrito=negrito, italico=italico)
    if cor is not None:
        for run in par.runs:
            run.font.color.rgb = cor


def tabela(doc, linhas: list[list[str]], larguras: list[float] | None = None,
           fonte: float = 9.0) -> None:
    tab = doc.add_table(rows=len(linhas), cols=len(linhas[0]))
    tab.style = "Table Grid"
    tab.autofit = larguras is None
    # Repete o cabeçalho quando a tabela quebra entre páginas.
    tr_pr = tab.rows[0]._tr.get_or_add_trPr()
    tr_pr.append(OxmlElement("w:tblHeader"))
    for i, linha in enumerate(linhas):
        for j, celula in enumerate(linha):
            cel = tab.cell(i, j)
            cel.text = ""
            runs(cel.paragraphs[0], celula.strip(), tamanho=fonte,
                 negrito=(i == 0))
            cel.paragraphs[0].paragraph_format.line_spacing = 1.0
            cel.paragraphs[0].paragraph_format.space_after = Pt(0)
    if larguras:
        tab.autofit = False
        for j, largura in enumerate(larguras):
            tab.columns[j].width = Cm(largura)
            for celula in tab.columns[j].cells:
                celula.width = Cm(largura)
    doc.add_paragraph()


def configurar(doc: Document, *, top: float = 3.0, left: float = 3.0,
               bottom: float = 2.0, right: float = 2.0,
               tamanho: float = 12) -> None:
    for secao in doc.sections:
        secao.page_width, secao.page_height = Cm(21.0), Cm(29.7)
        secao.top_margin, secao.left_margin = Cm(top), Cm(left)
        secao.bottom_margin, secao.right_margin = Cm(bottom), Cm(right)
    normal = doc.styles["Normal"]
    normal.font.name = FONTE
    normal.font.size = Pt(tamanho)


def _campo_pagina(par, inicio: int) -> None:
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    run = OxmlElement("w:r")
    txt = OxmlElement("w:t")
    txt.text = str(inicio)
    run.append(txt)
    fld.append(run)
    par._p.append(fld)


def pagina(doc: Document, inicio: int = 1, *,
           cabecalho: str | None = None) -> None:
    """Numera as páginas; com `cabecalho`, usa título no topo e número no rodapé."""
    secao = doc.sections[0]
    if cabecalho:
        header = secao.header.paragraphs[0]
        header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        run = header.add_run(cabecalho)
        run.font.name = FONTE
        run.font.size = Pt(8)
        run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
        footer = secao.footer.paragraphs[0]
        footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _campo_pagina(footer, inicio)
    else:
        header = secao.header.paragraphs[0]
        header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        _campo_pagina(header, inicio)
    if inicio != 1:
        pg = OxmlElement("w:pgNumType")
        pg.set(qn("w:start"), str(inicio))
        cols = secao._sectPr.find(qn("w:cols"))
        if cols is not None:
            cols.addprevious(pg)
        else:
            secao._sectPr.append(pg)
