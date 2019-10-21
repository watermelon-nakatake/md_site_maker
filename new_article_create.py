# -*- coding: utf-8 -*-
import os
import re
import article_maker_rb
import reibun_upload
import markdown
import pickle
import datetime

side_bar_list = {'important': [], 'new': [], 'pop': []}
dir_list = ['policy', 'caption', 'majime', 'qa', 'site']
category_str = {'mp_': 'profile', 'm0': 'post', 'm1': 'fmail', 'm2': 'second_mail', 'm3': 'date', 't0_': 'post'}
directory_name = {'policy': 'ポリシー', 'caption': '出会い系の予備知識', 'majime': '出会いメール例文',
                  'qa': '出会い系Ｑ＆Ａ', 'site': '出会い系サイト情報'}
category_name = {'policy': ['ポリシー', 'index.html'], 'caption': ['出会い系の予備知識', 'index.html'],
                 'profile': ['プロフィール例文', 'kakikata_p.html'], 'qa': ['出会い系Ｑ＆Ａ', 'index.html'],
                 'site': ['出会い系サイト情報', 'index.html'], 'post': ['掲示板例文', 'kakikata_t.html'],
                 'f_mail': ['ファーストメール例文', 'kakikata_f.html'], 's_mail': ['２通目以降のメール例文', 'majime.html'],
                 'date': ['デートに誘うメール例文', 'date.html']}
m_index_name = ['date.html', 'index.html', 'kakikata_d.html', 'kakikata_f.html', 'kakikata_p.html', 'kakikata_t.html',
                'majime.html', 'mail-applicaton_test.html']


def make_file_list():
    result = []
    for directory in dir_list:
        file_list = os.listdir('reibun/pc/' + directory)
        for file_name in file_list:
            if '.html' in file_name:
                result.append('reibun/pc/' + directory + '/' + file_name)
    return result


def directory_and_category_select(file_path):
    # file_pathはpc/やamp/以降のpath
    directory = re.sub(r'/.+$', '', file_path)
    category = ''
    if directory != 'majime':
        category = directory
    else:
        file_name = re.sub(r'^.*?/', '', file_path)
        for c_str in category_str:
            if c_str in file_name:
                category = category_str[c_str]
            else:
                category = 'majime'
    return directory, category


def breadcrumb_maker(category, directory, file_name):
    result = ''
    if 'index.html' in file_name:
        return result
    else:
        result += '<div itemscope itemtype="http://data-vocabulary.org/Breadcrumb" class="brd2"><a href="../' +\
                  directory + '/"itemprop="url"><span itemprop="title">' + directory_name[directory]\
                  + '</span></a> &gt;&gt;</div>'
        if directory == 'majime' and file_name not in m_index_name:
            result += '<div itemscope itemtype="http://data-vocabulary.org/Breadcrumb" class="brd2"><a href="../' + \
                      directory + '/' + category_name[category][1] + '"itemprop="url"><span itemprop="title">' + \
                      category_name[category][0] + '</span></a>&gt;&gt;&gt;</div>'
        return result


