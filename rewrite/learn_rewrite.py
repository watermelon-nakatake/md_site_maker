import os
import re
import MeCab
import difflib
import pprint
import pickle


def compare_manual_rewrite():
    print('a')
    a_str = 'あああああいいいいいああああああ'
    b_str = 'あああああああううううあああいいいいいい'
    d = difflib.Differ()
    diff = d.compare(a_str, b_str)

    s = difflib.SequenceMatcher(None, a_str, b_str).ratio()
    print(s)
    return ''.join(diff)


def example_switch_filter(md_str):
    used = []
    ex_str_l = re.findall(r'や[亜-熙ぁ-んァ-ヶa-zA-Zー]{1,8}?、[亜-熙ぁ-んァ-ヶa-zA-Zー]{1,8}?など', md_str)
    for p in ex_str_l:
        print(p)
        words = re.findall(r'や([亜-熙ぁ-んァ-ヶa-zA-Zー]{,8}?)、([亜-熙ぁ-んァ-ヶa-zA-Zー]{,8}?)など', p)
        md_str = md_str.replace(p, 'や{}、{}等'.format(words[0][1], words[0][0]))
        used.append('や{}、{}等'.format(words[0][1], words[0][0]))
    ex_str_l1 = re.findall(r'や[亜-熙ぁ-んァ-ヶa-zA-Zー]{1,8}?、[亜-熙ぁ-んァ-ヶa-zA-Zー]{1,8}?等', md_str)
    for q in ex_str_l1:
        if q not in used:
            print(q)
            words2 = re.findall(r'や([亜-熙ぁ-んァ-ヶa-zA-Zー]{,8}?)、([亜-熙ぁ-んァ-ヶa-zA-Zー]{,8}?)等', q)
            md_str = md_str.replace(q, 'や{}、{}など'.format(words2[0][1], words2[0][0]))
    ex_str_l3 = re.findall(r'や[亜-熙ぁ-んァ-ヶa-zA-Zー]{1,8}?、[亜-熙ぁ-んァ-ヶa-zA-Zー]{1,8}?、[亜-熙ぁ-んァ-ヶa-zA-Zー]{1,8}?など',
                           md_str)
    for r in ex_str_l3:
        print(r)
        words3 = re.findall(r'や([亜-熙ぁ-んァ-ヶa-zA-Zー]{,8}?)、([亜-熙ぁ-んァ-ヶa-zA-Zー]{,8}?)、([亜-熙ぁ-んァ-ヶa-zA-Zー]{,8}?)など',
                            r)
        md_str = md_str.replace(r, 'や{}、{}, {}等'.format(words3[0][2], words3[0][0], words3[0][1]))
        used.append('や{}、{}等'.format(words3[0][1], words3[0][0]))
    ex_str_l4 = re.findall(r'や[亜-熙ぁ-んァ-ヶa-zA-Zー]{1,8}?、[亜-熙ぁ-んァ-ヶa-zA-Zー]{1,8}?、[亜-熙ぁ-んァ-ヶa-zA-Zー]{1,8}?等',
                           md_str)
    for s in ex_str_l4:
        if s not in used:
            print(s)
            words4 = re.findall(r'や([亜-熙ぁ-んァ-ヶa-zA-Zー]{,8}?)、([亜-熙ぁ-んァ-ヶa-zA-Zー]{,8}?)、([亜-熙ぁ-んァ-ヶa-zA-Zー]{,8}?)等',
                                s)
            md_str = md_str.replace(s, 'や{}、{}、{}など'.format(words4[0][1], words4[0][2], words4[0][0]))
    print(md_str)


def md_match_filter(md_str):
    md_str = re.sub(r'\n\n', '\n', md_str)
    md_str = re.sub(r']\(\.\./.*?\)', '', md_str)
    md_str = re.sub(r'%\w+?%', '', md_str)
    md_str = re.sub(r'\n[a-z]::', '', md_str)
    return md_str


