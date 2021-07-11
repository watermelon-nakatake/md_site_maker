import csv
import datetime
import os
from add_article import new_from_md, make_article_list
import re
import reibun.main_info
import query_check_and_make_html


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
    for page in csv_list[1:]:
        f_page = page[0].replace('https:www.demr.jp/', '').replace('amp/', 'pc/')
        f_page = re.sub(r'^(.+)#.+', r'\1', f_page)
        if f_page not in result:
            result[f_page] = page + [1]
        else:
            # print('------------------')
            # print(page)
            recent_page = result[f_page]
            # print(recent_page)
            result[f_page] = [recent_page[0].replace('/amp/', '/pc/'), str(int(page[1]) + int(recent_page[1])),
                              str(int(page[2]) + int(recent_page[2])), recent_page[3], recent_page[4],
                              recent_page[5] + 1]
            # print(result[f_page])
    result_list = [result[x] for x in result]
    return result_list


def next_update_target_search(aim_date, len_dec, pd):
    i = 0
    # with open('/Users/nakataketetsuhiko/Downloads/https___www/ページ.csv') as f:
    #     reader = csv.reader(f)
    #     csv_list = [row for row in reader]
    # c_list = sc_data_match_page(csv_list)
    # c_list = [y for y in csv_list[1:] if '#' not in y[0] and '/amp/' not in y[0]]
    today = datetime.date.today()
    pj_dir, domain, main_dir, site_name, pj_domain_main = query_check_and_make_html.project_select(pd['project_dir'] + '/')
    end_date = query_check_and_make_html.make_target_data_for_today(today, aim_date, pj_dir, domain)
    if aim_date == 28:
        period_name = 'month'
    elif aim_date == 7:
        period_name = 'week'
    else:
        period_name = str(aim_date) + '_'
    with open('gsc_data/' + pj_dir + '/p_' + period_name + end_date + '.csv') as f:
        reader = csv.reader(f)
        csv_list = [row for row in reader]
    c_list = query_check_and_make_html.sc_data_match_page(csv_list, domain)
    mod_list = make_article_list.read_pickle_pot('mod_date_list', pd)
    limit_d = datetime.datetime.now() - datetime.timedelta(days=aim_date)
    for i in range(len(mod_list)):
        if datetime.datetime.strptime(mod_list[i][1], '%Y-%m-%d') < limit_d:
            break
    mod_list_n = mod_list[:i + 1]
    print('日数 : ' + str(aim_date) + '日間')
    print('クリック数順')
    click_list = check_no_mod_page(mod_list_n, c_list, len_dec, pd)
    c_list.sort(key=lambda x: int(x[2]), reverse=True)
    print('表示回数順')
    display_list = check_no_mod_page(mod_list_n, c_list, len_dec, pd)
    c_list.sort(key=lambda x: int(x[1]), reverse=True)
    return click_list, display_list, c_list


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
                    with open(pd['project_dir'] + '/md_files/' + page.replace('.html', '.md'), 'r', encoding='utf-8')\
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
    p_d = reibun.main_info.info_dict
    pickle_dec = make_article_list.read_pickle_pot('main_data', p_d)
    # print(pickle_dec)
    str_len_dec = {'/' + p_d['main_dir'] + pickle_dec[x]['file_path']: pickle_dec[x]['str_len'] for x in pickle_dec}
    layout_dec = {'/' + p_d['main_dir'] + pickle_dec[x]['file_path']: pickle_dec[x]['layout_flag'] for x in pickle_dec}
    shift_dec = {'/' + p_d['main_dir'] + pickle_dec[x]['file_path']: pickle_dec[x]['shift_flag'] for x in pickle_dec}
    # print(str_len_dec)
    # make_side_bar_article_list(10, p_d)
    # print('\n')
    c_l, d_l, c_l2 = next_update_target_search(60, str_len_dec, p_d)
    print('\n')
    t_l = count_title_str_num(str_len_dec, p_d)
    print('\n')
    make_to_do_list(c_l, d_l, t_l)
    print('\n')
    new_from_md.insert_main_length(p_d)
    # print(c_l2)
    check_layout_flag(c_l2, layout_dec, pickle_dec)
    check_shift_flag(c_l2, shift_dec, p_d)

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
