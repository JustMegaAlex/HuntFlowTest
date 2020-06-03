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