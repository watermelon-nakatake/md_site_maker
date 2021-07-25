import copy
import random
import re
import numpy as np
import os
import pprint
import pickle
import source_data
import words_dict
import words_dict as wd
import obj_source
import key_source


def make_new_pages_to_md(project_dir, obj_list, act_list, sub_list, source_mod, dir_name, start_num, html_head):
    keywords_dict = {}
    recipe_dict = {}
    art_map = [[source_mod.introduction, 1], [source_mod.d_introduction, 'straight'],
               [source_mod.d_advantage, [2, 3, 4]],
               [source_mod.p_introduction, 'straight'], [source_mod.purpose_advantage, 3],
               [source_mod.tips_bonus, [0, 1, 2]], [source_mod.process, 'straight'],
               [source_mod.tips_bonus, [1, 2, 3]], [source_mod.conclusion, 1]]
    # print(art_map_p)
    # art_map = [[[{x['info']['sec_name']: x for x in u} for u in z[0]], z[1]] for z in art_map_p]
    # print(art_map)
    link_dict = make_key_and_path_list(project_dir, dir_name, html_head, [], [])
    id_num = start_num
    if not os.path.exists(project_dir + '/md_files/' + dir_name):
        os.mkdir(project_dir + '/md_files/' + dir_name)
    for obj in obj_list:
        if obj_source_filter(obj):
            sub_str = np.random.choice(['独身男性', '童貞', '男性'])
            sub_adj = np.random.choice(['普通の', 'モテない', '婚活中の'])
            if obj['ms'] == 'm':
                act_adj = np.random.choice(['不倫', '浮気', 'NTR'])
            else:
                act_adj = np.random.choice(['安全に', '確実に', '簡単に', 'すぐに', '無料で'])
            page_name = '{}_{}'.format(html_head, obj['eng'].replace('-', '_'))
            keywords = {
                'page_name': page_name, 'id': id_num,

                's_adj': sub_adj, 'sub': sub_str,

                'o_adj': obj['adj'], 'obj': obj['noun'], 'obj_key': obj['keyword'], 'obj_p': obj['particle'],
                'o_reason': obj['reason'], 't_sex': 'm', 't_age': 'n', 't_cat': 'j',

                'act_adj': act_adj, 'act': 'セックスする', 'act_noun': 'セックス相手', 'act_noun_flag': False,
                'act_connection': ['肉体関係'],

                'act_code': 'sex',
                'hot_month': '８月', 'hot_season': '夏', 'hot_month_next': '９月'}
            # sex: m or w, age: y o n,  cat: job age chara body looks preference(性的嗜好) status
            make_keywords_sample(keywords)
            recipe_list = make_new_page(keywords, source_mod, art_map, project_dir, dir_name, obj_list, html_head,
                                        link_dict)
            keywords_dict[page_name] = keywords
            recipe_dict[page_name] = recipe_list
            id_num += 1
    # print(recipe_dict)


def make_new_pages_to_md_from_key_list(project_dir, dir_name, html_str, source_mod, main_key, use_id_list, key_list):
    # 必要最低限のキーワードリストで機動的に記事作成
    # 個別記事のリストの中にメインワードのキーワード ex.gf で選択
    # 既存記事のキーワードとurlをランダム選択scrに渡す
    recipe_dict = {}
    art_map = [[source_mod.introduction, 1], [source_mod.d_introduction, 'straight'],
               [source_mod.d_advantage, [2, 3, 4]],
               [source_mod.p_introduction, 'straight'], [source_mod.purpose_advantage, 3],
               [source_mod.tips_bonus, [0, 1, 2]], [source_mod.process, 'straight'],
               [source_mod.tips_bonus, [1, 2, 3]], [source_mod.conclusion, 1]]
    add_key_dict = {'s_adj': ['普通の', 'モテない', '婚活中の'], 'sub': ['独身男性', '童貞', '男性']}
    main_key_dict = {'sex': {'act': 'セックスする', 'act_noun': 'セックス相手', 'act_noun_flag': False,
                             'act_connection': ['肉体関係'], 'act_code': 'sex'}}
    hot_info = {'hot_month': '８月', 'hot_season': '夏', 'hot_month_next': '９月'}
    link_dict = make_key_and_path_list(project_dir, dir_name, html_str, use_id_list, key_list)
    if not os.path.exists(project_dir + '/md_files/' + dir_name):
        os.mkdir(project_dir + '/md_files/' + dir_name)
    for key_id in use_id_list:
        keywords = key_list[key_id]
        keywords['id'] = str(key_id)
        if main_key:
            keywords.update(main_key_dict[main_key])
        keywords['page_name'] = html_str.replace('{}', keywords['eng'].replace('-', '_'))
        for add_key in add_key_dict:
            if add_key not in keywords or not keywords[add_key]:
                keywords[add_key] = np.random.choice(add_key_dict[add_key])
        if 'a_adj' not in keywords:
            if main_key == 'sex' and keywords['o_ms'] == 'm':
                keywords['a_adj'] = np.random.choice(['不倫', '浮気', 'NTR'])
            else:
                keywords['a_adj'] = np.random.choice(['安全に', '確実に', '簡単に', 'すぐに', '無料で'])
        keywords.update(hot_info)
        print(keywords)
        # make_keywords_sample(keywords)
        recipe_list = make_new_page(keywords, source_mod, art_map, project_dir, dir_name, key_list,
                                    keywords['page_name'], link_dict)
        recipe_dict[keywords['page_name']] = recipe_list
    # print(recipe_dict)


