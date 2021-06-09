import os
import glob
import re
from datetime import datetime, timedelta
import csv
import pickle
import query_check_and_make_html as qcm


def check_all_site_data(limit_d, period, main_str_limit, print_flag, ma_flag, ignore_flag):
    os.chdir('../')
    no_edit_c = []
    no_edit_q = []
    all_site_c = []
    all_site_p = {}
    target_project_list = ['reibun', 'rei_site', 'joshideai']  # , 'rei_site', 'joshideai'
    today = datetime.today()
    if period == 28:
        period_name = 'month'
    elif period == 7:
        period_name = 'week'
    else:
        period_name = str(period) + '_'
    for target_project in target_project_list:
        print(target_project)
        pj_dir, domain, main_dir, site_name, pj_domain_main = qcm.project_select(target_project + '/')
        end_date = qcm.make_target_data_for_today(today, period, pj_dir, domain)
        if os.path.exists('gsc_data/' + pj_dir + '/p_' + period_name + end_date + '.csv'):
            with open('gsc_data/' + pj_dir + '/p_' + period_name + end_date + '.csv') as f:
                reader = csv.reader(f)
                csv_list = [row for row in reader]
            c_list = qcm.sc_data_match_page(csv_list, domain)
            all_site_c.extend(c_list)
            with open('gsc_data/' + pj_dir + '/qp_' + period_name + end_date + '.csv') as f:
                q_reader = csv.reader(f)
                q_list = [row for row in q_reader]
            q_list = q_list[1:]
            # print(c_list)
            with open(pj_dir + '/pickle_pot/main_data.pkl', 'rb') as f:
                pk_dic = pickle.load(f)
            # print(pk_dic)
            e_pk_dic = {pk_dic[x]['file_path']: pk_dic[x] for x in pk_dic}
            all_site_p.update({pj_domain_main + e_pk_dic[y]['file_path']: e_pk_dic[y] for y in e_pk_dic})
            no_edit_click, no_edit_query = rewrite_page_check(c_list, e_pk_dic, q_list, pj_domain_main)
            if no_edit_click:
                no_edit_c.extend(no_edit_click)
            if no_edit_query:
                no_edit_q.extend(no_edit_query)
            # print(q_list)
            # print('クリック数順')
            # qcm.check_list_and_bs(c_list, e_pk_dic, limit_d, q_list, main_str_limit, today, print_flag, ma_flag, end_date,
            #                       period, target_project, ignore_flag)
        else:
            print('{} no data'.format(target_project))
    no_edit_c = [[y[0], int(y[1]), int(y[2]), float(y[3]), float(y[4])] for y in no_edit_c]
    no_edit_c.sort(key=lambda x: x[2], reverse=True)
    # print('no_edit: {}'.format(no_edit_c))
    for ne in no_edit_c:
        if ne[1] > 0 or ne[2] > 10:
            print(ne)
    # print(no_edit_q)
    # print(all_site_p)
    # all_site_c.sort(key=lambda x: int(x[1]), reverse=True)
    # for row in all_site_c:
    #     print(row)


def add_http_and_https_csv(start_period, end_period):
    start = datetime.strptime(start_period, '%Y-%m-%d').date()
    end = datetime.strptime(end_period, '%Y-%m-%d').date()
    days_list = [(start + timedelta(n)).strftime('%Y-%m-%d') for n in range((end - start).days)]
    # print(days_list)
    for day_str in days_list:
        n_list, o_list = [], []
        if os.path.exists('gsc_data/rei_site/ed_data/od' + day_str + '.csv'):
            with open('gsc_data/rei_site/ed_data/od' + day_str + '.csv') as f:
                reader = csv.reader(f)
                n_list = [row for row in reader]
        if os.path.exists('gsc_data/rs_o/ed_data/od' + day_str + '.csv'):
            with open('gsc_data/rs_o/ed_data/od' + day_str + '.csv') as g:
                o_reader = csv.reader(g)
                o_list = [row for row in o_reader]
        if n_list:
            if o_list:
                u_list = n_list + o_list[1:]
            else:
                u_list = n_list
        else:
            if o_list:
                u_list = o_list
            else:
                u_list = []
        # print(u_list)
        if u_list:
            with open('gsc_data/rei_site/new_csv/od' + day_str + '.csv', 'w') as h:
                writer = csv.writer(h)
                writer.writerows(u_list)


def rewrite_page_check(c_list, e_pk_dic, q_list, pj_domain_main):
    no_edit_list = [pj_domain_main + e_pk_dic[x]['file_path'] for x in e_pk_dic if 'edit_flag' in e_pk_dic[x] and
                    not e_pk_dic[x]['edit_flag']]
    # print(no_edit_list)
    no_edit_click = [y for y in c_list if y[0] in no_edit_list]
    no_edit_query = [z for z in q_list if z[5] in no_edit_list]
    return no_edit_click, no_edit_query


def insert_rewrite_flag(prj_name, dir_list):
    for dir_name in dir_list:
        md_list = glob.glob('{}/md_files/{}/**.md'.format(prj_name, dir_name))
        for md_file in md_list:
            with open(md_file, 'r', encoding='utf-8') as f:
                long_str = f.read()
                if '\ne::' not in long_str:
                    long_str = re.sub(r'\n(n::\d*)\n', r'\n\1\ne::\n', long_str)
                    with open(md_file, 'w', encoding='utf-8') as g:
                        g.write(long_str)
        with open(prj_name + '/pickle_pot/main_data.pkl', 'rb') as h:
            pk_dic = pickle.load(h)
        for i in pk_dic:
            if dir_name + '/' in pk_dic[i]['file_path'] and 'edit_flag' not in pk_dic[i]:
                pk_dic[i]['edit_flag'] = False
        print(pk_dic)
        with open(prj_name + '/pickle_pot/main_data.pkl', 'wb') as j:
            pickle.dump(pk_dic, j)


# todo: scからページのデータを落として合わせる
# todo: 新規作成のページで検索からの流入がスタートしたページを検索
# todo: クリック数やimpが増加傾向のページをピックアップ
# todo: そのページのクエリのデータを表示

if __name__ == '__main__':
    check_all_site_data(100, 28, 3000, False, True, False)
    # add_http_and_https_csv('2020-04-23', '2021-05-25')
    # insert_rewrite_flag('joshideai', ['make_love'])
