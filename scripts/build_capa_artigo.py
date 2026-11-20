#!/usr/bin/env python3
"""Gera capa e folha de rosto no padrão UFRN/CERES-BSI.

Saídas:
  docs/capa_folha_rosto_artigo.docx
  docs/capa_folha_rosto_artigo.pdf
  docs/artigo_2013_2024_abnt_completo.pdf (capa + folha + artigo)
"""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "docs" / "capa_folha_rosto_artigo.docx"
ARTIGO = RAIZ / "docs" / "artigo_2013_2024_abnt.pdf"
COMPLETO = RAIZ / "docs" / "artigo_2013_2024_abnt_completo.pdf"

TITULO = ("VANTAGEM DE JOGAR EM CASA NA SÉRIE A: UMA ANÁLISE BASEADA "
          "EM MODELOS DE 12 TEMPORADAS (2013–2024)")
AUTOR = "JOSÉ INAMAR DE MEDEIROS JÚNIOR"
INSTITUICAO = [
    "UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE",
    "CENTRO DE ENSINO SUPERIOR DO SERIDÓ",
    "DEPARTAMENTO DE COMPUTAÇÃO E TECNOLOGIA",
    "BACHARELADO EM SISTEMAS DE INFORMAÇÃO",
]
NATUREZA = (
    "Artigo apresentado ao Bacharelado em Sistemas de Informação do Centro de "
    "Ensino Superior do Seridó da Universidade Federal do Rio Grande do Norte "
    "como requisito parcial para obtenção do título de Bacharel em Sistemas "
    "de Informação."
)
ORIENTADOR = "Orientador: Prof. Dr. Francisco Marcio Barboza"
CIDADE = "CAICÓ – RN"
ANO = "2026"


def _texto(doc, texto: str, *, tamanho: float = 12, negrito: bool = False,
           central: bool = True, antes: int = 0, depois: int = 0,
           esquerda: float = 0.0) -> None:
    par = doc.add_paragraph()
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER if central else WD_ALIGN_PARAGRAPH.JUSTIFY
    fmt = par.paragraph_format
    fmt.space_before = Pt(antes)
    fmt.space_after = Pt(depois)
    fmt.line_spacing = 1.5
    if esquerda:
        fmt.left_indent = Cm(esquerda)
    run = par.add_run(texto)
    run.font.name = "Times New Roman"
    run.font.size = Pt(tamanho)
    run.bold = negrito


def _configurar(doc: Document) -> None:
    for secao in doc.sections:
        secao.page_width, secao.page_height = Cm(21.0), Cm(29.7)
        secao.top_margin, secao.left_margin = Cm(3.0), Cm(3.0)
        secao.bottom_margin, secao.right_margin = Cm(2.0), Cm(2.0)
    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(12)


def _capa(doc: Document) -> None:
    for linha in INSTITUICAO:
        _texto(doc, linha, negrito=True, depois=0)
    _texto(doc, "", depois=0)
    _texto(doc, "", depois=0)
    _texto(doc, TITULO, tamanho=14, negrito=True, antes=60, depois=0)
    _texto(doc, "", depois=0)
    _texto(doc, "", depois=0)
    _texto(doc, AUTOR, antes=48, depois=0)
    for _ in range(8):
        _texto(doc, "", depois=0)
    _texto(doc, CIDADE, depois=0)
    _texto(doc, ANO, depois=0)
    doc.add_page_break()


def _folha(doc: Document) -> None:
    _texto(doc, AUTOR, negrito=True, depois=0)
    _texto(doc, TITULO, tamanho=14, negrito=True, antes=48, depois=0)
    _texto(doc, "", depois=0)
    _texto(doc, NATUREZA, tamanho=12, central=False, antes=48,
           depois=0, esquerda=8.0)
    _texto(doc, "", depois=0)
    _texto(doc, ORIENTADOR, antes=12, depois=0)
    for _ in range(6):
        _texto(doc, "", depois=0)
    _texto(doc, CIDADE, depois=0)
    _texto(doc, ANO, depois=0)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artigo", type=Path, default=ARTIGO)
    args = parser.parse_args(argv)
    artigo = args.artigo if args.artigo.is_absolute() else RAIZ / args.artigo
    doc = Document()
    _configurar(doc)
    _capa(doc)
    _folha(doc)
    doc.core_properties.title = TITULO
    doc.core_properties.author = AUTOR
    doc.save(SAIDA)
    subprocess.run(
        ["libreoffice", "--headless", "--convert-to", "pdf",
         "--outdir", str(SAIDA.parent), str(SAIDA)],
        check=True,
    )
    subprocess.run(
        ["pdfunite",
         str(SAIDA.with_suffix(".pdf")), str(artigo), str(COMPLETO)],
        check=True,
    )
    print(f"gravado em: {SAIDA}")
    print(f"gravado em: {SAIDA.with_suffix('.pdf')}")
    print(f"gravado em: {COMPLETO}")


if __name__ == "__main__":
    main()
