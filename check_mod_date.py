import csv
import datetime
import make_article_list
import os


def make_mod_date_list():
    seen = []
    mod_list = []
    mod_log = make_article_list.read_pickle_pot('modify_log')
    mod_log.reverse()
    for log in mod_log:
        if log[0] not in seen:
            mod_list.append([log[0].replace('reibun', ''), log[1]])
            seen.append(log[0])
    make_article_list.save_data_to_pickle(mod_list, 'mod_date_list')


def next_update_target_search(aim_date):
    i = 0
    with open('/Users/nakataketetsuhiko/Downloads/https___www/ページ.csv') as f:
        reader = csv.reader(f)
        csv_list = [row for row in reader]
    c_list = [y for y in csv_list[1:] if '#' not in y[0] and '/amp/' not in y[0]]
    mod_list = make_article_list.read_pickle_pot('mod_date_list')
    limit_d = datetime.datetime.now() - datetime.timedelta(days=aim_date)
    for i in range(len(mod_list)):
        if datetime.datetime.strptime(mod_list[i][1], '%Y-%m-%d') < limit_d:
            break
    mod_list_n = mod_list[:i]
    print('日数 : ' + str(check_number_of_days()) + '日間')
    print('クリック数順')
    check_no_mod_page(mod_list_n, c_list)
    c_list.sort(key=lambda x: int(x[2]), reverse=True)
    print('表示回数順')
    check_no_mod_page(mod_list_n, c_list)


def check_no_mod_page(mod_list, csv_list):
    result = []
    url_list = [x[0] for x in mod_list]
    i = 1
    for g_data in csv_list:
        url_str = g_data[0].replace('https://www.demr.jp', '')
        if url_str not in url_list and g_data[0] != 'https://www.demr.jp/':
            result.append(url_str)
            print('{} : {}位, {}クリック, 表示{}回, 掲載順位平均{}'.format(str(i), url_str, g_data[1], g_data[2], g_data[4]))
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


def make_side_bar_article_list(list_length):
    click_list = []
    time_list = []
    pk_dec = make_article_list.read_pickle_pot('title_img_list')
    with open('/Users/nakataketetsuhiko/Downloads/https___www/ページ.csv') as f:
        reader = csv.reader(f)
        csv_list = [row for row in reader]
    c_list = [y for y in csv_list[1:] if '#' not in y[0] and '/amp/' not in y[0]]
    print('pop by click')
    for click_a in c_list:
        if '/pc/' in click_a[0]:
            path = click_a[0].replace('https://www.demr.jp/pc/', '')
            for pk_id in pk_dec:
                if pk_dec[pk_id][0] == path:
                    click_list.append(pk_id)
                    print('{} : {}, {}'.format(path, str(pk_id), pk_dec[pk_id][1]))
        if len(click_list) == list_length:
            break
    ga_list = make_ga_csv_list()
    t_list = [x for x in ga_list if '#' not in x[0] and '/pc/' not in x[0] and int(x[1]) >= 100]
    t_list.sort(key=lambda x: datetime.datetime.strptime(x[3], '%H:%M:%S'), reverse=True)
    print('\nimportant by reading time')
    for t_art in t_list:
        t_path = t_art[0].replace('/amp/', '')
        for pk_i in pk_dec:
            if pk_dec[pk_i][0] == t_path and pk_i not in click_list:
                time_list.append(pk_i)
                print('{} : {}, {}, {}'.format(t_path, str(pk_i), pk_dec[pk_i][1], t_art[3]))
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
    make_side_bar_article_list(10)
    print('\n')
    next_update_target_search(100)

    # print(make_article_list.read_pickle_pot('title_img_list'))
    # make_mod_date_list()
    # print(make_ga_csv_list())
