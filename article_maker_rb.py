# -*- coding: utf-8 -*-

import random
import numpy as np
import re
import copy
import io
import os
import datetime
import pickle
from ftplib import FTP
from html.parser import HTMLParser
# 以下、データ
from word_list_rb_sf import word_list
from word_list_rb_sf import word_list_fix
from word_list_rb_sf import o_other
from word_list_rb_sf import conjunction_list
from word_list_rb_sf import actress_list
from word_list_rb_sf import sexy_actress_list
from word_list_rb_sf import area_link_list
from word_list_rb_sf import keyword_dec_list
from word_list_rb_sf import site_list
from word_list_rb_sf import point_tag
from word_list_rb_sf import wp_tag
from word_list_rb_sf import wp_update_list
from word_list_rb_sf import atom_rss
from word_list_rb_sf import one_rss
from word_list_rb_sf import two_rss
from word_list_rb_sf import random_adj_list

from template_rb_sex import rb_sex_template

from dup_list import dup_list_full


key_list = ["st", "ch", "sc", "sh", "ps", "ps-s", "ps-p", "look", "age-o", "h2", "h3"]
illegal_id = ['199', '200', '201', '223']


def main(sentence_list_b, keyword_list, start, stop):
    c_list = []
    file_list = {}
    rss_list = []
    old_time_list = get_timestamp('files_sf')
    template_path = 'file_other/sex1.html'
    # this_date = datetime.datetime(2019, 4, 25, 18, 00, 00)
    at_one_day = 208
    # interval = 1
    # day_counter = 0
    timestamp_m = str(datetime.datetime.now().isoformat())[:-7] + '+09:00'
    # timestamp_m = '2019-05-18T11:54:34+09:00'
    with open(template_path, mode='r', encoding='utf-8') as f:
        template_file = f.read()
    for key in keyword_list[start:stop]:
        print(key["keyword"])
        dup_l = dup_list_maker(key)
        if at_one_day >= stop - start:
            stop_num = stop
        else:
            stop_num = int(key['id'])
        sentence_list = copy.deepcopy(sentence_list_b)
        title_choice(sentence_list, key)
        list_a = sentence_choice(sentence_list, key, dup_l)
        list_b = list_pop(list_a)
        while 'st' in list_b:
            list_b.remove('st')
        while 'nodata' in list_b:
            list_b.remove('nodata')
        # print(list_b)
        while [] in list_b:
            list_b.remove([])
        # print(list_b)
        result_a = ''.join(list_b)
        if key['id'] in illegal_id:
            print('illegal')
            result_a = illegal_key_checker(result_a, key, dup_list_full, sentence_list)
        result_a = first_insert(result_a, sentence_list['insert_f'], '<!--insert-first-a-->')
        result_a = paragraph_insert(result_a, key, dup_l, sentence_list)
        result_a = result_a.replace("nodata", "")
        result = tag_maker(result_a)
        result = word_insert(result, key, keyword_list, stop_num)
        if 'っぽい<!--woman-y-->' in key['keyword']:
            data_keyword = key['keyword'].replace('っぽい<!--woman-y-->', '')
        else:
            data_keyword = key['keyword']
        result = result + '<!--data#key#' + data_keyword + '#' + key['id'] + '#-->'
        result = html_maker(result, key)
        # タイムスタンプ挿入
        # result, this_date, day_counter = timestamp_insert(result, at_one_day, interval, this_date, day_counter)
        result = section_insert(result)
        result = index_maker(result)
        result = wp_checker(result, key)
        c_list.append(num_code_pickup(result, key['eng']))
        result = re.sub(r'<!--\|.*?\|-->', '', result)
        result = result.replace('<br></p>', '</p>')
        file_name = 'sex-' + str(key['eng']) + '.html'
        if int(key['id']) >= 0:
            file_list[file_name] = re.findall(r'<h1>(.*?)</h1>', result)[0]
        main_text = re.findall(r'<main>.{500}', result)[0]
        if file_name in old_time_list:
            timestamp_p = str(old_time_list[file_name])
        else:
            timestamp_p = timestamp_m
        jap_timestamp_p = jap_timestamp_maker(timestamp_p)
        jap_timestamp_m = jap_timestamp_maker(timestamp_m)
        result = html_insert(template_file, result)
        result = result.replace('<!--is-pub-j-->', jap_timestamp_p)
        result = result.replace('<!--is-pub-e-->', timestamp_p)
        result = result.replace('<!--is-mod-j-->', jap_timestamp_m)
        result = result.replace('<!--is-mod-e-->', timestamp_m)
        make_file(file_name, result)
        r_title = re.findall(r'<title>(.*?)</title>', result)[0]
        r_summary = re.findall(r'<meta name="description" content="(.*?)">', result)[0]
        r_content = MyHtmlStripper(main_text).value[:300]
        rss_key = str(key['keyword'].replace('っぽい<!--woman-y-->', '')) + ' セックス'
        rss_data = [file_name, r_title, r_summary, r_content, timestamp_p, timestamp_m, rss_key]
        rss_list.append(rss_data)
    c_list.append(timestamp_m)
    save_pickle(c_list, 'rb_make_love', 'files_sf', timestamp_m)
    html_sitemap_maker(file_list)
    xml_sitemap_maker(file_list, timestamp_m)
    # make_rss(rss_list)  # RSS新規作成の場合
    add_rss(rss_list)  # RSS追記の場合
    relational_article('/Users/nakataketetsuhiko/PycharmProjects/reibun_sf/files_sf', timestamp_m)
    amp_file_maker('files_sf')


def save_pickle(data_list, file_name, directory, pub_time):
    p_time = pub_time.replace('-', '')
    p_time = p_time.replace('+09:00', '')
    p_time = p_time.replace(':', '')
    file_name_u = file_name + p_time
    with open(directory + '/' + file_name_u + '.pkl', 'wb') as p:
        pickle.dump(data_list, p)


def html_insert(template, long_str):
    insert_key = ['title', 'meta', 'h1', 'amp', 'main']
    for key in insert_key:
        insert_str = re.findall('<' + str(key) + '>(.*?)</' + str(key) + '>', long_str)[0]
        template = template.replace('<!--is-' + str(key) + '-->', insert_str)
    return template


def get_timestamp(directory):
    time_dec = {}
    dir_list = os.listdir(directory)
    for old_file in dir_list:
        if '.html' in old_file:
            with open(directory + '/' + old_file, "r", encoding='utf-8') as f:
                file_str = f.read()
                pub_date = re.findall(r'<time itemprop="datePublished"\s+datetime="(.*?)">.*?</time>', file_str)[0]
            time_dec[old_file] = pub_date
    return time_dec


