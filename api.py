
import os
import requests
import mimetypes

UPLOAD_HEADERS = {
    'X-File-Parse': 'true'
}

API_ENDPOINT = 'https://dev-100-api.huntflow.ru'

class API:

    def __init__(self, token):

        self.authtoken = token
        self.headers = {'Authorization':f'Bearer {self.authtoken}'}
        self.account_id = 6

    def get_statuses_ids_mapping(self):

        statuses_ids = {}

        statuses = self.send(api_method = 'vacancy/statuses')['items']

        for item in statuses:

            statuses_ids.update({item['name']:item['id']})

        return statuses_ids

    def get_vacancies_ids_mapping(self):

        vacancies_ids = {}

        vacancies = self.send(api_method = 'vacancy/statuses')['items']

        for item in vacancies:

            vacancies_ids.update({item['name']:item['id']})

        return vacancies_ids

    def send(self, api_method, method = 'get', extraheaders = None, files = None, json = None):

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

        r = method(f'{API_ENDPOINT}/account/{self.account_id}/{api_method}', headers = headers, files = files, json = json)

        r.raise_for_status()

        return r.json()

    def add_candidate(self, candidate):

        data = self.send(method = 'post', api_method = 'applicants', json = candidate)

        return data

    def upload_resume(self, file_path):

        file_name = os.path.split(file_path)[1]

        file_type = mimetypes.guess_type(file_path)[0]

        with open(file_path, 'rb') as f:

            data = self.send('upload', method = 'post', extraheaders = [UPLOAD_HEADERS], files = {'file':(file_name, f, file_type)})

        return data