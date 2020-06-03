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


class API:

    def __init__(self, token):

        self.authtoken = token
        self.headers = {'Authorization':f'Bearer {self.authtoken}'}
        self.account_id = 6
        self.vacancies_ids = {}
        self.statuses_ids = {}
        self.statuses_ru_to_api = {
            'Отправлено письмо': 'Contacted',
            'Интервью с HR': 'HR interview',
            'Выставлен оффер': 'Offered',
            'Отказ': 'Declined'
        }

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

    wb = openpyxl.load_workbook(fr'{path}')
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

    api = API(ARGS.token)