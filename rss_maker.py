# -*- coding: utf-8 -*-
import re
import os
from article_maker_rb import MyHtmlStripper
from article_maker_rb import keyword_search
from article_maker_rb import make_rss


def pick_up_and_make_rss(path):
    file_list = os.listdir(path)
    rss_list = []
    timestamp = '2019-04-25T18:00:00+09:00'
    for z in file_list:
        if '.html' not in z:
            file_list.remove(z)
    for file in file_list:
        with open(path + '/' + file, "r", encoding='utf-8') as f:
            str_x = f.read()
            r_title = re.findall(r'<title>(.*?)</title>', str_x)[0]
            r_summary = re.findall(r'<meta name="description" content="(.*?)">', str_x)[0]
            main_text = re.findall(r'<!--top-img-.{600}', str_x)[0]
            r_content = MyHtmlStripper(main_text).value[:300]
            keyword = keyword_search(str_x)
            rss_data = [file, r_title, r_summary, r_content, timestamp, timestamp, keyword + ',セックス']
            rss_list.append(rss_data)
    result = make_rss(rss_list)
    return result


print(pick_up_and_make_rss('/Users/nakataketetsuhiko/PycharmProjects/reibun_sf/make-love'))



