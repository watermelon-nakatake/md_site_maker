import copy
import glob
import random
import re
import numpy as np
import os
import pprint
import pickle
import datetime
import source_data
import words_dict
import words_dict as wd
import key_data.key_source
import key_data.obj_source
import key_data.key_obj_man
import key_data.key_obj_woman
import key_data.key_adj_act
import key_data.key_sub_man

key_source_dict = {'obj_m': key_data.key_obj_woman.keyword_dict, 'obj_w': key_data.key_obj_man.keyword_dict,
                   'adj_act': key_data.key_adj_act.key_dict, 'act': key_data.key_adj_act.act_dict}
no_adult_prj = ['mh', 'olm', 'women', 'bf', 'koi']
opposite_sex = {'man': 'w', 'woman': 'm'}
html_str_dict = {
    'sfd': {'obj_m': 'sf_{}_f', 'obj_w': 'sf_{}_m', 'sub_m': 'sf_s_{}_m', 'sub_w': 'sf_s_{}_f',
            'act': 'sf_a_{}', 'adj_act': 'sf_a_{}'},
    'bf': {'obj_m': 'gf_{}', 'obj_w': 'gf_{}', 'sub_m': 'sf_s_{}_m', 'sub_w': 'sf_s_{}_f',
           'act': 'ac_{}', 'adj_act': 'ac_{}'},
    'sex': {'obj_m': 'sex_{}', 'obj_w': 'sex_{}', 'sub_m': 'sex_{}_m', 'sub_w': 'sex_{}_f',
            'act': 'sex_a_{}', 'adj_act': 'sex_a_{}'},
    'goodbyedt': {'obj_m': '{}_dt', 'obj_w': '', 'sub_m': '{}_s_dt', 'sub_w': '',
                  'act': '{}_a_dt', 'adj_act': '{}_a_dt'},
}


def make_new_pages_to_md_from_key_list(project_dir, dir_name, source_mod, main_key, use_id_list, key_list,
                                       recipe_flag, subject_sex, start_id, insert_pub_date, part_code,
                                       copy_pub_flag):
    # 必要最低限のキーワードリストで機動的に記事作成
    # 個別記事のリストの中にメインワードのキーワード ex.gf で選択
    # 既存記事のキーワードとurlをランダム選択scrに渡す
    html_str = choice_html_str(subject_sex, project_dir, part_code)
    recipe_dict = {}
    counter_d = {}
    if not use_id_list:
        use_id_list = list(key_list.keys())
    use_id_list = id_filter(use_id_list, main_key, key_list)
    this_key_code = check_key_code(key_list)
    used_dict, add_id_dict = make_used_key_dict(project_dir, use_id_list, this_key_code, start_id)
    if insert_pub_date:
        dt1 = datetime.datetime.strptime(insert_pub_date, '%Y-%m-%dT%H:%M:%S')
    else:
        dt1 = ''
    # print(used_dict)
    # print(add_id_dict)
    if main_key in no_adult_prj and part_code == 'obj':
        used_dict_l = {x: {y: used_dict[x][y] for y in used_dict[x] if key_source_dict[x][y]['ad'] == 3} if type(
            used_dict[x]) == dict else used_dict[x] for x in used_dict}
        ad_used_dict = {x: {y: used_dict[x][y] for y in used_dict[x] if key_source_dict[x][y]['ad'] == 1} if type(
            used_dict[x]) == dict else used_dict[x] for x in used_dict}
        ad_link_dict = make_key_and_path_list(html_str, ad_used_dict, project_dir)
    else:
        used_dict_l = used_dict
        ad_link_dict = {}
    # print(used_dict_l)
    link_dict = make_key_and_path_list(html_str, used_dict_l, project_dir)
    # print(link_dict)
    # return
    art_map = [[source_mod.introduction, 1], [source_mod.d_introduction, 'straight'],
               [source_mod.d_advantage, [2, 3, 4]],
               [source_mod.p_introduction, 'straight'], [source_mod.purpose_advantage, 3],
               [source_mod.tips_bonus, [0, 1, 2]], [source_mod.process, 'straight'],
               [source_mod.tips_bonus, [1, 2, 3]], [source_mod.conclusion, 1]]
    if subject_sex == 'man':
        friend_str = '彼女'
    else:
        friend_str = '彼氏'
    main_key_dict = {'obj': {'sex': {'act': 'セックスする', 'act_noun': 'セックス相手', 'act_noun_flag': False,
                                     'a_adj_flag': False,
                                     '2act_w': 'セックスしたい', '2act_noun': 'セックス', '2act_do': 'セックスする',
                                     'act_connection': ['肉体関係'], 'act_code': 'sex', 'replace_words': []},
                             'dt': {'act': '<!--lost-dt-->', 'act_noun': '<!--lost-dt-pt-->', 'act_noun_flag': False,
                                    'a_adj_flag': False,
                                    '2act_w': 'セックスしたい', '2act_noun': 'セックス', '2act_do': 'セックスする',
                                    'act_connection': ['肉体関係'], 'act_code': 'dt', 'replace_words': []},
                             'mh': {'act': '出会う', 'act_noun': '出会い', 'act_noun_flag': False, 'a_adj': '婚活で',
                                    'a_adj_flag': True,
                                    '2act_w': '結婚したい', '2act_noun': '結婚', '2act_do': '結婚する',
                                    'act_connection': ['交際', 'お付き合い'], 'act_code': 'mh',
                                    'replace_words': [['出会い系サイト', '婚活サイト'], ['出会い掲示板', '婚活掲示板'],
                                                      ['出会い系掲示板', '婚活掲示板'], ['出会い系', '婚活サイト'],
                                                      ['で婚活で', 'の婚活で']]},
                             'olm': {'act': '結婚する', 'act_noun': '結婚', 'act_noun_flag': False,
                                     'a_adj': 'オンラインの出会いで', 'a_adj_flag': True,
                                     '2act_w': '結婚したい', '2act_noun': '結婚', '2act_do': '結婚する',
                                     'act_connection': ['交際', 'お付き合い'], 'act_code': 'mh',
                                     'replace_words': [['出会い系サイト', '婚活サイト'], ['出会い掲示板', '婚活掲示板'],
                                                       ['出会い系掲示板', '婚活掲示板'], ['出会い系', '婚活サイト'],
                                                       ['で婚活で', 'の婚活で']]},
                             'sf': {'act': 'セフレを作る', 'act_noun': 'セフレ', 'act_noun_flag': True, 'a_adj_flag': False,
                                    '2act_w': 'セックスしたい', '2act_noun': 'セックス', '2act_do': 'セックスする',
                                    'act_connection': ['セフレ関係', '肉体関係'], 'act_code': 'sf', 'replace_words': []},
                             'gf': {'act': '彼女を作る', 'act_noun': '彼女', 'act_noun_flag': False, 'a_adj_flag': False,
                                    '2act_w': 'デートしたい', '2act_noun': 'デート', '2act_do': 'デートする',
                                    'act_connection': ['交際', 'お付き合い'], 'act_code': 'gf',
                                    'replace_words': []},
                             'bf': {'act': '彼氏を作る', 'act_noun': '彼氏', 'act_noun_flag': False, 'a_adj_flag': False,
                                    '2act_w': 'デートしたい', '2act_noun': 'デート', '2act_do': 'デートする',
                                    'act_connection': ['交際', 'お付き合い'], 'act_code': 'bf',
                                    'replace_words': []},
                             'koi': {'act': '恋人を作る', 'act_noun': '恋人', 'act_noun_flag': False, 'a_adj': 'ネットの恋活で',
                                     'a_adj_flag': True,
                                     '2act_w': 'デートしたい', '2act_noun': 'デート', '2act_do': 'デートする',
                                     'act_connection': ['恋愛'], 'act_code': 'gf',
                                     'replace_words': []},
                             'cov': {'act': friend_str + 'を作る', 'act_noun': friend_str, 'act_noun_flag': False,
                                     'a_adj': 'コロナ禍に', 'a_adj_flag': True,
                                     '2act_w': 'デートしたい', '2act_noun': 'デート', '2act_do': 'デートする',
                                     'act_connection': ['交際', 'お付き合い'], 'act_code': 'cov',
                                     'replace_words': [['出会い系サイト', 'マッチングアプリ'],
                                                       ['マッチングアプリのマッチングアプリ', 'マッチングアプリ'],
                                                       ['マッチングアプリのマッチングサイト', 'マッチングサイト'],
                                                       ['マッチングサイトのマッチングアプリ', 'マッチングアプリ'],
                                                       ['マッチングサイトのマッチングサイト', 'マッチングサイト']]},
                             'ht': {'act': 'エッチする', 'act_noun': 'エッチの相手', 'act_noun_flag': False,
                                    'a_adj': 'マッチングアプリで', 'a_adj_flag': True,
                                    '2act_w': 'セフレにしたい', '2act_noun': 'セフレ', '2act_do': 'セフレにする',
                                    'act_connection': ['エッチな関係', 'ヤリ友'], 'act_code': 'ht',
                                    'replace_words': [['出会い系サイト', 'マッチングアプリ'],
                                                      ['マッチングアプリのマッチングアプリ', 'マッチングアプリ'],
                                                      ['マッチングアプリのマッチングサイト', 'マッチングサイト'],
                                                      ['マッチングサイトのマッチングアプリ', 'マッチングアプリ'],
                                                      ['マッチングサイトのマッチングサイト', 'マッチングサイト']]}
                             },
                     'act': {
                         'sf': {'a_adj_flag': True, 'act_code': 'sf', 'replace_words': []},
                         'bf': {'a_adj_flag': True, 'act_code': 'bf', 'replace_words': []},
                         'sex': {'a_adj_flag': True, 'act_code': 'sex', 'replace_words': []},
                         'dt': {'a_adj_flag': True, 'act_code': 'dt', 'replace_words': [],
                                'sub_key': '童貞', 'sub': '童貞男子', 's_sex': 'm', 's_ms': 's', 's_adj': '真面目な'}
                     },
                     'sub': {
                         'sf': {'act': 'セフレを作る', 'act_noun': 'セフレ', 'act_noun_flag': True, 'a_adj_flag': False,
                                '2act_w': 'セックスしたい', '2act_noun': 'セックス', '2act_do': 'セックスする',
                                'act_connection': ['セフレ関係', '肉体関係'], 'act_code': 'sf', 'replace_words': [],
                                'act_target': 'セフレ', 's_adj': ''}
                     }
                     # act と　a_adj の切り替え
                     }
    hot_info = {'hot_month': '10月', 'hot_season': '秋', 'hot_month_next': '11月'}
    a_adj_flag = main_key_dict[part_code][main_key]['a_adj_flag']
    dt_str = ''
    # print(link_dict)
    if not os.path.exists(project_dir + '/md_files/' + dir_name):
        os.mkdir(project_dir + '/md_files/' + dir_name)
    for key_id in use_id_list:
        keywords = key_list[key_id]
        keywords['id'] = str(key_id)
        if main_key:
            keywords.update(main_key_dict[part_code][main_key])
        keywords['page_name'] = html_str.replace('{}', keywords['eng'].replace('-', '_'))

        if 'sub' not in keywords:
            no_sub_flag = True
            if subject_sex == 'man':
                keywords['s_adj'] = np.random.choice(['普通の', 'モテない'])
                keywords['sub'] = np.random.choice(['独身男性', '男性'])
            else:
                keywords['s_adj'] = np.random.choice(['普通の', 'モテない'])
                keywords['sub'] = np.random.choice(['独身女性', '女性', '女子'])
        else:
            no_sub_flag = False
        if 'obj' not in keywords:
            no_obj_flag = True
            c_obj = np.random.choice(['女性', '女性', '女子'])
            if project_dir in ['sfd']:
                women_list = ['魅力的な', 'かわいい', 'きれいな', 'エッチな', 'Hな', 'エロい', 'すけべな', 'スケベな',
                              'セクシーな', 'セクシー']
            else:
                women_list = ['魅力的な', 'かわいい', 'きれいな']
            c_adj = np.random.choice(women_list)
            keywords['obj'] = c_adj + c_obj
            keywords['obj_key'] = c_adj + c_obj
            keywords['obj_p'] = 'の'
            keywords['o_sex'] = opposite_sex[subject_sex]
            keywords['o_age'] = 'n'
            keywords['o_cat'] = 's'
            keywords['o_adj'] = ''
        else:
            no_obj_flag = False
        if keywords['obj_p'] == 'no' or keywords['obj_p'] == 'n':
            keywords['obj_p'] = ''
        if 'a_adj' not in keywords:
            if main_key == 'sex' and keywords['o_ms'] == 'm':
                keywords['a_adj'] = np.random.choice(['不倫', '浮気', 'NTR'])
            else:
                keywords['a_adj'] = np.random.choice(['安全に', '確実に', '簡単に', 'すぐに', '無料で'])
        if main_key in no_adult_prj and part_code == 'obj':
            if keywords['ad'] != 3:
                link_dict_u = ad_link_dict
            else:
                link_dict_u = link_dict
                keywords['o_adj'] = ''
        else:
            link_dict_u = link_dict
        if 'o_reason' not in keywords:
            keywords['o_reason'] = '素敵な出会いが欲しいから'
        keywords.update(hot_info)
        # print(keywords)
        make_keywords_sample(keywords, a_adj_flag, no_obj_flag, no_sub_flag)
        old_md = '{}/md_files/{}/{}.md'.format(project_dir, dir_name, keywords['page_name'])
        old_pub = ''
        if os.path.exists(old_md):
            with open(old_md, 'r', encoding='utf-8') as m:
                md_str = m.read()
            old_pub_l = re.findall(r'p::(.+?)\n', md_str)
            if old_pub_l:
                old_pub = old_pub_l[0]
        if copy_pub_flag and old_pub:
            dt_str = old_pub
        else:
            if dt1:
                dt1 = dt1 + datetime.timedelta(hours=int(random.random() * 12), minutes=int(random.random() * 60),
                                               seconds=int(random.random() * 59))
                dt_str = dt1.strftime('%Y-%m-%dT%H:%M:%S')
        recipe_list, counter_d = make_new_page(keywords, source_mod, art_map, project_dir, dir_name, link_dict_u,
                                               main_key, recipe_flag, subject_sex, a_adj_flag, add_id_dict, dt_str,
                                               part_code, no_obj_flag, no_sub_flag, counter_d)
        recipe_dict[keywords['page_name']] = recipe_list
    if dt_str:
        print('last pub_date :  {}'.format(dt_str))
    # print(recipe_dict)
    # print(counter_d)
    # sort_counter_dict(counter_d)


