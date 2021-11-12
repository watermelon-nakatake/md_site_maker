import pickle
import os
import re
import shutil
import importlib
import preparation
import make_new_article
# import source_data
# import pprint
import new_from_md

# Taichi Yamaoka
# 239

site_data = {
    0: {'title': 'マッチングアプリでセフレ探し',
        'domain': 'sefure-matching.com',
        'adj': 'マッチングアプリで',
        'sub': 'r',
        'obj': 'r',
        'act': 'セフレを探す',
        'dir': {'target': 'セフレ作り'},
        'f_name': '{}_mf_m',
        'no_adult_flag': False,
        'part_code': 'obj'},
    1: {'title': '出会えるマッチングアプリ掲示板',
        'domain': 'matching-bbs.com',
        'adj': 'パパ活で',
        'sub': '',
        'obj': 'r',
        'act': 'r',
        'dir': {'papa': '秘密の出会い'},
        'f_name': 'ma_man_{}',
        'no_adult_flag': False,
        'part_code': 'obj'},
    # パパ活,マッチングアプリ
    2: {'title': 'おすすめ割り切り掲示板',
        'domain': 'secret-matching.com',
        'adj': '割り切りで',
        'sub': 'r',
        'obj': '',
        'act': 'r',
        'dir': {'money': '割り切り'},
        'f_name': 'w_man_{}',
        'no_adult_flag': False,
        'part_code': 'sub'},
    # 割り切り
    3: {'title': '絶対にバレない不倫のやり方',
        'domain': 'cheating-love.com',
        'adj': '不倫で',
        'sub': 'r',
        'obj': '',
        'act': 'r',
        'dir': {'cheating': '不倫と浮気'},
        'f_name': '{}_adultery',
        'no_adult_flag': False,
        'part_code': 'act'},
    # 不倫
    4: {'title': 'マッチングアプリで出会う方法',
        'domain': 'my-matching.com',
        'adj': 'マッチングアプリで',
        'sub': 'r',
        'obj': 'r',
        'act': '彼女と出会う',
        'dir': {'girlfriend': '彼女探し'},
        'f_name': '{}_love_app_man',
        'no_adult_flag': False,
        'part_code': 'obj'},
    # マッチングアプリ、出会う
    5: {'title': '高齢者が出会えるおすすめ出会い系サイト',
        'domain': 'senior-matching.com',
        'adj': 'スマホを使って',
        'sub': '高齢者の男性が',
        'obj': 'r',
        'act': 'r',
        'dir': {'love': 'シニアの出会い'},
        'f_name': '{}_m_40s',
        'no_adult_flag': False,
        'part_code': 'obj'},
    # 高齢者,出会い系サイト,スマホ
    6: {'title': '結婚相手と出会える婚活アプリ紹介所',
        'domain': 'good-marriage.com',
        'adj': '婚活アプリでアプリで',
        'sub': 'r',
        'obj': 'r',
        'act': '結婚する',
        'dir': {'marriage': '結婚相手探し'},
        'f_name': '{}_m_app',
        'no_adult_flag': False,
        'part_code': 'obj'},
    # 婚活アプリ、婚活,地域の婚活
    7: {'title': '趣味の合うメル友の探し方',
        'domain': 'online-pen-pal.com',
        'adj': '趣味の出会いで',
        'sub': 'r',
        'obj': 'r',
        'act': 'メル友を作る',
        'dir': {'mail_friend': 'メル友探し'},
        'f_name': 'mail_{}_m',
        'no_adult_flag': False,
        'part_code': 'obj'},
    # 趣味の出会い、メル友
    8: {'title': 'アフターコロナの安全な出会いのやり方',
        'domain': 'after-covid-love.com',
        'adj': 'アフターコロナに',
        'sub': 'r',
        'obj': 'r',
        'act': '安全に出会う',
        'dir': {'matching': '出会いの方法'},
        'f_name': '{}_corona_m',
        'no_adult_flag': False,
        'part_code': 'obj'},
    # アフターコロナ,安全な出会い
    9: {'title': 'マッチングアプリでセフレ探し',
        'domain': 'marriage-hunt.com',
        'adj': 'マッチングアプリで',
        'sub': 'r',
        'obj': 'r',
        'act': '婚活する',
        'dir': {'hunting': 'オンライン婚活'},
        'f_name': 'mh_man_{}',
        'no_adult_flag': False,
        'part_code': 'obj'}
    # オンライン婚活,結婚
}