def file_update():
    upload_list = []
    with open('reibun/pc/template/pc_tmp.html', 'r', encoding='utf-8') as t:
        tmp_str = t.read()
    with open('pickle_pot/title_img_list.pkl', 'rb') as p:
        pk_dec = pickle.load(p)
    side_bar_str = make_side_bar(pk_dec)
    current_files = make_file_list()

    for file_name in current_files:
        with open(file_name, 'r', encoding='utf-8') as f:
            plain_txt = f.read()
            plain_txt = reibun_upload.tab_and_line_feed_remove_from_str(plain_txt)
            title_l = re.findall(r'<title>(.+?)\|出会い系メール例文集</title>', plain_txt)[0]
            if title_l:
                title = title_l[0]
            m_key_l = re.findall(r'<meta name="Keywords" content="(.+?)">', plain_txt)[0]
            if m_key_l:
                m_key = m_key_l[0]
            description_l = re.findall(r'"><meta name="description" content="(.+?)">', plain_txt)[0]
            if description_l:
                description = description_l[0]
            m_key_l = re.findall(r'<meta name="Keywords" content="(.+?)">', plain_txt)[0]
            if m_key_l:
                m_key = m_key_l[0]
            o_key_l = re.findall(r'<!--kw#(.+?)-->', plain_txt)[0]
            if o_key_l:
                o_key = o_key_l[0]
            t_img_l = re.findall(r'<meta property="og:image" content="https://www.demr.jp/pc/images/(.+?)"/>', plain_txt)[0]
            if t_img_l:
                t_img = t_img_l[0]
            h1_l = re.findall(r'<h1 itemprop="headline alternativeHeadline name">(.+?)</h1>', plain_txt)[0]
            if h1_l:
                h1 = h1_l[0]
            mod_l = re.findall(r'<time itemprop="dateModified" datetime="(.+?)">', plain_txt)[0]
            if mod_l:
                mod = mod_l[0]
            content_l = re.findall(r'ゴーヤン</span></span></a></div>(.+?)<!-- maincontentEnd -->', plain_txt)[0]
            if content_l:
                con_str = content_l[0]
            pub_l = re.findall(r'<time itemprop="datePublished" datetime="(.+?)">', plain_txt)[0]
            if pub_l:
                pub = pub_l[0]

            # 以下、modifyでも共通
            new_str = tmp_str.replace('<!--title-->', title)
            new_str = new_str.replace('<!--main-content-->', con_str)
            # new_str = new_str.replace('<h2>', '<!--p-index--><h2>', 1)
            # new_str = article_maker_rb.index_maker(new_str)
            # new_str = article_maker_rb.section_insert(new_str)

            directory, category = directory_and_category_select(file_name)
            new_str = new_str.replace('<!--sb-pop-->', side_bar_str['pop'])
            new_str = new_str.replace('<!--sb-new-->', side_bar_str['new'])
            new_str = new_str.replace('<!--sb-important-->', side_bar_str['important'])
            new_str = new_str.replace('<!--sb-category-->', side_bar_str[category])
            now = datetime.datetime.now()
            new_str = new_str.replace('<!--mod-date-->', mod)
            new_str = new_str.replace('<!--mod-date-j-->', mod.replace('-', '/').replace('/0', '/'))
            new_str = new_str.replace('<!--pub-date-->', pub)
            new_str = new_str.replace('<!--pub-date-j-->', pub.replace('-', '/').replace('/0', '/'))

            bread_str = breadcrumb_maker(category, directory, re.sub(r'^.*?/', '', file_name))
            new_str = new_str.replace('<!--bread-->', bread_str)

            print(new_str)
            return
            """
            with open('reibun/pc/' + file_name, 'w', encoding='utf-8') as g:
                g.write(new_str)
                upload_list.append('pc/' + file_name)
    reibun_upload.ftp_upload(upload_list)
    """


def import_from_markdown():
    md_file_list = ['test.md']
    upload_list = []
    with open('reibun/pc/template/pc_tmp.html', 'r', encoding='utf-8') as t:
        tmp_str = t.read()
    with open('pickle_pot/title_img_list.pkl', 'rb') as p:
        pk_dec = pickle.load(p)
    side_bar_str = make_side_bar(pk_dec)
    for md_file_name in md_file_list:
        with open(md_file_name, 'r', encoding='utf-8') as f:
            plain_txt = f.read()
            if 'd::' in plain_txt:
                description = re.findall(r'd::(.+?)\n', plain_txt)[0]
            if 'f::' in plain_txt:
                file_name = re.findall(r'f::(.+?)\n', plain_txt)[0] + '.html'
            if 'k::' in plain_txt:
                keyword_str = re.findall(r'k::(.+?)\n', plain_txt)[0]
                keyword = keyword_str.split(' ')
                if '' in keyword:
                    keyword.remove('')
                print('keyword')
                print(keyword)
            con_str = markdown.markdown(plain_txt)
            title_l = re.findall('<h1>(.+?)</h1>', con_str)
            if title_l:
                title = title_l[0]
            else:
                print('There is no title!!')
            con_str = re.sub(r'^([\s\S]*)</h1>', '', con_str)

            # 以下、modifyでも共通
            new_str = tmp_str.replace('<!--title-->', title)
            new_str = new_str.replace('<!--main-content-->', con_str)
            new_str = new_str.replace('<h2>', '<!--p-index--><h2>', 1)
            new_str = article_maker_rb.index_maker(new_str)
            new_str = article_maker_rb.section_insert(new_str)
            category = re.sub(r'/.+$', '', file_name)
            new_str = new_str.replace('<!--sb-pop-->', side_bar_str['pop'])
            new_str = new_str.replace('<!--sb-new-->', side_bar_str['new'])
            new_str = new_str.replace('<!--sb-important-->', side_bar_str['important'])
            new_str = new_str.replace('<!--sb-category-->', side_bar_str[category])
            now = datetime.datetime.now()
            new_str = new_str.replace('<!--mod-date-->', str(now)[:-7])
            new_str = new_str.replace('<!--mod-date-j-->', str(now.year) + '/' + str(now.month) + '/' + str(now.day))

            new_str = new_str.replace('<!--pub-date-->', str(now)[:-7])
            new_str = new_str.replace('<!--pub-date-j-->', str(now.year) + '/' + str(now.month) + '/' + str(now.day))

            print(new_str)

            with open('reibun/pc/' + file_name, 'w', encoding='utf-8') as g:
                g.write(new_str)
                upload_list.append('pc/' + file_name)
                new_data = [file_name, title, '', str(now)[:-7]]
                add_pickle_dec(pk_dec, new_data)
    reibun_upload.ftp_upload(upload_list)


