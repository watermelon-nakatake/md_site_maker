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


def sc_data_match_page(csv_list, domain):
    result = {}
    # print(csv_list)
    for page in csv_list[1:]:
        f_page = page[4].replace(domain + '/', '')
        f_page = re.sub(r'^(.+)#.+', r'\1', f_page)
        result[f_page] = page
    result_list = [[x[4], x[0], x[1], str(round(float(x[2]), 2)),
                    str(round(float(x[3]), 2))] for x in csv_list[1:]]
    return result_list


def make_target_data_for_today(today, period, pj_dir, domain):
    start_d = today - timedelta(days=period)
    end_d = today - timedelta(days=3)
    start_str = start_d.strftime('%Y-%m-%d')
    end_str = end_d.strftime('%Y-%m-%d')
    if not os.path.exists('gsc_data/' + pj_dir + '/p_month' + end_str + '.csv'):
        search_console_data.make_csv_from_gsc(domain, start_str, end_str, pj_dir,
                                              'qp_month', ['query', 'page'])
        search_console_data.make_csv_from_gsc(domain, start_str, end_str, pj_dir,
                                              'p_month', ['page'])
    return end_str


def project_select(file_path):
    project_str = re.sub(r'^(.+?)/.*$', r'\1', file_path)
    pj_dir, domain, main_dir = '', '', ''
    print(project_str)
    if project_str == 'reibun':
        pj_dir = 'reibun'
        domain = 'https://www.demr.jp'
        main_dir = 'reibun/html_files/pc/'
    return pj_dir, domain, main_dir


def check_single_page_seo(period, html_path):
    main_str_limit = 5000
    limit_d = 100
    today = datetime.today()
    if '.md' in html_path:
        html_path = html_path.replace('.md', '.html').replace('/md_files/', '/html_files/')
    pj_dir, domain, main_dir = project_select(html_path)
    end_date = make_target_data_for_today(today, period, pj_dir, domain)
    with open('gsc_data/' + pj_dir + '/p_month' + end_date + '.csv') as f:
        reader = csv.reader(f)
        csv_list = [row for row in reader]
    c_list = sc_data_match_page(csv_list, domain)
    with open('gsc_data/' + pj_dir + '/qp_month' + end_date + '.csv') as f:
        q_reader = csv.reader(f)
        q_list = [row for row in q_reader]
    q_list = q_list[1:]
    with open(pj_dir + '/pickle_pot/main_data.pkl', 'rb') as f:
        pk_dic = pickle.load(f)
    url = html_path.replace(pj_dir + '/html_files/', domain + '/')
    page_name = html_path.replace(main_dir, '')
    this_pk_data = {}
    for id_num in pk_dic:
        if pk_dic[id_num]['file_path'] == page_name:
            this_pk_data = pk_dic[id_num]
            continue
    page = [x for x in c_list if x[0] == url]
    click_num, view_num, order_num = page[0][1], page[0][2], page[0][4]
    this_query = [x for x in q_list if url == x[5]]
    q_dic = make_simple_keyword_dic(this_query)
    error_list = seo_checker_to_pk_data(this_pk_data, main_str_limit, limit_d, today)
    print(page_name + ' : ' + this_pk_data['title'] + '  (' + str(len(this_pk_data['title'])) + ')')
    print('   {}        {}      {}'.format(click_num, view_num, order_num))
    if error_list:
        print(error_list)
    query_str_list, top_words = seo_checker_by_query(this_pk_data, q_dic)
    if top_words:
        for tw in top_words:
            print(tw)
    for qs in query_str_list:
        print(qs)
    get_gsc_query(page_name, q_list)


