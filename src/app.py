import logging
import xlrd
import csv
from itertools import zip_longest

from typing import Any, Dict, List, Tuple

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
    #self.sum_lignite = _get_cell_value(51, 26, data) #take row,col from known_values dict {"sum_lignite":[row,col]}

def parse_row_to_list(row: int , col_start: int, col_end: int, data: list) -> List:
    output = []
    for i in range(col_start,col_end):
        cell_value = _get_cell_value(row, i, data)
        output.append(cell_value)
    return output

# def export_to_csv(self, filename):
#     with open(filename , mode="w") as csv_file:
#         fieldnames = ["date_month", "posts_sum", "comments_sum"]
#         writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#         writer.writeheader()
#         for date, sum in self.calculate_monthly_stats().items():
#             writer.writerow({ "date_month" : date , "posts_sum": sum["posts_sum"], "comments_sum": sum["comments_sum"]})
#     return None

def write_to_csv(filepath: str, data_lists: List):
    export_data = zip_longest(*data_lists, fillvalue = '')
    with open(filepath , mode="w") as csv_file:
        wr = csv.writer(csv_file)
        wr.writerows(export_data)  

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    xls_filename = '20220430_SystemRealizationSCADA_01.xls'
    date = xls_filename[:8]

    folder = 'data'
    filepath = f'{folder}/{xls_filename}'
    sheet_number = 1 # 1 is the 2nd worksheet
    data_dict = read_xls(filepath, sheet_number)
    validate_content(data_dict['content'], expected_labels)

    index_list = parse_row_to_list(row=4 , col_start=1, col_end=26, data=data_dict['content']) # col_end=27 if SUM want to be included
    print(index_list)

    lignite_row = parse_row_to_list(row=51 , col_start=1, col_end=26, data=data_dict['content'])
    print(lignite_row)

    gas_row = parse_row_to_list(row=83 , col_start=1, col_end=26, data=data_dict['content'])
    res_row = parse_row_to_list(row=187 , col_start=1, col_end=26, data=data_dict['content'])

    data_lists = (index_list, lignite_row, gas_row, res_row)
    output_folder = 'data/output'
    csv_filepath = f'{output_folder}/{date}.csv'
    write_to_csv(csv_filepath, data_lists)
