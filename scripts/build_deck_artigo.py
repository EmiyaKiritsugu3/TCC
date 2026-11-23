#!/usr/bin/env python3
"""Gera o deck de apresentação do artigo 2013–2024 (PPTX).

Uso:
  python3 scripts/build_deck_artigo.py
  libreoffice --headless --convert-to pdf --outdir apresentacao \
      apresentacao/apresentacao_artigo_2013_2024.pptx
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
SAIDA = RAIZ / "apresentacao" / "apresentacao_artigo_2013_2024.pptx"

DARK = RGBColor(0x0B, 0x3D, 0x2E)
DARK2 = RGBColor(0x12, 0x46, 0x35)
CREAM = RGBColor(0xF7, 0xF3, 0xE8)
GOLD = RGBColor(0xE9, 0xB4, 0x4C)
MOSS = RGBColor(0x6A, 0x99, 0x4E)
MOSS_LIGHT = RGBColor(0xDD, 0xE7, 0xD3)
TERRA = RGBColor(0xC8, 0x55, 0x3D)
TERRA_LIGHT = RGBColor(0xF1, 0xD8, 0xD0)
MOSS_TEXT = RGBColor(0x4F, 0x7A, 0x3A)
GOLD_DARK = RGBColor(0x8A, 0x5A, 0x00)
TERRA_DARK = RGBColor(0xA8, 0x43, 0x2F)
SALMON = RGBColor(0xF2, 0xB8, 0xA8)
CARD_DARK = RGBColor(0x17, 0x4C, 0x3A)
CARD_LINE = RGBColor(0x2E, 0x5B, 0x47)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TEXT = RGBColor(0x1F, 0x2A, 0x24)
MUTED = RGBColor(0x5F, 0x65, 0x5E)
LINE = RGBColor(0xDD, 0xD6, 0xC6)
DARK_TEXT = RGBColor(0xF7, 0xF3, 0xE8)
DARK_MUTED = RGBColor(0xB9, 0xC6, 0xB6)
FOOTER_LIGHT = RGBColor(0x57, 0x53, 0x4E)
FOOTER_DARK = RGBColor(0x9F, 0xB3, 0xA2)


def _bg(slide, cor: RGBColor) -> None:
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = cor


def _text(slide, texto, left, top, width, height, *, font="Calibri",
          size=14, bold=False, color=TEXT, align=PP_ALIGN.LEFT,
          anchor=MSO_ANCHOR.TOP, spacing=1.0, space_after=2):
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
        p.space_before = Pt(0)
        p.space_after = Pt(space_after)
        for run in p.runs:
            run.font.name = font
            run.font.size = Pt(size)
            run.font.bold = bold
            run.font.color.rgb = color
    return caixa


def _rect(slide, left, top, width, height, *, fill=WHITE, line=LINE,
          rounded=False, line_width=1.0):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    shp = slide.shapes.add_shape(shape_type, Inches(left), Inches(top),
                                 Inches(width), Inches(height))
    if rounded:
        shp.adjustments[0] = 0.08
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(line_width)
    shp.shadow.inherit = False
    return shp


def _image(slide, caminho: Path, left, top, max_w, max_h):
    with Image.open(caminho) as im:
        largura, altura = im.size
    escala = min(max_w / largura, max_h / altura)
    w, h = largura * escala, altura * escala
    slide.shapes.add_picture(
        str(caminho),
        Inches(left + (max_w - w) / 2),
        Inches(top + (max_h - h) / 2),
        Inches(w), Inches(h),
    )


def _kicker(slide, texto: str, *, color=MOSS_TEXT):
    _rect(slide, 0.55, 0.44, 0.07, 0.07, fill=color, line=None)
    _text(slide, texto.upper(), 0.72, 0.37, 8.5, 0.22, size=9.5, bold=True,
          color=color)


def _titulo(slide, texto: str, *, color=TEXT, size=29):
    _text(slide, texto, 0.55, 0.64, 9.0, 0.85, font="Georgia", size=size,
          bold=True, color=color, spacing=1.0)


def _rodape(slide, pagina: int, *, dark=False):
    cor = FOOTER_DARK if dark else FOOTER_LIGHT
    _text(slide, "Vantagem de jogar em casa · Série A 2013–2024",
          0.55, 5.27, 7.0, 0.2, size=8, color=cor)
    _text(slide, f"{pagina:02d}", 9.05, 5.27, 0.4, 0.2, size=8, color=cor,
          align=PP_ALIGN.RIGHT)


def _nota(slide, texto: str) -> None:
    slide.notes_slide.notes_text_frame.text = texto


def _slide(prs, kicker: str, titulo: str, pagina: int, *, dark=False):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _bg(slide, DARK if dark else CREAM)
    _kicker(slide, kicker, color=GOLD if dark else MOSS_TEXT)
    _titulo(slide, titulo, color=DARK_TEXT if dark else TEXT)
    _rodape(slide, pagina, dark=dark)
    return slide


def _stat(slide, left, top, width, height, valor, rotulo, *,
          value_size=28, color=DARK):
    _rect(slide, left, top, width, height, fill=WHITE, line=LINE, rounded=True)
    _text(slide, valor, left + 0.14, top + 0.12, width - 0.28, 0.55,
          font="Georgia", size=value_size, bold=True, color=color)
    _text(slide, rotulo, left + 0.14, top + 0.72, width - 0.28, height - 0.8,
          size=9.5, color=MUTED, spacing=1.0)


def _titulo_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _bg(slide, DARK)
    _rect(slide, 0.55, 1.0, 0.06, 3.2, fill=GOLD, line=None)
    _text(slide, "TCC · SISTEMAS DE INFORMAÇÃO · UFRN/CERES", 0.85, 0.55,
          8.4, 0.22, size=9, bold=True, color=DARK_MUTED)
    _text(slide, "Vantagem de jogar\nem casa na Série A", 0.85, 0.98, 6.2, 1.5,
          font="Georgia", size=39, bold=True, color=DARK_TEXT, spacing=1.0)
    _text(slide, "Uma análise baseada em modelos · 2013–2024", 0.85, 2.55,
          6.1, 0.35, size=16, color=GOLD)
    _text(slide, "José Inamar de Medeiros Júnior", 0.85, 4.28, 5.0, 0.25,
          size=11.5, color=DARK_TEXT)
    _text(slide, "Orientador: Prof. Dr. Francisco Marcio Barboza", 0.85, 4.58,
          5.2, 0.25, size=9, color=DARK_MUTED)

    ring = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(6.35), Inches(0.85),
                                  Inches(2.95), Inches(2.95))
    ring.fill.background()
    ring.line.color.rgb = MOSS
    ring.line.width = Pt(1.2)
    ring.shadow.inherit = False

    _text(slide, "63,0%", 6.45, 1.4, 2.75, 0.9, font="Georgia", size=48,
          bold=True, color=GOLD, align=PP_ALIGN.CENTER)
    _text(slide, "dos pontos ficaram\ncom o mandante", 6.55, 2.35, 2.55, 0.6,
          size=11.5, color=DARK_TEXT, align=PP_ALIGN.CENTER, spacing=1.05)
    _text(slide, "IC 95% 61,7–64,3", 6.55, 3.0, 2.55, 0.25, size=8.5,
          color=DARK_MUTED, align=PP_ALIGN.CENTER)
    _text(slide, "github.com/EmiyaKiritsugu3/TCC", 0.85, 5.15, 5.0, 0.2,
          size=8, color=DARK_MUTED)
    _nota(slide, 'Abrir com o número central: 63,0% dos pontos ficaram com o mandante. Dizer que o artigo fecha o recorte 2013–2024, com base MIT, e que o objetivo da conversa é avaliar estrutura, escopo e próximos passos.')
    return slide


def _slide_pergunta(prs):
    slide = _slide(prs, "A pergunta", "Três perguntas, uma base de 12 temporadas", 2)
    cartoes = [
        ("01", "Qual a magnitude?",
         "O mandante somou 63,0% dos pontos (IC 95% 61,7–64,3)."),
        ("02", "Mudou após 2018?",
         "65,0% (2013–18) → 61,0% (2019–24). Quebra em 2019."),
        ("03", "Quais canais?",
         "Público, viagem, cartões e arbitragem. O desenho é observacional."),
    ]
    x = [0.55, 3.5, 6.45]
    for (num, titulo, corpo), left in zip(cartoes, x):
        _rect(slide, left, 1.45, 2.85, 2.2, fill=WHITE, line=LINE, rounded=True)
        _text(slide, num, left + 0.15, 1.6, 0.6, 0.4, font="Georgia",
              size=24, bold=True, color=GOLD_DARK)
        _text(slide, titulo, left + 0.15, 2.05, 2.55, 0.4, font="Georgia",
              size=16, bold=True, color=TEXT, spacing=1.0)
        _text(slide, corpo, left + 0.15, 2.55, 2.55, 1.0, size=10.5,
              color=MUTED, spacing=1.08)
    _text(slide, "4.559 partidas · 12 temporadas · BrazilianFootball/Data (MIT)",
          0.55, 4.15, 9.0, 0.25, size=10, color=MUTED)
    _nota(slide, 'As três perguntas organizam o artigo: magnitude, mudança temporal e canais. A pergunta sobre canais é a mais delicada: o desenho é observacional e não identifica causalidade.')
    return slide


def _slide_dados(prs):
    slide = _slide(prs, "Dados", "Uma base aberta, validada e reproduzível", 3)
    dados = [
        ("4.559", "partidas"),
        ("12", "temporadas"),
        ("99,92%", "placares idênticos"),
        ("12/12", "campeões"),
    ]
    x = [0.55, 2.8, 5.05, 7.3]
    for (valor, rotulo), left in zip(dados, x):
        _stat(slide, left, 1.35, 2.1, 1.25, valor, rotulo, value_size=24)

    _text(slide, "Base: BrazilianFootball/Data (MIT)\n"
                 "Validação: OpenFootball (CC0)\n"
                 "Público e arbitragem: Base dos Dados/Transfermarkt\n"
                 "1 divergência de placar e 1 exceção de data documentadas.",
          0.55, 2.85, 4.4, 1.25, size=9.5, color=MUTED, spacing=1.15)

    # Linha do tempo em escala linear (2013–2024)
    y = 3.85
    x0, x1 = 5.2, 9.0
    escala = (x1 - x0) / (2024 - 2013)
    _rect(slide, x0, y, x1 - x0, 0.025, fill=MOSS, line=None)
    marcos = [(2013, "2013", False), (2019, "2019", False),
              (2020, "2020", True), (2024, "2024", False)]
    for ano, rotulo, acima in marcos:
        xm = x0 + (ano - 2013) * escala
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(xm - 0.06),
                                     Inches(y - 0.045), Inches(0.12), Inches(0.12))
        dot.fill.solid(); dot.fill.fore_color.rgb = MOSS
        dot.line.fill.background(); dot.shadow.inherit = False
        _text(slide, rotulo, xm - 0.25, y - 0.24 if acima else y + 0.12,
              0.5, 0.2, size=8, color=MUTED, align=PP_ALIGN.CENTER)
    _text(slide, "recorte 2013–2024", x0, y - 0.28, 1.6, 0.2, size=8,
          color=MUTED)
    _text(slide, "2019: quebra estimada · 2020: pandemia", x0, y + 0.42,
          3.8, 0.2, size=8, color=TERRA_DARK)
    _text(slide, "A base bruta não é redistribuída: o pipeline reconstrói o "
                 "recorte a partir do commit fixado.", 0.55, 4.72, 9.0, 0.3,
          size=9, color=MUTED)
    _nota(slide, 'Destacar a validação: 2.658 de 2.660 placares e 12/12 campeões. Mencionar que a base bruta não é redistribuída e que o pipeline reconstrói o recorte. A divergência de 2019 está documentada.')
    return slide


def _slide_metodos(prs):
    slide = _slide(prs, "Métodos", "Quatro camadas de evidência", 4)
    cartoes = [
        ("01", "Pollard",
         "Pontos do mandante / pontos totais.\nIC 95% por bootstrap de partidas.\n63,0% no período (IC 61,7–64,3)."),
        ("02", "Mudança de nível",
         "Regressão segmentada; quebra por mínimos quadrados.\nIC por cluster de temporada.\n65,0% → 61,0% (−4,0 p.p.; IC −6,6 a −0,9)."),
        ("03", "Poisson ataque–defesa",
         "log λ = μ + ataque − defesa + γ + temporada.\nSepara qualidade do efeito de casa.\nPrêmio: +56,5% → +37,7%."),
        ("04", "Variância",
         "Entre equipes vs. dentro de equipes/temporadas.\nICC = 2,2%.\n97,8% é variação dentro de equipes/temporadas."),
    ]
    pos = [(0.55, 1.35), (5.05, 1.35), (0.55, 3.02), (5.05, 3.02)]
    for (num, titulo, corpo), (left, top) in zip(cartoes, pos):
        _rect(slide, left, top, 4.35, 1.45, fill=WHITE, line=LINE, rounded=True)
        _text(slide, num, left + 0.15, top + 0.12, 0.45, 0.3, font="Georgia",
              size=15, bold=True, color=GOLD)
        _text(slide, titulo, left + 0.65, top + 0.1, 3.55, 0.3, size=13,
              bold=True, color=TEXT)
        _text(slide, corpo, left + 0.15, top + 0.55, 4.05, 0.8, size=9.5,
              color=MUTED, spacing=1.08)
    _text(slide, "Nenhum modelo identifica causalidade: o desenho é observacional.",
          0.55, 4.7, 9.0, 0.25, size=10.5, color=TERRA_DARK, bold=True)
    _nota(slide, 'Explicar em uma frase cada camada. O Poisson é o que separa qualidade das equipes do efeito de casa; a decomposição mostra que a vantagem é da liga, não de um clube.')
    return slide


def _slide_resultado1(prs):
    slide = _slide(prs, "Resultado 1", "A vantagem caiu a partir de 2019", 5)
    _text(slide, "63,0%", 0.55, 1.25, 2.2, 0.7, font="Georgia", size=34,
          bold=True, color=DARK)
    _text(slide, "dos pontos com o mandante", 0.55, 1.9, 3.0, 0.25, size=10,
          color=MUTED)
    _text(slide, "65,0% → 61,0%", 0.55, 2.45, 3.4, 0.5, font="Georgia",
          size=24, bold=True, color=DARK)
    _text(slide, "média 2013–2018 → 2019–2024", 0.55, 2.92, 3.5, 0.25,
          size=9.5, color=MUTED)
    _text(slide, "−4,0 p.p.", 0.55, 3.45, 2.4, 0.5, font="Georgia", size=27,
          bold=True, color=TERRA)
    _text(slide, "IC 95% −6,6 a −0,9 · quebra estimada em 2019", 0.55, 3.95,
          4.0, 0.25, size=9.5, color=MUTED)

    _rect(slide, 4.05, 1.15, 5.4, 3.0, fill=WHITE, line=LINE, rounded=True)
    _image(slide, FIG / "deck_serie_pollard.png", 4.15, 1.25, 5.2, 2.75)
    _text(slide, "Figura 1 · Pollard por temporada; faixa = IC 95%.",
          4.15, 3.95, 5.2, 0.2, size=7.5, color=MUTED, align=PP_ALIGN.CENTER)
    _text(slide, "Fonte: BrazilianFootball/Data (MIT); cálculos do autor. "
                 "A queda não é só no índice: aparece também em gols.",
          0.55, 4.7, 9.0, 0.25, size=9, color=MUTED)
    _nota(slide, 'O número de 63,0% é a média do período. A queda de 4,0 p.p. é o resultado central; a quebra em 2019 é estimada, não imposta. O IC −6,6 a −0,9 mostra que a queda é negativa e precisa.')
    return slide


def _slide_resultado2(prs):
    slide = _slide(prs, "Resultado 2", "Em gols, o prêmio de casa caiu 12,0%", 6)
    _rect(slide, 0.55, 1.3, 3.65, 2.0, fill=WHITE, line=LINE, rounded=True)
    _text(slide, "2013–2018", 0.75, 1.45, 3.2, 0.2, size=8.5, bold=True,
          color=MUTED)
    _text(slide, "+56,5%", 0.75, 1.72, 3.2, 0.55, font="Georgia", size=31,
          bold=True, color=MOSS)
    _text(slide, "log 0,448 · IC 0,397–0,500", 0.75, 2.55, 3.2, 0.2, size=9,
          color=MUTED)
    _text(slide, "gols esperados do mandante\nvs. visitante", 0.75, 2.85, 3.2,
          0.4, size=9, color=MUTED, spacing=1.05)

    _rect(slide, 5.75, 1.3, 3.65, 2.0, fill=WHITE, line=LINE, rounded=True)
    _text(slide, "2019–2024", 5.95, 1.45, 3.2, 0.2, size=8.5, bold=True,
          color=MUTED)
    _text(slide, "+37,7%", 5.95, 1.72, 3.2, 0.55, font="Georgia", size=31,
          bold=True, color=TERRA)
    _text(slide, "log 0,320 · IC 0,270–0,371", 5.95, 2.55, 3.2, 0.2, size=9,
          color=MUTED)
    _text(slide, "mesmo controle de ataque,\ndefesa e temporada", 5.95, 2.85,
          3.2, 0.4, size=9, color=MUTED, spacing=1.05)

    arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(4.35),
                                   Inches(2.15), Inches(1.25), Inches(0.38))
    arrow.fill.solid(); arrow.fill.fore_color.rgb = TERRA
    arrow.line.fill.background(); arrow.shadow.inherit = False
    _text(slide, "variação relativa", 4.25, 1.45, 1.45, 0.2, size=7.5,
          color=MUTED, align=PP_ALIGN.CENTER)
    _text(slide, "−12,0%", 4.3, 1.68, 1.35, 0.3, font="Georgia", size=14,
          bold=True, color=TERRA, align=PP_ALIGN.CENTER)

    _text(slide, "Multiplicador de gols do mandante: 1,565 → 1,377 · "
                 "IC −18,1% a −5,5%", 0.55, 3.55, 9.0, 0.3, size=12,
          bold=True, color=TEXT)
    _text(slide, "Poisson ataque–defesa com efeitos de temporada; N = 4.559 "
                 "partidas (9.118 observações de gols).", 0.55, 4.0, 9.0, 0.4,
          size=9.5, color=MUTED)
    _text(slide, "A queda sobrevive ao controle de qualidade das equipes.",
          0.55, 4.65, 9.0, 0.25, size=9, color=MUTED)
    _nota(slide, 'O Poisson confirma a queda em espaço de gols: o prêmio cai de +56,5% para +37,7%. O multiplicador cai 12,0%. Isso afasta a explicação de que a queda é só composição de equipes.')
    return slide


def _slide_resultado3(prs):
    slide = _slide(prs, "Resultado 3", "A vantagem é da liga, não de um clube", 7)
    _text(slide, "2,2%", 0.55, 1.25, 2.6, 0.9, font="Georgia", size=46,
          bold=True, color=TERRA)
    _text(slide, "da variância está entre equipes", 0.55, 2.1, 3.4, 0.25,
          size=10, color=MUTED)
    _text(slide, "97,8% é variação dentro de equipes/temporadas", 0.55, 2.45, 3.6, 0.25,
          size=10, color=MUTED)
    _text(slide, "Não é um traço permanente de clube.", 0.55, 2.95, 3.5, 0.3,
          size=12, bold=True, color=DARK)
    _text(slide, "n = 240 equipe-temporadas · 36 clubes", 0.55, 3.35, 3.5, 0.25,
          size=8.5, color=MUTED)

    _rect(slide, 5.15, 1.3, 4.3, 1.05, fill=WHITE, line=LINE, rounded=True)
    _text(slide, "ρ = 0,08", 5.3, 1.42, 1.6, 0.4, font="Georgia", size=22,
          bold=True, color=MUTED)
    _text(slide, "público × vantagem de casa", 7.05, 1.45, 2.25, 0.25,
          size=9.5, color=MUTED)
    _text(slide, "associação fraca", 7.05, 1.72, 2.25, 0.2, size=8.5,
          color=MUTED)

    _rect(slide, 5.15, 2.55, 4.3, 1.05, fill=WHITE, line=LINE, rounded=True)
    _text(slide, "ρ = 0,41", 5.3, 2.67, 1.6, 0.4, font="Georgia", size=22,
          bold=True, color=DARK)
    _text(slide, "público × pontos", 7.05, 2.7, 2.25, 0.25, size=9.5,
          color=MUTED)
    _text(slide, "associação forte", 7.05, 2.97, 2.25, 0.2, size=8.5,
          color=MUTED)

    _text(slide, "2020: 60,2% · 2022–24: 60,6%", 5.15, 3.85, 4.3, 0.25,
          size=11, bold=True, color=DARK)
    _text(slide, "O retorno da torcida não restaurou o patamar anterior.",
          5.15, 4.15, 4.3, 0.4, size=9.5, color=MUTED, spacing=1.05)
    _text(slide, "O público separa clubes grandes de pequenos, não explica a "
                 "vantagem dentro do mesmo clube.", 0.55, 4.55, 4.3, 0.6,
          size=9, color=MUTED, spacing=1.05)
    _text(slide, "Fonte: Base dos Dados/Transfermarkt; cálculos do autor.",
          0.55, 5.0, 9.0, 0.18, size=7.5, color=MUTED)
    _nota(slide, 'O ICC de 2,2% mostra que a vantagem é predominantemente da liga. O público tem correlação fraca com a vantagem e forte com pontos: ele separa clubes grandes, não explica a vantagem dentro do clube.')
    return slide


def _slide_canais(prs):
    slide = _slide(prs, "Canais", "Cartões e pênaltis: sinal, não prova", 8)
    _rect(slide, 0.55, 1.25, 4.2, 1.5, fill=WHITE, line=LINE, rounded=True)
    _text(slide, "CARTÕES AMARELOS", 0.75, 1.38, 3.6, 0.2, size=8.5, bold=True,
          color=MUTED)
    _text(slide, "+0,35", 0.75, 1.62, 2.0, 0.45, font="Georgia", size=28,
          bold=True, color=MOSS)
    _text(slide, "diferença-em-diferenças 2019→2020", 0.75, 2.15, 3.6, 0.2,
          size=8.5, color=MUTED)
    _text(slide, "IC 95% −0,03 a +0,72", 0.75, 2.42, 3.6, 0.2, size=9,
          color=MUTED)
    _rect(slide, 3.35, 1.38, 1.3, 0.3, fill=MOSS_LIGHT, line=None, rounded=True)
    _text(slide, "sugestivo", 3.35, 1.42, 1.3, 0.2, size=8, bold=True,
          color=DARK, align=PP_ALIGN.CENTER)

    _rect(slide, 0.55, 2.95, 4.2, 1.5, fill=WHITE, line=LINE, rounded=True)
    _text(slide, "PÊNALTIS CONVERTIDOS", 0.75, 3.08, 3.6, 0.2, size=8.5,
          bold=True, color=MUTED)
    _text(slide, "+0,05", 0.75, 3.32, 2.0, 0.45, font="Georgia", size=28,
          bold=True, color=DARK)
    _text(slide, "piloto 2019–2020 · n = 760", 0.75, 3.85, 3.6, 0.2, size=8.5,
          color=MUTED)
    _text(slide, "IC 95% −0,06 a +0,15", 0.75, 4.1, 3.6, 0.2, size=9,
          color=MUTED)

    _rect(slide, 5.0, 1.25, 4.45, 2.7, fill=WHITE, line=LINE, rounded=True)
    _image(slide, FIG / "deck_cartoes.png", 5.1, 1.35, 4.25, 2.35)
    _text(slide, "Figura 2 · cartões casa−fora; faixa = IC 95%. "
                 "Fonte: BrazilianFootball/Data (MIT).",
          5.1, 3.75, 4.25, 0.2, size=6.8, color=MUTED, align=PP_ALIGN.CENTER)
    _text(slide, "2020 mistura pandemia, calendário e protocolos. O sinal é "
                 "compatível com canal arbitral, mas não é prova causal.",
          0.55, 4.62, 9.0, 0.45, size=9.5, color=TERRA_DARK, spacing=1.05)
    _nota(slide, 'Cartões vão na direção esperada, mas o IC inclui zero. Pênaltis convertidos não mostram mudança detectável. A leitura é sugestiva, não causal; 2020 mistura pandemia, calendário e protocolos.')
    return slide


def _slide_conclusoes(prs):
    slide = _slide(prs, "Conclusões", "Evidência vs. especulação", 9, dark=True)
    _rect(slide, 0.55, 1.35, 4.35, 2.35, fill=CARD_DARK, line=CARD_LINE, rounded=True)
    _text(slide, "SUSTENTA", 0.75, 1.5, 3.9, 0.25, size=9, bold=True, color=MOSS_LIGHT)
    linhas_ok = [
        "Vantagem grande: 63,0% (61,7–64,3)",
        "Queda de 4,0 p.p., robusta em gols",
        "Fenômeno da liga: ICC 2,2%",
        "Público é canal fraco; cartões são sugestivos",
    ]
    _text(slide, "\n".join(f"✓  {l}" for l in linhas_ok), 0.75, 1.85, 3.9, 1.7,
          size=11.5, color=DARK_TEXT, spacing=1.25)

    _rect(slide, 5.15, 1.35, 4.3, 2.35, fill=CARD_DARK, line=CARD_LINE, rounded=True)
    _text(slide, "NÃO SUSTENTA", 5.35, 1.5, 3.9, 0.25, size=9, bold=True,
          color=SALMON)
    linhas_nao = [
        "Culpar VAR, torcida ou arbitragem",
        "Tratar 2019 como causa",
        "Rankear clubes por vantagem de casa",
        "Prever 2025 sem teste fora da amostra",
    ]
    _text(slide, "\n".join(f"×  {l}" for l in linhas_nao), 5.35, 1.85, 3.9, 1.7,
          size=11.5, color=DARK_TEXT, spacing=1.25)

    _text(slide, "A queda é real; a causa segue em aberto.", 0.55, 3.95, 9.0, 0.35,
          font="Georgia", size=17, bold=True, color=GOLD)
    _text(slide, "Leitura descritiva; sem identificação causal.", 0.55, 4.45,
          9.0, 0.2, size=8.5, color=DARK_MUTED)
    _nota(slide, 'Separar claramente o que a evidência sustenta do que seria especulação. A frase de fechamento é: a queda é real; a causa segue em aberto.')
    return slide


def _slide_proximos(prs):
    slide = _slide(prs, "Próximos passos", "O que falta para fechar o depósito",
                   10, dark=True)
    itens = [
        ("01", "Template oficial", "UFRN/CERES-BSI + ficha SISBI"),
        ("02", "Banca", "nomes, titulação, instituição e data"),
        ("03", "Escopo do artigo", "manter público e cartões ou só o núcleo?"),
        ("04", "Dashboard", "artefato complementar ou link de reprodutibilidade?"),
    ]
    pos = [(0.55, 1.35), (5.05, 1.35), (0.55, 2.7), (5.05, 2.7)]
    for (num, titulo, corpo), (left, top) in zip(itens, pos):
        _rect(slide, left, top, 4.3, 1.1, fill=DARK2, line=None, rounded=True)
        _text(slide, num, left + 0.15, top + 0.17, 0.45, 0.3, font="Georgia",
              size=14, bold=True, color=GOLD)
        _text(slide, titulo, left + 0.65, top + 0.12, 3.5, 0.3, size=12.5,
              bold=True, color=DARK_TEXT)
        _text(slide, corpo, left + 0.65, top + 0.47, 3.5, 0.5, size=9,
              color=DARK_MUTED, spacing=1.05)

    _text(slide, "Obrigado.", 0.55, 4.15, 3.0, 0.5, font="Georgia", size=28,
          bold=True, color=GOLD)
    _text(slide, "Fico à disposição para ajustar o que for necessário.",
          0.55, 4.7, 6.0, 0.25, size=10, color=DARK_MUTED)
    _text(slide, "github.com/EmiyaKiritsugu3/TCC", 6.5, 4.95, 3.0, 0.2,
          size=8, color=DARK_MUTED, align=PP_ALIGN.RIGHT)
    _nota(slide, 'Fechar pedindo o template, os dados da banca e as decisões sobre público/cartões e dashboard. Agradecer e abrir para perguntas.')
    return slide


def main() -> None:
    for nome in ("deck_serie_pollard.png", "deck_cartoes.png"):
        if not (FIG / nome).exists():
            raise SystemExit(
                f"figura ausente: {FIG / nome}; rode scripts/make_deck_figures.py"
            )
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)
    prs.core_properties.title = "Vantagem de jogar em casa na Série A (2013–2024)"
    prs.core_properties.author = "José Inamar de Medeiros Júnior"
    _titulo_slide(prs)
    _slide_pergunta(prs)
    _slide_dados(prs)
    _slide_metodos(prs)
    _slide_resultado1(prs)
    _slide_resultado2(prs)
    _slide_resultado3(prs)
    _slide_canais(prs)
    _slide_conclusoes(prs)
    _slide_proximos(prs)
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    prs.save(SAIDA)
    print(f"gravado em: {SAIDA}")


if __name__ == "__main__":
    main()
