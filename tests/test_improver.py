import pytest
import re
from main.improver import display_results, improve_code


# @pytest.mark.skip("TODO")
def test_if_functions_exist():
    assert display_results and improve_code

# @pytest.mark.skip("TODO")
def test_improve_code_theme():
    input_text = """str0 = W"orld'"""

    expected = r'str0 = "World"'
    actual = improve_code(input_text)

    assert bool(re.search(expected,actual))

# @pytest.mark.skip("TODO")
def test_display_results():
    try:
        input_text = "Here is something to display"
        display_results(input_text,5)
    except Exception as err:
        assert (False), "test_display_results didn't pass"