def next_update_target_search(limit_d, period, main_str_limit, target_project):
    today = datetime.today()
    pj_dir, domain, main_dir = project_select(target_project + '/')
    end_date = make_target_data_for_today(today, period, pj_dir, domain)
    with open('gsc_data/' + pj_dir + '/p_month' + end_date + '.csv') as f:
        reader = csv.reader(f)
        csv_list = [row for row in reader]
    c_list = sc_data_match_page(csv_list, domain)
    with open('gsc_data/' + pj_dir + '/qp_month' + end_date + '.csv') as f:
        q_reader = csv.reader(f)
        q_list = [row for row in q_reader]
    q_list = q_list[1:]
    # print(c_list)
    with open(pj_dir + '/pickle_pot/main_data.pkl', 'rb') as f:
        pk_dic = pickle.load(f)
    # print(pk_dic)
    # print(q_list)
    print('日数 : ' + str(period) + '日間')
    print('クリック数順')
    target_list = check_list_and_bs(c_list, pk_dic, limit_d, q_list, main_str_limit, today)

    # click_list = check_no_mod_page(mod_list_n, c_list)
    # c_list.sort(key=lambda x: int(x[2]), reverse=True)
    # print('表示回数順')
    # display_list = check_no_mod_page(mod_list_n, c_list)
    # c_list.sort(key=lambda x: int(x[1]), reverse=True)
    # with open('reibun/pickle_pot/main_data.pkl', 'wb') as p:
    #     pickle.dump(pk_dic, p)
    with open(pj_dir + '/pickle_pot/target_files.pkl', 'wb') as q:
        pickle.dump(target_list, q)
    return pk_dic


def display_mod_target_data():
    today = datetime.today()
    end_d = today - timedelta(days=2)
    limit_date = today - timedelta(days=100)
    end_date = end_d.strftime('%Y-%m-%d')
    if os.path.exists('gsc_data/reibun/p_month' + end_date + '.csv'):
        with open('reibun/pickle_pot/target_files.pkl', 'rb') as t:
            target_pages = pickle.load(t)
        # print(target_pages)
        with open('gsc_data/reibun/p_month' + end_date + '.csv') as f:
            reader = csv.reader(f)
            csv_list = [row for row in reader]
        c_dic = {x[4]: [x[0], x[1], x[3]] for x in csv_list if x[4].replace('https://www.demr.jp/', '')
                 in target_pages}
        # print(c_dic)
        with open('gsc_data/reibun/qp_month' + end_date + '.csv') as f:
            q_reader = csv.reader(f)
            q_list = [row for row in q_reader]
        q_list = q_list[1:]
        with open('reibun/pickle_pot/date_img.pkl', 'rb') as p:
            pk_dic = pickle.load(p)

        for tp in target_pages:
            # print(tp)
            # print(pk_dic[tp])
            check_target_data(pk_dic[tp], limit_date)
            tp = 'https://www.demr.jp/' + tp
            print('   {}        {}      {}'.format(c_dic[tp][0], c_dic[tp][1], round(float(c_dic[tp][2]), 2)))
            get_gsc_query(tp, q_list)
            print('\n')
    else:
        print('make data for today')
        next_update_target_search(100, 28, 4000, 'reibun')


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


def seo_checker_to_pk_data(pk_data, main_str_limit, limit_d, today):
    error_list = []
    if 'layout_flag' in pk_data:
        if not pk_data['layout_flag']:
            error_list.append('collect layout !')
    # if 'shift_flag' in pk_data:
    #     if not pk_data['shift_flag']:
    #         error_list.append('delete mt !')
    if len(pk_data['title']) > 33:
        error_list.append('too long title str !')
    elif len(pk_data['title']) < 29:
        error_list.append('too short title !')
    if pk_data['str_len'] < main_str_limit:
        error_list.append('too short main contents')
    this_date = datetime.strptime(pk_data['mod_date'], '%Y-%m-%d')
    if this_date < today - timedelta(days=limit_d):
        error_list.append('too old !!')
    return error_list