def wp_checker(long_str, keyword):
    for x in wp_update_list:
        if x['link'] == keyword['eng']:
            if 'image' in x:
                print('image置換' + str(keyword['eng']))
                long_str = re.sub('<!--top-img-.*?-->', x['img'], long_str)
            if 'title' in x:
                print('タイトル置換' + str(keyword['eng']))
                long_str = re.sub('<title>.*?</title>', '<title>' + x['title'] + '</title>', long_str)
                long_str = re.sub('<h1>.*?</h1>', '<h1>' + x['title'] + '</h1>', long_str)
    return long_str


def title_choice(sentence_list, key_dec):
    five_word = key_dec['kyoki'][:5]
    if "セックス" in five_word:
        title_list = sentence_list[0][1][1:6]
    else:
        title_list = sentence_list[0][1][6:]
    title = random.choice(title_list)
    sentence_list[0][1] = title
    return sentence_list


def make_file(f_name, text):
    path_w = 'files_sf/' + f_name
    with open(path_w, mode='w') as f:
        f.write(text)


def make_file_d(directory, f_name, text):
    path_w = directory + '/' + f_name
    with open(path_w, mode='w') as f:
        f.write(text)


def make_list_file(text):
    now = datetime.datetime.now()
    path_w = 'files_sf_code/c' + str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '-' + str(now.hour)\
             + '-' + str(now.minute) + '.txt'
    with open(path_w, mode='w') as f:
        f.write(text)


def first_insert(main_str, insert_list, insert_str):
    insert_obj = random.choice(insert_list)
    main_str = main_str.replace(insert_str, insert_obj, 1)
    main_str = main_str.replace(insert_str, '')
    return main_str


def paragraph_insert(main_str, key, dup_list, template):
    # insert_list = [make_insert_para(template['second_key'], dup_list)]
    insert_list = [insert_para_maker(template['second_key'], key, dup_list)]
    count_num = main_str.count("<!--insert-para-->")
    insert_para_list_c = copy.deepcopy(template['insert_para'])
    if key['ps'] is "s":
        insert_para_list_c.append(template['ps_s'])
    while len(insert_list) < count_num:
        # print(insert_para_list_c)
        insert_object = random.choice(insert_para_list_c)
        insert_para_list_c.remove(insert_object)
        insert_str = insert_para_maker(insert_object, key, dup_list)
        insert_list.append(insert_str)
    random.shuffle(insert_list)
    for y in insert_list:
        main_str = main_str.replace("<!--insert-para-->", y, 1)
    return main_str


def insert_para_maker(list_p, key_d, dup_list):
    choice_list = sentence_choice(list_p, key_d, dup_list)
    choice_list = list_pop(choice_list)
    p_str = ''.join(choice_list)
    return p_str


def make_insert_para(list_a, dup_list):
    result = ''
    pop_data = list_a[0]
    if pop_data == 'ch':
        del list_a[0]
        insert_sentence = random.choice(duplication_checker(list_a, dup_list))
        result += insert_sentence
    elif pop_data == 'h2':
        del list_a[0]
        result = '<h2>' + duplication_checker(list_a, dup_list) + '</h2>'
    elif pop_data == 'h3':
        del list_a[0]
        result = '<h3>' + duplication_checker(list_a, dup_list) + '</h3>'
    return result


def dup_list_maker(key_dec):
    result = []
    for x in dup_list_full:
        if key_dec['eng'] is x[0]:
            result = x
            break
    return result


def duplication_checker(str_list, dup_list):
    for x in str_list:
        if isinstance(x, list):
            return str_list
    for x in str_list:
        if len(str_list) > 1:
            code_nums = re.findall(r'<!--\|(.*?)\|-->', x)
            if code_nums:
                if code_nums[0] in dup_list:
                    str_list.remove(x)
    return str_list


def sentence_choice(sentence_list, keyword_dic, dup_list):
    """
    再帰的に文をシャッフルやチョイス、複数選択する
    :param sentence_list: 記事要素のリスト
    :param keyword_dic: キーワードの辞書
    :param dup_list: 既存の記事の文配列
    :return: 順番を整えられたリスト
    """
    # print(type(sentence_list))
    result = []
    list_lc1 = []
    if isinstance(sentence_list, list):
        pop_data = sentence_list[0]
        # print('配列先頭')
        # print(pop_data)
        if pop_data == 'ch':
            # print("ここはch")
            del sentence_list[0]
            # print(sentence_list)
            result = random.choice(duplication_checker(sentence_list, dup_list))
            # print("new_data")
            # print(result)
        elif pop_data == 'sh':
            del sentence_list[0]
            random.shuffle(sentence_list)
            result = sentence_list
            # print("new_data")
            # print(result)
        elif pop_data == 'sc':
            del sentence_list[0]
            choice_and_shuffle(sentence_list)
            result = sentence_list
            # print("new_data")
            # print(result)
        elif pop_data == 'st':
            del sentence_list[0]
            result = sentence_list
            # print("new_data")
            # print(result)
        elif pop_data == 'h2':
            del sentence_list[0]
            # print(sentence_list)
            result = '<h2>' + random.choice(duplication_checker(sentence_list, dup_list)) + '</h2>'
        elif pop_data == 'h3':
            del sentence_list[0]
            # print(sentence_list)
            result = '<h3>' + random.choice(duplication_checker(sentence_list, dup_list)) + '</h3>'
        elif pop_data == 'ja':
            del sentence_list[0]
            if keyword_dic['jaf'] == 'j':
                result = sentence_list[1]
            elif keyword_dic['jaf'] == 'a':
                result = sentence_list[2]
            elif keyword_dic['jaf'] == 'f':
                result = sentence_list[0]
        elif pop_data == 'ps':
            del sentence_list[0]
            if keyword_dic['ps'] == 'p':
                result = sentence_list[0]
            elif keyword_dic['ps'] == 's':
                result = sentence_list[1]
        elif pop_data == 'age-o':
            del sentence_list[0]
            if keyword_dic['age'] != 'y':
                result = sentence_list[0]
            else:
                result = ""
        elif pop_data == 'ps-s':
            del sentence_list[0]
            if keyword_dic['ps'] != 'p':
                result = sentence_list[0]
            else:
                result = ""
        elif pop_data == 'ps-p':
            del sentence_list[0]
            if keyword_dic['ps'] != 's':
                result = sentence_list[0]
            else:
                result = ""
        elif pop_data == 'look':
            del sentence_list[0]
            if not keyword_dic['look']:
                result = sentence_list[0]
            else:
                result = ""
        elif pop_data == 'lc1':
            del sentence_list[0]
            result = link_choice_maker(sentence_list, list_lc1, keyword_dic, dup_list)
            print('lc1: ' + str(result))
        else:
            result = sentence_list
        if isinstance(result, list):
            if result[0] in key_list:
                result = sentence_choice(result, keyword_dic, dup_list)
            else:
                result_list = []
                for x in result:
                    x_e = sentence_choice(x, keyword_dic, dup_list)
                    result_list.append(x_e)
                    # print("result_list")
                    # print(result_list)
                    result = result_list
    else:
        result = sentence_list
    # print("answer")
    # print(result)
    return result


