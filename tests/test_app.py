import sys
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

RAIZ = Path(__file__).resolve().parent.parent
PROCESSED = RAIZ / "data" / "processed" / "matches_processed.csv"

pytestmark = pytest.mark.skipif(
    not PROCESSED.exists(), reason="rode scripts/build_processed.py"
)


def test_aba_equipes_filtra_temporada_e_flamengo_2019():
    at = AppTest.from_file(str(RAIZ / "app.py"), default_timeout=60).run()
    assert not at.exception

    at.selectbox(key="temporada").select(2006).run()
    assert "America-MG" not in at.selectbox(key="equipe").options

    at.selectbox(key="temporada").select(2019).run()
    at.selectbox(key="equipe").select("Flamengo").run()
    m = {x.label: x.value for x in at.metric}
    assert m["Flamengo em casa"] == "53 pts"
    assert m["Flamengo fora"] == "37 pts"
    assert m["Total"] == "90 pts"
    assert m["Jogos"] == "38"


def test_aba_equipes_respeita_filtro_global():
    at = AppTest.from_file(str(RAIZ / "app.py"), default_timeout=60).run()
    at.sidebar.multiselect[0].set_value([2019]).run()
    assert at.selectbox(key="temporada").options == ["2019"]
    assert "America-MG" not in at.selectbox(key="equipe").options
    assert not at.exception
