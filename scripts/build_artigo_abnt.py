#!/usr/bin/env python3
"""Gera o artigo 2013–2024 em formato ABNT (DOCX e PDF).

Entrada: docs/artigo_2013_2024_abnt.md
Saídas: docs/artigo_2013_2024_abnt.docx e .pdf

Formato: A4, margens 3 cm (superior/esquerda) e 2 cm (inferior/direita),
Times New Roman 12, espaçamento 1,5, recuo de primeira linha 1,25 cm,
títulos de seção primária em caixa alta, referências em NBR 6023.
"""
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm

from docx_common import configurar, pagina, paragrafo, tabela

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "docs" / "artigo_2013_2024_abnt.md"
SAIDA = RAIZ / "docs" / "artigo_2013_2024_abnt.docx"
SAIDA_P4 = RAIZ / "docs" / "artigo_2013_2024_abnt_p4.docx"


def _paragrafo(doc, texto: str, **kwargs) -> None:
    kwargs.setdefault("indent", 1.25)
    kwargs.setdefault("espaco", 1.5)
    paragrafo(doc, texto, **kwargs)


def _tabela(doc, linhas: list[list[str]], larguras: list[float],
            fonte: float = 9.0) -> None:
    tabela(doc, linhas, larguras=larguras, fonte=fonte)


def _pagina(doc, inicio: int = 1) -> None:
    pagina(doc, inicio)


def _titulo_secao(titulo: str) -> tuple[str, bool]:
    """Devolve (texto, é_primária) no padrão ABNT."""
    m = re.match(r"^(\d+)\.\s+(.+)$", titulo)
    if m:
        return f"{m.group(1)} {m.group(2).upper()}", True
    m = re.match(r"^(\d+\.\d+)\s+(.+)$", titulo)
    if m:
        return f"{m.group(1)} {m.group(2)}", False
    return titulo.upper(), True


def _renderizar(doc, linhas: list[str], pasta: Path) -> None:
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
        if s.startswith("#### "):
            _paragrafo(doc, s[5:], tamanho=11, negrito=True, antes=6,
                       depois=2, recuo=False, espaco=1.2)
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
                    _tabela(doc, linhas_tab, [5.8, 2.0, 1.5, 2.8, 2.8], 9.0)
                else:
                    _tabela(doc, linhas_tab, [3.2] * len(linhas_tab[0]), 9.0)
            continue
        imagem = re.fullmatch(r"!\[(.*?)\]\((.+?)\)", s)
        if imagem:
            legenda, caminho = imagem.groups()
            arquivo = (pasta / caminho).resolve()
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
            _paragrafo(doc, s, tamanho=9, espaco=1.0,
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


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inicio", type=int, default=1)
    parser.add_argument("--entrada", type=Path, default=None,
                        help="Markdown de entrada (opcional)")
    parser.add_argument("--saida", type=Path, default=None,
                        help="DOCX de saída (opcional)")
    args = parser.parse_args(argv)
    entrada = args.entrada or ENTRADA
    if args.saida is not None:
        saida = args.saida
    else:
        saida = SAIDA_P4 if args.inicio == 4 else SAIDA
    if not entrada.is_absolute():
        entrada = RAIZ / entrada
    if not saida.is_absolute():
        saida = RAIZ / saida
    linhas = entrada.read_text(encoding="utf-8").splitlines()
    doc = Document()
    configurar(doc, top=3.0, left=3.0, bottom=2.0, right=2.0, tamanho=12)
    doc.core_properties.title = "Vantagem de jogar em casa na Série A (2013–2024)"
    doc.core_properties.author = "José Inamar de Medeiros Júnior"
    _renderizar(doc, linhas, entrada.parent)
    _pagina(doc, args.inicio)
    doc.save(saida)
    print(f"gravado em: {saida}")
    subprocess.run(
        ["libreoffice", "--headless", "--convert-to", "pdf",
         "--outdir", str(saida.parent), str(saida)],
        check=True,
    )


if __name__ == "__main__":
    main()