def seo_checker_by_query(pk_data, q_dic):
    result_list = []
    top_words_data = []
    c_list = []
    ignore_list = ['出会系']
    if 'ign_words' in pk_data:
        ignore_list.extend(pk_data['ign_words'])
    with open('reibun/md_files/pc/' + pk_data['file_path'].replace('.html', '.md'), 'r', encoding='utf-8') as f:
        long_str = f.read()
    main_text = re.sub(r'^[\S\s]*\n# .+?\n', '', long_str)
    main_text = re.sub(r'%kanren%[\S\s]*$', '', main_text)
    main_text = re.sub(r']\(.+?\)', ']', main_text)
    main_text = main_text.replace('\n', '')
    main_text = main_text.lower()
    title = re.findall(r't::(.+?)\n', long_str)[0]
    h2_list = re.findall(r'\n## (.+?)\n', long_str)
    h3_list = re.findall(r'\n### (.+?)\n', long_str)
    h4_list = re.findall(r'\n#### (.+?)\n', long_str)
    if h4_list:
        result_list.append('クリック   表示回数      main    title   h2   h3   h4   キーワード')
    elif not h3_list:
        result_list.append('クリック   表示回数      main    title   h2   キーワード')
    else:
        result_list.append('クリック   表示回数      main    title   h2   h3   キーワード')
    i = 0
    words_list = [x[0] for x in q_dic]
    for word in q_dic:
        l_word = word[0].lower()
        count_w = main_text.count(l_word)
        title_str = title + '|出会い系メール例文集'
        t_count = title_str.lower().count(l_word)
        h2_count = 0
        h3_count = 0
        h4_count = 0
        if h2_list:
            for h2 in h2_list:
                h2_count += h2.lower().count(l_word)
        else:
            h2_count = 'n'
        if h3_list:
            for h3 in h3_list:
                h3_count += h3.lower().count(l_word)
        else:
            h3_count = 'n'
        if h4_list:
            for h4 in h4_list:
                h4_count += h4.lower().count(l_word)
        else:
            h4_count = 'n'
        if h4_list:
            result_list.append(
                ' ' * (4 - len(str(word[1]))) + str(word[1]) + ' ' * (11 - len(str(word[2]))) + str(word[2]) +
                ' ' * (10 - len(str(count_w))) + str(count_w) + ' ' * (10 - len(str(t_count))) + str(t_count) +
                ' ' * (5 - len(str(h2_count))) + str(h2_count) + ' ' * (5 - len(str(h3_count))) + str(h3_count) +
                ' ' * (5 - len(str(h4_count))) + str(h4_count) + ' ' * 5 + word[0])
        elif not h3_list:
            result_list.append(
                ' ' * (4 - len(str(word[1]))) + str(word[1]) + ' ' * (11 - len(str(word[2]))) + str(word[2]) +
                ' ' * (10 - len(str(count_w))) + str(count_w) + ' ' * (10 - len(str(t_count))) + str(t_count) +
                ' ' * (5 - len(str(h2_count))) + str(h2_count) + ' ' * 5 + word[0])
        else:
            result_list.append(
                ' ' * (4 - len(str(word[1]))) + str(word[1]) + ' ' * (11 - len(str(word[2]))) + str(word[2]) +
                ' ' * (10 - len(str(count_w))) + str(count_w) + ' ' * (10 - len(str(t_count))) + str(t_count) +
                ' ' * (5 - len(str(h2_count))) + str(h2_count) + ' ' * (5 - len(str(h3_count))) + str(h3_count) +
                ' ' * 5 + word[0])
        if i < 10 and t_count < 1 and l_word not in ignore_list:
            c_str = combined_keyword_checker(l_word, words_list, title_str)
            if not c_str:
                top_words_data.append(
                    ' ' * (4 - len(str(word[1]))) + str(word[1]) + ' ' * (11 - len(str(word[2]))) + str(word[2]) +
                    ' ' * (10 - len(str(count_w))) + str(count_w) + ' ' * (10 - len(str(t_count))) + str(t_count) +
                    ' ' * 5 + word[0] + ' (' + str(i) + ')')
            else:
                c_list.append(c_str + str(i) + ')')
        i += 1
    if top_words_data:
        top_words_data.extend(c_list)
    return result_list, top_words_data