def link_choice_maker(s_dic, lc_list, key, dup_list):
    """
    s_dic = ['lc1', {1: [.....], 2: [.....], 3: [....]}]
    :param s_dic: lc1で始めるリスト内の辞書部分
    :param lc_list:　順序を格納するリスト
    :param key:　選ばれたキーワード
    :param dup_list:　重複リスト
    :return:　選択・整列された記事リストと順序のリスト
    """
    result_list = []
    if not lc_list:
        n = len(s_dic)
        if n >= 7:
            s_num = [n, n - 1, n - 2]
        elif 7 > n >= 4:
            s_num = [n, n - 1]
        else:
            s_num = [n]
        c_num = random.choice(s_num)
        keys = s_dic.keys()
        lc_list = random.sample(keys, c_num)
    else:
        pass
    for key in lc_list:
        result_list.append(s_dic[key])
    result = sentence_choice(result_list, key, dup_list)
    return result, lc_list


def choice_and_shuffle(sentence_list):
    x = len(sentence_list)
    cut_list = [[0], [0], [0], [0, 1], [1, 2], [2, 3], [2, 3], [3, 4]]
    y = random.choice(cut_list[x])
    # print(y)
    random.shuffle(sentence_list)
    for i in range(0, y):
        z = random.choice(sentence_list)
        sentence_list.remove(z)
    return sentence_list


def list_pop(sentence_list):
    # print('扱う配列')
    # print(sentence_list)

    for i in range(len(sentence_list)):
        # print(i)
        # print('要素')
        if sentence_list[i]:
            # print(sentence_list[i])
            if isinstance(sentence_list[i], list):
                # print(sentence_list)
                sentence_list[i:i + 1] = list_pop(sentence_list[i])
    for j in range(len(sentence_list)):
        if sentence_list[j]:
            if isinstance(sentence_list[j], list):
                # print(sentence_list)
                list_pop(sentence_list)
    return sentence_list


def tag_maker(sentence_list):
    sentence_list = sentence_list.replace("nodata", "")
    sentence_list = sentence_list.replace("。", "。<br>")
    sentence_list = sentence_list.replace("<p></p>", "")
    sentence_list = sentence_list.replace("<br></p>", "</p>")
    sentence_list = sentence_list.replace("<br><h2>", "</p><h2>")
    sentence_list = sentence_list.replace("<br><h3>", "</p><h3>")
    return sentence_list


# 以下、文字列挿入

def word_insert(long_str, keyword_dec, keyword_list, stop_num):
    """
    文字列にキーワードや接続詞、表記揺れなどを挿入する
    :param long_str: 置換される文字列
    :param keyword_dec: キーワードの辞書部分
    :param keyword_list: キーワードのリスト
    :param stop_num: キーリストの上限
    :return: 置換されて完成した文字列
    """
    # ミュータブルなリストのコピー
    kw_list = copy.deepcopy(keyword_list)
    # キーワードリストの調整
    kw_list = kw_list[:stop_num]
    for key_p in kw_list:
        if key_p['id'] in illegal_id:
            kw_list.remove(key_p)
    atl = copy.deepcopy(actress_list)
    sal = copy.deepcopy(sexy_actress_list)
    allist = copy.deepcopy(area_link_list)
    stl = copy.deepcopy(site_list)
    # キーワードの挿入
    # print("メインキー挿入後: " + str(len(kw_list)))
    long_str = long_str.replace('<!--keyword-->', keyword_dec['keyword'])
    long_str = long_str.replace('<!--keyword-h-->', keyword_dec['noun'])
    long_key = keyword_dec['adj'] + keyword_dec['noun']
    long_key_list = [long_key, keyword_dec['noun']]
    long_str = re.sub(r'<title>(.*?)<!--keyword-l-->(.*?)</title>', r'<title>\1' + long_key + r'\2</title>', long_str)
    adj_key = keyword_dec['keyword'] + keyword_dec['particle']
    long_str = long_str.replace('<!--keyword-adj-->', adj_key)
    while '<!--keyword-l-->' in long_str:
        long_str = long_str.replace('<!--keyword-l-->', random.choice(long_key_list))
    if keyword_dec['id'] in illegal_id:
        search_str = re.findall(r'<title>.*?<!--il-insert-->', long_str)[0]
        replace_str = search_str.replace('っぽい<!--woman-y-->', '')
        long_str = long_str.replace(search_str, replace_str)
    long_str = long_str.replace('<!--il-insert-->', '')
    long_str = long_str.replace('<!--il-insert-e-->', '')
    # ランダム形容詞の挿入
    if '<!--random-adj-->' in long_str:
        rdm_adj_list = copy.deepcopy(random_adj_list)
        if keyword_dec['rdm_adj']:
            for x in keyword_dec['rdm_adj']:
                del rdm_adj_list[x]
        long_str = long_str.replace('<!--random-adj-->', random.choice(rdm_adj_list))
    # キーワード2の挿入
    keyword_sec = random.choice(kw_list)
    kw_list.remove(keyword_sec)
    # print("サブキー挿入後: " + str(len(kw_list)))
    long_str = long_str.replace('<!--keyword2-->', keyword_sec['keyword'])
    long_str = long_str.replace('<!--keyword2-h-->', keyword_sec['noun'])
    # おすすめサイトの挿入
    site_one = random.choice(stl)
    stl.remove(site_one)
    long_str = long_str.replace('<!--site-1-->', site_one['word'])
    long_str = long_str.replace('<!--site-1-l-->', '<a href="' + site_one['path'] + '">' + site_one['word'] + '</a>')
    site_sec = random.choice(stl)
    stl.remove(site_sec)
    long_str = long_str.replace('<!--site-2-->', site_sec['word'])
    long_str = long_str.replace('<!--site-2-l-->', '<a href="' + site_sec['path'] + '">' + site_sec['word'] + '</a>')
    # 一般名詞のランダム挿入
    for dec in word_list:
        if 'plist' in dec:
            long_str = p_word_choice(long_str, dec['before'], dec['after'], dec['plist'])
        else:
            long_str = word_random_choice(long_str, dec['before'], dec['after'])
    # 一般名詞の選択挿入
    long_str = select_word_insert(long_str, keyword_dec)
    # 固有名詞のランダム挿入
    while '<!--actress-->' in long_str:
        actress_name = random.choice(atl)
        atl.remove(actress_name)
        long_str = long_str.replace('<!--actress-->', actress_name + 'さん', 1)
    while '<!--AV-act-->' in long_str:
        sexy_actress_name = random.choice(sal)
        sal.remove(sexy_actress_name)
        long_str = long_str.replace('<!--AV-act-->', sexy_actress_name + 'さん', 1)
    # 他のページにリンクするキーワードの挿入
    while '<!--link-word-->' in long_str:
        link_word = random.choice(kw_list)
        kw_list.remove(link_word)
        # print("リンクワード挿入後: " + str(len(kw_list)))
        keyword_tag = '<a href="sex-' + link_word['eng'] + '.html">' + link_word['noun'] + '</a>'
        long_str = long_str.replace('<!--link-word-->', keyword_tag, 1)
    while '<!--link-area-->' in long_str:
        link_area = random.choice(allist)
        allist.remove(link_area)
        area_tag = '<a href="../fuck-buddy/prf' + str(link_area['id']).zfill(2) + '-' + link_area['alpha'] + '.html">'\
                   + link_area['ari']\
                   + '</a>'
        long_str = long_str.replace('<!--link-area-->', area_tag, 1)
    while '<!--site-link-->' in long_str:
        link_site = random.choice(stl)
        stl.remove(link_site)
        long_str = long_str.replace('<!--site-link-->', link_site, 1)
    for site_s in site_list:
        long_str = first_txt_linker(long_str, site_s['word'], site_s['path'])
    # 接続詞の挿入
    long_str = conjunction_insert(long_str)
    # 共起語の挿入
    k_list = copy.deepcopy(keyword_dec['kyoki'])
    for k_word in k_list:
        if k_word in long_str:
            k_list.remove(k_word)
    while '<!--kyoki-->' in long_str:
        for k_word in k_list:
            long_str = long_str.replace('<!--kyoki-->', k_word, 1)
        if not k_list:
            k_list = copy.deepcopy(keyword_dec['kyoki'])

    # 選択文字列の挿入
    long_str = choice_from_str(long_str)
    long_str = long_str.replace('<!--reason-->', keyword_dec['reason'])
    long_str = page_point_insert(long_str)
    return long_str


