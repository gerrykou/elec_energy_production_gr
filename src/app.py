#!/usr/bin/env python3 
import logging
import xlrd
import csv
from itertools import zip_longest
from pathlib import Path
from typing import Dict, List, Tuple

from helpers import list_of_content # test breaks when implemented

expected_labels = {
    'NET LOAD':(10, 1),
    'TOTAL IMPORTS':(24, 1),
    'TOTAL EXPORTS':(30, 1),
    'EXPORTS-IMPORTS':(31,1),
    'TOTAL LIGNITE':(51, 1),
    'TOTAL GAS':(83, 1),
    'TOTAL HYDRO':(106, 1),
    'TOTAL RES':(187, 1)
    } # TODO {{"label":'NET LOAD',"row":10,"col":1},{"label":'TOTAL IMPORTS',"row":24,"col":1}}

def read_xls(xls_filepath: str, sheet_number: int) -> Dict:
    '''Read an xls file, return a dictionary with keys()=[sheet_name, content]'''
    with xlrd.open_workbook(xls_filepath) as f:
        logging.debug(f'Worksheet name(s): {f.sheet_names()}')
        # f.sheet_by_name()

        sh = f.sheet_by_index(sheet_number)
        logging.debug(f'{sh.name}, {sh.nrows}, {sh.ncols}')

        file_content = []
        for rx in range(sh.nrows):
            row_content = []
            file_content.append(row_content)
            for cx in range(sh.ncols):
                row_content.append(sh.cell_value(rowx=rx, colx=cx))

        # logging.debug(file_content)
        output_dict = {"sheet_name":sh.name, "content":file_content, "nrows":sh.nrows , "ncols":sh.ncols }
    return output_dict

def validate_content(data: list, expected_labels: Dict[str, Tuple]):
    for item in expected_labels.items():
        label = item[0]
        row = item[1][0]
        col = item[1][1]
        # logging.debug(f'label:{label}, row:{row}, col:{col}')
        cell_value = _get_cell_value(row, col, data)
        if cell_value == label:
            pass
        else:
            raise Exception(f'{label}, not found in row:{row}, col:{col}, {data[row][col]}')
    return True

def _get_cell_value(row: int, col: int, data: list):
    cell_value = data[row][col]
    return cell_value

def parse_row_to_list(row: int, col_start: int, col_end: int, data: list, new_header: str='') -> List:
    output = []
    for i in range(col_start,col_end):
        if i == 1 and new_header != '':
            cell_value = new_header # replace existing header with new_header
        else:
            cell_value = _get_cell_value(row, i, data)
        output.append(cell_value)
    return output

def _write_to_csv(filepath: str, data_lists: List):
    ''' Write lists in csv as columns'''
    export_data = zip_longest(*data_lists, fillvalue = '')
    with open(filepath , mode="w") as csv_file:
        wr = csv.writer(csv_file)
        wr.writerows(export_data)  

def export_daily_production(folder, output_folder, date, data_lists):
    csv_file_dir = f'{folder}/{output_folder}/{date}'
    p = Path(csv_file_dir)
    p.mkdir(parents=True,exist_ok=True)
    csv_filepath = f'{csv_file_dir}/{date}_daily_production.csv'
    _write_to_csv(csv_filepath, data_lists)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    xls_filename = '20220430_SystemRealizationSCADA_01.xls'
    date = xls_filename[:8]

    folder = 'data'
    filepath = f'{folder}/{xls_filename}'
    sheet_number = 1 # 1 is the 2nd worksheet
    data_dict = read_xls(filepath, sheet_number)
    validate_content(data_dict['content'], expected_labels)

    # output_dict_of_lists = {}
    # for i in list_of_content:
    #     output_dict_of_lists[f"{i['index']}"] = parse_row_to_list(i['row'],i['col_start'],i['col_end'],data_dict['content'])
    # print(output_dict_of_lists)

    data_lists = []
    for i in list_of_content:
        # data_lists.append(parse_row_to_list(i['row'], i['col_start'], i['col_end'], data_dict['content'], i['new_header']))
        col_start = 1
        col_end =26
        data_lists.append(parse_row_to_list(i['row'], col_start, col_end, data_dict['content'], i['new_header']))
    print(data_lists)

    output_folder = 'output'
    export_daily_production(folder, output_folder, date, data_lists)
