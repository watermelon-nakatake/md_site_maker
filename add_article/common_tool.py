# -*- coding: utf-8 -*-
import re
import os


# 目次作成
def index_maker(long_str):
    list_p = make_list(long_str)
    str_p = index_str(list_p)
    str_a = anchor_insert(long_str)
    result = str_a.replace('<!--p-index-->', str_p, 1)
    return result


def index_str(index_list):
    work_list = index_list
    work_str = ''.join(work_list)
    ex_list = [{'h_tag': '</h2><h2>', 'li_tag': '</a></li><li><a href="#sc¥num¥">'},
               {'h_tag': '</h3><h3>', 'li_tag': '</a></li><li><a href="#sc¥num¥">'},
               {'h_tag': '</h4><h4>', 'li_tag': '</a></li><li><a href="#sc¥num¥">'},
               {'h_tag': '</h2><h3>', 'li_tag': '</a><ol><li><a href="#sc¥num¥">'},
               {'h_tag': '</h3><h2>', 'li_tag': '</a></li></ol></li><li><a href="#sc¥num¥">'},
               {'h_tag': '</h3><h4>', 'li_tag': '</a><ol><li><a href="#sc¥num¥">'},
               {'h_tag': '</h4><h3>', 'li_tag': '</a></li></ol></li><li><a href="#sc¥num¥">'},
               {'h_tag': '</h4><h2>', 'li_tag': '</a></li></ol></li></ol></li><li><a href="#sc¥num¥">'},
               {'h_tag': r'</h2>$', 'li_tag': '</a></li></ol>'},
               {'h_tag': r'</h3>$', 'li_tag': '</a></li></ol></li></ol>'},
               {'h_tag': r'</h4>$', 'li_tag': '</a></li></ol></li></ol></li></ol>'},
               {'h_tag': r'^<h2>', 'li_tag': '<ol><li><a href="#sc¥num¥">'},
               {'h_tag': r'^<h3>', 'li_tag': '<ol><li><ol><li><a href="#sc¥num¥">'},
               {'h_tag': r'^<h4>', 'li_tag': '<ol><li><ol><li><ol><li><a href="#sc¥num¥">'}]
    for ex in ex_list:
        work_str = re.sub(ex['h_tag'], ex['li_tag'], work_str)
    i = 1
    while '¥num¥' in work_str:
        work_str = work_str.replace('¥num¥', str(i), 1)
        i += 1
    work_str = '<div id="mokujio"><nav id="mokuji"><div class="moh">目次 <span class="small">' \
               '[<label for="label1">開く/閉じる</label>]</span></div><input type="checkbox" id="label1"/>' \
               '<div class="hidden_show">' + work_str + '</div></nav></div>'
    return work_str


def anchor_insert(str_a):
    str_w = re.sub(r'(<h[234]>)(.*?)(</h[234]>)', r'\1<span id="sc¥num_i¥">\2</span>\3', str_a)
    if '関連記事' in str_w:
        str_w = str_w.replace('<h2><span id="sc¥num_i¥">関連記事</span></h2>', '<h2>関連記事</h2>')
    i = 1
    while '¥num_i¥' in str_w:
        str_w = str_w.replace('¥num_i¥', str(i), 1)
        i += 1
    return str_w


def make_list(input_file):
    matched_list = re.findall(r'<h[234]>.*?</h[234]>', input_file)
    if '<h2>関連記事</h2>' in matched_list:
        matched_list.remove('<h2>関連記事</h2>')
    result = []
    for x in matched_list:
        x = re.sub(r'[0-9]\.\s', '', x)
        result.append(x)
    return result


def section_insert(long_str):
    h_tag_outer = re.findall(r'<h[2|3]>.*?</h[2|3]>', long_str)
    if h_tag_outer:
        h_tag_outer.reverse()
        insert_list = []
        for i in range(len(h_tag_outer) - 1):
            if '<h2>' in h_tag_outer[i]:
                if '<h2>' in h_tag_outer[i + 1]:
                    insert_list.append('</section><section>' + h_tag_outer[i])
                elif '<h3>' in h_tag_outer[i + 1]:
                    insert_list.append('</section></section><section>' + h_tag_outer[i])
            elif '<h3>' in h_tag_outer[i]:
                if '<h2>' in h_tag_outer[i + 1]:
                    insert_list.append('<section>' + h_tag_outer[i])
                elif '<h3>' in h_tag_outer[i + 1]:
                    insert_list.append('</section><section>' + h_tag_outer[i])
        insert_list.append('<section>' + h_tag_outer[-1])
        insert_list.reverse()
        h_tag_outer.reverse()
        for j in range(len(h_tag_outer)):
            long_str = long_str.replace(h_tag_outer[j], insert_list[j])
        if '<h2>' in h_tag_outer[-1]:
            long_str = long_str.replace('<!--last-section-->', '</section>')
        elif '<h3>' in h_tag_outer[-1]:
            long_str = long_str.replace('<!--last-section-->', '</section></section>')
    return long_str


