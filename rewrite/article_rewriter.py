import re
import shutil
import MeCab
import os
import word_dict
from numpy import random


def md_rewrite(base_md_path, replace_words, target_words, import_wl):
    if import_wl:
        if os.path.getmtime('/Users/tnakatake/PycharmProjects/multiple_article/words_dict.py')\
                > os.path.getmtime('word_dict.py'):
            shutil.copy('/Users/tnakatake/PycharmProjects/multiple_article/words_dict.py', 'word_dict.py')
    sorted_noun_list = []
    conj_dict = {}
    c_used = []
    if replace_words:
        main_re = [[x[0], '<!--main-r-{}-->'.format(i), x[1]] for i, x in enumerate(replace_words)]
    else:
        main_re = []
    before_word = [['ワクワクメール', '<!--wkwk-->'], ['ハッピーメール', '<!--hm-->'], ['Jメール', '<!--jmail-->'],
                   ['PCMAX', '<!--pcmax-->'], ['例文アプリ', '<!--sample-app-->']]
    ignore_list = ['DM']
    ignore_elm = ['<!--there-is-->', '<!--exist-->', '<!--question-->']
    for conj in word_dict.conj_list:
        for c in conj['after']:
            if c not in c_used:
                conj_dict[c] = conj['after'][:conj['after'].index(c)] + conj['after'][conj['after'].index(c) + 1:]
    for word in word_dict.noun_list:
        if word['before'] not in ignore_elm:
            sorted_noun_list.extend(
                [[x, word['before'], word['after'][:word['after'].index(x)] + word['after'][word['after'].index(x) + 1:]]
                 for x in word['after'] if len(x) > 1 and x not in target_words])
    for w in sorted_noun_list:
        if '<!--' in w[0]:
            for y in word_dict.noun_list:
                if y['before'] in w[0]:
                    w[0] = w[0].replace(y['before'], y['after'][0])
                    break
        for q in w[2]:
            if q in ignore_list:
                w[2].remove(q)
    sorted_noun_list = sorted(sorted_noun_list, key=lambda z: len(z[0]), reverse=True)
    # print(sorted_noun_list)
    with open(base_md_path, 'r', encoding='utf-8') as f:
        base_str = f.read()
    # print(base_str)
    row_list = []
    ana_list = []
    s_base = base_str.split('\n')
    for row in s_base:
        n_list = []
        if replace_words:
            for m_r in main_re:
                if m_r[0] in row:
                    row = row.replace(m_r[0], m_r[1])
                    n_list.append([m_r[1], [m_r[2]]])
        for b_s in before_word:
            if b_s[0] in row:
                row = row.replace(b_s[0], b_s[1])
                n_list.append([b_s[1], [b_s[0]]])
        for noun in sorted_noun_list:
            # print(noun)
            if noun[0] in row:
                row = row.replace(noun[0], noun[1])
                n_list.append([noun[1], noun[2]])
        # print(row)
        # print(n_list)
        ana_list.append(row)
        for n_i in n_list:
            row = row.replace(n_i[0], random.choice(n_i[1]))
        row = mecab_filter(row, conj_dict)
        row_list.append(row)
    new_str = '\n'.join(row_list)
    new_str = re.sub(r'(#+)', r'\1 ', new_str)
    new_str = re.sub(r'\n-', '\n- ', new_str)
    new_str = re.sub(r'\n(d::.*?)\n', r'\n\1\ne::\n', new_str)
    new_str = re.sub(r'\n(n::.*?)\n', r'\n', new_str)
    check_non_changed_words(ana_list)
    # print(new_str)
    with open(base_md_path.replace('.md', '_rw_copy.md'), 'w', encoding='utf-8') as g:
        g.write(new_str)


def check_non_changed_words(ana_list):
    m_list = []
    use_list = []
    for sentence in ana_list:
        sentence = re.sub(r'<!--.+?-->', '', sentence)
        sentence = re.sub(r'%\w+', '', sentence)
        sentence = sentence.replace('### ', '').replace('## ', '').replace('<li>', '').replace(
            '</li>', '')
        for m in mecab_list(sentence):
            if m not in use_list:
                m_list.append([m, 0])
                use_list.append(m)
            else:
                m_list[use_list.index(m)] = [m, m_list[use_list.index(m)][1] + 1]
                # print(m_list[use_list.index(m)])
    m_list.sort(key=lambda x: x[1], reverse=True)
    for y in m_list:
        if y[1] > 1 and y[0][1] != '記号' and y[0][1] != '助詞':
            print(y)


def make_word_dict(word_list):
    result = {}
    for row in word_list:
        for word in row['after']:
            if word not in result:
                result[word] = row['before']
    return result


def mecab_filter(sentence_str, conj_dict):
    after_list = []
    m_list = mecab_list(sentence_str)
    for m_data in m_list:
        # print(m_data)
        if m_data[0] in conj_dict and m_data[1] == '接続詞':
            # print(m_data)
            after_list.append(random.choice(conj_dict[m_data[0]]))
        else:
            after_list.append(m_data[0])
    new_str = ''.join(after_list)
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


if __name__ == '__main__':
    md_rewrite('../reibun/md_files/pc/majime/m0_4.md', [['PCMAX', 'ハッピーメール']], ['童貞'], False)
