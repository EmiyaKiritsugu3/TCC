#!/usr/bin/env python3
"""Gera o artigo 2013–2024 em DOCX e PDF (layout de manuscrito).

Entrada: docs/artigo_2013_2024.md
Saídas: docs/artigo_2013_2024.docx e .pdf
"""
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, RGBColor

from docx_common import configurar, pagina, paragrafo, tabela

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA_EN = RAIZ / "docs" / "artigo_2013_2024.md"
SAIDA_EN = RAIZ / "docs" / "artigo_2013_2024.docx"
ENTRADA_PT = RAIZ / "docs" / "artigo_2013_2024_pt.md"
SAIDA_PT = RAIZ / "docs" / "artigo_2013_2024_pt.docx"
VERDE = RGBColor(0x14, 0x53, 0x2D)
CINZA = RGBColor(0x55, 0x55, 0x55)


def _renderizar(doc, linhas: list[str], pasta: Path) -> None:
    i = 0
    refs = False
    abstract = False
    while i < len(linhas):
        s = linhas[i].strip()
        if not s or s == "---":
            i += 1
            continue
        if s.startswith("# "):
            paragrafo(doc, s[2:], tamanho=17, negrito=True, central=True,
                       espaco=1.05, depois=8, cor=VERDE)
            i += 1
            continue
        if s.startswith("José Inamar"):
            paragrafo(doc, s, tamanho=11.5, central=True, depois=2)
            i += 1
            continue
        if s.startswith("Universidade Federal"):
            paragrafo(doc, s, tamanho=9.8, italico=True, central=True,
                       depois=10, cor=CINZA)
            i += 1
            continue
        if s.startswith("#### "):
            paragrafo(doc, s[5:], tamanho=10.7, negrito=True, italico=True,
                       antes=6, depois=2, cor=VERDE)
            i += 1
            continue
        if s.startswith("### "):
            paragrafo(doc, s[4:], tamanho=11.3, negrito=True, italico=True,
                       antes=8, depois=2, cor=VERDE)
            i += 1
            continue
        if s.startswith("## "):
            titulo = s[3:]
            chave = titulo.lower()
            refs = chave in {"references", "referências", "referencias"}
            abstract = chave in {"abstract", "resumo"}
            paragrafo(doc, titulo, tamanho=12.5, negrito=True, antes=12,
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
                    tabela(doc, linhas_tab, fonte=8.0,
                            larguras=[1.6, 1.7, 4.2, 2.8, 5.7])
                elif ncols == 5:
                    tabela(doc, linhas_tab, fonte=8.2,
                            larguras=[5.8, 2.0, 1.5, 2.8, 2.8])
                else:
                    tabela(doc, linhas_tab)
            continue
        imagem = re.fullmatch(r"!\[(.*?)\]\((.+?)\)", s)
        if imagem:
            legenda, caminho = imagem.groups()
            arquivo = (pasta / caminho).resolve()
            if not arquivo.exists():
                raise FileNotFoundError(f"figura ausente: {arquivo}")
            doc.add_picture(str(arquivo), width=Cm(13.5))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            paragrafo(doc, legenda, tamanho=8.5, italico=True,
                       central=True, antes=2, depois=8, cor=CINZA)
            i += 1
            continue
        if s.startswith("**Table 1."):
            paragrafo(doc, s, tamanho=9.5, central=True, antes=4, depois=2)
            i += 1
            continue
        if s.startswith("**Table ") or s.startswith("**Figure ") \
                or s.startswith("**Tabela ") or s.startswith("**Figura "):
            paragrafo(doc, s, tamanho=9.5, central=True, antes=4, depois=2)
            i += 1
            continue
        if s.startswith("Notes:") or s.startswith("Notas:") \
                or s.startswith("Nota:") or s.startswith("Fonte:"):
            paragrafo(doc, s, tamanho=8.3, italico=True, depois=8, cor=CINZA)
            i += 1
            continue
        if s.startswith("**Keywords:**") or s.startswith("**JEL codes:**") \
                or s.startswith("**Palavras-chave:**") \
                or s.startswith("**Códigos JEL:**"):
            paragrafo(doc, s, tamanho=9.8, depois=3)
            abstract = False
            i += 1
            continue
        paragrafo(doc, s, recuo=(not refs and not abstract), hanging=refs,
                   tamanho=8.8 if refs else (10.0 if abstract else 10.6),
                   espaco=0.98 if refs else 1.12,
                   depois=2 if refs else 4)
        i += 1


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pt", action="store_true",
                        help="gera a versão em português")
    parser.add_argument("--entrada", type=Path, default=None,
                        help="Markdown de entrada (opcional)")
    parser.add_argument("--saida", type=Path, default=None,
                        help="DOCX de saída (opcional)")
    args = parser.parse_args(argv)
    if args.pt:
        entrada, saida = ENTRADA_PT, SAIDA_PT
        header = "Vantagem de jogar em casa na Série A (2013–2024)"
    else:
        entrada, saida = ENTRADA_EN, SAIDA_EN
        header = "Home advantage in Brazilian Série A (2013–2024)"
    if args.entrada is not None:
        entrada = args.entrada if args.entrada.is_absolute() else RAIZ / args.entrada
    if args.saida is not None:
        saida = args.saida if args.saida.is_absolute() else RAIZ / args.saida
    linhas = entrada.read_text(encoding="utf-8").splitlines()
    doc = Document()
    configurar(doc, top=2.0, left=2.3, bottom=1.8, right=2.3, tamanho=10.6)
    doc.core_properties.title = header
    doc.core_properties.author = "José Inamar de Medeiros Júnior"
    _renderizar(doc, linhas, entrada.parent)
    pagina(doc, cabecalho=header)
    doc.save(saida)
    print(f"gravado em: {saida}")
    subprocess.run(
        ["libreoffice", "--headless", "--convert-to", "pdf",
         "--outdir", str(saida.parent), str(saida)],
        check=True,
    )


if __name__ == "__main__":
    main()