def add_pickle_dec(pk_dec, new_data):
    path_list = [pk_dec[x][0] for x in pk_dec]
    if new_data[0] not in path_list:
        pk_dec[len(pk_dec)] = new_data
    return pk_dec


def import_from_evernote(insert_dir, new_file_name):
    directory = os.listdir('/Users/nakataketetsuhiko/Downloads/自分のノート')
    if directory:
        file_name = directory[0]
        with open('reibun/pc/template/pc_tmp.html', 'r', encoding='utf-8') as t:
            tmp_str = t.read()
        with open('/Users/nakataketetsuhiko/Downloads/自分のノート/' + file_name, 'r', encoding='utf-8') as f:
            original_str = f.read()
            title_l = re.findall('<title>(.+?)</title>', original_str)
            if title_l:
                title = title_l[0]
                print('title: ' + title)
            else:
                print('there is no title!')
                return
            content_l = re.findall(r'<body>(.+?)</body>', original_str)
            if content_l:
                content = content_l[0]
            else:
                print('There is no content!')
                return
            keyword_list = re.findall(r'<div>Key:.*?</div>', content)
            if keyword_list:
                keyword_str = re.findall(r'<div>Key:(.*?)</div>', keyword_list[0])
                keyword = keyword_str[0].split(' ')
                keyword.remove('')
                print('keyword')
                print(keyword)
                content = content.replace(keyword_list[0], '')
            else:
                print('there is no keyword!')
                return
            description_list = re.findall(r'<div>Des:.*?</div>', content)
            if description_list:
                description_str = re.findall(r'<div>Des:(.*?)</div>', description_list[0])
                description = description_str[0].strip()
                print('description: ' + description)
                content = content.replace(description_list[0], '')
            else:
                print('There is no description!')
                return
            content = re.sub(r'^<div>', '<p>', content)
            content = re.sub(r'</div><div><br/></div>$', '</p>', content)
            content = re.sub(r'</div>$', '</p>', content)
            content = re.sub(r'</div>$', '</p>', content)
            content = content.replace('<span>', '')
            content = content.replace('</span>', '')
            content = content.replace('<u>', '<a href="">')
            content = content.replace('</u>', '</a>')

            content = re.sub(r'</div><div><br/></div><div><br/></div><div>H(\d) (.+?)</div><div><br/></div><div>',
                             r'</p><h\1>\2</h\1><p>', content)
            content = content.replace('</div><div><br/></div><div>', '</p><p>')
            content = content.replace('</div><div><br/></div><div><br/></div><div>(.', '</p><h2>')
            content = content.replace('</div><div>', '<br>')

            new_str = tmp_str.replace('<!--title-->', title)
            new_str = new_str.replace('<!--main-content-->', content)

            new_str = new_str.replace('<h2>', '<!--p-index--><h2>', 1)
            new_str = article_maker_rb.index_maker(new_str)
            new_str = article_maker_rb.section_insert(new_str)
            # todo: 関連記事挿入

            print(new_str)
            return


def make_xml_site_map(pk_dec):
        data_str = ''
        for id_pk in pk_dec:
            data_str += ''


def make_side_bar_str(id_list, pk_dec):
    result_str = ''
    for use_id in id_list:
        class_add = ''
        if len(pk_dec[use_id][1]) <= 15:
            class_add = ' class="he1"'
        result_str += '<li' + class_add + '><a href="../' + pk_dec[use_id][0] + '">' + pk_dec[use_id][1] + '</a></li>'
    return result_str


def make_side_bar(pk_dec):
    sb_pop = make_side_bar_str(side_bar_list['pop'], pk_dec)
    sb_important = make_side_bar_str(side_bar_list['important'], pk_dec)
    sb_new = make_side_bar_str(side_bar_list['new'], pk_dec)
    result = {'pop': sb_pop, 'important': sb_important, 'new': sb_new}
    category_list = category_search(pk_dec)
    for category in dir_list:
        result[category] = make_side_bar_str(category_list[category], pk_dec)
    return result


def category_search(pk_dec):
    directory_dec = {'policy': [], 'caption': [], 'majime': [], 'qa': [], 'site': []}
    for file_id in pk_dec:
        directory = re.sub(r'/.+$', '', pk_dec[file_id][0])
        directory_dec[directory].append(file_id)
    return directory_dec


def new_article_finish():
    print()
    # todo: 目次の挿入
    # todo: amp作成
    # todo: upload


if __name__ == '__main__':
    # import_from_evernote('majime', 'new_a_test')
    # import_from_markdown()
    # print(make_side_bar_list([1, 3, 4, 138, 142]))
    print(re.sub(r'/.+$', '', 'majime/m0_1.html'))

