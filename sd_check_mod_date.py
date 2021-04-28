import csv
import datetime
import make_article_list
import os
import re
from bs4 import BeautifulSoup
import requests
import pickle
from datetime import datetime, timedelta
import search_console_data


def make_mod_date_list(pd):
    seen = []
    mod_list = []
    mod_log = make_article_list.read_pickle_pot('modify_log', pd)
    mod_log.reverse()
    for log in mod_log:
        if log[0] not in seen:
            mod_list.append([log[0].replace('reibun', ''), log[1]])
            seen.append(log[0])
    make_article_list.save_data_to_pickle(mod_list, 'mod_date_list', pd)


def sc_data_match_page(csv_list):
    result = {}
    # print(csv_list)
    for page in csv_list[1:]:
        f_page = page[4].replace('https://www.sefure-do.com/', '')
        f_page = re.sub(r'^(.+)#.+', r'\1', f_page)
        result[f_page] = page
    result_list = [[x[4], x[0], x[1], str(round(float(x[2]), 2)),
                    str(round(float(x[3]), 2))] for x in csv_list[1:]]
    return result_list


def make_target_data_for_today(today, period):
    start_d = today - timedelta(days=period)
    end_d = today - timedelta(days=2)
    start_str = start_d.strftime('%Y-%m-%d')
    end_str = end_d.strftime('%Y-%m-%d')
    # print(start_str)
    # print(end_str)
    if not os.path.exists('gsc_data/sfd/p_month' + end_str + '.csv'):
        search_console_data.make_csv_from_gsc('https://www.sefure-do.com', start_str, end_str, 'sfd',
                                              'qp_month', ['query', 'page'])
        search_console_data.make_csv_from_gsc('https://www.sefure-do.com', start_str, end_str, 'sfd',
                                              'p_month', ['page'])
    return end_str


def next_update_target_search(aim_date, period):
    today = datetime.today()
    end_date = make_target_data_for_today(today, period)
    with open('gsc_data/sfd/p_month' + end_date + '.csv') as f:
        reader = csv.reader(f)
        csv_list = [row for row in reader]
    c_list = sc_data_match_page(csv_list)
    with open('gsc_data/sfd/qp_month' + end_date + '.csv') as f:
        q_reader = csv.reader(f)
        q_list = [row for row in q_reader]
    q_list = q_list[1:]
    # print(c_list)
    with open('sfd/pickle_pot/date_img.pkl', 'rb') as f:
        pk_dic = pickle.load(f)
    limit_d = today - timedelta(days=aim_date)
    print('日数 : ' + str(period) + '日間')
    print('クリック数順')
    pk_dic, target_list = check_list_and_bs(c_list, pk_dic, limit_d, q_list)

    # click_list = check_no_mod_page(mod_list_n, c_list)
    # c_list.sort(key=lambda x: int(x[2]), reverse=True)
    # print('表示回数順')
    # display_list = check_no_mod_page(mod_list_n, c_list)
    # c_list.sort(key=lambda x: int(x[1]), reverse=True)
    with open('sfd/pickle_pot/date_img.pkl', 'wb') as p:
        pickle.dump(pk_dic, p)
    with open('sfd/pickle_pot/target_files.pkl', 'wb') as q:
        pickle.dump(target_list, q)
    return pk_dic


def display_mod_target_data():
    today = datetime.today()
    end_d = today - timedelta(days=2)
    limit_date = today - timedelta(days=100)
    end_date = end_d.strftime('%Y-%m-%d')
    if os.path.exists('gsc_data/sfd/p_month' + end_date + '.csv'):
        with open('sfd/pickle_pot/target_files.pkl', 'rb') as t:
            target_pages = pickle.load(t)
        # print(target_pages)
        with open('gsc_data/sfd/p_month' + end_date + '.csv') as f:
            reader = csv.reader(f)
            csv_list = [row for row in reader]
        c_dic = {x[4]: [x[0], x[1], x[3]] for x in csv_list if x[4].replace('https://www.sefure-do.com/', '')
                 in target_pages}
        # print(c_dic)
        with open('gsc_data/sfd/qp_month' + end_date + '.csv') as f:
            q_reader = csv.reader(f)
            q_list = [row for row in q_reader]
        q_list = q_list[1:]
        with open('sfd/pickle_pot/date_img.pkl', 'rb') as p:
            pk_dic = pickle.load(p)

        for tp in target_pages:
            # print(tp)
            # print(pk_dic[tp])
            check_target_data(pk_dic[tp], limit_date)
            tp = 'https://www.sefure-do.com/' + tp
            print('   {}        {}      {}'.format(c_dic[tp][0], c_dic[tp][1], round(float(c_dic[tp][2]), 2)))
            get_gsc_query(tp, q_list)
            print('\n')
    else:
        print('make data for today')
        next_update_target_search(100, 28)


