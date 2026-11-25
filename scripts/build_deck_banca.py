#!/usr/bin/env python3
"""Gera a versão de banca do deck 2013–2024 (PPTX).

Reaproveita o desenho e os slides de resultado de `build_deck_artigo.py`,
acrescentando literatura, contribuições/limitações e conclusão.

Uso:
  python3 scripts/build_deck_banca.py
  libreoffice --headless --convert-to pdf --outdir apresentacao \
      apresentacao/apresentacao_banca_2013_2024.pptx
"""
from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.util import Inches

import build_deck_artigo as base

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "apresentacao" / "apresentacao_banca_2013_2024.pptx"


def _slide_literatura(prs, pagina: int = 2):
    slide = base._slide(prs, "Literatura", "O que já sabemos — e o que falta", pagina)
    cartoes = [
        ("Vantagem de casa",
         "Regularidade robusta no esporte coletivo (Pollard, 1986; "
         "Nevill & Holder, 1999)."),
        ("Brasil",
         "Estudos descritivos, amostras curtas e foco em diferenças entre "
         "clubes (Silva & Moreira, 2008; Pollard et al., 2008)."),
        ("Modelos",
         "Poisson ataque–defesa separa a qualidade das equipes do mando "
         "(Maher, 1982; Dixon & Coles, 1997)."),
        ("Jogos sem torcida",
         "Evidência internacional mista (Bryson et al., 2021; Fischer & "
         "Haucap, 2021; Endrich & Gesche, 2020)."),
    ]
    pos = [(0.55, 1.35), (5.05, 1.35), (0.55, 2.95), (5.05, 2.95)]
    for (titulo, corpo), (left, top) in zip(cartoes, pos):
        base._rect(slide, left, top, 4.35, 1.2, fill=base.WHITE,
                   line=base.LINE, rounded=True)
        base._text(slide, titulo, left + 0.15, top + 0.13, 4.05, 0.3,
                   size=13, bold=True, color=base.TEXT)
        base._text(slide, corpo, left + 0.15, top + 0.52, 4.05, 0.62,
                   size=9.5, color=base.MUTED, spacing=1.08)

    base._rect(slide, 0.55, 4.55, 9.0, 0.45, fill=base.MOSS_LIGHT,
               line=None, rounded=True)
    base._text(slide, "Lacuna: 12 temporadas, choques brasileiros (VAR e "
                      "pandemia) e um modelo formal de mudança.",
               0.75, 4.65, 8.6, 0.25, size=10.5, bold=True, color=base.DARK)
    base._nota(slide, "Situar o artigo: a literatura descreve a vantagem, mas "
                       "pouco testa sua estabilidade com modelos formais no "
                       "Brasil. O artigo preenche essa lacuna com 12 temporadas "
                       "e um desenho reprodutível.")
    return slide


def _slide_contribuicoes(prs, pagina: int = 10):
    slide = base._slide(prs, "Contribuições e limitações",
                        "O que entrega — e o que não entrega", pagina)
    base._rect(slide, 0.55, 1.35, 4.35, 2.3, fill=base.WHITE,
               line=base.LINE, rounded=True)
    base._text(slide, "CONTRIBUIÇÕES", 0.75, 1.5, 3.9, 0.25, size=9,
               bold=True, color=base.MOSS_TEXT)
    contrib = [
        "Base aberta e reprodutível, 2013–2024",
        "Mudança de nível e Poisson ataque–defesa",
        "Vantagem como fenômeno da liga (ICC 2,2%)",
        "Evidência multi-canal: público, cartões e pênaltis",
    ]
    base._text(slide, "\n".join(f"✓  {l}" for l in contrib), 0.75, 1.85,
              3.9, 1.7, size=11, color=base.TEXT, spacing=1.25)

    base._rect(slide, 5.15, 1.35, 4.3, 2.3, fill=base.WHITE,
               line=base.LINE, rounded=True)
    base._text(slide, "LIMITAÇÕES", 5.35, 1.5, 3.9, 0.25, size=9,
               bold=True, color=base.TERRA_DARK)
    limites = [
        "Observacional: sem identificação causal",
        "Apenas Série A; outras competições não observadas",
        "Pênaltis: só convertidos, sem marcados/perdidos",
        "Quebra de 2019 confundida com VAR e pandemia",
    ]
    base._text(slide, "\n".join(f"×  {l}" for l in limites), 5.35, 1.85,
              3.9, 1.7, size=11, color=base.TEXT, spacing=1.25)

    base._text(slide, "A conclusão central é descritiva: magnitude e queda não "
                      "dependem de identificação causal.",
               0.55, 4.05, 9.0, 0.25, size=9.5, color=base.MUTED)
    base._nota(slide, "Separar o que o desenho entrega do que ele não entrega. "
                       "As contribuições são a base reprodutível, os modelos e a "
                       "leitura da vantagem como fenômeno da liga. As limitações "
                       "são o desenho observacional, o recorte Série A, os "
                       "pênaltis convertidos e a confusão de 2019.")
    return slide