def illegal_para_maker(key, dup_list, template):
    keyword_il = key['keyword'].replace('っぽい', '')
    i_para_1 = insert_para_maker(template['illegal'][0], key, dup_list)
    i_para_1 = i_para_1.replace('<!--keyword-il-->', keyword_il)
    i_para_2 = insert_para_maker(template['illegal'][1], key, dup_list)
    i_para_2 = i_para_2.replace('<!--keyword-il-->', keyword_il)
    return i_para_1, i_para_2


def illegal_key_checker(long_str, key, dup_list, template):
    il_para_1, il_para_2 = illegal_para_maker(key, dup_list, template)
    long_str = re.sub(r'<!--il-insert-->.*<!--il-insert-e-->', '<!--il-insert-->' + str(il_para_1), long_str)
    long_str = long_str.replace('<point2>', str(il_para_2) + '<point2>')
    return long_str


def select_word_insert(long_str, keyword_dec_s):
    for dec_f in word_list_fix:
        insert_words = []
        # print(dec_f)
        for f_word in dec_f['after']:
            if f_word in keyword_dec_s['kyoki']:
                insert_words.append(f_word)
        if insert_words:
            long_str = long_str.replace(dec_f['before'], random.choice(insert_words))
        else:
            if 'plist' in dec_f:
                long_str = long_str.replace(dec_f['before'], np.random.choice(dec_f['after'], p=dec_f['plist']))
            else:
                long_str = long_str.replace(dec_f['before'], random.choice(dec_f['after']))
    return long_str


def jap_timestamp_maker(timestamp):
    time_data = re.findall(r'(\d{4})-(\d{2})-(\d{2})', timestamp)
    jap_time = str(time_data[0][0]) + '年' + str(time_data[0][1]) + '月' + str(time_data[0][2]) + '日'
    return jap_time


def html_maker(long_str, key_dec):
    for i in range(long_str.count('</h2><p>')):
        long_str = long_str.replace("</h2><p>", "</h2><!--image-rb" + str(key_dec['id']) + '-' + str(i)
                                    + "--><p>", 1)
    amp_tag = '<amp><link rel="amphtml" href="https://www.demr.jp/amp/make-love/sex-' + key_dec['eng'] + '.html"></amp>'
    meta_str = re.findall(r'<meta>.*?</meta>', long_str)
    meta_str_i = meta_str[0].replace('<br>', '')
    long_str = re.sub(r'<meta>.*?</meta>', meta_str_i, long_str)
    title_str = re.findall(r'<title>(.*?)</title>', long_str)
    long_str = long_str.replace('</title><meta>', '|出会い系メール例文集</title><meta>')
    head_str = '</meta>' + amp_tag + '<h1>' + title_str[0] + '</h1><main><!--top-img-'\
               + key_dec['id'] + '-->'
    long_str = long_str.replace('</meta>', head_str)
    footer = '<!--last-section--></main>'
    long_str = long_str + footer
    long_str = long_str.replace('<sfd1>', '<span class="hutoaka">')
    long_str = long_str.replace('</sfd1>', '</span>')
    long_str = long_str.replace('<sfd2>', '<span class="hutokuro">')
    long_str = long_str.replace('</sfd2>', '</span>')
    long_str = long_str.replace('</point>', '</point><!--p-index-->', 1)
    long_str = long_str.replace('<point>', point_tag)
    long_str = long_str.replace('</point>', '</ul></div>')
    point_tag_s = point_tag.replace("この記事のポイント", "この記事のまとめ")
    point_tag_s = point_tag_s.replace('id="kijip"', 'id="kijim"')
    long_str = long_str.replace('<point2>', point_tag_s)
    long_str = long_str.replace('<br></li>', '</li>')
    long_str = re.sub(r'(</h2>)<span', '</h2><p>', long_str)
    long_str = re.sub(r'href=#(.*?)#>', r'href="\1">', long_str)
    return long_str


def first_txt_linker(long_str, word_str, link_url):
    insert_str = '<a href="' + link_url + '">' + word_str + '</a>'
    match_str = re.findall(r'</h[2|3]>.*?' + word_str, long_str)
    for x in match_str:
        y = x.replace(word_str, insert_str)
        long_str = long_str.replace(x, y, 1)
    long_str = re.sub(r'<a href="url.*?"><a href="url(.*?)">(.*?)</a></a>', '<a href="\\1">\\2</a>', long_str)
    return long_str


