#!/usr/bin/env python3
"""Gera o rascunho DOCX da monografia com estilos próximos à ABNT.

Uso: .venv/bin/python scripts/build_docx.py
Saída: docs/monografia_draft_abnt.docx

Formato aplicado (NBR 14724:2024 + Resolução 001/2016-CSI):
- A4, margens 3 cm (sup/esq) e 2 cm (inf/dir);
- Times New Roman 12, 1,5 de espaçamento, justificado, recuo de 1ª linha 1,25 cm;
- Resumo/Abstract em espaço simples; tabelas/legendas/fonte em 10 (Tabela 1 em 8);
- Capítulos (`# ...`) começam em página nova.

Limitações conhecidas do rascunho (não do conteúdo):
- Sumário estático, sem numeração de páginas (paginação vem no passe final);
- Bloco inicial de notas de trabalho (`> **Documento consolidado...**) omitido;
- Ficha catalográfica entra como placeholder (só o SISBI emite);
- Sem capa institucional gráfica — texto centralizado.
"""
from pathlib import Path

import re

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "docs" / "monografia_v2.md"
SAIDA = RAIZ / "docs" / "monografia_draft_abnt.docx"

PRE_CENTRALIZAR = ("CAPA", "FOLHA DE ROSTO", "FOLHA DE AVALIAÇÃO",
                   "LISTA DE FIGURAS", "LISTA DE TABELAS", "LISTA DE SIGLAS")


def add_runs(par, texto, tamanho=12, negrito_base=False):
    """Adiciona runs com **negrito** e `código`."""
    import re
    for i, parte in enumerate(re.split(r"(\*\*.+?\*\*|`.+?`)", texto)):
        if not parte:
            continue
        if parte.startswith("**") and parte.endswith("**"):
            r = par.add_run(parte[2:-2])
            r.bold = True
        elif parte.startswith("`") and parte.endswith("`"):
            r = par.add_run(parte[1:-1])
            r.font.name = "Consolas"
            r.font.size = Pt(10)
        else:
            r = par.add_run(parte)
            r.bold = negrito_base
        r.font.name = "Times New Roman" if r.font.name != "Consolas" else "Consolas"
        r.font.size = Pt(tamanho)


def corpo(doc, texto, simples=False, central=False, negrito=False, tamanho=12,
          recuo=True, antes=0, depois=6):
    par = doc.add_paragraph()
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER if central else WD_ALIGN_PARAGRAPH.JUSTIFY
    fmt = par.paragraph_format
    fmt.line_spacing = 1.0 if simples else 1.5
    fmt.space_before = Pt(antes)
    fmt.space_after = Pt(depois)
    if recuo and not central:
        fmt.first_line_indent = Cm(1.25)
    add_runs(par, texto.replace("&nbsp;", " "), tamanho=tamanho, negrito_base=negrito)
    return par


def tabela(doc, linhas, fonte=10):
    cab, dados = linhas[0], linhas[1:]
    tab = doc.add_table(rows=1 + len(dados), cols=len(cab))
    tab.style = "Table Grid"
    tab.autofit = True
    for j, celula in enumerate(cab):
        cel = tab.cell(0, j)
        cel.text = ""
        add_runs(cel.paragraphs[0], celula.strip(), tamanho=fonte, negrito_base=True)
    for i, linha in enumerate(dados, start=1):
        for j, celula in enumerate(linha):
            cel = tab.cell(i, j)
            cel.text = ""
            if j < len(cab):
                add_runs(cel.paragraphs[0], celula.strip(), tamanho=fonte)
    doc.add_paragraph()


def rodape_numerado(doc):
    """Rodapé centralizado com campo PAGE (avaliado no Word/LibreOffice)."""
    par = doc.sections[0].footer.paragraphs[0]
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    run = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    nome = OxmlElement("w:rFonts")
    nome.set(qn("w:ascii"), "Times New Roman")
    nome.set(qn("w:hAnsi"), "Times New Roman")
    rpr.append(nome)
    tam = OxmlElement("w:sz")
    tam.set(qn("w:val"), "20")
    rpr.append(tam)
    run.append(rpr)
    txt = OxmlElement("w:t")
    txt.text = "1"
    run.append(txt)
    fld.append(run)
    par._p.append(fld)


