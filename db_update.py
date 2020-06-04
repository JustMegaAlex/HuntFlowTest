import sys
import os
import requests
import openpyxl
import argparse
import re
import shutil
import filetype
import mimetypes

ADD_CANDIDATE_FIELDS = [
    'last_name', 
    'first_name', 
    'middle_name', 
    'phone',
    'email',
    'position',
    'company',
    'money',
    'birthday_day',
    'birthday_month',
    'birthday_year',
    'photo'
]

UPLOAD_HEADERS = {
    'X-File-Parse': 'true'
}

STATUSES_MAPPING = {
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
    with open('token.txt') as f:
        token = f.read()
    ARGS = argparser.parse_args(rf'--path C:\repos\HuntFlowTest\test -t {token}'.split())

api = API(ARGS.token)

class API:

    def __init__(self, token):

        self.authtoken = token
        self.headers = {'Authorization':f'Bearer {self.authtoken}'}
        self.account_id = 6
        self.vacancies_ids = {}
        self.statuses_ids = {}

        vacancies = self.send(api_method = 'vacancies')['items']

        for item in vacancies:

            self.vacancies_ids.update({item['position']:item['id']})

        statuses = self.send(api_method = 'vacancy/statuses')['items']

        for item in statuses:

            self.statuses_ids.update({item['name']:item['id']})

    def send(self, api_method, method = 'get', extraheaders = None, files = None):

        if method == 'get':
            method = requests.get
        elif method == 'post':
            method = requests.post
        elif method == 'put':
            method = requests.put

        headers = self.headers.copy()

        if extraheaders:

            for h in extraheaders:
                
                headers.update(h)

        r = method(f'{API_ENDPOINT}/account/{self.account_id}/{api_method}', headers = headers, files = files)

        r.raise_for_status()

        return r.json()

    def add_candidate(self, candidate):

        file_path = candidate['local_file']

        data = {}

    def upload_resume(self, file_path):

        file_name = os.path.split(file_path)[1]

        file_type = mimetypes.guess_type(file_path)[0]

        with open(file_path, 'rb') as f:

            data = self.send('upload', method = 'post', extraheaders = [UPLOAD_HEADERS], files = {'file':(file_name, f, file_type)})

        return data


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

    resume_path = None

    for f in files:

        # fix wrong 'й' encoding
        f_check = re.sub(b'\xd0\xb8\xcc\x86'.decode('utf8'), 'й', f)

        if name.strip() in f_check.strip():

            resume_path = os.path.join(files_path, f)

            break

    return resume_path

def get_candidate_api_data(src_data):

    resume_text = 

    cand_data = {
        'last_name': src_data.get(),
        'first_name': src_data.get(),
        'middle_name': src_data.get(),
        'phone': src_data.get(),
        'email': src_data.get(),
        'position': src_data.get(),
        'company': src_data.get(),
        'money': src_data.get(),
        'birthday_day': src_data.get(),
        'birthday_month': src_data.get(),
        'birthday_year': src_data.get(),
        'photo': src_data.get(),
        'externals': [
            {
                'data': {
                    'body': 'Текст резюме\nТакой текст'
                },
                'auth_type': 'NATIVE',
                'files': [
                    {
                        'id': 12430
                    }
                ],
                'account_source': 208
            }
        ]
    }


if __name__ == '__main__':

    data = load_candidates_data(ARGS.path)

    for cand in data:

        data_from_file = api.upload_resume(cand['local_file'])

        print(data_from_file)