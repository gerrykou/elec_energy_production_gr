import pytest

import src.app as app

# TEST FUNCTIONS
def test_read_xls():
    my_file = 'test/test.xls'
    actual_output = app.read_xls(my_file)
    expected_output = 'System_Production'
    assert actual_output['sheet_name'] == expected_output
    assert 'sheet_name' in actual_output.keys()
    assert 'content' in actual_output.keys()

def test_get_cell_value():
    my_file = 'test/test.xls'
    data = app.read_xls(my_file)['content']
    actual_output = app._get_cell_value(51,1,data)
    expected_output = 'TOTAL LIGNITE'
    assert actual_output == expected_output
