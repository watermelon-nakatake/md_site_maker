from PIL import Image, ImageDraw, ImageFont
import os
import re
from reibun_upload import ftp_upload


def insert_img_tag(image_name_list, article_path_long):
    # ファイルへのimgタグ挿入
    with open(article_path_long, 'r', encoding='utf-8') as f:
        file_str = f.read()
        if 'pic250' not in file_str:
            if 'alt_img_t' not in file_str:
                h1str_list = re.findall(r'<h1 itemprop="headline alternativeHeadline name">(.+?)</h1>', file_str)
                if h1str_list:
                    alt_str = h1str_list[0]
                else:
                    alt_str = '出会い系画像'
                if image_name_list:
                    file_str = file_str.replace('<span itemprop="name">ゴーヤン</span></span></a></div>',
                                                '<span itemprop="name">ゴーヤン</span></span></a></div>'
                                                + '<div class="alt_img_t"><img src="../images/art_images/' +
                                                image_name_list[0]
                                                + '" alt="' + alt_str + 'の画像"></div>')
                with open(article_path_long, 'w', encoding='utf-8') as g:
                    g.write(file_str)
            else:
                print('there is alt_t images already!')
        else:
            print('there is pic250 images already!')


def image_insert(article_path_long, color_str):
    color_list = {'w': (255, 255, 255), 'b': (0, 0, 0)}
    with open(article_path_long, "r", encoding="utf-8") as t:
        text_str = t.read()
        str_list = re.findall(r'<h1 itemprop="headline alternativeHeadline name">(.+?)</h1>',
                              text_str)
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
        ftp_upload(['reibun/pc/images/art_images/' + new_name])
        ftp_upload(['reibun/amp/images/art_images/' + new_name])
    insert_img_tag(image_name_list, article_path_long)
    ftp_upload([article_path_long])


def images_add_to_rb(target_file, color):
    image_insert(target_file, color)
    ftp_upload([target_file])
    # todo: ampの更新も追加


# 以下実行
if __name__ == '__main__':
    images_add_to_rb('reibun/pc/majime/mail-applicaton.html', 'b')
