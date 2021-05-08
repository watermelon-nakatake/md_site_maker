import pandas as pd

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
KEY_FILE_LOCATION = 'absolute-nexus-311706-6f8ae9bea293.json'


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
    response = webmasters.searchanalytics().query(siteUrl=url, body=body).execute()
    if 'rows' in response:
        df = pd.json_normalize(response['rows'])
        for i, d in enumerate(d_list):
            df[d] = df['keys'].apply(lambda x: x[i])
        df.drop(columns='keys', inplace=True)
        df.to_csv('gsc_data/{}/{}.csv'.format(dir_path, file_name + end_date), index=False)


if __name__ == '__main__':
    # make_csv_from_gsc('https://www.sefure-do.com', '2021-01-23', '2021-05-07', 'sd', 'month', ['query', 'page'])
    make_csv_from_gsc('https://www.demr.jp', '2020-04-01', '2021-05-07', 'reibun', 'test', ['page'])