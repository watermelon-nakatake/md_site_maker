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
import key_data.key_act
import insert_relational_list

key_source_dict = {'obj_m': key_data.key_obj_woman.keyword_dict, 'obj_w': key_data.key_obj_man.keyword_dict,
                   'adj_act': key_data.key_adj_act.key_dict, 'act': key_data.key_act.act_dict,
                   'sub_m': key_data.key_sub_man.key_dict}
no_adult_prj = ['mh', 'olm', 'women', 'bf', 'koi', 'test']
no_adult_dir = ['konkatsu', 'online_marriage', 'women', 'koibito', 'test']
opposite_sex = {'man': 'w', 'woman': 'm'}
mass_dir_list = ['sefure_matching', 'matching_bbs', 'secret_matching', 'cheating_love', 'my_matching',
                 'senior_matching', 'good_marriage', 'online_pen_pal', 'after_covid_love', 'marriage_hunt']
html_str_dict = {
    'sfd': {'obj_m': 'sf_{}_f', 'obj_w': 'sf_{}_m', 'sub_m': 'sf_s_{}_m', 'sub_w': 'sf_s_{}_f',
            'act': 'sf_a_{}', 'adj_act': 'sf_a_{}'},
    'bf': {'obj_m': 'gf_{}', 'obj_w': 'gf_{}', 'sub_m': 'sf_s_{}_m', 'sub_w': 'sf_s_{}_f',
           'act': 'ac_{}', 'adj_act': 'ac_{}'},
    'sex': {'obj_m': 'sex_{}', 'obj_w': 'sex_{}', 'sub_m': 'sex_{}_m', 'sub_w': 'sex_{}_f',
            'act': 'sex_a_{}', 'adj_act': 'sex_a_{}'},
    'shoshin': {'obj_m': '{}_by_beginner_m', 'obj_w': '{}_by_beginner_w', 'sub_m': '{}_by_beginner_s',
                'sub_w': '{}_by_beginner_s', 'act': '{}_by_beginner_a', 'adj_act': '{}_by_beginner_a'},
    'test': {'obj_m': '{}_by_beginner_m', 'obj_w': '{}_by_beginner_w', 'sub_m': '{}_by_beginner_s',
             'sub_w': '{}_by_beginner_s', 'act': '{}_by_beginner_a', 'adj_act': '{}_by_beginner_d'},
    'goodbyedt': {'obj_m': '{}_dt', 'obj_w': '', 'sub_m': '{}_s_dt', 'sub_w': '',
                  'act': '{}_a_dt', 'adj_act': '{}_a_dt'},
    'howto': {'obj_m': '{}_m_cov', 'obj_w': '{}_w_cov'},
    'htaiken': {'obj_m': 'm_ht_{}', 'obj_w': 'w_ht_{}'},
    'joshideai': {'obj_m': 'sex_{}', 'adj_act': 'sex_a_{}'},
    'koibito': {'obj_m': '{}_love_m', 'obj_w': '{}_love_w'},
    'konkatsu': {'obj_m': 'mh_{}_m', 'obj_w': 'mh_{}_f'},
    'online_marriage': {'obj_m': 'love_m_{}', 'obj_w': 'love_w_{}'},
    'rei_site': {'obj_m': 'gf_{}', 'adj_act': 'ac_{}'},
    'women': {'obj_w': '{}_bf'},
    'mass': {'obj_m': '{}_m', 'obj_w': '{}_w', 'sub_m': '{}_s', 'sub_w': '{}_s', 'act': '{}_a', 'adj_act': '{}_d'}
}  # for multiple

dir_dict = {'sfd': {'obj_m': 'obj_m', 'obj_w': 'obj_w', 'sub_m': 'sub_m', 'sub_w': 'sub_w', 'act': 'act',
                    'adj_act': 'adj_act'},
            'goodbyedt': {'obj_m': 'object', 'act': 'action'},  # 'sub_m': 'subject',
            'howto': {'obj_m': 'online_love', 'obj_w': 'online_love'},
            'htaiken': {'obj_m': 'how_to_sex', 'obj_w': 'how_to_sex'},
            'shoshin': {'act': 'beginner'},  # 'obj_m': 'object', 'sub_m': 'subject',
            'joshideai': {'obj_m': 'make_love', 'adj_act': 'website'},
            'koibito': {'obj_m': 'lover', 'obj_w': 'lover'},
            'konkatsu': {'obj_m': 'partner', 'obj_w': 'partner'},
            'online_marriage': {'obj_m': 'online_love', 'obj_w': 'online_love'},
            'test': {'obj_m': 'o_test_m', 'sub_m': 's_test', 'act': 'a_test', 'adj_act': 'adj_test'},
            'rei_site': {'obj_m': 'girl_friend', 'adj_act': 'site'},
            'women': {'obj_w': 'boyfriend'},
            'mass': {'obj_m': 'tec', 'obj_w': 'tec', 'sub_m': 'tec', 'sub_w': 'tec', 'act': 'tec', 'adj_act': 'tec'}
            }  # for multiple
relational_list_len = 15


