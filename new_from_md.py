# -*- coding: utf-8 -*-
import datetime
import pickle
import re
import os
import markdown
from PIL import Image
import time
from email import utils
import common_tool
import make_article_list
import new_article_create
import amp_file_maker
import reibun_upload
import image_upload
import check_mod_date

side_bar_list = {'important': [34, 76, 38, 21, 28, 49, 17, 41, 66, 43],
                 'pop': [11, 117, 19, 107, 25, 74, 67, 98, 23, 73]}
category_name = {'policy': ['ポリシー', 'index.html'], 'caption': ['出会い系の予備知識', 'index.html'],
                 'profile': ['プロフィール例文', 'kakikata_p.html'], 'qa': ['出会い系Ｑ＆Ａ', 'index.html'],
                 'site': ['出会い系サイト情報', 'index.html'], 'post': ['掲示板例文', 'kakikata_t.html'],
                 'f_mail': ['ファーストメール例文', 'kakikata_f.html'], 's_mail': ['２通目以降のメール例文', 'majime.html'],
                 'date': ['デートに誘うメール例文', 'date.html'], 'how_to': ['出会い系攻略法', 'kakikata_d.html']}
up_dir = ['caption/', 'majime/', 'policy/', 'qa/', 'site/', 'images/art_images/']
category_data = {'policy': ['ポリシー', 'index.html', 1], 's_mail': ['２通目以降のメール例文', 'majime.html', 41],
                 'caption': ['出会い系の予備知識', 'index.html', 6], 'profile': ['プロフィール例文', 'kakikata_p.html', 17],
                 'qa': ['出会い系Ｑ＆Ａ', 'index.html', 114], 'site': ['出会い系サイト情報', 'index.html', 122],
                 'post': ['掲示板例文', 'kakikata_t.html', 74], 'f_mail': ['ファーストメール例文', 'kakikata_f.html', 107],
                 'date': ['デートに誘うメール例文', 'date.html', 102], 'how_to': ['出会い系攻略法', 'kakikata_d.html', 39],
                 'ap_mail': ['メール例文アプリ情報', 'mail-applicaton.html', 92],
                 'majime': ['出会い系メール例文', 'index.html', 32], 'sitepage': ['出会い系サイト', 'index.html', 122]}


def main(mod_hour):
    """
    新規markdownファイルやファイル更新でサイト全体とアップデートしてアップロード
    :param mod_hour: 今回更新するファイルの更新時から現時点までの経過時間（時間） int形式
    :return: none
    """
    add_files = ['reibun/index.html', 'reibun/amp/index.html', 'reibun/pc/css/base11.css', 'reibun/pc/css/pc11.css',
                 'reibun/pc/css/phone11.css', 'reibun/p_sitemap.xml']
    mod_list = []
    now = time.time()
    st_time = 60 * 60 * mod_hour
    for dir_path in up_dir[:-1]:
        mod_files = os.listdir('md_files/pc/' + dir_path)
        for file in mod_files:
            if '.md' in file:
                mod_time = os.path.getmtime('md_files/pc/' + dir_path + file)
                if now - mod_time < st_time:
                    print('update: ' + file)
                    with open('md_files/pc/' + dir_path + file, 'r', encoding='utf-8') as h:
                        m_str = h.read()
                        md_title = re.findall(r't::(.+?)\n', m_str)[0]
                    mod_list.append(['md_files/pc/' + dir_path + file, mod_time, md_title])
        for file_a in ['md_files/index.md']:  # , 'new_art_1.md'
            mod_time_a = os.path.getmtime(file_a)
            if now - mod_time_a < st_time:
                print('update: ' + file_a)
                with open('md_files/pc/' + dir_path + file_a, 'r', encoding='utf-8') as g:
                    m_str = g.read()
                    md_title = re.findall(r't::(.+?)\n', m_str)[0]
                mod_list.append([file_a, mod_time_a, md_title])
    mod_list.sort(key=lambda x: x[1], reverse=True)
    print('modify list :')
    print(mod_list)
    upload_list, pk_dec, new_file_data = import_from_markdown([y[0] for y in mod_list])
    upload_list = modify_file_check(now, st_time, upload_list)
    side_bar_dec = make_all_side_bar(pk_dec)
    mod_log = make_article_list.read_pickle_pot('modify_log')
    with open('reibun/pc/majime/index.html', 'r', encoding='utf-8') as f:
        index_str = f.read()
        mod_title = re.findall(r'<div class="sbh">最近の更新記事</div><ul><li><a href=".+?">(.+?)<', index_str)[0]
        print('mod_title : ' + mod_title)
        print('mod_log[3] : ' + re.sub(r'【.+?】', '', mod_log[-1][3]))
        if re.sub(r'【.+?】', '', mod_log[-1][3]) == mod_title:
            print('change only one page')
            insert_sidebar_to_modify_page(side_bar_dec, upload_list)
            change_files = upload_list
            if mod_log[-1][0] in ['reibun/pc/majime/majime.html', 'reibun/pc/majime/index.html']:
                insert_to_index_page(pk_dec)
        else:
            change_files = insert_sidebar_to_existing_art(side_bar_dec, mod_list)
            insert_to_index_page(pk_dec)
    insert_to_top_page()
    xml_site_map_maker(pk_dec)
    make_rss(new_file_data)
    amp_file_maker.amp_maker([x for x in change_files if '/amp/' not in x])
    upload_list.extend(change_files)
    amp_upload = [x.replace('/pc/', '/amp/') for x in upload_list]
    upload_list.extend(amp_upload)
    upload_list.extend(modify_file_check(now, st_time, add_files))
    # todo: 文中に関連記事挿入 card
    upload_list = set(upload_list)
    upload_list = list(upload_list)
    upload_list.sort()
    print(upload_list)
    reibun_upload.ftp_upload(upload_list)
    check_mod_date.make_mod_date_list()


def pick_up_same_name_images(file_path):
    file_name = re.sub(r'.*/(.+?).html', r'\1', file_path)
    img_list = os.listdir('reibun/pc/images/art_images')
    up_list = ['reibun/pc/images/art_images/' + x for x in img_list if file_name in x]
    return up_list


def modify_file_check(now, st_time, file_list):
    result = []
    for file_path in file_list:
        mod_time = os.path.getmtime(file_path)
        print(file_path + ' : ' + str(now - mod_time))
        if now - mod_time < st_time:
            result.append(file_path)
    return result