def page_point_insert(long_str):
    match_str = re.findall(r'<!--point-sec-->(.*?)<!--/point-sec-->', long_str)
    if match_str:
        long_str = long_str.replace('<!--point-sec-insert-->', match_str[0])
    long_str = long_str.replace("<!--point-sec-->", "")
    long_str = long_str.replace("<!--/point-sec-->", "")
    return long_str


def word_random_choice(div_str, str_pattern, str_word):
    """
    段落の文中のキーワードをランダムに挿入
    :param div_str: 文字列
    :param str_pattern: 置換する目標
    :param str_word: 置換する文字列のリスト
    :return: 置換された文字列
    """
    div_str_c = div_str
    while str_pattern in div_str_c:
        div_str_c = div_str_c.replace(str_pattern, random.choice(str_word), 1)
    return div_str_c


def p_word_choice(div_str, str_pattern, str_word, p_list):
    while str_pattern in div_str:
        # print(str_pattern)
        div_str = div_str.replace(str_pattern, np.random.choice(str_word, p=p_list), 1)
    return div_str


def conjunction_insert(long_str):
    """
    接続詞を挿入
    :param long_str: 置換される文字列
    :return: 置換された文字列
    """
    long_str = long_str.replace('</h2><!--but-->', '')
    long_str = long_str.replace('</h3><!--but-->', '')
    # one,the other表現の挿入
    sub_txt = r'\1' + random.choice(o_other) + r'\2'
    long_str = re.sub(r'<!--one-other1e-->(.*?)<!--one-other1-->(.*?)<!--one-other1e-->', sub_txt, long_str)
    long_str = long_str.replace('<!--one-other1-->', '')
    long_str = long_str.replace('<!--one-other1e-->', '')
    # 接続詞のランダム挿入
    for dec in conjunction_list:
        insert_word_b = ""
        if 'plist' in dec:
            while dec['before'] in long_str:
                insert_word = np.random.choice(dec['after'], p=dec['plist'])
                if insert_word_b != insert_word:
                    pass
                else:
                    if insert_word != dec['after'][0]:
                        insert_word = dec['after'][0]
                    else:
                        insert_word = dec['after'][1]
                long_str = long_str.replace(dec['before'], insert_word + '、', 1)
                insert_word_b = insert_word
        else:
            while dec['before'] in long_str:
                insert_word = random.choice(dec['after'])
                if insert_word_b != insert_word:
                    pass
                else:
                    if insert_word != dec['after'][0]:
                        insert_word = dec['after'][0]
                    else:
                        insert_word = dec['after'][1]
                long_str = long_str.replace(dec['before'], insert_word + '、', 1)
                insert_word_b = insert_word
    return long_str


def choice_from_str(long_str):
    match_list = re.findall(r'<!--ya#.*?#ya-->', long_str)
    for match_str in match_list:
        # print(match_str)
        choice_word_list_b = re.findall(r'(.*?)#', match_str)
        num_w = choice_word_list_b[1]
        choice_word_list = copy.deepcopy(choice_word_list_b)
        insert_words = choice_word_list[2:]
        ins_list = random.sample(insert_words, int(num_w))
        # for i in range(int(num_w)):
        #    ins_list.append(random.choice(insert_words))
        f_word = ins_list[0]
        if num_w != '1':
            f_word = f_word + 'や' + '、'.join(ins_list[1:])
        long_str = long_str.replace(match_str, f_word, 1)
    return long_str


def section_insert(long_str):
    h_tag_outer = re.findall(r'<h[2|3]>.*?</h[2|3]>', long_str)
    h_tag_outer.reverse()
    insert_list = []
    for i in range(len(h_tag_outer) - 1):
        if '<h2>' in h_tag_outer[i]:
            if '<h2>' in h_tag_outer[i + 1]:
                insert_list.append('</section><section>' + h_tag_outer[i])
            elif '<h3>' in h_tag_outer[i + 1]:
                insert_list.append('</section></section><section>' + h_tag_outer[i])
        elif '<h3>' in h_tag_outer[i]:
            if '<h2>' in h_tag_outer[i + 1]:
                insert_list.append('<section>' + h_tag_outer[i])
            elif '<h3>' in h_tag_outer[i + 1]:
                insert_list.append('</section><section>' + h_tag_outer[i])
    insert_list.append('<section>' + h_tag_outer[-1])
    insert_list.reverse()
    h_tag_outer.reverse()
    for j in range(len(h_tag_outer)):
        long_str = long_str.replace(h_tag_outer[j], insert_list[j])
    if '<h2>' in h_tag_outer[-1]:
        long_str = long_str.replace('<!--last-section-->', '</section>')
    elif '<h3>' in h_tag_outer[-1]:
        long_str = long_str.replace('<!--last-section-->', '</section></section>')
    return long_str


def num_code_pickup(long_str, key_eng):
    match_list = re.findall(r"<!--\|(.*?)\|-->", long_str)
    match_list.insert(0, key_eng)
    return match_list


# 目次作成
def index_maker(long_str):
    list_p = make_list(long_str)
    str_p = index_str(list_p)
    str_a = anchor_insert(long_str)
    result = str_a.replace('<!--p-index-->', str_p, 1)
    return result


def index_str(index_list):
    work_list = index_list
    work_str = ''.join(work_list)
    ex_list = [{'h_tag': '</h2><h2>', 'li_tag': '</a></li><li><a href="#sc¥num¥">'},
               {'h_tag': '</h3><h3>', 'li_tag': '</a></li><li><a href="#sc¥num¥">'},
               {'h_tag': '</h2><h3>', 'li_tag': '</a><ol><li><a href="#sc¥num¥">'},
               {'h_tag': '</h3><h2>', 'li_tag': '</a></li></ol></li><li><a href="#sc¥num¥">'},
               {'h_tag': r'</h2>$', 'li_tag': '</a></li></ol>'},
               {'h_tag': r'</h3>$', 'li_tag': '</a></li></ol></li></ol>'},
               {'h_tag': r'^<h2>', 'li_tag': '<ol><li><a href="#sc¥num¥">'},
               {'h_tag': r'^<h3>', 'li_tag': '<ol><li><ol><li><a href="#sc¥num¥">'}]
    for ex in ex_list:
        work_str = re.sub(ex['h_tag'], ex['li_tag'], work_str)
    i = 1
    while '¥num¥' in work_str:
        work_str = work_str.replace('¥num¥', str(i), 1)
        i += 1
    work_str = '<div id="mokujio"><nav id="mokuji"><div class="moh">目次 <span class="small">' \
               '[<label for="label1">表示切替</label>]</span></div><input type="checkbox" id="label1"/>' \
               '<div class="hidden_show">' + work_str + '</div></nav></div>'
    return work_str


