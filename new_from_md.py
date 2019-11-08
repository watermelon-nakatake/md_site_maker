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

side_bar_list = {'important': [0, 19, 55, 65, 77, 98, 124], 'pop': [22, 24, 25, 30, 34, 38, 56, 100, 104]}
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
                 'ap_mail': ['メール例文アプリ情報', 'mail-applicaton.html', 92]}


def main(mod_hour):
    """
    新規markdownファイルやファイル更新でサイト全体とアップデートしてアップロード
    :param mod_hour: 今回更新するファイルの更新時から現時点までの経過時間（時間） int形式
    :return: none
    """
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
                    mod_list.append('md_files/pc/' + dir_path + file)
        for file_a in ['md_files/index.html', 'new_art_1.md']:
            mod_time_a = os.path.getmtime(file_a)
            if now - mod_time_a < st_time:
                print('update: ' + file_a)
                mod_list.append(file_a)
    print('modify list :')
    print(mod_list)
    upload_list, pk_dec, new_file_data = import_from_markdown(mod_list)
    side_bar_dec = make_all_side_bar(pk_dec)
    change_files = insert_sidebar_to_existing_art(side_bar_dec)
    insert_to_top_page(side_bar_dec)
    insert_to_index_page(pk_dec)
    xml_site_map_maker(pk_dec)
    if new_file_data:
        make_rss(new_file_data)
    amp_file_maker.amp_maker(change_files)

    # todo: 文中に関連記事挿入 card
    # reibun_upload.ftp_upload(upload_list)


def insert_to_top_page(side_bar_dec):
    mod_log = make_article_list.read_pickle_pot('modify_log')
    latest_art = [x for x in mod_log if x[1] == mod_log[-1][1]]
    latest_art.reverse()
    print(latest_art)
    with open('reibun/index.html', 'r', encoding='utf-8') as f:
        long_str = f.read()
        # 更新記事一覧
        up_str_l = re.findall(r'<ul class="updli">(.+?)</ul>', long_str)
        if up_str_l:
            up_str = up_str_l[0]
            up_data_l = re.findall(r'<li>.+?</li>', up_str)
            latest_date = re.findall(r'^<li>.+? \[', up_data_l[0])[0]
            if latest_date == latest_art[0][1].replace('-', '/').replace('/0', '/'):
                replace_str = re.sub(r'<li>' + latest_date + r' \[.+?<li>', '', up_str)
            else:
                replace_str = up_str
            add_str = ''
            for new_art in latest_art:
                status_str = '更新' if new_art[4] == 'mod' else '追加'
                add_str += '<li>{} [{}・<a href="{}">{}</a>]を{}</li>'.format(
                    new_art[1].replace('-', '/').replace('/0', '/'), category_data[new_art[2]][0],
                    new_art[0].replace('pc/', ''), new_art[3], status_str)
            long_str = long_str.replace(up_str, add_str + replace_str)
        # side bar
        long_str = re.sub(r'"sbh">人気記事</div><ul>.+?</ul></div>',
                          '"sbh">人気記事</div><ul>' + side_bar_dec['pop'].replace('../', 'pc/') + '</ul></div>',
                          long_str)
        long_str = re.sub(r'"sbh">重要記事</div><ul>.+?</ul></div>',
                          '"sbh">重要記事</div><ul>' + side_bar_dec['important'].replace('../', 'pc/') + '</ul></div>',
                          long_str)
        long_str = re.sub(r'"sbh">最近の更新記事</div><ul>.+?</ul></div>',
                          '"sbh">最近の更新記事</div><ul>' + side_bar_dec['new'].replace('../', 'pc/') + '</ul></div>',
                          long_str)
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
                                      '<!--' + m_cat + '-i/s-->' + cat_str_m + '<!--' + m_cat + '-i/e-->',
                                      long_str)
                with open('reibun/pc/majime/index.html', 'w', encoding='utf-8') as j:
                    j.write(long_str)