def sort_counter_dict(counter_d):
    c_list = [[x, counter_d[x]] for x in counter_d]
    c_list.sort(key=lambda x: x[1], reverse=True)
    for row in c_list:
        print('{} : {}'.format(row[0], round(row[1] / 87)))


def choice_html_str(subject_sex, project_dir, part_code):
    if part_code in ['obj', 'sub']:
        if subject_sex == 'man':
            hs_str = part_code + '_m'
        else:
            hs_str = part_code + '_w'
    else:
        hs_str = part_code
    html_str = html_str_dict[project_dir][hs_str]
    return html_str


def id_filter(use_id_list, main_key, key_list):
    if main_key in no_adult_prj:
        # print(key_list)
        if 'ad' not in key_list[0]:
            use_id_list = use_id_list
        else:
            use_id_list = [x for x in use_id_list if key_list[x]['ad'] != 0]
    # print(use_id_list)
    return use_id_list


def make_used_key_dict(project_dir, use_id_list, this_key_code, start_id):
    pkl_path = '{}/pickle_pot/used_id.pkl'.format(project_dir)
    add_id_dict = {}
    dict_temp = {'obj_m': {}, 'obj_w': {}, 'sub_m': {}, 'sub_w': {}, 'act': {}, 'adj_act': {}, 'max_id': 'n'}
    if os.path.exists(pkl_path):
        with open(pkl_path, 'rb') as p:
            used_dict = pickle.load(p)
        for d_key in dict_temp:
            if d_key not in used_dict:
                used_dict[d_key] = {}
        # print(used_dict)
    else:
        used_dict = dict_temp
    if used_dict['max_id'] == 'n':
        if start_id:
            next_id = start_id
        else:
            next_id = 1
    else:
        next_id = int(used_dict['max_id']) + 1
    use_id_list.sort()
    for use_id in use_id_list:
        if use_id not in used_dict[this_key_code]:
            used_dict[this_key_code][use_id] = next_id
            add_id_dict[use_id] = next_id
            next_id += 1
        else:
            add_id_dict[use_id] = used_dict[this_key_code][use_id]
    used_dict['max_id'] = next_id - 1
    with open(project_dir + '/pickle_pot/used_id.pkl', 'wb') as k:
        pickle.dump(used_dict, k)
    return used_dict, add_id_dict


def make_used_key_data(project_dir):
    used_dict = {'obj_m': {}, 'obj_w': {}, 'sub_m': {}, 'sub_w': {}, 'act': {}, 'adj_act': {}, 'max_id': 'n'}
    obj_m = list(range(0, 209, 1))
    obj_w = list(range(0, 116, 1))
    used_dict['obj_m'] = {x: x for x in obj_m}
    used_dict['obj_w'] = {y: y + 209 for y in obj_w}
    used_dict['max_id'] = 324
    # print(used_dict)
    with open(project_dir + '/pickle_pot/used_id.pkl', 'wb') as k:
        pickle.dump(used_dict, k)


def check_key_code(key_list):
    if key_list[0]['type'] == 'only_obj' and key_list[0]['o_sex'] == 'w':
        this_key_code = 'obj_m'
    elif key_list[0]['type'] == 'only_obj' and key_list[0]['o_sex'] == 'm':
        this_key_code = 'obj_w'
    elif key_list[0]['type'] == 'only_sub' and key_list[0]['o_sex'] == 'm':
        this_key_code = 'sub_m'
    elif key_list[0]['type'] == 'only_sub' and key_list[0]['o_sex'] == 'w':
        this_key_code = 'sub_w'
    elif key_list[0]['type'] == 'only_act':
        this_key_code = 'act'
    elif key_list[0]['type'] == 'mix_act':
        this_key_code = 'adj_act'
    else:
        this_key_code = ''
        print('key_code error!')
    return this_key_code


def make_key_and_path_list(html_str, used_dict, project_dir):
    result = {'obj_m': [], 'obj_w': [], 'sub_m': [], 'sub_w': [], 'act': [], 'adj_act': []}
    if project_dir != 'sfd':
        for key_name in key_source_dict:
            if key_name != 'adj_act' and key_name != 'act':
                if project_dir in html_str_dict:
                    if key_name in html_str_dict[project_dir]:
                        html_str = html_str_dict[project_dir][key_name]
                result[key_name] = [[key_source_dict[key_name][x]['all_key'],
                                     html_str.replace('{}', key_source_dict[key_name][x]['eng'].replace('-', '_'))]
                                    for x in used_dict[key_name] if x in key_source_dict[key_name]]
            else:
                # print(key_source_dict['adj_act'])
                if project_dir in html_str_dict:
                    if key_name in html_str_dict[project_dir]:
                        html_str = html_str_dict[project_dir][key_name]
                result[key_name] = [[key_source_dict[key_name][x]['act_noun'],
                                     html_str.replace('{}', key_source_dict[key_name][x]['eng'].replace('-', '_'))]
                                    for x in used_dict[key_name] if x in key_source_dict[key_name]]
    else:
        for key_name in key_source_dict:
            # print(key_name)
            if key_name != 'obj_m' and key_name != 'adj_act':
                if project_dir in html_str_dict:
                    if key_name in html_str_dict[project_dir]:
                        html_str = html_str_dict[project_dir][key_name]
                result[key_name] = [[key_source_dict[key_name][x]['all_key'],
                                     html_str.replace('{}', key_source_dict[key_name][x]['eng'].replace('-', '_'))]
                                    for x in used_dict[key_name] if x in key_source_dict[key_name]]
            elif key_name == 'adj_act':
                if project_dir in html_str_dict:
                    if key_name in html_str_dict[project_dir]:
                        html_str = html_str_dict[project_dir][key_name]
                result[key_name] = [[key_source_dict[key_name][x]['act_noun'],
                                     html_str.replace('{}', key_source_dict[key_name][x]['eng'].replace('-', '_'))]
                                    for x in used_dict[key_name] if x in key_source_dict[key_name]]
            else:
                if project_dir in html_str_dict:
                    if key_name in html_str_dict[project_dir]:
                        html_str = html_str_dict[project_dir][key_name]
                for k_id in used_dict[key_name]:
                    if int(k_id) < 209:
                        result['obj_m'].append([key_source_dict['obj_m'][k_id]['obj'],
                                                key_source_dict[key_name][k_id]['eng']])
                    else:
                        result['obj_m'].append([key_source_dict['obj_m'][k_id]['obj'],
                                                html_str.replace('{}',
                                                                 key_source_dict['obj_m'][k_id]['eng'].replace('-',
                                                                                                               '_'))])
    # print(result)
    for key_n in key_source_dict:
        if not result[key_n]:
            if key_n == 'adj_act':
                result[key_n] = [[key_source_dict[key_n][x]['all_key'], ''] for x in key_source_dict[key_n]]
            else:
                result[key_n] = [[key_source_dict[key_n][x]['all_key'], ''] for x in key_source_dict[key_n]]
    return result


def obj_source_changer():
    o_list = key_data.obj_source.obj_key_list
    result = {
        int(x['id']): {'obj_key': x['keyword'], 'obj': x['noun'], 'o_adj': x['adj'], 'obj_p': x['particle'],
                       'o_sex': 'w', 'o_reason': x['reason'], 'o_cat': x['t_cat'], 'o_ms': x['o_ms'],
                       'o_age': x['t_age'],
                       'o_look': x['look'], 'eng': x['eng'], 'type': 'only_obj', 'all_key': x['keyword']} for x in
        o_list}
    return result


def obj_source_filter(source_dict):
    print(source_dict)
    return True
    # if source_dict['o_ms'] == 's':
    #     return True
    # else:
    #     return False


