import pytest

import src.app as app

# TEST FUNCTIONS
def test_read_xls():
    my_file = 'test/test.xls'
    sheet_number = 1
    actual_output = app.read_xls(my_file, sheet_number)
    expected_output = 'System_Production'
    assert actual_output['sheet_name'] == expected_output
    assert 'sheet_name' in actual_output.keys()
    assert 'content' in actual_output.keys()
    assert 'nrows' in actual_output.keys()
    assert 'ncols' in actual_output.keys()

def test_get_cell_value():
    my_file = 'test/test.xls'
    sheet_number = 1
    data = app.read_xls(my_file, sheet_number)['content']
    assert app._get_cell_value(10,1,data) == 'NET LOAD'
    assert app._get_cell_value(51,1,data) == 'TOTAL LIGNITE'
    assert app._get_cell_value(83,1,data) == 'TOTAL GAS'
    assert app._get_cell_value(106,1,data) == 'TOTAL HYDRO'
    assert app._get_cell_value(187,1,data) == 'TOTAL RES'

def test_validate_content():
    my_file = 'test/test.xls'
    sheet_number = 1
    data = app.read_xls(my_file, sheet_number)['content']
    known_labels = {
    'NET LOAD':(10, 1),
    'TOTAL IMPORTS':(24, 1),
    'TOTAL EXPORTS':(30, 1),
    'EXPORTS-IMPORTS':(31,1),
    'TOTAL LIGNITE':(51, 1),
    'TOTAL GAS':(83, 1),
    'TOTAL HYDRO':(106, 1),
    'TOTAL RES':(187, 1)
    }
    assert app.validate_content(data, known_labels) == True

def test_parse_row_to_list():
    my_file = 'test/test.xls'
    sheet_number = 1
    data = app.read_xls(my_file, sheet_number)['content']
    actual_output1 = app.parse_row_to_list(row=51 , col_start=1, col_end=26, data=data)
    expected_output1 = [
        'TOTAL LIGNITE', 204.0, 190.0, 191.0, 191.0, 191.0, 189.0, 190.0, 190.0, 189.0, 189.0, 187.0,
        192.0, 199.0, 200.0, 190.0, 190.0, 191.0, 195.0, 195.0, 199.0, 203.0, 219.0, 229.0, 204.0
        ]
    actual_output2 = app.parse_row_to_list(row=4 , col_start=1, col_end=26, data=data)
    expected_output2 = [
        '', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', 
        '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'
        ]
    assert actual_output1 == expected_output1
    assert actual_output2 == expected_output2

# TEST FAILURES
def test_rvalidate_content_error():
    my_file = 'test/test.xls'
    sheet_number = 1
    data = app.read_xls(my_file, sheet_number)['content']
    with pytest.raises(Exception):
        known_labels = {'wrong_value':(10, 1),}
        app.validate_content(data, known_labels)