def _slide_conclusao(prs, pagina: int = 11):
    slide = base._slide(prs, "Conclusão", "A vantagem caiu — e o patamar mudou",
                        pagina, dark=True)
    base._text(slide, "63,0%", 0.55, 1.25, 2.6, 0.7, font="Georgia", size=38,
               bold=True, color=base.GOLD)
    base._text(slide, "dos pontos no período", 0.55, 1.92, 3.2, 0.25,
               size=10, color=base.DARK_MUTED)
    base._text(slide, "65,0% → 61,0%", 0.55, 2.45, 3.4, 0.5,
               font="Georgia", size=25, bold=True, color=base.DARK_TEXT)
    base._text(slide, "média 2013–2018 → 2019–2024", 0.55, 2.95, 3.5, 0.25,
               size=9.5, color=base.DARK_MUTED)
    base._text(slide, "61,0%", 0.55, 3.55, 2.0, 0.5, font="Georgia", size=28,
               bold=True, color=base.GOLD)
    base._text(slide, "referência pós-2019 (60,6% em 2022–24)", 0.55, 4.05,
              3.8, 0.25, size=9, color=base.DARK_MUTED)

    base._rect(slide, 5.05, 1.25, 4.4, 3.2, fill=base.CARD_DARK,
               line=base.CARD_LINE, rounded=True)
    base._text(slide, "O QUE FICA", 5.25, 1.4, 4.0, 0.25, size=9, bold=True,
               color=base.GOLD)
    linhas = [
        "A vantagem é grande, mas não constante.",
        "A queda é robusta em gols e não é composição de equipes.",
        "A causa segue em aberto: VAR, pandemia, calendário e arbitragem.",
    ]
    base._text(slide, "\n".join(f"—  {l}" for l in linhas), 5.25, 1.8,
              4.0, 2.2, size=11, color=base.DARK_TEXT, spacing=1.25)

    base._text(slide, "Obrigado. Perguntas?", 0.55, 4.65, 5.5, 0.4,
               font="Georgia", size=24, bold=True, color=base.GOLD)
    base._text(slide, "github.com/EmiyaKiritsugu3/TCC", 6.5, 4.95, 3.0, 0.2,
               size=8, color=base.DARK_MUTED, align=base.PP_ALIGN.RIGHT)
    base._nota(slide, "Fechar com a resposta curta: a vantagem é grande, caiu "
                       "4,0 p.p. e o patamar pós-2019 é 61,0%. A causa não é "
                       "identificada; o artigo entrega a magnitude, a robustez "
                       "em gols e a agenda.")
    return slide


def main() -> None:
    for nome in ("deck_serie_pollard.png", "deck_cartoes.png"):
        if not (base.FIG / nome).exists():
            raise SystemExit(
                f"figura ausente: {base.FIG / nome}; rode scripts/make_deck_figures.py"
            )
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)
    prs.core_properties.title = "Vantagem de jogar em casa na Série A (2013–2024) — banca"
    prs.core_properties.author = "José Inamar de Medeiros Júnior"

    base._titulo_slide(prs)
    _slide_literatura(prs, 2)
    base._slide_pergunta(prs, 3)
    base._slide_dados(prs, 4)
    base._slide_metodos(prs, 5)
    base._slide_resultado1(prs, 6)
    base._slide_resultado2(prs, 7)
    base._slide_resultado3(prs, 8)
    base._slide_canais(prs, 9)
    _slide_contribuicoes(prs, 10)
    _slide_conclusao(prs, 11)

    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    prs.save(SAIDA)
    print(f"gravado em: {SAIDA}")


if __name__ == "__main__":
    main()
