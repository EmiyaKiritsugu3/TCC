#!/usr/bin/env python3
"""Gera o artigo 2013–2024 em formato ABNT (DOCX e PDF).

Entrada: docs/artigo_2013_2024_abnt.md
Saídas: docs/artigo_2013_2024_abnt.docx e .pdf

Formato: A4, margens 3 cm (superior/esquerda) e 2 cm (inferior/direita),
Times New Roman 12, espaçamento 1,5, recuo de primeira linha 1,25 cm,
títulos de seção primária em caixa alta, referências em NBR 6023.
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
ENTRADA = RAIZ / "docs" / "artigo_2013_2024_abnt.md"
SAIDA = RAIZ / "docs" / "artigo_2013_2024_abnt.docx"
PRETO = RGBColor(0, 0, 0)
CINZA = RGBColor(0x44, 0x44, 0x44)


def _runs(par, texto: str, tamanho: float = 12, negrito: bool = False,
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
        run.font.color.rgb = PRETO


def _paragrafo(doc, texto: str, *, tamanho: float = 12, negrito: bool = False,
               italico: bool = False, central: bool = False,
               espaco: float = 1.5, antes: int = 0, depois: int = 0,
               recuo: bool = True, hanging: bool = False,
               alinhamento: str = "justify") -> None:
    par = doc.add_paragraph()
    if central:
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif alinhamento == "left":
        par.alignment = WD_ALIGN_PARAGRAPH.LEFT
    else:
        par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    fmt = par.paragraph_format
    fmt.line_spacing = espaco
    fmt.space_before = Pt(antes)
    fmt.space_after = Pt(depois)
    if hanging:
        fmt.left_indent = Cm(0.0)
        fmt.first_line_indent = Cm(0.0)
    elif recuo:
        fmt.first_line_indent = Cm(1.25)
    _runs(par, texto, tamanho=tamanho, negrito=negrito, italico=italico)


def _tabela(doc, linhas: list[list[str]], larguras: list[float],
            fonte: float = 9.0) -> None:
    tab = doc.add_table(rows=len(linhas), cols=len(linhas[0]))
    tab.style = "Table Grid"
    tab.autofit = False
    for i, linha in enumerate(linhas):
        for j, celula in enumerate(linha):
            cel = tab.cell(i, j)
            cel.text = ""
            _runs(cel.paragraphs[0], celula.strip(), tamanho=fonte,
                  negrito=(i == 0))
            cel.paragraphs[0].paragraph_format.line_spacing = 1.0
            cel.paragraphs[0].paragraph_format.space_after = Pt(0)
    for j, largura in enumerate(larguras):
        for celula in tab.columns[j].cells:
            celula.width = Cm(largura)
    doc.add_paragraph()


def _pagina(doc) -> None:
    header = doc.sections[0].header.paragraphs[0]
    header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    run = OxmlElement("w:r")
    txt = OxmlElement("w:t")
    txt.text = "1"
    run.append(txt)
    fld.append(run)
    header._p.append(fld)


def _configurar(doc) -> None:
    for secao in doc.sections:
        secao.page_width, secao.page_height = Cm(21.0), Cm(29.7)
        secao.top_margin, secao.left_margin = Cm(3.0), Cm(3.0)
        secao.bottom_margin, secao.right_margin = Cm(2.0), Cm(2.0)
    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(12)


def _titulo_secao(titulo: str) -> tuple[str, bool]:
    """Devolve (texto, é_primária) no padrão ABNT."""
    m = re.match(r"^(\d+)\.\s+(.+)$", titulo)
    if m:
        return f"{m.group(1)} {m.group(2).upper()}", True
    m = re.match(r"^(\d+\.\d+)\s+(.+)$", titulo)
    if m:
        return f"{m.group(1)} {m.group(2)}", False
    return titulo.upper(), True


def _renderizar(doc, linhas: list[str]) -> None:
    i = 0
    refs = False
    resumo = False
    while i < len(linhas):
        s = linhas[i].strip()
        if not s or s == "---":
            i += 1
            continue
        if s.startswith("# "):
            _paragrafo(doc, s[2:], tamanho=14, negrito=True, central=True,
                       espaco=1.2, depois=6, recuo=False)
            i += 1
            continue
        if s.startswith("José Inamar"):
            _paragrafo(doc, s, tamanho=12, central=True, depois=1, recuo=False)
            i += 1
            continue
        if s.startswith("Universidade Federal"):
            _paragrafo(doc, s, tamanho=10, central=True, depois=12, recuo=False)
            i += 1
            continue
        if s.startswith("### "):
            _paragrafo(doc, s[4:], tamanho=12, negrito=True, antes=8,
                       depois=3, recuo=False)
            i += 1
            continue
        if s.startswith("## "):
            titulo = s[3:]
            refs = titulo.lower() == "referências"
            resumo = titulo.lower() in ("resumo", "abstract")
            texto, primaria = _titulo_secao(titulo)
            _paragrafo(doc, texto, tamanho=12, negrito=True,
                       antes=12 if primaria else 8, depois=6, recuo=False)
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
                cabecalho = " ".join(linhas_tab[0])
                if "Vitória / empate / derrota" in cabecalho:
                    _tabela(doc, linhas_tab, [1.7, 1.7, 4.1, 2.7, 5.8], 8.5)
                elif "Coeficiente" in cabecalho:
                    _tabela(doc, linhas_tab, [4.6, 2.2, 1.6, 3.0, 3.0], 9.0)
                else:
                    _tabela(doc, linhas_tab, [3.2] * len(linhas_tab[0]), 9.0)
            continue
        imagem = re.fullmatch(r"!\[(.*?)\]\((.+?)\)", s)
        if imagem:
            legenda, caminho = imagem.groups()
            arquivo = RAIZ / caminho
            if not arquivo.exists():
                raise FileNotFoundError(f"figura ausente: {arquivo}")
            _paragrafo(doc, legenda, tamanho=9.5, central=True,
                       antes=8, depois=3, recuo=False)
            doc.paragraphs[-1].paragraph_format.keep_with_next = True
            doc.add_picture(str(arquivo), width=Cm(14.0))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.paragraphs[-1].paragraph_format.keep_with_next = True
            i += 1
            continue
        if s.startswith("**Tabela "):
            _paragrafo(doc, s, tamanho=10, negrito=False, central=True,
                       antes=8, depois=3, recuo=False)
            doc.paragraphs[-1].paragraph_format.keep_with_next = True
            i += 1
            continue
        if s.startswith("Fonte:") or s.startswith("Nota:"):
            _paragrafo(doc, s, tamanho=9, central=True, espaco=1.0,
                       depois=6, recuo=False, alinhamento="left")
            i += 1
            continue
        if s.startswith("**Palavras-chave:**") or s.startswith("**Keywords:**") \
                or s.startswith("**Códigos JEL:**"):
            _paragrafo(doc, s, tamanho=10, espaco=1.0, depois=3, recuo=False)
            resumo = False
            i += 1
            continue
        if refs:
            _paragrafo(doc, s, tamanho=10.0, espaco=1.0, depois=4,
                       recuo=False, alinhamento="left")
        elif resumo:
            _paragrafo(doc, s, tamanho=10, espaco=1.0, depois=3, recuo=False)
        else:
            _paragrafo(doc, s, tamanho=12, espaco=1.5, depois=0, recuo=True)
        i += 1


def main() -> None:
    linhas = ENTRADA.read_text(encoding="utf-8").splitlines()
    doc = Document()
    _configurar(doc)
    doc.core_properties.title = "Vantagem de jogar em casa na Série A (2013–2024)"
    doc.core_properties.author = "José Inamar de Medeiros Júnior"
    _renderizar(doc, linhas)
    _pagina(doc)
    doc.save(SAIDA)
    print(f"gravado em: {SAIDA}")
    subprocess.run(
        ["libreoffice", "--headless", "--convert-to", "pdf",
         "--outdir", str(SAIDA.parent), str(SAIDA)],
        check=True,
    )


if __name__ == "__main__":
    main()