def make_new_pages_to_md_from_key_list(project_dir, dir_name, source_mod, main_key, use_id_list, key_list,
                                       recipe_flag, subject_sex, start_id, insert_pub_date, part_code,
                                       copy_pub_flag, exist_update_flag):
    # 必要最低限のキーワードリストで機動的に記事作成
    # 個別記事のリストの中にメインワードのキーワード ex.gf で選択
    # 既存記事のキーワードとurlをランダム選択scrに渡す
    now = datetime.datetime.now()
    # print(now)
    html_str = choice_html_str(subject_sex, project_dir, part_code)
    if os.path.exists(project_dir + '/pickle_pot/recipe_dict.pkl'):
        with open(project_dir + '/pickle_pot/recipe_dict.pkl', 'rb') as rf:
            recipe_dict = pickle.load(rf)
    else:
        recipe_dict = {}
    if os.path.exists(project_dir + '/pickle_pot/key_dict.pkl'):
        with open(project_dir + '/pickle_pot/key_dict.pkl', 'rb') as rk:
            key_dict = pickle.load(rk)
    else:
        key_dict = {}
    counter_d = {}
    if not use_id_list:
        use_id_list = list(key_list.keys())
    use_id_list = id_filter(use_id_list, main_key, key_list, part_code)
    this_key_code = check_key_code(key_list)
    used_dict, add_id_dict = make_used_key_dict(project_dir, use_id_list, this_key_code, start_id)
    if insert_pub_date:
        dt1 = datetime.datetime.strptime(insert_pub_date, '%Y-%m-%dT%H:%M:%S')
        start_dt = dt1
        print('insert_pub : {}'.format(insert_pub_date))
    else:
        dt1 = ''
        start_dt = now
    print('dt1 : {}'.format(dt1))
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
    print('used_dict : {}'.format(used_dict_l))
    link_dict = make_key_and_path_list(html_str, used_dict_l, project_dir)
    # print('link_dict : {}'.format(link_dict))
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
                         'bg': {'a_adj_flag': False, 'act_code': 'bg', 'replace_words': [],
                                'sub_key': '初心者', 'sub': '出会い系初心者', 's_sex': 'm', 's_ms': 's', 's_adj': '普通の'},
                         'dt': {'a_adj_flag': True, 'act_code': 'dt', 'replace_words': [],
                                'sub_key': '童貞', 'sub': '童貞男性', 's_sex': 'm', 's_ms': 's', 's_adj': '真面目な'}
                     },
                     'adj_act': {
                         'sex': {'a_adj_flag': True, 'act_code': 'sex', 'replace_words': []},
                         'gf': {'a_adj_flag': True, 'act_code': 'gf', 'replace_words': []},
                         'sf': {'a_adj_flag': True, 'act_code': 'sf', 'replace_words': []}
                     },
                     'sub': {
                         'sf': {'act': 'セフレを作る', 'act_noun': 'セフレ', 'act_noun_flag': True, 'a_adj_flag': False,
                                '2act_w': 'セックスしたい', '2act_noun': 'セックス', '2act_do': 'セックスする',
                                'act_connection': ['セフレ関係', '肉体関係'], 'act_code': 'sf', 'replace_words': [],
                                'act_target': 'セフレ', 's_adj': ''}
                     }
                     # act と　a_adj の切り替え
                     }
    hot_info = {'hot_month': '11月', 'hot_season': '秋', 'hot_month_next': '12月'}
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
        old_md = '{}/md_files/{}/{}.md'.format(project_dir, dir_name, keywords['page_name'])
        old_pub = ''
        if os.path.exists(old_md):
            if not exist_update_flag:
                continue
            with open(old_md, 'r', encoding='utf-8') as m:
                md_str = m.read()
            if '<!--ori-->' in md_str:
                print('original sentence in : ' + old_md)
                keywords['ori_flag'] = True
                continue
            old_pub_l = re.findall(r'p::(.+?)\n', md_str)
            if old_pub_l:
                old_pub = old_pub_l[0]
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
        if project_dir in no_adult_dir:
            keywords['o_adj'] = np.random.choice(['魅力的な', '素敵な', '理想的な'])
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
        # print('no_obj_flag : {}'.format(no_obj_flag))
        # print('no_sub_flag : {}'.format(no_sub_flag))
        # print('a_adj_flag : {}'.format(a_adj_flag))
        if keywords['obj_p'] == 'no' or keywords['obj_p'] == 'n':
            keywords['obj_p'] = ''
        if 'a_adj' not in keywords:
            if main_key == 'sex' and keywords['o_ms'] == 'm':
                keywords['a_adj'] = np.random.choice(['不倫', '浮気', 'NTR'])
            else:
                keywords['a_adj'] = np.random.choice(['安全に', '確実に', '簡単に', 'すぐに'])
        if adult_checker_by_keywords(keywords):
            link_dict_u = ad_link_dict
        else:
            link_dict_u = link_dict
        if 'o_reason' not in keywords:
            keywords['o_reason'] = '素敵な出会いが欲しいから'
        keywords.update(hot_info)
        # print(keywords)
        # make_keywords_sample(keywords, a_adj_flag, no_obj_flag, no_sub_flag)
        if copy_pub_flag and old_pub:
            dt_str = old_pub
        else:
            if dt1:
                if dt1 < now:
                    dt1 = dt1 + datetime.timedelta(hours=int(random.random() * 12), minutes=int(random.random() * 60),
                                                   seconds=int(random.random() * 59))
                else:
                    dt1 = start_dt
                dt_str = dt1.strftime('%Y-%m-%dT%H:%M:%S')
            else:
                dt_str = now.strftime('%Y-%m-%dT%H:%M:%S')
        recipe_list, counter_d, title_str = make_new_page(keywords, source_mod, art_map, project_dir, dir_name,
                                                          link_dict_u, main_key, recipe_flag, subject_sex, a_adj_flag,
                                                          add_id_dict[key_id], dt_str, part_code, no_obj_flag,
                                                          no_sub_flag, counter_d)
        keywords['title_str'] = title_str
        keywords['dir_name'] = dir_name
        keywords['sub_sex'] = subject_sex
        keywords['page_id'] = add_id_dict[key_id]
        recipe_dict[dir_name + '/' + keywords['page_name']] = recipe_list
        key_dict[dir_name + '/' + keywords['page_name']] = keywords
    if dt_str:
        print('last pub_date :  {}'.format(dt_str))
    # print(recipe_dict)
    # print(key_dict)
    with open(project_dir + '/pickle_pot/recipe_dict.pkl', 'wb') as rp:
        pickle.dump(recipe_dict, rp)
    with open(project_dir + '/pickle_pot/key_dict.pkl', 'wb') as wk:
        pickle.dump(key_dict, wk)
    if project_dir != 'sfd':
        insert_relation_page_list_to_md(project_dir, key_dict)
    # print(counter_d)
    # sort_counter_dict(counter_d)