def check_target_data(target_data, limit_date):
    print(target_data['path'] + '  ' + target_data['title'])
    if target_data['title_len'] > 33 or target_data['title_len'] < 29:
        print('change title !')
    if not target_data['main_img_flag']:
        print('there is no images !')
    if not target_data['k2_flag']:
        print('make k2 comment')
    if not target_data['mt_flag']:
        print('delete mt !')
    new_date = datetime.strptime(target_data['mod_time'].replace('T', ' ').replace('+0900', ''), '%Y-%m-%d %H:%M:%S')
    if new_date < limit_date:
        print('too old !!')


def get_gsc_query(target_page, q_list):
    filtered_data = [x for x in q_list if target_page in x[5]]
    filtered_data.sort(key=lambda x: (int(x[0]), int(x[1]), float(x[3])), reverse=True)
    print('クリック   表示回数    平均順位       クエリ')
    for d_r in filtered_data:
        position = str(round(float(d_r[3]), 1))
        print(' ' * (4 - len(d_r[0])) + d_r[0] + ' ' * (11 - len(d_r[1])) + d_r[1] +
              ' ' * (10 - len(position)) + position + ' ' * 6 + d_r[4])


def check_list_and_bs(sc_list, pk_dic, limit_d, q_list):
    i = 0
    target_list = []
    for page in sc_list:
        if page[0] != 'https://www.sefure-do.com/friend-with-benefits/area-bbs/' and\
                page[0] != 'https://www.sefure-do.com/friend-with-benefits/' and\
                page[0] != 'https://www.sefure-do.com/':
            page_name = page[0].replace('https://www.sefure-do.com/', '')
            click_num, view_num, order_num = page[1], page[2], page[4]
            if page_name in pk_dic:
                if not pk_dic[page_name]['update_flag']:
                    page_data = read_sd_page(page[0])
                    if not page_data['update_flag']:
                        print(page_data['path'] + '  ' + page_data['title'])
                        if page_data['title_len'] > 33 or page_data['title_len'] < 29:
                            print('change title !')
                        if not page_data['main_img_flag']:
                            print('there is no images !')
                        if not page_data['k2_flag']:
                            print('make k2 comment')
                        if not page_data['mt_flag'] and 'area-bbs/' not in page_name:
                            print('delete mt !')
                        print('   {}        {}      {}'.format(click_num, view_num, order_num))
                        get_gsc_query(page_name, q_list)
                        i += 1
                        target_list.append(page_name)
                    pk_dic[page_name] = page_data
                else:
                    this_date = datetime.strptime(pk_dic[page_name]['mod_time'].replace('T', ' ').replace('+0900', ''),
                                                  '%Y-%m-%d %H:%M:%S')
                    if this_date < limit_d:
                        page_data = read_sd_page(page[0])
                        new_date = datetime.strptime(page_data['mod_time'].replace('T', ' ').replace('+0900', ''),
                                                     '%Y-%m-%d %H:%M:%S')
                        if new_date < limit_d:
                            print(page_data['path'] + '  ' + page_data['title'])
                            print('too old !!')
                            print('   {}        {}      {}'.format(click_num, view_num, order_num))
                            get_gsc_query(page_name, q_list)
                            i += 1
                            target_list.append(page_name)
                        pk_dic[page_name] = page_data
            else:
                page_data = read_sd_page(page[0])
                if not page_data['update_flag']:
                    if not page_data['update_flag']:
                        print(page_data['path'] + '  ' + page_data['title'])
                        if page_data['title_len'] > 33 or page_data['title_len'] < 29:
                            print('change title !')
                        if not page_data['main_img_flag']:
                            print('there is no images !')
                        if not page_data['k2_flag']:
                            print('make k2 comment')
                        if not page_data['mt_flag'] and 'area-bbs/' not in page_name:
                            print('delete mt !')
                    print('   {}        {}      {}'.format(click_num, view_num, order_num))
                    get_gsc_query(page_name, q_list)
                    i += 1
                    target_list.append(page_name)
                else:
                    new_date = datetime.strptime(page_data['mod_time'].replace('T', ' ').replace('+0900', ''),
                                                 '%Y-%m-%d %H:%M:%S')
                    if new_date < limit_d:
                        print(page_data['path'] + '  ' + page_data['title'])
                        print('too old !!')
                        print('   {}        {}      {}'.format(click_num, view_num, order_num))
                        get_gsc_query(page_name, q_list)
                        i += 1
                        target_list.append(page_name)
                pk_dic[page_name] = page_data
        # if 'mod_time' not in pk_dic[page_name]:
        #     pk_dic[page_name] = read_sd_page(page[0])

        # print('{} : {} : {} : {}'.format(click_num, pk_dic[page_name]['title'], pk_dic[page_name]['path'],
        #       re.sub(r'T.*$', '', pk_dic[page_name]['mod_time'])))
        if i >= 10:
            break
    return pk_dic, target_list


