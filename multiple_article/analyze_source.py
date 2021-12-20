import pprint
import re

import source_data
import make_new_resource
import words_dict as wd
import source_data_o


def make_noun_list():
    used_list = []
    noun_list = []
    app_list = []
    result = []
    for n_list in [wd.noun_list, wd.fix_noun_list]:
        for row in n_list:
            for word in row['after']:
                if word and len(word) > 2:
                    if 'omit' in row:
                        if word not in row['omit'] and word not in used_list:
                            noun_list.append([word, row['before'], row['omit']])
                            used_list.append(word)
                    else:
                        if word not in used_list:
                            noun_list.append([word, row['before']])
                            used_list.append(word)
    noun_list.sort(key=lambda x: len(x[0]), reverse=True)
    for w in noun_list:
        if '<!--' in w[0]:
            app_list.append(w)
        else:
            result.append(w)
    result.extend(app_list)
    return result


def check_changed_source(c_str):
    after_dict = make_source_dict(source_data.all_list)
    before_dict = make_source_dict(source_data_o.all_list)
    ad_hit = {x: after_dict[x] for x in after_dict if c_str in after_dict[x]}
    bd_hit = {x: before_dict[x] for x in before_dict if c_str in before_dict[x]}
    # print(ad_hit)
    only_ad = {x: re.sub(r'^.*(...' + c_str + '...).*$', r'\1', ad_hit[x]) for x in ad_hit if x in before_dict and x not in bd_hit}
    only_bd = {x: re.sub(r'^.*(...' + c_str + '...).*$', r'\1', bd_hit[x]) for x in bd_hit if x not in ad_hit}
    print('only_bd :')
    pprint.pprint(only_bd)
    print('only_ad :')
    pprint.pprint(only_ad)


def make_source_dict(this_dict):
    result = {}
    for row in this_dict:
        if row['info']['sec_name'] == 'title':
            for i1 in row:
                if i1 != 'info':
                    for i2 in row[i1]:
                        for s in row[i1][i2]:
                            result['-'.join([row['info']['sec_name'], i1, i2, str(row[i1][i2].index(s))])] = s
        elif row['info']['sec_name'] == 'des':
            for i1 in row:
                if i1 != 'info':
                    for s in row[i1]:
                        result['-'.join([row['info']['sec_name'], i1, str(row[i1].index(s))])] = s
        else:
            for i1 in row:
                if i1 != 'info' and row[i1] != 'space':
                    for s in row[i1]:
                        result['-'.join([row['info']['sec_name'], str(i1), str(row[i1].index(s))])] = s
    # pprint.pprint(result)
    return result


def check_noun_list():
    used_str = []
    for n_list in [wd.noun_list, wd.fix_noun_list]:
        for row in n_list:
            if row['before'] not in used_str:
                used_str.append(row['before'])
            else:
                print('there is {}'.format(row['before']))
            if 'plist' in row:
                if len(row['plist']) != len(row['after']):
                    print('Be same num in plist !! : {}'.format(row['before']))
                else:
                    if not 0.999 < sum(row['plist']) < 1.001:
                        print('sum is not 1 !! : {}'.format(row['before']))


def check_sentence_by_noun_list(s_list, noun_list):
    # print(noun_list)
    r_dict = {}
    for sen in s_list:
        for row in noun_list:
            if row[0] in sen:
                if len(row) <= 2:
                    # print('{}({}) in {}'.format(row[0], row[1], sen))
                    if row[1] in r_dict:
                        r_dict[row[1]].append([row[0], row[1], sen])
                    else:
                        r_dict[row[1]] = [[row[0], row[1], sen]]
                else:
                    omit_flag = False
                    for omit in row[2]:
                        if row[0] in omit:
                            if omit in sen:
                                omit_flag = True
                    if not omit_flag:
                        # print('{}({}) in {}'.format(row[0], row[1], sen))
                        if row[1] in r_dict:
                            r_dict[row[1]].append([row[0], row[1], sen])
                        else:
                            r_dict[row[1]] = [[row[0], row[1], sen]]
    pprint.pprint(r_dict)


def pick_up_word_in_source(select_num):
    noun_list = make_noun_list()
    source = source_data.all_list[1:]
    # pprint.pprint(source)
    s_list = []
    check_noun_list()
    for row in source:
        if type(row) == str:
            s_list.extend(str_filter(row))
        elif type(row) == list:
            s_list.extend(list_flat(row))
        elif type(row) == dict:
            s_list.extend(dict_flat(row))
        else:
            # print('error : {}'.format(row))
            pass
    s_list = list(set(s_list))
    s_list.sort(key=lambda x: len(x), reverse=True)

    if select_num == 0:
        check_sentence_by_noun_list(s_list, noun_list)

    elif select_num == 1:
        s_list = [x for x in s_list if len(x) > 10]
        pprint.pprint(s_list)
    elif select_num == 2:
        s_str = ''.join(s_list)
        m_list = make_new_resource.mecab_list(s_str)
        c_list = [list(x) + [m_list.count(x)] for x in m_list]
        n_list = []
        for r in c_list:
            if r not in n_list:
                n_list.append(r)
        # pprint.pprint(n_list)
        n_list = [x for x in n_list if x[1] not in ['助詞', '助動詞', '記号']]
        n_list.sort(key=lambda x: x[-1], reverse=True)
        pprint.pprint(n_list)

    # print(s_str)


def list_flat(s_list):
    result = []
    for row in s_list:
        if type(row) == str:
            result.extend(str_filter(row))
        elif type(row) == list:
            result.extend(list_flat(row))
        elif type(row) == dict:
            result.extend(dict_flat(row))
        else:
            # print('error : {}'.format(row))
            pass
    return result


def str_filter(s_str):
    result = []
    if s_str == 'space':
        pass
    elif s_str.startswith('%'):
        s_str = re.sub(r'^%._.%', '', s_str)
        s_str = re.sub(r'^%._.', '', s_str)
    elif s_str.startswith('#'):
        s_str = re.sub(r'^#+ ', '', s_str)
    elif s_str.startswith('-'):
        s_str = re.sub(r'^- ', '', s_str)
        s_str = re.sub(r'^-', '', s_str)
    if s_str.endswith('!'):
        s_str = re.sub(r'!$', '', s_str)
    s_str = s_str.replace('「', '')
    s_str = s_str.replace('」', '')
    s_str = s_str.replace('*', '')
    s_str = s_str.replace(',', ' ')
    s_str = re.sub(r'<!--.*?-->', ' ', s_str)
    result = s_str.split()
    return result


def dict_flat(s_dict):
    result = []
    for x in s_dict:
        if x == 'info':
            pass
        elif s_dict[x] == 'space':
            pass
        elif type(s_dict[x]) == str:
            result.extend(s_dict[x])
        elif type(s_dict[x]) == list:
            result.extend(list_flat(s_dict[x]))
        elif type(s_dict[x]) == dict:
            result.extend(dict_flat(s_dict[x]))
        else:
            print('error : {}'.format(s_dict[x]))
    return result


if __name__ == '__main__':
    pick_up_word_in_source(0)
    # check_changed_source('<!--waste-->')
