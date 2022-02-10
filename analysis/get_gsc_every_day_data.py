from analysis import search_console_data
from datetime import datetime, timedelta
import os
import time


def get_one_day_data_in_period(url, start_period, end_period, dir_path):
    start = datetime.strptime(start_period, '%Y-%m-%d').date()
    end = datetime.strptime(end_period, '%Y-%m-%d').date()
    days_list = [(start + timedelta(n)).strftime('%Y-%m-%d') for n in range((end - start).days)]
    # print(days_list)
    for day_str in days_list:
        if not os.path.exists('gsc_data/' + dir_path + '/ed_data/od' + day_str + '.csv'):
            print(day_str)
            search_console_data.make_csv_from_gsc(url, day_str, day_str, dir_path + '/ed_data', 'od', ['page'])
            time.sleep(1)


if __name__ == '__main__':
    get_one_day_data_in_period('https://www.sefure-do.com', '2021-08-09', '2022-02-08', 'sfd')
