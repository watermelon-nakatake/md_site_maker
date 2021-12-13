import datetime
import glob
import pickle
import random
import markdown
import pprint
import csv
import os
import re
import shoshin.main_info
import new_from_md


def translate_md_to_html(temp_path, md_path_dir_l, sub_sex, pub_flag, pub_take_over):
    up_file_list = []
    if not md_path_dir_l:
        md_path_dir_l = ['means', 'beginner']
    with open('shoshin/pickle_pot/key_dict.pkl', 'rb') as p:
        key_dict = pickle.load(p)
    key_list = [x for x in key_dict]
    select_key = random.sample(key_list, 15)
    recent_art_str = ''.join(
        ['<li><a href="../{}.html">{}</a></li>'.format(x, re.sub(r'<!--.*?-->', '', key_dict[x]['title_str'])) for x in
         select_key])
    with open(temp_path, 'r', encoding='utf-8') as f:
        temp_str = f.read()
    temp_str = temp_str.replace('<!--new-article-list-->', recent_art_str)
    dt1 = datetime.datetime(2021, 11, 15, 8, 21, 33, 333)
    for html_dir in md_path_dir_l:
        md_path_dir = 'shoshin/md_files/' + html_dir
        if not os.path.exists('shoshin/html_files/' + html_dir):
            os.mkdir('shoshin/html_files/' + html_dir)
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
            m_str = m_str.replace('.md', '.html')
            m_str = re.sub(r'<!--sw-.+?-->', '', m_str)
            m_str = re.sub(r'<!--rs-.+?-->', '', m_str)

            ht_str = markdown.markdown(m_str)
            ht_str = ht_str.replace('<p>[st-kaiwa2]',
                                    '<div class="fr2"><div class="icon"><div class="rm_b rm_2"></div></div><p>')
            ht_str = ht_str.replace('[/st-kaiwa2]</p>', '</p></div>')
            ht_str = ht_str.replace('<p>[st-kaiwa1 r]',
                                    '<div class="fl1"><div class="icon"><div class="lm_b lm_2"></div></div><p>')
            ht_str = ht_str.replace('[/st-kaiwa1]</p>', '</p></div>')
            ht_str = re.sub(r'<p>(<img.+?>)</p>', r'<div class="alt_img_t">\1</div>', ht_str)
            ht_str = ht_str.replace('<em>', '<strong>')
            ht_str = ht_str.replace('</em>', '</strong>')

            ht_str = ht_str.replace('。\n', '。<br/>\n')
            temp = temp.replace('<!--main-->', ht_str)
            if pub_take_over and os.path.exists(
                    'shoshin/html_files/' + html_dir + '/' + md_path.replace('.md', '.html')):
                with open('shoshin/html_files/' + html_dir + '/' + md_path.replace('.md', '.html'), 'r',
                          encoding='utf-8') as h:
                    old_s = h.read()
                # print(old_s)
                old_pub = re.findall(r'<time itemprop="dateModified" datetime="(.+?)">', old_s)[0]
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
            temp = temp.replace('\n', '')
            # print(temp)
            h_file_name = 'shoshin/html_files/' + html_dir + '/' + md_path.replace('.md', '.html')
            with open(h_file_name, 'w', encoding='utf-8') as g:
                g.write(temp)
                up_file_list.append(h_file_name)
    # make_shoshin_xml_sitemap(pk_dict=)
    return up_file_list


