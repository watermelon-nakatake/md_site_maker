# -*- coding: utf-8 -*-
import os
import re
import article_maker_rb
import reibun_upload


def import_from_evernote(insert_dir, new_file_name):
    directory = os.listdir('/Users/nakataketetsuhiko/Downloads/自分のノート')
    if directory:
        file_name = directory[0]
        with open('reibun/pc/template/pc_tmp.html', 'r', encoding='utf-8') as t:
            tmp_str = t.read()
        with open('/Users/nakataketetsuhiko/Downloads/自分のノート/' + file_name, 'r', encoding='utf-8') as f:
            original_str = f.read()
            title_l = re.findall('<title>(.+?)</title>', original_str)
            if title_l:
                title = title_l[0]
                print('title: ' + title)
            else:
                print('there is no title!')
                return
            content_l = re.findall(r'<body>(.+?)</body>', original_str)
            if content_l:
                content = content_l[0]
            else:
                print('There is no content!')
                return
            keyword_list = re.findall(r'<div>Key:.*?</div>', content)
            if keyword_list:
                keyword_str = re.findall(r'<div>Key:(.*?)</div>', keyword_list[0])
                keyword = keyword_str[0].split(' ')
                keyword.remove('')
                print('keyword')
                print(keyword)
                content = content.replace(keyword_list[0], '')
            else:
                print('there is no keyword!')
                return
            description_list = re.findall(r'<div>Des:.*?</div>', content)
            if description_list:
                description_str = re.findall(r'<div>Des:(.*?)</div>', description_list[0])
                description = description_str[0].strip()
                print('description: ' + description)
                content = content.replace(description_list[0], '')
            else:
                print('There is no description!')
                return
            content = re.sub(r'^<div>', '<p>', content)
            content = re.sub(r'</div><div><br/></div>$', '</p>', content)
            content = re.sub(r'</div>$', '</p>', content)
            content = re.sub(r'</div>$', '</p>', content)
            content = content.replace('<span>', '')
            content = content.replace('</span>', '')
            content = content.replace('<u>', '<a href="">')
            content = content.replace('</u>', '</a>')

            content = re.sub(r'</div><div><br/></div><div><br/></div><div>H(\d) (.+?)</div><div><br/></div><div>',
                             r'</p><h\1>\2</h\1><p>', content)
            content = content.replace('</div><div><br/></div><div>', '</p><p>')
            content = content.replace('</div><div><br/></div><div><br/></div><div>(.', '</p><h2>')
            content = content.replace('</div><div>', '<br>')

            new_str = tmp_str.replace('<!--title-->', title)
            new_str = new_str.replace('<!--main-content-->', content)

            new_str = new_str.replace('<h2>', '<!--p-index--><h2>', 1)
            new_str = article_maker_rb.index_maker(new_str)
            new_str = article_maker_rb.section_insert(new_str)
            # todo: 関連記事挿入

            print(new_str)
            return

            with open('reibun/pc/' + insert_dir + '/' + new_file_name, 'w', encoding='utf-8') as g:
                g.write(content)
                reibun_upload.ftp_upload(['reibun/pc/' + insert_dir + '/' + new_file_name])


def new_article_finish():
    print()
    # todo: 目次の挿入
    # todo: amp作成
    # todo: upload


if __name__ == '__main__':
    import_from_evernote('majime', 'new_a_test')