def make_key_and_path_list(project_dir, dir_name, html_str, use_id_list, key_list):
    pkl_path = '{}/pickle_pot/{}/key_and_path.pkl'.format(project_dir, dir_name)
    if os.path.exists(pkl_path):
        with open(pkl_path, 'rb') as p:
            pkl_data = pickle.load(p)
    else:
        pkl_data = []
    result = {'obj': [], 'sub': [], 'act': []}
    use_id_list.extend(pkl_data)
    use_id_list = list(set(use_id_list))
    for key_id in use_id_list:
        keywords = key_list[key_id]
        if keywords['type'] == 'only_obj':
            result['obj'].append([keywords['obj'], html_str.replace('{}', keywords['eng'].replace('-', '_'))])
    with open(pkl_path, 'wb') as k:
        pickle.dump(use_id_list, k)
    return result


def obj_source_changer():
    o_list = obj_source.obj_key_list
    result = {
        int(x['id']): {'obj_key': x['keyword'], 'obj': x['noun'], 'o_adj': x['adj'], 'obj_p': x['particle'],
                       'o_sex': 'w', 'o_reason': x['reason'], 'o_cat': x['t_cat'], 'o_ms': x['ms'],
                       'o_age': x['t_age'],
                       'o_look': x['look'], 'eng': x['eng'], 'type': 'only_obj', 'all_key': x['keyword']} for x in
        o_list}
    return result


def obj_source_filter(source_dict):
    return True
    # if source_dict['ms'] == 's':
    #     return True
    # else:
    #     return False