def make_new_page(keywords, source_mod, art_map, project_dir, dir_name, link_dict, main_key, recipe_flag, subject_sex,
                  a_adj_flag, add_id_dict, dt_str, part_code, no_obj_flag, no_sub_flag, counter_d):
    recipe_list = {}
    site_list = ['ワクワクメール', 'ハッピーメール']
    site1 = np.random.choice(['ワクワクメール', 'ハッピーメール'])
    site_data = {'sf': {'site_name': 'セフレ道', 'site_author': '田中'},
                 'mh': {'site_name': 'ネット婚活で結婚相手探し', 'site_author': '伊東'},
                 'dt': {'site_name': '出会い系で童貞卒業', 'site_author': 'サム'},
                 'olm': {'site_name': 'オンラインの出会いで結婚する方法', 'site_author': '池田'},
                 'cov': {'site_name': 'マッチングアプリで恋人探し', 'site_author': '山本'},
                 'ht': {'site_name': '出会い系エッチ体験談', 'site_author': 'ごろう'},
                 'bf': {'site_name': '女性のための出会い系教室', 'site_author': '橋下'},
                 'koi': {'site_name': 'ネット恋活で恋人と出会う方法', 'site_author': '谷本'},
                 'sex': {'site_name': 'セックスできる出会い系サイトを探せ', 'site_author': '後藤'}}
    sex_dict = [[['男性', '男'], [0.9, 0.1]], [['女性', '女子', '女の人'], [0.6, 0.2, 0.2]],
                [['女性', '女の人']], [['女の子', '女子']],
                [['彼氏', '恋人'], [0.7, 0.3]], [['彼女', '恋人'], [0.7, 0.3]],
                [['旦那', '旦那さん', '夫', '配偶者'], [0.3, 0.2, 0.3, 0.2]],
                [['奥さん', '妻', '配偶者', '夫人'], [0.4, 0.3, 0.2, 0.1]],
                [['人妻', '既婚女性'], [0.6, 0.4]], [['既婚男性', '既婚者', '妻子持ち'], [0.5, 0.3, 0.2]],  # 10
                [['処女']], [['童貞']],
                [['女性会員', '女性利用者', '女性の利用者']], [['男性会員', '男性利用者', '男性の利用者']],
                [['方', '男性', '人'], [0.4, 0.4, 0.2]], [['方', '女性', '人'], [0.4, 0.4, 0.2]],
                [['ブサイク', 'ブス', 'デブス'], [0.4, 0.4, 0.2]],
                [['ブサイクな', 'ブサメンの', 'イケメンじゃない'], [0.5, 0.2, 0.3]],
                [['美人', '美女', '美形'], [0.5, 0.4, 0.1]], [['イケメン', '男前', 'いい男'], [0.5, 0.4, 0.1]],
                [['かわいい', '美人', '美女', '美形'], [0.5, 0.3, 0.1, 0.1]],  # 20
                [['熟女', '熟年女性']], [['熟年男性', 'イケオジ', 'おじ様']],
                [['人', '女性', '女の人']], [['人', '男性', '男の人']]]
    site_list.remove(site1)
    if len(site_list) <= 1:
        site2 = site_list[0]
    else:
        site2 = np.random.choice(site_list.remove(site1))
    section_list = []
    used_list = []
    mp_code = keywords['act_code'] + '_' + part_code
    # print(mp_code)
    for section in art_map:
        if section[1] == 'straight':
            for s_code in section[0]:
                section_list.append(
                    np.random.choice([x for x in section[0][s_code]
                                      if ((x['info']['only'] and
                                           (keywords['act_code'] in x['info']['only'] or mp_code in x['info']['only']
                                            or part_code in x['info']['only']))
                                          or not x['info']['only'])
                                      and keywords['act_code'] not in x['info']['deny']
                                      and mp_code not in x['info']['deny'] and part_code not in x['info']['deny']
                                      and subject_sex not in x['info']['deny']]))
        else:
            if type(section[1]) == int:
                s_num = section[1]
            else:
                s_num = np.random.choice(section[1])
            sample_l = [x for x in section[0].keys() if x not in used_list]
            # print(sample_l)
            if s_num == 1:
                t1 = [np.random.choice(sample_l)]
            else:
                np.random.shuffle(sample_l)
                t1 = sample_l[:s_num]
            # print(t1)
            for t1e in t1:
                # print(t1e)
                t_list = [x for x in section[0][t1e]
                          if ((x['info']['only'] and
                               (keywords['act_code'] in x['info']['only'] or mp_code in x['info']['only']
                                or part_code in x['info']['only']))
                              or not x['info']['only']) and keywords['act_code'] not in x['info']['deny']
                          and mp_code not in x['info']['deny'] and part_code not in x['info']['deny']
                          and subject_sex not in x['info']['deny']]
                if t_list:
                    section_list.append(
                        np.random.choice([x for x in section[0][t1e]
                                          if ((x['info']['only'] and
                                               (keywords['act_code'] in x['info']['only'] or mp_code in x['info'][
                                                   'only']
                                                or part_code in x['info']['only']))
                                              or not x['info']['only']) and keywords['act_code'] not in x['info'][
                                              'deny']
                                          and mp_code not in x['info']['deny'] and part_code not in x['info']['deny']
                                          and subject_sex not in x['info']['deny']]))
                    used_list.append(t1e)
    # print(section_list)
    this_path = dir_name + '/' + keywords['page_name']
    result_str = ''
    key_phrase = key_phrase_maker(keywords, a_adj_flag, no_obj_flag, no_sub_flag)
    # print(key_phrase)
    # return
    key_phrase['this-site-title'] = [site_data[main_key]['site_name']]
    key_phrase['this-site-author'] = [site_data[main_key]['site_author']]
    noun_dict = {'<!--{}-->'.format(y): [key_phrase[y]] for y in key_phrase}
    for noun in wd.noun_list:
        if 'plist' in noun:
            noun_dict[noun['before']] = [noun['after'], noun['plist']]
        else:
            noun_dict[noun['before']] = [noun['after']]
    if main_key in ['mh', 'olm']:
        noun_dict['<!--sex-->'] = [['結婚']]
        noun_dict['<!--to-sex-->'] = [['結婚']]
        noun_dict['<!--can-sex-->'] = [['結婚できる']]
        noun_dict['<!--h-2-->'] = [['素敵', '魅力的']]
        noun_dict['<!--hな-->'] = [['素敵な', '魅力的な']]
        noun_dict['<!--ero-n-->'] = [['素敵', '魅力的']]
        noun_dict['<!--ero-->'] = [['素敵', '魅力的']]
        noun_dict['<!--sefure-->'] = [['結婚相手']]
        noun_dict['<!--d-app-->'] = [['婚活サイト', '婚活アプリ', 'マッチングサイト', 'マッチングアプリ']]
        noun_dict['<!--site-->'] = [['婚活サイト', '婚活アプリ', 'マッチングサイト', 'マッチングアプリ']]
        noun_dict['<!--deaikei-->'] = [['婚活サイト', '婚活アプリ', 'マッチングサイト', 'マッチングアプリ']]
        noun_dict['<!--net-d-->'] = [['ネット婚活', 'オンラインの出会い', 'オンライン婚活']]
        noun_dict['<!--kiss-or-sof-->'] = [['彼氏', '恋人']]
        noun_dict['<!--eros-degree-->'] = [['真剣さ']]
        noun_dict['<!--be-adult-->'] = [['真面目な', '真剣な', '本気の']]
        noun_dict['<!--adult-->'] = [['結婚相手探し', '婚活', '真面目な出会い', '真剣な出会い', '本気の出会い']]
        noun_dict['<!--adult-bbs-->'] = [['婚活掲示板']]
        noun_dict['<!--kiss-->'] = [['デート']]
    elif main_key in ['bf', 'koi']:
        noun_dict['<!--sex-->'] = [['お付き合い', '交際']]
        noun_dict['<!--to-sex-->'] = [['お付き合い', '交際']]
        noun_dict['<!--can-sex-->'] = [['お付き合いできる', '交際できる', '付き合える', '恋愛できる']]
        noun_dict['<!--h-2-->'] = [['素敵', '魅力的']]
        noun_dict['<!--hな-->'] = [['素敵な', '魅力的な']]
        noun_dict['<!--ero-n-->'] = [['素敵', '魅力的']]
        noun_dict['<!--ero-->'] = [['素敵', '魅力的']]
        noun_dict['<!--sefure-->'] = [['彼氏']]
        noun_dict['<!--d-app-->'] = [['出会いアプリ', '出会い系アプリ', 'マッチングサイト', 'マッチングアプリ', '恋活アプリ']]
        noun_dict['<!--site-->'] = [['出会いアプリ', '出会い系アプリ', 'マッチングサイト', 'マッチングアプリ', '恋活アプリ']]
        noun_dict['<!--deaikei-->'] = [['出会いアプリ', '出会い系アプリ', 'マッチングサイト', 'マッチングアプリ', '恋活アプリ']]
        noun_dict['<!--kiss-or-sof-->'] = [['彼氏', '恋人']]
        noun_dict['<!--eros-degree-->'] = [['真剣さ']]
        noun_dict['<!--be-adult-->'] = [['真面目な', '真剣な', '本気の']]
        noun_dict['<!--adult-->'] = [['彼氏探し', '恋活', '恋人探し', '真剣な出会い', '本気の出会い', '真面目な出会い']]
        noun_dict['<!--adult-bbs-->'] = [['恋人募集掲示板', '彼氏募集掲示板']]
        noun_dict['<!--kiss-->'] = [['デート']]
    elif main_key == 'cov':
        noun_dict['<!--d-app-->'] = [['マッチングアプリ', 'マッチングサイト'], [0.8, 0.2]]
        noun_dict['<!--site-->'] = [['マッチングアプリ', 'マッチングサイト'], [0.8, 0.2]]
        noun_dict['<!--deaikei-->'] = [['マッチングアプリ', 'マッチングサイト'], [0.8, 0.2]]
        noun_dict['<!--net-d-->'] = [['オンラインの出会い', 'ネットの出会い'], [0.8, 0.2]]
        noun_dict['<!--adult-bbs-->'] = [['マッチングアプリ', 'マッチングサイト'], [0.8, 0.2]]
        noun_dict['<!--d-bbs-->'] = [['マッチングアプリ', 'マッチングサイト'], [0.8, 0.2]]
        noun_dict['<!--s-bbs-->'] = [['マッチングアプリ', 'マッチングサイト'], [0.8, 0.2]]
        noun_dict['<!--pure-bbs-->'] = [['マッチングアプリ', 'マッチングサイト'], [0.8, 0.2]]
        noun_dict['<!--b-bbs-->'] = [['マッチングアプリ', 'マッチングサイト'], [0.8, 0.2]]

    if subject_sex == 'man':
        noun_dict['<!--sub-sex-->'] = sex_dict[0]
        noun_dict['<!--obj-sex-->'] = sex_dict[1]
        noun_dict['<!--obj-sex-o-->'] = sex_dict[2]
        noun_dict['<!--obj-sex-y-->'] = sex_dict[3]
        noun_dict['<!--obj-partner-->'] = sex_dict[4]
        noun_dict['<!--sub-partner-->'] = sex_dict[5]
        noun_dict['<!--obj-l-partner-->'] = sex_dict[6]
        noun_dict['<!--sub-l-partner-->'] = sex_dict[7]
        noun_dict['<!--obj-married-->'] = sex_dict[8]
        noun_dict['<!--sub-married-->'] = sex_dict[9]
        noun_dict['<!--obj-virgin-->'] = sex_dict[10]
        noun_dict['<!--sub-virgin-->'] = sex_dict[11]
        noun_dict['<!--obj-user-->'] = sex_dict[12]
        noun_dict['<!--sub-reader-->'] = sex_dict[14]
        noun_dict['<!--obj-not-beauty-->'] = sex_dict[16]
        noun_dict['<!--sub-not-beauty-->'] = sex_dict[17]
        noun_dict['<!--obj-beauty-->'] = sex_dict[18]
        noun_dict['<!--sub-beauty-->'] = sex_dict[19]
        noun_dict['<!--obj-beauty-y-->'] = sex_dict[20]
        noun_dict['<!--sub-beauty-y-->'] = sex_dict[19]
        noun_dict['<!--obj-older-->'] = sex_dict[21]
        noun_dict['<!--target-person-->'] = sex_dict[23]
    else:
        noun_dict['<!--sub-sex-->'] = sex_dict[1]
        noun_dict['<!--obj-sex-->'] = sex_dict[0]
        noun_dict['<!--obj-sex-o-->'] = sex_dict[0]
        noun_dict['<!--obj-sex-y-->'] = sex_dict[0]
        noun_dict['<!--obj-partner-->'] = sex_dict[5]
        noun_dict['<!--sub-partner-->'] = sex_dict[4]
        noun_dict['<!--obj-l-partner-->'] = sex_dict[7]
        noun_dict['<!--sub-l-partner-->'] = sex_dict[6]
        noun_dict['<!--obj-married-->'] = sex_dict[9]
        noun_dict['<!--sub-married-->'] = sex_dict[8]
        noun_dict['<!--obj-virgin-->'] = sex_dict[11]
        noun_dict['<!--sub-virgin-->'] = sex_dict[10]
        noun_dict['<!--obj-user-->'] = sex_dict[13]
        noun_dict['<!--sub-reader-->'] = sex_dict[15]
        noun_dict['<!--obj-not-beauty-->'] = sex_dict[17]
        noun_dict['<!--sub-not-beauty-->'] = sex_dict[16]
        noun_dict['<!--obj-beauty-->'] = sex_dict[19]
        noun_dict['<!--sub-beauty-->'] = sex_dict[18]
        noun_dict['<!--obj-beauty-y-->'] = sex_dict[19]
        noun_dict['<!--sub-beauty-y-->'] = sex_dict[20]
        noun_dict['<!--obj-older-->'] = sex_dict[22]
        noun_dict['<!--target-person-->'] = sex_dict[24]

    if not no_sub_flag:
        noun_dict['<!--sub-reader-->'][0][1] = keywords['sub']
        noun_dict['<!--sub-reader-->'][0][2] = keywords['sub']
    conj_dict = {x['before']: x['after'] for x in wd.conj_list}
    title_count = 40
    title_str = ''
    while title_count > 35:
        title_str, t_recipe, counter_d = make_new_title(source_mod.title[part_code][main_key], noun_dict, conj_dict,
                                                        site1, site2, link_dict, this_path, subject_sex, recipe_flag,
                                                        main_key, part_code, project_dir, counter_d)
        title_count = len(re.sub(r'<!--sw-.*?-->', '', title_str))
    print('{}  ({})'.format(title_str, title_count))
    result_str += 't::' + title_str + '\n'
    des_str, d_recipe, counter_d = make_new_title(source_mod.des[keywords['act_code']], noun_dict, conj_dict, site1,
                                                  site2, link_dict, this_path, subject_sex, recipe_flag, main_key,
                                                  part_code, project_dir, counter_d)
    result_str += 'd::' + des_str.replace('\n', '') + '\n'
    # print(used_id)
    # print(type(used_id[-1]))
    # print(type(keywords['id']))
    result_str += 'n::' + str(add_id_dict[int(keywords['id'])]) + '\n'
    result_str += 'e::\n'
    if dt_str:
        result_str += 'p::' + dt_str + '\n'
    if main_key in ['mh', 'olm']:
        result_str += 'a::' + str(keywords['ad']) + '\n'
        result_str += 'k::' + ' '.join([keywords['all_key'], '婚活']) + '\n'
    elif main_key in ['bf', 'koi'] and part_code == 'obj':
        result_str += 'a::' + str(keywords['ad']) + '\n'
        result_str += 'k::' + ' '.join([keywords['all_key'], '恋活']) + '\n'
    elif main_key == 'cov':
        result_str += 'k::' + ' '.join([keywords['all_key'], 'コロナ禍 マッチングアプリ']) + '\n'
    elif part_code == 'act':
        result_str += 'k::' + keywords['all_key'] + '\n'
    elif main_key == 'dt':
        result_str += 'k::' + keywords['all_key'] + ' 童貞卒業\n'
    else:
        result_str += 'k::' + ' '.join([keywords['all_key'], keywords['act'].replace('する', '')]) + '\n'

    for this_sec in section_list:
        section_str, recipe, counter_d = make_new_section(this_sec, noun_dict, conj_dict, site1, site2, link_dict,
                                                          this_path, recipe_flag, subject_sex, main_key, part_code,
                                                          project_dir, counter_d)
        section_str = section_str.replace('%', '\n%')
        result_str += section_str + '\n\n'
        recipe_list[this_sec['info']['sec_name']] = recipe
    # if 'ins_link_' in result_str:
    #     result_str = result_str.replace('ins_link_', html_head + '_')
    result_str = replace_code_to_md(result_str, subject_sex)
    result_str = result_str.replace('\n\n- ', '\n\n%arlist%\n- ')
    if keywords['replace_words']:
        for r_words in keywords['replace_words']:
            result_str = result_str.replace(r_words[0], r_words[1])
    result_str = insert_ds_link(result_str, project_dir)
    result_str += 'recipe_list = ' + str(recipe_list) + '\n\n'
    result_str += 'use_keywords = ' + str(keywords)
    # print(result_str)
    if project_dir in ['reibun']:
        dir_name = 'pc/' + dir_name
    with open(project_dir + '/md_files/' + dir_name + '/' + keywords['page_name'] + '.md', 'w', encoding='utf-8') as f:
        f.write(result_str)
    return recipe_list, counter_d


