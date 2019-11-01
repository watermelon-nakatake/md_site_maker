# -*- coding: utf-8 -*-
import re


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
               '[<label for="label1">表示切替</label>]</span></div><input type="checkbox" id="label1"/>' \
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
        category = search_category(directory, file_name)
    else:
        directory = 'top'
        category = 'top'
    return directory, category


def search_category(directory, file_name):
    if directory != 'majime':
        category = directory
    else:
        if 'm0' in file_name:
            category = 'post'
        elif 'mp_' in file_name:
            category = 'profile'
        elif 'm1' in file_name:
            category = 'f_mail'
        elif 'm2' in file_name:
            category = 's_mail'
        elif 'm3' in file_name:
            category = 'date'
        elif 'm4' in file_name:
            category = 'how_to'
        elif 't0_' in file_name:
            category = 'post'
        else:
            category = 'majime'
    return category


if __name__ == '__main__':
    print('test')