def read_sd_page(page_url):
    # スクレイピング対象の URL にリクエストを送り HTML を取得する
    # print(page_url)
    # print('scrape: ' + page_url)
    res = requests.get(page_url)
    # レスポンスの HTML から BeautifulSoup オブジェクトを作る
    soup = BeautifulSoup(res.text, 'html.parser')
    title_text = soup.find('title').get_text().replace(' - セフレ道', '')
    title_len = len(title_text)
    if 29 <= title_len <= 33:
        tl_flag = True
    else:
        tl_flag = False
    main_img = soup.find_all('img', {'class': 'size-large'})
    full_img = soup.find_all('img', {'class': 'size-full'})
    # print(main_img)
    if not main_img and not full_img:
        # print('There in no main image!')
        main_img_flag = False
    else:
        main_img_flag = True
    md = soup.find('time', {'class': 'updated'})
    if md:
        mod_time = md.get('datetime')
    else:
        mod_time = ''
    k2_box = soup.find_all('div', {'class': 'kaiwaicon2'})
    k3_box = soup.find_all('div', {'class': 'kaiwaicon3'})
    # print(k_box)
    if not k2_box and not k3_box:
        # print('There in no kaiwaicon2!')
        k2_flag = False
    else:
        k2_flag = True
    main_txt = soup.find_all('div', {'class': 'mainbox'})[0]

    # print(main_txt)
    for script in main_txt(["script", "style"]):
        script.decompose()
    text = main_txt.get_text()
    id_str = '0'
    for c_str in soup.body.get('class'):
        if 'postid' in c_str:
            id_str = re.sub(r'postid-(\d*)', r'\1', c_str)
            break
    post_id = int(id_str)
    if 'ミント' in text or 'Jメール' in text:
        if '/area-bbs/' not in page_url:
            # print('Jmail in this page')
            mt_flag = False
        else:
            mt_flag = True
    else:
        mt_flag = True
    if main_img_flag and k2_flag and mt_flag and tl_flag:
        update_flag = True
    else:
        update_flag = False
    result = {'path': page_url, 'title': title_text, 'title_len': title_len, 'main_img_flag': main_img_flag,
              'k2_flag': k2_flag, 'mt_flag': mt_flag, 'update_flag': update_flag, 'post_id': post_id,
              'mod_time': str(mod_time)}
    return result


def check_old_page(c_list):
    print(c_list)