def replace_code_to_md(md_str, subject_sex):
    if subject_sex == 'man':
        replace_list = [['%rp', '%r_palm%\n'], ['%r?', '%r_?%\n'], ['%r!', '%r_!%\n'], ['%l!', '%l_!%\n']]
    else:
        replace_list = [['%rp', '%rw_palm%\n'], ['%r?', '%rw_?%\n'], ['%r!', '%rw_!%\n'], ['%l!', '%l_!%\n']]
    for r_list in replace_list:
        md_str = md_str.replace(r_list[0], r_list[1])
    return md_str


def insert_ds_link(md_str, project_dir):
    sc_url = {'ワクワクメール': '550909', 'PCMAX': 'pcmax',
              'ハッピーメール': 'happymail', 'Jメール': 'mintj'}
    if project_dir == 'reibun':
        main_dir = 'pc/'
        aff_dir = 'ds'
    elif project_dir == 'rei_site':
        main_dir = ''
        aff_dir = 'site_data'
    elif project_dir == 'joshideai':
        main_dir = ''
        aff_dir = 'site_page'
    else:
        main_dir = ''
        aff_dir = 'link'
    main_str = re.sub(r'^([\s\S]+?\n)## ', '##', md_str)
    str_list = main_str.split('\n')
    for key in sc_url:
        if aff_dir + '/' + sc_url[key] not in md_str:
            for row in str_list:
                if '##' not in row and not row.startswith('- '):
                    if key in row and '](' not in row:
                        i_url = '[{}(R18)](../../{}html_files/{}{}/{})'.format(key, '../' * main_dir.count('/'),
                                                                               main_dir, aff_dir, sc_url[key])
                        new_row = row.replace(key, i_url)
                        md_str = md_str.replace(row, new_row)
                        # print('insert {} link str'.format(key))
                        # used_name.append(key)
                        break
    return md_str


