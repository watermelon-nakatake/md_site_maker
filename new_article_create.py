# -*- coding: utf-8 -*-
import os
import re
import article_maker_rb
import reibun_upload
import markdown
import pickle
import datetime
import copy
import random
import make_article_list

side_bar_list = {'important': [0, 19, 55, 65, 77, 98, 124],
                 'new': [81, 90, 99, 112, 136], 'pop': [22, 24, 25, 30, 34, 38, 56, 100, 104]}
no_side_bar = []
dir_list = ['policy', 'caption', 'majime', 'qa', 'site']
category_str = {'mp_': 'profile', 'm0': 'post', 'm1': 'f_mail', 'm2': 's_mail', 'm3': 'date', 't0_': 'post'}
directory_name = {'policy': 'ポリシー', 'caption': '出会い系の予備知識', 'majime': '出会いメール例文',
                  'qa': '出会い系Ｑ＆Ａ', 'site': '出会い系サイト情報', 'sitepage': '出会い系サイト紹介'}
category_name = {'policy': ['ポリシー', 'index.html'], 'caption': ['出会い系の予備知識', 'index.html'],
                 'profile': ['プロフィール例文', 'kakikata_p.html'], 'qa': ['出会い系Ｑ＆Ａ', 'index.html'],
                 'site': ['出会い系サイト情報', 'index.html'], 'post': ['掲示板例文', 'kakikata_t.html'],
                 'f_mail': ['ファーストメール例文', 'kakikata_f.html'], 's_mail': ['２通目以降のメール例文', 'majime.html'],
                 'date': ['デートに誘うメール例文', 'date.html'], 'how_to': ['出会い系攻略法', 'kakikata_d.html']}
m_index_name = ['date.html', 'index.html', 'kakikata_d.html', 'kakikata_f.html', 'kakikata_p.html', 'kakikata_t.html',
                'majime.html', 'mail-applicaton_test.html']
banner_str = '<section><h2>簡単に出会えるメールが書ける出会い系メール例文アプリ</h2><p>当サイトでご紹介しているメール例文を簡単にコピペして利用できるアプリができました。<br>' \
             'もちろん利用無料です。<br>気になる方はぜひお試しください。</p><div class="center"><a href="../../app/">' \
             '<img class="app_bn1" src="../images/common/app_bn_f.png" alt="出会い系メール例文アプリ"></a></div></section>'


def make_file_list():
    result = []
    for directory in ['sitepage']:  # dir_list:
        file_list = os.listdir('reibun/pc/' + directory)
        for file_name in file_list:
            if '.html' in file_name and '_test' not in file_name and '_copy' not in file_name:
                result.append('reibun/pc/' + directory + '/' + file_name)
    return result


def directory_and_category_select(file_path):
    # file_pathはpc/やamp/以降のpath
    directory_l = re.findall(r'^reibun/pc/(.+?)/.+$', file_path)
    if directory_l:
        directory = directory_l[0]
        directory = directory.replace('reibun/pc/', '')
        file_name = file_path.replace('reibun/pc/', '')
        file_name = re.sub(r'^.*?/', '', file_name)
        print('directory: ' + directory)
        print('file_name: ' + file_name)
        category = make_article_list.search_category(directory, file_name)
    else:
        directory = 'top'
        category = 'top'
    return directory, category


def breadcrumb_maker(category, directory, file_name):
    result = ''
    if 'index.html' in file_name:
        return result
    else:
        result += '<div itemscope itemtype="http://data-vocabulary.org/Breadcrumb" class="brd2"><a href="../' +\
                  directory + '/"itemprop="url"><span itemprop="title">' + directory_name[directory]\
                  + '</span></a> &gt;&gt;</div>'
        if directory == 'majime' and category != 'majime':
            result += '<div itemscope itemtype="http://data-vocabulary.org/Breadcrumb" class="brd2"><a href="../' + \
                      directory + '/' + category_name[category][1] + '"itemprop="url"><span itemprop="title">' + \
                      category_name[category][0] + '</span></a>&gt;&gt;&gt;</div>'
        return result


