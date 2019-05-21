# -*- coding: utf-8 -*-

import os
import re


def main(path):
    file_list = os.listdir(path)
    with open('file_other/amp_tp.html', "r", encoding='utf-8') as g:
        amp_str = g.read()
    for z in file_list:
        if '.html' not in z:
            file_list.remove(z)
    for file in file_list:
        print(file)
        with open(path + '/' + file, "r", encoding='utf-8') as f:
            str_x = f.read()
            str_x = re.sub('\n', '', str_x)
            str_x = re.sub('\t', '', str_x)
            title = re.findall(r'<h1 itemprop="headline alternativeHeadline name">(.*?)</h1>', str_x)[0]
            content = re.findall(r'ゴーヤン</span></span></a></div>(.*?)<!-- maincontentEnd -->', str_x)[0]
            pub_date = re.findall(r'itemprop="datePublished" datetime="(.*?)">', str_x)[0]
            mod_date = re.findall(r'itemprop="dateModified" datetime="(.*?)">', str_x)[0]
            description = re.findall(r'<meta name="description" content="(.*?)">', str_x)[0]
            date_data = re.findall(r'(\d{4})-(\d{2})-(\d{2})', str_x)
            new_date = date_data[0][0] + '年' + date_data[0][1] + '月' + date_data[0][2] + '日'
            amp_data = amp_str.replace('<!--title-->', title)
            amp_data = amp_data.replace('<!--content-->', content)
            amp_data = amp_data.replace('<!--pub-date-->', str(pub_date) + 'T18:30:00.000+09:00')
            amp_data = amp_data.replace('<!--mod-date-->', str(mod_date) + 'T18:30:00.000+09:00')
            amp_data = amp_data.replace('<!--description-->', description)
            amp_data = amp_data.replace('<!--path-->', str(path) + '/' + str(file))
            amp_data = amp_data.replace('<!--new-date-->', new_date)
        with open('amp_file/' + file, "w") as h:
            h.write(amp_data)


if __name__ == '__main__':
    main('files_sf')
