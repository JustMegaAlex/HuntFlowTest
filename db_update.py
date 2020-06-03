import sys
import requests
import openpyxl
import argparse

API_ENDPOINT = 'https://dev-100-api.huntflow.ru'

# handle external arguments
argparser = argparse.ArgumentParser()
argparser.add_argument('--token', '-t', required = True)
argparser.add_argument('--path', '-p', required = True)
ARGS = argparser.parse_args()

def load_candidates_data(path):

    field_names = {'position':1, 'name':2, 'money':3, 'comment':4, 'status_name':5}

    data = []

    wb = openpyxl.load_workbook(path)
    ws = wb.active
    row = 2
    cell_val = ws.cell(row, 1).value

    while cell_val:

        cand_data = {}

        cand_data['position'] = ws.cell(row, field_names['position']).value
        cand_data['money'] = ws.cell(row, field_names['money']).value
        cand_data['comment'] = ws.cell(row, field_names['comment']).value
        cand_data['status_name'] = ws.cell(row, field_names['status_name']).value
        name = ws.cell(row, field_names['name']).value.split()
        cand_data['first_name'] = name[0]
        cand_data['second_name'] = name[1]
        cand_data['middle_name'] = name[2] if len(name) == 3 else ''

        data.append(cand_data)
        row += 1
        cell_val = ws.cell(row, 1).value


    return data

if __name__ == "__main__":

    data = load_candidates_data(ARGS.path)

    print(data)