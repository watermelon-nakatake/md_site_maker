import os
import pickle
import pprint
import csv
import re

import requests
from bs4 import BeautifulSoup


def make_pop_list(limit_num):
    with open('gsc_data/all_list.pkl', 'rb') as p:
        pk_data = pickle.load(p)
    # print(pk_data['shoshin'])

    with open('shoshin/all-urls.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        r_list = [x for x in reader]
    title_dict = {x[2]: x[1] for x in r_list}
    use_dict = []
    for category in ['imp', 'click']:
        imp_sum = [[x, sum(pk_data['shoshin'][x][category][-1 * limit_num:])] for x in pk_data['shoshin']]
        imp_sum.sort(key=lambda x: x[1], reverse=True)
        imp_list = [x[0] for x in imp_sum[:15]]
        # pprint.pprint(imp_list)
        imp_title = [[x, title_dict[x]] for x in imp_list if x in title_dict]
        # pprint.pprint(imp_title)
        for row in imp_title:
            if row not in use_dict:
                use_dict.append(row)
    pprint.pprint(use_dict)
    print(len(use_dict))
    result_str = ''.join(['<li><a href="{}">{}</a></li>'.format(x[0].replace('https://www.deaishoshinsha.com', ''),
                                                                x[1]) for x in use_dict])
    print(result_str)


def check_gsc_and_html(day_lim, str_len_lim):
    od_list = os.listdir('gsc_data/shoshin/ed_data')
    od_list.remove('p_today.csv')
    od_list.sort()
    m_dict = {}
    with open('shoshin/pickle_pot/checked_page.pkl', 'rb') as p:
        checked_list = pickle.load(p)
    # checked_list = {}
    for day_d in od_list[-1 * day_lim:]:
        # print(day_d)
        with open('gsc_data/shoshin/ed_data/' + day_d, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            r_list = [x for x in reader]
        for row in r_list[1:]:
            if row[4] not in m_dict:
                m_dict[row[4]] = [int(row[0]), int(row[1])]
            else:
                m_dict[row[4]] = [m_dict[row[4]][0] + int(row[0]), m_dict[row[4]][1] + int(row[1])]
    # pprint.pprint(m_dict)
    m_list = [[x, m_dict[x][0], m_dict[x][1]] for x in m_dict if (m_dict[x][0] > 1 or m_dict[x][1] > day_lim * 10)
              and '/tag/' not in x and '/beginner/' not in x and (x not in checked_list or not checked_list[x]['tag']
              or not checked_list[x]['desc'] or not checked_list[x]['j_flag'] or not checked_list[x]['k_flag']
                                                                  or checked_list[x]['len'] < str_len_lim)]
    m_list.sort(key=lambda x: x[1], reverse=True)
    # pprint.pprint(m_list)
    counter = 0
    for page in m_list:
        # print('start: {}'.format(page))
        p_result = {}
        res = requests.get(page[0])
        # レスポンスの HTML から BeautifulSoup オブジェクトを作る
        soup = BeautifulSoup(res.text, 'html.parser')
        meta_desc = soup.find_all("meta", attrs={"name": "description"})
        desc = meta_desc[0].get('content')
        art_l = soup.find_all('article')
        if art_l:
            a_str = art_l[0].text
            if '出会い系サイト口コミ評価ランキング' in a_str:
                main_str = re.sub(r'出会い系サイト口コミ評価ランキング[\s\S]*$', '', a_str)
            elif '関連のある出会い系用語' in a_str:
                main_str = re.sub(r'関連のある出会い系用語[\s\S]*$', '', a_str)
            else:
                main_str = a_str
            str_len = len(main_str)
            if 'Jメール' in main_str or 'ミント' in main_str:
                j_flag = False
            else:
                j_flag = True
            if '関連のある出会い系用語' in main_str:
                k_flag = False
            else:
                k_flag = True
        else:
            str_len = 0
            j_flag = False
            k_flag = False
        p_result['len'] = str_len
        p_result['j_flag'] = j_flag
        p_result['k_flag'] = k_flag
        if desc == '出会い系サイトを始めて利用する初心者の方が出会えるように出会い系に関する専門用語辞典や出会い系サイトの攻略法で' \
                   '応援します。':
            p_result['desc'] = False
        else:
            p_result['desc'] = True
        tag_l = soup.find_all('div', {'class': 'tagl'})
        if tag_l:
            tag = tag_l[0].text
            if len(tag) < 4:
                p_result['tag'] = False
            else:
                p_result['tag'] = True
        else:
            p_result['tag'] = False
        if not p_result['tag'] or not p_result['desc'] or not p_result['j_flag'] or not p_result['k_flag']\
                or p_result['len'] < str_len_lim:
            id_l = soup.find_all('link', attrs={'rel': 'alternate', 'type': 'application/json'})
            i_str = id_l[0].attrs['href']
            id_num = re.sub(r'^.+/(\d+)$', r'\1', i_str)
            check_l = [x for x in p_result if (x in ['tag', 'desc', 'j_flag', 'k_flag'] and not p_result[x])
                       or (x == 'len' and p_result[x] < str_len_lim)]
            if 'len' in check_l:
                check_l.remove('len')
                check_l.append('len : ' + str(p_result['len']))
            print('{} : {}, {}'.format(page[0].replace('https://www.deaishoshinsha.com/', ''), page[1], page[2]))
            # print(p_result)
            print('https://www.deaishoshinsha.com/wp/wp-admin/post.php?post={}&action=edit : {}'.format(id_num, check_l))
            counter += 1
        checked_list[page[0]] = p_result
        if counter > 10:
            break
    with open('shoshin/pickle_pot/checked_page.pkl', 'wb') as r:
        pickle.dump(checked_list, r)


if __name__ == '__main__':
    # make_pop_list(28)
    check_gsc_and_html(day_lim=30, str_len_lim=500)