def key_phrase_maker(keywords, a_adj_flag, no_obj_flag, no_sub_flag):
    if '作る' in keywords['act']:
        act_base = keywords['act']
        act_i = act_base.replace('を作る', 'にし')
        act_and = act_base.replace('作る', '作って')
        act_can = act_base.replace('作る', '作れ')
        act_can_d = act_base.replace('を作る', 'にでき')
        act_noun = keywords['act_noun']
        if 'act_target' in keywords['act_target']:
            act_target = keywords['act_target']
        else:
            act_target = act_base.replace('を作る', '')
        act_with = keywords['obj_p']
        act_with_g = keywords['obj_p']
        act_with_d = 'を'
        act_way = act_noun + '<!--make-way-->'
        act_way_g = act_noun + '<!--make-way-g-->'
        obj = keywords['obj']
        obj_k = keywords['obj_key']
        if keywords['obj_p'] == 'no' or keywords['obj_p'] == 'n' or keywords['obj_p'] == '':
            obj_as_target = keywords['obj_key'] + keywords['act_noun']
        else:
            obj_as_target = keywords['obj_key'] + keywords['obj_p'] + keywords['act_noun']
        connection = keywords['act_connection']
    elif keywords['act_code'] == 'dt':
        act_base = keywords['act']
        act_i = '<!--lost-dt-i-->'
        act_and = '<!--lost-dt-i-->' + 'て'
        act_can = '<!--lost-dt-can-->'
        act_can_d = '<!--lost-dt-can-->'
        act_noun = keywords['act_noun']
        act_target = keywords['act_noun']
        act_with = 'と'
        act_with_g = 'と'
        act_with_d = 'と'
        act_way = keywords['act'] + '<!--way-->'
        act_way_g = keywords['act'] + '<!--way-->'
        obj = keywords['obj']
        obj_k = keywords['obj_key']
        obj_as_target = keywords['obj_key'] + keywords['obj_p'] + keywords['act_noun']
        connection = keywords['act_connection']
    elif '出会う' in keywords['act']:
        act_base = keywords['act']
        act_i = act_base.replace('出会う', '出会い')
        act_and = act_base.replace('出会う', '出会って')
        act_can = act_base.replace('出会う', '出会え')
        act_can_d = act_base.replace('出会う', '出会え')
        act_noun = keywords['act_noun']
        act_with = 'と'
        act_with_g = 'と'
        act_with_d = 'と'
        act_way = act_base + '<!--way-->'
        act_way_g = act_base + '<!--way-->'
        obj = keywords['obj']
        obj_k = keywords['obj']
        if keywords['act_target']:
            act_target = keywords['act_target']
            obj_as_target = act_target + 'の' + obj
        else:
            if keywords['act_code'] in no_adult_prj:
                act_target = '結婚相手'
                obj_as_target = '<!--sub-l-partner-->にしたい' + obj
            else:
                act_target = act_base.replace('出会う', '出会い')
                obj_as_target = act_target + 'の' + obj
        connection = keywords['act_connection']
    elif 'をする' in keywords['act']:
        act_base = keywords['act']
        act_i = act_base.replace('する', 'し')
        act_and = act_base.replace('する', 'して')
        act_can = act_base.replace('をする', 'ができ')
        act_can_d = act_base.replace('をする', 'ができ')
        act_noun = keywords['act_noun']
        if keywords['act_target']:
            act_target = keywords['act_target']
        else:
            act_target = act_base.replace('する', '相手')
        act_with = 'と'
        act_with_g = 'と'
        act_with_d = 'と'
        act_way = act_base + '<!--way-->'
        act_way_g = act_base + '<!--way-->'
        obj = keywords['obj']
        obj_k = keywords['obj']
        obj_as_target = act_target + 'の' + obj
        connection = keywords['act_connection']
    elif 'する' in keywords['act']:
        act_base = keywords['act']
        act_i = act_base.replace('する', 'し')
        act_and = act_base.replace('する', 'して')
        act_can = act_base.replace('する', 'でき')
        act_can_d = act_base.replace('する', 'でき')
        act_noun = keywords['act_noun']
        if keywords['act_target']:
            act_target = keywords['act_target']
        else:
            act_target = act_base.replace('する', '相手')
        act_with = 'と'
        act_with_g = 'と'
        act_with_d = 'と'
        act_way = act_base + '<!--way-->'
        act_way_g = act_base + '<!--way-->'
        obj = keywords['obj']
        obj_k = keywords['obj']
        obj_as_target = act_target + 'の' + obj
        connection = keywords['act_connection']
    elif 'なる' in keywords['act']:
        act_base = keywords['act']
        act_i = act_base.replace('なる', 'なり')
        act_and = act_base.replace('なる', 'なって')
        act_can = act_base.replace('なる', 'なれ')
        act_can_d = act_base.replace('なる', 'なれ')
        act_noun = keywords['act_noun']
        if keywords['act_target']:
            act_target = keywords['act_target']
        else:
            act_target = act_base.replace('なる', '相手')
        act_with = 'と'
        act_with_g = 'と'
        act_with_d = 'と'
        act_way = act_base + '<!--way-->'
        act_way_g = act_base + '<!--way-->'
        obj = keywords['obj']
        obj_k = keywords['obj']
        obj_as_target = act_target + 'の' + obj
        connection = keywords['act_connection']
    elif 'てもらう' in keywords['act']:
        act_base = keywords['act']
        act_i = act_base.replace('てもらう', 'てもらい')
        act_and = act_base.replace('てもらう', 'てもらって')
        act_can = act_base.replace('てもらう', 'てもらえ')
        act_can_d = act_base.replace('てもらう', 'てもらえ')
        act_noun = keywords['act_noun']
        if keywords['act_target']:
            act_target = keywords['act_target']
        else:
            act_target = act_base.replace('てもらう', '相手')
        act_with = 'に'
        act_with_g = 'に'
        act_with_d = 'に'
        act_way = act_base + '<!--way-->'
        act_way_g = act_base + '<!--way-->'
        obj = keywords['obj']
        obj_k = keywords['obj']
        obj_as_target = act_target + 'の' + obj
        connection = keywords['act_connection']
    elif keywords['act'].endswith('う'):
        act_base = keywords['act']
        act_i = re.sub(r'う$', 'い', act_base)
        act_and = re.sub(r'う$', 'って', act_base)
        act_can = re.sub(r'う$', 'い', act_base)
        act_can_d = re.sub(r'う$', 'え', act_base)
        act_noun = keywords['act_noun']
        if keywords['act_target']:
            act_target = keywords['act_target']
        else:
            act_target = re.sub(r'う$', 'う相手', act_base)
        act_with = 'と'
        act_with_g = 'と'
        act_with_d = 'と'
        act_way = act_base + '<!--way-->'
        act_way_g = act_base + '<!--way-->'
        obj = keywords['obj']
        obj_k = keywords['obj']
        obj_as_target = act_target + 'の' + obj
        connection = keywords['act_connection']
    elif keywords['act'].endswith('す'):
        act_base = keywords['act']
        act_i = re.sub(r'す$', 'し', act_base)
        act_and = re.sub(r'す$', 'して', act_base)
        act_can = re.sub(r'す$', 'せ', act_base)
        act_can_d = re.sub(r'す$', 'せ', act_base)
        act_noun = keywords['act_noun']
        if keywords['act_target']:
            act_target = keywords['act_target']
        else:
            act_target = re.sub(r'す$', 'す相手', act_base)
        act_with = 'と'
        act_with_g = 'と'
        act_with_d = 'と'
        act_way = act_base + '<!--way-->'
        act_way_g = act_base + '<!--way-->'
        obj = keywords['obj']
        obj_k = keywords['obj']
        obj_as_target = act_target + 'の' + obj
        connection = keywords['act_connection']
    elif keywords['act'].endswith('てる'):
        act_base = keywords['act']
        act_i = re.sub(r'てる$', 'て', act_base)
        act_and = re.sub(r'てる$', 'てて', act_base)
        act_can = re.sub(r'てる$', 'てられ', act_base)
        act_can_d = re.sub(r'てる$', 'てられ', act_base)
        act_noun = keywords['act_noun']
        if keywords['act_target']:
            act_target = keywords['act_target']
        else:
            act_target = re.sub(r'てる$', 'てる相手', act_base)
        act_with = 'と'
        act_with_g = 'と'
        act_with_d = 'と'
        act_way = act_base + '<!--way-->'
        act_way_g = act_base + '<!--way-->'
        obj = keywords['obj']
        obj_k = keywords['obj']
        obj_as_target = act_target + 'の' + obj
        connection = keywords['act_connection']
    elif keywords['act'].endswith('れる'):
        act_base = keywords['act']
        act_i = re.sub(r'れる$', 'れ', act_base)
        act_and = re.sub(r'れる$', 'って', act_base)
        act_can = re.sub(r'れる$', 'れ', act_base)
        act_can_d = re.sub(r'れる$', 'れ', act_base)
        act_noun = keywords['act_noun']
        if keywords['act_target']:
            act_target = keywords['act_target']
        else:
            act_target = re.sub(r'れる$', 'れる相手', act_base)
        act_with = 'を'
        act_with_g = 'を'
        act_with_d = 'を'
        act_way = act_base + '<!--way-->'
        act_way_g = act_base + '<!--way-->'
        obj = keywords['obj']
        obj_k = keywords['obj']
        obj_as_target = act_target + 'の' + obj
        connection = keywords['act_connection']
    elif keywords['act'].endswith('せる'):
        act_base = keywords['act']
        act_i = re.sub(r'せる$', 'せ', act_base)
        act_and = re.sub(r'せる$', 'せて', act_base)
        act_can = re.sub(r'せる$', 'せられ', act_base)
        act_can_d = re.sub(r'せる$', 'せられ', act_base)
        act_noun = keywords['act_noun']
        if keywords['act_target']:
            act_target = keywords['act_target']
        else:
            act_target = re.sub(r'せる$', 'せる相手', act_base)
        act_with = 'を'
        act_with_g = 'を'
        act_with_d = 'を'
        act_way = act_base + '<!--way-->'
        act_way_g = act_base + '<!--way-->'
        obj = keywords['obj']
        obj_k = keywords['obj']
        obj_as_target = act_target + 'の' + obj
        connection = keywords['act_connection']
    elif keywords['act'].endswith('く'):
        act_base = keywords['act']
        act_i = re.sub(r'く$', 'き', act_base)
        act_and = re.sub(r'く$', 'って', act_base)
        act_can = re.sub(r'く$', 'け', act_base)
        act_can_d = re.sub(r'く$', 'け', act_base)
        act_noun = keywords['act_noun']
        if keywords['act_target']:
            act_target = keywords['act_target']
        else:
            act_target = re.sub(r'く$', 'く相手', act_base)
        act_with = 'を'
        act_with_g = 'を'
        act_with_d = 'を'
        act_way = act_base + '<!--way-->'
        act_way_g = act_base + '<!--way-->'
        obj = keywords['obj']
        obj_k = keywords['obj']
        obj_as_target = act_target + 'の' + obj
        connection = keywords['act_connection']
    elif keywords['act'].endswith('る'):
        act_base = keywords['act']
        act_i = re.sub(r'る$', 'り', act_base)
        act_and = re.sub(r'る$', 'って', act_base)
        act_can = re.sub(r'る$', 'れ', act_base)
        act_can_d = re.sub(r'る$', 'れ', act_base)
        act_noun = keywords['act_noun']
        if keywords['act_target']:
            act_target = keywords['act_target']
        else:
            act_target = re.sub(r'る$', 'る相手', act_base)
        act_with = 'を'
        act_with_g = 'を'
        act_with_d = 'を'
        act_way = act_base + '<!--way-->'
        act_way_g = act_base + '<!--way-->'
        obj = keywords['obj']
        obj_k = keywords['obj']
        obj_as_target = act_target + 'の' + obj
        connection = keywords['act_connection']
    else:
        # print(keywords)
        act_base = keywords['act']
        act_i = act_base.replace('する', 'し')
        act_and = act_base.replace('する', 'して')
        act_can = act_base.replace('する', 'でき')
        act_can_d = act_base.replace('する', 'でき')
        act_noun = keywords['act_noun']
        if keywords['act_target']:
            act_target = keywords['act_target']
        else:
            act_target = act_base.replace('する', '相手')
        act_with = 'と'
        act_with_g = 'と'
        act_with_d = 'と'
        act_way = act_base + '<!--way-->'
        act_way_g = act_base + '<!--way-->'
        obj = keywords['obj']
        obj_k = keywords['obj']
        obj_as_target = act_target + 'の' + obj
        connection = keywords['act_connection']
    if keywords['o_sex'] == 'w':
        target_person = '<!--woman-{}-->'.format(keywords['o_age'])
    elif keywords['o_sex'] == 'm':
        target_person = '<!--man-->'
    else:
        target_person = '人'
    if keywords['o_cat'] == 'j':
        obj_cat1 = '職業'
        obj_cat2 = '職業'
    elif keywords['o_cat'] == 'a':
        obj_cat1 = '年代'
        obj_cat2 = 'タイプ'
    elif keywords['o_cat'] == 'c':
        obj_cat1 = '性格'
        obj_cat2 = 'タイプ'
    elif keywords['o_cat'] == 'b':
        obj_cat1 = '体型'
        obj_cat2 = 'タイプ'
    elif keywords['o_cat'] == 'l':
        obj_cat1 = '見た目'
        obj_cat2 = 'タイプ'
    elif keywords['o_cat'] == 's':
        obj_cat1 = '性的嗜好'
        obj_cat2 = 'タイプ'
    else:
        obj_cat1 = 'タイプ'
        obj_cat2 = 'タイプ'
    sub = keywords['sub']
    sub_adj = keywords['s_adj']
    obj_adj = keywords['o_adj']
    if keywords['2act_w']:
        act2_w = keywords['2act_w']
    else:
        act2_w = act_i + 'たい'
    if keywords['2act_noun']:
        act2_n = keywords['2act_noun']
    else:
        act2_n = act_noun
    if '2act_do' in keywords:
        act2_d = keywords['2act_do']
        if 'する' in keywords['2act_do']:
            act2_i = keywords['2act_do'].replace('する', 'し')
        else:
            act2_i = keywords['2act_do'].replace('る', 'り')
    else:
        act2_d = act_base
        act2_i = act_i
    if a_adj_flag:
        act_adj = ''
        m_act_adj = keywords['a_adj']
    else:
        act_adj = keywords['a_adj']
        m_act_adj = ''
    if no_sub_flag:
        alt_sub_s = ''
        alt_sub = ''
        sub_also = ''
        sub_by = ''
    else:
        alt_sub_s = ''
        alt_sub = sub + 'が'
        sub_also = sub + 'でも'
        sub_by = sub + 'の'
    if no_obj_flag:
        alt_obj = ''
        alt_obj_g = ''
        alt_obj_d = ''
        alt_target = act_target
        if '女子' in obj:
            s_obj = '女子'
        else:
            s_obj = '女性'
    else:
        alt_obj = obj + act_with
        alt_obj_g = obj + act_with_g
        alt_obj_d = obj + act_with_d
        alt_target = obj
        s_obj = obj

    keys = {'k-how-to': [sub + 'が' + m_act_adj + obj + act_with_g + act_way_g,
                         sub + 'が' + m_act_adj + obj_adj + obj + act_with_g + act_way_g,
                         alt_sub + m_act_adj + obj + act_with_g + act_way_g,
                         alt_sub + m_act_adj + obj_adj + obj + act_with_g + act_way_g,
                         ],
            'k-how-to-adj': [sub + 'が' + m_act_adj + obj_adj + obj + act_with_g + act_way_g,
                             alt_sub + m_act_adj + obj_adj + obj + act_with_g + act_way_g],
            'k-can': [sub + 'が' + obj + act_with + act_can + 'る',
                      alt_sub + obj + act_with + act_can + 'る'],
            'k-can-s': [sub + 'が' + obj + act_with + act_can + 'ます',
                        alt_sub + obj + act_with + act_can + 'ます'],
            'k-do': [sub + 'が' + m_act_adj + obj + act_with + act_base,
                     alt_sub + m_act_adj + obj + act_with + act_base],
            'k-do-a': [sub + 'が' + m_act_adj + obj_adj + obj + act_with + act_base,
                       alt_sub + m_act_adj + obj_adj + obj + act_with + act_base],
            'k-easy': [sub + 'が' + m_act_adj + obj + act_with_d + act_i + 'やすい',
                       alt_sub + m_act_adj + obj + act_with_d + act_i + 'やすい'],
            'k-want': [sub + 'が' + m_act_adj + obj + act_with_d + act_i + 'たい',
                       alt_sub + m_act_adj + obj + act_with_d + act_i + 'たい'],
            'k-find': [sub + 'が' + m_act_adj + obj + 'の' + act_target + 'を探す',
                       alt_sub + m_act_adj + obj + 'の' + act_target + 'を探す'],

            'k-rnd-how-to': [sub + 'が' + m_act_adj + obj + act_with_g + act_way_g,
                             sub + 'が' + m_act_adj + alt_obj + act_way_g,
                             sub + 'が' + m_act_adj + obj_adj + obj + act_with_g + act_way_g,
                             sub + 'が' + m_act_adj + obj_adj + alt_obj + act_way_g,
                             alt_sub + m_act_adj + obj + act_with_g + act_way_g,
                             alt_sub + m_act_adj + alt_obj + act_way_g,
                             alt_sub + m_act_adj + obj_adj + obj + act_with_g + act_way_g,
                             alt_sub + m_act_adj + obj_adj + alt_obj + act_way_g,
                             ],
            'k-rnd-how-to-adj': [sub + 'が' + m_act_adj + obj_adj + obj + act_with_g + act_way_g,
                                 alt_sub + m_act_adj + obj_adj + obj + act_with_g + act_way_g],
            'k-rnd-can': [sub + 'が' + obj + act_with + act_can + 'る',
                          alt_sub + obj + act_with + act_can + 'る'],
            'k-rnd-can-s': [sub + 'が' + obj + act_with + act_can + 'ます',
                            alt_sub + obj + act_with + act_can + 'ます'],
            'k-rnd-do': [sub + 'が' + m_act_adj + obj + act_with + act_base,
                         sub + 'が' + m_act_adj + alt_obj + act_base,
                         alt_sub + m_act_adj + obj + act_with + act_base,
                         alt_sub + m_act_adj + alt_obj + act_base],
            'k-rnd-do-a': [sub + 'が' + m_act_adj + obj_adj + obj + act_with + act_base,
                           alt_sub + m_act_adj + obj_adj + obj + act_with + act_base],
            'k-rnd-easy': [sub + 'が' + m_act_adj + obj + act_with_d + act_i + 'やすい',
                           alt_sub + m_act_adj + obj + act_with_d + act_i + 'やすい'],
            'k-rnd-want': [sub + 'が' + m_act_adj + obj + act_with_d + act_i + 'たい',
                           alt_sub + m_act_adj + obj + act_with_d + act_i + 'たい'],
            'k-rnd-find': [sub + 'が' + m_act_adj + obj + 'の' + act_target + 'を探す',
                           alt_sub + m_act_adj + obj + 'の' + act_target + 'を探す'],

            'k-alt-sub': [alt_sub_s],
            'k-alt-can-do': [alt_sub + m_act_adj + alt_obj + act_can + 'る'],
            'k-alt-can-do-a': [alt_sub + m_act_adj + obj_adj + alt_obj + act_can + 'る'],
            'k-alt-can-do-long': [alt_sub + m_act_adj + alt_obj + act_can + 'ます'],
            'k-alt-can-not-do': [alt_sub + m_act_adj + alt_obj + act_can + 'ない'],
            'k-alt-can-not-do-long': [alt_sub + m_act_adj + alt_obj + act_can + 'ません'],
            'k-alt-way': [alt_sub + m_act_adj + alt_obj + act_way, alt_obj_g + act_way_g],
            'k-alt-do': [alt_sub + m_act_adj + alt_obj + act_base],
            'k-alt-do-a': [alt_sub + m_act_adj + obj_adj + alt_obj + act_base],
            'k-alt-easy': [alt_sub + m_act_adj + alt_obj_d + act_i + 'やすい'],
            'k-alt-to-find': [sub_by + obj_as_target + '探し'],
            'k-alt-to-find-a': [sub_by + obj_adj + obj_as_target + '探し'],
            'k-alt-find': [alt_sub + m_act_adj + obj_as_target + 'を探す'],
            'k-alt-find-a': [alt_sub + m_act_adj + obj_adj + obj_as_target + 'を探す'],

            'k-obj': [obj],
            'k-obj-adj': [obj + 'の'],
            'k-obj-status': [obj],
            'k-obj-noun': [obj_adj + obj, obj],
            'k-obj-noun-l': [obj_adj + obj],
            'k-obj-noun-s': [s_obj],
            'k-obj-noun-s-alt': [s_obj, alt_target],
            'k-obj-noun-j': [obj_adj + obj, obj],
            'k-obj-target': [obj_as_target],
            'k-obj-want': [act_i + 'たい' + obj],
            'k-obj-wife': ['<!--obj-married-->の' + obj],
            'k-obj-act-find': [m_act_adj + obj_as_target + 'を探す'],
            'k-obj-act-find-a': [m_act_adj + obj_adj + obj_as_target + 'を探す'],
            'k-obj-act-can-find': [m_act_adj + obj_as_target + 'が見つかる', m_act_adj + obj_as_target + 'が探せる'],
            'k-obj-act-can-do': [m_act_adj + obj + act_with + act_can + 'る'],
            'k-obj-act-can-do-a': [m_act_adj + obj_adj + obj + act_with + act_can + 'る'],
            'k-obj-act-can-do-long': [m_act_adj + obj + act_with + act_can + 'ます'],
            'k-obj-act-can-not-do': [m_act_adj + obj + act_with + act_can + 'ない'],
            'k-obj-act-can-not-do-long': [m_act_adj + obj + act_with + act_can + 'ません'],
            'k-obj-act-to-find': [obj_as_target + '探し'],
            'k-obj-act-to-find-a': [obj_adj + obj_as_target + '探し'],
            'k-obj-act-want': [m_act_adj + obj + act_with_d + act_i + 'たい',
                               m_act_adj + obj + act_with_d + act_i + 'たい'],
            'k-obj-act-want-a': [m_act_adj + obj_adj + obj + act_with_d + act_i + 'たい'],
            'k-obj-act-way': [m_act_adj + obj + act_with + act_way, obj + act_with_g + act_way_g],
            'k-obj-act-do': [m_act_adj + obj + act_with + act_base],
            'k-obj-act-do-a': [m_act_adj + obj_adj + obj + act_with + act_base],
            'k-obj-act-easy': [m_act_adj + obj + act_with_d + act_i + 'やすい'],
            'k-obj-act-find-easy': [m_act_adj + act_can_d + 'る' + obj + 'を探しやすい',
                                    m_act_adj + act_can_d + 'る' + obj + 'を見つけやすい'],
            'k-obj-act-can-meet': [m_act_adj + obj_as_target + 'と出会える'],
            'k-obj-act-can-meet-a': [m_act_adj + obj_adj + obj_as_target + 'と出会える'],
            'k-obj-act-noun': [obj_as_target],
            'k-obj-act-noun-a': [obj_adj + obj_as_target],
            'k-act': [m_act_adj + act_base, m_act_adj + act_adj + act_base],
            'k-act-adj': [m_act_adj + act_adj + act_base],
            'k-act-adj-b': [m_act_adj + act_adj],
            'k-act-i': [m_act_adj + act_i],
            'k-act-and': [m_act_adj + act_and],
            'k-act-want': [m_act_adj + act_i + 'たい'],
            'k-act-want-sim': [act_i + 'たい'],
            'k-act-can': [act_can + 'る', act_can_d + 'る'],
            'k-act-can-adj': [m_act_adj + act_can + 'る', m_act_adj + act_can_d + 'る'],
            'k-act-can-i': [act_can],  # セフレにでき（そう）,セックスでき(ない）
            'k-act-can-d-i': [act_can_d],  # セフレにでき
            'k-act-can-long': [act_can + 'ます'],
            'k-act-can-not-do': [act_can + 'ない'],
            'k-act-can-not-do-long': [act_can + 'ません'],
            'k-act-way': [m_act_adj + act_way, act_way],
            'k-act-way-sim': [act_way],
            'k-act-way-adj': [m_act_adj + act_way],
            'k-act-can-easy': [act_i + 'やすい', '<!--easily-->' + act_can + 'る'],
            'k-act-to-find': [act_target + '探し'],
            'k-act-find': [act_target + 'を探す'],
            'k-act-can-find': [act_target + 'を探せる'],
            'k-act-can-find-long': [act_target + 'を探せます'],
            'k-act-noun': [act_noun],  # セックス、セフレを
            'k-act-noun-f': [act_noun],  # セフレを作る、彼女を作る等actが名詞と動詞でできているもの限定
            'k-act-v-can': ['でき'],  # でき（る）、作れ(る)
            'k-act-v-do': ['す'],  # す（る）、作(る)
            'k-act-v-i': ['す'],  # 探し（て）、作(って)
            'k-act-connection': connection,
            'k-act-target': [act_target],
            'k-sub': [sub],
            'k-sub-adj': [sub_adj + sub],
            'k-sub-want': [act_i + 'たい' + sub],
            'k-sub-act-do': [sub + 'が' + m_act_adj + act_base],
            'k-sub-act-can': [sub + 'が' + m_act_adj + act_can + 'る'],
            'k-sub-act-can-s': [sub + 'が' + m_act_adj + act_can + 'ます'],
            'k-sub-act-way': [sub + 'が' + m_act_adj + act_way_g,
                              sub + 'が' + m_act_adj + act_way_g],
            'k-sub-act-want': [sub + 'が' + m_act_adj + act_i + 'たい'],
            'k-sub-act-can-easy': [sub + 'が' + act_i + 'やすい', sub + 'が' + '<!--easily-->' + act_can + 'る'],

            'k-sub-is': [alt_sub],
            'k-sub-also': [sub_also],
            'k-sub-by': [sub_by],

            'k-obj-category': [obj_cat1],
            'k-obj-category2': [obj_cat2],
            'k-2nd-act-noun': [act2_n],
            'k-2nd-act-want': [act2_w],
            'k-2nd-act': [act2_d],
            'k-2nd-act-i': [act2_i],
            'k-a-adj': [m_act_adj + act_adj],
            'k-a-adj-make': [m_act_adj + act_adj],
            'target-parson': [target_person],
            'reason': keywords['o_reason'],
            'act-with-d': [act_with_d]}
    if 'を作って' in keywords['a_adj']:
        if keywords['obj_p'] == 'と':
            add_str = 'と'
        elif keywords['obj_p'] == 'に':
            add_str = 'に'
        elif keywords['obj_p'] == 'を':
            add_str = 'を'
        else:
            add_str = ''
        if add_str:
            with_adj = keywords['a_adj'].replace('を作って', add_str)
            add_keys = {
                'k-act': [with_adj + act_base, with_adj + act_adj + act_base],
                'k-act-adj': [with_adj + act_adj + act_base],
                'k-act-adj-b': [with_adj + act_adj],
                'k-act-i': [with_adj + act_i],
                'k-act-and': [with_adj + act_and],
                'k-act-want': [with_adj + act_i + 'たい'],
                'k-act-can': [act_can + 'る', act_can_d + 'る'],
                'k-act-can-adj': [with_adj + act_can + 'る', with_adj + act_can_d + 'る'],
                'k-act-way': [with_adj + act_way, act_way],
                'k-act-way-adj': [with_adj + act_way],
                'k-a-adj': [with_adj + act_adj]}
            for a_key in add_keys:
                keys[a_key].extend(add_keys[a_key])
    if no_obj_flag:
        add_keys = {'k-how-to': [sub + 'が' + m_act_adj + act_way_g,
                                 sub + 'が' + m_act_adj + obj_adj + act_way_g],
                    'k-how-to-adj': [sub + 'が' + m_act_adj + obj_adj + act_way_g],
                    'k-can': [sub + 'が' + act_can + 'る'],
                    'k-can-s': [sub + 'が' + act_can + 'ます'],
                    'k-do': [sub + 'が' + m_act_adj + act_base],
                    'k-do-a': [sub + 'が' + m_act_adj + obj_adj + act_base],
                    'k-easy': [sub + 'が' + m_act_adj + obj + act_with_d + act_i + 'やすい'],
                    'k-want': [sub + 'が' + m_act_adj + obj + act_with_d + act_i + 'たい'],
                    'k-obj-act-can-do': [m_act_adj + act_can + 'る'],
                    'k-obj-act-can-do-a': [m_act_adj + obj_adj + act_can + 'る'],
                    'k-obj-act-can-do-long': [m_act_adj + act_can + 'ます'],
                    'k-obj-act-can-not-do': [m_act_adj + act_can + 'ない'],
                    'k-obj-act-can-not-do-long': [m_act_adj + act_can + 'ません'],
                    'k-obj-act-want': [m_act_adj + act_i + 'たい',
                                       m_act_adj + act_i + 'たい'],
                    'k-obj-act-want-a': [m_act_adj + obj_adj + act_i + 'たい'],
                    'k-obj-act-way': [m_act_adj + act_way, act_way_g],
                    'k-obj-act-do': [m_act_adj + act_base],
                    'k-obj-act-do-a': [m_act_adj + obj_adj + act_base],
                    'k-obj-act-easy': [m_act_adj + act_i + 'やすい']}
        for a_key in add_keys:
            keys[a_key].extend(add_keys[a_key])
        if 'を作って' in keywords['a_adj']:
            c_obj = keywords['a_adj'].replace('を作って', '')
            change_keys = {
                'k-obj': [c_obj],
                'k-obj-adj': [c_obj + 'の'],
                'k-obj-status': [c_obj],
                'k-obj-noun': [obj_adj + c_obj, c_obj],
                'k-obj-noun-l': [obj_adj + c_obj],
                'k-obj-noun-s': [c_obj],
                'k-obj-noun-j': [obj_adj + c_obj, c_obj],
                'k-obj-wife': ['<!--obj-married-->', '<!--obj-married-->' + c_obj],
                'k-a-adj-make': [c_obj + 'にして'],
            }
            for c_key in change_keys:
                keys[c_key] = change_keys[c_key]
    if no_sub_flag:
        add_keys = {'k-how-to': [m_act_adj + act_way_g,
                                 m_act_adj + act_way_g],
                    'k-how-to-adj': [m_act_adj + act_with_g + act_way_g],
                    'k-can': [act_can + 'る'],
                    'k-can-s': [act_can + 'ます'],
                    'k-do': [m_act_adj + act_base],
                    'k-do-a': [m_act_adj + act_with + act_base],
                    'k-easy': [m_act_adj + act_i + 'やすい'],
                    'k-want': [m_act_adj + act_i + 'たい'],
                    'k-find': [m_act_adj + act_target + 'を探す']}
        for a_key in add_keys:
            keys[a_key].extend(add_keys[a_key])
    if no_sub_flag and no_obj_flag:
        add_keys = {'k-how-to': [m_act_adj + obj + act_with_g + act_way_g,
                                 m_act_adj + obj_adj + obj + act_with_g + act_way_g],
                    'k-how-to-adj': [m_act_adj + obj_adj + obj + act_with_g + act_way_g],
                    'k-can': [obj + act_with + act_can + 'る'],
                    'k-can-s': [obj + act_with + act_can + 'ます'],
                    'k-do': [m_act_adj + obj + act_with + act_base],
                    'k-do-a': [m_act_adj + obj_adj + obj + act_with + act_base],
                    'k-easy': [m_act_adj + obj + act_with_d + act_i + 'やすい'],
                    'k-want': [m_act_adj + obj + act_with_d + act_i + 'たい'],
                    'k-find': [m_act_adj + obj + 'の' + act_target + 'を探す']}
        for a_key in add_keys:
            keys[a_key].extend(add_keys[a_key])
    if '作る' in keywords['act']:
        keys['k-want'].append(alt_sub + obj + 'の' + act_target + 'が欲しい')
        keys['k-obj-act-want'].append(obj + 'の' + act_target + 'が欲しい')
        keys['k-obj-act-want'].append(obj_adj + obj + 'の' + act_target + 'が欲しい')
        keys['k-obj-act-want'].append(obj + 'の' + act_target + 'を作りたい')
        keys['k-act-want'].append(act_target + 'が欲しい')
        keys['k-act-want'].append(act_target + 'を作りたい')
        keys['k-act-to-find'].append(act_target + '作り')
        keys['k-obj-act-to-find'].append(obj_as_target + '作り')
        keys['k-obj-act-can-not-do'].append(obj + act_with + act_can.replace('を', 'が') + 'ない')
        keys['k-act-can-not-do'].append(act_can.replace('を', 'が') + 'ない')
        if '女性' not in keywords['obj'] or '女子' not in keywords['obj'] or '女性' not in keywords['obj']:
            keys['k-how-to'].append(alt_sub + obj_k + act_way_g)
            keys['k-can'].append(alt_sub + obj_k + act_can + 'る')
            keys['k-can-s'].append(alt_sub + obj_k + act_can + 'ます')
            keys['k-do'].append(alt_sub + obj_k + act_base)
            keys['k-do-a'].append(alt_sub + obj_adj + obj_k + act_base)
            keys['k-find'].append(alt_sub + obj_k + act_noun + 'を探す')
            keys['k-obj-act-way'].append(obj_k + act_way)
            keys['k-obj-act-way'].append(obj_k + act_way_g)
            keys['k-obj-act-do'].append(obj_k + act_base)
            keys['k-obj-act-do-a'].append(obj_adj + obj_k + act_base)
            keys['k-obj-act-can-do'].append(obj_k + act_can + 'る')
            keys['k-obj-act-can-do-a'].append(obj_adj + obj_k + act_can + 'る')
            keys['k-obj-act-want'].append(obj_k + act_noun + 'が欲しい')
            keys['k-obj-act-want'].append(obj_adj + obj_k + act_noun + 'が欲しい')
            keys['k-obj-act-want'].append(obj_k + act_noun + 'を作りたい')
            keys['k-obj-act-want'].append(obj_adj + obj_k + act_noun + 'を作りたい')
            keys['k-obj-act-want'].append(obj_k + act_noun + 'が欲しい')
            keys['k-obj-act-want-a'].append(obj_adj + obj_k + act_noun + 'が欲しい')
            keys['k-obj-act-find'].append(obj_k + act_noun + 'を探す')
            keys['k-obj-act-find-a'].append(obj_adj + obj_k + act_noun + 'を探す')
            keys['k-obj-act-to-find'].append(obj_k + act_noun + '作り')
            keys['k-obj-act-to-find'].append(obj_k + act_noun + '探し')
            keys['k-obj-act-to-find-a'].append(obj_adj + obj_k + act_noun + '作り')
            keys['k-obj-act-to-find-a'].append(obj_adj + obj_k + act_noun + '探し')
            keys['k-obj-act-can-meet'].append(obj_k + act_noun + 'と出会える')
            keys['k-obj-act-can-meet-a'].append(obj_adj + obj_k + act_noun + 'と出会える')
            keys['k-obj-act-can-do-a'].append(obj_adj + obj_k + act_can + 'る')
            keys['k-obj-act-can-do-long'].append(obj_k + act_can + 'ます')
            keys['k-obj-act-can-do-long'].append(obj_adj + obj_k + act_can + 'ます')
            keys['k-obj-act-noun'].append(obj_k + act_noun)
            keys['k-obj-act-noun-a'].append(obj_adj + obj_k + act_noun)
    keys['hot-month'] = [keywords['hot_month']]
    keys['hot-season'] = [keywords['hot_season']]
    keys['hot-month-next'] = [keywords['hot_month_next']]
    return keys


