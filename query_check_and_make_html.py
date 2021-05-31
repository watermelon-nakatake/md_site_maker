import csv
import datetime
import os
import re
import pickle
from datetime import datetime, timedelta
import search_console_data
import get_gsc_every_day_data

project_info = {
    'reibun': {'pj_dir': 'reibun', 'pj_domain': 'https://www.demr.jp',
               'main_dir': 'reibun/html_files/pc/', 'site_name': '出会い系メール例文集'},
    'rei_site': {'pj_dir': 'rei_site', 'pj_domain': 'https://www.reibunsite.com',
                 'main_dir': 'rei_site/html_files/pc/', 'site_name': '出会い系メールの例文サイト'},
    'joshideai': {'pj_dir': 'joshideai', 'pj_domain': 'https://www.joshideai.com',
                  'main_dir': 'joshideai/html_files/', 'site_name': '出会い系メールの例文サイト'},
    'sfd': {'pj_dir': 'sfd', 'pj_domain': 'https://www.sefure-do.com', 'main_dir': '', 'site_name': 'セフレ道'}}


def make_data_for_graph(pj_dir, start_period, end_period, domain):
    main_dict = {}
    start = datetime.strptime(start_period, '%Y-%m-%d').date()
    end = datetime.strptime(end_period, '%Y-%m-%d').date()
    days_list = [(start + timedelta(n)).strftime('%Y-%m-%d') for n in range((end - start).days + 1)]
    # print(days_list)
    for day_str in days_list:
        if os.path.exists('gsc_data/' + pj_dir + '/ed_data/od' + day_str + '.csv'):
            with open('gsc_data/' + pj_dir + '/ed_data/od' + day_str + '.csv') as f:
                reader = csv.reader(f)
                csv_list = [row for row in reader]
            for page_data in csv_list[1:]:
                if page_data[4] == 'https://www.demr.jp/':
                    page_name = 'top'
                else:
                    page_name = page_data[4].replace(domain + '/', '')
                if page_name in main_dict:
                    main_dict[page_name][day_str] = [int(page_data[0]), int(page_data[1]),
                                                     round(float(page_data[3]), 2)]
                else:
                    main_dict[page_name] = {day_str: [int(page_data[0]), int(page_data[1]),
                                                      round(float(page_data[3]), 2)]}
        if 'day_key' not in main_dict:
            main_dict['day_key'] = [day_str]
        else:
            main_dict['day_key'].append(day_str)
    # print(main_dict)
    with open(pj_dir + '/pickle_pot/gsc_page_data.pkl', 'wb') as p:
        pickle.dump(main_dict, p)


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
    i = 0
    end_str = (today - timedelta(days=3)).strftime('%Y-%m-%d')
    if not os.path.exists('gsc_data/' + pj_dir):
        os.mkdir('gsc_data/' + pj_dir)
    if not os.path.exists('gsc_data/' + pj_dir + '/ed_data'):
        os.mkdir('gsc_data/' + pj_dir + '/ed_data')
    while i < 3:
        if os.path.exists('gsc_data/' + pj_dir + '/ed_data/ed' + (today - timedelta(days=i)).strftime('%Y-%m-%d')
                          + '.csv'):
            end_str = (today - timedelta(days=i)).strftime('%Y-%m-%d')
            print(i)
            print('gsc_data/' + pj_dir + '/ed_data/ed' + (today - timedelta(days=i)).strftime('%Y-%m-%d') + '.csv')
            break
        i += 1
    print(end_str)
    start_d = today - timedelta(days=(period + i))
    start_str = start_d.strftime('%Y-%m-%d')
    if period == 28:
        period_name = 'month'
    elif period == 7:
        period_name = 'week'
    else:
        period_name = str(period) + '_'
    if not os.path.exists('gsc_data/' + pj_dir + '/p_' + period_name + end_str + '.csv'):
        print('connect to search console')
        search_console_data.make_csv_from_gsc(domain, start_str, end_str, pj_dir,
                                              'qp_' + period_name, ['query', 'page'])
        search_console_data.make_csv_from_gsc(domain, start_str, end_str, pj_dir,
                                              'p_' + period_name, ['page'])
    return end_str


