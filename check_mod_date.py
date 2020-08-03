import csv
import datetime
import make_article_list


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


if __name__ == '__main__':
    # print(make_article_list.read_pickle_pot('modify_log'))
    # make_mod_date_list()
    next_update_target_search(100)