def make_keywords_sample(keywords, a_adj_flag, no_obj_flag, no_sub_flag):
    r_str = ''
    keys = key_phrase_maker(keywords, a_adj_flag, no_obj_flag, no_sub_flag)
    for k in keys:
        r_str += '<!--{}-->  :  {}\n'.format(k, pprint.pformat(keys[k]))
        # print('<!--{}-->  :  {}'.format(k, keys[k]))
    # with open('key_sample.md', 'w', encoding='utf-8') as f:
    #     f.write(r_str)


def make_keywords_sample_dict(keywords, a_adj_flag, no_obj_flag, no_sub_flag):
    result_dict = {}
    new_dict = []
    keys = key_phrase_maker(keywords, a_adj_flag, no_obj_flag, no_sub_flag)
    anchor_dict = {y['before']: y['after'] for y in wd.noun_list}
    anchor_dict.update({'<!--obj-married-->': '人妻'})
    print(keys)
    for before_s in keys:
        if type(keys[before_s]) == str:
            result_dict[keys[before_s]] = ['<!--{}-->'.format(before_s)]
        else:
            for x in keys[before_s]:
                if x not in result_dict:
                    result_dict[x] = ['<!--{}-->'.format(before_s)]
                else:
                    result_dict[x].append('<!--{}-->'.format(before_s))
    for kw in result_dict:
        if '<!--' in kw:
            print(kw)
            anchor_l = re.findall(r'<!--.+?-->', kw)
            if anchor_l:
                if len(anchor_l) == 1:
                    anchor = anchor_l[0]
                    for word in anchor_dict[anchor]:
                        new_dict.append([kw.replace(anchor, word), result_dict[kw]])
        else:
            new_dict.append([kw, result_dict[kw]])
    new_dict.sort(key=lambda y: len(y[0]), reverse=True)
    # print(new_dict)
    return new_dict


