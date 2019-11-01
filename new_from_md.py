# -*- coding: utf-8 -*-
import datetime
import pickle
import re
import os
import markdown
from PIL import Image, ImageDraw, ImageFont
import common_tool
import make_article_list
import new_article_create
import reibun_upload

side_bar_list = {'important': [0, 19, 55, 65, 77, 98, 124],
                 'new': [81, 90, 99, 112, 136], 'pop': [22, 24, 25, 30, 34, 38, 56, 100, 104]}


def import_from_markdown(md_file_list):
    upload_list = []
    with open('reibun/pc/template/pc_tmp.html', 'r', encoding='utf-8') as t:
        tmp_str = t.read()
    with open('pickle_pot/title_img_list.pkl', 'rb') as p:
        pk_dec = pickle.load(p)
    side_bar_str = new_article_create.make_side_bar(pk_dec, side_bar_list)
    for md_file_path in md_file_list:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            plain_txt = f.read()
            if 'd::' in plain_txt:
                description = re.findall(r'd::(.+?)\n', plain_txt)[0]
            if 'f::' in plain_txt:
                if 'new_art' in md_file_path:
                    file_name_l = re.findall(r'f::(.+?)\n', plain_txt)
                    if file_name_l:
                        if '.html' in file_name_l[0]:
                            file_name = file_name_l[0]
                        else:
                            file_name = file_name_l[0] + '.html'
                else:
                    file_name = md_file_path.replace('reibun/pc/', '')
            if 'k::' in plain_txt:
                keyword_str = re.findall(r'k::(.+?)\n', plain_txt)[0]
                if '&' in keyword_str:
                    print('There is "&" !')
                    return
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
            plain_txt = mail_sample_replace(plain_txt)

            con_str = markdown.markdown(plain_txt)
            con_str = re.sub(r'^([\s\S]*)</h1>', '', con_str)

            # 以下、modifyでも共通
            directory, category = common_tool.directory_and_category_select('reibun/pc/' + file_name)
            title = re.sub(r'%(.+?)%', r'【\1】', title_str)
            new_str = tmp_str.replace('<!--title-->', title)
            h1_str = re.sub(r'%.+?%', '', title_str)
            new_str = new_str.replace('<!--h1-->', h1_str)
            new_str = new_str.replace('<!--meta-key-->', ','.join(keyword))
            new_str = new_str.replace('<!--file-path-->', file_name)
            new_str = new_str.replace('<!--category-->', category)

            new_str = new_str.replace('<!--description-->', description)
            new_str = new_str.replace('<!--main-content-->', con_str)
            new_str = new_str.replace('<h2>', '<!--p-index--><h2>', 1)
            new_str = common_tool.index_maker(new_str)
            new_str = common_tool.section_insert(new_str)

            new_str = new_str.replace('<!--sb-pop-->', side_bar_str['pop'])
            new_str = new_str.replace('<!--sb-new-->', side_bar_str['new'])
            new_str = new_str.replace('<!--sb-important-->', side_bar_str['important'])

            if side_bar_str[category]:
                sb_str = '<div class="leftnav"><div class="sbh">' + new_article_create.category_name[category][0]\
                         + '</div><ul>' + side_bar_str[category] + '</ul></div>'
                new_str = new_str.replace('<!--sb-category-->', sb_str)

            now = datetime.datetime.now()
            print(now.date())
            new_str = new_str.replace('<!--mod-date-->', str(now.date()))
            new_str = new_str.replace('<!--mod-date-j-->', str(now.year) + '/' + str(now.month) + '/' + str(now.day))

            new_str = new_str.replace('<!--pub-date-->', str(now.date()))
            new_str = new_str.replace('<!--pub-date-j-->', str(now.year) + '/' + str(now.month) + '/' + str(now.day))

            new_str = new_str.replace('<!--kanren-->', '<div class="kanren"><h2>関連記事</h2>')
            new_str = new_str.replace('<!--e/kanren-->', '</div>')
            new_str = new_str.replace('<!--btnli-->', '<div class="btnli">')
            new_str = new_str.replace('<!--e/btnli-->', '</div>')
            new_str = new_str.replace('<!--bread-->',
                                      new_article_create.breadcrumb_maker(category, directory, file_name))
            new_str = new_str.replace('<!--t-image-->',
                                      t_image)
            if 'new_art' in md_file_path:
                new_str = new_str.replace('"reibun/pc/', '"../')
            insert_img_l = re.findall(r'<p>(<img.+?>)</p>', new_str)
            if insert_img_l and 'new_art' in md_file_path:
                for insert_img in insert_img_l:
                    img_str = img_str_filter(insert_img)

            with open('reibun/pc/' + file_name, 'w', encoding='utf-8') as g:
                g.write(new_str)
                upload_list.append('reibun/pc/' + file_name)
                # new_data = [file_name, title, '', str(now)[:-7]]
                # pk_dec = add_pickle_dec(pk_dec, new_data)
    # update_xml_site_map(pk_dec)
    # reibun_upload.ftp_upload(upload_list)


def img_str_filter(ing_str):
    print('p')
    return 'p'


def resize_and_rename_image(img_path, file_path):
    file_name = re.sub(r'^.*?/(.+?).html', r'\1', file_path)
    print(file_name)
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
        long_str = long_str.replace('<!--km-el--><div class="sample">', '')
    return long_str


def add_pickle_dec(pk_dec, new_data):
    path_list = [pk_dec[x][0] for x in pk_dec]
    if new_data[0] not in path_list:
        pk_dec[len(pk_dec)] = new_data
    make_article_list.save_data_to_pickle(pk_dec, 'title_img_list')
    make_article_list.save_text_file(pk_dec)
    return pk_dec


if __name__ == '__main__':
    # import_from_markdown(['new_art_t.md'])
    resize_and_rename_image('insert_image/AdobeStock_15946903.jpeg', 'majime/m0_test.html')

    # todo: 本文の作成
    # todo: 見出しの簡単な入力方法　ex.## ==   済み　markdown
    # todo: section挿入
    # todo: 目次挿入
    # todo: 関連記事作成
    # todo: 時間挿入
    # todo: サイドバー表示
    # todo: xmlサイトマップ
    # todo: htmlサイトマップ
    # todo: RSS
    # todo: topへの表示
    # todo: アップロード

    # todo: test.md 削除
