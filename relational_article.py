import re
import os
import make_article_list
import random

up_dir = ['caption/', 'majime/', 'policy/', 'qa/', 'site/']


def pick_up_md_files():
    change_files = []
    for dir_u in up_dir:
        files = os.listdir('md_files/pc/' + dir_u)
        change_files.extend(['md_files/pc/' + dir_u + x for x in files if '_copy' not in x and '_test' not in x and
                             '_ud' not in x])
    return change_files


def pick_up_html_files():
    change_files = []
    for dir_u in up_dir:
        files = os.listdir('reibun/pc/' + dir_u)
        change_files.extend(['reibun/pc/' + dir_u + x for x in files if '_copy' not in x and '_test' not in x and
                             '_ud' not in x])
    return change_files


def change_html_relational_list():
    md_files = pick_up_html_files()
    k = make_article_list.read_pickle_pot('title_img_list')
    pk_dec = {k[x][0]: k[x][1] for x in k}
    for md_path in md_files:
        print('path : ' + md_path)
        with open(md_path, 'r', encoding='utf-8') as f:
            long_str = f.read()
        r_str = re.findall(r'<div class="kanren">(.+?)</div>', long_str)
        if r_str:
            l_str_l = re.findall(r'<li><a href="(.+?)">(.+?)</a></li>', r_str[0])
            if l_str_l:
                for l_str in l_str_l:
                    url = l_str[0]
                    # print(url)
                    if '../' in url:
                        c_url = url.replace('../', '')
                    else:
                        c_url = re.findall(r'reibun/pc/(.+?)/.+?.html', md_path)[0] + '/' + url
                    # print(c_url)
                    now_title = l_str[1]
                    long_str = re.sub('<li><a href="{}">{}</a></li>'.format(url, now_title),
                                      '<li><a href="{}">{}</a></li>'.format(url, pk_dec[c_url]), long_str)
        with open(md_path, 'w', encoding='utf-8') as g:
            g.write(long_str)


def collect_md_relation_title(md_path, pk_data_b):
    pk_data = {pk_data_b[x][0]: pk_data_b[x][1] for x in pk_data_b}
    with open(md_path, 'r', encoding='utf-8') as h:
        md_str = h.read()
    k_txt = re.findall(r'%kanren%\n([\s\S]*?)$', md_str)
    if k_txt:
        k_txt_e = k_txt[0].replace('-[', '- [')
        k_str_l = re.findall(r'- \[(.+?)]\((.+?)\)', k_txt_e)
        if k_str_l:
            if 'coronavirus' not in k_txt[0]:
                k_str_l = insert_new_article_to_relational_list_md(md_str, k_str_l)
            result = ''
            for k_str in k_str_l:
                # print(k_str)
                t_url = k_str[1].replace('../../../reibun/pc/', '')
                # print(pk_data[t_url])
                result += '- [{}]({})\n'.format(pk_data[t_url], k_str[1])
            md_str = md_str.replace(k_txt[0], result + '\n')
    # print(md_str)
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_str)


def change_md_relational_art_list():
    p = pick_up_md_files()
    # print(p)
    k = make_article_list.read_pickle_pot('title_img_list')
    e_k = {k[x][0]: k[x][1] for x in k}
    # print(e_k)
    for m in p:
        # print(m)
        collect_md_relation_title(m, e_k)


def insert_new_article_to_relational_list(file_path):
    html_path = file_path
    if 'coronavirus' not in file_path:
        with open(html_path, 'r', encoding='utf-8') as f:
            long_str = f.read()
        title_l = re.findall(r'<title>(.+?)\|出会い系メール例文集</title>', long_str)
        if title_l:
            title = title_l[0]
        else:
            title = re.findall(r'<title>(.+?)</title>', long_str)[0]
        r_str = re.findall(r'<div class="kanren">(.+?)</div>', long_str)
        if r_str:
            if 'coronavirus' not in r_str[0]:
                l_str_l = re.findall(r'(<li>.+?</li>)', r_str[0])
                if l_str_l:
                    if 'セフレ' in title or '人妻' in title or '主婦' in title:
                        i_text = '<a href="../majime/m4coronavirus_sf.html">' \
                                 'コロナ下でのセフレの作り方と新型コロナの出会い系サイトへの影響</a>'
                    else:
                        i_text = '<a href="../majime/m4coronavirus_gf.html">' \
                                 '新型コロナとオンライン恋愛と婚活 コロナ禍での出会い系攻略法</a>'
                    l_str_l.insert(random.randrange(len(l_str_l) + 1), '<li>{}</li>'.format(i_text))
                    # print(l_str_l)
                    new_str = long_str.replace(r_str[0], ''.join(l_str_l))
                    with open(html_path, 'w', encoding='utf-8') as g:
                        g.write(new_str)


def insert_new_article_to_relational_list_md(long_str, k_str_l):
    title_l = re.findall(r't::(.+?)\n', long_str)
    title = title_l[0]
    if 'セフレ' in title or '人妻' in title or '主婦' in title:
        i_text = ['コロナ下でのセフレの作り方と新型コロナの出会い系サイトへの影響',
                  '../../../reibun/pc/majime/m4coronavirus_sf.html']
    else:
        i_text = ['新型コロナとオンライン恋愛と婚活 コロナ禍での出会い系攻略法',
                  '../../../reibun/pc/majime/m4coronavirus_gf.html']
    k_str_l.insert(random.randrange(len(k_str_l) + 1), i_text)
    # print(k_str_l)
    return k_str_l


if __name__ == '__main__':
    # change_md_relational_art_list()
    # change_html_relational_list()
    for p_file in pick_up_html_files():
        insert_new_article_to_relational_list(p_file)