def project_select(file_path):
    project_str = re.sub(r'^(.+?)/.*$', r'\1', file_path)
    if project_str in project_info:
        pj_dir = project_info[project_str]['pj_dir']
        domain = project_info[project_str]['pj_domain']
        main_dir = project_info[project_str]['main_dir']
        site_name = project_info[project_str]['site_name']
        pj_domain_main = domain + re.sub(r'^.*/html_files', '', main_dir)
    else:
        pj_dir, domain, main_dir, site_name, pj_domain_main = '', '', '', '', ''
    return pj_dir, domain, main_dir, site_name, pj_domain_main


def check_single_page_seo(period, html_path, ignore_flag):
    main_str_limit = 5000
    limit_d = 100
    today = datetime.today()
    if '.md' in html_path:
        html_path = html_path.replace('.md', '.html').replace('/md_files/', '/html_files/')
    pj_dir, domain, main_dir, site_name, pj_domain_main = project_select(html_path)
    end_date = make_target_data_for_today(today, period, pj_dir, domain)
    if period == 28:
        period_name = 'month'
    elif period == 7:
        period_name = 'week'
    else:
        period_name = str(period) + '_'
    with open('gsc_data/' + pj_dir + '/p_' + period_name + end_date + '.csv') as f:
        reader = csv.reader(f)
        csv_list = [row for row in reader]
    c_list = sc_data_match_page(csv_list, domain)
    with open('gsc_data/' + pj_dir + '/qp_' + period_name + end_date + '.csv') as f:
        q_reader = csv.reader(f)
        q_list = [row for row in q_reader]
    q_list = q_list[1:]
    with open(pj_dir + '/pickle_pot/main_data.pkl', 'rb') as f:
        pk_dic = pickle.load(f)
    e_pk_dic = {pk_dic[x]['file_path']: pk_dic[x] for x in pk_dic}
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
    query_str_list, top_words, h_result, t_result, e_q_list = \
        seo_checker_by_query(this_pk_data, q_dic, pj_dir, q_list, pj_domain_main, e_pk_dic, site_name, ignore_flag)
    if top_words:
        for tw in top_words:
            print(tw)
    for qs in query_str_list:
        print(qs)
    get_gsc_query(page_name, q_list)


def next_update_target_search(limit_d, period, main_str_limit, target_project, print_flag, ma_flag, ignore_flag):
    today = datetime.today()
    pj_dir, domain, main_dir, site_name, pj_domain_main = project_select(target_project + '/')
    end_date = make_target_data_for_today(today, period, pj_dir, domain)
    if period == 28:
        period_name = 'month'
    elif period == 7:
        period_name = 'week'
    else:
        period_name = str(period) + '_'
    with open('gsc_data/' + pj_dir + '/p_' + period_name + end_date + '.csv') as f:
        reader = csv.reader(f)
        csv_list = [row for row in reader]
    c_list = sc_data_match_page(csv_list, domain)
    with open('gsc_data/' + pj_dir + '/qp_' + period_name + end_date + '.csv') as f:
        q_reader = csv.reader(f)
        q_list = [row for row in q_reader]
    q_list = q_list[1:]
    # print(c_list)
    with open(pj_dir + '/pickle_pot/main_data.pkl', 'rb') as f:
        pk_dic = pickle.load(f)
    # print(pk_dic)
    e_pk_dic = {pk_dic[x]['file_path']: pk_dic[x] for x in pk_dic}
    # print(q_list)
    print('日数 : ' + str(period) + '日間')
    # print('クリック数順')
    check_list_and_bs(c_list, e_pk_dic, limit_d, q_list, main_str_limit, today, print_flag, ma_flag, end_date, period,
                      target_project, ignore_flag)


def get_gsc_query(target_page, q_list):
    filtered_data = [x for x in q_list if target_page in x[5]]
    filtered_data.sort(key=lambda x: (int(x[0]), int(x[1]), float(x[3])), reverse=True)
    print('クリック   表示回数    平均順位       クエリ')
    for d_r in filtered_data:
        position = str(round(float(d_r[3]), 1))
        print(' ' * (4 - len(d_r[0])) + d_r[0] + ' ' * (11 - len(d_r[1])) + d_r[1] +
              ' ' * (10 - len(position)) + position + ' ' * 6 + d_r[4])