def xml_site_map_maker(pk_dec):
    pk_list = [[pk_dec[x][0], pk_dec[x][3]] for x in pk_dec]
    pk_list.sort(key=lambda y: y[0])
    now = datetime.datetime.now()
    xml_str = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="https://www.sitemaps.org/schemas/sitemap/0.9">' \
              '<url><loc>https://www.demr.jp</loc><lastmod>' + str(now.date())\
              + '</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>'
    for page in pk_list:
        if 'index.html' in page[0]:
            page_url = page[0].replace('/index.html', '/')
        else:
            page_url = page[0]
        xml_str += '<url><loc>https://www.demr.jp/pc/' + page_url + '</loc><lastmod>' + page[1]\
                   + '</lastmod><changefreq>weekly</changefreq><priority>0.5</priority></url>'
    xml_str += '</urlset>'
    with open('reibun/p_sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(xml_str)


def cat_index_str_maker(cat_dec, directory):
    cat_str = '<ul class="libut">'
    for page_i in cat_dec:
        if len(page_i) < 3:
            cat_str += '<li><a href="{}">{}</a></li>'.format(page_i[0].replace(directory + '/', ''), page_i[1])
        else:
            cat_str += '<li><a href="{}">{}<span>{}</span></a></li>'.format(page_i[0].replace(directory + '/', ''),
                                                                            page_i[1], page_i[2])
    cat_str += '</ul>'
    return cat_str


def insert_sidebar_to_existing_art(side_bar_dec):
    change_files = []
    for dir_r in up_dir[:-1]:
        r_files = os.listdir('reibun/pc/' + dir_r)
        for r_file in r_files:
            print(r_file)
            with open('reibun/pc/' + dir_r + '/' + r_file, 'r', encoding='utf-8') as f:
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
                with open('reibun/pc/' + dir_r + '/' + r_file, 'w', encoding='utf-8') as g:
                    g.write(long_str)
                    change_files.append('reibun/pc/' + dir_r + r_file)
    return change_files


def make_all_side_bar(pk_dec):
    cat_dec = {'policy': [], 'caption': [], 'qa': [], 'site': [], 'post': [], 'f_mail': [], 's_mail': [],
               'date': [], 'how_to': [], 'profile': [], 'majime': []}
    pk_list = []
    for i in pk_dec:
        pk_list.append(pk_dec[i])
    sorted_list = sorted(pk_list, key=lambda x: datetime.date(datetime.datetime.strptime(x[3], '%Y-%m-%d').year,
                                                              datetime.datetime.strptime(x[3], '%Y-%m-%d').month,
                                                              datetime.datetime.strptime(x[3], '%Y-%m-%d').day),
                         reverse=True)
    new_art = sorted_list[:10]
    new_str = ''.join(['<li><a href="../{}">{}</a></li>'.format(y[0], y[1]) for y in new_art])
    for id_pk in pk_dec:
        cat_dec[pk_dec[id_pk][4]].append('<li><a href="../{}">{}</a></li>'.format(pk_dec[id_pk][0], pk_dec[id_pk][1]))
    result_dec = {x: ''.join(cat_dec[x]) for x in cat_dec}
    result_dec['new'] = new_str
    for z in side_bar_list:
        result_dec[z] = ''.join(
            ['<li><a href="../{}">{}</a></li>'.format(pk_dec[use_id][0], pk_dec[use_id][1]) for use_id in
             side_bar_list[z]])
    return result_dec


def make_rss(new_file_data):
    now = datetime.datetime.now()
    now_str = str(now)[:-7]
    # rss1.0
    with open('reibun/rss10.xml', 'r', encoding='utf-8') as f:
        rss1_str = f.read()
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
        with open('reibun/rss10.xml', 'w', encoding='utf-8') as g:
            g.write(rss1_str)
    # rss2.0
    with open('reibun/rss20.xml', 'r', encoding='utf-8') as h:
        rss2_str = h.read()
        now_j = now + datetime.timedelta(hours=9)
        now_tuple = now_j.timetuple()
        now_timestamp = time.mktime(now_tuple)
        rfc_str = utils.formatdate(now_timestamp)[:-6]
        item_list_2 = re.findall(r'<item>.+?</item>', rss2_str)
        if len(item_list_2) + len(new_file_data) >= 10:
            item_list_2 = item_list_2[:-(len(item_list_2) + len(new_file_data) - 10)]
        for new_data in new_file_data:
            item_list_2.insert(0, '<item><title>{}</title><link>https://www.demr.jp/pc/{}</link><description>{}'
                                  '</description><pubDate>{} +0900</pubDate></item>'.format(new_data[1], new_data[0],
                                                                                            new_data[2], rfc_str))
        rss2_str = re.sub(r'<item>.*</item>', ''.join(item_list_2), rss2_str)
        with open('reibun/rss20.xml', 'w', encoding='utf-8') as i:
            i.write(rss2_str)
        # atom
        with open('reibun/atom.xml', 'r', encoding='utf-8') as j:
            atom_str = j.read()
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
            with open('reibun/atom.xml', 'w', encoding='utf-8') as k:
                k.write(atom_str)
    

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
            if 'i::' in plain_txt:
                t_image_l = re.findall(r'i::(.+?)\n', plain_txt)
                t_image = t_image_l[0]
            else:
                if '![' in plain_txt:
                    img_l = re.findall(r'!\[.*?\]\((.+?)\)', plain_txt)
                    t_image = re.sub(r'^.*?reibun/', 'https://www.demr.jp/', img_l[0])
                else:
                    t_image = 'https://www.demr.jp/pc/images/demr_mgirl_1200x630.jpg'
            plain_txt = plain_txt.replace(r'%app_b%', '<div class="center"><a href="../../app/"><img class="app_bn1" '
                                                      'src="../images/common/app_bn_f.png" alt="出会い系メール例文アプリ">'
                                                      '</a></div>')
            plain_txt = re.sub(r'%kanren%\n([\s\S]*?)\n\n', r'<!--kanren-->\n\n\n\1\n\n<!--e/kanren-->', plain_txt)
            plain_txt = re.sub(r'%btnli%\n([\s\S]*?)\n\n', r'<!--btnli-->\n\n\n\1\n\n<!--e/btnli-->', plain_txt)
            plain_txt = re.sub(r'%arlist%\n([\s\S]*?)\n\n', r'<!--arlist-->\n\n\n\1\n\n<!--e/arlist-->', plain_txt)
            plain_txt = re.sub(r'%arlist_b%\n([\s\S]*?)\n\n', r'<!--arlist-->\n\n\n\1\n\n<!--e/arlist_b-->', plain_txt)
            plain_txt = re.sub(r'%point%\n([\s\S]*?)\n\n', r'<!--point-->\n\n\n\1\n\n<!--e/point-->', plain_txt)

            plain_txt = re.sub(r'%rm_(\d)%([\s\S]+?)\n\n',
                               r'<!--rm_\1-->\n\n\2\n\n<!--e/rm-->\n\n\n', plain_txt)
            plain_txt = re.sub(r'%lm_(\d)%([\s\S]+?)\n\n',
                               r'<!--lm_\1-->\n\n\2\n\n<!--e/lm-->\n\n\n', plain_txt)

            plain_txt = mail_sample_replace(plain_txt)
            # card挿入
            if '[card](' in plain_txt:
                card_l = re.findall(r'\[card\]\(.+?\)', plain_txt)
                for card in card_l:
                    card_url_l = re.findall(r'\[card\]\((.+?)\)', card)
                    if card_url_l:
                        card_url = card_url_l[0]
                        for page_id in pk_dec:
                            if pk_dec[page_id][0] in card_url:
                                card_str = '<div class="ar_card"><a href="{}"><div class="ar_in"><span class="p_title">' \
                                           '{}</span><span>{}</span></div></a></div>'.format(
                                            card_url, pk_dec[page_id][1], pk_dec[page_id][4])
                                plain_txt = plain_txt.replace(card, card_str)
                                break
            # コメントアウト削除
            plain_txt = re.sub(r'\(\)\[.*?\]\n', '', plain_txt)
            plain_txt = re.sub(r'\n(<!--.+?-->)\n', r'\n\1', plain_txt)

            print(plain_txt)
            print('markdown start!')
            con_str = markdown.markdown(plain_txt)
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

            new_str = new_str.replace('<!--description-->', description)
            new_str = new_str.replace('<!--main-content-->', con_str + '<!--last-section-->')
            new_str = new_str.replace('<h2>', '<!--p-index--><h2>', 1)
            new_str = common_tool.index_maker(new_str)
            new_str = common_tool.section_insert(new_str)
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
            new_str = new_str.replace('<!--point-->', '<div id="kijip"><div class="kijoph"><p>この記事のポイント</p></div>')
            new_str = new_str.replace('<!--e/point-->', '</div>')
            new_str = re.sub(r'。。<br />', r'。</p><p>', new_str)
            new_str = re.sub(r'。。', r'。</p><p>', new_str)
            for lr_str in ['r', 'l']:
                rm_str_l = re.findall(r'<!--' + lr_str + 'm_.+?<!--e/' + lr_str + 'm-->', new_str)
                if rm_str_l:
                    for rm_str in rm_str_l:
                        rm_replace = rm_str.replace('。', '。<br />')
                        new_str = new_str.replace(rm_str, rm_replace)
            new_str = re.sub(r'([^>])。([^<])', r'\1。<br />\2', new_str)

            new_str = re.sub(r'<!--lm_(\d)-->',
                             r'<div class="fl1"><div class="icon"><div class="lm_b lm_\1"></div></div>', new_str)
            new_str = new_str.replace('<!--e/lm-->', '</div>')
            new_str = re.sub(r'<!--rm_(\d)-->',
                             r'<div class="fr2"><div class="icon"><div class="rm_b rm_\1"></div></div>', new_str)
            new_str = new_str.replace('<!--e/rm-->', '</div>')

            new_str = new_str.replace('<!--bread-->',
                                      new_article_create.breadcrumb_maker(category, directory, file_name))
            new_str = new_str.replace('<!--t-image-->', t_image)
            new_str = new_str.replace('<p>%libut%</p><ul>', '<ul class="libut">')
            if 'new_art' in md_file_path:
                new_str = new_str.replace('"reibun/pc/', '"../')
                pub_or_mod = 'pub'
                new_file_data.append([file_name, title, description])
            else:
                pub_or_mod = 'mod'
            insert_img_l = re.findall(r'<p><img.+?></p>', new_str)
            if insert_img_l:
                for insert_img in insert_img_l:
                    img_str = img_str_filter(insert_img, file_name)
                    new_str = new_str.replace(insert_img, img_str)
            with open('reibun/pc/' + file_name, 'w', encoding='utf-8') as g:
                g.write(new_str)
                upload_list.append('reibun/pc/' + file_name)
                # new_data = [file_name, title, '', str(now.date()), category, description]
                # pk_dec = add_pickle_dec(pk_dec, new_data)
            add_modify_log('reibun/pc/' + file_name, now.date(), category, title, pub_or_mod)
    return upload_list, pk_dec, new_file_data


def add_modify_log(mod_file_path, now, category, title, pub_or_mod):
    # mod_log = [mod_file_path, str(now), category, title, pub_or_mod]
    mod_log = make_article_list.read_pickle_pot('modify_log')
    today_mod = [x[0] for x in mod_log if x[1] == str(now)]
    if mod_file_path not in today_mod:
        mod_log.append([mod_file_path, str(now), category, title, pub_or_mod])
    make_article_list.save_data_to_pickle(mod_log, 'modify_log')


def img_str_filter(img_str, file_path):
    img_data_l = re.findall(r'alt="(.*?)" src="(.+?)"', img_str)
    if img_data_l:
        if 'insert_image' in img_data_l[0][1]:
            img_url = img_data_l[0][1]
            new_img_path = resize_and_rename_image(img_url, file_path)
            img_str = '<div class="alt_img_t"><img alt="{}" src="{}" /></div>'.format(img_data_l[0][0], new_img_path)
    print('insert_image: ' + img_str)
    return img_str


def resize_and_rename_image(img_path, file_path):
    file_name = re.sub(r'^.*?/(.+?).html', r'\1', file_path)
    img = Image.open(img_path)
    width, height = 759, 506
    img = img.resize((width, height))
    current_images = os.listdir('reibun/pc/images/art_images')
    i = 1
    new_name = file_name + '_' + str(i) + '.jpg'
    while new_name in current_images:
        i += 1
        new_name = file_name + '_' + str(i) + '.jpg'
    img.save('reibun/pc/images/art_images/' + new_name)
    # img.save('reibun/amp/images/art_images/' + new_name)
    # os.remove('insert_image/' + img_path)
    # reibun_upload.ftp_upload(['reibun/pc/images/art_images/' + new_name])
    # reibun_upload.ftp_upload(['reibun/amp/images/art_images/' + new_name])
    return '../images/art_images/' + new_name


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
            f_str = '<div class="wmail"><p>' + f_mail.replace('\n', '<br />') + '</p></div>'
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
        long_str = long_str.replace('</div></div><div class="arr"><img width="17" height="17" src="../images/arr.png" '
                                    'alt="↓"></div><div class="wmail">',
                                    '</div><div class="arr"><img width="17" height="17" src="../images/arr.png" alt="↓">'
                                    '</div><div class="wmail">')
        long_str = long_str.replace('</div><div class="arr"><img width="17" height="17" src="../images/arr.png" '
                                    'alt="↓"></div><div class="sample"><div class="mail">',
                                    '</div><div class="arr"><img width="17" height="17" src="../images/arr.png" alt="↓">'
                                    '</div><div class="wmail">')
        long_str = long_str.replace('</div></div><div class="cm">', '</div><div class="cm">')
        long_str = re.sub(r'<!--km-el-->[\s]*?<div class="sample">', '', long_str)
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


if __name__ == '__main__':
    # main(1)
    import_from_markdown(['md_files/pc/majime/kakikata_t.md'])
    # print(resize_and_rename_image('insert_image/AdobeStock_15946903.jpeg', 'majime/m0_test.html'))
    # t_l = {0: ['']}
    # print(make_all_side_bar(t_l))
    # insert_to_index_page(t_l)
    # xml_site_map_maker(t_l)
    # reibun_upload.tab_and_line_feed_remover('reibun/pc/majime/index.html')
    # print(markdown.markdown('## h2\n[](あああああ)\n<!--あああああ-->'))
    # print([x for x in test_l if x[1] == test_l[-1][1]])
    print(str(datetime.datetime.now())[:-7])

    # todo: アップロード
    # todo: 関連記事改善