def make_new_pages_to_md_for_mass(pd, site_data, subject_sex, start_id, insert_pub_date):
    # print(pd)
    project_dir = pd['project_dir']
    dir_name = [x for x in pd['category_data']][0]
    now = datetime.datetime.now()
    # print(now)
    html_str = site_data['f_name']
    p_dir_path = 'mass_production/' + project_dir
    if os.path.exists(p_dir_path + 'mass_production/used_comb.pkl'):
        with open('mass_production/used_comb.pkl', 'rb') as rc:
            used_comb = pickle.load(rc)
    else:
        used_comb = []
    if os.path.exists(p_dir_path + '/pickle_pot/recipe_dict.pkl'):
        with open(p_dir_path + '/pickle_pot/recipe_dict.pkl', 'rb') as rf:
            recipe_dict = pickle.load(rf)
    else:
        recipe_dict = {}
    if os.path.exists(p_dir_path + '/pickle_pot/key_dict.pkl'):
        with open(p_dir_path + '/pickle_pot/key_dict.pkl', 'rb') as rk:
            key_dict = pickle.load(rk)
    else:
        key_dict = {}
    counter_d = {}
    key_base = {x: site_data[x] for x in site_data if x not in ['title', 'domain', 'dir', 'f_name', 'no_adult_flag']}
    print(key_base)
    if insert_pub_date:
        dt1 = datetime.datetime.strptime(insert_pub_date, '%Y-%m-%dT%H:%M:%S')
        start_dt = dt1
        print('insert_pub : {}'.format(insert_pub_date))
    else:
        dt1 = ''
        start_dt = now
    print('dt1 : {}'.format(dt1))
    art_num = random.choice(list(range(40, 100)))
    print(art_num)
    key_list = []
    used_key1 = []
    used_key2 = []
    for i in range(art_num):
        new_key = {}
        ak_list = []
        eng_list = []
        type_list = []
        part_counter = 1
        key1 = ''
        for part in key_base:
            if key_base[part] == 'r':
                if part in ['obj', 'sub']:
                    part_c = part + '_m'
                elif part == 'adj':
                    part_c = 'adj_act'
                else:
                    part_c = part
                choice_id = random.choice([x for x in key_source_dict[part_c]])
                if part_counter == 1:
                    if choice_id in used_key1:
                        if len(key_source_dict[part_c]) <= len(used_key1):
                            used_key1 = []
                        while choice_id in used_key1:
                            choice_id = random.choice([x for x in key_source_dict[part_c]])
                    key1 = part_c + '_' + str(choice_id)
                    used_key1.append(choice_id)
                else:
                    if choice_id in used_key2 or [key1, part_c + '_' + str(choice_id)] in used_comb:
                        if len(key_source_dict[part_c]) <= len(used_key2):
                            used_key2 = []
                        while choice_id in used_key2 or [key1, part_c + '_' + str(choice_id)] in used_comb:
                            choice_id = random.choice([x for x in key_source_dict[part_c]])
                    used_comb.append([key1, part_c + '_' + str(choice_id)])
                    used_key2.append(choice_id)
                this_key = key_source_dict[part_c][choice_id]
                new_key.update(this_key)
                ak_list.append(this_key['all_key'])
                eng_list.append(this_key['eng'])
                type_list.append(part)
                part_counter += 1
            else:
                new_key[part] = key_base[part]
            new_key['eng'] = '_and_'.join(eng_list)
            new_key['all_key'] = ' '.join(ak_list)
            new_key['type'] = '+'.join(type_list)
        key_list.append(new_key)
        # print(new_key)
        # print('\n')
    # print(key_list)
    # return
    dt_str = ''
    if not os.path.exists(p_dir_path + '/md_files/' + dir_name):
        os.mkdir(p_dir_path + '/md_files/' + dir_name)
    link_dict = make_key_and_path_list_for_mass(html_str, key_list)
    # print(link_dict)
    for i, key_i in enumerate(key_list):
        this_id = start_id + i
        base_key = {'act': 'セックスする', 'act_noun': 'セックス相手',
                    '2act_w': 'セックスしたい', '2act_noun': 'セックス', '2act_do': 'セックスする',
                    'act_connection': ['肉体関係'], 'act_target': 'セフレ',
                    'sub_key': '初心者', 'sub': '出会い系初心者', 's_sex': 'm', 's_ms': 's', 's_adj': '普通の',
                    'o_cat': '', 'o_sex': 'w', 'o_adj': '', 'obj_key': '',
                    'act_noun_flag': False, 'a_adj_flag': False, 'act_code': 'sex', 'replace_words': [],
                    'hot_month': '11月', 'hot_season': '秋', 'hot_month_next': '12月'}
        keywords = base_key
        base_key.update(key_i)
        # print(keywords)
        # return
        keywords['id'] = str(this_id)
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
        if site_data['no_adult_flag']:
            keywords['o_adj'] = np.random.choice(['魅力的な', '素敵な', '理想的な'])
            keywords['no_adult_flag'] = True
        else:
            keywords['no_adult_flag'] = False
        if 'obj' not in keywords:
            no_obj_flag = True
            c_obj = np.random.choice(['女性', '女性', '女子'])
            if not site_data['no_adult_flag']:
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
        a_adj_flag = keywords['a_adj_flag']
        # print('no_obj_flag : {}'.format(no_obj_flag))
        # print('no_sub_flag : {}'.format(no_sub_flag))
        # print('a_adj_flag : {}'.format(a_adj_flag))
        if keywords['obj_p'] == 'no' or keywords['obj_p'] == 'n':
            keywords['obj_p'] = ''
        if 'a_adj' not in keywords:
            if 'o_ms' in keywords:
                if not site_data['no_adult_flag'] and keywords['o_ms'] == 'm':
                    keywords['a_adj'] = np.random.choice(['不倫', '浮気', 'NTR'])
                else:
                    keywords['a_adj'] = np.random.choice(['安全に', '確実に', '簡単に', 'すぐに'])
            else:
                keywords['a_adj'] = np.random.choice(['安全に', '確実に', '簡単に', 'すぐに'])
        if 'o_reason' not in keywords:
            keywords['o_reason'] = '素敵な出会いが欲しいから'
        # print(keywords)
        if dt1:
            if dt1 < now:
                dt1 = dt1 + datetime.timedelta(hours=int(random.random() * 12), minutes=int(random.random() * 60),
                                               seconds=int(random.random() * 59))
            else:
                dt1 = start_dt
            dt_str = dt1.strftime('%Y-%m-%dT%H:%M:%S')
        else:
            dt_str = now.strftime('%Y-%m-%dT%H:%M:%S')
        source_mod = source_data
        art_map = [[source_mod.introduction, 1], [source_mod.d_introduction, 'straight'],
                   [source_mod.d_advantage, [2, 3, 4]],
                   [source_mod.p_introduction, 'straight'], [source_mod.purpose_advantage, 3],
                   [source_mod.tips_bonus, [0, 1, 2]], [source_mod.process, 'straight'],
                   [source_mod.tips_bonus, [1, 2, 3]], [source_mod.conclusion, 1]]
        recipe_list, counter_d, title_str = make_new_page(keywords, source_mod, art_map, project_dir, dir_name,
                                                          link_dict, 'mass', True, subject_sex, a_adj_flag,
                                                          this_id, dt_str, site_data['part_code'], no_obj_flag,
                                                          no_sub_flag, counter_d)
        keywords['title_str'] = title_str
        keywords['dir_name'] = dir_name
        keywords['sub_sex'] = subject_sex
        keywords['page_id'] = this_id
        recipe_dict[dir_name + '/' + keywords['page_name']] = recipe_list
        key_dict[dir_name + '/' + keywords['page_name']] = keywords
    if dt_str:
        print('last pub_date :  {}'.format(dt_str))
    # print(recipe_dict)
    # print(key_dict)
    with open(p_dir_path + '/pickle_pot/recipe_dict.pkl', 'wb') as rp:
        pickle.dump(recipe_dict, rp)
    with open(p_dir_path + '/pickle_pot/key_dict.pkl', 'wb') as wk:
        pickle.dump(key_dict, wk)
    with open('mass_production/used_comb.pkl', 'wb') as wk:
        pickle.dump(key_dict, wk)
    insert_relation_page_list_to_md(project_dir, key_dict)


