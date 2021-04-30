import csv
import datetime
import os
import re
import pickle
from datetime import datetime, timedelta
import search_console_data


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
    query_str_list, top_words, h_result, t_result = seo_checker_by_query(this_pk_data, q_dic)
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
    h_result = []
    t_result = []
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
    description = re.findall(r'd::(.+?)\n', long_str)[0]
    h2_list = re.findall(r'\n## (.+?)\n', long_str)
    h3_list = re.findall(r'\n### (.+?)\n', long_str)
    h4_list = re.findall(r'\n#### (.+?)\n', long_str)
    if h4_list:
        result_list.append('クリック   表示回数      main   title  des   h2   h3   h4   キーワード')
    elif not h3_list:
        result_list.append('クリック   表示回数      main   title  des   h2   キーワード')
    else:
        result_list.append('クリック   表示回数      main   title  des   h2   h3   キーワード')
    i = 0
    words_list = [x[0] for x in q_dic]
    for word in q_dic:
        l_word = word[0].lower()
        count_w = main_text.count(l_word)
        title_str = title + '|出会い系メール例文集'
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
                ' ' * (4 - len(str(word[1]))) + str(word[1]) + ' ' * (11 - len(str(word[2]))) + str(word[2]) +
                ' ' * (10 - len(str(count_w))) + str(count_w) + ' ' * (8 - len(str(t_count))) + str(t_count) +
                ' ' * (5 - len(str(d_count))) + str(d_count) + ' ' * (5 - len(str(h2_count))) + str(h2_count) +
                ' ' * (5 - len(str(h3_count))) + str(h3_count) + ' ' * (5 - len(str(h4_count))) + str(h4_count) +
                ' ' * 5 + word[0])
            h_result.append([word[0], word[1], word[2], count_w, t_count, d_count, h2_count, h3_count, h4_count])
        elif not h3_list:
            result_list.append(
                ' ' * (4 - len(str(word[1]))) + str(word[1]) + ' ' * (11 - len(str(word[2]))) + str(word[2]) +
                ' ' * (10 - len(str(count_w))) + str(count_w) + ' ' * (8 - len(str(t_count))) + str(t_count) +
                ' ' * (5 - len(str(d_count))) + str(d_count) + ' ' * (5 - len(str(h2_count))) + str(h2_count) +
                ' ' * 5 + word[0])
            h_result.append([word[0], word[1], word[2], count_w, t_count, d_count, h2_count])
        else:
            result_list.append(
                ' ' * (4 - len(str(word[1]))) + str(word[1]) + ' ' * (11 - len(str(word[2]))) + str(word[2]) +
                ' ' * (10 - len(str(count_w))) + str(count_w) + ' ' * (8 - len(str(t_count))) + str(t_count) +
                ' ' * (5 - len(str(d_count))) + str(d_count) + ' ' * (5 - len(str(h2_count))) + str(h2_count) +
                ' ' * (5 - len(str(h3_count))) + str(h3_count) + ' ' * 5 + word[0])
            h_result.append([word[0], word[1], word[2], count_w, t_count, d_count, h2_count, h3_count])
        if i < 10 and t_count < 1 and l_word not in ignore_list:
            c_str = combined_keyword_checker(l_word, words_list, title_str)
            if not c_str:
                top_words_data.append(
                    ' ' * (4 - len(str(word[1]))) + str(word[1]) + ' ' * (11 - len(str(word[2]))) + str(word[2]) +
                    ' ' * (10 - len(str(count_w))) + str(count_w) + ' ' * (10 - len(str(t_count))) + str(t_count) +
                    ' ' * 5 + word[0] + ' (' + str(i) + ')')
                t_result.append([word[0], word[1], word[2], count_w, t_count, d_count, h2_count])
            else:
                c_list.append(c_str + str(i) + ')')
        i += 1
    if top_words_data:
        top_words_data.extend(c_list)
        t_result.extend(c_list)
    return result_list, top_words_data, h_result, t_result

# todo: 調査済みデータのhtmlページ作成 リンク アップロード中にも見られるように tempから作成 アコーディオンで見やすいように


def make_seo_html_file(html_dic, q_list):
    content_t = ''
    if t_result:
        for t_row in t_result:
            content_t += '<tr>'
            for t_d in t_row:
                content_t += '<td>' + str(t_d) + '</td>'
            content_t += '</tr>'



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
                        return 'clear_by_combined_key : {} + {} ('.format(a_word, b_word)
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
    html_dic = {}
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
            query_str_list, top_words, h_result, t_result = seo_checker_by_query(this_pk_data, q_dic)
            if error_list:
                print('\n{} : {}  ({})'.format(page_name, this_pk_data['title'], str(len(this_pk_data['title']))))
                print(error_list)
                print('   {}        {}      {}'.format(click_num, view_num, order_num))
                # for qs in query_str_list:
                #     print(qs)
                # get_gsc_query(page_name, q_list)
                i += 1
                html_dic[page_name] = {'h_result': h_result, 't_result': t_result}
            elif top_words:
                print('\n{} : {}  ({})'.format(page_name, this_pk_data['title'], str(len(this_pk_data['title']))))
                print('   {}        {}      {}'.format(click_num, view_num, order_num))
                for tw in top_words:
                    print(tw)
                # for qs in query_str_list:
                #     print(qs)
                # get_gsc_query(page_name, q_list)
                i += 1
                html_dic[page_name] = {'h_result': h_result, 't_result': t_result}
        else:
            print('url not in : ' + page_name)
        if i >= 10:
            break
    if html_dic:
        make_seo_html_file(html_dic, q_list)
    return target_list


if __name__ == '__main__':
    next_update_target_search(100, 28, 3000, 'reibun')
