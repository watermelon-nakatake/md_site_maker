import pprint

import pandas as pd
import pathlib

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
KEY_FILE_LOCATION = 'analysis/absolute-nexus-311706-6f8ae9bea293.json'


def make_csv_from_gsc(url, start_date, end_date, dir_path, file_name, d_list):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, SCOPES)
    webmasters = build('webmasters', 'v3', credentials=credentials)
    row_limit = 25000
    body = {
        'startDate': start_date,
        'endDate': end_date,
        'dimensions': d_list,
        'rowLimit': row_limit
    }
    print(body)
    print(url)
    response = webmasters.searchanalytics().query(siteUrl=url, body=body).execute()
    if 'rows' in response:
        df = pd.json_normalize(response['rows'])
        for i, d in enumerate(d_list):
            df[d] = df['keys'].apply(lambda x: x[i])
        df.drop(columns='keys', inplace=True)
        if dir_path == 'all_site_data':
            df.to_csv('gsc_data/{}/{}.csv'.format(dir_path, file_name), index=False)
        else:
            df.to_csv('gsc_data/{}/{}.csv'.format(dir_path, file_name + end_date), index=False)
            if 'qp_' in file_name:
                df.to_csv('gsc_data/{}/qp_today.csv'.format(dir_path), index=False)
            else:
                df.to_csv('gsc_data/{}/p_today.csv'.format(dir_path), index=False)
    else:
        print('no data in gsc in {}'.format(start_date))
        empty_str = 'empty'
        with open('gsc_data/{}/{}.csv'.format(dir_path, file_name + end_date), 'w', encoding='utf-8') as e:
            e.write(empty_str)


def make_list_from_gsc(site_url, start_date, end_date, dimension_list, row_limit):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, SCOPES)
    webmasters = build('webmasters', 'v3', credentials=credentials)
    body = {
        'startDate': start_date,
        'endDate': end_date,
        'dimensions': dimension_list,
        'rowLimit': row_limit
    }
    response = webmasters.searchanalytics().query(siteUrl=site_url, body=body).execute()
    df = pd.json_normalize(response['rows'])
    for i, d in enumerate(dimension_list):
        df[d] = df['keys'].apply(lambda x: x[i])
    df.drop(columns='keys', inplace=True)
    l_2d = df.values.tolist()
    df_index = df.columns
    df_index = [x for x in df_index]
    # print(df_index)
    # pprint.pprint(l_2d, width=150)
    return l_2d, df_index


if __name__ == '__main__':
    make_csv_from_gsc('https://www.sefure-do.com', '2021-02-06', '2022-02-13', 'all_site_data', 'month', ['query', 'page'])
    # make_csv_from_gsc('https://www.demr.jp', '2021-04-01', '2021-10-07', 'test', 'test_date', ['date'])
