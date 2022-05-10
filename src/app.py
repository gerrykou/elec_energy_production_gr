#!/usr/bin/env python3 
import logging
import xlrd
import csv
import os
from itertools import zip_longest
from pathlib import Path
from typing import Dict, List, Tuple
import requests

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
    ''' Data quality check '''
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

def parse_row_to_list(row: int, col_start: int, col_end: int, data: list, date_str: str, new_header: str='') -> List:
    output = []
    for i in range(col_start,col_end):
        if i == 1 and new_header != '': # new_header is empty for hours row
            cell_value = new_header # replace existing header with new_header
        else:
            cell_value = _get_cell_value(row, i, data)
            if new_header == 'time': # create new datetime strings
                cell_value = _get_iso_datetime_str(date_str, int(cell_value)-1) # change hours from 01 - 24 to 00 - 23
        output.append(cell_value)
    return output

def _write_to_csv(filepath: str, data_lists: List):
    ''' Write lists in csv as columns'''
    export_data = zip_longest(*data_lists, fillvalue = '')
    with open(filepath , mode="w") as csv_file:
        wr = csv.writer(csv_file)
        wr.writerows(export_data)

def _get_iso_datetime_str(date: str, hrs: str):
    return f'{date}T{hrs}:00:00'

def export_daily_production(folder, output_folder, date, data_lists):
    csv_file_dir = f'{folder}/{output_folder}/{date}'
    p = Path(csv_file_dir)
    p.mkdir(parents=True,exist_ok=True)
    csv_filepath = f'{csv_file_dir}/{date}_daily_production.csv'
    _write_to_csv(csv_filepath, data_lists)

def _get_url(date_str: str, filecategory: str) -> str:
    ''' Return the download url '''
    operation_market_file_url = f'https://www.admie.gr/getOperationMarketFile?dateStart={date_str}&dateEnd={date_str}&FileCategory={filecategory}'
    r = requests.get(operation_market_file_url)
    try:
        d = r.json()
        url = d[-1]['file_path']
        return url
    except ValueError:
        print(f'{r.text} not a valid json format')
        

def _get_download(file_url: str, directory: str) -> str:
    ''' Download file in the directory, returns filepath '''
    # file url: https://www.admie.gr/sites/default/files/attached-files/type-file/2022/05/20220501_SystemRealizationSCADA_01.xls

    try:
        print(f'Downloading file from {file_url} ...')
        r = requests.get(file_url)
        dl_filename = file_url.split('/')[-1]
        file_path = f'{directory}/{dl_filename}'
        p = Path(directory)
        p.mkdir(parents=True,exist_ok=True)
        print(f'Saving file in {file_path} ...')
        with open(file_path, 'wb') as output:
            output.write(r.content)
        return file_path
    except:
        print(f'cannot access {file_url}')
        return False

def download_xls(date_str: str):
    folder = 'data'
    download_dir = f'{folder}/raw/{date_str}'
    filecategory = 'SystemRealizationSCADA' 

    url = _get_url(date_str, filecategory)

    _get_download(url, download_dir)

def xls_to_csv(date_str: str):
    folder = 'data'
    output_folder = 'output'

    download_dir = f'{folder}/raw/{date_str}'
    xls_filename = os.listdir(download_dir)[0]
    filepath = f'{download_dir}/{xls_filename}'

    sheet_number = 1 # 1 is the 2nd worksheet
    data_dict = read_xls(filepath, sheet_number)

    validate_content(data_dict['content'], expected_labels)

    data_lists = []
    for i in list_of_content:
        col_start = 1
        col_end =26
        data_lists.append(parse_row_to_list(i['row'], col_start, col_end, data_dict['content'], date_str, i['new_header']))

    export_daily_production(folder, output_folder, date_str, data_lists)

def main():
    date_str = '2022-05-05'
    download_xls(date_str)
    xls_to_csv(date_str)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # https://www.admie.gr/getOperationMarketFile?dateStart=2022-05-01&dateEnd=2022-05-01&FileCategory=SystemRealizationSCADA
    main()
