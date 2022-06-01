import os
import pprint

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

address = 'python-to-ga4@python-to-search-console.iam.gserviceaccount.com'
ga_id = '107526009797434172243'

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'analysis/python-to-search-console-007dba6793fa.json'
VIEW_ID = '32863616'


def initialize_analytics_reporting():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, SCOPES)
    return build('analyticsreporting', 'v4', credentials=credentials)


def get_report(analytics, start_date, limit):
    request_body = {
        'reportRequests': [{
            'viewId': VIEW_ID,
            'pageSize': limit,
            'dateRanges': [{'startDate': start_date, 'endDate': 'today'}],
            'metrics': [{'expression': 'ga:pageviews'}],
            'dimensions': [{'name': 'ga:pagePath'}, {'name': 'ga:pageTitle'}],
            'orderBys': [{'fieldName': 'ga:pageviews', 'sortOrder': 'DESCENDING'}]
        }]
    }
    return analytics.reports().batchGet(body=request_body).execute()


def print_response(response):
    for report in response.get('reports', []):
        column_header = report.get('columnHeader', {})
        dimension_headers = column_header.get('dimensions', [])
        metric_headers = column_header.get('metricHeader', {}).get('metricHeaderEntries', [])

        for row in report.get('data', {}).get('rows', []):
            print('-----------------------------')
            dimensions = row.get('dimensions', [])
            date_range_values = row.get('metrics', [])
            for header, dimension in zip(dimension_headers, dimensions):
                print(header + ': ' + dimension)
            for i, values in enumerate(date_range_values):
                for metricHeader, value in zip(metric_headers, values.get('values')):
                    print(metricHeader.get('name') + ': ' + value)


def make_ga_list(response):
    result = []
    for report in response.get('reports', []):
        column_header = report.get('columnHeader', {})
        dimension_headers = column_header.get('dimensions', [])
        metric_headers = column_header.get('metricHeader', {}).get('metricHeaderEntries', [])
        for row in report.get('data', {}).get('rows', []):
            insert_l = []
            dimensions = row.get('dimensions', [])
            date_range_values = row.get('metrics', [])
            for header, dimension in zip(dimension_headers, dimensions):
                insert_l.append(dimension)
                # print(header + ': ' + dimension)
            for i, values in enumerate(date_range_values):
                for metricHeader, value in zip(metric_headers, values.get('values')):
                    insert_l.append(value)
                    # print(metricHeader.get('name') + ': ' + value)
            result.append(insert_l)
    pprint.pprint(result)
    return result


def main(start_date, limit):
    analytics = initialize_analytics_reporting()
    response = get_report(analytics, start_date, limit)
    # print_response(response)
    make_ga_list(response)


def get_ga_data(start_date, limit):
    analytics = initialize_analytics_reporting()
    response = get_report(analytics, start_date, limit)
    ga_list = make_ga_list(response)
    return ga_list


if __name__ == '__main__':
    os.chdir('../')
    main(start_date='2022-04-01', limit='100')
