#!/usr/bin/env python3
"""Gera a versão de 5 minutos do deck 2013–2024 (PPTX).

Estrutura enxuta: pergunta/base, nível, gols, equipes/canais e conclusão.
Reaproveita o desenho de `build_deck_artigo.py` e a conclusão da banca.
"""
from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.util import Inches

import build_deck_artigo as base
from build_deck_banca import _slide_conclusao

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "apresentacao" / "apresentacao_5min_2013_2024.pptx"


def _slide_pergunta_base(prs, pagina: int = 2):
    slide = base._slide(prs, "Pergunta e base",
                        "Pergunta, base e métodos", pagina)
    perguntas = [
        ("01", "Qual a magnitude?",
         "63,0% dos pontos (IC 95% 61,7–64,3)."),
        ("02", "Mudou após 2018?",
         "65,0% → 61,0%; quebra estimada em 2019."),
        ("03", "Quais canais?",
         "Público, viagem, cartões e arbitragem."),
    ]
    for i, (num, titulo, corpo) in enumerate(perguntas):
        top = 1.35 + i * 1.02
        base._rect(slide, 0.55, top, 4.35, 0.9, fill=base.WHITE,
                   line=base.LINE, rounded=True)
        base._text(slide, num, 0.7, top + 0.15, 0.45, 0.3,
                   font="Georgia", size=14, bold=True, color=base.GOLD_DARK)
        base._text(slide, titulo, 1.15, top + 0.1, 3.55, 0.3,
                   size=11.5, bold=True, color=base.TEXT)
        base._text(slide, corpo, 1.15, top + 0.43, 3.55, 0.35,
                   size=9.5, color=base.MUTED)

    stats = [
        ("4.559", "partidas"),
        ("12", "temporadas"),
        ("99,92%", "placares idênticos"),
        ("12/12", "campeões"),
    ]
    pos = [(5.2, 1.35), (7.35, 1.35), (5.2, 2.55), (7.35, 2.55)]
    for (valor, rotulo), (left, top) in zip(stats, pos):
        base._stat(slide, left, top, 2.0, 1.0, valor, rotulo, value_size=21)

    base._text(slide, "Métodos: Pollard, mudança de nível, Poisson ataque–defesa "
                      "e ICC. Base MIT; validação OpenFootball (CC0).",
              0.55, 4.55, 9.0, 0.3, size=9.5, color=base.MUTED)
    base._text(slide, "O desenho é observacional: não identifica causalidade.",
              0.55, 4.9, 9.0, 0.2, size=8.5, color=base.TERRA_DARK)
    base._nota(slide, "Em 5 minutos: apresentar a pergunta, o recorte de 12 "
                       "temporadas e a base validada. Dizer que os métodos "
                       "separam qualidade das equipes do efeito de casa.")
    return slide


def _slide_equipes_canais(prs, pagina: int = 5):
    slide = base._slide(prs, "Equipes e canais",
                        "A vantagem é da liga; os canais são fracos", pagina)
    cards = [
        ("2,2%", "da variância entre equipes", base.TERRA),
        ("ρ = 0,08", "público × vantagem de casa", base.MUTED),
        ("+0,35", "cartões: IC −0,03 a +0,72", base.MOSS),
        ("+0,05", "pênaltis: IC −0,06 a +0,15", base.DARK),
    ]
    pos = [(0.55, 1.3), (5.15, 1.3), (0.55, 2.75), (5.15, 2.75)]
    for (valor, rotulo, cor), (left, top) in zip(cards, pos):
        base._rect(slide, left, top, 4.3, 1.15, fill=base.WHITE,
                   line=base.LINE, rounded=True)
        base._text(slide, valor, left + 0.15, top + 0.12, 2.0, 0.45,
                   font="Georgia", size=26, bold=True, color=cor)
        base._text(slide, rotulo, left + 0.15, top + 0.67, 4.0, 0.3,
                   size=9.5, color=base.MUTED)

    base._text(slide, "O público separa clubes grandes de pequenos, mas não "
                      "explica a vantagem dentro do mesmo clube. Cartões são "
                      "sugestivos; 2020 mistura pandemia e calendário.",
              0.55, 4.15, 9.0, 0.45, size=9.5, color=base.MUTED, spacing=1.05)
    base._nota(slide, "A vantagem é fenômeno da liga: ICC de 2,2%. O público "
                       "tem correlação fraca com a vantagem e forte com pontos. "
                       "Cartões e pênaltis são sugestivos, não conclusivos.")
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
    prs.core_properties.title = "Vantagem de jogar em casa na Série A (2013–2024) — 5 min"
    prs.core_properties.author = "José Inamar de Medeiros Júnior"

    base._titulo_slide(prs)
    _slide_pergunta_base(prs, 2)
    base._slide_resultado1(prs, 3)
    base._slide_resultado2(prs, 4)
    _slide_equipes_canais(prs, 5)
    _slide_conclusao(prs, 6)

    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    prs.save(SAIDA)
    print(f"gravado em: {SAIDA}")


if __name__ == "__main__":
    main()