def anchor_insert(str_a):
    str_w = re.sub(r'(<h[23]>)(.*?)(</h[23]>)', r'\1<span id="sc¥num_i¥">\2</span>\3', str_a)
    if '関連記事' in str_w:
        str_w = str_w.replace('<h2><span id="sc¥num_i¥">関連記事</span></h2>', '<h2>関連記事</h2>')
    i = 1
    while '¥num_i¥' in str_w:
        str_w = str_w.replace('¥num_i¥', str(i), 1)
        i += 1
    return str_w


def make_list(input_file):
    matched_list = re.findall(r'<h[23]>.*?</h[23]>', input_file)
    # matched_list.remove('<h2>関連記事</h2>')
    result = []
    for x in matched_list:
        x = re.sub(r'[0-9]\.\s', '', x)
        result.append(x)
    return result


# 関連記事挿入
def relational_article(path, mod_time):
    file_list = os.listdir(path)
    title_list = []
    file_list.remove('how-to-sex.html')
    for file in file_list:
        print(file)
        if '.html' in file:
            with open(path + '/' + file, "r", encoding='utf-8') as f:
                str_x = f.read()
                title = re.findall(r'<h1 .*?>(.*?)</h1>', str_x)
                l_key = re.findall(r'<!--data#key#(.*?)#.*?#-->', str_x)[0]
                dec = {'title': title[0], 'url': file, 'key': l_key}
                title_list.append(dec)
    for file_s in file_list:
        title_list_c = copy.deepcopy(title_list)
        index_list = []
        if '.html' in file_s:
            with open(path + '/' + file_s, "r", encoding='utf-8') as g:
                str_y = g.read()
                comment_str = re.findall(r'<!--data#key#(.*?)#(.*?)#-->', str_y)
                if len(comment_str) >= 1:
                    keyword = comment_str[0][0]
                    key_id = comment_str[0][1]
                    for key_c in keyword_dec_list:
                        if key_c['id'] == key_id:
                            ky_list = key_c['kyoki']
        for title in title_list_c:
            if title['url'] == file_s:
                title_list_c.remove(title)
            else:
                if keyword in title['title']:
                    index_list.append(title)
                    title_list_c.remove(title)
                else:
                    if title['key'] in ky_list:
                        index_list.append(title)
                        title_list_c.remove(title)
        while len(index_list) < 10:
            if title_list_c:
                c_page = random.choice(title_list_c)
                title_list_c.remove(c_page)
                index_list.append(c_page)
            else:
                break
        str_i = '<!--kanren--><section><div class="kanren"><h3>関連記事</h3><ul>'
        random.shuffle(index_list)
        for x in index_list:
            index = '<li><a href="' + x['url'] + '">' + x['title'] + '</a></li>'
            str_i += index
        str_i += '</ul></div></section><!--kanren-e-->'
        str_y = re.sub(r'<!--kanren-->.*<!--kanren-e-->', str_i, str_y)
        str_y = re.sub(r'<time itemprop="dateModified" datetime=".*?">.*?日</time> by',
                       '<time itemprop="dateModified" datetime="' + str(mod_time) + '">'
                       + jap_timestamp_maker(mod_time) + '</time> by', str_y)
        make_file(file_s, str_y)


def html_sitemap_maker(file_data):
    file_data = sorted(file_data.items())
    list_str = ['<li><a href="../make-love/' + x[0] + '">' + x[1] + '</a></li>' for x in file_data]
    list_str = '<!--make-love-entry-start-->' + ''.join(list_str) + '<!--make-love-entry-->'
    replace_html('file_other/sitemap.html', r'<!--make-love-entry-start-->[\s\S]*<!--make-love-entry-->', list_str)
    list_str = list_str.replace('href="../make-love/', 'href="')
    replace_html('files_sf/how-to-sex.html', r'<!--make-love-entry-start-->[\s\S]*<!--make-love-entry-->', list_str)
    return


def xml_sitemap_maker(file_data, mod_date):
    file_data = sorted(file_data.items())
    list_str = ['<url>\n<loc>https://www.demr.jp/pc/make-love/' + x[0]
                + '</loc>\n<lastmod>' + str(mod_date)
                + '</lastmod>\n<changefreq>weekly</changefreq>\n<priority>0.8</priority>\n</url>\n'
                for x in file_data]
    list_str = '<!--make-love-entry-start-->' + ''.join(list_str) + '<!--make-love-entry-->'
    replace_html('file_other/p_sitemap.xml', r'<!--make-love-entry-start-->[\s\S]*<!--make-love-entry-->', list_str)
    return


def make_rss(rss_list):
    entry_list = []
    for x in rss_list:
        entry_str = make_rss_entry(x, atom_rss)
        entry_list.append(entry_str)
    atom_str = atom_rss['header'] + ''.join(entry_list) + atom_rss['footer']
    make_file_d('file_other', 'atom.xml', atom_str)

    entry_list = []
    index_list = []
    for y in rss_list:
        entry_str = make_rss_entry(y, one_rss)
        entry_list.append(entry_str)
        index_list.append(one_rss['index'].replace('<!--file_name-->', y[0]))
    rss_one = one_rss['header'] + ''.join(index_list) + one_rss['second'] + ''.join(entry_list) + one_rss['footer']
    make_file_d('file_other', 'rss10.xml', rss_one)

    entry_list = []
    for y in rss_list:
        entry_str = make_rss_entry(y, two_rss)
        entry_list.append(entry_str)
    rss_two = two_rss['header'] + ''.join(entry_list) + two_rss['footer']
    make_file_d('file_other', 'rss20.xml', rss_two)
    return


def rss_insert(file_path, e_str):
    with open(file_path, 'r') as r:
        base_str = r.read()
        base_str = re.sub(r'<!--rss-insert-s-->([\s\S]*)<!--rss-insert-e-->',
                          '<!--rss-insert-s-->' + str(e_str) + '<!--rss-insert-e-->', base_str)
    with open(file_path, 'w') as s:
        s.write(base_str)