def make_md_from_exist_keywords(use_path_list):
    update_md = []
    recipe_flag = True
    source_mod = source_data
    if type(use_path_list) == list:
        project_dir = re.sub(r'/.*$', '', use_path_list[0])
    else:
        project_dir = re.sub(r'/.*$', '', use_path_list)
    print('project_dir : {}'.format(project_dir))
    with open(project_dir + '/pickle_pot/recipe_dict.pkl', 'rb') as rf:
        recipe_dict = pickle.load(rf)
    with open(project_dir + '/pickle_pot/key_dict.pkl', 'rb') as rk:
        key_dict = pickle.load(rk)
    counter_d = {}
    # print(key_dict)
    if type(use_path_list) == list:
        change_list = [re.sub(r'^.+/md_files/(.+).md', r'\1', x) for x in use_path_list]
    elif type(use_path_list) == str and use_path_list == project_dir:
        change_list = [x for x in key_dict if 'ori_flag' not in key_dict[x] or not key_dict[x]['ori_flag']]
    else:
        change_dir = re.sub(r'^.+/md_files/', '', use_path_list)
        change_list = [x for x in key_dict if change_dir in x]
    if project_dir in no_adult_dir:
        key_dict_l = keyword_dict_adult_filter(key_dict, 3)
        ad_used_dict = keyword_dict_adult_filter(key_dict, 1)
        ad_link_dict = make_key_and_path_list_from_exist_keys(ad_used_dict, project_dir, 1)
    else:
        key_dict_l = key_dict
        ad_link_dict = {}

    link_dict = make_key_and_path_list_from_exist_keys(key_dict_l, project_dir, 3)
    # print(link_dict)
    # print(ad_link_dict)
    art_map = [[source_mod.introduction, 1], [source_mod.d_introduction, 'straight'],
               [source_mod.d_advantage, [2, 3, 4]],
               [source_mod.p_introduction, 'straight'], [source_mod.purpose_advantage, 3],
               [source_mod.tips_bonus, [0, 1, 2]], [source_mod.process, 'straight'],
               [source_mod.tips_bonus, [1, 2, 3]], [source_mod.conclusion, 1]]
    for md_name in change_list:
        old_md = '{}/md_files/{}.md'.format(project_dir, md_name)
        with open(old_md, 'r', encoding='utf-8') as m:
            md_str = m.read()
        keywords = key_dict[md_name]
        if '<!--ori-->' in md_str:
            print('original sentence in : ' + old_md)
            keywords['ori_flag'] = True
            continue
        else:
            update_md.append(old_md)
        if 'sub' not in keywords:
            no_sub_flag = True
        else:
            no_sub_flag = False
        if 'obj' not in keywords:
            no_obj_flag = True
        else:
            no_obj_flag = False
        a_adj_flag = keywords['a_adj_flag']
        main_key = keywords['act_code']
        part_code = keywords['type'].replace('only_', '')
        dir_name = re.sub(r'/.*$', '', md_name)
        subject_sex = keywords['sub_sex']
        page_id = keywords['page_id']
        # print(keywords)
        # print(adult_checker_by_keywords(keywords))
        if adult_checker_by_keywords(keywords):
            link_dict_u = ad_link_dict
        else:
            link_dict_u = link_dict
        # print(keywords)
        make_keywords_sample(keywords, a_adj_flag, no_obj_flag, no_sub_flag, part_code)
        old_pub = ''
        old_pub_l = re.findall(r'p::(.+?)\n', md_str)
        if old_pub_l:
            old_pub = old_pub_l[0]
        dt_str = old_pub
        recipe_list, counter_d, title_str = make_new_page(keywords, source_mod, art_map, project_dir, dir_name,
                                                          link_dict_u, main_key, recipe_flag, subject_sex, a_adj_flag,
                                                          page_id, dt_str, part_code, no_obj_flag, no_sub_flag,
                                                          counter_d)
        keywords['title_str'] = title_str
        key_dict[md_name] = keywords
        recipe_dict[keywords['page_name']] = recipe_list
    # print(recipe_dict)
    with open(project_dir + '/pickle_pot/recipe_dict.pkl', 'wb') as rp:
        pickle.dump(recipe_dict, rp)
    with open(project_dir + '/pickle_pot/key_dict.pkl', 'wb') as kp:
        pickle.dump(key_dict, kp)
    insert_relation_page_list_to_md(project_dir, key_dict)
    return update_md


def change_section_in_exist_art(use_path_list, target_section, insert_source):
    # 例えば、既存の時期もの段落の段落を他のsourceに差し替え
    recipe_flag = True
    if type(use_path_list) == list:
        project_dir = re.sub(r'/.*$', '', use_path_list[0])
    else:
        project_dir = re.sub(r'/.*$', '', use_path_list)
    print('project_dir : {}'.format(project_dir))
    with open(project_dir + '/pickle_pot/recipe_dict.pkl', 'rb') as rf:
        recipe_dict = pickle.load(rf)
    with open(project_dir + '/pickle_pot/key_dict.pkl', 'rb') as rk:
        key_dict = pickle.load(rk)
    counter_d = {}
    # print(key_dict)
    # print(recipe_dict)
    if type(use_path_list) == list:
        change_list = [re.sub(r'^.+/md_files/(.+).md', r'\1', x) for x in use_path_list]
    else:
        change_dir = re.sub(r'^.+/md_files/', '', use_path_list)
        change_list = [x for x in key_dict if change_dir in x]
    # print(change_list)
    include_list = [x for x in change_list if target_section in recipe_dict[x]]
    # print(include_list)
    # return
    for md_name in include_list:
        # print(keywords)
        old_md = '{}/md_files/{}.md'.format(project_dir, md_name)
        with open(old_md, 'r', encoding='utf-8') as m:
            md_str = m.read()

        keywords = key_dict[md_name]
        if 'sub' not in keywords:
            no_sub_flag = True
        else:
            no_sub_flag = False
        if 'obj' not in keywords:
            no_obj_flag = True
        else:
            no_obj_flag = False
        a_adj_flag = keywords['a_adj_flag']
        main_key = keywords['act_code']
        part_code = keywords['type'].replace('only_', '')
        subject_sex = keywords['sub_sex']
        sec_str = re.findall(r'\n.*?<!--sw-' + target_section + r'[\s\S]*<!--sw-' + target_section + r'.+?-->\n',
                             md_str)
        # print(sec_str)
        if sec_str:
            if '<!--ori-->' in sec_str[0]:
                print('original sentence in : ' + sec_str[0])
                keywords['ori_flag'] = True
                continue
        key_phrase = key_phrase_maker(keywords, a_adj_flag, no_obj_flag, no_sub_flag, part_code)
        noun_dict = noun_dict_maker(key_phrase, main_key, subject_sex, no_sub_flag, keywords)
        # print(noun_dict)
        conj_dict = {x['before']: x['after'] for x in wd.conj_list}
        site_list = ['ワクワクメール', 'ハッピーメール']
        site1 = random.choice(site_list)
        site_list.remove(site1)
        site2 = site_list[0]

        section_str, recipe, counter_d = make_new_section(insert_source, noun_dict, conj_dict, site1, site2, {},
                                                          '', recipe_flag, subject_sex, main_key, part_code,
                                                          project_dir, counter_d)
        section_str = section_str.replace('%', '\n%')
        result_str = section_str + '\n\n'
        recipe_dict[insert_source['info']['sec_name']] = recipe
        print('result_str : {}'.format(result_str))

        # print(keywords)
        # print(adult_checker_by_keywords(keywords))
        # if adult_checker_by_keywords(keywords):
        #     link_dict_u = ad_link_dict
        # else:
        #     link_dict_u = link_dict
        # print(keywords)

    # print(recipe_dict)
    # with open(project_dir + '/pickle_pot/recipe_dict.pkl', 'wb') as rp:
    #     pickle.dump(recipe_dict, rp)
    insert_relation_page_list_to_md(project_dir, key_dict)


def adult_checker_by_keywords(keywords):
    result = False
    if keywords['act_code'] in no_adult_prj:
        if 'ad' in keywords:
            if keywords['ad'] != 3:
                result = True
        elif 'a_ad' in keywords:
            if keywords['a_ad'] != 3:
                result = True
        elif 's_ad' in keywords:
            if keywords['s_ad'] != 3:
                result = True
    return result


def keyword_dict_adult_filter(key_dict, ad_num):
    result = {}
    for key_id in key_dict:
        if 'ad' in key_dict[key_id]:
            if key_dict[key_id]['ad'] == ad_num:
                result[key_id] = key_dict[key_id]
        elif 'a_ad' in key_dict[key_id]:
            if key_dict[key_id]['a_ad'] == ad_num:
                result[key_id] = key_dict[key_id]
        elif 's_ad' in key_dict[key_id]:
            if key_dict[key_id]['s_ad'] == ad_num:
                result[key_id] = key_dict[key_id]
        else:
            result[key_id] = key_dict[key_id]
    return result