# todo: 調査済みデータのhtmlページ作成 リンク アップロード中にも見られるように tempから作成 アコーディオンで見やすいように
# todo: descriptionの検索


def combined_keyword_checker(c_word, words_list, title_str):
    if len(c_word) >= 3:
        for i in range(len(c_word) - 1):
            a_word = c_word[:i + 1]
            b_word = c_word[i + 1:]
            # print(a_word + ' : ' + b_word)
            if a_word in words_list and b_word in words_list:
                a_count = title_str.count(a_word)
                if a_count:
                    b_count = title_str.count(b_word)
                    if b_count:
                        return 'combined_key : {} + {} ('.format(a_word, b_word)
    return ''


def make_simple_keyword_dic(this_q_list):
    result = {}
    # print(this_q_list)
    for row in this_q_list:
        phrase_data = [int(row[0]), int(row[1]), float(row[2]), float(row[3])]
        if ' ' in row[4]:
            words = row[4].split(' ')
            for word in words:
                if word not in result:
                    result[word] = phrase_data
                else:
                    result[word] = [result[word][0] + phrase_data[0], result[word][1] + phrase_data[1],
                                    result[word][2] + phrase_data[2], result[word][3] + phrase_data[3]]
        else:
            word = row[4]
            if word not in result:
                result[word] = phrase_data
            else:
                result[word] = [result[word][0] + phrase_data[0], result[word][1] + phrase_data[1],
                                result[word][2] + phrase_data[2], result[word][3] + phrase_data[3]]
    # print(result)
    result = {x: [result[x][0], result[x][1], round(result[x][2], 2), round(result[x][3], 2)] for x in result}
    result_list = [[x] + result[x] for x in result if len(x) < 15 and (result[x][1] > 10 or result[x][0] > 0)]
    result_list.sort(key=lambda x: (x[1], x[2]), reverse=True)
    # print(result_list)
    return result_list


def check_list_and_bs(sc_list, pk_dic, limit_d, q_list, main_str_limit, today):
    i = 0
    target_list = []
    id_to_url = {pk_dic[x]['file_path']: x for x in pk_dic}
    for page in sc_list:
        page_name = page[0].replace('https://www.demr.jp/pc/', '')
        if page_name in id_to_url:
            # print('start : ' + page_name)
            click_num, view_num, order_num = page[1], page[2], page[4]
            this_query = [x for x in q_list if page[0] == x[5]]
            q_dic = make_simple_keyword_dic(this_query)
            this_pk_data = pk_dic[id_to_url[page_name]]
            error_list = seo_checker_to_pk_data(this_pk_data, main_str_limit, limit_d, today)
            query_str_list, top_words = seo_checker_by_query(this_pk_data, q_dic)
            if error_list:
                print('\n{} : {}  ({})'.format(page_name, this_pk_data['title'], str(len(this_pk_data['title']))))
                print(error_list)
                print('   {}        {}      {}'.format(click_num, view_num, order_num))
                # for qs in query_str_list:
                #     print(qs)
                # get_gsc_query(page_name, q_list)
                i += 1
                target_list.append(page_name)
            elif top_words:
                print('\n{} : {}  ({})'.format(page_name, this_pk_data['title'], str(len(this_pk_data['title']))))
                print('   {}        {}      {}'.format(click_num, view_num, order_num))
                for tw in top_words:
                    print(tw)
                # for qs in query_str_list:
                #     print(qs)
                # get_gsc_query(page_name, q_list)
                i += 1
        else:
            print('url not in : ' + page_name)
        if i >= 10:
            break
    return target_list


def read_md_page(page_url):
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


if __name__ == '__main__':
    next_update_target_search(100, 28, 3000, 'reibun')