def file_update():
    upload_list = ['reibun/p_sitemap.xml', 'reibun/pc/css/base7.css', 'reibun/pc/css/pc7.css',
                   'reibun/pc/css/phone7.css',
                   'reibun/pc/sitepage/yyc.html', 'reibun/pc/sitepage/meru-para.html',
                   'reibun/pc/sitepage/wakuwakumail.html', 'reibun/pc/sitepage/loveseach.html',
                   'reibun/pc/sitepage/pcmax.html', 'reibun/pc/sitepage/mintj.html', 'reibun/pc/sitepage/194964.html',
                   'reibun/pc/sitepage/happymail.html',]
    with open('reibun/pc/template/pc_tmp.html', 'r', encoding='utf-8') as t:
        tmp_str = t.read()
    with open('pickle_pot/title_img_list.pkl', 'rb') as p:
        pk_dec = pickle.load(p)
    side_bar_str = make_side_bar(pk_dec)
    current_files = make_file_list()
    current_files.append('reibun/index.html')
    # current_files = ['reibun/pc/sitepage/happymail.html']
    for file_name in current_files:
        print(file_name)
        with open(file_name, 'r', encoding='utf-8') as f:
            plain_txt = f.read()
            plain_txt = reibun_upload.tab_and_line_feed_remove_from_str(plain_txt)
            title_l = re.findall(r'<title>(.+?)\|出会い系メール例文集</title>', plain_txt)
            if title_l:
                title = title_l[0]
            else:
                title = re.findall(r'<title>(.+?)</title>', plain_txt)[0]
            m_key_l = re.findall(r'<meta name="Keywords" content="(.+?)">', plain_txt)
            if m_key_l:
                m_key = m_key_l[0]
            description_l = re.findall(r'"><meta name="description" content="(.+?)">', plain_txt)
            if description_l:
                description = description_l[0]
            m_key_l = re.findall(r'<meta name="keywords" content="(.+?)">', plain_txt)
            if m_key_l:
                m_key = m_key_l[0]
            o_key_l = re.findall(r'<!--kw#.+?-->', plain_txt)
            if o_key_l:
                o_key = o_key_l[0]
            else:
                o_key = ''
            t_img_l = re.findall(r'<meta property="og:image" content="https://www.demr.jp/pc/images/(.+?)" /><head>', plain_txt)
            if t_img_l:
                t_img = t_img_l[0]
            else:
                t_img = 'demr_mgirl_1200x630.jpg'
            h1_l = re.findall(r'<h1 itemprop="headline alternativeHeadline name">(.+?)</h1>', plain_txt)
            if h1_l:
                h1_str = h1_l[0]
            mod_l = re.findall(r'<time itemprop="dateModified" datetime="(.+?)">', plain_txt)
            if mod_l:
                mod = mod_l[0]
            content_l = re.findall(r'ゴーヤン</span></span></a></div>(.+?)<!-- maincontentEnd -->', plain_txt)
            if content_l:
                con_str = content_l[0]
            pub_l = re.findall(r'<time itemprop="datePublished" datetime="(.+?)">', plain_txt)
            if pub_l:
                pub = pub_l[0]

            # 以下、modifyでも共通
            new_str = tmp_str.replace('<!--title-->', title)
            new_str = new_str.replace('<!--meta-key-->', m_key)
            new_str = new_str.replace('<!--description-->', description)
            new_str = new_str.replace('<!--ori-key-->', o_key)
            new_str = new_str.replace('<!--file-path-->', file_name.replace('reibun/pc/', ''))
            new_str = new_str.replace('<!--t-image-->', t_img)
            new_str = new_str.replace('<!--h1-->', h1_str)
            new_str = new_str.replace('<!--main-content-->', con_str)

            # new_str = new_str.replace('<h2>', '<!--p-index--><h2>', 1)
            # new_str = article_maker_rb.index_maker(new_str)
            # new_str = article_maker_rb.section_insert(new_str)

            directory, category = directory_and_category_select(file_name)
            print(directory)
            print(category)
            new_str = new_str.replace('<!--directory-->', directory)
            if category != 'sitepage':
                new_str = new_str.replace('<!--sb-pop-->', side_bar_str['pop'])
                new_str = new_str.replace('<!--sb-new-->', side_bar_str['new'])
                new_str = new_str.replace('<!--sb-important-->', side_bar_str['important'])
                no_sb_cat = ['majime', 'top']
                if category not in no_sb_cat:
                    sb_str = '<div class="leftnav"><div class="sbh">' + category_name[category][0] + '</div><ul>' \
                             + side_bar_str[category] + '</ul></div>'
                    new_str = new_str.replace('<!--sb-category-->', sb_str)
                else:
                    new_str = new_str.replace('<!--sb-category-->', '')
            else:
                new_str = re.sub(r'<div class="navi_brock".+?<!--sb-new--></ul></div></div>', '', new_str)
            now = datetime.datetime.now()
            new_str = new_str.replace('<!--mod-date-->', mod)
            new_str = new_str.replace('<!--mod-date-j-->', mod.replace('-', '/').replace('/0', '/'))
            new_str = new_str.replace('<!--pub-date-->', pub)
            new_str = new_str.replace('<!--pub-date-j-->', pub.replace('-', '/').replace('/0', '/'))
            if '/common/app_bn_f.png' not in new_str:
                if '<section><div class="kanren">' in new_str:
                    new_str = new_str.replace('<section><div class="kanren">',
                                              banner_str + '<section><div class="kanren">')
                else:
                    new_str = new_str.replace('</article>', banner_str + '')
            bread_str = breadcrumb_maker(category, directory, re.sub(r'^.*?/', '', file_name))
            new_str = new_str.replace('<!--bread-->', bread_str)
            # if '<!--index-page-->' in new_str:
            #    new_str = insert_index_page(pk_dec, new_str)
            if file_name == 'reibun/index.html':
                new_str = re.sub(r'href="\.\./\.\./([^"])', r'href="\1', new_str)
                new_str = re.sub(r'href="\.\./\.\./"', 'href="index.html"', new_str)
                new_str = re.sub(r'href="\.\./([^\.])', r'href="pc/\1', new_str)
                new_str = new_str.replace('src="../images/', 'src="pc/images/')
            if '565通' in new_str:
                print('there is 565通')
            print(new_str)
            with open(file_name.replace('reibun/', 'reibun/'), 'w', encoding='utf-8') as g:
                g.write(new_str)
                upload_list.append(file_name)
    # update_xml_site_map(pk_dec)
    print(upload_list)
    # reibun_upload.ftp_upload(upload_list)