def insert_relation_page_list_to_md(project_dir, key_dict):
    re_dict = insert_relational_list.compare_key_for_relational_art(key_dict, relational_list_len)
    for page_name in re_dict:
        if project_dir in mass_dir_list:
            p_dir_path = 'mass_production/' + project_dir
        else:
            p_dir_path = project_dir
        with open(p_dir_path + '/md_files/' + page_name + '.md', 'r', encoding='utf-8') as f:
            md_str = f.read()
        if 'relation_list' not in md_str:
            md_str += "\n\nrelation_list = '" + re_dict[page_name] + "'"
        else:
            md_str = re.sub(r"relation_list = '.+?'", "relation_list = '" + re_dict[page_name] + "'", md_str)
        # print(md_str)
        with open(p_dir_path + '/md_files/' + page_name + '.md', 'w', encoding='utf-8') as g:
            g.write(md_str)


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
    # print('html_str : '.format(html_str))
    return html_str


def id_filter(use_id_list, main_key, key_list, part_cord):
    if main_key in no_adult_prj:
        # print(key_list)
        if 'ad' in key_list[0]:
            use_id_list = [x for x in use_id_list if key_list[x]['ad'] != 0]
        elif 'a_ad' in key_list[0]:
            use_id_list = [x for x in use_id_list if key_list[x]['a_ad'] != 0]
        elif 's_ad' in key_list[0]:
            use_id_list = [x for x in use_id_list if key_list[x]['s_ad'] != 0]
    if main_key == 'dt' and part_cord == 'act':
        use_id_list = [x for x in use_id_list if key_list[x]['a_sex'] != 'w']
    # print('use_id_list : {}'.format(use_id_list))
    return use_id_list


def make_used_key_dict(project_dir, use_id_list, this_key_code, start_id):
    pkl_path = '{}/pickle_pot/used_id.pkl'.format(project_dir)
    add_id_dict = {}
    dict_temp = {'obj_m': {}, 'obj_w': {}, 'sub_m': {}, 'sub_w': {}, 'act': {}, 'adj_act': {}, 'max_id': 'n'}
    if os.path.exists(pkl_path):
        with open(pkl_path, 'rb') as p:
            used_dict = pickle.load(p)
        # print('exist_pk_data : {}'.format(used_dict))
        # used_dict['act'] = {}
        # used_dict['adj_act'] = {}
        # used_dict['obj_w'] = {}
        # used_dict['max_id'] = 0
        # print(used_dict)
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
            if key_name in dir_dict[project_dir]:
                dir_str = '../{}/'.format(dir_dict[project_dir][key_name])
            else:
                dir_str = ''
            if key_name != 'adj_act' and key_name != 'act':
                if project_dir in html_str_dict:
                    if key_name in html_str_dict[project_dir]:
                        html_str = html_str_dict[project_dir][key_name]
                result[key_name] = [[key_source_dict[key_name][x]['all_key'],
                                     dir_str + html_str.replace('{}',
                                                                key_source_dict[key_name][x]['eng'].replace('-', '_'))]
                                    for x in used_dict[key_name] if x in key_source_dict[key_name]]
            else:
                # print(key_source_dict['adj_act'])
                if project_dir in html_str_dict:
                    if key_name in html_str_dict[project_dir]:
                        html_str = html_str_dict[project_dir][key_name]
                result[key_name] = [[key_source_dict[key_name][x]['act_noun'],
                                     dir_str + html_str.replace('{}',
                                                                key_source_dict[key_name][x]['eng'].replace('-', '_'))]
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


def make_key_and_path_list_for_mass(html_str, key_list):
    result = {'obj_m': [], 'obj_w': [], 'sub_m': [], 'sub_w': [], 'act': [], 'adj_act': []}
    link_list = [[x['all_key'].replace(' ', ''), html_str.replace('{}', x['eng'].replace('-', '_'))] for x in key_list]
    for key in result:
        result[key] = link_list
    return result


def make_key_and_path_list_from_exist_keys(key_dict, project_dir, ad_num):
    result = {'obj_m': [], 'obj_w': [], 'sub_m': [], 'sub_w': [], 'act': [], 'adj_act': []}
    for md_path in key_dict:
        keywords = key_dict[md_path]
        if keywords['type'] == 'only_act':
            cat = 'act'
        elif keywords['type'] == 'only_obj' and keywords['o_sex'] == 'm':
            cat = 'obj_m'
        elif keywords['type'] == 'only_obj' and keywords['o_sex'] == 'w':
            cat = 'obj_w'
        elif keywords['type'] == 'only_sub' and keywords['o_sex'] == 'm':
            cat = 'sub_m'
        elif keywords['type'] == 'only_sub' and keywords['o_sex'] == 'w':
            cat = 'sub_w'
        else:
            print('error!! : ' + md_path)
            return
        result[cat].append([keywords['all_key'], '../' + md_path])
    # print(result)
    for key_n in key_source_dict:
        if not result[key_n]:
            if project_dir not in no_adult_dir:
                if key_n == 'adj_act':
                    result[key_n] = [[key_source_dict[key_n][x]['all_key'], ''] for x in key_source_dict[key_n]]
                else:
                    result[key_n] = [[key_source_dict[key_n][x]['all_key'], ''] for x in key_source_dict[key_n]]
            else:
                for key_id in key_source_dict[key_n]:
                    if 'ad' in key_source_dict[key_n][key_id]:
                        if key_source_dict[key_n][key_id]['ad'] == ad_num:
                            result[key_n].append([key_source_dict[key_n][key_id]['all_key'], ''])
                    elif 'a_ad' in key_source_dict[key_n][key_id]:
                        if key_source_dict[key_n][key_id]['a_ad'] == ad_num:
                            result[key_n].append([key_source_dict[key_n][key_id]['all_key'], ''])
                    elif 's_ad' in key_source_dict[key_n][key_id]:
                        if key_source_dict[key_n][key_id]['s_ad'] == ad_num:
                            result[key_n].append([key_source_dict[key_n][key_id]['all_key'], ''])
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
    print('source_dict : {}'.format(source_dict))
    return True
    # if source_dict['o_ms'] == 's':
    #     return True
    # else:
    #     return False


def make_new_page(keywords, source_mod, art_map, project_dir, dir_name, link_dict, main_key, recipe_flag, subject_sex,
                  a_adj_flag, page_id, dt_str, part_code, no_obj_flag, no_sub_flag, counter_d):
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
                 'gf': {'site_name': '出会い系メールの例文サイト', 'site_author': 'ピエール'},
                 'koi': {'site_name': 'ネット恋活で恋人と出会う方法', 'site_author': '谷本'},
                 'sex': {'site_name': 'セックスできる出会い系サイトを探せ', 'site_author': '後藤'},
                 'bg': {'site_name': '出会い系初心者のための攻略法', 'site_author': '丸山'},
                 'mass': {'site_name': '当サイト', 'site_author': '管理人'}}
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
    key_phrase = key_phrase_maker(keywords, a_adj_flag, no_obj_flag, no_sub_flag, part_code)
    # print('key_phrase : {}'.format(key_phrase))
    key_phrase['this-site-title'] = [site_data[main_key]['site_name']]
    key_phrase['this-site-author'] = [site_data[main_key]['site_author']]
    noun_dict = noun_dict_maker(key_phrase, main_key, subject_sex, no_sub_flag, keywords)
    conj_dict = {x['before']: x['after'] for x in wd.conj_list}
    title_count = 40
    title_str = ''
    t_counter = 0
    while title_count > 35 and t_counter < 30:
        title_str, t_recipe, counter_d = make_new_title(source_mod.title[part_code][main_key], noun_dict, conj_dict,
                                                        site1, site2, link_dict, this_path, subject_sex, recipe_flag,
                                                        main_key, part_code, project_dir, counter_d)
        title_count = len(re.sub(r'<!--sw-.*?-->', '', title_str))
        t_counter += 1
    print('{}  ({})'.format(title_str, title_count))
    result_str += 't::' + title_str + '\n'
    des_str, d_recipe, counter_d = make_new_title(source_mod.des[keywords['act_code']], noun_dict, conj_dict, site1,
                                                  site2, link_dict, this_path, subject_sex, recipe_flag, main_key,
                                                  part_code, project_dir, counter_d)
    result_str += 'd::' + des_str.replace('\n', '') + '\n'
    # print(used_id)
    # print(type(used_id[-1]))
    # print(type(keywords['id']))
    result_str += 'n::' + str(page_id) + '\n'
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
        this_sec = option_section_filter(this_sec, keywords, project_dir)
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
    if project_dir in mass_dir_list:
        p_dir_path = 'mass_production/' + project_dir
    else:
        p_dir_path = project_dir
    with open(p_dir_path + '/md_files/' + dir_name + '/' + keywords['page_name'] + '.md', 'w', encoding='utf-8') as f:
        f.write(result_str)
    return recipe_list, counter_d, title_str