def icon_filter(long_str):
    long_str = long_str.replace('%l_normal%', '%lm_1%')
    long_str = long_str.replace('%l_!%', '%lm_2%')
    long_str = long_str.replace('%l_?%', '%lm_5%')
    long_str = long_str.replace('%l_good%', '%lm_6%')
    long_str = long_str.replace('%l_angry%', '%lm_4%')
    long_str = long_str.replace('%l_palm%', '%lm_3%')
    long_str = long_str.replace('%l_normal', '%lm_1%')
    long_str = long_str.replace('%l_!', '%lm_2%')
    long_str = long_str.replace('%l_?', '%lm_5%')
    long_str = long_str.replace('%l_good', '%lm_6%')
    long_str = long_str.replace('%l_angry', '%lm_4%')
    long_str = long_str.replace('%l_palm', '%lm_3%')

    long_str = long_str.replace('%r_normal%', '%rm_1%')
    long_str = long_str.replace('%r_!%', '%rm_3%')
    long_str = long_str.replace('%r_?%', '%rm_2%')
    long_str = long_str.replace('%r_good%', '%rm_4%')
    long_str = long_str.replace('%r_angry%', '%rm_5%')
    long_str = long_str.replace('%r_palm%', '%rm_6%')
    long_str = long_str.replace('%r_normal', '%rm_1%')
    long_str = long_str.replace('%r_!', '%rm_3%')
    long_str = long_str.replace('%r_?', '%rm_2%')
    long_str = long_str.replace('%r_good', '%rm_4%')
    long_str = long_str.replace('%r_angry', '%rm_5%')
    long_str = long_str.replace('%r_palm', '%rm_6%')

    long_str = long_str.replace('%rw_?%', '%rw_1%')
    long_str = long_str.replace('%rw_!%', '%rw_2%')
    long_str = long_str.replace('%rw_?', '%rw_1%')
    long_str = long_str.replace('%rw_!', '%rw_2%')

    if '%r_' in long_str or '%l_' in long_str:
        print('There is wrong icon tag !')
        return
    return long_str


def insert_to_top_page():
    today = datetime.date.today()
    mod_log = make_article_list.read_pickle_pot('modify_log')
    latest_art = [x for x in mod_log if x[1] == mod_log[-1][1]]
    latest_art.reverse()
    with open('reibun/index.html', 'r', encoding='utf-8') as f:
        long_str = f.read()
        # 更新記事一覧
        up_str_l = re.findall(r'<ul class="updli">(.+?)</ul>', long_str)
        if up_str_l:
            up_str = up_str_l[0]
            up_data_l = re.findall(r'<li>.+?</li>', up_str)
            latest_date = re.findall(r'^<li>(.+?) \[', up_data_l[0])[0]
            if latest_date == latest_art[0][1].replace('-', '/').replace('/0', '/'):
                replace_str = re.sub(r'<li>' + latest_date + r' \[.+?</li>', '', up_str)
            else:
                replace_str = up_str
                latest_mod = re.findall(r'<li>(.+?) \[.*?<a href="(.+?)"', up_data_l[0])
                if latest_mod[0][1] == latest_art[-1][0].replace('reibun/', ''):
                    replace_str = replace_str.replace(up_data_l[0], '')
            add_str = ''
            for new_art in latest_art:
                status_str = '更新' if new_art[4] == 'mod' else '追加'
                add_str += '<li>{} [{}・<a href="{}">{}</a>]を{}</li>'.format(
                    new_art[1].replace('-', '/').replace('/0', '/'), category_data[new_art[2]][0],
                    new_art[0].replace('reibun/', ''), re.sub(r'【.+?】', '', new_art[3]), status_str)
            long_str = long_str.replace(up_str, add_str + replace_str)
            insert_to_amp_top(add_str + replace_str)
            long_str = re.sub(r'<time itemprop="dateModified" datetime=".+?">.+?</time>',
                              '<time itemprop="dateModified" datetime="' + str(today) + '">'
                              + str(today).replace('-0', '/').replace('-', '/') + '</time>', long_str)
        with open('reibun/index.html', 'w', encoding='utf-8') as g:
            g.write(long_str)


def insert_to_amp_top(replace_str):
    today = datetime.date.today()
    with open('reibun/index.html', 'r', encoding='utf-8') as f:
        long_str = f.read()
        long_str = re.sub(r'<ul class="updli">.+?</ul>', '<ul class="updli">' + replace_str + '</ul>', long_str)
        long_str = re.sub(r'</amp-img>.+?</time>',
                          '</amp-img>' + str(today).replace('-0', '/').replace('-', '/') + '</time>', long_str)
        long_str = re.sub(r'"dateModified": ".+?","description":',
                          '"dateModified": "' + str(today) + '","description":', long_str)

        with open('reibun/index.html', 'w', encoding='utf-8') as g:
            g.write(long_str)


def insert_to_index_page(pk_dec):
    h_dec = {'policy': [], 'caption': [], 'qa': [], 'site': [], 'post': [], 'f_mail': [], 's_mail': [],
             'date': [], 'how_to': [], 'profile': [], 'majime': [], 'ap_mail': []}
    category_list = ['ap_mail', 'profile', 'post', 'f_mail', 's_mail', 'date', 'how_to', 'site', 'caption', 'qa',
                     'policy', 'majime']
    for id_num in pk_dec:
        h_dec[pk_dec[id_num][4]].append([pk_dec[id_num][0], pk_dec[id_num][1]])
    for category in h_dec:
        h_dec[category].sort(key=lambda x: x[0])
    # html site map
    with open('reibun/pc/policy/sitemap.html', 'r', encoding='utf-8') as f:
        long_str = f.read()
        long_str = reibun_upload.tab_and_line_feed_remove_from_str(long_str)
        h_str = '<ul class="arlist" id="deaikei"><li><a href="{}">{}</a><ul>'.format(pk_dec[32][0], pk_dec[32][1])
        for category in category_list:
            if category != 'majime':
                h_str += '<li><a href="{}">{}</a><ul>'.format(pk_dec[category_data[category][2]][0],
                                                              pk_dec[category_data[category][2]][1])
                if h_dec[category]:
                    for page in h_dec[category]:
                        if 'index.html' not in page[0]:
                            h_str += '<li><a href="{}">{}</a></li>'.format(page[0], page[1])
                h_str += '</ul></li>'
        h_str += '</ul>'
        h_str = h_str.replace('</li><li><a href="site/index.html">',
                              '</li></ul></li><li><a href="site/index.html">')
        h_str = h_str.replace('<a href="', '<a href="../')
        long_str = re.sub('</h2>.*?</section>', '</h2>' + h_str + '</section>', long_str)
        with open('reibun/pc/policy/sitemap.html', 'w', encoding='utf-8') as g:
            g.write(long_str)
    # category page
    for cat in category_list:
        if cat in ['ap_mail', 'profile', 'post', 'f_mail', 's_mail', 'date', 'how_to']:
            directory = 'majime'
        else:
            directory = cat
        if cat != 'majime':
            with open('reibun/pc/' + directory + '/' + category_data[cat][1], 'r', encoding='utf-8') as h:
                long_str = h.read()
                long_str = reibun_upload.tab_and_line_feed_remove_from_str(long_str)
                cat_str = cat_index_str_maker(h_dec[cat], directory)
                long_str = re.sub(r'<!--index/s-->.*?<!--index/e-->', '<!--index/s-->' + cat_str + '<!--index/e-->',
                                  long_str)
                with open('reibun/pc/' + directory + '/' + category_data[cat][1], 'w', encoding='utf-8') as k:
                    k.write(long_str)
        else:
            with open('reibun/pc/majime/index.html', 'r', encoding='utf-8') as i:
                long_str = i.read()
                long_str = reibun_upload.tab_and_line_feed_remove_from_str(long_str)
                for m_cat in ['ap_mail', 'profile', 'post', 'f_mail', 's_mail', 'date', 'how_to', 'majime']:
                    cat_str_m = cat_index_str_maker(h_dec[m_cat], directory)
                    long_str = re.sub(r'<!--' + m_cat + '-i/s-->.*?<!--' + m_cat + '-i/e-->',
                                      '<!--' + m_cat + '-i/s-->' + cat_str_m.replace(' id="cat_index"', '')
                                      + '<!--' + m_cat + '-i/e-->',
                                      long_str)
                with open('reibun/pc/majime/index.html', 'w', encoding='utf-8') as j:
                    j.write(long_str)