def check_no_mod_page(mod_list, csv_list, len_dec, pd):
    result = []
    url_list = [x[0].replace('/' + pd['main_dir'], '') for x in mod_list]
    # print(url_list)
    i = 1
    for g_data in csv_list:
        url_str = g_data[0].replace('https://www.demr.jp', '').replace('/' + pd['main_dir'], '')
        # print(url_str)
        if url_str not in url_list and g_data[0] != 'https://www.demr.jp/':
            result.append(url_str)
            if re.findall(r'/$', url_str):
                url_str_n = url_str + 'index.html'
            else:
                url_str_n = url_str
            len_dec = {y.replace('/' + pd['main_dir'], ''): len_dec[y] for y in len_dec}
            if url_str_n in len_dec:
                if '/sitepage/' not in url_str:
                    print('{} : {}, {}クリック, 表示{}回, 掲載順位平均{}, 文字数 {}'
                          .format(str(i), url_str, g_data[1], g_data[2], g_data[4], len_dec[url_str_n]))
                else:
                    print('{} : {}, {}クリック, 表示{}回, 掲載順位平均{}'
                          .format(str(i), url_str, g_data[1], g_data[2], g_data[4]))
        if len(result) == 10:
            break
        i += 1
    return result


def check_number_of_days():
    with open('/Users/nakataketetsuhiko/Downloads/https___www/日付.csv') as f:
        reader = csv.reader(f)
        csv_list = [row for row in reader]
    result = len(csv_list) - 1
    return result


def make_side_bar_article_list(list_length, pd):
    click_list = []
    time_list = []
    pk_dec = make_article_list.read_pickle_pot('main_data', pd)
    with open('/Users/nakataketetsuhiko/Downloads/https___www/ページ.csv') as f:
        reader = csv.reader(f)
        csv_list = [row for row in reader]
    c_list = [y for y in csv_list[1:] if '#' not in y[0] and '/amp/' not in y[0]]
    print('pop by click')
    for click_a in c_list:
        if '/pc/' in click_a[0]:
            path = click_a[0].replace('https://www.demr.jp/pc/', '')
            for pk_id in pk_dec:
                if pk_dec[pk_id]['file_path'] == path:
                    click_list.append(pk_id)
                    print('{} : {}, {}'.format(path, str(pk_id), pk_dec[pk_id]['title']))
        if len(click_list) == list_length:
            break
    ga_list = make_ga_csv_list()
    t_list = [x for x in ga_list if '#' not in x[0] and '/pc/' not in x[0] and int(x[1].replace(',', '')) >= 100]
    t_list.sort(key=lambda x: datetime.datetime.strptime(x[3], '%H:%M:%S'), reverse=True)
    print('\nimportant by reading time')
    for t_art in t_list:
        t_path = t_art[0].replace('/amp/', '')
        for pk_i in pk_dec:
            if pk_dec[pk_i]['file_path'] == t_path and pk_i not in click_list:
                time_list.append(pk_i)
                print('{} : {}, {}, {}'.format(t_path, str(pk_i), pk_dec[pk_i]['title'], t_art[3]))
                break
        if len(time_list) == list_length:
            break
    print('\n')
    print(time_list)
    print(click_list)


def make_ga_csv_list():
    down_path_l = os.listdir('/Users/nakataketetsuhiko/Downloads')
    result = []
    for path in down_path_l:
        if 'Analytics' in path:
            with open('/Users/nakataketetsuhiko/Downloads/' + path) as f:
                reader = csv.reader(f)
                csv_list = [row for row in reader]
            start_row = 0
            end_row = 0
            for i in range(len(csv_list)):
                if len(csv_list[i]) > 2:
                    if 'ページ別訪問数' in csv_list[i][2]:
                        start_row = i
                if len(csv_list[i]) >= 1:
                    if '日の指標' in csv_list[i][0]:
                        end_row = i
                        break
            result = [x for x in csv_list[start_row + 1:end_row - 2] if '/pc/' not in x[0]]
    return result


