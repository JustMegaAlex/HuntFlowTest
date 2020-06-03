import sys
import os
import requests
import openpyxl
import argparse
import re

STATUSES = {
    'Отправлено письмо': 'Contacted',
    'Интервью с HR': 'HR interview',
    'Выставлен оффер': 'Offered',
    'Отказ': 'Declined'
}

API_ENDPOINT = 'https://dev-100-api.huntflow.ru'

DBFILE = 'Тестовая база.xlsx'

# handle external arguments
argparser = argparse.ArgumentParser()
argparser.add_argument('--token', '-t', required = True)
argparser.add_argument('--path', '-p', required = True)

try:
    ARGS = argparser.parse_args()
except:
    ARGS = argparser.parse_args(r'--path C:\repos\HuntFlowTest\test -t 71e89e8af02206575b3b4ae80bf35b6386fe3085af3d4085cbc7b43505084482'.split())


class API:

    def __init__(self, token):

        self.authtoken = token
        self.headers = {'Authorization':f'Bearer {self.authtoken}'}
        self.account_id = 6
        self.vacancies_ids = {}
        self.statuses_ids = {}

        vacancies = self.__send__(api_method = 'vacancies')['items']

        for item in vacancies:

            self.vacancies_ids.update({item['position']:item['id']})

        statuses = self.__send__(api_method = 'vacancy/statuses')['items']

        for item in statuses:

            self.statuses_ids.update({item['name']:item['id']})

    def __send__(self, api_method, method = 'get', extraheaders = None):

        if method == 'get':
            method = requests.get
        elif method == 'post':
            method = requests.post
        elif method == 'put':
            method = requests.put

        headers = self.headers.copy()

        if extraheaders:

            headers.update(extraheaders)

        r = method(f'{API_ENDPOINT}/account/{self.account_id}/{api_method}', headers = headers)

        r.raise_for_status()

        return r.json()

    def add_candidate(self, data):

        pass

    def upload_resume(self, localpath):

        pass


def load_candidates_data(path):

    field_names = {'position':1, 'name':2, 'money':3, 'comment':4, 'status_name':5}
    data = []
    path = fr'{path}'
    xl_path = os.path.join(path, DBFILE)
    wb = openpyxl.load_workbook(xl_path)
    ws = wb.active
    row = 2
    cell_val = ws.cell(row, 1).value

    while cell_val:

        cand_data = {}

        cand_data['position'] = ws.cell(row, field_names['position']).value
        cand_data['money'] = ws.cell(row, field_names['money']).value
        cand_data['comment'] = ws.cell(row, field_names['comment']).value
        cand_data['status_name'] = ws.cell(row, field_names['status_name']).value
        name = ws.cell(row, field_names['name']).value
        name_list = name.split()
        cand_data['first_name'] = name_list[0]
        cand_data['second_name'] = name_list[1]
        cand_data['middle_name'] = name_list[2] if len(name_list) == 3 else ''
        # add resume file path if exists
        file_path = get_resume_local_path(path, name, cand_data['position'])
        cand_data['local_file'] = file_path

        data.append(cand_data)
        row += 1
        cell_val = ws.cell(row, 1).value

    return data

def get_resume_local_path(db_path, name, position):

    files_path = os.path.join(db_path, position)
    
    files = os.listdir(files_path)

    # fix wrong 'й' encoding
    files = [re.sub(b'\xd0\xb8\xcc\x86'.decode('utf8'), 'й', f) for f in files]

    resume_path = None

    for f in files:

        if name.strip() in f.strip():

            resume_path = os.path.join(files_path, f)

            break 

    return resume_path


if __name__ == "__main__":

    data = load_candidates_data(ARGS.path)

    api = API(ARGS.token)