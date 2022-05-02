import logging
import xlrd


def read_xls(xls_filepath: str) -> dict:
    '''Read an xls file, return a dictionary with keys()=[sheet_name, content]'''
    f = xlrd.open_workbook(xls_filepath)
    logging.debug(f'Worksheet name(s): {f.sheet_names()}')

    sh = f.sheet_by_index(1) # selects the 2nd sheet
    logging.debug(f'{sh.name}, {sh.nrows}, {sh.ncols}')

    file_content = []
    for rx in range(sh.nrows):
        file_content.append(sh.row(rx))
    # logging.debug(file_content)

    output_dict = {"sheet_name":sh.name, "content":file_content}
    # print("Cell D30 is {0}".format(sh.cell_value(rowx=29, colx=3)))
    return output_dict

def test_content(data: list):
    # TODO a dictionary {[row,col]:'known_value', [50,1]:'TOTAL LIGNITE'}
    row = 51
    col = 1
    cell_value = _get_cell_value(row, col, data)
    if cell_value == 'TOTAL LIGNITE':
        print(cell_value)
    else:
        logging.error(f'TOTAL LIGNITE, not found in {data[row][col]}')

def _get_cell_value(row: int, col: int, data: list):
    cell = str(data[row][col])
    cell_list = cell.split(':')
    cell_value = cell_list[1].strip("'")
    return cell_value

def parse_hours(data: list):
    '''Return hours list'''
    hours = []
    for i in range(2,26):
        cell_value = _get_cell_value(34, i, data)
        hours.append(cell_value)
    return hours

def get_sum_lignite(data: list):
    cell = str(data[51][26])
    cell_list = cell.split(':')
    cell_value = cell_list[1].strip("'")
    sum_lignite = cell_value
    logging.debug(f'sum_lignite:{sum_lignite}')
    return sum_lignite


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    xls_filename = '20220430_SystemRealizationSCADA_01.xls'
    folder = 'data'
    filepath = f'{folder}/{xls_filename}'
    data_dict = read_xls(filepath)
    test_content(data_dict['content'])
    hours_list = parse_hours(data_dict['content'])
    sum_lignite = get_sum_lignite(data_dict['content'])