def option_section_filter(this_sec, keywords, project_dir):
    if project_dir != 'sfd':
        random_list = [0, 1, 1]
        opt_dict = {'month': [source_data.di_3_1, source_data.di_3_2]}
        if 'option' in this_sec['info']:
            if this_sec['info']['option'][0] == 'month':
                if random.choice(random_list) == 1:
                    month_num = int(keywords['hot_month'].replace('月', ''))
                    for source in opt_dict['month']:
                        if month_num in source['info']['option'][1]:
                            this_sec = source
    return this_sec


def noun_dict_maker(key_phrase, main_key, subject_sex, no_sub_flag, keywords):
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
    return noun_dict


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
                    if key in row:
                        removed_str = re.sub(r'\[.*?]\(.*?\)', '', row)
                        removed_str = re.sub(r'<a .*?>.*?</a>', '', removed_str)
                        if key in removed_str:
                            new_row = row
                            i_url = '[{}(R18)](../../{}html_files/{}{}/{})'.format(key, '../' * main_dir.count('/'),
                                                                                   main_dir, aff_dir, sc_url[key])
                            if row.count(key) == 1:
                                new_row = row.replace(key, i_url, 1)
                            else:
                                wide_str = re.findall(r'.' + key + r'.', row)
                                if wide_str:
                                    for ws in wide_str:
                                        if ws in removed_str:
                                            new_row = row.replace(ws, ws.replace(key, i_url), 1)
                                        else:
                                            print('site aff replace error!!')
                            md_str = md_str.replace(row, new_row)
                        # print('insert {} link str'.format(key))
                        # used_name.append(key)
                        break
    return md_str