def shoshin_md_to_html(md_list, mod_flag):
    up_file_list = []
    today = datetime.date.today()
    dir_list = ['means', 'beginner']
    if not md_list:
        md_list = []
        for dir_path in dir_list:
            md_list.extend(glob.glob('shoshin/md_files/' + dir_path + '/**.md'))

    with open('shoshin/pickle_pot/key_dict.pkl', 'rb') as k:
        key_dict = pickle.load(k)
    with open('shoshin/pickle_pot/main_data.pkl', 'rb') as p:
        pk_dict = pickle.load(p)
    with open('shoshin/html_files/template/wp_temp.html', 'r', encoding='utf-8') as t:
        temp_str = t.read()
    new_str = shoshin_new_list_maker(pk_dict, key_dict)
    pop_str = shoshin_pop_list_maker(key_dict)
    temp_str = temp_str.replace('<!--new-article-list-->', new_str)
    temp_str = temp_str.replace('<!--pop-article-list-->', pop_str)
    mod_date = ''
    if mod_flag:
        temp_str = temp_str.replace('<!--mod-date-->', str(today))
        temp_str = temp_str.replace('<!--mod-date-j-->', str(today).replace('-', '/'))
        mod_date = str(today)
    # print(temp_str)
    # print(md_list)

    for md_path in md_list:
        # print(md_path)
        temp = temp_str
        md_name = md_path.replace('shoshin/md_files/', '').replace('.md', '')
        dir_name = re.sub(r'^.*/md_files/(.+?)/.*$', r'\1', md_path)
        with open(md_path, 'r', encoding='utf-8') as m:
            main_str = m.read()
        t_str = re.findall(r't::(.+?)\n', main_str)[0]
        t_str = re.sub(r'<!--.*?-->', '', t_str)
        t_str = re.sub(r'<!--.*?-->', '', t_str)
        temp = temp.replace('<!--title-->', t_str)
        d_str = re.findall(r'd::(.+?)\n', main_str)[0]
        d_str = re.sub(r'<!--.*?-->', '', d_str)
        temp = temp.replace('<!--description-->', d_str)
        n_str = re.findall(r'n::(.+?)\n', main_str)[0]
        this_id = int(n_str)
        temp = temp.replace('#id__num#', '#' + n_str + '#')
        k_str = re.findall(r'k::(.*?)\n', main_str)[0]
        temp = temp.replace('#key__words#', '#' + k_str + '#')
        p_str = re.findall(r'p::(.*?)\n', main_str)[0]
        p_str = re.sub(r'T.*$', '', p_str)

        e_str = re.findall(r'e::(.+?)\n', main_str)
        if e_str:
            edit_flag = True
        else:
            if main_str.count('<!--ori-->') > 0:
                edit_flag = True
            else:
                edit_flag = False
        re_str_l = re.findall(r"relation_list = '(.*?)'", main_str)
        if re_str_l:
            temp = temp.replace('<!--relation-list-->',
                                '<section><h2><!--keyword-main-noun-->の関連記事</h2><ul>{}</ul></section>'.format(
                                    re_str_l[0].replace('.md', '.html')))
            temp = temp.replace('</section></section><section><h2><!--keyword-main-noun-->',
                                '</section><section><h2><!--keyword-main-noun-->')
        if '<!--keyword-main-noun-->' in temp and md_name in key_dict:
            key_data = key_dict[md_name]
            if "'type': 'only_act'" in main_str:
                key_noun = key_data['act_noun']
            elif "'type': 'only_obj'" in main_str:
                key_noun = key_data['obj_noun']
            elif "'type': 'only_sub'" in main_str:
                key_noun = key_data['sub_noun']
            elif "'type': 'mix_act'" in main_str:
                key_noun = key_data['all_key']
            else:
                key_noun = ''
            if key_noun:
                if type(key_noun) == str:
                    temp = temp.replace('<!--keyword-main-noun-->', key_noun)
                elif type(key_noun) == list:
                    temp = temp.replace('<!--keyword-main-noun-->', key_noun[0])
                else:
                    temp = temp.replace('<!--keyword-main-noun-->', 'この記事')
            else:
                temp = temp.replace('<!--keyword-main-noun-->', 'この記事')
        m_str = re.sub(r'^[\s\S]+?k::.*?\n', '', main_str)
        m_str = re.sub(r'recipe_list = {[\s\S]+$', '', m_str)

        m_str = m_str.replace('%arlist%', '\n')
        # m_str = re.sub(r'%l_.+?%([\s\S]+?)\n\n', r'\[st-kaiwa1 r]\1[/st-kaiwa1]\n\n', m_str)

        # print(m_str)

        # if dir_name not in ['beginner', 'means']:
        #     m_str = re.sub(r'%r_.+?%([\s\S]+?)\n\n', r'\[st-kaiwa3]\1[/st-kaiwa3]\n\n', m_str)
        #     m_str = re.sub(r'%r_\?([\s\S]+?)\n\n', r'\[st-kaiwa3]\1[/st-kaiwa3]\n\n', m_str)
        # else:
        #     m_str = re.sub(r'%r_.+?%([\s\S]+?)\n\n', r'\[st-kaiwa2]\1[/st-kaiwa2]\n\n', m_str)
        #     m_str = re.sub(r'%r_\?([\s\S]+?)\n\n', r'\[st-kaiwa2]\1[/st-kaiwa2]\n\n', m_str)

        # print('_____________________________________')
        # print(m_str)
        # m_str = m_str.replace('[st-kaiwa1 r]\n', '[st-kaiwa1 r]')
        # m_str = m_str.replace('[st-kaiwa2]\n', '[st-kaiwa2]')
        # m_str = m_str.replace('[st-kaiwa3]\n', '[st-kaiwa3]')
        m_str = m_str.replace('.md', '.html')
        m_str = m_str.replace('../../html_files/', '../')
        m_str = re.sub(r'<!--sw-.+?-->', '', m_str)
        m_str = re.sub(r'<!--rs-.+?-->', '', m_str)

        ht_str = markdown.markdown(m_str)
        ht_str = icon_filter(ht_str)
        # print(ht_str)

        ht_str = ht_str.replace('../../html_files/', '../')
        ht_str = ht_str.replace('<em>', '<strong>')
        ht_str = ht_str.replace('</em>', '</strong>')

        ht_str = ht_str.replace('。\n', '。<br/>\n')
        temp = temp.replace('<!--main-->', ht_str)

        if not mod_flag:
            if this_id in pk_dict:
                temp = temp.replace('<!--mod-date-->', pk_dict[this_id]['mod_date'])
                temp = temp.replace('<!--mod-date-j-->', pk_dict[this_id]['mod_date'].replace('-', '/'))
            else:
                temp = temp.replace('<!--mod-date-->', str(today))
                temp = temp.replace('<!--mod-date-j-->', str(today).replace('-', '/'))
                mod_date = str(today)
        if p_str:
            temp = temp.replace('<!--pub-date-->', p_str)
            temp = temp.replace('<!--pub-date-j-->', p_str.replace('-', '/'))
        else:
            temp = temp.replace('<!--pub-date-->', str(today))
            temp = temp.replace('<!--pub-date-j-->', str(today).replace('-', '/'))
            p_str = str(today)
        temp = temp.replace('.md"', '.html"')
        temp = re.sub(r'<!--sw-.+?-->', '', temp)
        temp = temp.replace('\n', '')

        if this_id in pk_dict:
            pk_dict[this_id]['title'] = t_str
            pk_dict[this_id]['description'] = d_str
            pk_dict[this_id]['edit_flag'] = edit_flag
            if mod_date:
                pk_dict[this_id]['mod_date'] = mod_date
            pk_dict[this_id]['str_len'] = len(ht_str)
        else:
            pk_dict[this_id] = {'category': dir_name,
                                'description': d_str,
                                'edit_flag': edit_flag,
                                'file_path': md_name + '.html',
                                'layout_flag': False,
                                'mod_date': str(today),
                                'pub_date': p_str,
                                'shift_flag': False,
                                'str_len': len(ht_str),
                                'title': t_str}
        if md_name in key_dict:
            if key_dict[md_name]['title_str'] != t_str:
                key_dict[md_name]['title_str'] = t_str

        # print(temp)
        html_name = 'shoshin/html_files/{}.html'.format(md_name)
        # print(html_name)
        with open(html_name, 'w', encoding='utf-8') as g:
            g.write(temp)
            up_file_list.append(html_name)
    # pprint.pprint(pk_dict)
    make_shoshin_xml_sitemap(pk_dict)
    with open('shoshin/pickle_pot/main_data.pkl', 'wb') as s:
        pickle.dump(pk_dict, s)
    with open('shoshin/pickle_pot/main_data.txt', 'w', encoding='utf-8') as tp:
        tp.write(str(pk_dict))
    with open('shoshin/pickle_pot/key_dict.pkl', 'wb') as t:
        pickle.dump(key_dict, t)
    return up_file_list