def pickup_chang_str(before_path, after_path, counter_num):
    b_list = []
    with open(before_path, 'r', encoding='utf-8') as f:
        b_str = f.read()
    with open(after_path, 'r', encoding='utf-8') as g:
        a_str = g.read()
    if '<<<' in b_str or '>>>' in b_str:
        b_str = b_str.replace('>>>', '').replace('<<<', '')
    if '<<<' in a_str or '>>>' in a_str:
        a_str = a_str.replace('>>>', '').replace('<<<', '')
    # a_str = a_str.split('\n')
    # b_str = b_str.split('\n')
    d = difflib.Differ()
    diff = d.compare(b_str, a_str)
    now_f = ' '
    pass_str = ''
    list_stock = ['', '']
    a_counter = 0
    pc_num = -1 * counter_num
    for ds in diff:
        # print(ds)
        if now_f == ' ':
            if ds[0] == '+':
                list_stock[0] = pass_str[pc_num:] + ds[2]
                list_stock[1] = pass_str[pc_num:]
            elif ds[0] == '-':
                list_stock[0] = pass_str[pc_num:]
                list_stock[1] = pass_str[pc_num:] + ds[2]
        else:
            if ds[0] == '+':
                list_stock[0] += ds[2]
            elif ds[0] == '-':
                list_stock[1] += ds[2]
            elif ds[0] == ' ':
                b_list.append(list_stock)
                list_stock = ['', '']
                a_counter = counter_num
        now_f = ds[0]
        if a_counter != 0 and ds[0] == ' ':
            b_list[-1][0] += ds[2]
            b_list[-1][1] += ds[2]
            a_counter -= 1
        pass_str += ds[2]
    dir_name = re.sub(r'/md_files/.*$', '/rewrite_log', after_path)
    pk_path = after_path.replace('/', '_').replace('_md_files_', '/rewrite_log/').replace('.md', '.pkl')
    print(pk_path)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    if os.path.exists(pk_path):
        with open(pk_path, 'rb') as i:
            o_pk = pickle.load(i)
            b_list = o_pk + b_list
    with open(pk_path, 'wb') as p:
        pickle.dump(b_list, p)
    tx_str = '\n\n--------------------------------\n\n'.join(['{} ==> {}'.format(y[0], y[1]) for y in b_list])
    if os.path.exists(pk_path.replace('.pkl', '.txt')):
        with open(pk_path.replace('.pkl', '.txt'), 'r', encoding='utf-8') as j:
            o_tx = j.read()
            tx_str = o_tx + '-' * 20 + tx_str
    with open(pk_path.replace('.pkl', '.txt'), 'w', encoding='utf-8') as h:
        h.write(tx_str)
    return b_list


def md_resemblance(file_a, file_b, len_lim, url_flag):
    with open(file_a, 'r', encoding='utf-8') as f:
        a_str = f.read()
    with open(file_b, 'r', encoding='utf-8') as g:
        b_str = g.read()
    if '<<<' in b_str or '>>>' in b_str:
        b_str = b_str.replace('>>>', '').replace('<<<', '')
    a_str_f = md_match_filter(a_str)
    b_str_f = md_match_filter(b_str)
    s = difflib.SequenceMatcher(None, a_str_f, b_str_f).ratio()
    print('resemblance ratio : {}'.format(s))
    d = difflib.Differ()
    diff = d.compare(a_str, b_str)

    m_str = ''
    same_l = []
    diff_l = []
    count_l = []
    flag = True
    r_count = 0
    for ds in diff:
        # print(ds)
        if flag:
            if ds[0] == ' ':
                same_l.append(ds[2])
            elif ds[0] == '+':
                same_str = ''.join(same_l)
                if len(same_l) >= len_lim and '/images/art_images/' not in same_str and 'f::' not in same_str:
                    if url_flag:
                        m_str += '<<<' + same_str + '>>>'
                        count_l.append(same_str)
                        r_count += 1
                    else:
                        if '](' in same_str:
                            if ')' not in same_str:
                                removed_s = re.sub(r']\(.+$', '', same_str)
                                print(same_str)
                                print(removed_s)
                            else:
                                removed_s = re.sub(r']\(.+?\)', '', same_str)
                            if len(removed_s) >= len_lim:
                                m_str += '<<<' + same_str + '>>>'
                                count_l.append(same_str)
                                r_count += 1
                            else:
                                m_str += same_str
                        else:
                            m_str += '<<<' + same_str + '>>>'
                            count_l.append(same_str)
                            r_count += 1
                else:
                    m_str += same_str
                same_l.clear()
                diff_l.append(ds[2])
                flag = False
        else:
            if ds[0] == ' ':
                m_str += ''.join(diff_l)
                diff_l.clear()
                same_l.append(ds[2])
                flag = True
            elif ds[0] == '+':
                diff_l.append(ds[2])
    if diff_l:
        m_str += ''.join(diff_l)
    if same_l:
        m_str += ''.join(same_l)
    # print(m_str)
    print('len_lim: {} => {} match'.format(len_lim, r_count))
    new_file_path = re.sub(r'\.md', '_rw_ud.md', file_b)
    print(new_file_path)
    with open(new_file_path, 'w', encoding='utf-8') as h:
        h.write(m_str)
    # print(count_l)
    # count_l.sort(key=lambda z: len(z), reverse=True)
    # for cs in count_l:
    #     if len(cs) > 8:
    #         print('{} : {}'.format(len(cs), cs))
    # print(count_l)
    # print('\n'.join(diff))
    return '\n'.join(diff)


def reflect_rewrite_file(before_path):
    with open(before_path.replace('.md', '_rw_ud.md'), 'r', encoding='utf-8') as f:
        a_str = f.read()
        a_str = a_str.replace('<<<', '').replace('>>>', '')
    with open(before_path, 'w', encoding='utf-8') as g:
        g.write(a_str)


# todo: 関連記事の自動作成　複製元との被り防止


if __name__ == '__main__':
    # print(compare_manual_rewrite())
    base_path = 'reibun/md_files/pc/majime/m0_4.md'
    rewrite_path = 'reibun/md_files/pc/majime/m0_dt_hm.md'
    checker_path = rewrite_path.replace('.md', '_rw_ud.md')
    md_resemblance(base_path, rewrite_path, 8, False)
    # pprint.pprint(pickup_chang_str(rewrite_path, checker_path, 5))
    # reflect_rewrite_file(rewrite_path)