def make_new_section(section_dict_p, noun_dict, conj_dict, site1, site2, link_dict, this_path, recipe_flag,
                     subject_sex, main_key, part_code, project_dir, counter_d):
    recipe = {}
    str_list = []
    used_conj = []
    v_word = []
    section_dict = copy.deepcopy(section_dict_p)
    # print(section_dict)
    if section_dict['info']['shuffle']:
        for i in range(len(section_dict['info']['shuffle'])):
            shuffle_nums = section_dict['info']['shuffle'][i]
            random.shuffle(shuffle_nums)
            # print(shuffle_nums)
            for s_i, s_num in enumerate(shuffle_nums):
                section_dict[section_dict_p['info']['shuffle'][i][s_i]] = section_dict_p[s_num]
            # print(section_dict)
    if '<!--vrt-' in section_dict[0][0]:
        v_code = re.findall(r'<!--vrt-(.+?)-->', section_dict[0][0])[0]
        v_word = ['<!--vrt-{}-->'.format(v_code), random.choice(words_dict.vrt_list[v_code])]
    for sen_num in range(len(section_dict) - 1):
        if section_dict[sen_num] == 'space':
            str_list.append('')
            recipe[sen_num] = 0
        elif len(section_dict[sen_num]) == 1:
            str_list, used_conj, counter_d = insert_word_to_sentence(section_dict[sen_num][0], noun_dict, conj_dict,
                                                                     site1, site2,
                                                                     str_list, used_conj, v_word, link_dict, this_path,
                                                                     subject_sex, main_key, part_code, project_dir,
                                                                     counter_d)
            if recipe_flag:
                str_list[-1] = str_list[-1] + '<!--sw-{}-n{}-c{}-->'.format(section_dict['info']['sec_name'],
                                                                            str(sen_num), '0')
            recipe[sen_num] = 0
        else:
            choice_str = random.choice(section_dict[sen_num])
            str_list, used_conj, counter_d = insert_word_to_sentence(choice_str, noun_dict, conj_dict, site1, site2,
                                                                     str_list, used_conj, v_word, link_dict, this_path,
                                                                     subject_sex, main_key, part_code, project_dir,
                                                                     counter_d)
            recipe[sen_num] = section_dict[sen_num].index(choice_str)
            if recipe_flag:
                str_list[-1] = str_list[-1] + '<!--sw-{}-n{}-c{}-->'.format(section_dict['info']['sec_name'],
                                                                            str(sen_num),
                                                                            section_dict[sen_num].index(choice_str))
    section_str = '\n'.join(str_list)
    if not recipe_flag:
        section_str = section_str + '\n<!--rs-{}-->'.format(section_dict['info']['sec_name'])
    return section_str, recipe, counter_d


def make_new_title(section_list, noun_dict, conj_dict, site1, site2, obj_list, link_dict, subject_sex, recipe_flag,
                   main_key, part_code, project_dir, counter_d):
    str_list = []
    used_conj = []
    choice_str = random.choice(section_list)
    section_str, used_conj, counter_d = insert_word_to_sentence(choice_str, noun_dict, conj_dict, site1, site2,
                                                                str_list,
                                                                used_conj, [], obj_list, link_dict, subject_sex,
                                                                main_key,
                                                                part_code, project_dir, counter_d)
    recipe = {0: section_list.index(choice_str)}
    if recipe_flag:
        section_str[0] = section_str[0] + '<!--sw-c{}-->'.format(section_list.index(choice_str))
    return section_str[0], recipe, counter_d


def link_area_insert(sentence_str, project_dir):
    used_list = []
    if project_dir == 'sfd':
        pf_d = words_dict.area_link_list
        id_list = list(pf_d.keys())
        while '<!--link-area-->' in sentence_str:
            p_id = random.choice(id_list)
            if p_id in used_list:
                while p_id in used_list:
                    p_id = random.choice(id_list)
                used_list.append(p_id)
            sentence_str = sentence_str.replace('<!--link-area-->',
                                                '[{}](../area-bbs/{}-{})'.format(pf_d[p_id]['ari'],
                                                                                 p_id, pf_d[p_id]['alpha']))
    else:
        choice_list = random.choice([words_dict.pref_list, words_dict.city_list])
        while '<!--link-area-->' in sentence_str:
            select_str = random.choice(choice_list)
            if select_str in used_list:
                while select_str in used_list:
                    select_str = random.choice(choice_list)
                used_list.append(select_str)
            sentence_str = sentence_str.replace('<!--link-area-->', select_str, 1)
    return sentence_str


def link_obj_word_insert(sentence_str, link_dict, this_path, subject_sex):
    used_list = []
    type_str_l = re.findall(r'<!--link-word-(.+?)-->', sentence_str)
    if subject_sex == 'man':
        s_str = 'm'
    else:
        s_str = 'w'
    for type_str in type_str_l:
        # print(link_dict)
        type_str_s = type_str + '_' + s_str
        if type_str == 'obj' and not link_dict[type_str_s] and link_dict['adj_act']:
            target_list = link_dict['adj_act']
        elif type_str == 'act':
            target_list = link_dict['adj_act']
        else:
            target_list = link_dict[type_str_s]
        select_str = random.choice(target_list)
        if select_str[1] in used_list or select_str[1] == this_path:
            while select_str[1] in used_list or select_str[1] == this_path:
                select_str = random.choice(link_dict[type_str_s])
            used_list.append(select_str[1])
        if select_str[1]:
            sentence_str = sentence_str.replace('<!--link-word-{}-->'.format(type_str),
                                                '[{}]({}.md)'.format(select_str[0], select_str[1]), 1)
        else:
            sentence_str = sentence_str.replace('<!--link-word-{}-->'.format(type_str), select_str[0], 1)
    return sentence_str


def same_line_words_filter(sentence_str):
    sl_str_l = re.findall(r'<!--sl-s-->.+?<!--sl-s/e-->', sentence_str)
    for sl_str in sl_str_l:
        inner_str = re.sub(r'<!--sl-s-->(.+?)<!--sl-s/e-->', r'\1', sl_str)
        str_list = inner_str.split(',')
        random.shuffle(str_list)
        insert_s = ''
        for i, s_str in enumerate(str_list):
            if i == 0:
                insert_s += s_str
            elif i == 1:
                insert_s += 'や' + s_str
            elif i > 1:
                insert_s += '、' + s_str
        sentence_str = sentence_str.replace(sl_str, insert_s)
    sla_str_l = re.findall(r'<!--sl-a-->.+?<!--sl-a/e-->', sentence_str)
    for sla_str in sla_str_l:
        inner_str = re.sub(r'<!--sl-a-->(.+?)<!--sl-a/e-->', r'\1', sla_str)
        str_list = inner_str.split(',')
        random.shuffle(str_list)
        insert_a = 'と'.join(str_list)
        sentence_str = sentence_str.replace(sla_str, insert_a)
    return sentence_str