def remove_no_use_images(dir_path):
    no_use_list = check_no_use_images(dir_path)
    for file_name in no_use_list:
        if 'art_images/' in file_name:
            if '_thumb' not in file_name and '_gr' not in file_name:
                os.remove(file_name)
        else:
            os.remove(file_name)


def lost_link_checker(dir_path):
    html_list = make_html_list(dir_path)
    html_list.append('reibun/app/index.html')
    # print(html_list)
    lost_link_dec = {}
    for html_file in html_list:
        if '.html' in html_file:
            # print('file : ' + html_file)
            lost_list = []
            with open(html_file, 'r', encoding='utf-8') as f:
                long_str = f.read()
                link_l = re.findall(r'href="(.+?)"', long_str)
            for link_str in link_l:
                if 'http://' not in link_str and 'https://' not in link_str and '#' not in link_str\
                        and '.css' not in link_str and 'images/' not in link_str and '.xml' not in link_str:
                    if '.html' not in link_str and '/ds/' not in link_str:
                        link_str = link_str + '/index.html'
                        link_str = link_str.replace('//', '/')
                    elif '/ds/' in link_str:
                        link_str = re.sub(r'/$', '', link_str)
                    # print('生link : ' + link_str)
                    dir_name_l = re.findall(r'(.+?/)', html_file)
                    if '../../../' in link_str:
                        link_path = ''.join(dir_name_l[:-3]) + link_str.replace('../../../', '')
                    elif '../../' in link_str:
                        link_path = ''.join(dir_name_l[:-2]) + link_str.replace('../../', '')
                    elif '../' in link_str:
                        link_path = ''.join(dir_name_l[:-1]) + link_str.replace('../', '')
                    elif './' in link_str:
                        link_path = ''.join(dir_name_l) + link_str.replace('./', '')
                    else:
                        link_path = ''.join(dir_name_l) + link_str
                    # print('修正link : ' + link_path)
                    if link_path not in html_list:
                        lost_list.append(link_path)
                    if '/amp/' in html_file:
                        if 'reibun/index.html' in lost_list:
                            lost_list.remove('reibun/index.html')
                        elif 'reibun/amp/mailform/index.html' in lost_list:
                            lost_list.remove('reibun/amp/mailform/index.html')
                    elif '/app/' in html_file:
                        lost_list = []
            if lost_list:
                lost_link_dec[html_file] = lost_list
                print(html_file)
                print(lost_list)
                print('\n')
    return lost_link_dec


def check_no_use_images(dir_path):
    image_list = make_file_list(dir_path + '/images')
    print(image_list)
    html_list = make_html_list(dir_path)
    if '/pc/' in dir_path:
        html_list.append('reibun/index.html')
    no_image_list = []
    used_list = []
    for html_file in html_list:
        if '.html' in html_file or 'css' in html_file:
            print(html_file)
            with open(html_file, 'r', encoding='utf-8') as f:
                long_str = f.read()
                image_l = re.findall(r'(images/.+?)["|<)]', long_str)
            for image in image_l:
                print(image)
                if dir_path + '/' + image in image_list:
                    image_list.remove(dir_path + '/' + image)
                    used_list.append(dir_path + '/' + image)
                else:
                    if dir_path + '/' + image not in used_list:
                        no_image_list.append(dir_path + '/' + image)
    print(no_image_list)
    return image_list


def make_file_list(list_path):
    all_list = os.listdir(list_path)
    dir_list = []
    file_list = []
    for x in all_list:
        if '.' in x:
            file_list.append(list_path + '/' + x)
        else:
            dir_list.append(x)
    for y in dir_list:
        file_list.extend([list_path + '/' + y + '/' + z for z in os.listdir(list_path + '/' + y)])
    return file_list


def make_html_list(list_path):
    all_list = os.listdir(list_path)
    dir_list = []
    file_list = []
    for x in all_list:
        if '.html' in x:
            file_list.append(list_path + '/' + x)
        else:
            dir_list.append(x)
    for y in dir_list:
        if '.htaccess' not in y:
            file_list.extend([list_path + '/' + y + '/' + z for z in os.listdir(list_path + '/' + y)])  # if '.html' in z
    if '/pc/' in list_path:
        file_list.extend(['reibun/pc/css/' + z for z in os.listdir('reibun/pc/css') if '9' in z])
    return file_list


if __name__ == '__main__':
    # print(lost_link_checker('reibun/amp'))
    print(check_no_use_images('reibun/amp'))
    # remove_no_use_images('reibun/amp')