def get_gsc_query_for_html(target_page, q_list):
    filtered_data = [[x[4], int(x[0]), int(x[1]), round(float(x[3]), 2), x[6], x[7], x[8], x[9]] for x in q_list
                     if target_page in x[5]]
    filtered_data.sort(key=lambda x: (x[1], x[2], x[3]), reverse=True)
    return filtered_data


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


def seo_checker_by_query(pk_data, q_dic, pj_dir, q_list, pj_domain_main, e_pk_dic, site_name, ignore_flag):
    result_list = []
    h_result = []
    t_result = []
    top_words_data = []
    c_list = []
    ignore_list = []
    e_q_list = []
    if 'ign_words' in pk_data and ignore_flag:
        ignore_list.extend(pk_data['ign_words'])
    with open(pj_dir + '/md_files/pc/' + pk_data['file_path'].replace('.html', '.md'), 'r', encoding='utf-8') as f:
        long_str = f.read()
    main_text = re.sub(r'^[\S\s]*\n# .+?\n', '', long_str)
    main_text = re.sub(r'%kanren%[\S\s]*$', '', main_text)
    main_text = re.sub(r']\(.+?\)', ']', main_text)
    main_text = main_text.replace('\n', '')
    main_text = main_text.lower()
    title = re.findall(r't::(.+?)\n', long_str)[0]
    description = re.findall(r'd::(.+?)\n', long_str)[0]
    h2_list = re.findall(r'\n## (.+?)\n', long_str)
    h3_list = re.findall(r'\n### (.+?)\n', long_str)
    h4_list = re.findall(r'\n#### (.+?)\n', long_str)
    if h4_list:
        result_list.append('click   表示      main   title  des   h2   h3   h4   keyword')
        h_result.append(['keyword', 'click', '表示', 'main', 'title', 'des', 'h2', 'h3', 'h4'])
    elif not h3_list:
        result_list.append('click   表示      main   title  des   h2   keyword')
        h_result.append(['keyword', 'click', '表示', 'main', 'title', 'des', 'h2'])
    else:
        result_list.append('click   表示      main   title  des   h2   h3   keyword')
        h_result.append(['keyword', 'click', '表示', 'main', 'title', 'des', 'h2', 'h3'])
    i = 0
    words_list = [x[0] for x in q_dic]
    for word in q_dic:
        l_word = word[0].lower()
        l_word = l_word.replace('出会系', '出会い系')
        count_w = main_text.count(l_word)
        title_str = title + '|' + site_name
        t_count = title_str.lower().count(l_word)
        d_count = description.lower().count(l_word)
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
                ' ' * (4 - len(str(word[1]))) + str(word[1]) + ' ' * (7 - len(str(word[2]))) + str(word[2]) +
                ' ' * (10 - len(str(count_w))) + str(count_w) + ' ' * (8 - len(str(t_count))) + str(t_count) +
                ' ' * (5 - len(str(d_count))) + str(d_count) + ' ' * (5 - len(str(h2_count))) + str(h2_count) +
                ' ' * (5 - len(str(h3_count))) + str(h3_count) + ' ' * (5 - len(str(h4_count))) + str(h4_count) +
                ' ' * 5 + word[0])
            h_result.append([word[0], word[1], word[2], count_w, t_count, d_count, h2_count, h3_count, h4_count])
        elif not h3_list:
            result_list.append(
                ' ' * (4 - len(str(word[1]))) + str(word[1]) + ' ' * (7 - len(str(word[2]))) + str(word[2]) +
                ' ' * (10 - len(str(count_w))) + str(count_w) + ' ' * (8 - len(str(t_count))) + str(t_count) +
                ' ' * (5 - len(str(d_count))) + str(d_count) + ' ' * (5 - len(str(h2_count))) + str(h2_count) +
                ' ' * 5 + word[0])
            h_result.append([word[0], word[1], word[2], count_w, t_count, d_count, h2_count])
        else:
            result_list.append(
                ' ' * (4 - len(str(word[1]))) + str(word[1]) + ' ' * (7 - len(str(word[2]))) + str(word[2]) +
                ' ' * (10 - len(str(count_w))) + str(count_w) + ' ' * (8 - len(str(t_count))) + str(t_count) +
                ' ' * (5 - len(str(d_count))) + str(d_count) + ' ' * (5 - len(str(h2_count))) + str(h2_count) +
                ' ' * (5 - len(str(h3_count))) + str(h3_count) + ' ' * 5 + word[0])
            h_result.append([word[0], word[1], word[2], count_w, t_count, d_count, h2_count, h3_count])
        if i < 10 and t_count < 1 < word[1] and l_word not in ignore_list:
            c_str = combined_keyword_checker(l_word, words_list, title_str)
            if not c_str:
                top_words_data.append(
                    ' ' * (4 - len(str(word[1]))) + str(word[1]) + ' ' * (11 - len(str(word[2]))) + str(word[2]) +
                    ' ' * (10 - len(str(count_w))) + str(count_w) + ' ' * (10 - len(str(t_count))) + str(t_count) +
                    ' ' * 5 + word[0] + ' (' + str(i) + ')')
                t_result.append([i + 1, word[0], word[1], word[2], count_w, t_count, d_count, h2_count])
                another_page_data = check_keyword_in_another_page(l_word, q_list, pk_data['file_path'], pj_domain_main,
                                                                  e_pk_dic)
                if another_page_data:
                    t_result.extend(another_page_data)
            else:
                c_list.append('clear_by_combined_key : ' + c_str + '(' + str(i) + ')')
                t_result.append([i + 1, c_str, word[1], word[2], count_w, t_count, d_count, h2_count])
        i += 1
    if top_words_data:
        top_words_data.extend(c_list)
    for q_row in q_list:
        if ' ' in q_row[4]:
            qw_str = []
            qt_str = []
            qd_str = []
            qh_str = []
            for s_word in q_row[4].split(' '):
                for h_row in h_result:
                    if s_word == h_row[0]:
                        qw_str.append(str(h_row[3]))
                        qt_str.append(str(h_row[4]))
                        qd_str.append(str(h_row[5]))
                        qh_str.append(str(h_row[6]))
                        break
            e_q_list.append(q_row + [' + '.join(qw_str), ' + '.join(qt_str), ' + '.join(qd_str), ' + '.join(qh_str)])
        else:
            for o_row in h_result:
                if q_row[4] == o_row[0]:
                    e_q_list.append(q_row + [str(o_row[3]), str(o_row[4]), str(o_row[5]), str(o_row[6])])
    return result_list, top_words_data, h_result, t_result, e_q_list


