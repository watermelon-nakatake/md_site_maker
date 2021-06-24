import pprint
import re
import MeCab
from numpy import random
import words_dict
# import rw_word_dict
# import rewrite_word_list
import make_new_article


def joint_word_list(lists_list):
    joint_list = []
    used_key = {}
    review_list = []
    for w_list in lists_list:
        for word in w_list:
            if word['before'] not in used_key:
                used_key[word['before']] = word
                joint_list.append(word)
            else:
                if word != used_key[word['before']]:
                    review_list.append(word)
                    print(word)
    # print(joint_list)


def pick_up_str(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        long_str = f.read()
    f_list = re.findall(r"\['h3',[\s\S]+?]", long_str)
    for r in f_list:
        g_list = re.findall(r"'\S+?'", r)
        for g in g_list:
            if g != "'h3'":
                # print(g)
                ge = re.sub(r"'(\S+?')", r"'### \1", g)
                # print(ge)
                long_str = long_str.replace(g, ge)
    long_str = re.sub(r"\[('h\d',\s+)'", "['", long_str)
    long_str = long_str.replace('[[', '[\n\t[')
    list_name = [x[2] if x[2] else x[0] for x in re.findall(r'\n(\w+(_\d)+) =|\n(\w+) =', long_str)]
    # print(list_name)
    long_str += "\nlist_name = ['{}']".format("', '".join(list_name))
    print(long_str)
    with open('ts_1.py', 'w', encoding='utf-8') as h:
        h.write(long_str)


def search_by_mecab(data_list):
    m_list = []
    use_list = []
    for w_list in data_list:
        for list1 in w_list:
            if type(list1) is list:
                for sentence in list1:
                    # print(sentence)
                    # print(mecab_list(sentence))
                    sentence = re.sub(r'<!--.+?-->', '', sentence)
                    sentence = re.sub(r'%\w+', '', sentence)
                    sentence = sentence.replace('### ', '').replace('## ', '').replace('<li>', '').replace('</li>', '')
                    for m in mecab_list(sentence):
                        if m not in use_list:
                            m_list.append([m, 0])
                            use_list.append(m)
                        else:
                            m_list[use_list.index(m)] = [m, m_list[use_list.index(m)][1] + 1]
                            # print(m_list[use_list.index(m)])
    m_list.sort(key=lambda x: x[1], reverse=True)
    for y in m_list:
        if y[1] > 1 and y[0][1] != '記号':
            print(y)


def make_word_dict(word_list, ignore_list):
    result = {}
    for row in word_list:
        for word in row['after']:
            if '<!--' in word:
                find_l = re.findall(r'<!--.+?-->', word)
                if find_l:
                    for f_str in find_l:
                        for i_w in word_list:
                            if i_w['before'] == f_str:
                                for aw in i_w['after']:
                                    result[word.replace(f_str, aw)] = row['before']
            else:
                if word not in result and len(word) > 1 and word not in ignore_list\
                        and word not in words_dict.ignore_words:
                    result[word] = row['before']
                # else:
                    # print('error : {}'.format(word))
    return result


def word_filter(target_str, word_key_dict, word_key_list, omit_list, ignore_words):
    for word in word_key_list:
        if word not in words_dict.ignore_words and word not in ignore_words:
            if word not in omit_list:
                target_str = target_str.replace(word, word_key_dict[word])
            else:
                flag = False
                for o_word in omit_list[word]:
                    if o_word in target_str:
                        flag = True
                        break
                if not flag:
                    target_str = target_str.replace(word, word_key_dict[word])
    return target_str


def resource_import_from_sf(w_list):
    if type(w_list) is list:
        if len(w_list) == 1:
            return resource_import_from_sf(w_list[0])
        elif len(w_list) < 1:
            return False
        else:
            for y in w_list:
                if type(y) == list:
                    return resource_import_from_sf(y)
            t_list = [resource_import_from_sf(x) for x in w_list if x not in ['st', 'title', 'sc', 'ch', 'sh', 'nodata',
                                                                              'ps']]
            return t_list
    else:
        return w_list


def make_omit_list(word_list):
    result = {}
    for word in word_list:
        if 'omit' in word:
            for after in word['after']:
                result[after] = word['omit']
    return result


def list_duplication_check(noun_list):
    used_list = []
    for word in noun_list:
        if word['before'] not in used_list:
            used_list.append(word['before'])
        else:
            print('error : {} already used'.format(word['before']))


def md_to_data_dict(md_path, keywords, ignore_words, replace_list):
    key_phrase_dict = make_new_article.make_keywords_sample_dict(keywords)
    list_duplication_check(words_dict.noun_list)
    # print(key_phrase_dict)
    conj_dict = make_word_dict(words_dict.conj_list, ignore_words)
    conj_list = sorted(conj_dict.keys(), key=lambda x: len(x), reverse=True)
    # print(conj_dict)
    noun_dict = make_word_dict(words_dict.noun_list, ignore_words)
    noun_list = sorted(noun_dict.keys(), key=lambda x: len(x), reverse=True)
    omit_list = make_omit_list(words_dict.noun_list)
    # print(noun_list)
    with open(md_path, 'r', encoding='utf-8') as f:
        md_str = f.read()
        if 'keywords =' in md_str:
            key_str = re.findall(r'keywords = ([\s|\S]+)$', md_str)[0]
            key_str = key_str.replace('\n', '')
            # print(key_str)
            keywords['s_adj'] = re.findall(r's_adj: (.+?),', key_str)[0]
            keywords['sub'] = re.findall(r'sub: (.+?),', key_str)[0]
            keywords['o_adj'] = re.findall(r'o_adj: (.+?),', key_str)[0]
            keywords['obj'] = re.findall(r'obj: (.+?),', key_str)[0]
            keywords['obj_key'] = re.findall(r'obj_key: (.+?),', key_str)[0]
            keywords['obj_p'] = re.findall(r'obj_p: (.+?),', key_str)[0]
            keywords['act_adj'] = re.findall(r'act_adj: (.+?),', key_str)[0]
            keywords['act'] = re.findall(r'act: (.+?),', key_str)[0]
            keywords['act_noun'] = re.findall(r'act_noun: (.+?),', key_str)[0]
            keywords['act_connection'] = re.findall(r'act_connection: (.+?) ', key_str)[0]
            # print(keywords)
            md_str = re.sub(r'keywords =[\s|\S]+$', '', md_str)
        word_dict = {'info': {}}
        split_str = md_str.split('\n')
        index = 0
        h_mark = ''
        h_flag = False
        for row in split_str:
            if row.startswith('o::'):
                word_dict['info']['only'] = [x for x in row.replace('o::', '').split() if x]
            elif row.startswith('d::'):
                word_dict['info']['deny'] = [x for x in row.replace('d::', '').split() if x]
            elif '::' not in row:
                if index != 0 and row == '':
                    if word_dict[index - 1] != 'space':
                        word_dict[index] = 'space'
                        index += 1
                elif index == 0 and row == '':
                    continue
                else:
                    if not row.startswith('|'):
                        if row.startswith('#'):
                            h_mark = re.sub(r'(#+ ).*$', r'\1', row)
                            h_flag = True
                        else:
                            h_flag = False
                            h_mark = ''
                        word_dict[index] = [h_mark + sentence_filter(row, conj_dict, conj_list, noun_dict, noun_list,
                                                                     key_phrase_dict, omit_list, ignore_words,
                                                                     replace_list).replace('#', '')]
                        index += 1
                    else:
                        if h_flag:
                            word_dict[index - 1].append(h_mark + sentence_filter(row.replace('|', ''),
                                                                                 conj_dict, conj_list,noun_dict, noun_list,
                                                                                 key_phrase_dict, omit_list, ignore_words,
                                                                                 replace_list))
                        else:
                            word_dict[index - 1].append(sentence_filter(row.replace('|', ''), conj_dict, conj_list, noun_dict,
                                                                        noun_list, key_phrase_dict, omit_list, ignore_words,
                                                                        replace_list))
        r_index = list(filter(lambda x: type(x) == int, word_dict.keys()))
        i = max(r_index)
        while word_dict[i] == 'space':
            del word_dict[i]
            i -= 1
        word_dict = shuffle_filter(word_dict)
    list_name = re.sub(r'^.*/(.+?).md', r'\1', md_path)
    word_dict['info']['sec_name'] = list_name
    insert_str = '{} = {}\n# {}/end\n'.format(list_name, pprint.pformat(word_dict), list_name)
    print(insert_str)
    for w_id in word_dict:
        if type(word_dict[w_id]) == list and len(word_dict[w_id]) < 2:
            print('too small list : {}'.format(w_id))
        elif type(word_dict[w_id]) == list and len(word_dict[w_id]) == 2:
            for w_str in word_dict[w_id]:
                if not re.findall(r'<!--k-', w_str):
                    print('no keyword and small list : {}'.format(w_str))
    with open('multiple_article/source_data.py', 'r', encoding='utf-8') as h:
        souse_str = h.read()
        if list_name + ' =' in souse_str:
            souse_str = re.sub(list_name + r' =[\s\S]+?# ' + list_name + r'/end\n', insert_str, souse_str)
        else:
            list_num = re.findall(r'_\d+?_(\d+)$', list_name)[0]
            pre_list_name = re.sub(list_num + r'$', str(int(list_num) - 1), list_name)
            souse_str = souse_str.replace('# ' + pre_list_name + '/end\n',
                                          '# ' + pre_list_name + '/end\n\n' + insert_str + '\n')
        # print(souse_str)
        # with open('source_data.py', 'w', encoding='utf-8') as g:
        #     g.write(souse_str)


def shuffle_filter(md_dict):
    result_list = []
    i_num = 0
    shf_list_num = 0
    list_flag = False
    while i_num in md_dict:
        if '%s' in md_dict[i_num][0]:
            if len(result_list) < shf_list_num + 1:
                result_list.append([i_num])
                list_flag = True
            else:
                result_list[shf_list_num].append(i_num)
            md_dict[i_num] = [x.replace('%s', '') for x in md_dict[i_num]]
        elif md_dict[i_num] != 'space' and list_flag:
            shf_list_num += 1
            list_flag = False
        i_num += 1
    if result_list:
        md_dict['info']['shuffle'] = result_list
    return md_dict


def sentence_filter(sentence_str, conj_dict, conj_list, noun_dict, noun_list, key_list, omit_list, ignore_words,
                    replace_list):
    after_list = []
    for kw in key_list:
        if len(kw[0]) > 2 and kw[0] in sentence_str:
            if len(kw[1]) > 1:
                sentence_str = sentence_str.replace(kw[0], random.choice(kw[1]))
            else:
                sentence_str = sentence_str.replace(kw[0], kw[1][0])
    new_str = sentence_str
    for r_word in replace_list:
        if r_word[0] in new_str:
            new_str = new_str.replace(r_word[0], r_word[1])
    for conj in conj_list:
        if conj in new_str:
            new_str = new_str.replace(conj + '、', conj_dict[conj])
    # m_list = mecab_list(sentence_str)
    # for m_data in m_list:
    #     # print(m_data)
    #     if m_data[0] in conj_dict:
    #         after_list.append(conj_dict[m_data[0]])
    #     else:
    #         after_list.append(m_data[0])
    # new_str = ''.join(after_list)
    new_str = word_filter(new_str, noun_dict, noun_list, omit_list, ignore_words)
    return new_str


def mecab_list(text):
    tagger = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    tagger.parse('')
    node = tagger.parseToNode(text)
    word_class = []
    while node:
        word = node.surface
        wclass = node.feature.split(',')
        if wclass[0] != u'BOS/EOS':
            if wclass[6] is None:
                word_class.append((word, wclass[0], wclass[1], wclass[2], ""))
            else:
                word_class.append((word, wclass[0], wclass[1], wclass[2], wclass[6]))
        node = node.next
    return word_class

    # introduction = []
    # body_p = []
    # conclusion = []
    # tips = []
    # process = []
    # site_info = []
    # sub_str = []  # 童貞男性　が
    # obj_str = []  # 人妻ナース と
    # act_str = []  # セックスする
    # way_str = []  # 出会い系サイトで
    # adv_str = []  # 確実に、早く


if __name__ == '__main__':
    # joint_word_list([words_dict.noun_list, rw_word_dict.noun_list, rewrite_word_list.word_dict])

    k_p = {
        's_adj': '普通の', 'sub': '男性',
        'o_adj': '淫乱な', 'obj': '巨乳女性', 'obj_key': '巨乳', 'obj_p': 'の',
        'act_adj': '安全に', 'act': 'セフレを作る', 'act_noun': 'セフレ', 'act_noun_flag': True,
        'act_connection': ['セフレ関係'],
        'o_reason': '',
        't_sex': 'm', 't_age': 'n', 't_cat': 'j', 'act_code': 'gf'}

    md_to_data_dict('multiple_article/source_md/tips/tips_9_1.md', k_p, [], [['誠実さ', '<!--vrt-imp-->']])

    # t = pprint.pformat(resource_import_from_sf(sf_s_list.main_list))
    # with open('ts.py', 'w', encoding='utf-8') as p:
    #     p.write('i = ' + t)
    # pick_up_str('ts.py')
    # search_by_mecab()