def xml_site_map_maker(pk_dec):
    pk_list = [[pk_dec[x][0], pk_dec[x][3]] for x in pk_dec]
    pk_list.sort(key=lambda y: y[0])
    now = datetime.datetime.now()
    xml_str = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="https://www.sitemaps.org/schemas/sitemap/0.9">' \
              '<url><loc>https://www.demr.jp</loc><lastmod>' + str(now.date()) \
              + '</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>'
    for page in pk_list:
        if 'index.html' in page[0]:
            page_url = page[0].replace('/index.html', '/')
        else:
            page_url = page[0]
        xml_str += '<url><loc>https://www.demr.jp/pc/' + page_url + '</loc><lastmod>' + page[1] \
                   + '</lastmod><changefreq>weekly</changefreq><priority>0.5</priority></url>'
    xml_str += '</urlset>'
    with open('reibun/p_sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(xml_str)


def cat_index_str_maker(cat_dec, directory):
    cat_str = '<ul class="libut" id="cat_index">'
    for page_i in cat_dec:
        if len(page_i) < 3:
            cat_str += '<li><a href="{}">{}</a></li>'.format(page_i[0].replace(directory + '/', ''),
                                                             re.sub(r'【.+?】', '', page_i[1]))
        else:
            cat_str += '<li><a href="{}">{}<span>{}</span></a></li>'.format(page_i[0].replace(directory + '/', ''),
                                                                            re.sub(r'【.+?】', '', page_i[1]), page_i[2])
    cat_str += '</ul>'
    return cat_str


def insert_sidebar_to_existing_art(side_bar_dec, mod_list):
    change_files = []
    for dir_r in up_dir[:-1]:
        r_files = os.listdir('reibun/pc/' + dir_r)
        for r_file in r_files:
            if '_copy' not in r_file:
                with open('reibun/pc/' + dir_r + '/' + r_file, 'r', encoding='utf-8') as f:
                    long_str = f.read()
                    long_str = reibun_upload.tab_and_line_feed_remove_from_str(long_str)
                    str_l = re.findall(
                        r'<body class="(.+?)" itemscope="itemscope" itemtype="https://schema.org/WebPage">',
                        long_str)
                    if str_l:
                        category = str_l[0]
                    long_str = insert_sidebar_to_str(long_str, side_bar_dec, category)
                    long_str = modify_relation_list(long_str, mod_list)
                    with open('reibun/pc/' + dir_r + '/' + r_file, 'w', encoding='utf-8') as g:
                        g.write(long_str)
                        change_files.append('reibun/pc/' + dir_r + r_file)
                with open('reibun/amp/' + dir_r + r_file, 'r', encoding='utf-8') as h:
                    amp_str = h.read()
                    amp_str = insert_sidebar_to_str(amp_str, side_bar_dec, category)
                    with open('reibun/amp/' + dir_r + r_file, 'w', encoding='utf-8') as i:
                        i.write(amp_str)
    change_files.extend([x.replace('/pc/', '/amp/') for x in change_files])
    return change_files


def insert_sidebar_to_str(long_str, side_bar_dec, category):
    long_str = re.sub(r'"sbh">人気記事</div><ul>.+?</ul></div>',
                      '"sbh">人気記事</div><ul>' + side_bar_dec['pop'] + '</ul></div>', long_str)
    long_str = re.sub(r'"sbh">重要記事</div><ul>.+?</ul></div>',
                      '"sbh">重要記事</div><ul>' + side_bar_dec['important'] + '</ul></div>', long_str)
    long_str = re.sub(r'"sbh">最近の更新記事</div><ul>.+?</ul></div>',
                      '"sbh">最近の更新記事</div><ul>' + side_bar_dec['new'] + '</ul></div>', long_str)
    if category != 'majime':
        long_str = re.sub(r'<div class="leftnav"><div class="sbh cat-i">.*?</div><ul>.*?</ul></div>',
                          '<div class="leftnav"><div class="sbh cat-i">' + category_name[category][0]
                          + '</div><ul>' + side_bar_dec[category] + '</ul></div>', long_str)
    return long_str


def insert_sidebar_to_modify_page(side_bar_dec, upload_list):
    for r_file in upload_list:
        print(r_file)
        if '.html' in r_file:
            with open(r_file, 'r', encoding='utf-8') as f:
                long_str = f.read()
                long_str = reibun_upload.tab_and_line_feed_remove_from_str(long_str)
                str_l = re.findall(r'<body class="(.+?)" itemscope="itemscope" itemtype="https://schema.org/WebPage">',
                                   long_str)
                if str_l:
                    category = str_l[0]
                long_str = re.sub(r'"sbh">人気記事</div><ul>.+?</ul></div>',
                                  '"sbh">人気記事</div><ul>' + side_bar_dec['pop'] + '</ul></div>', long_str)
                long_str = re.sub(r'"sbh">重要記事</div><ul>.+?</ul></div>',
                                  '"sbh">重要記事</div><ul>' + side_bar_dec['important'] + '</ul></div>', long_str)
                long_str = re.sub(r'"sbh">最近の更新記事</div><ul>.+?</ul></div>',
                                  '"sbh">最近の更新記事</div><ul>' + side_bar_dec['new'] + '</ul></div>', long_str)
                if category != 'majime':
                    long_str = re.sub(r'<div class="leftnav"><div class="sbh cat-i">.*?</div><ul>.*?</ul></div>',
                                      '<div class="leftnav"><div class="sbh cat-i">' + category_name[category][0]
                                      + '</div><ul>' + side_bar_dec[category] + '</ul></div>', long_str)
                with open(r_file, 'w', encoding='utf-8') as g:
                    g.write(long_str)


def make_all_side_bar(pk_dec):
    cat_dec = {'policy': [], 'caption': [], 'qa': [], 'site': [], 'post': [], 'f_mail': [], 's_mail': [],
               'date': [], 'how_to': [], 'profile': [], 'majime': []}
    # pk_list = []
    # for i in pk_dec:
    #    pk_list.append(pk_dec[i])
    pk_list = [pk_dec[i] for i in pk_dec if pk_dec[i][4] != 'policy']

    sorted_list = sorted(pk_list, key=lambda x: datetime.date(datetime.datetime.strptime(x[3], '%Y-%m-%d').year,
                                                              datetime.datetime.strptime(x[3], '%Y-%m-%d').month,
                                                              datetime.datetime.strptime(x[3], '%Y-%m-%d').day),
                         reverse=True)
    new_art = sorted_list[:10]
    new_str = ''.join(['<li><a href="../{}">{}</a></li>'.format(y[0], re.sub(r'【.+?】', '', y[1])) for y in new_art])
    for id_pk in pk_dec:
        cat_dec[pk_dec[id_pk][4]].append('<li><a href="../{}">{}</a></li>'.format(
            pk_dec[id_pk][0], re.sub(r'【.+?】', '', pk_dec[id_pk][1])))
    result_dec = {x: ''.join(cat_dec[x]) for x in cat_dec}
    result_dec['new'] = new_str
    for z in side_bar_list:
        result_dec[z] = ''.join(
            ['<li><a href="../{}">{}</a></li>'.format(pk_dec[use_id][0],
                                                      re.sub(r'【.+?】', '', pk_dec[use_id][1])) for use_id in
             side_bar_list[z]])
    return result_dec


def make_rss(new_file_data):
    now = datetime.datetime.now()
    now_str = str(now)[:-7]
    # rss1.0
    with open('reibun/pc/template/rss10.xml', 'r', encoding='utf-8') as f:
        rss1_str = f.read()
        if new_file_data:
            rss1_str = re.sub(r'<dc:date>.*?</dc:date>', '<dc:date>' + now_str + ' +9:00</dc:date>', rss1_str)
            list_str_l = re.findall(r'<rdf:Seq>.*?</rdf:Seq>', rss1_str)
            url_list = re.findall(r'<rdf:li rdf:resource=".+?" />', list_str_l[0])
            item_list_s = re.findall(r'</channel>.+?</rdf:RDF>', rss1_str)[0]
            item_list = re.findall(r'<item rdf:about=".+?</item>', item_list_s)
            if len(url_list) + len(new_file_data) >= 10:
                url_list = url_list[:-(len(url_list) + len(new_file_data) - 10)]
            for new_data in new_file_data:
                url_list.insert(0, '<rdf:li rdf:resource="https://www.demr.jp/pc/' + new_data[0] + '" />')
                item_list.insert(0, '<item rdf:about="https://www.demr.jp/pc/{}"><title>{}</title><link>{}</link>'
                                    '<description><![CDATA[{}]]></description><dc:creator>mail@demr.jp (goyan)</dc:creator>'
                                    '<dc:date>{}</dc:date></item>'.format(new_data[0], new_data[1], new_data[0],
                                                                          new_data[2], now_str))
            rss1_str = rss1_str.replace(list_str_l[0], '<rdf:Seq>' + ''.join(url_list) + '</rdf:Seq>')
            rss1_str = rss1_str.replace(item_list_s, '</channel>' + ''.join(item_list) + '<</rdf:RDF>')
        else:
            rss1_str = re.sub(r'<items><rdf:Seq><rdf:li rdf:resource="記事1のURL" /></rdf:Seq></items>',
                              r'<items><rdf:Seq></rdf:Seq></items>', rss1_str)
            rss1_str = re.sub(r'</channel>.+?</rdf:RDF>',
                              r'</channel></rdf:RDF>', rss1_str)
        with open('reibun/rss10.xml', 'w', encoding='utf-8') as g:
            g.write(rss1_str)
    # rss2.0
    with open('reibun/pc/template/rss20.xml', 'r', encoding='utf-8') as h:
        rss2_str = h.read()
        if new_file_data:
            now_j = now + datetime.timedelta(hours=9)
            now_tuple = now_j.timetuple()
            now_timestamp = time.mktime(now_tuple)
            rfc_str = utils.formatdate(now_timestamp)[:-6]
            item_list_2 = re.findall(r'<item>.+?</item>', rss2_str)
            if len(item_list_2) + len(new_file_data) >= 10:
                item_list_2 = item_list_2[:-(len(item_list_2) + len(new_file_data) - 10)]
            for new_data in new_file_data:
                item_list_2.insert(0, '<item><title>{}</title><link>https://www.demr.jp/pc/{}</link><description>{}'
                                      '</description><pubDate>{} +0900</pubDate></item>'.format(new_data[1],
                                                                                                new_data[0],
                                                                                                new_data[2], rfc_str))
            rss2_str = re.sub(r'<item>.*</item>', ''.join(item_list_2), rss2_str)
        else:
            rss2_str = re.sub(r'<item>.+?</channel>', r'</channel>', rss2_str)
        with open('reibun/rss20.xml', 'w', encoding='utf-8') as i:
            i.write(rss2_str)
    # atom
    with open('reibun/pc/template/atom.xml', 'r', encoding='utf-8') as j:
        atom_str = j.read()
        if new_file_data:
            atom_str = re.sub(r'</title><updated>.*?</updated><link', '</title><updated>' + now_str + '</updated><link',
                              atom_str)
            item_list_a = re.findall(r'<entry>.+?</entry>', atom_str)
            if len(item_list_a) + len(new_file_data) >= 10:
                item_list_a = item_list_a[:-(len(item_list_a) + len(new_file_data) - 10)]
            for new_data in new_file_data:
                item_list_a.insert(0, "<entry><id>demr.jp/pc/{}</id><title>{}</title><link rel='alternate' "
                                      "type='text/html' href='https://www.demr.jp/pc/{}' /><updated>{}</updated>"
                                      "<summary>{}</summary></entry>".format(new_data[0], new_data[1], new_data[0],
                                                                             now_str, new_data[2]))
            atom_str = re.sub(r'<entry>.*</entry>', ''.join(item_list_a), atom_str)
        else:
            atom_str = re.sub(r'<entry>.*?</entry>', '<entry></entry>', atom_str)
        with open('reibun/atom.xml', 'w', encoding='utf-8') as k:
            k.write(atom_str)


def insert_tag_to_upper_anchor(long_str):
    top_str_l = re.findall(r'</h1>.+?<div id="mokujio"', long_str)
    if '<a href="#sc' in top_str_l[0]:
        a_str_l = re.findall(r'<a href="#.+?</a>', top_str_l[0])
        for a_str in a_str_l:
            r_str = a_str
            if 'class=' not in a_str:
                l_text = re.findall(r'>(.+?)<', a_str)[0]
                g_tag = "gtag('event','click',{'event_category':'inner_anchor','event_label':'" + l_text + "'});"
                r_str = re.sub(r'<a href="(.+?)">',
                               r'<a href="\1" class="upper_anchor" onClick="' + g_tag + '">', r_str)
                long_str = long_str.replace(a_str, r_str)
    return long_str


def insert_markdown_anchor(long_str):
    a_str_l = re.findall(r'href="#[^s].+?"', long_str)
    if a_str_l:
        index_str_l = re.findall(r'<nav id="mokuji">.+?</nav>', long_str)
        index_list = [[str_i[1], str_i[0]] for str_i in re.findall(r'<a href="(.+?)">(.+?)</a>', index_str_l[0])]
        for a_str in a_str_l:
            a_text = re.sub(r'href="#(.+?)"', r'\1', a_str)
            r_str = re.sub(r'href="#(.+?)"', 'href="' + [x[1] for x in index_list if x[0] == a_text][0] + '"',
                           a_str)
            long_str = long_str.replace(a_str, r_str)
    return long_str


def top_page_filter(long_str):
    long_str = long_str.replace('"../../"', './')
    long_str = long_str.replace('"../../', '"')
    long_str = long_str.replace('"../', '"../pc/')
    return long_str


def insert_page_card(long_str, pk_dec):
    if '[card]' in long_str:
        card_str_l = re.findall(r'\[card]\(.+?\)', long_str)
        if card_str_l:
            card_str = card_str_l[0]
            card_url_list = re.findall(r'\((.+?)\)', card_str)
            if card_url_list:
                card_url = card_url_list[0]
                c_url = card_url.replace('../../../', '')
                for page_id in pk_dec:
                    if pk_dec[page_id][0] in c_url:
                        url_str = c_url.replace('reibun/pc/', '../')
                        img_str = re.sub(r'reibun/pc/.+?/(.+?).html', r'../images/art_images/\1_thumb.jpg', c_url)
                        replace_str = '<div class="ar_card"><a href="{}"><div class="ar_in"><div class="ac_img">' \
                                      '<img src="{}" alt="{}"></div><div class="ac_r"><span class="p_title">{}</span>' \
                                      '<span class="ar_dis">{}</span></div></div></a>' \
                                      '</div>'.format(url_str, img_str, pk_dec[page_id][1], pk_dec[page_id][1],
                                                      pk_dec[page_id][5][:100] + '...')
                        print(replace_str)
                        long_str = long_str.replace(card_str, replace_str)
    return long_str


def import_from_markdown(md_file_list):
    upload_list = []
    new_file_data = []
    with open('reibun/pc/template/pc_tmp.html', 'r', encoding='utf-8') as t:
        tmp_str = t.read()
    with open('pickle_pot/title_img_list.pkl', 'rb') as p:
        pk_dec = pickle.load(p)
    for md_file_path in md_file_list:
        print(md_file_path)
        with open(md_file_path, 'r', encoding='utf-8') as f:
            plain_txt = f.read()
            md_replace_str = plain_txt
            plain_txt = re.sub(r'\[]\([\s\S]*?\)', '', plain_txt)
            if 'd::' in plain_txt:
                description = re.findall(r'd::(.+?)\n', plain_txt)[0]
            if 'p::' in plain_txt:
                pub_date = re.findall(r'p::(.+?)\n', plain_txt)[0]
            if 'f::' in plain_txt:
                if 'new_art' in md_file_path:
                    file_name_l = re.findall(r'f::(.+?)\n', plain_txt)
                    if file_name_l:
                        if '.html' in file_name_l[0]:
                            file_name = file_name_l[0]
                        else:
                            file_name = file_name_l[0] + '.html'
                else:
                    file_name = md_file_path.replace('md_files/pc/', '').replace('.md', '.html')
            if 'k::' in plain_txt:
                keyword_str = re.findall(r'k::(.+?)\n', plain_txt)[0]
                if '&' in keyword_str:
                    print('There is "&" !')
                keyword = keyword_str.split(' ')
                if '' in keyword:
                    keyword.remove('')
            title_l = re.findall(r't::(.+?)\n', plain_txt)
            if title_l:
                title_str = title_l[0]
            else:
                print('There is no title!!')
            plain_txt = plain_txt.replace(r'%app_b%', '<div class="center"><a href="../../app/"><img class="app_bn1" '
                                                      'src="../images/common/app_bn_f.png" alt="出会い系メール例文アプリ">'
                                                      '</a></div>')
            if '%arlist' in plain_txt:
                arlist_o_l = re.findall(r'%arlist%\n([\s\S]*?)\n\n', plain_txt)
                if arlist_o_l:
                    for arlist_o in arlist_o_l:
                        if '%%%' in arlist_o:
                            arlist_l = re.findall(r'- (.*?)\n', arlist_o)
                            for arlist in arlist_l:
                                if '%%%' in arlist:
                                    ar_re = re.sub(r'(.+?)%%%', r'<em>\1</em><br />', arlist)
                                    plain_txt = plain_txt.replace(arlist, ar_re)
                plain_txt = re.sub(r'%arlist%\n([\s\S]*?)\n\n', r'<!--arlist-->\n\n\n\1\n\n<!--e/arlist-->', plain_txt)
                plain_txt = re.sub(r'%arlist_b%\n([\s\S]*?)\n\n', r'<!--arlist-b-->\n\n\n\1\n\n<!--e/arlist_b-->',
                                   plain_txt)
            plain_txt = re.sub(r'%kanren%\n([\s\S]*?)\n\n', r'<!--kanren-->\n\n\n\1\n\n<!--e/kanren-->', plain_txt)
            plain_txt = re.sub(r'%btnli%\n([\s\S]*?)\n\n', r'<!--btnli-->\n\n\n\1\n\n<!--e/btnli-->', plain_txt)
            plain_txt = re.sub(r'%point%\n([\s\S]*?)\n\n', r'<!--point-->\n\n\n\1\n\n<!--e/point-->', plain_txt)
            plain_txt = re.sub(r'%matome%\n([\s\S]*?)\n\n', r'<!--matome-->\n\n\n\1\n\n<!--e/matome-->', plain_txt)
            plain_txt = re.sub(r'%p%\n([\s\S]*?)\n\n', r'<!--point_i-->\n\n\n\1\n\n<!--e/point_i-->', plain_txt)

            plain_txt = icon_filter(plain_txt)
            plain_txt = re.sub(r'%rm_(\d)%([\s\S]+?)\n\n',
                               r'<!--rm_\1-->\n\n\2\n\n<!--e/rm-->\n\n\n', plain_txt)
            plain_txt = re.sub(r'%lm_(\d)%([\s\S]+?)\n\n',
                               r'<!--lm_\1-->\n\n\2\n\n<!--e/lm-->\n\n\n', plain_txt)
            plain_txt = re.sub(r'%rw_(\d)%([\s\S]+?)\n\n',
                               r'<!--rw_\1-->\n\n\2\n\n<!--e/rw-->\n\n\n', plain_txt)
            plain_txt = plain_txt.replace('%sample%', '<!--sample/s-->')
            plain_txt = plain_txt.replace('%sample/e%', '<!--sample/e-->')

            plain_txt = mail_sample_replace(plain_txt)
            plain_txt = strong_insert_filter(plain_txt)

            # card挿入
            plain_txt = insert_page_card(plain_txt, pk_dec)

            # コメントアウト削除
            plain_txt = re.sub(r'\(\)\[.*?]\n', '', plain_txt)
            plain_txt = re.sub(r'\n(<!--.+?-->)\n', r'\n\1', plain_txt)
            plain_txt = re.sub(r'>[\s]+?<', '><', plain_txt)

            print(plain_txt)
            print('markdown start!')
            con_str = markdown.markdown(plain_txt, extensions=['tables'])
            print(con_str)
            con_str = con_str.replace('\n', '')
            con_str = re.sub(r'^([\s\S]*)</h1>', '', con_str)

            directory, category = common_tool.directory_and_category_select('reibun/pc/' + file_name)
            title = re.sub(r'%(.+?)%', r'【\1】', title_str)
            new_str = tmp_str.replace('<!--title-->', title)
            new_str = new_str.replace('<!--h1-->', title)  # titleから()削除しないver.
            new_str = new_str.replace('<!--meta-key-->', ','.join(keyword))
            new_str = new_str.replace('<!--file-path-->', file_name)
            new_str = new_str.replace('<!--category-->', category)

            new_str = new_str.replace('<!--main-content-->', con_str + '<!--last-section-->')
            new_str = new_str.replace('<h2>', '<!--p-index--><h2>', 1)
            new_str = common_tool.index_maker(new_str)
            new_str = common_tool.section_insert(new_str)
            if '"mokuji"' in new_str:
                new_str = insert_markdown_anchor(new_str)
                new_str = insert_tag_to_upper_anchor(new_str)
            if category != 'majime':
                new_str = new_str.replace('<!--sb-category-->', '<div class="leftnav"><div class="sbh cat-i"></div>'
                                                                '<ul></ul></div>')
            else:
                new_str = new_str.replace('<!--sb-category-->', '')

            now = datetime.datetime.now()
            new_str = new_str.replace('<!--mod-date-->', str(now.date()))
            new_str = new_str.replace('<!--mod-date-j-->', str(now.year) + '/' + str(now.month) + '/' + str(now.day))
            if pub_date:
                new_str = new_str.replace('<!--pub-date-->', pub_date)
                new_str = new_str.replace('<!--pub-date-j-->', pub_date.replace('-', '/').replace('/0', '/'))
            else:
                new_str = new_str.replace('<!--pub-date-->', str(now.date()))
                new_str = new_str.replace('<!--pub-date-j-->',
                                          str(now.year) + '/' + str(now.month) + '/' + str(now.day))

            new_str = new_str.replace('<!--kanren-->', '</section><section><div class="kanren"><h2>関連記事</h2>')
            new_str = new_str.replace('<!--e/kanren-->', '</div>')
            new_str = new_str.replace('<!--btnli-->', '<div class="btnli">')
            new_str = new_str.replace('<!--e/btnli-->', '</div>')
            new_str = new_str.replace('<!--arlist--><ul>', '<ul class="arlist">')
            new_str = new_str.replace('</ul><!--e/arlist-->', '</ul>')
            new_str = new_str.replace('<!--arlist_b--><ul>', '<ul class="arlist" id="deaikei">')
            new_str = new_str.replace('</ul><!--e/arlist_b-->', '</ul>')
            new_str = new_str.replace('<!--point-->', '<div id="kijip"><div class="kijoph"><p>この記事のポイント</p>' +
                                      '</div>')
            new_str = new_str.replace('<!--e/point-->', '</div>')
            new_str = new_str.replace('<!--matome-->', '<div id="kijim"><div class="kijoph"><p>この記事のまとめ</p>' +
                                      '</div>')
            new_str = new_str.replace('<!--e/matome-->', '</div>')
            new_str = new_str.replace('<!--point_i-->', '<div class="in_point"><span>ポイント</span>')
            new_str = new_str.replace('<!--e/point_i-->', '</div>')
            new_str = new_str.replace('<ol>', '<ol class="arlist">')
            new_str = new_str.replace('<div class="hidden_show"><ol class="arlist">', '<div class="hidden_show"><ol>')
            new_str = new_str.replace('<br /></p>', '</p>')
            new_str = new_str.replace('。。<br />', '。</p><p>')
            new_str = new_str.replace('。。', '。</p><p>')
            new_str = new_str.replace('）。<br />', '）</p><p>')
            new_str = new_str.replace(')。<br />', ')</p><p>')
            new_str = new_str.replace(')。', ')</p><p>')
            new_str = new_str.replace('）。', '）</p><p>')
            new_str = new_str.replace('？。', '？<br />')
            new_str = new_str.replace('？。。', '？</p><p>')

            new_str = logical_box_filter(new_str)
            new_str, add_list = img_str_filter(new_str, file_name, md_replace_str, md_file_path)
            p_img_str_l = re.findall(r'<p><img .+?/></p>', new_str)
            if p_img_str_l:
                for p_img_str in p_img_str_l:
                    if '/w_500/' in p_img_str and 'width="' not in p_img_str:
                        p_img_r = re.sub(r'<p>(.+?)/></p>', r'<div class="w_500">\1 width="500" height="375"/></div>',
                                         p_img_str)
                    else:
                        p_img_r = re.sub(r'<p>(.+?)/></p>', r'<div class="center">\1 /></div>', p_img_str)
                    new_str = new_str.replace(p_img_str, p_img_r)
            for lr_str in ['r', 'l']:
                rm_str_l = re.findall(r'<!--' + lr_str + 'm_.+?<!--e/' + lr_str + 'm-->', new_str)
                if rm_str_l:
                    for rm_str in rm_str_l:
                        rm_replace = rm_str.replace('。', '。<br />')
                        new_str = new_str.replace(rm_str, rm_replace)
            new_str = re.sub(r'([^>])。([^<])', r'\1。<br />\2', new_str)
            new_str = new_str.replace('。<a ', '。<br /><a ')
            new_str = new_str.replace('。<br />）', '。）')
            new_str = new_str.replace('。<br />)', '。)')
            new_str = new_str.replace('！。<br />', '！<br />')
            new_str = new_str.replace('。<br /></p>', '。</p>')
            new_str = re.sub(r'(件名: .+?)<br />', r'<span class="m_title">\1</span>', new_str)
            new_str = new_str.replace('<table>', '<table class="tb_n">')

            new_str = re.sub(r'<!--lm_(\d)-->',
                             r'<div class="fl1"><div class="icon"><div class="lm_b lm_\1"></div></div>', new_str)
            new_str = new_str.replace('<!--e/lm-->', '</div>')
            new_str = re.sub(r'<!--rm_(\d)-->',
                             r'<div class="fr2"><div class="icon"><div class="rm_b rm_\1"></div></div>', new_str)
            new_str = re.sub(r'<!--rw_(\d)-->',
                             r'<div class="fr2"><div class="icon"><div class="rw_b rw_\1"></div></div>', new_str)
            new_str = new_str.replace('<!--e/rm-->', '</div>')
            new_str = new_str.replace('<!--e/rw-->', '</div>')

            new_str = new_str.replace('<!--bread-->',
                                      new_article_create.breadcrumb_maker(category, directory, file_name))
            new_str = new_str.replace('"../../../reibun/pc/', '"../')
            new_str = new_str.replace('<!--sample/s-->', '<div class="sample">')
            new_str = new_str.replace('<!--sample/e-->', '</div>')

            if 'i::' in plain_txt:
                t_image_l = re.findall(r'i::(.+?)\n', plain_txt)
                t_image = t_image_l[0]
            else:
                if '_1_gr.jpg' in new_str:
                    t_img_l = re.findall(r'<div class="alt_img_t"><img src="(.*?/images/art_images/.+?_1_gr\.jpg)"',
                                         new_str)
                    if t_img_l:
                        t_image = t_img_l[0].replace('../images/', '')
                    else:
                        t_image = 'demr_mgirl_1200x630.jpg'
                else:
                    t_image = 'demr_mgirl_1200x630.jpg'
            new_str = new_str.replace('<!--t-image-->', t_image)
            new_str = new_str.replace('<!--description-->', description)
            new_str = new_str.replace('<div id="footer2">出会い系サイトは18禁です。<br />18歳未満',
                                      '<div id="footer2">出会い系サイトは18禁です。18歳未満')
            new_str = new_str.replace('.md"', '.html"')
            new_str = new_str.replace('<p>%libut%</p><ul>', '<ul class="libut">')
            new_str = json_img_data_insert(new_str)
            card_br_l = re.findall(r'<span class="ar_dis">.+?</span>', new_str)
            if card_br_l:
                for card_br in card_br_l:
                    new_str = new_str.replace(card_br, card_br.replace('<br />', ''))
            if 'new_art' in md_file_path:
                new_str = new_str.replace('"reibun/pc/', '"../')
                pub_or_mod = 'pub'
                new_file_data.append([file_name, title, description])
            else:
                pub_or_mod = 'mod'
            upload_list.extend(add_list)
            upload_list.extend(pick_up_same_name_images(file_name))
            pick_up_same_name_images(file_name)
            if md_file_path == 'md_files/index.md':
                with open('reibun/index.html', 'r', encoding='utf-8') as h:
                    top_long_str = h.read()
                    mod_log = re.findall(r'<div id="update"><ul class="updli">.+?</ul></div></div>', top_long_str)[0]
                top_page_filter(new_str)
                new_str = new_str.replace('</article>',
                                          '<section><div class="tabn"><h2>主な更新履歴</h2>' + mod_log +
                                          '</section></article>')

            with open('reibun/pc/' + file_name, 'w', encoding='utf-8') as g:
                g.write(new_str)
                upload_list.append('reibun/pc/' + file_name)
                new_data = [file_name, title, '', str(now.date()), category, description]
                pk_dec = add_pickle_dec(pk_dec, new_data)
            add_modify_log('reibun/pc/' + file_name, now.date(), category, title, pub_or_mod)
    return upload_list, pk_dec, new_file_data


def json_img_data_insert(long_str):
    img_path = 'eyec.jpg'
    height = '464'
    width = '700'
    if '<div class="alt_img_t">' in long_str:
        img_l = re.findall(r'<div class="alt_img_t"><img src="\.\./images/(.+?)" alt="', long_str)
        if img_l:
            img_path = img_l[0]
            height = '470'
            width = '760'
    i_str = long_str.replace('<!--jd-img-path-->', img_path)
    i_str = i_str.replace('"<!--jd-height-->"', height)
    i_str = i_str.replace('"<!--jd-width-->"', width)
    return i_str


def logical_box_filter(long_str):
    lg_box_str_l = re.findall(r'<div class="logi_box_e.+?>.+?</div>', long_str)
    if lg_box_str_l:
        for lg_box_str in lg_box_str_l:
            box_str = re.findall(r'>(.*?)<', lg_box_str)[0]
            if '*' in box_str:
                box_str_r = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', box_str)
                box_str_r = re.sub(r'\*(.+?)\*', r'<em>\1</em>', box_str_r)
                long_str = long_str.replace(box_str, box_str_r)
    return long_str


def add_modify_log(mod_file_path, now, category, title, pub_or_mod):
    # mod_log = [[mod_file_path, str(now), category, title, pub_or_mod]]
    mod_log = make_article_list.read_pickle_pot('modify_log')
    today_mod = [x[0] for x in mod_log if x[1] == str(now)]
    if mod_file_path not in today_mod:
        mod_log.append([mod_file_path, str(now), category, title, pub_or_mod])
    else:
        for data in mod_log:
            if data[0] == mod_file_path and data[1] == str(now):
                mod_log.remove(data)
                mod_log.append([mod_file_path, str(now), category, title, pub_or_mod])
    make_article_list.save_data_to_pickle(mod_log, 'modify_log')


def img_str_filter(long_str, file_name, md_str, md_file_path):
    add_list = []
    insert_img_l = re.findall(r'<p><img.+?></p>', long_str)
    if insert_img_l:
        for img_str in insert_img_l:
            img_data_l = re.findall(r'alt="(.*?)" src="(.+?)"', img_str)
            if 'insert_image/' in img_data_l[0][1]:
                img_url = img_data_l[0][1]
                new_img_path, add_img = resize_and_rename_image(img_url, file_name)
                insert_str = '<div class="alt_img_t"><img src="{}" alt="{}" /></div>'.format(new_img_path,
                                                                                             img_data_l[0][0])
                long_str = long_str.replace(img_str, insert_str)
                md_str = md_str.replace(img_url, new_img_path)
                add_list.extend(add_img)
            else:
                img_url = img_data_l[0][1]
                insert_str = '<div class="alt_img_t"><img src="{}" alt="{}" /></div>'.format(img_url, img_data_l[0][0])
                long_str = long_str.replace(img_str, insert_str)
    with open(md_file_path, 'w', encoding='utf-8') as f:
        f.write(md_str)
    return long_str, add_list


def resize_and_rename_image(img_path, file_path):
    file_name = re.sub(r'^.*/(.+?).html', r'\1', file_path)
    current_images = os.listdir('reibun/pc/images/art_images')
    if file_name + '_1_gr.jpg' in current_images:
        i = 2
        new_name = file_name + '_' + str(i) + '_gr.jpg'
        while new_name in current_images:
            i += 1
            new_name = file_name + '_' + str(i) + '_gr.jpg'
        image_path = re.sub(r'^.+insert_image/', 'insert_image/', img_path)
        img = Image.open(image_path)
        img_gr = img.resize((760, 470))
        img_gr.save('reibun/pc/images/art_images/' + new_name)
        img_gr.save('reibun/amp/images/art_images/' + new_name)
        img_gr.save('md_files/pc/images/art_images/' + new_name)
        img.save('image_stock/' + file_name + '_' + str(i) + '.jpg')
        os.remove(img_path.replace('../../../', ''))
        add_img = ['reibun/pc/images/art_images/' + new_name, 'reibun/amp/images/art_images/' + new_name]
    else:
        add_img = image_upload.make_thumbnail(file_name, img_path.replace('../../../', ''))
        new_name = file_name + '_1_gr.jpg'
    return '../images/art_images/' + new_name, add_img


def mail_sample_replace(long_str):
    k_mail_l = re.findall(r'%k%([\s\S]+?)\n\n', long_str)
    if k_mail_l:
        for k_mail in k_mail_l:
            k_str = '<div class="sample"><div class="kenmei">' + k_mail + '</div><!--km-el-->'
            long_str = long_str.replace('%k%' + k_mail + '\n\n', k_str)
    m_mail_l = re.findall(r'%m%([\s\S]+?)\n\n', long_str)
    if m_mail_l:
        for m_mail in m_mail_l:
            m_str = '<div class="sample"><div class="mail"><p>' + m_mail.replace('\n', '<br />') + '</p></div></div>'
            long_str = long_str.replace('%m%' + m_mail + '\n\n', m_str)
    f_mail_l = re.findall(r'%w%([\s\S]+?)\n\n', long_str)
    if f_mail_l:
        for f_mail in f_mail_l:
            f_str = '<div class="sample"><div class="wmail"><p>' + f_mail.replace('\n', '<br />') + '</p></div></div>'
            long_str = long_str.replace('%w%' + f_mail + '\n\n', f_str)
    long_str = long_str.replace('%arr' + '\n\n',
                                '<div class="arr"><img width="17" height="17" src="../images/arr.png" alt="↓"></div>')
    cm_mail_l = re.findall(r'%cm%([\s\S]+?)\n\n', long_str)
    if cm_mail_l:
        for cm_mail in cm_mail_l:
            cm_str = '<div class="cm"><p>' + cm_mail.replace('\n', '<br />') + '</p></div></div>'
            long_str = long_str.replace('%cm%' + cm_mail + '\n\n', cm_str)
    if '%%%' in long_str:
        long_str = re.sub(r'%%%([\s\S]+?)%%%', r'<div class="sample">\1</div>', long_str)
    else:
        long_str = long_str.replace('</div></div><div class="arr">', '</div><div class="arr">')
        long_str = long_str.replace('alt="↓"></div><div class="sample"><div class="mail">',
                                    'alt="↓"></div><div class="mail">')
        long_str = long_str.replace('alt="↓"></div><div class="sample"><div class="wmail">',
                                    'alt="↓"></div><div class="wmail">')
        long_str = long_str.replace('</div></div><div class="cm">', '</div><div class="cm">')
        long_str = re.sub(r'<!--km-el-->[\s]*?<div class="sample">', '', long_str)
    return long_str


def strong_insert_filter(long_str):
    if '*' in long_str:
        box_str_r = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', long_str)
        box_str_r = re.sub(r'\*(.+?)\*', r'<em>\1</em>', box_str_r)
        long_str = long_str.replace(long_str, box_str_r)
    return long_str


def add_pickle_dec(pk_dec, new_data):
    path_list = [pk_dec[x][0] for x in pk_dec]
    if new_data[0] not in path_list:
        pk_dec[len(pk_dec)] = new_data
    else:
        for i in range(len(path_list)):
            if path_list[i] == new_data[0]:
                pk_dec[i] = new_data
    make_article_list.save_data_to_pickle(pk_dec, 'title_img_list')
    make_article_list.save_text_file(pk_dec)
    return pk_dec


def css_optimize(html_path, css_path):
    with open(css_path, 'r', encoding='utf-8') as f:
        css_str = f.read()
    with open(html_path, 'r', encoding='utf-8') as g:
        html_str = g.read()
    return css_str_optimize(html_str, css_str)


def css_str_optimize(html_str, css_str):
    css_str = css_str.replace('\n', '')
    css_str = css_str.replace('@charset "UTF-8";', '')
    css_str = re.sub(r';[\s]*', ';', css_str)
    css_str = re.sub(r'{[\s]*', '{', css_str)
    css_str = re.sub(r',[\s]*', ',', css_str)
    css_str = re.sub(r':[\s]*', ':', css_str)
    css_str = re.sub(r' {', '{', css_str)
    css_str = re.sub(r'/\*.+?\*/', '', css_str)
    css_str = re.sub(r'@media.*$', '', css_str)
    css_list = css_str.split('}')
    css_list = [c + '}' for c in css_list[:-1]]
    css_sep_list = []
    for line in css_list:
        selector_str_l = re.findall(r'(.+?){', line)
        if ',' in selector_str_l[0]:
            selector_c_list = selector_str_l[0].split(',')
        else:
            selector_c_list = [selector_str_l[0]]
        css_sep_list.append([selector_c_list, re.findall(r'{([\s\S]*)}', line)[0]])
    # print(css_sep_list)

    z_l = [z.split() for z in re.findall(r'class="(.+?)"', html_str)]
    class_list = []
    for z_e in z_l:
        class_list.extend(['.' + q for q in z_e])

    id_list = ['#' + z for z in re.findall(r'id="(.+?)"', html_str)]
    selector_list = class_list + id_list
    selector_list = set(selector_list)
    selector_list = list(selector_list)
    selector_list.sort()
    # print(selector_list)

    tag_list = re.findall('<(.+?)[ |>]', html_str)
    tag_list = [b for b in tag_list if '/' not in b and '!' not in b]
    tag_list = set(tag_list)
    tag_list = list(tag_list)
    new_list = []
    for x in css_sep_list:
        css_selector = []
        for y in x[0]:
            # print(y)
            if '.' in y or '#' in y:
                for z in selector_list:
                    if z in y:
                        css_selector.append(y)
                        break
            else:
                for i in tag_list:
                    if i in y:
                        css_selector.append(y)
                        break
        if css_selector:
            new_list.append([css_selector, x[1]])
    # print(len(new_list))
    # print(new_list)
    str_list = [','.join(a[0]) + '{' + a[1] + '}' for a in new_list]
    new_str = ''.join(str_list)
    # print(new_str)
    return new_str


def modify_relation_list(long_str, mod_list):
    r_str = re.findall(r'<div class="kanren">(.+?)</div>', long_str)
    if r_str[0]:
        for mod in mod_list:
            new_url = mod[0].replace('md_files/pc/', '../')
            if new_url in r_str[0]:
                new_title = mod[2]
                l_str_l = re.findall(r'<li><a href="(.+?)">(.+?)</a></li>', r_str[0])
                if l_str_l:
                    for l_str in l_str_l:
                        if l_str[0] == new_url:
                            long_str = long_str.replace('<li><a href="{}">{}</a></li>'.format(new_url, l_str[1]),
                                                        '<li><a href="{}">{}</a></li>'.format(new_url, new_title))
    return long_str


if __name__ == '__main__':
    main(1)
    reibun_upload.files_upload(['reibun/index.html'])

    # import_from_markdown(['md_files/pc/qa/q3_test.md'])
    # print(resize_and_rename_image('insert_image/AdobeStock_15946903.jpeg', 'majime/m0_test.html'))
    # t_l = {0: ['']}
    # print(make_all_side_bar(t_l))
    # insert_to_index_page(t_l)
    # xml_site_map_maker(t_l)
    # reibun_upload.tab_and_line_feed_remover('reibun/index.html')
    # print(markdown.markdown('## h2\n[](あああああ)\n<!--あああああ-->'))
    # print([x for x in test_l if x[1] == test_l[-1][1]])
    # print(str(datetime.datetime.now())[:-7])
    # print(make_article_list.read_pickle_pot('modify_log'))
    # print(css_optimize('reibun/index.html', 'reibun/pc/css/top1.css'))

    # make_rss([])
    # reibun_upload.files_upload(['reibun/atom.xml', 'reibun/rss10.xml', 'reibun/rss20.xml'])

    # todo: アップロード
    # todo: 関連記事改善