def check_keyword_in_another_page(keyword, q_list, this_path, pj_domain_main, e_pk_dic):
    result = []
    i = 0
    for row in q_list:
        if keyword in row[4]:
            if this_path in row[5]:
                break
            elif i < 5:
                this_page = row[5].replace(pj_domain_main, '')
                if 'sitepage/' in this_page:
                    if this_page == 'sitepage/mintj.html':
                        result.append([this_page, row[4], row[0], row[1], '', 'Jメール', '', ''])
                else:
                    result.append([this_page, row[4], row[0], row[1], '', e_pk_dic[this_page]['title'].count(keyword),
                                   '', ''])
                i += 1
            else:
                result.append(['', 'and more', '', '', '', '', '', ''])
                break
    return result


def make_seo_html_file(html_dic, pj_dir, pj_main_domain, ma_flag, end_day_str, period, domain):
    with open(pj_dir + '/pickle_pot/gsc_page_data.pkl', 'rb') as h:
        gsc_dic = pickle.load(h)
    if end_day_str not in gsc_dic['day_key']:
        print('no ' + end_day_str)
        get_gsc_every_day_data.get_one_day_data_in_period(pj_main_domain.replace('/pc', '/'), '2020-04-01',
                                                          end_day_str, pj_dir)
        make_data_for_graph(pj_dir, '2020-04-01', end_day_str, domain)
        with open(pj_dir + '/pickle_pot/gsc_page_data.pkl', 'rb') as i:
            gsc_dic = pickle.load(i)
    with open(pj_dir + '/sc_data_temp.html', 'r', encoding='utf-8') as f:
        base_str = f.read()
    index_str = '<table class="i_data"><thead><tr><th>rank</th><th class="w40">title</th><th>url</th><th>未使用</th>' \
                '<th>キーワード</th><th>フレーズ</th></tr></thead><tbody>'
    content_t = ''
    js_str = ''
    id_num = 0
    last_id = len(html_dic)
    label_data = gsc_dic['day_key'][-90:]
    for p_name in html_dic:
        id_num += 1
        page = html_dic[p_name]
        content_t += '<div class="page_data"><div class="title" id="d' + str(id_num) + '_0">' + page['title'] + \
                     '</div><div class="url"><a href="' + pj_main_domain + page['path'] + '" target="_blank">' \
                     + page['path'] + '</a></div>'
        if id_num != last_id:
            content_t += '<div class="next"><a href="#d' + str(id_num + 1) + '_0">NEXT PAGE</a></div>'
        content_t += '<table class="m_data"><thead><tr><th>rank</th><th>click</th><th>表示</th><th>平均順位</th>' + \
                     '<th>更新</th><th>len</th></tr></thead><tbody><tr><td>' + str(page['rank']) + '</td><td>' + \
                     str(page['page_data'][0]) + '</td><td>' + str(page['page_data'][1]) + '</td><td>' + \
                     str(page['page_data'][2]) + '</td><td>' + str(page['mod_date']) + '</td><td>' + \
                     str(page['title_len']) + '</td></tr></tbody></table>'
        index_str += '<tr><td>' + str(page['rank']) + '</td><td>' + page['title'] + '</td><td><a href="#d' + \
                     str(id_num) + '_0">' + page['path'] + '</a></td><td><a href="#d' + str(id_num) + \
                     '_1">未使用</a></td><td><a href="#d' + str(id_num) + '_2">キーワード</a></td><td><a href="#d' \
                     + str(id_num) + '_3">フレーズ</a></td></tr>'
        long_name = 'pc/' + p_name
        label_data_e = [re.sub(r'^.\d*?-', '', x).replace('-', '/') for x in label_data]
        if long_name in gsc_dic:
            click_data = []
            imp_data = []
            pos_data = []
            if ma_flag:
                p_click_data = []
                p_imp_data = []
                p_pos_data = []
                for day_str in label_data:
                    if day_str in gsc_dic[long_name]:
                        p_click_data.append(gsc_dic[long_name][day_str][0])
                        p_imp_data.append(gsc_dic[long_name][day_str][1])
                        p_pos_data.append(gsc_dic[long_name][day_str][2])
                    else:
                        p_click_data.append(0)
                        p_imp_data.append(0)
                        p_pos_data.append(0)
                click_data = [str(round(sum(x) / 7, 2)) for x in
                              zip(p_click_data[:-6], p_click_data[1:-5], p_click_data[2:-4],
                                  p_click_data[3:-3], p_click_data[4:-2], p_click_data[5:-1],
                                  p_click_data[6:])]
                imp_data = [str(round(sum(x) / 7)) for x in zip(p_imp_data[:-6], p_imp_data[1:-5], p_imp_data[2:-4],
                                                                p_imp_data[3:-3], p_imp_data[4:-2], p_imp_data[5:-1],
                                                                p_imp_data[6:])]
                pos_data = [str(round(sum(x) / 7, 2)) for x in zip(p_pos_data[:-6], p_pos_data[1:-5], p_pos_data[2:-4],
                                                                   p_pos_data[3:-3], p_pos_data[4:-2], p_pos_data[5:-1],
                                                                   p_pos_data[6:])]
                label_data_e = label_data_e[6:]
            else:
                for day_str in label_data:
                    if day_str in gsc_dic[long_name]:
                        click_data.append(str(gsc_dic[long_name][day_str][0]))
                        imp_data.append(str(gsc_dic[long_name][day_str][1]))
                        pos_data.append(str(gsc_dic[long_name][day_str][2]))
                    else:
                        click_data.append('0')
                        imp_data.append('0')
                        pos_data.append('0')
            content_t += '<canvas id="chart' + str(id_num) + '"></canvas>' + \
                         '<script>let ctx' + str(id_num) + '=document.getElementById("chart' + str(id_num) + '");' + \
                         "let chart" + str(id_num) + "=new Chart(ctx" + str(id_num) + ",{type:'line',data:{labels:['" + \
                         "','".join(label_data_e) + "'],datasets:[{label:'click',data:[" + ','.join(click_data) + \
                         '],borderColor:"rgba(255,0,0,1)",backgroundColor:"rgba(0,0,0,0)",yAxisID:"y-axis-1"},' + \
                         "{label:'impressions',data:[" + ','.join(imp_data) + \
                         '],borderColor:"rgba(0,0,255,1)",backgroundColor:"rgba(0,0,0,0)",' + \
                         "yAxisID:'y-axis-2'}," + "{label:'positions',data:[" + ','.join(pos_data) + \
                         '],borderColor:"rgba(0,255,0,1)",backgroundColor:"rgba(0,0,0,0)",' + \
                         "yAxisID:'y-axis-1'}],}" + ",options:{scales:{yAxes:[{id:'y-axis-1',type:'linear'," + \
                         "position:'left', ticks: {stepSize: 10,suggestedMin: 0}}," + \
                         "{id: 'y-axis-2', type: 'linear', position: 'right', ticks: {stepSize: 100," + \
                         "suggestedMin: 0}}]},}});</script>"
        if 't_result' in page:
            content_t += '<div class="table_name" id="d' + str(id_num) + '_1">未使用重要ワード</div>' + \
                         '<div class="next"><a href="#d' + str(id_num) + '_2">NEXT</a></div>' + \
                         '<table class="t_data"><thead><tr><th>rank</th><th>word</th><th>click</th>' + \
                         '<th>表示</th><th>main</th><th>title</th><th>des</th><th>h2</th></tr></thead><tbody>'
            for t_row in page['t_result']:
                content_t += '<tr>'
                for t_i, t_d in enumerate(t_row):
                    if t_i == 0 and type(t_d) != int:
                        content_t += '<td><a href="' + pj_main_domain + t_d + '" target="_blank">' + \
                                     '<span class="blue">' + t_d + '</span></a></td>'
                    elif t_i == 1 and ' + ' in t_d:
                        content_t += '<td><span class="blue">' + str(t_d) + '</span></td>'
                    else:
                        content_t += '<td>' + str(t_d) + '</td>'
                content_t += '</tr>'
            content_t += '</tbody></table>'

        if 'h_result' in page:
            if len(page['h_result']) > 11:
                content_t += '<div class="table_name" id="d' + str(id_num) + '_2">ワード使用状況</div>' + \
                             '<div class="ac_btn" id="btn' + str(id_num) + 'w">OPEN</div><div class="next">' + \
                             '<a href="#d' + str(id_num) + '_3">NEXT</a></div><table class="h_data"><thead><tr>' + \
                             '<th>rank</th>'
                js_str += "let btn" + str(id_num) + "w=document.getElementById('btn" + str(id_num) + "w');let tr" \
                          + str(id_num) + "w=document.getElementsByClassName('tr" + str(id_num) + "w');btn" + \
                          str(id_num) + "w.addEventListener('click',()=>{if (tr" + str(id_num) + "w[0].classList" \
                          + ".contains('close')===true){btn" + str(id_num) + "w.innerText='CLOSE';for(let i=0;i<tr" \
                          + str(id_num) + "w.length;i++){tr" + str(id_num) + "w[i].classList.remove('close');}}" + \
                          "else{btn" + str(id_num) + "w.innerText='OPEN';for(let i=0;i<tr" + str(id_num) + \
                          "w.length;i++){tr" + str(id_num) + "w[i].classList.add('close');}}});"
            else:
                content_t += '<div class="table_name" id="d' + str(id_num) + '_2">ワード使用状況</div><div class="next">' \
                             + '<a href="#d' + str(id_num) + '_3">NEXT</a></div><table class="h_data"><thead><tr>' + \
                             '<th>rank</th>'
            for thd_i, t_hd in enumerate(page['h_result'][0]):
                if thd_i == 0:
                    content_t += '<th class="w30">' + str(t_hd) + '</th>'
                else:
                    content_t += '<th>' + str(t_hd) + '</th>'
            content_t += '</tr></thead><tbody>'
            for hi, h_row in enumerate(page['h_result'][1:], 1):
                if hi > 20:
                    content_t += '<tr class="tr' + str(id_num) + 'w close"><td>' + str(hi) + '</td>'
                else:
                    content_t += '<tr><td>' + str(hi) + '</td>'
                for hdi, h_d in enumerate(h_row):
                    if hdi in [4, 5] and hi <= 10 and h_d == 0:
                        content_t += '<td><span class="red">' + str(h_d) + '</span></td>'
                    elif hdi in [6] and hi <= 20 and h_d == 0:
                        content_t += '<td><span class="red">' + str(h_d) + '</span></td>'
                    elif hdi == 3 and hi <= 30 and h_d == 0:
                        content_t += '<td><span class="red">' + str(h_d) + '</span></td>'
                    else:
                        content_t += '<td>' + str(h_d) + '</td>'
                content_t += '</tr>'
            content_t += '</tbody></table>'

        if 'query' in page:
            if len(page['query']) > 10:
                content_t += '<div class="table_name" id="d' + str(id_num) + '_3">クエリ</div>' + \
                             '<div class="ac_btn" id="btn' + str(id_num) + 'q">OPEN</div>'
                if id_num != last_id:
                    content_t += '<div class="next"><a href="#d' + str(id_num + 1) + '_0">NEXT</a></div>'
                content_t += '<table class="h_data"><thead><tr><th>rk</th><th class="w30">フレーズ</th>' \
                             '<th>cl</th><th>表示</th><th>順位</th><th>main</th><th>title</th><th>des</th>' \
                             '<th>h2</th></tr></thead><tbody>'
                js_str += "let btn" + str(id_num) + "q=document.getElementById('btn" + str(id_num) + "q');let tr" \
                          + str(id_num) + "q=document.getElementsByClassName('tr" + str(id_num) + "q');btn" + \
                          str(id_num) + "q.addEventListener('click',()=>{if (tr" + str(id_num) + "q[0].classList" \
                          + ".contains('close')===true){btn" + str(id_num) + "q.innerText='CLOSE';for(let i=0;i<tr" \
                          + str(id_num) + "q.length;i++){tr" + str(id_num) + "q[i].classList.remove('close');}}" + \
                          "else{btn" + str(id_num) + "q.innerText='OPEN';for(let i=0;i<tr" + str(id_num) + \
                          "q.length;i++){tr" + str(id_num) + "q[i].classList.add('close');}}});"
            else:
                content_t += '<div class="table_name" id="d' + str(id_num) + '_3">クエリ</div><div class="next">' + \
                             '<a href="#d' + str(id_num + 1) + '_0">NEXT</a></div><table class="raw_q">' + \
                             '<thead><tr><th>rk</th><th class="w30">フレーズ</th><th>cl</th><th>表示</th>' + \
                             '<th>順位</th><th>main</th><th>title</th><th>des</th><th>h2</th></tr></thead><tbody>'
            for qi, q_row in enumerate(page['query'], 1):
                if qi > 10:
                    content_t += '<tr class="tr' + str(id_num) + 'q close"><td>' + str(qi) + '</td>'
                else:
                    content_t += '<tr><td>' + str(qi) + '</td>'
                for qdi, q_d in enumerate(q_row):
                    if qi <= 10 and qdi >= 5:
                        if q_d == '0':
                            content_t += '<td><span class="red">0</span></td>'
                        elif ' 0' in q_d:
                            content_t += '<td>' + q_d.replace(' 0', ' <span class="red">0</span>') + '</td>'
                        elif '0 ' in q_d:
                            content_t += '<td>' + re.sub(r'^0', '<span class="red">0</span>', q_d) + '</td>'
                        else:
                            content_t += '<td>' + q_d + '</td>'
                    else:
                        content_t += '<td>' + str(q_d) + '</td>'
                content_t += '</tr>'
            content_t += '</tbody></table>'
        content_t += '</div>'
    index_str += '</tbody></table>'
    base_str = base_str.replace('<!--insert-->', content_t)
    base_str = base_str.replace('<!--index-->', index_str)
    base_str = base_str.replace('<!--period-->', '{}日間'.format(period))
    if js_str:
        base_str = base_str.replace('<!--script-->', '<script>' + js_str + '</script>')
    if period == 28:
        period_name = 'month'
    elif period == 7:
        period_name = 'week'
    else:
        period_name = str(period)
    with open(pj_dir + '/sc_data_' + period_name + '.html', 'w', encoding='utf-8') as g:
        g.write(base_str)


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
                        return '{} + {}'.format(a_word, b_word)
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
    result_list = [[x] + result[x] for x in result if len(x) < 15]
    result_list.sort(key=lambda x: (x[1], x[2]), reverse=True)
    # print(result_list)
    return result_list