def icon_filter(html_str):
    r_dict = {'!': '3', '?': '2', 'p': '6'}
    l_dict = {'!': '2', '?': '5', 'p': '3'}
    if '%r_' in html_str:
        r_list = re.findall(r'<p>%r_(.)([\s\S]+?)</p>', html_str)
        for r_row in r_list:
            new_str = r_row[1]
            if new_str.startswith('%'):
                new_str = re.sub(r'^%', '', new_str)
            if new_str.startswith('\n'):
                new_str = re.sub(r'^\n', '', new_str)
            i_str = '<div class="fr2"><div class="icon"><div class="rm_b rm_{}"></div></div><p>{}</p></div>'.format(
                r_dict[r_row[0]], new_str)
            html_str = html_str.replace('<p>%r_{}{}</p>'.format(r_row[0], r_row[1]), i_str)
    if '%l_' in html_str:
        l_list = re.findall(r'<p>%l_(.)([\s\S]+?)</p>', html_str)
        # l_list = list(l_list)
        for l_row in l_list:
            new_str = l_row[1]
            if new_str.startswith('%'):
                new_str = re.sub(r'^%', '', new_str)
            if new_str.startswith('\n'):
                new_str = re.sub(r'^\n', '', new_str)
            i_str2 = '<div class="fl1"><div class="icon"><div class="lm_b lm_{}"></div></div><p>{}</p></div>'.format(
                l_dict[l_row[0]], new_str)
            html_str = html_str.replace('<p>%l_{}{}</p>'.format(l_row[0], l_row[1]), i_str2)
        # print(l_list)
    return html_str