def key_phrase_maker(keywords, a_adj_flag, no_obj_flag, no_sub_flag, part_code):
    if '作る' in keywords['act']:
        act_base = keywords['act']
        act_i = act_base.replace('を作る', 'にし')
        act_y = act_base.replace('を作る', 'を作っ')
        act_and = act_base.replace('作る', '作って')
        act_can = act_base.replace('作る', '作れ')
        act_can_d = act_base.replace('を作る', 'にでき')
        act_noun = keywords['act_noun']
        if 'act_target' in keywords:
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
    elif '探す' in keywords['act']:
        act_base = keywords['act']
        act_i = act_base.replace('を探す', 'にし')
        act_y = act_base.replace('を探す', 'を探し')
        act_and = act_base.replace('探す', '探して')
        act_can = act_base.replace('探す', '探せ')
        act_can_d = act_base.replace('を探す', 'にでき')
        act_noun = keywords['act_noun']
        if 'act_target' in keywords:
            act_target = keywords['act_target']
        else:
            act_target = act_base.replace('を探す', '')
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
        act_y = '<!--lost-dt-i-->'
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
        act_y = act_base.replace('出会う', '出会っ')
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
        if 'act_target' in keywords:
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
        act_y = act_base.replace('する', 'し')
        act_and = act_base.replace('する', 'して')
        act_can = act_base.replace('をする', 'ができ')
        act_can_d = act_base.replace('をする', 'ができ')
        act_noun = keywords['act_noun']
        if 'act_target' in keywords:
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
        act_y = act_base.replace('する', 'し')
        act_and = act_base.replace('する', 'して')
        act_can = act_base.replace('する', 'でき')
        act_can_d = act_base.replace('する', 'でき')
        act_noun = keywords['act_noun']
        if 'act_target' in keywords:
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
        act_y = act_base.replace('なる', 'なっ')
        act_and = act_base.replace('なる', 'なって')
        act_can = act_base.replace('なる', 'なれ')
        act_can_d = act_base.replace('なる', 'なれ')
        act_noun = keywords['act_noun']
        if 'act_target' in keywords:
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
        act_y = act_base.replace('てもらう', 'てもらっ')
        act_and = act_base.replace('てもらう', 'てもらって')
        act_can = act_base.replace('てもらう', 'てもらえ')
        act_can_d = act_base.replace('てもらう', 'てもらえ')
        act_noun = keywords['act_noun']
        if 'act_target' in keywords:
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
        act_y = re.sub(r'う$', 'っ', act_base)
        act_and = re.sub(r'う$', 'って', act_base)
        act_can = re.sub(r'う$', 'い', act_base)
        act_can_d = re.sub(r'う$', 'え', act_base)
        act_noun = keywords['act_noun']
        if 'act_target' in keywords:
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
        act_y = re.sub(r'す$', 'し', act_base)
        act_and = re.sub(r'す$', 'して', act_base)
        act_can = re.sub(r'す$', 'せ', act_base)
        act_can_d = re.sub(r'す$', 'せ', act_base)
        act_noun = keywords['act_noun']
        if 'act_target' in keywords:
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
        act_y = re.sub(r'てる$', 'て', act_base)
        act_and = re.sub(r'てる$', 'てて', act_base)
        act_can = re.sub(r'てる$', 'てられ', act_base)
        act_can_d = re.sub(r'てる$', 'てられ', act_base)
        act_noun = keywords['act_noun']
        if 'act_target' in keywords:
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
        act_y = re.sub(r'れる$', 'れ', act_base)
        act_and = re.sub(r'れる$', 'って', act_base)
        act_can = re.sub(r'れる$', 'れ', act_base)
        act_can_d = re.sub(r'れる$', 'れ', act_base)
        act_noun = keywords['act_noun']
        if 'act_target' in keywords:
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
        act_y = re.sub(r'せる$', 'せ', act_base)
        act_and = re.sub(r'せる$', 'せて', act_base)
        act_can = re.sub(r'せる$', 'せられ', act_base)
        act_can_d = re.sub(r'せる$', 'せられ', act_base)
        act_noun = keywords['act_noun']
        if 'act_target' in keywords:
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
        act_y = re.sub(r'く$', 'き', act_base)
        act_and = re.sub(r'く$', 'って', act_base)
        act_can = re.sub(r'く$', 'け', act_base)
        act_can_d = re.sub(r'く$', 'け', act_base)
        act_noun = keywords['act_noun']
        if 'act_target' in keywords:
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
        act_y = re.sub(r'る$', 'っ', act_base)
        act_and = re.sub(r'る$', 'って', act_base)
        act_can = re.sub(r'る$', 'れ', act_base)
        act_can_d = re.sub(r'る$', 'れ', act_base)
        act_noun = keywords['act_noun']
        if 'act_target' in keywords:
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
        act_y = act_base.replace('する', 'し')
        act_and = act_base.replace('する', 'して')
        act_can = act_base.replace('する', 'でき')
        act_can_d = act_base.replace('する', 'でき')
        act_noun = keywords['act_noun']
        if 'act_target' in keywords:
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
        print(keywords)
        if 'o_age' in keywords:
            target_person = '<!--woman-{}-->'.format(keywords['o_age'])
        else:
            target_person = '<!--woman-n-->'
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
        if 'adj_v' in keywords:
            m_act_adj = keywords['adj_v']
            m_act_adj_v = keywords['adj_n']
            t_act_adj = keywords['a_adj']
        else:
            m_act_adj = keywords['a_adj']
            m_act_adj_v = keywords['a_adj']
            t_act_adj = keywords['a_adj']
    else:
        act_adj = keywords['a_adj']
        m_act_adj = ''
        m_act_adj_v = ''
        t_act_adj = ''
    if no_sub_flag:
        alt_sub_s = ''
        alt_sub = ''
        alt_sub_g = ''
        sub_also = ''
        sub_by = ''
    else:
        alt_sub_s = ''
        alt_sub = sub + 'が'
        alt_sub_g = sub + 'の'
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
    way_for_all = act_way
    way_for_all_g = act_way_g
    obj_want_act = act_base + 'したい<!--obj-sex-->'
    if part_code == 'act':
        total_target = act_target
        act_way = '出会う<!--way-->'
        act_way_g = '出会う<!--way-->'
    elif part_code == 'sub':
        total_target = sub
    elif part_code == 'obj':
        total_target = obj
        obj_want_act = obj
    else:
        total_target = act_target
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
            'k-alt-way': [alt_sub + m_act_adj + alt_obj + act_way, alt_sub_g + alt_obj_g + act_way_g],
            'k-alt-do': [alt_sub + m_act_adj + alt_obj + act_base],
            'k-alt-do-a': [alt_sub + m_act_adj + obj_adj + alt_obj + act_base],
            'k-alt-easy': [alt_sub + m_act_adj + alt_obj_d + act_i + 'やすい'],
            'k-alt-to-find': [sub_by + obj_as_target + '探し'],
            'k-alt-to-find-a': [sub_by + obj_adj + obj_as_target + '探し'],
            'k-alt-find': [alt_sub + m_act_adj + obj_as_target + 'を探す'],
            'k-alt-find-a': [alt_sub + m_act_adj + obj_adj + obj_as_target + 'を探す'],

            'k-obj': [obj],
            'k-obj-adj': [obj + 'の'],
            'k-obj-status': [obj_want_act],
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
            'k-act-y': [m_act_adj + act_y],
            'k-act-and': [m_act_adj + act_and],
            'k-act-want': [m_act_adj + act_i + 'たい'],
            'k-act-want-sim': [act_i + 'たい'],
            'k-act-can': [act_can + 'る', act_can_d + 'る'],
            'k-act-can-adj': [m_act_adj + act_can + 'る', m_act_adj + act_can_d + 'る'],  # ミックス
            'k-act-can-i': [act_can],  # セフレにでき（そう）,セックスでき(ない）
            'k-act-can-d-i': [act_can_d],  # セフレにでき
            'k-act-can-long': [act_can + 'ます'],
            'k-act-can-not-do': [act_can + 'ない'],
            'k-act-can-not-do-long': [act_can + 'ません'],
            'k-act-way': [m_act_adj_v + act_way, act_way, act_way, m_act_adj + act_way_g],
            'k-act-way-sim': [act_way],
            'k-act-way-adj': [m_act_adj_v + act_way, m_act_adj + act_way_g],
            'k-act-way-t': [act_way],
            'k-act-can-easy': [act_i + 'やすい', '<!--easily-->' + act_can + 'る'],
            'k-act-can-easy-long': [act_i + 'やすいです', '<!--easily-->' + act_can + 'ます'],
            'k-act-can-easy-with': ['を' + act_i + 'やすい', 'の' + act_can + 'る'],
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
            'act-with-d': [act_with_d],
            'k-title_a_adj': [t_act_adj],
            'k-target-to-find': [total_target],
            'k-act-way-all': [way_for_all, way_for_all_g],
            'k-obj-want-act': [obj_want_act],
            'k-act-bbs': [act_noun + '掲示板']}
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
                    'k-obj-act-way': [m_act_adj + act_way_g, act_way_g],
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
    if no_sub_flag and no_obj_flag:
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
    if no_sub_flag:
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
        if '女性' not in keywords['obj'] or '女子' not in keywords['obj']:
            keys['k-how-to'].append(m_act_adj + alt_sub + obj_k + act_way_g)
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


def make_keywords_sample(keywords, a_adj_flag, no_obj_flag, no_sub_flag, part_code):
    r_str = ''
    keys = key_phrase_maker(keywords, a_adj_flag, no_obj_flag, no_sub_flag, part_code)
    for k in keys:
        r_str += '<!--{}-->  :  {}\n'.format(k, pprint.pformat(keys[k]))
        # print('<!--{}-->  :  {}'.format(k, keys[k]))
    # with open('key_sample.md', 'w', encoding='utf-8') as f:
    #     f.write(r_str)


def make_keywords_sample_dict(keywords, a_adj_flag, no_obj_flag, no_sub_flag, part_code):
    result_dict = {}
    new_dict = []
    keys = key_phrase_maker(keywords, a_adj_flag, no_obj_flag, no_sub_flag, part_code)
    anchor_dict = {y['before']: y['after'] for y in wd.noun_list}
    anchor_dict.update({'<!--obj-married-->': '人妻'})
    # print(keys)
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
            # print(kw)
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
    if 'vrt' in section_dict['info']:
        for v_code in section_dict['info']['vrt']:
            v_word.append(['<!--vrt-{}-->'.format(v_code), random.choice(words_dict.vrt_list[v_code])])
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