def make_new_page(keywords, source_mod, art_map, project_dir, dir_name, obj_list, html_head, link_dict):
    recipe_list = {}
    site_list = ['ワクワクメール', 'PCMAX']
    site1 = np.random.choice(['ワクワクメール', 'PCMAX'])
    site_list.remove(site1)
    if len(site_list) <= 1:
        site2 = site_list[0]
    else:
        site2 = np.random.choice(site_list.remove(site1))
    section_list = []
    used_list = []
    for section in art_map:
        if section[1] == 'straight':
            for s_code in section[0]:
                section_list.append(
                    np.random.choice([x for x in section[0][s_code] if ((x['info']['only'] and keywords['act_code']
                                                                         in x['info']['only']) or not x['info']['only'])
                                      and keywords['act_code'] not in x['info']['deny']]))
        else:
            if type(section[1]) == int:
                s_num = section[1]
            else:
                s_num = np.random.choice(section[1])
            sample_l = [x for x in section[0].keys() if x not in used_list]
            print(sample_l)
            if s_num == 1:
                t1 = [np.random.choice(sample_l)]
            else:
                np.random.shuffle(sample_l)
                t1 = sample_l[:s_num]
            print(t1)
            for t1e in t1:
                section_list.append(
                    np.random.choice([x for x in section[0][t1e] if ((x['info']['only'] and keywords['act_code']
                                                                      in x['info']['only']) or not x['info']['only'])
                                      and keywords['act_code'] not in x['info']['deny']]))
                used_list.append(t1e)
    # print(section_list)
    this_path = dir_name + '/' + keywords['page_name']
    result_str = ''
    key_phrase = key_phrase_maker(keywords)
    noun_dict = {'<!--{}-->'.format(y): [key_phrase[y]] for y in key_phrase}
    for noun in wd.noun_list:
        if 'plist' in noun:
            noun_dict[noun['before']] = [noun['after'], noun['plist']]
        else:
            noun_dict[noun['before']] = [noun['after']]
    conj_dict = {x['before']: x['after'] for x in wd.conj_list}
    title_str, t_recipe = make_new_title(source_mod.title[keywords['act_code']], noun_dict, conj_dict, site1, site2,
                                         link_dict, this_path)
    result_str += 't::' + title_str + '\n'
    print(title_str)
    des_str, d_recipe = make_new_title(source_mod.des[keywords['act_code']], noun_dict, conj_dict, site1, site2,
                                       link_dict, this_path)
    result_str += 'd::' + des_str.replace('\n', '') + '\n'
    result_str += 'n::' + str(keywords['id']) + '\n'
    result_str += 'e::\n'
    result_str += 'k::' + ' '.join([keywords['all_key'], keywords['act'].replace('する', '')]) + '\n'

    for this_sec in section_list:
        section_str, recipe = make_new_section(this_sec, noun_dict, conj_dict, site1, site2, link_dict, this_path)
        section_str = section_str.replace('%', '\n%')
        result_str += section_str + '\n\n'
        recipe_list[this_sec['info']['sec_name']] = recipe
    # if 'ins_link_' in result_str:
    #     result_str = result_str.replace('ins_link_', html_head + '_')
    result_str = replace_code_to_md(result_str)
    result_str = result_str.replace('\n\n- ', '\n\n%arlist%\n- ')
    result_str += 'recipe_list = ' + str(recipe_list) + '\n\n'
    result_str += 'use_keywords = ' + str(keywords)
    # print(result_str)
    with open(project_dir + '/md_files/' + dir_name + '/' + keywords['page_name'] + '.md', 'w', encoding='utf-8') as f:
        f.write(result_str)
    return recipe_list


def replace_code_to_md(md_str):
    replace_list = [['%rp', '%r_palm%\n'], ['%r?', '%r_?%\n'], ['%r!', '%r_!%\n'], ['%l!', '%l_!%\n']]
    for r_list in replace_list:
        md_str = md_str.replace(r_list[0], r_list[1])
    return md_str