def add_rss(rss_list):
    entry_list = []
    for x in rss_list:
        entry_str = make_rss_entry(x, atom_rss)
        entry_list.append(entry_str)
    atom_str = ''.join(entry_list)
    rss_insert('file_other/atom.xml', atom_str)

    entry_list = []
    index_list = []
    for y in rss_list:
        entry_str = make_rss_entry(y, one_rss)
        entry_list.append(entry_str)
        index_list.append(one_rss['index'].replace('<!--file_name-->', y[0]))
    with open('file_other/rss10.xml', 'r') as r:
        long_str = r.read()
        long_str = re.sub(r'<!--rss-index-s-->([\s\S]*)<!--rss-index-e-->',
                          '<!--rss-index-s-->' + str(''.join(index_list)) + '<!--rss-index-e-->', long_str)
        long_str = re.sub(r'<!--rss-insert-s-->([\s\S]*)<!--rss-insert-e-->',
                          '<!--rss-insert-s-->' + str(''.join(entry_list)) + '<!--rss-insert-e-->', long_str)
    with open('file_other/rss10.xml', 'w') as s:
        s.write(long_str)

    entry_list = []
    for y in rss_list:
        entry_str = make_rss_entry(y, two_rss)
        entry_list.append(entry_str)
    rss_two = ''.join(entry_list)
    rss_insert('file_other/rss20.xml', rss_two)
    return


def make_rss_entry(rss_data, template):
    entry_str = template['entry']
    entry_str = entry_str.replace('<!--file_name-->', rss_data[0])
    entry_str = entry_str.replace('<!--r_title-->', rss_data[1])
    entry_str = entry_str.replace('<!--r_summary-->', rss_data[2])
    entry_str = entry_str.replace('<!--r_content-->', rss_data[3])
    entry_str = entry_str.replace('<!--publish-->', rss_data[4])
    entry_str = entry_str.replace('<!--modify-->', rss_data[5])
    entry_str = entry_str.replace('<!--r_subject-->', rss_data[6])
    return entry_str


def replace_html(path_w, search_str, replace_str):
    with open(path_w, mode='r') as f:
        long_str = f.read()
        long_str = re.sub(search_str, replace_str, long_str)
    with open(path_w, mode='w') as g:
        g.write(long_str)


# ampファイルを作成
def amp_file_maker(path):
    file_list = os.listdir(path)
    with open('file_other/amp_tp.html', "r", encoding='utf-8') as g:
        amp_str = g.read()
    for z in file_list:
        if '.html' not in z:
            file_list.remove(z)
    for file in file_list:
        # print(file)
        with open(path + '/' + file, "r", encoding='utf-8') as f:
            str_x = f.read()
            title = re.findall(r'<h1 itemprop="headline alternativeHeadline name">(.*?)</h1>', str_x)[0]
            content = re.findall(r'ゴーヤン</span></span></a></div>(.*?)<!-- maincontentEnd -->', str_x)[0]
            pub_date = re.findall(r'itemprop="datePublished" datetime="(.*?)">', str_x)[0]
            mod_date = re.findall(r'itemprop="dateModified" datetime="(.*?)">', str_x)[0]
            description = re.findall(r'<meta name="description" content="(.*?)">', str_x)[0]
            date_data = re.findall(r'(\d{4})-(\d{2})-(\d{2})', str_x)
            new_date = date_data[0][0] + '年' + date_data[0][1] + '月' + date_data[0][2] + '日'
            amp_data = amp_str.replace('<!--title-->', title)
            amp_data = amp_data.replace('<!--content-->', content)
            amp_data = amp_data.replace('<!--pub-date-->', str(pub_date))
            amp_data = amp_data.replace('<!--mod-date-->', str(mod_date))
            amp_data = amp_data.replace('<!--description-->', description)
            amp_data = amp_data.replace('<!--path-->', str(path) + '/' + str(file))
            amp_data = amp_data.replace('<!--new-date-->', new_date)
        with open('amp_file/' + file, "w") as h:
            h.write(amp_data)


# ftpアップロード
def ftp_upload(up_file_name, local_dir, remote_dir):
    """
    FTPでファイルをアップロード,ベースはドメイン直下
    :param up_file_name: アップロードするファイル名
    :param local_dir: ファイルのあるディレクトリ
    :param remote_dir: アップロードするディレクトリ
    :return: none
    """
    if remote_dir:
        up_dir_and_file = str(remote_dir) + '/' + str(up_file_name)
    else:
        up_dir_and_file = up_file_name
    with FTP('blackrhino1.sakura.ne.jp', passwd='k2u5n47ku6') as ftp:
        ftp.login(user='blackrhino1', passwd='k2u5n47ku6')
        ftp.cwd('www/reibun')
        with open(str(local_dir) + '/' + str(up_file_name), 'rb') as fp:
            ftp.storbinary("STOR " + up_dir_and_file, fp)
        print('upload: ' + str(up_file_name))
        ftp.close()
    return


def list_upload(files_list):
    """
    [(ファイル名, リモートディレクトリ, ローカルディレクトリ,), (......)]のリストで示したファイルをアップロードする
    :param files_list: タプルのリスト
    :return: なし
    """
    with FTP('blackrhino1.sakura.ne.jp', passwd='k2u5n47ku6') as ftp:
        ftp.login(user='blackrhino1', passwd='k2u5n47ku6')
        ftp.cwd('www/reibun')
        for file_u in files_list:
            with open(str(file_u[2]) + '/' + str(file_u[0]), 'rb') as fp:
                ftp.storbinary("STOR " + str(file_u[1]) + str(file_u[0]), fp)
            print('upload: ' + str(file_u[1]) + '/' + str(file_u[0]))
        ftp.close()
    return


def directory_upload(local_dir, pc_or_amp, remote_dir):
    file_list = os.listdir(local_dir)
    for file in file_list:
        if '.html' not in file:
            file_list.remove(file)
    with FTP('blackrhino1.sakura.ne.jp', passwd='k2u5n47ku6') as ftp:
        ftp.login(user='blackrhino1', passwd='k2u5n47ku6')
        ftp.cwd('www/reibun/' + str(pc_or_amp))
        items = ftp.nlst('.')
        if remote_dir not in items:
            ftp.mkd(remote_dir)
        ftp.cwd(remote_dir)
        for file_name in file_list:
            with open(str(local_dir) + '/' + str(file_name), 'rb') as fp:
                ftp.storbinary("STOR " + str(file_name), fp)
            print('upload: ' + str(file_name))
        ftp.close()
    return