def link_obj_word_insert(sentence_str, link_dict, this_path, subject_sex, part_code):
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
        elif type_str == 'adj_act':
            target_list = link_dict['adj_act']
        elif type_str == 'act':
            target_list = link_dict['act']
        else:
            target_list = link_dict[type_str_s]
        select_str = random.choice(target_list)
        if select_str[1] in used_list or select_str[1] == this_path:
            while select_str[1] in used_list or select_str[1] == this_path:
                select_str = random.choice(link_dict[type_str_s])
            used_list.append(select_str[1])
        if select_str[1]:
            if type_str == part_code:
                ed_str = re.sub(r'^.*/', '', select_str[1])
                sentence_str = sentence_str.replace('<!--link-word-{}-->'.format(type_str),
                                                    '[{}]({}.md)'.format(select_str[0], ed_str), 1)
            else:
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
        for v_row in v_word:
            sentence_str = sentence_str.replace(v_row[0], v_row[1])
    if main_key == 'bg':
        bbs_str = re.findall(r'<!--site-->', sentence_str)
        if bbs_str:
            if random.choices([True, False], [1, 4]):
                sentence_str = sentence_str.replace('<!--site-->', '<!--k-act-bbs-->')
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
        sentence_str = link_obj_word_insert(sentence_str, link_dict, this_path, subject_sex, part_code)
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
                # print(blank)
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
    print('pkl_data : {}'.format(pkl_data))


def auto_make_md_for_all_key(project_dir, dir_name, main_key, recipe_flag, start_id, insert_pub_date,
                             exist_update_flag):
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
                                           insert_pub_date=insert_pub_date, part_code=part_code_str,
                                           copy_pub_flag=False, exist_update_flag=exist_update_flag)


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
    dup_num = []
    md_files = glob.glob(project_dir + '/md_files/**/**.md')
    md_files = [x for x in md_files if '_copy' not in x]
    for file_path in md_files:
        # print('file_path : {}'.format(file_path))
        with open(file_path, 'r', encoding='utf-8') as f:
            md_str = f.read()
            id_str_l = re.findall(r'\nn::(\d*)\n', md_str)
            if id_str_l:
                if id_str_l[0] in num_list:
                    dup_num.append(id_str_l[0])
                num_list.append([int(id_str_l[0]), file_path])
    num_list.sort(key=lambda x: x[0])
    # print(num_list)
    if num_list:
        max_num = num_list[-1][0]
        print('max_id : {}'.format(max_num))
        no_use_list = [x for x in range(max_num + 1) if x not in [y[0] for y in num_list]]
        print('no_use_list : {}'.format(no_use_list))
        with open(num_list[-1][1], 'r', encoding='utf-8') as g:
            l_str = g.read()
            last_pub_l = re.findall(r'p::(.*?)\n', l_str)
            if last_pub_l:
                last_pub = last_pub_l[0]
            else:
                last_pub = ''
    else:
        max_num = 0
        last_pub = ''
    if dup_num:
        print('dup_num : {}'.format(dup_num))
    return max_num, last_pub


def test_dir_filter(md_dir, project_dir):
    if 'test' in project_dir:
        test_dir = md_dir
        test_num = 0
        while os.path.exists(project_dir + '/md_files/' + test_dir):
            test_num += 1
            test_dir = md_dir + '_' + str(test_num)
        md_dir = test_dir
    return md_dir


def make_md_by_project_and_part(project_dir, part_list, subject_sex, next_id, exist_update_flag):
    # part_dict = {'obj': {'man': 'obj_m', 'woman': 'obj_w'},
    #              'sub': {'man': 'sub_m', 'woman': 'sub_w'},
    #              'adj_act': {'man': 'adj_act', 'woman': 'adj_act'},
    #              'act': {'man': 'act', 'woman': 'act'}}
    main_key_dict = {'goodbyedt': 'dt', 'shoshin': 'bg', 'test': 'sf', 'howto': 'cov', 'htaiken': 'ht',
                     'joshideai': 'sex', 'koibito': 'koi', 'konkatsu': 'mh', 'online_marriage': 'olm',
                     'rei_site': 'gf', 'women': 'bf', 'sfd': 'sf'}  # for multiple
    sub_sex_dict = {'goodbyedt': {'act': ['man'], 'obj_m': ['man']},
                    'shoshin': {'act': ['man']},
                    'howto': {'obj_m': ['man'], 'obj_w': ['woman']},
                    'htaiken': {'obj_m': ['man'], 'obj_w': ['woman']},
                    'joshideai': {'obj_m': ['man'], 'adj_act': ['man']},
                    'koibito': {'obj_m': ['man'], 'obj_w': ['woman']},
                    'konkatsu': {'obj_m': ['man'], 'obj_w': ['woman']},
                    'online_marriage': {'obj_m': ['man'], 'obj_w': ['woman']},
                    'rei_site': {'obj_m': ['man'], 'adj_act': ['man']},
                    'women': {'obj_w': ['woman']},
                    'test': {'adj_act': ['man'], 'obj_m': ['man']},
                    'sfd': {'obj_m': ['man'], 'obj_w': ['woman'], 'sub_m': ['man'], 'sub_w': ['woman'], 'act': ['man'],
                            'adj_act': ['man']}
                    }  # for multiple
    if not part_list:
        part_list = []
        for p in dir_dict[project_dir]:
            if os.path.exists(project_dir + '/md_files/' + dir_dict[project_dir][p]):
                part_list.append(p)
    # print(part_list)
    for part_code in part_list:
        print('part_code : {}'.format(part_code))
        if part_code != 'adj_act':
            p_code = re.sub(r'_.', '', part_code)
        else:
            p_code = part_code
        # print(p_code)
        if not subject_sex:
            sub_list = sub_sex_dict[project_dir][part_code]
        else:
            sub_list = [subject_sex]
        for sub_sex in sub_list:
            md_dir = dir_dict[project_dir][part_code]
            # md_dir = test_dir_filter(md_dir, project_dir)
            key_source = key_source_dict[part_code]
            max_id, last_pub = search_max_id(project_dir)
            if not next_id or next_id == 0:
                next_id = max_id + 1
            if last_pub:
                if 'T' not in last_pub:
                    last_pub = last_pub + 'T16:33:19'
                last_pub = last_pub.replace('/', '-')
            else:
                last_pub = '2021-06-01T01:02:17'
            # return
            make_new_pages_to_md_from_key_list(project_dir, md_dir, source_data, main_key_dict[project_dir],
                                               [], key_source, recipe_flag=True, subject_sex=sub_sex, start_id=next_id,
                                               insert_pub_date=last_pub, part_code=p_code, copy_pub_flag=True,
                                               exist_update_flag=exist_update_flag)
            next_id = 0
    # with open(project_dir + '/pickle_pot/key_dict.pkl', 'rb') as f:
    #     key_dict = pickle.load(f)
    # print(key_dict)


if __name__ == '__main__':
    # test_new_section(source_data.all_list, keywords_p)
    # sf_import_to_source()
    # make_keywords_sample(keywords_p)
    # make_used_key_data('sfd')
    # auto_make_md_for_all_key('sfd', 'obj_m', 'sf', recipe_flag=True, start_id=554,
    #                          insert_pub_date='2021-04-08T18:22:12')
    # insert_pub_date の書式　'%Y-%m-%dT%H:%M:%S'
    # make_used_id_list_for_key_data('sfd')

    make_md_by_project_and_part('test', ['adj_act'], 'man', 580, exist_update_flag=False)  # for multiple
    # search_max_id('women')

    # todo: 出会い系サイトを他に変更　婚活サイト、SNS、ツイッター
    # todo: 地域の婚活, パパ活、　割り切り, 不倫, 出会う, マッチングアプリで出会う、趣味の出会い
    # todo: その対象の探し方、o_catで切り替えるなどして多様化
    # todo: 高齢者向けの記事とキーワード