def key_phrase_maker(keywords):
    if '作る' in keywords['act']:
        act_base = keywords['act']
        act_i = act_base.replace('を作る', 'にし')
        act_and = act_base.replace('作る', '作って')
        act_can = act_base.replace('作る', '作れ')
        act_can_d = act_base.replace('を作る', 'にでき')
        act_noun = keywords['act_noun']
        act_target = act_base.replace('を作る', '')
        act_with = keywords['obj_p']
        act_with_g = keywords['obj_p']
        act_with_d = 'を'
        act_way = act_noun + '<!--make-way-->'
        act_way_g = act_noun + '<!--make-way-g-->'
        obj = keywords['obj']
        obj_k = keywords['obj_key']
        obj_as_target = keywords['obj_key'] + keywords['obj_p'] + keywords['act_noun']
        connection = keywords['act_connection']
    else:
        act_base = keywords['act']
        act_i = act_base.replace('する', 'し')
        act_and = act_base.replace('する', 'して')
        act_can = act_base.replace('する', 'でき')
        act_can_d = act_base.replace('する', 'でき')
        act_noun = keywords['act_noun']
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
    act_adj = keywords['a_adj']
    if keywords['o_sex'] == 'w':
        target_person = '<!--women-{}-->'.format(keywords['o_age'])
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
    keys = {'k-how-to': [sub + 'が' + obj_k + act_with_g + act_way_g,
                         sub + 'が' + obj_adj + obj_k + act_with_g + act_way_g],
            'k-how-to-adj': [sub + 'が' + obj_adj + obj_k + act_with_g + act_way_g],
            'k-can': [sub + 'が' + obj_k + act_with + act_can + 'る'],
            'k-can-s': [sub + 'が' + obj_k + act_with + act_can + 'ます'],
            'k-do': [sub + 'が' + obj_k + act_with + act_base],
            'k-do-a': [sub + 'が' + obj_adj + obj_k + act_with + act_base],
            'k-easy': [sub + 'が' + obj + act_with_d + act_i + 'やすい'],
            'k-want': [sub + 'が' + obj + act_with_d + act_i + 'たい'],
            'k-find': [sub + 'が' + obj_k + 'の' + act_target + 'を探す'],
            'k-obj': [obj],
            'k-obj-adj': [obj_k + 'の'],
            'k-obj-status': [obj],
            'k-obj-noun': [obj_adj + obj, obj],
            'k-obj-noun-l': [obj_adj + obj],
            'k-obj-noun-s': [obj],
            'k-obj-noun-j': [obj_adj + obj, obj],
            'k-obj-target': [obj_as_target],
            'k-obj-want': [act_i + 'たい' + obj],
            'k-obj-wife': ['<!--wife-->の' + obj],
            'k-obj-act-find': [obj_as_target + 'を探す'],
            'k-obj-act-find-a': [obj_adj + obj_as_target + 'を探す'],
            'k-obj-act-can-find': [obj_as_target + 'が見つかる', obj_as_target + 'が探せる'],
            'k-obj-act-can-do': [obj_k + act_with + act_can + 'る'],
            'k-obj-act-can-do-a': [obj_adj + obj_k + act_with + act_can + 'る'],
            'k-obj-act-can-do-long': [obj_k + act_with + act_can + 'ます'],
            'k-obj-act-can-not-do': [obj_k + act_with + act_can + 'ない'],
            'k-obj-act-can-not-do-long': [obj_k + act_with + act_can + 'ません'],
            'k-obj-act-to-find': [obj_as_target + '探し'],
            'k-obj-act-to-find-a': [obj_adj + obj_as_target + '探し'],
            'k-obj-act-want': [obj + act_with_d + act_i + 'たい', obj + act_with_d + act_i + 'たい'],
            'k-obj-act-want-a': [obj_adj + obj + act_with_d + act_i + 'たい'],
            'k-obj-act-way': [obj_k + act_with + act_way, obj_k + act_with_g + act_way_g],
            'k-obj-act-do': [obj_k + act_with + act_base],
            'k-obj-act-do-a': [obj_adj + obj_k + act_with + act_base],
            'k-obj-act-easy': [obj + act_with_d + act_i + 'やすい'],
            'k-obj-act-find-easy': [act_can_d + 'る' + obj + 'を探しやすい', act_can_d + 'る' + obj + 'を見つけやすい'],
            'k-obj-act-can-meet': [obj_as_target + 'と出会える'],
            'k-obj-act-can-meet-a': [obj_adj + obj_as_target + 'と出会える'],
            'k-obj-act-noun': [obj_as_target],
            'k-obj-act-noun-a': [obj_adj + obj_as_target],
            'k-act': [act_base, act_adj + act_base],
            'k-act-adj': [act_adj + act_base],
            'k-act-adj-b': [act_adj],
            'k-act-i': [act_i],
            'k-act-and': [act_and],
            'k-act-want': [act_i + 'たい'],
            'k-act-can': [act_can + 'る', act_can_d + 'る'],
            'k-act-can-i': [act_can],  # セフレにでき（そう）,セックスでき(ない）
            'k-act-can-long': [act_can + 'ます'],
            'k-act-can-not-do': [act_can + 'ない'],
            'k-act-can-not-do-long': [act_can + 'ません'],
            'k-act-way': [act_way],
            'k-act-can-easy': [act_i + 'やすい', '<!--easily-->' + act_can + 'る'],
            'k-act-to-find': [act_target + '探し'],
            'k-act-find': [act_target + 'を探す'],
            'k-act-can-find': [act_target + 'を探せる'],
            'k-act-can-find-long': [act_target + 'を探せます'],
            'k-act-noun': [act_target],  # セックス、セフレを
            'k-act-noun-f': [act_noun],  # セフレを作る、彼女を作る等actが名詞と動詞でできているもの限定
            'k-act-v-can': ['でき'],  # でき（る）、作れ(る)
            'k-act-v-do': ['す'],  # す（る）、作(る)
            'k-act-v-i': ['す'],  # 探し（て）、作(って)
            'k-act-connection': connection,
            'k-sub': [sub],
            'k-sub-adj': [sub_adj + sub],
            'k-sub-want': [act_i + 'たい' + sub],
            'k-obj-category': [obj_cat1],
            'k-obj-category2': [obj_cat2],
            'k-2nd-act-noun': ['デート'],
            'k-2nd-act-want': [act_noun + 'にしたい'],
            'target-parson': [target_person],
            'reason': keywords['o_reason'],
            'act-with-d': [act_with_d]}
    if '作る' in keywords['act']:
        keys['k-want'].append(sub + 'が' + obj_k + 'の' + act_target + 'が欲しい')
        keys['k-obj-act-want'].append(obj_k + 'の' + act_target + 'が欲しい')
        keys['k-obj-act-want'].append(obj_adj + obj_k + 'の' + act_target + 'が欲しい')
        keys['k-obj-act-want'].append(obj_k + 'の' + act_target + 'を作りたい')
        keys['k-act-want'].append(act_target + 'が欲しい')
        keys['k-act-want'].append(act_target + 'を作りたい')
        keys['k-act-to-find'].append(act_target + '作り')
        keys['k-obj-act-to-find'].append(obj_as_target + '作り')
        keys['k-obj-act-can-not-do'].append(obj_k + act_with + act_can.replace('を', 'が') + 'ない')
        keys['k-act-can-not-do'].append(act_can.replace('を', 'が') + 'ない')
        if 'の女性' not in keywords['obj']:
            keys['k-how-to'].append(sub + 'が' + obj_k + act_way_g)
            keys['k-can'].append(sub + 'が' + obj_k + act_can + 'る')
            keys['k-can-s'].append(sub + 'が' + obj_k + act_can + 'ます')
            keys['k-do'].append(sub + 'が' + obj_k + act_base)
            keys['k-do-a'].append(sub + 'が' + obj_adj + obj_k + act_base)
            keys['k-find'].append(sub + 'が' + obj_k + act_noun + 'を探す')
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


