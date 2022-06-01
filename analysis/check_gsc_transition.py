import os
import pprint
import statistics
from datetime import datetime, timedelta
import search_console_data
import re
import csv
import time
import pickle
import numpy as np

url_dict = {'sfd': 'https://www.sefure-do.com',
            'reibun': 'https://www.demr.jp', 'rei_site': 'https://www.reibunsite.com',
            'joshideai': 'https://www.joshideai.com', 'goodbyedt': 'https://www.goodbyedt.com',
            'howto': 'https://www.deaihowto.com', 'htaiken': 'https://www.deaihtaiken.com',
            'koibito': 'https://www.koibitodeau.com', 'konkatsu': 'https://www.netdekonkatsu.com',
            'online_marriage': 'https://www.lovestrategyguide.com', 'shoshin': 'https://www.deaishoshinsha.com',
            'women': 'https://www.deaiwomen.com'}


def search_irregular_imp_data(pj_str, start_date, end_date):
    result = []
    days_list = make_days_list(start_date, end_date)
    data_dict = make_transition_dict(pj_str, days_list)
    for url_str in data_dict:
        f_imp_av = statistics.mean(data_dict[url_str]['imp'][:80])
        p_imp_av = statistics.mean(data_dict[url_str]['imp'][-80:])
        if f_imp_av > 10 and p_imp_av < 1:
            result.append([url_str, f_imp_av, p_imp_av])
    result.sort(key=lambda x: x[1], reverse=True)
    pprint.pprint(result, width=100)
    print(len(result))


def make_transition_data(page, start_date, end_date, ):
    if '.jp' in page:
        site_url = re.sub(r'(.+?\.jp/).*$', r'\1', page)
    else:
        site_url = re.sub(r'(.+?\.com/).*$', r'\1', page)
    print(site_url)
    search_console_data.make_csv_from_gsc(site_url, start_date, end_date, 'sfd', 'month', ['query', 'page'])


def make_days_list(start_date, end_date):
    start = datetime.strptime(start_date, '%Y-%m-%d').date()
    if end_date == 'today':
        now = datetime.now()
        if now.hour >= 8:
            m_day = 2
        else:
            m_day = 3
        end = datetime.today() - timedelta(days=m_day)
        end = end.date()
    else:
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
    days_list = [(start + timedelta(n)).strftime('%Y-%m-%d') for n in range((end - start).days)]
    return days_list


def make_transition_dict(pj_list, days_list):
    result = {'days': days_list}
    for pj_str in pj_list:
        print('start : ' + pj_str)
        data_dict = {}
        d_count = 0
        need_urls = []
        path_list = os.listdir('gsc_data/' + pj_str + '/ed_data')
        # print(path_list)
        long_url = url_dict[pj_str]
        for day_str in days_list:
            use_urls = []
            if 'od' + day_str + '.csv' not in path_list:
                print('get : ' + day_str)
                search_console_data.make_csv_from_gsc(long_url, day_str, day_str, pj_str + '/ed_data', 'od', ['page'])
                time.sleep(1)
            with open('gsc_data/' + pj_str + '/ed_data/od' + day_str + '.csv', 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                r_list = [x for x in reader]
            for row in r_list[1:]:
                if row[4] not in data_dict:
                    data_dict[row[4]] = {'click': [0] * d_count + [int(row[0])], 'imp': [0] * d_count + [int(row[1])]}
                    need_urls.append(row[4])
                else:
                    data_dict[row[4]]['click'].append(int(row[0]))
                    data_dict[row[4]]['imp'].append(int(row[1]))
                use_urls.append(row[4])
            un_use_list = [x for x in need_urls if x not in use_urls]
            for uu in un_use_list:
                data_dict[uu]['click'].append(0)
                data_dict[uu]['imp'].append(0)
            d_count += 1
        # print(data_dict)
        result[pj_str] = data_dict
    with open('gsc_data/all_list.pkl', 'wb') as q:
        pickle.dump(result, q)
    return result


def get_all_site_day_data(start_date):
    days_list = make_days_list(start_date, 'today')
    with open('gsc_data/all_list.pkl', 'rb') as p:
        pk_data = pickle.load(p)
    if pk_data['days'][-1] != days_list[-1]:
        pj_list = [x for x in url_dict]
        tr_data = make_transition_dict(pj_list, days_list)
    else:
        tr_data = pk_data
    # print(tr_data)
    return tr_data


def make_unite_csv(start_date):
    tr_dict = get_all_site_day_data(start_date)
    # print(tr_dict)
    c_list = []
    for sec in ['click', 'imp']:
        for pj in tr_dict:
            if pj != 'days':
                c_list.extend([[pj] + [x] + tr_dict[pj][x][sec] for x in tr_dict[pj]])
        c_list.insert(0, ['pj_name', 'url'] + tr_dict['days'])
        # print(c_list)
        with open('gsc_data/all_{}.csv'.format(sec), 'w') as f:
            writer = csv.writer(f)
            writer.writerows(c_list)
        sum_data = make_site_sum(c_list)
        # print(sum_data)
        with open('gsc_data/sum_{}.csv'.format(sec), 'w') as g:
            writer_s = csv.writer(g)
            writer_s.writerows(sum_data)


def make_site_sum(d_list):
    # print(d_list)
    o_list = [['days'] + d_list[0][2:]]
    result = {}
    flag = False
    add = np.empty(0)
    for row in d_list:
        if row[0] in ['pj_name']:
            pass
        elif row[0] not in result:
            result[row[0]] = [row[2:]]
        else:
            result[row[0]].append(row[2:])
    for pj in result:
        np_l = np.array(result[pj])
        np_sum = np.sum(np_l, axis=0)
        if not flag:
            add = np_sum
            flag = True
        else:
            add = np.add(add, np_sum)
        o_list.append([pj] + np_sum.tolist())
    # print(add)
    o_list.append(['sum'] + add.tolist())
    return o_list


if __name__ == '__main__':
    os.chdir('../')
    print(os.getcwd())
    # make_transition_data('https://www.sefure-do.com/friend-with-benefits/jc/')
    # search_irregular_imp_data('sfd', '2021-08-09', '2022-02-08')
    # make_transition_dict('reibun', '2021-02-09', 'today')
    make_unite_csv('2021-02-09')
