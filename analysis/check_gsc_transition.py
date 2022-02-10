import os
from datetime import datetime, timedelta
import search_console_data
import re
import pandas as pd

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
KEY_FILE_LOCATION = 'analysis/absolute-nexus-311706-6f8ae9bea293.json'


def make_transition_data(page, start_date, end_date, ):
    if '.jp' in page:
        site_url = re.sub(r'(.+?\.jp/).*$', r'\1', page)
    else:
        site_url = re.sub(r'(.+?\.com/).*$', r'\1', page)
    print(site_url)
    search_console_data.make_csv_from_gsc(site_url, start_date, end_date, 'sfd', 'month', ['query', 'page'])


def make_transition_dict(pj_str, url, start_date, end_date):
    path_list = os.listdir('gsc_data/' + pj_str + '/ed_data')
    print(path_list)
    start = datetime.strptime(start_date, '%Y-%m-%d').date()
    end = datetime.strptime(end_date, '%Y-%m-%d').date()
    days_list = [(start + timedelta(n)).strftime('%Y-%m-%d') for n in range((end - start).days)]
    print(days_list)


if __name__ == '__main__':
    # make_transition_data('https://www.sefure-do.com/friend-with-benefits/jc/')
    make_transition_dict('sfd', 'https://www.sefure-do.com/friend-with-benefits/jc/', '2021-08-09', '2022-02-08')