def shoshin_new_list_maker(pk_dict, key_dict):
    key_list = {x + '.html': key_dict[x]['title_str'] for x in key_dict}
    pub_pk = [[pk_dict[x]['file_path'], datetime.datetime.strptime(pk_dict[x]['pub_date'], '%Y-%m-%d')] for x in
              pk_dict if x not in [1, 2, 3, 4, 5, 6, 148]]
    pub_pk.sort(key=lambda x: x[1], reverse=True)
    new_str = ''.join(['<li><a href="../{}">{}</a></li>'.format(x[0], key_list[x[0]]) for x in pub_pk[:15]])
    # print(new_str)
    return new_str


def shoshin_pop_list_maker(key_dict):
    with open('gsc_data/shoshin/p_today.csv') as f:
        reader = csv.reader(f)
        csv_list = [row for row in reader]
    key_list = {x + '.html': key_dict[x]['title_str'] for x in key_dict}
    pop_list = [[x[4].replace('https://www.deaishoshinsha.com/', ''),
                 key_list[x[4].replace('https://www.deaishoshinsha.com/', '')]] for x in csv_list[1:] if
                ('/beginner/' in x[4] or '/means/' in x[4]) and not x[4].endswith('/') and '#' not in x[4]][:16]
    pop_str = ''.join(
        ['<li><a href="../{}">{}</a></li>'.format(x[0], re.sub(r'<!--.*?-->', '', x[1])) for x in pop_list])
    # print(pop_str)
    return pop_str


def make_shoshin_xml_sitemap(pk_dict):
    pd = shoshin.main_info.info_dict
    new_from_md.xml_site_map_maker(pk_dict, pd)


