import pytest

import src.app as app

# TEST FUNCTIONS
def test_read_xls():
    my_file = 'test.xls'
    actual_output = app.read_xls(my_file)
    expected_output = 'expected string'
    assert actual_output == expected_output

