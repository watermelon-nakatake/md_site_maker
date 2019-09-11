import re
import os
import shutil
from reibun_upload import ftp_upload


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
    ftp_upload(copy_file)


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
                        insert_str = top_img.replace('.jpg" alt="', '.jpg" width="759" height="506" layout="responsive" alt="')
                        insert_str = insert_str.replace('<img', '<amp-img')
                        insert_str = insert_str.replace('"></div>', '"></amp-img></div>')
                        content = content.replace(top_img, insert_str)
                content = re.sub(r'<img(.+?)>', r'<amp-img\1></amp-img>', content)
                pub_date = re.findall(r'itemprop="datePublished" datetime="(.*?)">', str_x)[0]
                mod_date = re.findall(r'itemprop="dateModified" datetime="(.*?)">', str_x)[0]
                description = re.findall(r'<meta name="description" content="(.*?)">', str_x)[0]
                date_data = re.findall(r'(\d{4})-(\d{2})-(\d{2})', str_x)
                new_date = date_data[0][0] + '年' + date_data[0][1] + '月' + date_data[0][2] + '日'
                amp_data = tmp_str.replace('<!--title-->', title)
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
            with open(amp_path, "w") as h:
                h.write(amp_data)
            relation_file_upload(amp_data)


if __name__ == '__main__':
    amp_maker(['reibun/pc/majime/mail-applicaton.html'])