def insert_ignore_key_to_pk_dic(target_project, path, keyword_list):
    with open(target_project + '/pickle_pot/main_data.pkl', 'rb') as f:
        pk_dic = pickle.load(f)
    for p_id in pk_dic:
        if path == pk_dic[p_id]['file_path']:
            if 'ign_words' not in pk_dic[p_id]:
                pk_dic[p_id]['ign_words'] = keyword_list
            else:
                new_ign = list(set(pk_dic[p_id]['ign_words'] + keyword_list))
                pk_dic[p_id]['ign_words'] = new_ign
            print(pk_dic[p_id])
    with open(target_project + '/pickle_pot/main_data.pkl', 'wb') as p:
        pickle.dump(pk_dic, p)


def check_list_and_bs(sc_list, pk_dic, limit_d, q_list, main_str_limit, today, print_flag, ma_flag, end_date, period,
                      target_project, ignore_flag):
    i = 0
    target_list = []
    html_dic = {}
    pj_dir, domain, main_dir, site_name, pj_domain_main = project_select(target_project + '/')
    for rank, page in enumerate(sc_list, 1):
        page_name = page[0].replace(pj_domain_main, '')
        if page_name in pk_dic:
            # print('start : ' + page_name)
            click_num, view_num, order_num = page[1], page[2], page[4]
            this_query = [x for x in q_list if page[0] == x[5]]
            q_dic = make_simple_keyword_dic(this_query)
            this_pk_data = pk_dic[page_name]
            error_list = seo_checker_to_pk_data(this_pk_data, main_str_limit, limit_d, today)
            query_str_list, top_words, h_result, t_result, e_q_list \
                = seo_checker_by_query(this_pk_data, q_dic, pj_dir, q_list, pj_domain_main, pk_dic, site_name,
                                       ignore_flag)
            if error_list:
                print('\n{} : {}  ({})'.format(page_name, this_pk_data['title'], str(len(this_pk_data['title']))))
                print(error_list)
                print('{}   {}        {}      {}'.format(str(rank), click_num, view_num, order_num))
                if print_flag:
                    for qs in query_str_list:
                        print(qs)
                    get_gsc_query(page_name, q_list)
                i += 1
                html_dic[page_name] = {'h_result': h_result, 't_result': t_result, 'title': this_pk_data['title'],
                                       'path': page_name, 'query': get_gsc_query_for_html(page_name, e_q_list),
                                       'rank': rank, 'page_data': [click_num, view_num, order_num],
                                       'mod_date': this_pk_data['mod_date'], 'title_len': len(this_pk_data['title'])}
            elif top_words:
                print('\n{} : {}  ({})'.format(page_name, this_pk_data['title'], str(len(this_pk_data['title']))))
                print('{}   {}        {}      {}'.format(str(rank), click_num, view_num, order_num))
                for tw in top_words:
                    print(tw)
                if print_flag:
                    for qs in query_str_list:
                        print(qs)
                    get_gsc_query(page_name, q_list)
                i += 1
                html_dic[page_name] = {'h_result': h_result, 't_result': t_result, 'title': this_pk_data['title'],
                                       'path': page_name, 'query': get_gsc_query_for_html(page_name, e_q_list),
                                       'rank': rank, 'page_data': [click_num, view_num, order_num],
                                       'mod_date': this_pk_data['mod_date'], 'title_len': len(this_pk_data['title'])}
        else:
            print('url not in : ' + page_name)
        if i >= 5:
            break
    if html_dic:
        make_seo_html_file(html_dic, pj_dir, pj_domain_main, ma_flag, end_date, period, domain)
    return target_list


if __name__ == '__main__':
    target_prj = 'reibun'
    # insert_ignore_key_to_pk_dic(target_prj, 'majime/kakikata_f.html', ['ファーストメッセージ'])
    next_update_target_search(100, 28, 3000, target_prj, False, True, False)
    # make_data_for_graph('reibun', '2020-04-01', '2021-05-04')
