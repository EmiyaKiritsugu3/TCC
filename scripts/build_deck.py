#!/usr/bin/env python3
"""Gera o deck de defesa (PPTX) a partir das figuras e números da monografia.

Uso:
  python3 scripts/build_deck.py
  libreoffice --headless --convert-to pdf --outdir apresentacao \
      apresentacao/apresentacao_tcc.pptx

O PDF não é gerado por este script porque depende do LibreOffice.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

RAIZ = Path(__file__).resolve().parent.parent
FIG = RAIZ / "figuras"
SAIDA = RAIZ / "apresentacao" / "apresentacao_tcc.pptx"

DARK = RGBColor(0x14, 0x53, 0x2D)
CREAM = RGBColor(0xF7, 0xF3, 0xE8)
GOLD = RGBColor(0xD4, 0xA0, 0x17)
TEXT = RGBColor(0x1F, 0x29, 0x37)
MUTED = RGBColor(0x6B, 0x72, 0x80)
LINE = RGBColor(0xE5, 0xE0, 0xD0)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
DARK_TEXT = RGBColor(0xF7, 0xF3, 0xE8)
DARK_MUTED = RGBColor(0xD9, 0xD2, 0xC0)
FOOTER_LIGHT = RGBColor(0x57, 0x53, 0x4E)
FOOTER_DARK = RGBColor(0xA9, 0xBE, 0xAE)


def _bg(slide, cor: RGBColor) -> None:
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = cor


def _texto(slide, texto, left, top, width, height, *, font="Calibri",
           size=15, bold=False, color=TEXT, align=PP_ALIGN.LEFT,
           anchor=MSO_ANCHOR.TOP, spacing=1.0, space_after=4):
    caixa = slide.shapes.add_textbox(Inches(left), Inches(top),
                                     Inches(width), Inches(height))
    tf = caixa.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    for i, linha in enumerate(str(texto).split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = linha
        p.alignment = align
        p.line_spacing = spacing
        p.space_after = Pt(space_after)
        for run in p.runs:
            run.font.name = font
            run.font.size = Pt(size)
            run.font.bold = bold
            run.font.color.rgb = color
    return caixa


def _barra(slide, left, top, width, height, cor=GOLD):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top),
                                 Inches(width), Inches(height))
    shp.fill.solid()
    shp.fill.fore_color.rgb = cor
    shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def _cartao(slide, left, top, width, height, *, fill=WHITE, line=LINE):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top),
                                 Inches(width), Inches(height))
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(1)
    shp.shadow.inherit = False
    return shp


def _imagem(slide, caminho: Path, left, top, max_w, max_h):
    with Image.open(caminho) as im:
        largura, altura = im.size
    escala = min(max_w / largura, max_h / altura)
    w, h = largura * escala, altura * escala
    slide.shapes.add_picture(
        str(caminho),
        Inches(left + (max_w - w) / 2),
        Inches(top + (max_h - h) / 2),
        Inches(w),
        Inches(h),
    )


def _rodape(slide, pagina: int, *, dark=False):
    cor = FOOTER_DARK if dark else FOOTER_LIGHT
    _texto(slide, "Vantagem de jogar em casa — Brasileirão Série A (2006–2024)",
           0.5, 5.25, 7.0, 0.25, size=9, color=cor)
    _texto(slide, str(pagina), 9.0, 5.25, 0.5, 0.25, size=9, color=cor,
           align=PP_ALIGN.RIGHT)


def _slide(prs, titulo: str, pagina: int, *, dark=False):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _bg(slide, DARK if dark else CREAM)
    _barra(slide, 0.7, 0.95, 0.9, 0.07)
    _texto(slide, titulo, 0.7, 0.25, 8.6, 0.7, font="Georgia", size=32,
           bold=True, color=DARK_TEXT if dark else TEXT)
    if pagina > 1:
        _rodape(slide, pagina, dark=dark)
    return slide


def _stat(slide, left, top, width, height, valor, rotulo, *,
          value_size=30, dark=False):
    _cartao(slide, left, top, width, height,
            fill=DARK if dark else WHITE,
            line=None if dark else LINE)
    _texto(slide, valor, left + 0.1, top + 0.1, width - 0.2, 0.62,
           font="Georgia", size=value_size, bold=True,
           color=WHITE if dark else DARK)
    _texto(slide, rotulo, left + 0.1, top + 0.72, width - 0.2, height - 0.8,
           size=11, color=DARK_MUTED if dark else MUTED)


def _titulo(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _bg(slide, DARK)
    _barra(slide, 0.5, 0.9, 0.12, 3.9)
    _texto(slide, "Vantagem de jogar em casa", 0.9, 0.9, 8.6, 0.9,
           font="Georgia", size=44, bold=True, color=DARK_TEXT)
    _texto(slide, "no Campeonato Brasileiro Série A", 0.9, 1.85, 8.6, 0.95,
           font="Georgia", size=30, color=GOLD)
    _texto(slide,
           "Dashboard interativo para análise de resultados históricos (2006–2024)",
           0.9, 2.85, 8.6, 0.5, size=17, color=DARK_TEXT)
    _texto(slide,
           "José Inamar de Medeiros Júnior  •  Sistemas de Informação  •  2026",
           0.9, 3.85, 8.6, 0.4, size=14, color=DARK_TEXT)
    _texto(slide,
           "Orientador: Dr. Francisco Marcio Barboza  •  Defesa de TCC",
           0.9, 4.3, 8.6, 0.4, size=13, color=DARK_MUTED)


def _problema(prs):
    s = _slide(prs, "Problema de pesquisa", 2)
    _texto(s,
           "Qual foi a magnitude da vantagem de jogar em casa no Brasileirão "
           "Série A entre 2006 e 2024, e como os indicadores variaram entre "
           "as temporadas?",
           0.7, 1.25, 5.6, 1.5, font="Georgia", size=18, color=DARK)
    _texto(s,
           "•  Proporção de vitórias do mandante, empates e visitantes\n"
           "•  Média de gols em casa × fora\n"
           "•  Índice de Pollard por temporada\n"
           "•  Diferenças entre temporadas e clubes",
           0.7, 2.95, 5.6, 2.0, size=15, spacing=1.15)
    _stat(s, 6.7, 1.25, 2.6, 1.7, "7.219", "partidas validadas\nSérie A 2006–2024")
    _stat(s, 6.7, 3.25, 2.6, 1.7, "63,7%", "índice de Pollard\nno período")


def _metodo(prs):
    s = _slide(prs, "Método em uma figura", 3)
    passos = ["Fonte\npinada", "Limpeza\nregrada", "Métricas\npuras",
              "Dashboard\nStreamlit", "Validação\ndupla"]
    for i, passo in enumerate(passos):
        left = 0.55 + i * 1.85
        _cartao(s, left, 1.5, 1.55, 1.5)
        _texto(s, passo, left + 0.05, 1.65, 1.45, 1.2, size=14, bold=True,
               color=TEXT, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        if i < len(passos) - 1:
            _texto(s, "›", left + 1.55, 1.9, 0.3, 0.7, size=28, bold=True,
                   color=DARK, align=PP_ALIGN.CENTER)
    _cartao(s, 0.55, 3.4, 4.35, 1.5, fill=DARK, line=None)
    _texto(s, "99,96% vs OpenFootball (CC0)\n2.659/2.660 idênticas",
           0.65, 3.55, 4.15, 1.2, size=15, bold=True, color=WHITE)
    _cartao(s, 5.1, 3.4, 4.35, 1.5, fill=DARK, line=None)
    _texto(s, "19/19 campeões recalculados\npontuações conferem",
           5.2, 3.55, 4.15, 1.2, size=15, bold=True, color=WHITE)


def _geral(prs):
    s = _slide(prs, "Resultado geral do período", 4)
    _imagem(s, FIG / "fig1_distribuicao_geral.png", 0.55, 1.3, 5.9, 3.05)
    _stat(s, 6.7, 1.3, 2.6, 1.05, "49,0%", "vitórias do mandante")
    _stat(s, 6.7, 2.65, 2.6, 1.05, "63,7%", "Pollard (H1 confirmada)")
    _stat(s, 6.7, 4.0, 2.6, 1.05, "1,49 × 1,00", "gols casa × fora / jogo")


def _evolucao(prs):
    s = _slide(prs, "Variação entre temporadas (H2)", 5)
    _imagem(s, FIG / "fig2_pollard_temporadas.png", 0.55, 1.3, 5.9, 3.05)
    _stat(s, 6.7, 1.3, 2.6, 1.05, "69,5%", "máximo — 2018")
    _stat(s, 6.7, 2.65, 2.6, 1.05, "58,2%", "mínimo — 2017")
    _texto(s,
           "Nenhum ano abaixo de 50%. Mudança de nível pós-2018: "
           "64,9% → 61,0% (IC 2,1–5,6).",
           6.7, 4.0, 2.6, 0.9, size=12, color=TEXT)


def _nivel(prs):
    s = _slide(prs, "Mudança de nível pós-2018", 6)
    _imagem(s, FIG / "fig9_serie_ic.png", 0.55, 1.3, 5.9, 3.05)
    _stat(s, 6.7, 1.3, 2.6, 1.05, "64,9%", "média 2006–2018")
    _stat(s, 6.7, 2.65, 2.6, 1.05, "61,0%", "média 2019–2024")
    _stat(s, 6.7, 4.0, 2.6, 0.9, "−3,9 p.p.", "IC 95% 2,1–5,6")
    _texto(s, "Ponto de quebra: 2019. VAR e pandemia no mesmo período — "
              "o desenho não separa os choques.",
           0.7, 4.55, 5.6, 0.5, size=12, color=MUTED)


def _gols(prs):
    s = _slide(prs, "Gols: casa × fora, sempre", 7)
    _imagem(s, FIG / "fig4_gols_temporadas.png", 0.55, 1.3, 5.9, 3.05)
    _texto(s,
           "Mandante marcou mais nas 19 temporadas. "
           "Diferença média: +0,49 gol/jogo.",
           6.7, 1.3, 2.6, 1.5, size=15, color=TEXT)
    _stat(s, 6.7, 3.3, 2.6, 1.3, "+0,49", "diferença média\ngol por jogo")


def _contexto(prs):
    s = _slide(prs, "Contexto da partida", 8)
    _imagem(s, FIG / "fig10_contexto.png", 0.45, 1.2, 4.3, 3.9)
    blocos = [
        ("Distância", "63,4%–63,9% nas três faixas", "viagem não é o principal"),
        ("Clássico", "58,2% mesmo sem viagem", "8,2 p.p. acima do neutro"),
        ("Estádio habitual", "64,1% vs. 59,4%", "0,13 ponto/jogo dentro da equipe"),
        ("Mandante zebra", "55,6%", "acima de 50% mesmo sendo pior"),
    ]
    y = 1.3
    for titulo, valor, nota in blocos:
        _texto(s, titulo, 4.95, y, 4.3, 0.28, size=12, bold=True, color=DARK)
        _texto(s, valor, 4.95, y + 0.26, 4.3, 0.32, font="Georgia", size=18,
               bold=True, color=TEXT)
        _texto(s, nota, 4.95, y + 0.58, 4.3, 0.28, size=10, color=MUTED)
        y += 0.92


def _matriz(prs):
    s = _slide(prs, "Matriz de correlação (Spearman)", 15)
    _imagem(s, FIG / "fig11_correlacoes_equipe.png", 0.45, 1.2, 4.5, 3.9)
    _texto(s,
           "HA × casa  +0,57\n"
           "HA × fora  −0,46\n"
           "componentes mecânicos do HA\n\n"
           "Distância média  −0,01\n"
           "Estádio habitual  +0,10\n"
           "Temporada  −0,19\n"
           "Pontos  +0,08  •  Posição  −0,08",
           5.1, 1.4, 4.2, 3.4, size=13, spacing=1.15)
    _texto(s,
           "No nível de partida, a maior associação é a diferença de posição "
           "(+0,19); as demais ficam entre −0,05 e +0,03.",
           5.1, 4.35, 4.2, 0.6, size=10, color=MUTED)


def _publico(prs):
    s = _slide(prs, "Público e arbitragem", 9)
    _imagem(s, FIG / "fig12_publico_ha.png", 0.55, 1.15, 8.9, 3.35)
    _texto(s,
           "6.618 registros de público (91,7%)  •  177 árbitros em 6.821 jogos  "
           "•  ρ público × HA = 0,04  •  ρ público × pontos = 0,79",
           0.7, 4.62, 8.8, 0.3, size=11, bold=True, color=DARK)
    _texto(s,
           "Em 2020, sem torcida, Pollard 60,2%; em 2022–2024, 60,6%. "
           "O retorno do público não restaurou o patamar pré-2019.",
           0.7, 4.92, 8.8, 0.3, size=10, color=MUTED)


def _cartoes_serie(prs):
    s = _slide(prs, "Cartões: um canal de arbitragem", 10)
    _imagem(s, FIG / "fig13_cartoes.png", 0.55, 1.25, 5.9, 3.15)
    _stat(s, 6.7, 1.3, 2.6, 1.05, "−0,18", "amarelos casa−fora (2019)")
    _stat(s, 6.7, 2.55, 2.6, 1.05, "+0,11", "em 2020, sem torcida")
    _stat(s, 6.7, 3.8, 2.6, 0.95, "4.559", "partidas (2013–2024)")
    _texto(s, "Fonte: BrazilianFootball/Data (MIT); 1 cartão não atribuído.",
           0.7, 4.6, 5.6, 0.3, size=10, color=MUTED)


def _cartoes_metodo(prs):
    s = _slide(prs, "Cartões: o que o dado permite dizer", 11)
    _cartao(s, 0.55, 1.35, 2.9, 2.95)
    _texto(s, "+0,35", 0.75, 1.5, 2.5, 0.7, font="Georgia", size=34,
           bold=True, color=DARK)
    _texto(s, "mudança casa−fora\ncom efeitos fixos de equipe",
           0.75, 2.2, 2.5, 0.7, size=12, color=TEXT)
    _texto(s, "IC 95% −0,03 a +0,72", 0.75, 3.0, 2.5, 0.35,
           size=13, bold=True, color=MUTED)
    _texto(s, "inclui zero:\nsugestivo, não conclusivo", 0.75, 3.4, 2.5, 0.7,
           size=11, color=MUTED)
    _cartao(s, 3.65, 1.35, 2.9, 2.95)
    _texto(s, "2019 → 2020", 3.85, 1.5, 2.5, 0.45, font="Georgia", size=20,
           bold=True, color=DARK)
    _texto(s, "−0,18  →  +0,11", 3.85, 2.05, 2.5, 0.5, font="Georgia", size=22,
           bold=True, color=TEXT)
    _texto(s, "mudança bruta +0,29\n16 equipes comuns: +0,34 (IC −0,04 a +0,72)",
           3.85, 2.65, 2.5, 1.2, size=11, color=MUTED)
    _cartao(s, 6.75, 1.35, 2.7, 2.95, fill=DARK, line=None)
    _texto(s, "O limite", 6.95, 1.5, 2.3, 0.4, font="Georgia", size=18,
           bold=True, color=GOLD)
    _texto(s,
           "2020 concentra pandemia, calendário e protocolos; VAR já existia.\n\n"
           "Cartões refletem arbítrio e comportamento do jogador; faltam pênaltis.",
           6.95, 2.0, 2.3, 2.1, size=11, color=DARK_TEXT, spacing=1.15)
    _texto(s, "A arbitragem fica mensurável, mas não identificada causalmente.",
           0.7, 4.55, 8.8, 0.35, size=12, bold=True, color=DARK)


def _dois_anos(prs):
    s = _slide(prs, "Dois anos, duas notas de método", 12)
    _cartao(s, 0.55, 1.4, 4.3, 3.4)
    _texto(s, "2016 — 379 jogos", 0.75, 1.55, 3.9, 0.5, font="Georgia",
           size=20, bold=True, color=DARK)
    _texto(s,
           "•  Chapecoense × Atlético-MG (rod. 38) cancelada\n"
           "•  Tragédia do voo; sem imputação de placar\n"
           "•  Caso documentado na metodologia",
           0.75, 2.15, 3.9, 2.4, size=14, spacing=1.2)
    _cartao(s, 5.15, 1.4, 4.25, 3.4)
    _texto(s, "2020 — Pollard 60,2%", 5.35, 1.55, 3.85, 0.5, font="Georgia",
           size=20, bold=True, color=DARK)
    _texto(s,
           "•  Temporada até 25/02/2021, sem torcida\n"
           "•  VAR estreia em 2019\n"
           "•  Calendário atípico",
           5.35, 2.15, 3.85, 2.4, size=14, spacing=1.2)


def _limitacoes(prs):
    s = _slide(prs, "Limitações declaradas", 13)
    _texto(s,
           "•  Observacional: placar + mando nominal; nenhuma leitura causal.\n"
           "•  Torcida aproximada pelo público externo; arbitragem só pela identidade "
           "(sem cartões/pênaltis).\n"
           "•  Contexto por proxies: distância, estádio, descanso e tabela; clima e "
           "elenco não medidos.\n"
           "•  Público: 2008 parcial (163/380) e 2024 completado pelo FBref; "
           "2020–2021 com portões fechados.\n"
           "•  O dashboard é ferramenta de exploração analítica, não modelo de previsão.",
           0.7, 1.45, 8.6, 3.2, size=14, spacing=1.25)
    _texto(s,
           "A conclusão é multifatorial e descritiva: associações modestas + "
           "resíduo grande.",
           0.7, 4.55, 8.6, 0.4, size=13, bold=True, color=DARK)


def _conclusao(prs):
    s = _slide(prs, "Conclusão", 14, dark=True)
    _texto(s,
           "Jogar em casa foi vantagem em todas as 19 temporadas: "
           "Pollard de 63,7%, oscilando entre 58,2% e 69,5%.",
           0.9, 1.5, 8.4, 1.35, font="Georgia", size=21, color=DARK_TEXT)
    _texto(s,
           "Contribuição: série anual longa e homogênea + fluxo reproduzível "
           "auditado + dashboard reutilizável.",
           0.9, 2.95, 8.4, 0.9, size=16, color=GOLD)
    _texto(s,
           "7.219 partidas  •  114 testes  •  validação 99,96%  •  11 tabelas / 13 figuras",
           0.9, 3.95, 8.4, 0.35, size=12, color=DARK_TEXT)
    _texto(s, "github.com/EmiyaKiritsugu3/TCC", 0.9, 4.3, 8.4, 0.35,
           size=13, color=DARK_MUTED)


def _anexo(prs):
    s = _slide(prs, "Anexo — resultados por temporada", 16)
    _imagem(s, FIG / "fig2_pollard_temporadas.png", 0.55, 1.3, 5.9, 3.05)
    _texto(s, "Tabela completa no CSV.", 6.7, 1.4, 2.6, 0.35,
           size=14, bold=True, color=DARK)
    _texto(s, "Demo ao vivo:", 6.7, 1.85, 2.6, 0.3, size=13, bold=True, color=DARK)
    _texto(s,
           "•  Visão geral → filtro 2020\n"
           "•  Aba Equipes (Flamengo 2019)\n"
           "•  Aba Contexto (clássico/distância)\n"
           "•  Metodologia e qualidade",
           6.7, 2.25, 2.6, 2.0, size=13, spacing=1.2)


def build() -> None:
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)
    prs.core_properties.title = (
        "Vantagem de jogar em casa — Brasileirão Série A (2006–2024)"
    )
    prs.core_properties.author = "José Inamar de Medeiros Júnior"
    _titulo(prs)
    _problema(prs)
    _metodo(prs)
    _geral(prs)
    _evolucao(prs)
    _nivel(prs)
    _gols(prs)
    _contexto(prs)
    _publico(prs)
    _cartoes_serie(prs)
    _cartoes_metodo(prs)
    _dois_anos(prs)
    _limitacoes(prs)
    _conclusao(prs)
    _matriz(prs)
    _anexo(prs)
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    prs.save(SAIDA)
    print(f"ok: {len(prs.slides)} slides -> {SAIDA}")


if __name__ == "__main__":
    build()