def make_keywords_sample(keywords):
    r_str = ''
    keys = key_phrase_maker(keywords)
    for k in keys:
        r_str += '<!--{}-->  :  {}\n'.format(k, pprint.pformat(keys[k]))
        # print('<!--{}-->  :  {}'.format(k, keys[k]))
    # with open('key_sample.md', 'w', encoding='utf-8') as f:
    #     f.write(r_str)


def make_keywords_sample_dict(keywords):
    result_dict = {}
    new_dict = []
    keys = key_phrase_maker(keywords)
    anchor_dict = {y['before']: y['after'] for y in wd.noun_list}
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


def make_new_section(section_dict_p, noun_dict, conj_dict, site1, site2, link_dict, this_path):
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
            str_list, used_conj = insert_word_to_sentence(section_dict[sen_num][0], noun_dict, conj_dict, site1, site2,
                                                          str_list, used_conj, v_word, link_dict, this_path)
            recipe[sen_num] = 0
        else:
            choice_str = random.choice(section_dict[sen_num])
            str_list, used_conj = insert_word_to_sentence(choice_str, noun_dict, conj_dict, site1, site2,
                                                          str_list, used_conj, v_word, link_dict, this_path)
            recipe[sen_num] = section_dict[sen_num].index(choice_str)
    section_str = '\n'.join(str_list)
    return section_str, recipe


def make_new_title(section_list, noun_dict, conj_dict, site1, site2, obj_list, link_dict):
    str_list = []
    used_conj = []
    choice_str = random.choice(section_list)
    section_str, used_conj = insert_word_to_sentence(choice_str, noun_dict, conj_dict, site1, site2, str_list,
                                                     used_conj, [], obj_list, link_dict)
    recipe = {0: section_list.index(choice_str)}
    return section_str[0], recipe


def link_area_insert(sentence_str):
    used_list = []
    choice_list = random.choice([words_dict.pref_list, words_dict.city_list])
    while '<!--link-area-->' in sentence_str:
        select_str = random.choice(choice_list)
        if select_str in used_list:
            while select_str in used_list:
                select_str = random.choice(choice_list)
            used_list.append(select_str)
        sentence_str = sentence_str.replace('<!--link-area-->', select_str, 1)
    return sentence_str