def add_new_article(new_md_list):
    new_md_list = [x for x in new_md_list if '.md' in x]
    now = datetime.datetime.today()
    temp_path = 'shoshin/html_files/template/wp_temp.html'
    with open(temp_path, 'r', encoding='utf-8') as f:
        temp = f.read()
    sub_sex = 'man'
    up_file_list = []
    with open('shoshin/pickle_pot/main_data.pkl', 'rb') as p:
        pk_dict = pickle.load(p)

    for md_path in new_md_list:
        h_file_name = md_path.replace('/md_files/', '/html_files/').replace('.md', '.html')
        with open(md_path, 'r', encoding='utf-8') as m:
            main_str = m.read()

        n_str = re.findall(r'n::(.+?)\n', main_str)[0]
        temp = temp.replace('#id__num#', '#' + n_str + '#')
        this_id = int(n_str)
        t_str = re.findall(r't::(.+?)\n', main_str)[0]
        t_str = re.sub(r'<!--.*?-->', '', t_str)
        pk_dict[this_id]['title'] = re.sub(r'<!--.*?-->', '', t_str)
        temp = temp.replace('<!--title-->', t_str)
        p_str = re.findall(r'p::(.+?)\n', main_str)[0]
        if 'T' in p_str:
            p_str = re.sub(r'T.*$', '', p_str)
        pk_dict[this_id]['pub_date'] = p_str.replace('T', ' ')
        pk_dict[this_id]['mod_date'] = str(now.date())
        d_str = re.findall(r'd::(.+?)\n', main_str)[0]
        temp = temp.replace('<!--description-->', d_str)
        pk_dict[this_id]['description'] = re.sub(r'<!--.*?-->', '', d_str)
        if not pk_dict[this_id]['edit_flag']:
            e_str = re.findall(r'e::(.+?)\n', main_str)
            if e_str:
                pk_dict[this_id]['edit_flag'] = True
            else:
                if main_str.count('<!--ori-->') > 0:
                    pk_dict[this_id]['edit_flag'] = True
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
        m_str = m_str.replace('.md', '.html')
        m_str = re.sub(r'<!--sw-.+?-->', '', m_str)
        m_str = re.sub(r'<!--rs-.+?-->', '', m_str)
        m_str = m_str.replace('<!--ori-->', '')

        ht_str = markdown.markdown(m_str)
        ht_str = ht_str.replace('<p>[st-kaiwa2]',
                                '<div class="fr2"><div class="icon"><div class="rm_b rm_2"></div></div><p>')
        ht_str = ht_str.replace('[/st-kaiwa2]</p>', '</p></div>')
        ht_str = ht_str.replace('<p>[st-kaiwa1 r]',
                                '<div class="fl1"><div class="icon"><div class="lm_b lm_2"></div></div><p>')
        ht_str = ht_str.replace('[/st-kaiwa1]</p>', '</p></div>')
        ht_str = re.sub(r'<p>(<img.+?>)</p>', r'<div class="alt_img_t">\1</div>', ht_str)
        ht_str = ht_str.replace('../../html_files/images/', '../images/')
        ht_str = ht_str.replace('<em>', '<strong>')
        ht_str = ht_str.replace('</em>', '</strong>')

        ht_str = ht_str.replace('。\n', '。<br/>\n')
        temp = temp.replace('<!--main-->', ht_str)

        with open(h_file_name, 'r', encoding='utf-8') as h:
            old_s = h.read()
        # print(old_s)
        recent_art_str = re.findall(r'<h3 class="navi_title">最新記事</h3><ul>.+?</ul>', old_s)[0]
        temp = temp.replace('<h3 class="navi_title">最新記事</h3><ul><!--new-article-list--></ul>', recent_art_str)
        temp = temp.replace('.md"', '"')
        temp = re.sub(r'<!--sw-.+?-->', '', temp)
        temp = temp.replace('<!--pub-date-->', p_str)
        temp = temp.replace('<!--pub-date-j-->', p_str.replace('-', '/'))
        temp = temp.replace('<!--mod-date-->', str(now.date()))
        temp = temp.replace('<!--mod-date-j-->', str(now.year) + '/' + str(now.month) + '/' + str(now.day))
        # print(temp)
        with open(h_file_name, 'w', encoding='utf-8') as g:
            g.write(temp)
            up_file_list.append(h_file_name)
        if pk_dict[int(n_str)]['title'] != t_str:
            old_title = pk_dict[int(n_str)]['title']
            all_html = glob.glob('shoshin/html_files/**/**.html', recursive=True)
            for o_h in all_html:
                with open(o_h, 'r', encoding='utf-8') as oh:
                    o_str = oh.read()
                    if old_title in o_str:
                        o_str = o_str.replace(old_title, t_str)
                        with open(o_h, 'w', encoding='utf-8') as nh:
                            nh.write(o_str)
                        up_file_list.append(o_h)
        with open('shoshin/pickle_pot/main_data.pkl', 'wb') as s:
            pickle.dump(pk_dict, s)
        with open('shoshin/pickle_pot/main_data.txt', 'w', encoding='utf-8') as tp:
            tp.write(str(pk_dict))
        make_shoshin_xml_sitemap(pk_dict)
    return up_file_list


if __name__ == '__main__':
    shoshin_md_to_html([], mod_flag=False)
