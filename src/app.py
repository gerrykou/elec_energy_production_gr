import logging
import xlrd


def read_xls(xls_filepath: str) -> dict:
    '''Read an xls file, return a dictionary with keys()=[sheet_name, content]'''
    f = xlrd.open_workbook(xls_filepath)
    logging.debug(f'Worksheet name(s): {f.sheet_names()}')

    sh = f.sheet_by_index(1) # select the 2nd sheet
    logging.debug(f'{sh.name}, {sh.nrows}, {sh.ncols}')

    file_content = []
    for rx in range(sh.nrows):
        logging.debug(sh.row(rx))
        file_content.append(sh.row(rx))
    logging.debug(file_content)

    output_dict = {"sheet_name":sh.name, "content":file_content}
    logging.debug(f'output_dict= {output_dict}')
    # print("Cell D30 is {0}".format(sh.cell_value(rowx=29, colx=3)))
    return output_dict

def filter_list(data: list):
    print(type(data[5][1]))
    my_str = str(data[5][1])
    print(my_str)
    # print(data[5][1])
    if 'text' in my_str:
        print(data[5][1])

if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)

    xls_filename = '20220430_SystemRealizationSCADA_01.xls'
    folder = 'data'
    filepath = f'{folder}/{xls_filename}'
    data_dict = read_xls(filepath)
    filter_list(data_dict['content'])
