# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import os
import re
import reibun_upload
import amp_file_maker
import datetime


def insert_img_tag(image_name_list, article_path_long):
    with open(article_path_long, 'r', encoding='utf-8') as f:
        file_str = f.read()
        if 'alt_img_t' not in file_str:
            h1str_list = re.findall(r'<h1 itemprop="headline alternativeHeadline name">(.+?)</h1>', file_str)
            if h1str_list:
                alt_str = h1str_list[0]
            else:
                alt_str = '出会い系画像'
            if image_name_list:
                file_str = file_str.replace('<span itemprop="name">ゴーヤン</span></span></a></div>',
                                            '<span itemprop="name">ゴーヤン</span></span></a></div>' +
                                            '<div class="alt_img_t"><img src="../images/art_images/'
                                            + image_name_list[0] + '" alt="' + alt_str + 'の画像"></div>')
            file_str = reibun_upload.insert_mod_timestamp(file_str)
            with open(article_path_long, 'w', encoding='utf-8') as g:
                g.write(file_str)
        else:
            print('there is alt_t images already!')


def image_insert(article_path_long, color_str):
    color_list = {'w': (255, 255, 255), 'b': (0, 0, 0)}
    with open(article_path_long, "r", encoding="utf-8") as t:
        text_str = t.read()
        str_list = re.findall(r'<h1 itemprop="headline alternativeHeadline name">(.+?)</h1>', text_str)
        if str_list:
            title = str_list[0]
        else:
            title = '出会い系メール例文集'
    article_path = re.sub(r'^.+/', '', article_path_long)
    article_path = article_path.replace('.html', '')
    # 画像の処理
    pick_up_image = os.listdir('insert_image')
    pick_up_image.sort()
    image_name_list = []
    for img_name in pick_up_image:
        img = Image.open('insert_image/' + img_name)
        width, height = 759, 506
        img = img.resize((width, height))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('/System/Library/Fonts/ヒラギノ角ゴシック W7.ttc', 35)
        if len(title) > 19:
            title = title[:19] + '\n' + title[19:]
        draw.text((30, 30), title, fill=color_list[color_str], font=font)
        current_images = os.listdir('reibun/pc/images/art_images')
        new_name = article_path + '.jpg'
        if new_name in current_images:
            i = 1
            new_name = article_path + '_' + str(i) + '.jpg'
            while new_name in current_images:
                i += 1
                new_name = article_path + '_' + str(i) + '.jpg'
        img.save('reibun/pc/images/art_images/' + new_name)
        img.save('reibun/amp/images/art_images/' + new_name)
        image_name_list.append(new_name)
        os.remove('insert_image/' + img_name)
        reibun_upload.ftp_upload(['reibun/pc/images/art_images/' + new_name])
        reibun_upload.ftp_upload(['reibun/amp/images/art_images/' + new_name])
    insert_img_tag(image_name_list, article_path_long)
    reibun_upload.ftp_upload([article_path_long])


def images_add_to_rb(target_file, color):
    image_insert(target_file, color)
    amp_file_maker.add_amp_file(target_file)
    today = datetime.date.today()
    reibun_upload.xml_sitemap_update({target_file.replace('reibun/pc/', ''): today})
    reibun_upload.ftp_upload(['reibun/p_sitemap.xml'])


def wrong_img_delete(file_name):
    del_name = file_name.replace('.html', '')
    pc_list = os.listdir('reibun/pc/images/art_images/')
    if del_name + '.jpg' in pc_list:
        os.remove('reibun/pc/images/art_images/' + del_name + '.jpg')
        os.remove('reibun/amp/images/art_images/' + del_name + '.jpg')
    else:
        return
    for i in range(1, 5):
        if del_name + '_' + str(i) + '.jpg' in pc_list:
            os.remove('reibun/pc/images/art_images/' + del_name + '.jpg')
            os.remove('reibun/amp/images/art_images/' + del_name + '.jpg')
        else:
            return


def paragraph_insert(file_path, title, insert_str):
    with open(file_path, 'r', encoding='utf-8')as f:
        long_str = f.read()
        max_num = 0
        index_match = re.findall(r'<nav id="mokuji">(.+?)</nav>', long_str)
        if index_match:
            index_ch_list = re.findall(r'<a href="(.+?)">', index_match[0])
            if index_ch_list:
                num_list = [int(re.findall(r'\d+', i_ch)[0]) for i_ch in index_ch_list]
                num_list.sort()
                max_num = num_list[-1]
        if '</section><section><div class="kanren"><h2>関連記事</h2>' in long_str:
            long_str = long_str.replace('</section><section><div class="kanren"><h2>関連記事</h2>',
                                        '</section><section><h2><span id="sc' + str(max_num) + '">' + title
                                        + '</span></h2>' + insert_str
                                        + '</section><section><div class="kanren"><h2>関連記事</h2>')
            long_str = long_str.replace('</ol></div></nav></div>', '<li><a href="#sc' + str(max_num) + '">' + title
                                        + '</a></li></ol></div></nav></div>')
            print(long_str)
            with open(file_path, 'w', encoding='utf-8') as g:
                g.write(long_str)
        else:
            print('error: There is no kanren or not 1 line')


if __name__ == '__main__':
    # images_add_to_rb('reibun/pc/majime/m2htalk.html', 'b')
    # reibun_upload.ftp_upload(['reibun/pc/majime/m0sexfriend.html'])
    # wrong_img_delete('fwari')
    paragraph_insert('reibun/pc/caption/fwari.html', 'テスト', '<p>ここでテストします</p>')
