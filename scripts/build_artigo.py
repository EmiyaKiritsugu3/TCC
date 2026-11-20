#!/usr/bin/env python3
"""Gera o artigo 2013–2024 em DOCX e PDF (layout de manuscrito).

Entrada: docs/artigo_2013_2024.md
Saídas: docs/artigo_2013_2024.docx e .pdf
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
ENTRADA = RAIZ / "docs" / "artigo_2013_2024.md"
SAIDA = RAIZ / "docs" / "artigo_2013_2024.docx"
VERDE = RGBColor(0x14, 0x53, 0x2D)
CINZA = RGBColor(0x55, 0x55, 0x55)


def _runs(par, texto: str, tamanho: float = 10.8, negrito: bool = False,
          italico: bool = False) -> None:
    for parte in re.split(r"(\*\*.+?\*\*|\*.+?\*|`.+?`)", texto):
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
        run.font.name = "Times New Roman"
        run.font.size = Pt(tamanho)


def _paragrafo(doc, texto: str, *, tamanho: float = 10.8, negrito: bool = False,
               italico: bool = False, central: bool = False,
               espaco: float = 1.12, antes: int = 0, depois: int = 4,
               recuo: bool = False, hanging: bool = False,
               cor: RGBColor | None = None) -> None:
    par = doc.add_paragraph()
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER if central else WD_ALIGN_PARAGRAPH.JUSTIFY
    fmt = par.paragraph_format
    fmt.line_spacing = espaco
    fmt.space_before = Pt(antes)
    fmt.space_after = Pt(depois)
    if hanging:
        fmt.left_indent = Cm(0.6)
        fmt.first_line_indent = Cm(-0.6)
    elif recuo:
        fmt.first_line_indent = Cm(0.6)
    _runs(par, texto, tamanho=tamanho, negrito=negrito, italico=italico)
    if cor is not None:
        for run in par.runs:
            run.font.color.rgb = cor


def _tabela(doc, linhas: list[list[str]], larguras: list[float] | None = None,
            fonte: float = 8.8) -> None:
    tab = doc.add_table(rows=len(linhas), cols=len(linhas[0]))
    tab.style = "Table Grid"
    tab.autofit = larguras is None
    for i, linha in enumerate(linhas):
        for j, celula in enumerate(linha):
            cel = tab.cell(i, j)
            cel.text = ""
            _runs(cel.paragraphs[0], celula.strip(), tamanho=fonte,
                  negrito=(i == 0))
    if larguras:
        for j, largura in enumerate(larguras):
            for celula in tab.columns[j].cells:
                celula.width = Cm(largura)
    doc.add_paragraph()


def _rodape(doc) -> None:
    secao = doc.sections[0]
    header = secao.header.paragraphs[0]
    header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = header.add_run("Home advantage in Brazilian Série A (2013–2024)")
    run.font.name = "Times New Roman"
    run.font.size = Pt(8)
    run.font.color.rgb = CINZA
    par = secao.footer.paragraphs[0]
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    r = OxmlElement("w:r")
    txt = OxmlElement("w:t")
    txt.text = "1"
    r.append(txt)
    fld.append(r)
    par._p.append(fld)


def _configurar(doc) -> None:
    for secao in doc.sections:
        secao.page_width, secao.page_height = Cm(21.0), Cm(29.7)
        secao.top_margin, secao.bottom_margin = Cm(2.3), Cm(2.0)
        secao.left_margin, secao.right_margin = Cm(2.5), Cm(2.5)
    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(10.8)


def _renderizar(doc, linhas: list[str]) -> None:
    i = 0
    refs = False
    abstract = False
    while i < len(linhas):
        s = linhas[i].strip()
        if not s or s == "---":
            i += 1
            continue
        if s.startswith("# "):
            _paragrafo(doc, s[2:], tamanho=17, negrito=True, central=True,
                       espaco=1.05, depois=8, cor=VERDE)
            i += 1
            continue
        if s.startswith("José Inamar"):
            _paragrafo(doc, s, tamanho=11.5, central=True, depois=2)
            i += 1
            continue
        if s.startswith("Universidade Federal"):
            _paragrafo(doc, s, tamanho=9.8, italico=True, central=True,
                       depois=10, cor=CINZA)
            i += 1
            continue
        if s.startswith("### "):
            _paragrafo(doc, s[4:], tamanho=11.3, negrito=True, italico=True,
                       antes=8, depois=2, cor=VERDE)
            i += 1
            continue
        if s.startswith("## "):
            titulo = s[3:]
            refs = titulo.lower() == "references"
            abstract = titulo.lower() == "abstract"
            _paragrafo(doc, titulo, tamanho=12.5, negrito=True, antes=12,
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
                ncols = len(linhas_tab[0])
                cabecalho = " ".join(linhas_tab[0])
                if "Home / draw / away" in cabecalho:
                    _tabela(doc, linhas_tab, fonte=8.0,
                            larguras=[1.6, 1.7, 4.2, 2.8, 5.7])
                elif ncols == 5:
                    _tabela(doc, linhas_tab, fonte=8.2,
                            larguras=[4.5, 2.2, 1.6, 3.0, 3.0])
                else:
                    _tabela(doc, linhas_tab)
            continue
        imagem = re.fullmatch(r"!\[(.*?)\]\((.+?)\)", s)
        if imagem:
            legenda, caminho = imagem.groups()
            arquivo = RAIZ / caminho
            if not arquivo.exists():
                raise FileNotFoundError(f"figura ausente: {arquivo}")
            doc.add_picture(str(arquivo), width=Cm(13.5))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            _paragrafo(doc, legenda, tamanho=8.5, italico=True,
                       central=True, antes=2, depois=8, cor=CINZA)
            i += 1
            continue
        if s.startswith("**Table 1."):
            _paragrafo(doc, s, tamanho=9.5, central=True, antes=4, depois=2)
            i += 1
            continue
        if s.startswith("**Table ") or s.startswith("**Figure "):
            _paragrafo(doc, s, tamanho=9.5, central=True, antes=4, depois=2)
            i += 1
            continue
        if s.startswith("Notes:"):
            _paragrafo(doc, s, tamanho=8.3, italico=True, depois=8, cor=CINZA)
            i += 1
            continue
        if s.startswith("**Keywords:**") or s.startswith("**JEL codes:**"):
            _paragrafo(doc, s, tamanho=9.8, depois=3)
            abstract = False
            i += 1
            continue
        _paragrafo(doc, s, recuo=(not refs and not abstract), hanging=refs,
                   tamanho=9.2 if refs else (10.2 if abstract else 10.8),
                   depois=3 if refs else 4)
        i += 1


def main() -> None:
    linhas = ENTRADA.read_text(encoding="utf-8").splitlines()
    doc = Document()
    _configurar(doc)
    doc.core_properties.title = "Home advantage in Brazilian Série A (2013–2024)"
    doc.core_properties.author = "José Inamar de Medeiros Júnior"
    _renderizar(doc, linhas)
    _rodape(doc)
    doc.save(SAIDA)
    print(f"gravado em: {SAIDA}")
    subprocess.run(
        ["libreoffice", "--headless", "--convert-to", "pdf",
         "--outdir", str(SAIDA.parent), str(SAIDA)],
        check=True,
    )


if __name__ == "__main__":
    main()
