import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from charts import outcome_distribution
from formatting import num, pct, signed


def test_formatacao_pt_br():
    assert pct(49.0) == "49,0%"
    assert pct(63.66, 2) == "63,66%"
    assert pct(None) == "—"
    assert num(1.49) == "1,49"
    assert num(None) == "—"
    assert signed(0.49) == "+0,49"
    assert signed(-2) == "-2,00"


def test_grafico_usa_separador_pt_br():
    fig = outcome_distribution({"p_home": 49.0, "p_draw": 26.8, "p_away": 24.1})
    assert fig.layout.separators == ",."