def make_new_site_dir_and_data(data_dict):
    test_flag = True
    if test_flag:
        shutil.rmtree('mass_production')
        os.mkdir('mass_production')
    for s_id in data_dict:
        pj_name = data_dict[s_id]['domain'].replace('.com', '').replace('-', '_')
        make_project_dir_and_pd_file_for_mass(pj_name, data_dict[s_id])


def make_project_dir_and_pd_file_for_mass(project_name, data_dict):
    test_flag = True
    if not os.path.exists('mass_production/' + project_name):
        os.mkdir('mass_production/' + project_name)
    if not os.path.exists('mass_production/' + project_name + '/' + 'main_info.py') or test_flag:
        pd_path = 'mass_production/' + project_name + '/' + 'main_info.py'
        shutil.copy('template_files/main_info.py', pd_path)
        with open(pd_path, 'r', encoding='utf-8') as f:
            pd_str = f.read()
            pd_str = pd_str.replace('<!--project-name-->', project_name)
            pd_str = pd_str.replace('rp_project_name', 'mass_production')
            pd_str = pd_str.replace("site_name = 'サイト名'", "site_name = '{}'".format(data_dict['title']))
            cat_dict = {x: [data_dict['dir'][x], 'index.html', i + 1] for i, x in enumerate(data_dict['dir'])}
            pd_str = pd_str.replace("category_data = {'policy': ['ポリシー', 'index.html', 1]}",
                                    "category_data = " + str(cat_dict))
            pd_str = pd_str.replace("domain_str = 'ドメイン名'", "domain_str = '{}'".format(data_dict['domain']))
            pd_str = pd_str.replace("default_img = ''", "default_img = 'common/{}_img.jpg'".format(project_name))
            pd_str = pd_str.replace("eyec_img = {'img_path': 'eyec.jpg', 'height': '464', 'width': '700'}",
                                    "eyec_img = {'img_path': 'common/" + project_name +
                                    "_img.jpg', 'height': '800', 'width': '1200'}")
            pd_str = pd_str.replace("info_dict = ", "mass_flag = True\n\ninfo_dict = ")
            pd_str = pd_str.replace("'google_id': google_id, 'relation_str': relation_str",
                                    "'google_id': google_id, 'mass_flag': mass_flag, 'relation_str': relation_str")
            with open(pd_path, 'w', encoding='utf-8') as g:
                g.write(pd_str)
            # print(pd_str)
        print('make pd file !')
    info_mod = importlib.import_module('mass_production.' + project_name + '.main_info')
    preparation.preparation_for_new_project(info_mod.info_dict)
    pd = info_mod.info_dict
    make_new_article.make_new_pages_to_md_for_mass(pd, data_dict, 'man', 2, '2021-10-08T18:22:12')
    new_from_md.main(0, pd, mod_date_flag=True, last_mod_flag=True, upload_flag=True,
                     first_time_flag=True, fixed_mod_date='')


def read_pickle(p_path):
    with open(p_path, 'rb') as f:
        p_str = pickle.load(f)
    print(p_str)


def change_pickle(p_path):
    with open(p_path, 'rb') as f:
        p_dict = pickle.load(f)
        del p_dict['obj_m'][346]
        print(p_dict)
        with open(p_path, 'wb') as g:
            pickle.dump(p_dict, g)


if __name__ == '__main__':
    # read_pickle('sfd/pickle_pot/used_id.pkl')
    # change_pickle('sfd/pickle_pot/used_id.pkl')

    make_new_site_dir_and_data(site_data)