# 以下、重複文字列チェッカー
def article_checker(directory_str):
    """
    記事の書かれたファイルを比較して一致する文字列を長い順に「１０」返す
    :param directory_str: ファイルのあるディレクトリパス
    :return: 一致するファイル名と文字列のリスト
    """
    file_list = os.listdir(directory_str)
    file_list.sort()
    file_list.pop(0)
    same_list = SameStrList()
    for x in range(0, len(file_list) - 1):
        with open(directory_str + '/' + file_list[x], "r", encoding='utf-8') as f:
            str_x_b = f.read()
        for y in range(x + 1, len(file_list)):
            with open(directory_str + '/' + file_list[y], "r", encoding='utf-8') as g:
                str_y_b = g.read()
            str_x = copy.deepcopy(str_x_b)
            str_y = copy.deepcopy(str_y_b)
            keyword_x = keyword_search(str_x)
            keyword_y = keyword_search(str_y)
            str_x = MyHtmlStripper(str_x).value
            str_y = MyHtmlStripper(str_y).value
            str_x = wp_tag_delete(str_x)
            str_y = wp_tag_delete(str_y)
            id_num = id_search(str_x)
            print(keyword_x, keyword_y)
            match_str_list = same_sentence_checker(str_x, str_y, keyword_x, keyword_y, same_list.min())
            for match_str in match_str_list:
                dec_b = {'length': len(match_str), 'str_s': match_str, 'low': file_list[x], 'high': file_list[y],
                         'id': id_num}
                same_list.insert(dec_b)
    return same_list


def wp_tag_delete(long_str):
    for x in wp_tag:
        long_str = long_str.replace(x, '')
    return long_str


def keyword_search(str_k):
    result = ""
    comment_str = re.findall(r'<!--data#key#(.*?)#.*#-->', str_k)
    if len(comment_str) >= 1:
        result = comment_str[0]
    return result


def id_search(str_k):
    result = ""
    comment_str = re.findall(r'<!--data#key#.*?#id#(.*?)#.*#-->', str_k)
    if len(comment_str) >= 1:
        result = comment_str[0]
    return result


class SameStrList:
    list_len = 20

    def __init__(self):
        self.list_body = []

    def insert(self, ins_dec):
        if len(self.list_body) < self.list_len:
            self.list_body.append(ins_dec)
        elif len(self.list_body) >= self.list_len:
            self.list_body.append(ins_dec)
            list_sort(self.list_body, 'length', True)
            while len(self.list_body) > self.list_len:
                self.list_body.pop()
        list_sort(self.list_body, 'length', True)

    def show(self):
        list_sort(self.list_body, 'length', True)
        for list_i in self.list_body:
            print(list_i)

    def high_show(self):
        list_sort(self.list_body, 'high', False)
        for list_i in self.list_body:
            print(list_i)

    def id_show(self):
        list_sort(self.list_body, 'id', False)
        for list_i in self.list_body:
            print(list_i)

    def length(self):
        return len(self.list_body)

    def min(self):
        if len(self.list_body) > 0:
            min_num = self.list_body[-1]['length']
        else:
            min_num = 0
        return min_num


def list_sort(s_list, sort_key, reverse):
    s_list.sort(key=lambda x: x[sort_key], reverse=reverse)
    return s_list


def same_sentence_checker(str_checked, str_other, keyword, other_keyword, min_len):
    """
    二つの記事を比較して一致するもっとも長い文字列を返す
    :param str_checked: 一つ目の記事
    :param str_other: ２つ目の記事
    :param keyword: １つ目の記事のキーワード
    :param other_keyword: ２つ目の記事のキーワード
    :param min_len: 結果リストの一番短い文字数
    :return: 一致したもっとも長い文字列
    """
    result = []
    if min_len < 20:
        min_len = 20
    list1 = keyword_slice(str_checked, keyword)
    list1 = str_length_checker(list1, min_len)
    list2 = keyword_slice(str_other, other_keyword)
    list2 = str_length_checker(list2, min_len)
    for str_1 in list1:
        for str_2 in list2:
            match_str = find_longest_substr(str_1, str_2, min_len)
            if match_str != 'n/a':
                result.append(match_str)
                min_len = len(match_str)
            else:
                pass
    return result


def str_length_checker(str_list, min_len):
    for str_s in str_list:
        if len(str_s) <= min_len:
            str_list.remove(str_s)
        else:
            pass
    return str_list


def keyword_slice(str_checked, keyword):
    """
    キーワードで文字列をスライスして文字列のリストを返す
    :param str_checked: 大きな文字列
    :param keyword: キーワード
    :return: スライスされてキーワードを取り除いたリスト
    """
    list_r = []
    key_len = len(keyword)
    while keyword in str_checked:
        index = str_checked.find(keyword) + key_len
        str_sliced = str_checked[0:index]
        str_sliced_c = str_sliced.replace(keyword, '')
        list_r.append(str_sliced_c)
        str_checked = str_checked[index:]
    return list_r


def find_longest_substr(str1, str2, last_length):
    """
    文字列を比較して一致するもっとも長い文字列を返す
    :param str1: 文字列
    :param str2: 文字列
    :param last_length: リストの最小の文字列の文字数（整数）
    :return: 一致するもっとも長い文字列
    """
    result = 'n/a'
    if len(str1) > last_length:
        for length in range(len(str2), last_length, -3):
            for p0 in range(len(str2) - length + 3):
                substr = str2[p0:(p0 + length)]
                # print(substr)
                if substr in str1:
                    result = substr
                    return result
    else:
        pass
    return result


class MyHtmlStripper(HTMLParser):
    def error(self, message):
        pass

    def __init__(self, s):
        super().__init__()
        self.sio = io.StringIO()
        self.feed(s)

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        self.sio.write(data)

    @property
    def value(self):
        return self.sio.getvalue()


def directory_to_list(path):
    directory = os.listdir(path)
    result = []
    for file in directory:
        file_path = path + "/" + file
        result.append(file_path)
    return result


# まとめてアップロード
def total_upload():
    directory_upload('files_sf', 'pc', 'make-love')
    directory_upload('amp_file', 'amp', 'make-love')
    upload_files = [('atom.xml', '', 'file_other',), ('p_sitemap.xml', '', 'file_other',),
                    ('rss10.xml', '', 'file_other',), ('rss20.xml', '', 'file_other',),
                    ('sitemap.html', 'pc/policy/', 'file_other',)]
    list_upload(upload_files)


def sentence_counter(template):
    with open('file_other/rb_sf_make_love20190518.pkl', 'rb') as f:
        pk_list = pickle.load(f)
    set_dic = {}
    del pk_list[-1]
    for data_p in pk_list:
        del data_p[0]
        for x in data_p:
            if x in set_dic:
                set_dic[x] += 1
            else:
                set_dic[x] = 1
    num_list = []
    for t in set_dic:
        num_d = re.findall(r'(\d+)-', t)[0]
        num_list.append(int(num_d))
    no_list = []
    for y in template['sentence_num']:
        if y not in num_list:
            print(str(y) + ' がありません')
            no_list.append(y)
    return no_list


# 以下、実行
if __name__ == '__main__':
    # 記事作成
    main(rb_sex_template, keyword_dec_list, 193, 209)
    # ファイル一括アップロード
    total_upload()

    # print(sentence_counter())
    # article_checker("/Users/nakataketetsuhiko/PycharmProjects/create_article/files_sf").show()