def insert_word_to_sentence(sentence_str, noun_dict, conj_dict, site1, site2, str_list, used_conj, v_word, link_dict,
                            this_path, subject_sex, main_key, part_code, project_dir, counter_d):
    aff_name_dict = {'ワクワクメール': 'ワクワク', 'PCMAX': 'ピシマ', 'ハッピーメール': 'ハピメ', 'Jメール': 'Jメール'}
    if v_word:
        sentence_str = sentence_str.replace(v_word[0], v_word[1])
    conj_blank = re.findall(r'<!--c-.+?-->', sentence_str)
    if conj_blank:
        for c_blank in conj_blank:
            next_c = random.choice(conj_dict[c_blank])
            try_count = 0
            while next_c in c_blank or try_count < 5:
                next_c = random.choice(conj_dict[c_blank])
                try_count += 1
            sentence_str = sentence_str.replace(c_blank, next_c + '、', 1)
            used_conj.append(next_c)
    sentence_str = sentence_str.replace('<!--site-1-->', site1)
    sentence_str = sentence_str.replace('<!--site-2-->', site2)
    if '<!--del-' in sentence_str:
        sentence_str = re.sub(r'<!--del-' + main_key + r'-->.+?<!--del/e-->', '', sentence_str)
        sentence_str = re.sub(r'<!--del-' + part_code + r'-->.+?<!--del/e-->', '', sentence_str)
        sentence_str = re.sub(r'<!--del-' + main_key + '_' + part_code + r'-->.+?<!--del/e-->', '', sentence_str)
        sentence_str = re.sub(r'<!--del-.*?-->', '', sentence_str)
        sentence_str = sentence_str.replace('<!--del/e-->', '')
    if '<!--link-word-' in sentence_str:
        sentence_str = link_obj_word_insert(sentence_str, link_dict, this_path, subject_sex)
    if '<!--link-area-->' in sentence_str:
        sentence_str = link_area_insert(sentence_str, project_dir)
    sentence_str = sentence_str.replace('<!--sefre-page-->', '')
    sentence_str = same_line_words_filter(sentence_str)
    while '<!--' in sentence_str:
        blank_list = re.findall(r'<!--.+?-->', sentence_str)
        # print(noun_dict)
        # print(sentence_str)
        if blank_list:
            for blank in blank_list:
                print(blank)
                if blank in noun_dict:
                    if len(noun_dict[blank]) <= 1:
                        sentence_str = sentence_str.replace(blank, random.choice(noun_dict[blank][0]), 1)
                    else:
                        sentence_str = sentence_str.replace(blank, np.random.choice(noun_dict[blank][0],
                                                                                    p=noun_dict[blank][1]), 1)
                if '<!--this-aff-site-->' in sentence_str:
                    for s_name in aff_name_dict:
                        if s_name in sentence_str:
                            sentence_str = sentence_str.replace('<!--this-aff-site-->', aff_name_dict[s_name])
                if blank in counter_d:
                    counter_d[blank] += 1
                else:
                    counter_d[blank] = 1
    for bad_w in words_dict.correct_dict:
        if bad_w in sentence_str:
            sentence_str = sentence_str.replace(bad_w, words_dict.correct_dict[bad_w])
    if '。' in sentence_str:
        sentence_str = re.sub(r'。(.+)$', r'。\n\1', sentence_str)
    sentence_str = a_adj_filter(sentence_str)
    str_list.append(sentence_str)
    return str_list, used_conj, counter_d


def a_adj_filter(sentence_str):
    a_adj_list = ['婚活で', 'コロナ禍に']
    for adj_str in a_adj_list:
        if sentence_str.count(adj_str) > 1:
            split_list = sentence_str.split(adj_str)
            if len(split_list) > 1:
                split_list.insert(1, adj_str)
            else:
                split_list.insert(0, adj_str)
            sentence_str = ''.join(split_list)
            # print('k_join : {}'.format(sentence_str))
    return sentence_str


def sf_import_to_source(import_list):
    main_str = ''
    list_name = ['title', 'des', 'int_1', 'point', 'di_1_1', 'di_1_2', 'da_1', 'da_2', 'da_3', 'da_4', 'da_5', 'da_6',
                 'da_7', 'da_8', 'da_9', 'da_10', 'da_11', 'da_12', 'tips_8', 'pa_1', 'pa_2', 'pa_3', 'pa_4', 'pa_5',
                 'pa_6', 'use_1', 'use_2', 'use_3', 'use_4', 'use_5', 'use_6', 'use_7', 'tips_1', 'tips_2', 'tips_3',
                 'tips_4', 'tips_5', 'tips_6', 'tips_7', 'cnc_1']
    for o_list, l_name in zip(import_list, list_name):
        new_dict = {'info': {'deny': [], 'only': [], 'shuffle': []}}
        index_num = 0
        # print(o_list)
        for row in o_list:
            new_dict[index_num] = row
            index_num += 1
        main_str += '{} = {}\n# {}/end\n\n'.format(l_name, pprint.pformat(new_dict), l_name)
    # print(main_str)
    main_str.split('\n')
    with open('list_test.py', 'w', encoding='utf-8') as f:
        f.write(main_str)


def make_used_id_list_for_key_data(project_name):
    used_id = {'obj_m': list(range(0, 209, 1)), 'obj_w': list(range(0, 116, 1)), 'sub_m': [], 'sub_w': [], 'act': []}
    with open(project_name + '/pickle_pot/used_id.pkl', 'wb') as k:
        pickle.dump(used_id, k)
    with open(project_name + '/pickle_pot/used_id.pkl', 'rb') as p:
        pkl_data = pickle.load(p)
    print(pkl_data)


def auto_make_md_for_all_key(project_dir, dir_name, main_key, recipe_flag, start_id, insert_pub_date):
    # html_str -> keyword : {},  性別 : {s},  main_key : {m}    for ex  '{}_{s}_{m}
    key_data_dict = {'obj_m': {'data': key_data.key_obj_woman.keyword_dict, 'sex': 'man', 'part': 'obj'},
                     'obj_w': {'data': key_data.key_obj_man.keyword_dict, 'sex': 'woman', 'part': 'obj'}}
    if project_dir in ['reibun']:
        if not os.path.exists(project_dir + '/md_files/pc/' + dir_name):
            os.mkdir(project_dir + '/md_files/pc/' + dir_name)
    else:
        if not os.path.exists(project_dir + '/md_files/' + dir_name):
            os.mkdir(project_dir + '/md_files/' + dir_name)
    for d_id in key_data_dict:
        part_code_str = re.sub(r'_.+^', '', d_id)
        make_new_pages_to_md_from_key_list(project_dir, dir_name, source_data, main_key, [],
                                           key_data_dict[d_id]['data'], recipe_flag=recipe_flag,
                                           subject_sex=key_data_dict[d_id]['sex'], start_id=start_id,
                                           insert_pub_date=insert_pub_date, part_code=part_code_str, copy_pub_flag=False)


def make_mix_act_key_list(key_data_a, key_data_b):
    if len(key_data_a) >= len(key_data_b):
        key_data1 = key_data_a
        key_data2 = key_data_b
        ud_flag = ['key_a', 'key_b']
    else:
        key_data1 = key_data_b
        key_data2 = key_data_a
        ud_flag = ['key_b', 'key_a']
    result_list = {}
    used_list = []
    i = 0
    for id1 in key_data1:
        if i < len(key_data2):
            pass
        else:
            i = 0
        result_list[id1] = key_data1[id1] | key_data2[i] | {'type': 'mix_act',
                                                            'all_key': key_data1[id1]['act'] + key_data2[i]['a_adj']}
        used_list.append(['{}_{}'.format(ud_flag[0], id1), '{}_{}'.format(ud_flag[1], i)])
        i += 1
    # print(result_list)
    # print(used_list)
    return result_list


def search_max_id(project_dir):
    num_list = []
    md_files = glob.glob(project_dir + '/md_files/**/**.md')
    md_files = [x for x in md_files if '_copy' not in x]
    for file_path in md_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            md_str = f.read()
            id_str_l = re.findall(r'\nn::(\d*)\n', md_str)
            if id_str_l:
                num_list.append([int(id_str_l[0]), file_path])
    num_list.sort(key=lambda x: x[0])
    # print(num_list)
    max_num = num_list[-1][0]
    print(max_num)
    no_use_list = [x for x in range(max_num + 1) if x not in [y[0] for y in num_list]]
    print(no_use_list)
    with open(num_list[-1][1], 'r', encoding='utf-8') as g:
        l_str = g.read()
        last_pub_l = re.findall(r'p::(.*?)\n', l_str)
        if last_pub_l:
            last_pub = last_pub_l[0]
        else:
            last_pub = ''
    return max_num, last_pub


def make_md_by_project_and_part(project_dir, part_cord, subject_sex):
    part_dict = {'obj': {'man': 'obj_m', 'woman': 'obj_w'},
                 'sub': {'man': 'sub_m', 'woman': 'sub_w'},
                 'adj_act': {'man': 'adj_act', 'woman': 'adj_act'},
                 'act': {'man': 'act', 'woman': 'act'}}
    md_dir_dict = {'goodbyedt': {'obj': 'object', 'sub': 'subject', 'act': 'action', }}
    md_dir = md_dir_dict[project_dir][part_cord]
    p_code = part_dict[part_cord][subject_sex]
    key_source = key_source_dict[p_code]
    main_key_dict = {'goodbyedt': 'dt'}
    max_id, last_pub = search_max_id(project_dir)
    next_id = max_id + 1
    if last_pub:
        if 'T' not in last_pub:
            last_pub = last_pub + 'T16:33:19'
        last_pub = last_pub.replace('/', '-')
    make_new_pages_to_md_from_key_list(project_dir, md_dir, source_data, main_key_dict[project_dir],
                                       [], key_source, recipe_flag=True, subject_sex=subject_sex, start_id=next_id,
                                       insert_pub_date=last_pub, part_code=part_cord, copy_pub_flag=True)


if __name__ == '__main__':
    make_md_by_project_and_part('goodbyedt', 'act', 'man')

    # test_new_section(source_data.all_list, keywords_p)
    # sf_import_to_source()

    # make_keywords_sample(keywords_p)

    # make_used_key_data('sfd')

    # t_key_list = key_data.key_obj_woman.keyword_dict
    # make_new_pages_to_md_from_key_list('online_marriage', 'online_love', 'love_{s}_{}', source_data, 'olm',
    #                                    list(range(0, 321, 1)), t_key_list, recipe_flag=True, subject_sex='man')

    # t_key_list = key_data.key_obj_woman.keyword_dict
    # make_new_pages_to_md_from_key_list('koibito', 'lover', '{}_love_{s}', source_data, 'dt',
    #                                    [], t_key_list, recipe_flag=True, subject_sex='man', start_id=23,
    #                                    insert_pub_date='2021-06-12T14:33:19')

    # t_key_list = make_mix_act_key_list(key_data.key_adj_act.act_dict, key_data.key_adj_act.adj_dict)

    # t_key_list = key_data.key_adj_act.key_dict
    # make_new_pages_to_md_from_key_list('sfd', 'sf_a', source_data, 'sf', [], t_key_list, recipe_flag=True,
    #                                    subject_sex='man', start_id=210, insert_pub_date='2021-08-27T14:33:19',
    #                                    part_code='act')

    # t_key_list = key_data.key_obj_woman.keyword_dict
    # make_new_pages_to_md_from_key_list('goodbyedt', 'action', source_data, 'dt', [], t_key_list, recipe_flag=True,
    #                                    subject_sex='man', start_id=359, insert_pub_date='2021-09-04T12:33:19',
    #                                    part_code='act', copy_pub_flag=True)

    # t_key_list = key_data.key_sub_man.keyword_dict
    # make_new_pages_to_md_from_key_list('sfd', 'sf_s', source_data, 'sf', [], t_key_list, recipe_flag=True,
    #                                    subject_sex='man', start_id=466, insert_pub_date='2021-09-02T14:33:19',
    #                                    part_code='sub')

    # search_max_id('goodbyedt')

    # auto_make_md_for_all_key('koibito', 'lover', '{}_love_{s}', 'koi', recipe_flag=True, start_id=23,
    #                          insert_pub_date='2021-04-08T18:22:12')
    # insert_pub_date の書式　'%Y-%m-%dT%H:%M:%S'

    # make_used_id_list_for_key_data('sfd')

    # todo: 関連記事の追加で相互リンク強化

    # todo: act_adj を複数で 無料で、サークルで、既婚者同士で　等 アダルト
    # todo: 会話の話題やobj,subリンク、趣味などのワードリストで多様性

    # todo: subの複数パターン　無職男性が、など
    # todo: 出会い系サイトを他に変更　婚活サイト、SNS、ツイッター
    # todo: 地域の婚活, パパ活、　割り切り, 不倫, 出会う, マッチングアプリで出会う、趣味の出会い
    # todo: 時期ネタの書き換え
    # todo: その対象の探し方、o_catで切り替えるなどして多様化
    # todo: 検索数が増えてきた記事をピンポイントで最新フォームで書き換えできる関数
    # todo: md変更箇所を<!--ori-->で管理
    # todo: 高齢者向けの記事とキーワード

    # pprint.pprint(obj_source_changer(), width=150)

    # k_p = {
    #     's_adj': '普通の', 'sub': '男性',
    #     'o_adj': '淫乱な', 'obj': '巨乳女性', 'obj_key': '巨乳', 'obj_p': 'の',
    #     'act_adj': '安全に', 'act': 'セフレを作る', 'act_noun': 'セフレ', 'act_noun_flag': True,
    #     'act_connection': ['セフレ関係'],
    #     'o_reason': '',
    #     't_sex': 'm', 't_age': 'n', 't_cat': 'j', 'act_code': 'gf'}
    # pprint.pprint(make_keywords_sample_dict(k_p))