def link_obj_word_insert(sentence_str, link_dict, this_path):
    used_list = []
    type_str_l = re.findall(r'<!--link-word-(.+?)-->', sentence_str)
    for type_str in type_str_l:
        select_str = random.choice(link_dict[type_str])
        print(select_str)
        print(link_dict[type_str])
        # print(used_list)
        if select_str[1] in used_list or select_str[1] == this_path:
            while select_str[1] in used_list or select_str[1] == this_path:
                select_str = random.choice(link_dict[type_str])
            used_list.append(select_str[1])
        sentence_str = sentence_str.replace('<!--link-word-{}-->'.format(type_str),
                                            '[{}]({}.md)'.format(select_str[0], select_str[1]), 1)
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
    return sentence_str


def insert_word_to_sentence(sentence_str, noun_dict, conj_dict, site1, site2, str_list, used_conj, v_word, link_dict,
                            this_path):
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
    if '<!--link-word-' in sentence_str:
        sentence_str = link_obj_word_insert(sentence_str, link_dict, this_path)
    if '<!--link-area-->' in sentence_str:
        sentence_str = link_area_insert(sentence_str)
    sentence_str = sentence_str.replace('<!--sefre-page-->', '')
    sentence_str = same_line_words_filter(sentence_str)
    while '<!--' in sentence_str:
        blank_list = re.findall(r'<!--.+?-->', sentence_str)
        # print(noun_dict)
        if blank_list:
            for blank in blank_list:
                # print(blank)
                if blank in noun_dict:
                    if len(noun_dict[blank]) <= 1:
                        sentence_str = sentence_str.replace(blank, random.choice(noun_dict[blank][0]), 1)
                    else:
                        sentence_str = sentence_str.replace(blank,
                                                            np.random.choice(noun_dict[blank][0],
                                                                             p=noun_dict[blank][1]), 1)
    for bad_w in words_dict.correct_dict:
        if bad_w in sentence_str:
            sentence_str = sentence_str.replace(bad_w, words_dict.correct_dict[bad_w])
    if '。' in sentence_str:
        sentence_str = re.sub(r'。(.+)$', r'。\n\1', sentence_str)
    str_list.append(sentence_str)
    return str_list, used_conj


def sf_import_to_source(import_list):
    main_str = ''
    list_name = ['title', 'des', 'int_1', 'point', 'di_1_1', 'di_1_2', 'da_1', 'da_2', 'da_3', 'da_4', 'da_5', 'da_6',
                 'da_7', 'da_8', 'da_9', 'da_10', 'da_11', 'da_12', 'tips_8', 'pa_1', 'pa_2', 'pa_3', 'pa_4', 'pa_5',
                 'pa_6', 'use_1', 'use_2', 'use_3', 'use_4', 'use_5', 'use_6', 'use_7', 'tips_1', 'tips_2', 'tips_3',
                 'tips_4', 'tips_5', 'tips_6', 'tips_7', 'cnc_1']
    for o_list, l_name in zip(import_list, list_name):
        new_dict = {'info': {'deny': [], 'only': [], 'shuffle': []}}
        index_num = 0
        print(o_list)
        for row in o_list:
            new_dict[index_num] = row
            index_num += 1
        main_str += '{} = {}\n# {}/end\n\n'.format(l_name, pprint.pformat(new_dict), l_name)
    print(main_str)
    main_str.split('\n')
    with open('list_test.py', 'w', encoding='utf-8') as f:
        f.write(main_str)


if __name__ == '__main__':
    # test_new_section(source_data.all_list, keywords_p)
    # sf_import_to_source()

    # make_keywords_sample(keywords_p)
    t_key_list = key_source.keyword_dict
    make_new_pages_to_md_from_key_list('test', 'make_love_o', 'sex_{}_f', source_data, 'sex',
                                       list(range(0, 208, 1)), t_key_list)

    # pprint.pprint(obj_source_changer(), width=150)

    # k_p = {
    #     's_adj': '普通の', 'sub': '男性',
    #     'o_adj': '淫乱な', 'obj': '巨乳女性', 'obj_key': '巨乳', 'obj_p': 'の',
    #     'act_adj': '安全に', 'act': 'セフレを作る', 'act_noun': 'セフレ', 'act_noun_flag': True,
    #     'act_connection': ['セフレ関係'],
    #     'o_reason': '',
    #     't_sex': 'm', 't_age': 'n', 't_cat': 'j', 'act_code': 'gf'}
    # pprint.pprint(make_keywords_sample_dict(k_p))
