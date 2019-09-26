# -*- coding: utf-8 -*-
import re
import os
import shutil
import reibun_upload


def relation_file_upload(amp_str):
    src_list = re.findall('img src="(.+?).jpg"', amp_str)
    copy_file = []
    if src_list:
        for src_str in src_list:
            if '/images/' in src_str:
                if not os.path.isfile(src_str + '.jpg'):
                    file_name = re.sub(r'^.*?/images/', '/images/', src_str)
                    if os.path.isfile('reibun/pc' + file_name):
                        shutil.copyfile('reibun/pc' + file_name, 'reibun/amp' + file_name)
                        copy_file.append('reibun/amp' + file_name)
    reibun_upload.ftp_upload(copy_file)


def a_tag_filter(main_str):
    match_list = re.findall(r'<a href=.+?>', main_str)
    if match_list:
        for a_str in match_list:
            element_order = []
            inner_str = a_str.replace('<a ', '')
            inner_str = inner_str.replace('">', '')
            a_element_list = inner_str.split('" ')
            element_words = ['href=', 'class=', 'onclick=', 'rel=']
            for e_word in element_words:
                for a_element in a_element_list:
                    if e_word in a_element:
                        element_order.append(a_element + '"')
            if '/ds/' in a_str:
                if 'rel=' not in a_str:
                    element_order.append('rel="nofollow"')
            jointed_a = '<a ' + ' '.join(element_order) + '>'
            main_str = main_str.replace(a_str, jointed_a)
    return main_str


def g_tag_insert(content_str):
    insert_str = ''
    g_tag_list = ['waku-otherb', 'mintj-otherb', 'happy-otherb', 'max1-otherb', 'merupa-otherb']
    for i in range(len(g_tag_list)):
        if g_tag_list[i] in content_str:
            event_label = g_tag_list[i].replace('-', '-amp')
            insert_str += ',"trackAncorClicks' + str(i + 1) + '":{"on":"click","selector":".' + g_tag_list[i] \
                          + '","request":"event","vars":{"eventCategory":"access","eventAction":"click","eventLabel":"' \
                          + event_label + '"}}'
    return insert_str


def amp_maker(pc_path_list):
    with open('reibun/amp/template/amp_tmp.html', "r", encoding='utf-8') as g:
        tmp_str = g.read()
    for pc_path in pc_path_list:
        if '.html' in pc_path:
            with open(pc_path, "r", encoding='utf-8') as f:
                str_x = f.read()
                title = re.findall(r'<h1 itemprop="headline alternativeHeadline name">(.*?)</h1>', str_x)[0]
                content = re.findall(r'ゴーヤン</span></span></a></div>(.*?)<!-- maincontentEnd -->', str_x)[0]
                top_images = re.findall(r'<div class="alt_img_t">.+?</div>', content)
                if top_images:
                    for top_img in top_images:
                        insert_str = top_img.replace('.jpg" alt="',
                                                     '.jpg" width="759" height="506" layout="responsive" alt="')
                        insert_str = insert_str.replace('<img', '<amp-img')
                        insert_str = insert_str.replace('"></div>', '"></amp-img></div>')
                        content = content.replace(top_img, insert_str)
                        img_path = re.findall(r'src="(.+?)"', top_img)
                        if img_path:
                            tmp_str = tmp_str.replace(
                                '"url": "https://www.demr.jp/pc/images/eyec.jpg","height": 464,"width": 700',
                                '"url": "' + str(img_path[0]) + '","height": 506,"width": 759')
                content = a_tag_filter(content)
                content = content.replace(' target="_blank"', '')
                content = re.sub(r'<img(.+?)>', r'<amp-img\1></amp-img>', content)
                content = re.sub(r'<a href="../ds/(.+?)" class="(.+?)" onclick="gtag\(.+?\}\);" rel="nofollow">',
                                 r'<a href="../ds/\1" class="\2" rel="nofollow">', content)
                pub_date = re.findall(r'itemprop="datePublished" datetime="(.*?)">', str_x)[0]
                mod_date = re.findall(r'itemprop="dateModified" datetime="(.*?)">', str_x)[0]
                description = re.findall(r'<meta name="description" content="(.*?)">', str_x)[0]
                h1_str = re.findall(r'<h1 itemprop="headline alternativeHeadline name">(.*?)</h1>', str_x)[0]
                date_data = re.findall(r'(\d{4})-(\d{2})-(\d{2})', str_x)
                new_date = date_data[0][0] + '年' + date_data[0][1] + '月' + date_data[0][2] + '日'
                amp_data = tmp_str.replace('<!--title-->', title)
                amp_data = amp_data.replace('<!--h1-->', h1_str)
                amp_data = amp_data.replace('<!--content-->', content)
                amp_data = amp_data.replace('<!--pub-date-->', str(pub_date))
                amp_data = amp_data.replace('<!--mod-date-->', str(mod_date))
                amp_data = amp_data.replace('<!--description-->', description)
                amp_path = pc_path.replace('/pc/', '/amp/')
                amp_data = amp_data.replace('<!--path-->', amp_path)
                amp_data = amp_data.replace('<!--new-date-->', new_date)
                side_bar_list = [['人気記事', 'pop-a'], ['重要記事', 'imp-a'], ['最近の更新記事', 'new-a']]
                for x in side_bar_list:
                    match_str_list = re.findall(r'<div class="sbh">' + x[0] + r'</div>.+?</ul>', str_x)
                    if match_str_list:
                        amp_data = amp_data.replace('<!--' + x[1] + '-->', match_str_list[0])
                relative_art = re.findall(r'<!--otherart-->(.+?)<!--otherart/end-->', str_x)
                if relative_art:
                    amp_data = amp_data.replace('<!--other-a-->', match_str_list[0])
                gtag_i = g_tag_insert(content)
                if gtag_i:
                    amp_data = amp_data.replace('{"trackPageview": {"on": "visible","request": "pageview"}}}',
                                                '{"trackPageview": {"on": "visible","request": "pageview"}' + gtag_i + '}}')
            with open(amp_path, "w") as h:
                h.write(amp_data)
            relation_file_upload(amp_data)


def add_amp_file(pc_path):
    file_name = pc_path.replace('reibun/pc/', '')
    amp_maker(['reibun/pc/' + file_name])
    reibun_upload.ftp_upload(['reibun/amp/' + file_name])


if __name__ == '__main__':
    # new_file = 'majime/mail-applicaton.html'
    # amp_maker(['reibun/pc/' + new_file])
    # reibun_upload.ftp_upload(['reibun/pc/' + new_file])
    # reibun_upload.ftp_upload(['reibun/amp/' + new_file])
    amp_maker(['reibun/pc/site/index.html'])