def insert_index_page(pk_dec, long_str):
    # todo: indexページの記事紹介の解決後作成
    return long_str


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

            if side_bar_str[category]:
                sb_str = '<div class="leftnav"><div class="sbh">' + category_name[category][0] + '</div><ul>'\
                         + side_bar_str[category] + '</ul></div>'
                new_str = new_str.replace('<!--sb-category-->', sb_str)
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
                pk_dec = add_pickle_dec(pk_dec, new_data)
    update_xml_site_map(pk_dec)
    reibun_upload.ftp_upload(upload_list)


def add_pickle_dec(pk_dec, new_data):
    path_list = [pk_dec[x][0] for x in pk_dec]
    if new_data[0] not in path_list:
        pk_dec[len(pk_dec)] = new_data
    make_article_list.save_data_to_pickle(pk_dec, 'title_img_list')
    make_article_list.save_text_file(pk_dec)
    return pk_dec


def update_xml_site_map(pk_dec):
    data_str = '<?xml version="1.0" encoding="UTF-8"?>' \
               '<urlset xmlns="https://www.sitemaps.org/schemas/sitemap/0.9">\n'
    data_str += '<url><loc>https://www.demr.jp</loc><lastmod>' + str(datetime.date.today()) +\
                '</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>\n'
    data_str += '<url><loc>https://www.demr.jp/app</loc><lastmod>' + str(datetime.date.today()) + \
                '</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>\n'
    for id_pk in pk_dec:
        data_str += '<url><loc>https://www.demr.jp/pc/' + pk_dec[id_pk][0] + '</loc><lastmod>' + pk_dec[id_pk][3] +\
                '</lastmod><changefreq>weekly</changefreq><priority>0.5</priority></url>\n'
    data_str += '</urlset>'
    with open('reibun/p_sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(data_str)


def make_side_bar_str(id_list, pk_dec):
    result_str = ''
    copy_list = copy.deepcopy(id_list)
    if len(copy_list) > 20:
        copy_list = random.sample(copy_list, 20)
    random.shuffle(copy_list)
    for use_id in copy_list:
        class_add = ''
        if len(pk_dec[use_id][1]) <= 15:
            class_add = ' class="he1"'
        result_str += '<li' + class_add + '><a href="../' + pk_dec[use_id][0] + '">' + pk_dec[use_id][1] + '</a></li>'
    return result_str


def make_side_bar(pk_dec):
    sb_pop = make_side_bar_str(side_bar_list['pop'], pk_dec)
    sb_important = make_side_bar_str(side_bar_list['important'], pk_dec)
    sb_new = make_side_bar_str(side_bar_list['new'], pk_dec)
    result = {'pop': sb_pop, 'important': sb_important, 'new': sb_new, 'majime': ''}
    category_list = category_search(pk_dec)
    for category in category_list:
        result[category] = make_side_bar_str(category_list[category], pk_dec)
    return result


def category_search(pk_dec):
    directory_dec = {'policy': [], 'caption': [], 'qa': [], 'site': [], 'post': [], 'f_mail': [], 's_mail': [],
                     'date': [], 'how_to': [], 'profile': [], 'majime': []}
    for file_id in pk_dec:
        directory_dec[pk_dec[file_id][4]].append(file_id)
    return directory_dec


def new_article_finish():
    print()
    # todo: 目次の挿入
    # todo: amp作成
    # todo: upload


def search_id(str_o):
    result = []
    with open('pickle_pot/title_img_list.pkl', 'rb') as p:
        pk_dec = pickle.load(p)
    url_list = re.findall('href="(.+?)"', str_o)
    for p_id in pk_dec:
        for url in url_list:
            if pk_dec[p_id][0] in url:
                result.append(p_id)
    print(result)


if __name__ == '__main__':
    # import_from_evernote('majime', 'new_a_test')
    # import_from_markdown()
    # print(make_side_bar_list([1, 3, 4, 138, 142]))
    # print(re.sub(r'/.+$', '', 'majime/m0_1.html'))
    file_update()
    # t_str = ''
    # search_id(t_str)

