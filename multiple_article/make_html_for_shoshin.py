import datetime
import pickle
import random

import markdown
import os
import re


def translate_md_to_html(temp_path, md_path_dir, sub_sex, pub_flag, pub_take_over, html_dir):
    up_file_list = []
    with open('shoshin/pickle_pot/key_dict.pkl', 'rb') as p:
        key_dict = pickle.load(p)
    key_list = [x for x in key_dict]
    select_key = random.sample(key_list, 15)
    recent_art_str = ''.join(
        ['<li><a href="../{}.html">{}</a></li>'.format(x, re.sub(r'<!--.*?-->', '', key_dict[x]['title_str'])) for x in
         select_key])
    if not os.path.exists('shoshin/html_files/' + html_dir):
        os.mkdir('shoshin/html_files/' + html_dir)
    with open(temp_path, 'r', encoding='utf-8') as f:
        temp_str = f.read()
    temp_str = temp_str.replace('<!--new-article-list-->', recent_art_str)
    dt1 = datetime.datetime(2021, 9, 15, 8, 21, 33, 333)
    for md_path in os.listdir(md_path_dir):
        temp = temp_str
        with open(md_path_dir + '/' + md_path, 'r', encoding='utf-8') as m:
            main_str = m.read()
        t_str = re.findall(r't::(.+?)\n', main_str)[0]
        t_str = re.sub(r'<!--.*?-->', '', t_str)
        temp = temp.replace('<!--title-->', t_str)
        d_str = re.findall(r'd::(.+?)\n', main_str)[0]
        temp = temp.replace('<!--description-->', d_str)
        n_str = re.findall(r'n::(.+?)\n', main_str)[0]
        temp = temp.replace('#id__num#', '#' + n_str + '#')
        k_str = re.findall(r'k::(.*?)\n', main_str)[0]
        temp = temp.replace('#key__words#', '#' + k_str + '#')
        re_str_l = re.findall(r"relation_list = '(.*?)'", main_str)
        if re_str_l:
            temp = temp.replace('<!--relation-list-->',
                                '<section><h2><!--keyword-main-noun-->の関連記事</h2><ul>{}</ul></section>'.format(
                                    re_str_l[0].replace('.md', '.html')))
            temp = temp.replace('</section></section><section><h2><!--keyword-main-noun-->',
                                '</section><section><h2><!--keyword-main-noun-->')
        if '<!--keyword-main-noun-->' in temp:
            if "'type': 'only_act'" in main_str:
                key_noun = re.findall(r"'act_noun': '(.+?)'", main_str)
            elif "'type': 'only_obj'" in main_str:
                key_noun = re.findall(r"'obj_noun': '(.+?)'", main_str)
            elif "'type': 'only_sub'" in main_str:
                key_noun = re.findall(r"'sub_noun': '(.+?)'", main_str)
            else:
                key_noun = []
            if key_noun:
                temp = temp.replace('<!--keyword-main-noun-->', key_noun[0])
            else:
                temp = temp.replace('<!--keyword-main-noun-->', 'この記事')
        if 'p::' in main_str:
            pub_str = re.findall(r'p::(.*?)\n', main_str)[0]
        else:
            pub_str = ''
        m_str = re.sub(r'^[\s\S]+?k::.*?\n', '', main_str)
        m_str = re.sub(r'recipe_list = {[\s\S]+$', '', m_str)

        m_str = m_str.replace('%arlist%', '\n')
        m_str = re.sub(r'%l_.+?%([\s\S]+?)\n\n', r'\[st-kaiwa1 r]\1[/st-kaiwa1]\n\n', m_str)
        if sub_sex == 'woman':
            m_str = re.sub(r'%r_.+?%([\s\S]+?)\n\n', r'\[st-kaiwa3]\1[/st-kaiwa3]\n\n', m_str)
            m_str = re.sub(r'%r_\?([\s\S]+?)\n\n', r'\[st-kaiwa3]\1[/st-kaiwa3]\n\n', m_str)
        else:
            m_str = re.sub(r'%r_.+?%([\s\S]+?)\n\n', r'\[st-kaiwa2]\1[/st-kaiwa2]\n\n', m_str)
            m_str = re.sub(r'%r_\?([\s\S]+?)\n\n', r'\[st-kaiwa2]\1[/st-kaiwa2]\n\n', m_str)
        m_str = m_str.replace('[st-kaiwa1 r]\n', '[st-kaiwa1 r]')
        m_str = m_str.replace('[st-kaiwa2]\n', '[st-kaiwa2]')
        m_str = m_str.replace('[st-kaiwa3]\n', '[st-kaiwa3]')
        m_str = m_str.replace('/link/', '/url/')
        m_str = m_str.replace('../area-bbs/', '/area-bbs/')
        m_str = m_str.replace('../../html_files/url/', '../url/')
        m_str = m_str.replace('../url/', '/url/')
        m_str = m_str.replace('.md', '.html')
        fb_link_l = re.findall(r']\((.+?)\)', m_str)
        if fb_link_l:
            for fb_link in fb_link_l:
                if '/' not in fb_link:
                    m_str = m_str.replace('](' + fb_link + ')', '](/friend-with-benefits/' + fb_link + ')')
        m_str = re.sub(r'<!--sw-.+?-->', '', m_str)
        m_str = re.sub(r'<!--rs-.+?-->', '', m_str)

        ht_str = markdown.markdown(m_str)
        ht_str = ht_str.replace('<p>[st-kaiwa2]',
                                '<div class="fr2"><div class="icon"><div class="rm_b rm_2"></div></div><p>')
        ht_str = ht_str.replace('[/st-kaiwa2]</p>', '</p></div>')
        ht_str = ht_str.replace('<p>[st-kaiwa1 r]',
                                '<div class="fl1"><div class="icon"><div class="lm_b lm_2"></div></div><p>')
        ht_str = ht_str.replace('[/st-kaiwa1]</p>', '</p></div>')
        ht_str = ht_str.replace('<em>', '<strong>')
        ht_str = ht_str.replace('</em>', '</strong>')

        ht_str = ht_str.replace('。\n', '。<br/>\n')
        temp = temp.replace('<!--main-->', ht_str)
        if pub_take_over and os.path.exists('shoshin/html_files/' + html_dir + '/' + md_path.replace('.md', '.html')):
            with open('shoshin/html_files/' + html_dir + '/' + md_path.replace('.md', '.html'), 'r',
                      encoding='utf-8') as h:
                old_s = h.read()
            print(old_s)
            old_pub = re.findall(r'<div id="date">(.+?)</div>', old_s)[0]
            temp = temp.replace('<!--mod-time-->', old_pub)
        else:
            print('no file :{}'.format(md_path))
            if pub_flag and pub_str:
                temp = temp.replace('<!--mod-time-->', pub_str)
            else:
                dt1 = dt1 + datetime.timedelta(hours=int(random.random() * 12), minutes=int(random.random() * 60),
                                               seconds=int(random.random() * 59))
                dt_str = dt1.strftime('%Y-%m-%dT%H:%M:%S')
                print(dt_str)
                temp = temp.replace('<!--mod-date-->', dt_str)
                temp = temp.replace('<!--mod-date-j-->', re.sub(r'T.*$', '', dt_str).replace('-', '/'))
        temp = temp.replace('.md"', '"')
        temp = re.sub(r'<!--sw-.+?-->', '', temp)
        # print(temp)
        h_file_name = 'shoshin/html_files/' + html_dir + '/' + md_path.replace('.md', '.html')
        with open(h_file_name, 'w', encoding='utf-8') as g:
            g.write(temp)
            up_file_list.append(h_file_name)
    return up_file_list