def count_title_str_num(len_dec, pd):
    result = []
    print('タイトル文字数チェック')
    p_data = make_article_list.read_pickle_pot('main_data', pd)
    # print(p_data)
    short_title_l = [[len(p_data[x]['title']), p_data[x]['file_path'], p_data[x]['title']] for x in p_data
                     if len(p_data[x]['title']) < 20]
    for y in sorted(short_title_l):
        if 'policy' not in y[1]:
            print(str(y[0]) + ' : {}  {}  {}'.format(y[1], y[2], len_dec['/pc/' + y[1]]))
            result.append(y[1])
    return result


def make_to_do_list(click_list, display_list, title_list):
    print('クリック順')
    for x in click_list:
        if x.replace('/pc/', '') in title_list:
            print(x)
    print('表示順')
    for y in display_list:
        if y.replace('/pc/', '') in title_list:
            print(y)
    print('共通')
    for z in click_list:
        if z in display_list:
            print(z)


def check_layout_flag(click_list, pk_dec, p_dic):
    print('レイアウト変更未実施')
    s_pk = {'str_len': 'n_a'}
    new_cl = [x[0] for x in click_list]
    i = 1
    j = 1
    for page in new_cl:
        page = page.replace('https://www.demr.jp', '')
        if page != '/' and '/sitepage/' not in page:
            if page in pk_dec:
                if not pk_dec[page]:
                    c_num = ''
                    for cl in click_list:
                        if page in cl[0]:
                            c_num = cl[1]
                            break
                    for pk in p_dic:
                        if page.replace('/pc/', '') in p_dic[pk]['file_path']:
                            s_pk = p_dic[pk]
                            break
                    print(str(i) + ' : ' + page + ' ' + c_num + ' ' + str(s_pk['str_len']))
                    j += 1
                if j > 9:
                    break
        i += 1


def check_shift_flag(click_list, pk_dec, pd):
    print('shift対応未実施')
    new_cl = [x[0] for x in click_list]
    i = 1
    j = 1
    for page in new_cl:
        page = page.replace('https://www.' + pd['domain_str'], '')
        if '/sitepage/' not in page and page in pk_dec:
            if page != '/' and not pk_dec[page]:
                if os.path.exists(pd['project_dir'] + '/md_files/' + page.replace('.html', '.md')):
                    with open(pd['project_dir'] + '/md_files/' + page.replace('.html', '.md'), 'r', encoding='utf-8') \
                            as f:
                        long_str = f.read()
                    if 'sitepage/mintj.html' in long_str:
                        c_num = ''
                        for cl in click_list:
                            if page in cl[0]:
                                c_num = cl[1]
                                break
                        print(str(i) + ' : ' + page + ' ' + c_num)
                        j += 1
            if j > 9:
                break
        i += 1


if __name__ == '__main__':
    # print(str_len_dec)
    # make_side_bar_article_list(10, p_d)
    # print('\n')

    c_l = next_update_target_search(100, 28)
    # display_mod_target_data()

    # get_gsc_query('gsc_data/sd/month2021-04-23.csv', 'chinese')

    # make_target_data_for_today('sd')

    # read_sd_page('https://www.sefure-do.com/friend-with-benefits/abnormal/')
    # read_sd_page('https://www.sefure-do.com/friend-with-benefits/physical-labor/')

    # # print('\n')
    # # t_l = count_title_str_num(str_len_dec, p_d)
    # print('\n')
    # make_to_do_list(c_l, d_l, t_l)
    # print('\n')
    # # print(c_l2)
    # check_layout_flag(c_l2, layout_dec, pickle_dec)
    # check_shift_flag(c_l2, shift_dec, p_d)

    # print(make_article_list.read_pickle_pot('mod_date_list', p_d))
    # print(make_article_list.read_pickle_pot('modify_log', p_d))
    #
    # print(make_article_list.read_pickle_pot('main_data', p_d))
    # np = make_article_list.read_pickle_pot('main_data', p_d)
    # op = make_article_list.read_pickle_pot('title_img_list2', p_d)
    # for s in np:
    #     if s == 144:
    #         np[s]['mod_date'] = op[146][3]
    #     else:
    #         np[s]['mod_date'] = op[s][3]
    # print(np)
    # make_article_list.save_data_to_pickle(np, 'main_data', p_d)
    # make_mod_date_list()
    # print(make_ga_csv_list())
