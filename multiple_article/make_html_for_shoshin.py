import datetime
import random

import markdown
import os
import re


def translate_md_to_html(temp_path, md_path_dir, sub_sex, pub_flag, pub_take_over, html_dir):
    if not os.path.exists('shoshin/html_files/' + html_dir):
        os.mkdir('shoshin/html_files/' + html_dir)
    with open(temp_path, 'r', encoding='utf-8') as f:
        temp_str = f.read()
    dt1 = datetime.datetime(2021, 8, 25, 8, 21, 33, 333)
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
        k_str = re.findall(r'k::(.+?)\n', main_str)[0]
        temp = temp.replace('#key__words#', '#' + k_str + '#')
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
        fb_link_l = re.findall(r']\((.+?)\)', m_str)
        if fb_link_l:
            for fb_link in fb_link_l:
                if '/' not in fb_link:
                    m_str = m_str.replace('](' + fb_link + ')', '](/friend-with-benefits/' + fb_link + ')')
        m_str = re.sub(r'<!--sw-.+?-->', '', m_str)
        m_str = re.sub(r'<!--rs-.+?-->', '', m_str)

        ht_str = markdown.markdown(m_str)
        ht_str = ht_str.replace('。\n', '。<br/>\n')
        temp = temp.replace('<!--main-->', ht_str)
        if pub_take_over and os.path.exists('shoshin/html_files/' + html_dir + '/' + md_path.replace('.md', '.html')):
            with open('shoshin/html_files/up_data/' + md_path.replace('.md', '.html'), 'r', encoding='utf-8') as h:
                old_s = h.read()
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
                temp = temp.replace('<!--mod-time-->', dt_str)
        temp = temp.replace('.md"', '"')
        temp = re.sub(r'<!--sw-.+?-->', '', temp)
        # print(temp)
        with open('shoshin/html_files/' + html_dir + '/' + md_path.replace('.md', '.html'), 'w', encoding='utf-8') as g:
            g.write(temp)


if __name__ == '__main__':
    translate_md_to_html('shoshin/wp_temp.html', 'shoshin/md_files/beginner', 'man', pub_flag=True, pub_take_over=True,
                         html_dir='up_data_s')
