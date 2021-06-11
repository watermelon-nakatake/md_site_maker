import pprint
import re
import MeCab
import words_dict
import ts_new1


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


def search_by_mecab():
    m_list = []
    use_list = []
    for w_list in ts_new1.all_list:
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


def make_word_dict(word_list):
    result = {}
    for row in word_list:
        for word in row['after']:
            if word not in result:
                result[word] = row['before']
    return result


def word_filter(target_str, word_key_dict, word_key_list):
    for word in word_key_list:
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


def md_to_data_dict(md_path):
    conj_dict = make_word_dict(words_dict.conj_list)
    noun_dict = make_word_dict(words_dict.noun_list)
    noun_list = sorted(noun_dict.keys(), key=lambda x: len(x), reverse=True)
    print(noun_list)
    with open(md_path, 'r', encoding='utf-8') as f:
        md_str = f.read()
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
                        word_dict[index] = [h_mark + sentence_filter(row, conj_dict, noun_dict,
                                                                     noun_list).replace('#', '')]
                        index += 1
                    else:
                        if h_flag:
                            word_dict[index - 1].append(h_mark + sentence_filter(row.replace('|', ''),
                                                                                 conj_dict, noun_dict, noun_list))
                        else:
                            word_dict[index - 1].append(sentence_filter(row.replace('|', ''), conj_dict, noun_dict,
                                                                        noun_list))
        r_index = list(filter(lambda x: type(x) == int, word_dict.keys()))
        i = max(r_index)
        while word_dict[i] == 'space':
            del word_dict[i]
            i -= 1
        word_dict = shuffle_filter(word_dict)
    list_name = md_path.replace('.md', '')
    insert_str = '{} = {}\n# {}/end\n'.format(list_name, pprint.pformat(word_dict), list_name)
    with open('source_data.py', 'r', encoding='utf-8') as h:
        souse_str = h.read()
        if list_name + ' =' in souse_str:
            souse_str = re.sub(list_name + r' =[\s\S]+?# ' + list_name + r'/end\n', insert_str, souse_str)
        else:
            list_num = re.findall(r'_\d+?_(\d+)$', list_name)[0]
            pre_list_name = re.sub(list_num + r'$', str(int(list_num) - 1), list_name)
            souse_str = souse_str.replace('# ' + pre_list_name + '/end\n',
                                          '# ' + pre_list_name + '/end\n\n' + insert_str + '\n')
        with open('source_data.py', 'w', encoding='utf-8') as g:
            g.write(souse_str)


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


def sentence_filter(sentence_str, conj_dict, noun_dict, noun_list):
    after_list = []
    m_list = mecab_list(sentence_str)
    for m_data in m_list:
        # print(m_data)
        if m_data[0] in conj_dict and m_data[1] == '接続詞':
            after_list.append(conj_dict[m_data[0]])
        else:
            after_list.append(m_data[0])
    new_str = ''.join(after_list)
    new_str = word_filter(new_str, noun_dict, noun_list)
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
    # md_to_data_dict('int_1_1.md')
    # t = pprint.pformat(resource_import_from_sf(sf_s_list.main_list))
    # with open('ts.py', 'w', encoding='utf-8') as p:
    #     p.write('i = ' + t)
    # pick_up_str('ts.py')
    search_by_mecab()