def main() -> None:
    linhas = ENTRADA.read_text(encoding="utf-8").splitlines()
    doc = Document()
    for secao in doc.sections:
        secao.page_width, secao.page_height = Cm(21.0), Cm(29.7)
        secao.top_margin, secao.left_margin = Cm(3), Cm(3)
        secao.bottom_margin, secao.right_margin = Cm(2), Cm(2)
    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(12)

    secoes_pre = True
    simples = False
    em_codigo = False
    bloco_tabela: list[str] = []
    pulou_nota = False
    i = 0
    while i < len(linhas):
        ln = linhas[i]
        s = ln.strip()

        if s.startswith("```"):
            em_codigo = not em_codigo
            i += 1
            continue
        if em_codigo:
            p = doc.add_paragraph()
            r = p.add_run(ln)
            r.font.name = "Consolas"
            r.font.size = Pt(9)
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_after = Pt(0)
            i += 1
            continue
        if not s or s == "---":
            if bloco_tabela:
                fonte = 8 if any("Temporada" in c for c in bloco_tabela[0].split("|")) else 10
                tabela(doc, [r.split("|")[1:-1] for r in bloco_tabela], fonte=fonte)
                bloco_tabela = []
            i += 1
            continue
        if s.startswith("<!--"):
            if "-->" not in s:
                while i < len(linhas) and "-->" not in linhas[i]:
                    i += 1
            i += 1
            continue
        if s.startswith("> ") and not pulou_nota and "Documento consolidado" in s:
            while i < len(linhas) and linhas[i].strip().startswith(">"):
                i += 1
            pulou_nota = True
            continue
        if s.startswith(">"):
            corpo(doc, s[2:], tamanho=10, simples=True)
            i += 1
            continue
        if s.startswith("|"):
            bloco_tabela.append(s)
            i += 1
            continue
        if s.startswith("# "):
            if secoes_pre and "INTRODUÇÃO" in s:
                secoes_pre = False
            p = doc.add_page_break() if i > 2 else None
            corpo(doc, s[2:], negrito=True, recuo=False, antes=12)
            simples = False
            i += 1
            continue
        if s.startswith("### "):
            corpo(doc, s[4:], negrito=True, recuo=False)
            i += 1
            continue
        if s.startswith("## "):
            titulo = s[3:]
            # Títulos pré-textuais carregam instruções de trabalho entre
            # parênteses no .md ("CAPA (elemento...)", "SUMÁRIO (obrigatório)");
            # o rascunho exibe só o nome da seção.
            titulo = re.sub(r"\s*\([^)]*\)\s*$", "", titulo)
            if titulo in ("RESUMO", "ABSTRACT"):
                simples = True
            elif titulo in PRE_CENTRALIZAR or titulo.startswith(("LISTA", "SUMÁRIO")):
                pass
            else:
                simples = False
            if titulo.startswith("APÊNDICE") or titulo == "REFERÊNCIAS":
                doc.add_page_break()
            corpo(doc, titulo, negrito=True, recuo=False, central=True, antes=12)
            if titulo == "FOLHA DE ROSTO":
                ph = corpo(doc, "[FICHA CATALOGRÁFICA — emitida pelo SISBI no depósito; placeholder]",
                            central=True, recuo=False, tamanho=10)
                ph.paragraph_format.space_before = Pt(24)
            i += 1
            continue
        # figura: linha só com (`figuras/....png`)
        if s.startswith("(`figuras/") and s.endswith("`)"):
            caminho = RAIZ / s[2:-2]
            if caminho.exists():
                doc.add_picture(str(caminho), width=Cm(15))
                doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            i += 1
            continue
        if s.startswith("**Figura ") or s.startswith("**Tabela "):
            corpo(doc, s, negrito=False, recuo=False, central=True)
            i += 1
            continue
        if s.startswith(("Legenda:", "Fonte:")):
            corpo(doc, s, tamanho=10, recuo=False, central=True)
            i += 1
            continue
        if s.startswith("- "):
            corpo(doc, "•  " + s[2:], recuo=False)
            i += 1
            continue
        corpo(doc, s, simples=simples)
        i += 1

    if bloco_tabela:
        tabela(doc, [r.split("|")[1:-1] for r in bloco_tabela])
    rodape_numerado(doc)
    doc.save(SAIDA)
    print(f"gravado em: {SAIDA} ({SAIDA.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
