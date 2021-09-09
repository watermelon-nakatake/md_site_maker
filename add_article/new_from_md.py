# -*- coding: utf-8 -*-
import datetime
import pickle
import re
import os
import shutil
import numpy

import markdown
from PIL import Image
import time
import glob
from email import utils

import make_article_list
from add_article import amp_file_maker, common_tool
from upload import file_upload
from analysis import check_mod_date
import relational_article
import reibun.main_info
from joshideai import main_info
import rei_site.main_info
import konkatsu.main_info


# import rei_site.main_info


def main(site_shift, pd, mod_date_flag, last_mod_flag, upload_flag, first_time_flag, fixed_mod_date):
    """
    新規markdownファイルやファイル更新でサイト全体とアップデートしてアップロード
    :param site_shift: サイトの表示に関するフラグ
    :param pd: projectのデータ
    :param mod_date_flag: mod_dateを更新するかのフラグ Trueなら更新
    :param last_mod_flag: last_modを更新するか否か Trueなら更新
    :param upload_flag: アップロードするか否か
    :param first_time_flag: 初回作成か否か 初回作成はTrue
    :param fixed_mod_date: mod_dateとpub_dateを固定、''ならなし
    :return: none
    """
    now = datetime.datetime.now()
    if first_time_flag:
        last_mod_time = now
        mod_list = [x for x in glob.glob(pd['project_dir'] + '/md_files/**/**.md', recursive=True) if
                    '_copy' not in x and '_test' not in x and '_ud' not in x]
        print(mod_list)
    else:
        mod_list, last_mod_time = pick_up_mod_md_files(pd)
    print('modify list :')
    print(mod_list)
    upload_list, pk_dic, title_change_id = import_from_markdown(mod_list, site_shift, now, pd, mod_date_flag,
                                                                first_time_flag, fixed_mod_date)
    # print(pk_dic)
    if pd['project_dir'] == 'konkatsu' or pd['project_dir'] == 'online_marriage':
        side_bar_dic, ad_side_bar_dic = ad_make_all_side_bar(pk_dic, pd)
    else:
        side_bar_dic = make_all_side_bar(pk_dic, pd)
        ad_side_bar_dic = {}
    print(upload_list)
    print(title_change_id)

    if title_change_id:
        print('change other page')
        change_files = insert_sidebar_to_existing_art(side_bar_dic, title_change_id, pk_dic, pd, ad_side_bar_dic)
        if pd['project_dir'] == 'reibun':
            reibun_index_insert(pk_dic, title_change_id, pd)
        else:
            insert_to_index_page(pk_dic, title_change_id, pd)
        insert_to_top_page(title_change_id, pk_dic, pd, first_time_flag)
    else:
        print('change only one page')
        change_files = [x for x in upload_list if '.html' in x]
    insert_sidebar_to_modify_page(side_bar_dic, mod_list, pd, ad_side_bar_dic)
    if pd['project_dir'] == 'reibun':
        change_files = reibun_qa_check(pk_dic, change_files, title_change_id)
    xml_site_map_maker(pk_dic, pd)
    # make_rss(new_file_data)
    upload_list.extend(change_files)
    if pd['amp_flag']:
        change_files = list(set(change_files))
        amp_upload = amp_file_maker.amp_maker([x for x in change_files if '/amp/' not in x], pd)
        upload_list.extend(amp_upload)
    if upload_flag:
        upload_list.extend(pd['add_files'])
        if os.path.exists('{}/html_files/sitemap.xml'.format(pd['project_dir'])):
            upload_list.append('{}/html_files/sitemap.xml'.format(pd['project_dir']))
        upload_list = list(set(upload_list))
        upload_list.sort()
        upload_list = modify_file_check(upload_list, last_mod_time)
        print(upload_list)
        file_upload.scp_upload([x for x in upload_list if '_copy' not in x and '_test' not in x], pd)
    if last_mod_flag:
        check_mod_date.make_mod_date_list(pd)
        save_last_mod(pd)


def pick_up_mod_md_files(pd):
    now = time.time()
    if os.path.exists(pd['project_dir'] + '/pickle_pot/last_md_mod.pkl'):
        last_md_mod = make_article_list.read_pickle_pot('last_md_mod', pd)
        print(last_md_mod)
    else:
        last_md_mod = now
    all_md_files = [x for x in glob.glob(pd['project_dir'] + '/md_files/**/**.md', recursive=True) if
                    '_copy' not in x and
                    '_test' not in x and '_ud' not in x]
    result = [y for y in all_md_files if os.path.getmtime(y) > last_md_mod]
    return result, last_md_mod


def save_last_mod(pd):
    now = time.time()
    make_article_list.save_data_to_pickle(now, 'last_md_mod', pd)


def modify_file_check(file_list, last_md_mod):
    if type(last_md_mod) == float:
        result = [y for y in file_list if os.path.getmtime(y) > last_md_mod]
    else:
        result = [y for y in file_list if os.path.getmtime(y) > last_md_mod.timestamp()]
    return result


def pick_up_same_name_images(file_path, pd):
    file_name = re.sub(r'.*/(.+?).html', r'\1', file_path)
    img_list = os.listdir(pd['project_dir'] + '/html_files/' + pd['main_dir'] + 'images/' + pd['ar_img_dir'])
    up_list = ['{}/html_files/{}images/{}/{}'.format(pd['project_dir'], pd['main_dir'], pd['ar_img_dir'], x)
               for x in img_list
               if file_name in x]
    return up_list


def update_filter(up_str):
    up_data_l = re.findall(r'<li>.+?</li>', up_str)
    use_list = []
    display_list = []
    for u_str in up_data_l:
        u_path_l = re.findall(r'href="(.+?)"', u_str)
        if u_path_l:
            u_path = u_path_l[0]
            if u_path not in use_list:
                display_list.append(u_str)
                use_list.append(u_path)
    return ''.join(display_list)


def insert_to_top_page(title_change_id, pk_dic, pd, first_time_flag):
    today = datetime.date.today()
    today_str = str(today).replace('-', '/').replace('/0', '/')
    with open(pd['project_dir'] + '/html_files/index.html', 'r', encoding='utf-8') as f:
        long_str = f.read()
        # 更新記事一覧
        up_str = re.findall(r'<ul class="updli">(.*?)</ul>', long_str)[0]
        add_str = ''
        if first_time_flag:
            up_list = []
            for i in pk_dic:
                if ((pd['project_dir'] == 'konkatsu' or pd['project_dir'] == 'online_marriage') and pk_dic[i][
                    'ad_flag'] == 3) or pk_dic[i]['category'] == 'top':
                    continue
                if ':' in pk_dic[i]['pub_date']:
                    up_list.append([datetime.datetime.strptime(pk_dic[i]['pub_date'], '%Y-%m-%d %H:%M:%S'),
                                    pk_dic[i]['category'], pk_dic[i]['file_path'], pk_dic[i]['title']])
                else:
                    up_list.append(
                        [datetime.datetime.strptime(pk_dic[i]['pub_date'] + ' 00:00:00', '%Y-%m-%d %H:%M:%S'),
                         pk_dic[i]['category'], pk_dic[i]['file_path'], pk_dic[i]['title']])
            up_list.sort(reverse=True)
            print(up_list)
            replace_str = ''.join(['<li>{} [{}・<a href="{}">{}</a>]を追加</li>'.format(
                datetime.date.strftime(x[0], '%Y/%m/%d'), pd['category_data'][x[1]][0], x[2], x[3]) for x in up_list])
            print(replace_str)
        else:
            if pd['project_dir'] != 'konkatsu' and pd['project_dir'] != 'online_marriage':
                for c_id in title_change_id:
                    if pk_dic[c_id]['category'] != 'top':
                        if ':' not in pk_dic[c_id]['pub_date']:
                            pub_datetime = datetime.datetime.strptime(pk_dic[c_id]['pub_date'] + ' 00:00:00',
                                                                      '%Y-%m-%d %H:%M:%S')
                        else:
                            pub_datetime = datetime.datetime.strptime(pk_dic[c_id]['pub_date'], '%Y-%m-%d %H:%M:%S')
                        pub_date = datetime.date(pub_datetime.year, pub_datetime.month, pub_datetime.day)
                        status_str = '更新' if today - datetime.timedelta(days=3) > pub_date else '追加'
                        add_str += '<li>{} [{}・<a href="{}">{}</a>]を{}</li>'.format(
                            today_str, pd['category_data'][pk_dic[c_id]['category']][0],
                            pd['main_dir'] + pk_dic[c_id]['file_path'], re.sub(r'【.+?】', '', pk_dic[c_id]['title']),
                            status_str)
            else:
                for c_id in title_change_id:
                    if pk_dic[c_id]['category'] != 'top' and pk_dic[c_id]['ad_flag'] == 3:
                        if ':' not in pk_dic[c_id]['pub_date']:
                            pub_datetime = datetime.datetime.strptime(pk_dic[c_id]['pub_date'] + ' 00:00:00',
                                                                      '%Y-%m-%d %H:%M:%S')
                        else:
                            pub_datetime = datetime.datetime.strptime(pk_dic[c_id]['pub_date'], '%Y-%m-%d %H:%M:%S')
                        pub_date = datetime.date(pub_datetime.year, pub_datetime.month, pub_datetime.day)
                        status_str = '更新' if today - datetime.timedelta(days=3) > pub_date else '追加'
                        add_str += '<li>{} [{}・<a href="{}">{}</a>]を{}</li>'.format(
                            today_str, pd['category_data'][pk_dic[c_id]['category']][0],
                            pd['main_dir'] + pk_dic[c_id]['file_path'], re.sub(r'【.+?】', '', pk_dic[c_id]['title']),
                            status_str)
            replace_str = update_filter(add_str + up_str)
        long_str = long_str.replace(up_str, replace_str)
        if pd['amp_flag']:
            insert_to_amp_top(replace_str, pd)
        long_str = re.sub(r'<time itemprop="dateModified" datetime=".+?">.+?</time>',
                          '<time itemprop="dateModified" datetime="' + str(today) + '">' + today_str + '</time>',
                          long_str)
        with open(pd['project_dir'] + '/html_files/index.html', 'w', encoding='utf-8') as g:
            g.write(long_str)


def insert_to_amp_top(replace_str, pd):
    today = datetime.date.today()
    amp_path = pd['project_dir'] + '/html_files/' + pd['main_dir'].replace('pc', 'amp') + 'index.html'
    with open(amp_path, 'r', encoding='utf-8') as f:
        long_str = f.read()
        long_str = re.sub(r'<ul class="updli">.+?</ul>', '<ul class="updli">' + replace_str.replace(pd['main_dir'], '')
                          + '</ul>', long_str)
        long_str = re.sub(r'<!--mod-->.+?<!--e/mod-->',
                          '<!--mod-->' + str(today).replace('-0', '/').replace('-', '/') + '<!--e/mod-->', long_str)
        long_str = re.sub(r'"dateModified":".+?","description":',
                          '"dateModified":"' + str(today) + '","description":', long_str)
        with open(amp_path, 'w', encoding='utf-8') as g:
            g.write(long_str)


def insert_to_index_page(pk_dic, title_change_id, pd):
    h_dec = {x: [] for x in pd['category_data']}
    for id_num in pk_dic:
        if pk_dic[id_num]['category'] in pd['category_name']:
            if pd['project_dir'] == 'konkatsu' or pd['project_dir'] == 'online_marriage':
                if pk_dic[id_num]['ad_flag'] == 3:
                    h_dec[pk_dic[id_num]['category']].append([pk_dic[id_num]['file_path'], pk_dic[id_num]['title']])
            else:
                h_dec[pk_dic[id_num]['category']].append([pk_dic[id_num]['file_path'], pk_dic[id_num]['title']])
    for category in h_dec:
        h_dec[category].sort(key=lambda x: x[0])
    # html site map
    h_str = '<ul class="arlist" id="sitemap"><li><a href="{}">トップページ</a></li>'.format('../' * pd['main_dir']
                                                                                      .count('/'))
    for category in h_dec:
        h_str += '<li><a href="{}">{}</a><ul>'.format(pk_dic[pd['category_data'][category][2]]['file_path'],
                                                      pk_dic[pd['category_data'][category][2]]['title'])
        if h_dec[category]:
            for page in h_dec[category]:
                if 'index.html' not in page[0]:
                    h_str += '<li><a href="{}">{}</a></li>'.format(page[0], page[1])
        h_str += '</ul></li>'
    h_str += '</ul><!--e/site_map-->'
    if '/policy/' in pd['h_sitemap_path']:
        h_str = h_str.replace('<a href="', '<a href="../')
    with open(pd['h_sitemap_path'], 'r', encoding='utf-8') as f:
        long_str = f.read()
        long_str = file_upload.tab_and_line_feed_remove_from_str(long_str)
        long_str = re.sub('<ul class="arlist" id="sitemap">.*?<!--e/site_map-->', h_str, long_str)
        with open(pd['h_sitemap_path'], 'w', encoding='utf-8') as g:
            g.write(long_str)
    # category page
    ct_cat = list(set([pk_dic[x]['category'] for x in title_change_id]))
    for cat in ct_cat:
        # print(cat)
        if cat != 'top':
            index_path = '{}/html_files/{}{}/{}'.format(pd['project_dir'], pd['main_dir'], cat,
                                                        pd['category_data'][cat][1])
            with open(index_path, 'r', encoding='utf-8') as h:
                long_str = h.read()
                long_str = file_upload.tab_and_line_feed_remove_from_str(long_str)
                cat_str = cat_index_str_maker(h_dec[cat], cat)
                long_str = re.sub(r'<!--index/s-->.*?<!--index/e-->', '<!--index/s-->' + cat_str + '<!--index/e-->',
                                  long_str)
                with open(index_path, 'w', encoding='utf-8') as k:
                    k.write(long_str)


def reibun_index_insert(pk_dic, title_change_id, pd):
    h_dec = {'policy': [], 'caption': [], 'qa': [], 'site': [], 'post': [], 'f_mail': [], 's_mail': [],
             'date': [], 'how_to': [], 'profile': [], 'majime': [], 'ap_mail': []}
    category_list = ['ap_mail', 'profile', 'post', 'f_mail', 's_mail', 'date', 'how_to', 'site', 'caption', 'qa',
                     'policy', 'majime']
    for id_num in pk_dic:
        h_dec[pk_dic[id_num]['category']].append([pk_dic[id_num]['file_path'], pk_dic[id_num]['title']])
    for category in h_dec:
        h_dec[category].sort(key=lambda x: x[0])
    # html site map
    h_str = '<ul class="arlist" id="deaikei"><li><a href="{}">{}</a><ul>'.format(pk_dic[32]['file_path'],
                                                                                 pk_dic[32]['title'])
    for category in category_list:
        if category != 'majime':
            h_str += '<li><a href="{}">{}</a><ul>'.format(pk_dic[pd['category_data'][category][2]]['file_path'],
                                                          pk_dic[pd['category_data'][category][2]]['title'])
            if h_dec[category]:
                for page in h_dec[category]:
                    if 'index.html' not in page[0]:
                        h_str += '<li><a href="{}">{}</a></li>'.format(page[0], page[1])
            h_str += '</ul></li>'
    h_str += '</ul>'
    h_str = h_str.replace('</li><li><a href="site/index.html">',
                          '</li></ul></li><li><a href="site/index.html">')
    h_str = h_str.replace('<a href="', '<a href="../')
    with open(pd['h_sitemap_path'], 'r', encoding='utf-8') as f:
        long_str = f.read()
        long_str = file_upload.tab_and_line_feed_remove_from_str(long_str)
        long_str = re.sub('</h2>.*?</section>', '</h2>' + h_str + '</section>', long_str)
        with open(pd['h_sitemap_path'], 'w', encoding='utf-8') as g:
            g.write(long_str)
    # category page
    ct_cat = list(set([pk_dic[x]['category'] for x in title_change_id]))
    for cat in ct_cat:
        if cat in ['ap_mail', 'profile', 'post', 'f_mail', 's_mail', 'date', 'how_to']:
            directory = 'majime'
        else:
            directory = cat
        if cat != 'qa' and cat != 'majime':
            with open('reibun/html_files/pc/' + directory + '/' + pd['category_data'][cat][1], 'r', encoding='utf-8') \
                    as h:
                long_str = h.read()
            long_str = file_upload.tab_and_line_feed_remove_from_str(long_str)
            cat_str = cat_index_str_maker(h_dec[cat], directory)
            long_str = re.sub(r'<!--index/s-->.*?<!--index/e-->', '<!--index/s-->' + cat_str + '<!--index/e-->',
                              long_str)
            with open('reibun/html_files/pc/' + directory + '/' + pd['category_data'][cat][1], 'w', encoding='utf-8') \
                    as k:
                k.write(long_str)
        if cat == 'majime' or directory == 'majime':
            with open('reibun/html_files/pc/majime/index.html', 'r', encoding='utf-8') as i:
                long_str = i.read()
            long_str = file_upload.tab_and_line_feed_remove_from_str(long_str)
            cat_str_m = cat_index_str_maker(h_dec[cat], directory)
            long_str = re.sub(r'<!--' + cat + '-i/s-->.*?<!--' + cat + '-i/e-->',
                              '<!--' + cat + '-i/s-->' + cat_str_m.replace(' id="cat_index"', '')
                              + '<!--' + cat + '-i/e-->', long_str)
            with open('reibun/html_files/pc/majime/index.html', 'w', encoding='utf-8') as j:
                j.write(long_str)


def reibun_qa_check(pk_dic, change_files, title_change_id):
    for c_id in title_change_id:
        if pk_dic[c_id]['category'] == 'qa':
            qa_index_list_insert(pk_dic)
            change_files.append('reibun/html_files/pc/qa/index.html')
            break
    return change_files


def qa_index_list_insert(pk_dic):
    qa_list = [[pk_dic[x]['file_path'], pk_dic[x]['title']] for x in pk_dic if pk_dic[x]['category'] == 'qa']
    # print(qa_list)
    for i in range(len(qa_list)):
        with open('reibun/html_files/pc/' + qa_list[i][0], 'r', encoding='utf-8') as f:
            long_str = f.read()
        if '<div class="rm_b' in long_str:
            question = re.findall(r'<div class="icon"><div class="rm_b.+?></div></div>(.+?)</div>', long_str)[0]
        elif '<h2>出会い系Ｑ＆Ａ 質問</h2>' in long_str:
            question = re.findall(r'<h2>出会い系Ｑ＆Ａ 質問</h2>(.+?)</section>', long_str)[0]
        else:
            question = ''
        question = re.sub(r'<.+?>', '', question)
        qa_list[i].append(question)
    index_str = ''.join(
        ['<li><a href="{}">{}</a><span>{}</span></li>'.format(y[0].replace('qa/', ''), y[1], y[2]) for y in qa_list])
    index_str = '<ul class="libut">' + index_str + '</ul>'
    with open('reibun/html_files/pc/qa/index.html', 'r', encoding='utf-8') as g:
        target_str = g.read()
    target_str = re.sub(r'<!--qa-index/s-->.*?<!--qa-index/e-->',
                        '<!--qa-index/s-->' + index_str + '<!--qa-index/e-->', target_str)
    with open('reibun/html_files/pc/qa/index.html', 'w', encoding='utf-8') as h:
        h.write(target_str)


def xml_site_map_maker(pk_dic, pd):
    pk_list = [[pk_dic[x]['file_path'], pk_dic[x]['mod_date']] for x in pk_dic]
    pk_list.sort(key=lambda y: y[0])
    now = datetime.datetime.now()
    xml_str = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="https://www.sitemaps.org/schemas/sitemap/0.9">' \
              '<url><loc>https://www.' + pd['domain_str'] + '</loc><lastmod>' + str(now.date()) \
              + '</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>'
    for page in pk_list:
        if '_test' not in page[0] and '_copy' not in page[0]:
            if 'index.html' in page[0]:
                page_url = page[0].replace('/index.html', '/')
            else:
                page_url = page[0]
            xml_str += '<url><loc>https://www.' + pd['domain_str'] + '/' + pd['main_dir'] + page_url + '</loc><lastmod>' \
                       + page[1] + '</lastmod><changefreq>weekly</changefreq><priority>0.5</priority></url>'
    xml_str += '</urlset>'
    if pd['project_dir'] == 'reibun':
        s_path = 'reibun/html_files/p_sitemap.xml'
    else:
        s_path = pd['project_dir'] + '/html_files/sitemap.xml'
    with open(s_path, 'w', encoding='utf-8') as f:
        f.write(xml_str)


def cat_index_str_maker(cat_dic, directory):
    cat_str = '<ul class="libut" id="cat_index">'
    for page_i in cat_dic:
        if len(page_i) < 3:
            cat_str += '<li><a href="{}">{}</a></li>'.format(page_i[0].replace(directory + '/', ''),
                                                             re.sub(r'【.+?】', '', page_i[1]))
        else:
            cat_str += '<li><a href="{}">{}<span>{}</span></a></li>'.format(page_i[0].replace(directory + '/', ''),
                                                                            re.sub(r'【.+?】', '', page_i[1]), page_i[2])
    cat_str += '</ul>'
    return cat_str


def insert_sidebar_to_existing_art(side_bar_dic, title_change_id, pk_dic, pd, ad_side_bar_dic):
    change_files = []
    # print(pk_dic)
    insert_cat = list(set([pk_dic[x]['category'] for x in title_change_id]))
    if pd['side_bar_list']['important'] or pd['side_bar_list']['pop']:
        for sb_cat in pd['side_bar_list']:
            for change_id in title_change_id:
                if change_id in pd['side_bar_list'][sb_cat]:
                    insert_cat.append(sb_cat)
                    break
    else:
        if not pd['side_bar_list']['important']:
            insert_cat.append('important')
        if not pd['side_bar_list']['pop']:
            insert_cat.append('pop')
    all_html_path = [x for x in glob.glob(pd['project_dir'] + '/html_files/' + pd['main_dir'] + '**/**.html',
                                          recursive=True)
                     if '_test' not in x and '_copy' not in x and x not in pd['ignore_files'] and '/template/' not in x]
    if pd['project_dir'] != 'reibun':
        all_html_path = all_html_path + [x for x in
                                         glob.glob(pd['project_dir'] + '/html_files/' + pd['main_dir'] + '**.html',
                                                   recursive=True)
                                         if '_test' not in x and '_copy' not in x and x not in pd[
                                             'ignore_files'] and '/template/' not in x]
    for html_path in all_html_path:
        with open(html_path, 'r', encoding='utf-8') as f:
            long_str = f.read()
        if (pd['project_dir'] == 'konkatsu' or pd[
            'project_dir'] == 'online_marriage') and '<!--adult_art-->' in long_str:
            t_side_bar_dic = ad_side_bar_dic
        else:
            t_side_bar_dic = side_bar_dic
        if '<!--no_change-->' not in long_str:
            long_str = file_upload.tab_and_line_feed_remove_from_str(long_str)
            category = re.findall(r'<!--category_(.+?)-->', long_str)[0]
            long_str = insert_sidebar_to_str(long_str, t_side_bar_dic, category, insert_cat, pd)
            long_str = modify_relation_list(long_str, title_change_id, pk_dic)
            with open(html_path, 'w', encoding='utf-8') as g:
                g.write(long_str)
                change_files.append(html_path)
    return change_files


def insert_sidebar_to_str(long_str, side_bar_dic, category, insert_cat, pd):
    if 'pop' in insert_cat:
        if category == 'top':
            pop_str = side_bar_dic['pop'].replace('"../', '"')
        else:
            pop_str = side_bar_dic['pop']
        long_str = re.sub(r'"sbh">人気記事</div><ul>.+?</ul></div>', '"sbh">人気記事</div><ul>' + pop_str + '</ul></div>',
                          long_str)
    if 'important' in insert_cat:
        if category == 'top':
            imp_str = side_bar_dic['important'].replace('"../', '"')
        else:
            imp_str = side_bar_dic['important']
        long_str = re.sub(r'"sbh">重要記事</div><ul>.+?</ul></div>', '"sbh">重要記事</div><ul>' + imp_str + '</ul></div>',
                          long_str)
    if category == 'top':
        new_str = side_bar_dic['new'].replace('"../', '"')
    else:
        new_str = side_bar_dic['new']
    long_str = re.sub(r'"sbh">最近の更新記事</div><ul>.+?</ul></div>',
                      '"sbh">最近の更新記事</div><ul>' + new_str + '</ul></div>', long_str)
    if category in insert_cat and category in pd['category_name']:
        long_str = re.sub(r'<div class="leftnav"><div class="sbh cat-i">.*?</div><ul>.*?</ul></div>',
                          '<div class="leftnav"><div class="sbh cat-i">' + pd['category_name'][category][0]
                          + '</div><ul>' + side_bar_dic[category] + '</ul></div>', long_str)
    return long_str


def insert_sidebar_to_modify_page(side_bar_dic, mod_list, pd, ad_side_bar_dic):
    for r_file in mod_list:
        r_file = r_file.replace('/md_files/', '/html_files/').replace('.md', '.html')
        with open(r_file, 'r', encoding='utf-8') as f:
            long_str = f.read()
            if (pd['project_dir'] == 'konkatsu' or pd['project_dir'] == 'online_marriage') and \
                    '<!--adult_art-->' in long_str:
                t_side_bar_dic = ad_side_bar_dic
            else:
                t_side_bar_dic = side_bar_dic
            long_str = file_upload.tab_and_line_feed_remove_from_str(long_str)
            category = re.findall(r'<!--category_(.+?)-->', long_str)[0]
            long_str = re.sub(r'"sbh">人気記事</div><ul>.+?</ul></div>',
                              '"sbh">人気記事</div><ul>' + t_side_bar_dic['pop'] + '</ul></div>', long_str)
            long_str = re.sub(r'"sbh">重要記事</div><ul>.+?</ul></div>',
                              '"sbh">重要記事</div><ul>' + t_side_bar_dic['important'] + '</ul></div>', long_str)
            long_str = re.sub(r'"sbh">最近の更新記事</div><ul>.+?</ul></div>',
                              '"sbh">最近の更新記事</div><ul>' + t_side_bar_dic['new'] + '</ul></div>', long_str)
            if category in pd['category_name']:
                long_str = re.sub(r'<div class="leftnav"><div class="sbh cat-i">.*?</div><ul>.*?</ul></div>',
                                  '<div class="leftnav"><div class="sbh cat-i">' + pd['category_name'][category][0]
                                  + '</div><ul>' + t_side_bar_dic[category] + '</ul></div>', long_str)
            with open(r_file, 'w', encoding='utf-8') as g:
                g.write(long_str)


def make_all_side_bar(pk_dic, pd):
    cat_dic = {x: [] for x in pd['category_data']}
    pk_list = [pk_dic[i] for i in pk_dic]
    # print(pk_dic)
    # print(pk_list)
    sorted_list = sorted(pk_list,
                         key=lambda x: datetime.date(datetime.datetime.strptime(x['mod_date'], '%Y-%m-%d').year,
                                                     datetime.datetime.strptime(x['mod_date'], '%Y-%m-%d').month,
                                                     datetime.datetime.strptime(x['mod_date'], '%Y-%m-%d').day),
                         reverse=True)
    new_art = sorted_list[:10]
    new_str = ''.join(['<li><a href="../{}">{}</a></li>'.format(y['file_path'], re.sub(r'【.+?】', '', y['title']))
                       for y in new_art])
    for id_pk in pk_dic:
        if pk_dic[id_pk]['category'] in pd['category_data']:
            cat_dic[pk_dic[id_pk]['category']].append('<li><a href="../{}">{}</a></li>'.format(
                pk_dic[id_pk]['file_path'], re.sub(r'【.+?】', '', pk_dic[id_pk]['title'])))
    result_dic = {x: ''.join(cat_dic[x]) for x in cat_dic}
    result_dic['new'] = new_str
    for z in pd['side_bar_list']:
        if pd['side_bar_list'][z]:
            id_list = pd['side_bar_list'][z]
        else:
            keys = list(pk_dic.keys())[:]
            numpy.random.shuffle(keys)
            id_list = keys[:10]
            # print(pk_dic)
        result_dic[z] = ''.join(
            ['<li><a href="../{}">{}</a></li>'.format(pk_dic[use_id]['file_path'],
                                                      re.sub(r'【.+?】', '', pk_dic[use_id]['title'])) for use_id in
             id_list])
    return result_dic


def ad_make_all_side_bar(pk_dic, pd):
    # for p in pk_dic:
    #     if 'ad_flag' not in pk_dic[p]:
    #         print(pk_dic[p])
    nm_pk_dict = {i: pk_dic[i] for i in pk_dic if pk_dic[i]['ad_flag'] == 3}
    ad_pk_dict = {i: pk_dic[i] for i in pk_dic if pk_dic[i]['ad_flag'] == 1}
    # print(pk_dic)
    # print(pk_list)
    result = []
    # print(ad_pk_dict)
    for this_pk in [nm_pk_dict, ad_pk_dict]:
        cat_dic = {x: [] for x in pd['category_data']}
        pk_list = [this_pk[i] for i in this_pk]
        sorted_list = sorted(pk_list,
                             key=lambda x: datetime.date(datetime.datetime.strptime(x['mod_date'], '%Y-%m-%d').year,
                                                         datetime.datetime.strptime(x['mod_date'], '%Y-%m-%d').month,
                                                         datetime.datetime.strptime(x['mod_date'], '%Y-%m-%d').day),
                             reverse=True)
        new_art = sorted_list[:10]
        new_str = ''.join(['<li><a href="../{}">{}</a></li>'.format(y['file_path'], re.sub(r'【.+?】', '', y['title']))
                           for y in new_art])

        for id_pk in this_pk:
            if this_pk[id_pk]['category'] in pd['category_data']:
                cat_dic[this_pk[id_pk]['category']].append('<li><a href="../{}">{}</a></li>'.format(
                    this_pk[id_pk]['file_path'], re.sub(r'【.+?】', '', this_pk[id_pk]['title'])))
        result_dic = {x: ''.join(cat_dic[x]) for x in cat_dic}
        result_dic['new'] = new_str
        for z in pd['side_bar_list']:
            if pd['side_bar_list'][z]:
                id_list = pd['side_bar_list'][z]
            else:
                keys = list([k for k in this_pk])[:]
                numpy.random.shuffle(keys)
                id_list = keys[:10]
                # print(this_pk)
            result_dic[z] = ''.join(
                ['<li><a href="../{}">{}</a></li>'.format(this_pk[use_id]['file_path'],
                                                          re.sub(r'【.+?】', '', this_pk[use_id]['title'])) for use_id in
                 id_list])
        result.append(result_dic)
        # print(result_dic)
    return result[0], result[1]


def make_rss(new_file_data, pd):
    now = datetime.datetime.now()
    now_str = str(now)[:-7]
    # rss1.0
    with open(pd['project_dir'] + '/html_files/' + pd['main_dir'] + 'template/rss10.xml', 'r', encoding='utf-8') as f:
        rss1_str = f.read()
        if new_file_data:
            rss1_str = re.sub(r'<dc:date>.*?</dc:date>', '<dc:date>' + now_str + ' +9:00</dc:date>', rss1_str)
            list_str_l = re.findall(r'<rdf:Seq>.*?</rdf:Seq>', rss1_str)
            url_list = re.findall(r'<rdf:li rdf:resource=".+?" />', list_str_l[0])
            item_list_s = re.findall(r'</channel>.+?</rdf:RDF>', rss1_str)[0]
            item_list = re.findall(r'<item rdf:about=".+?</item>', item_list_s)
            if len(url_list) + len(new_file_data) >= 10:
                url_list = url_list[:-(len(url_list) + len(new_file_data) - 10)]
            for new_data in new_file_data:
                url_list.insert(0, '<rdf:li rdf:resource="https://www.demr.jp/pc/' + new_data[0] + '" />')
                item_list.insert(0, '<item rdf:about="https://www.demr.jp/pc/{}"><title>{}</title><link>{}</link>'
                                    '<description><![CDATA[{}]]></description><dc:creator>mail@demr.jp (goyan)'
                                    '</dc:creator><dc:date>{}</dc:date></item>'
                                 .format(new_data[0], new_data[1], new_data[0], new_data[2], now_str))
            rss1_str = rss1_str.replace(list_str_l[0], '<rdf:Seq>' + ''.join(url_list) + '</rdf:Seq>')
            rss1_str = rss1_str.replace(item_list_s, '</channel>' + ''.join(item_list) + '<</rdf:RDF>')
        else:
            rss1_str = re.sub(r'<items><rdf:Seq><rdf:li rdf:resource="記事1のURL" /></rdf:Seq></items>',
                              r'<items><rdf:Seq></rdf:Seq></items>', rss1_str)
            rss1_str = re.sub(r'</channel>.+?</rdf:RDF>',
                              r'</channel></rdf:RDF>', rss1_str)
        with open(pd['project_dir'] + '/html_files/' + pd['main_dir'] + 'rss10.xml', 'w', encoding='utf-8') as g:
            g.write(rss1_str)
    # rss2.0
    with open(pd['project_dir'] + '/html_files/' + pd['main_dir'] + 'template/rss20.xml', 'r', encoding='utf-8') as h:
        rss2_str = h.read()
        if new_file_data:
            now_j = now + datetime.timedelta(hours=9)
            now_tuple = now_j.timetuple()
            now_timestamp = time.mktime(now_tuple)
            rfc_str = utils.formatdate(now_timestamp)[:-6]
            item_list_2 = re.findall(r'<item>.+?</item>', rss2_str)
            if len(item_list_2) + len(new_file_data) >= 10:
                item_list_2 = item_list_2[:-(len(item_list_2) + len(new_file_data) - 10)]
            for new_data in new_file_data:
                item_list_2.insert(0, '<item><title>{}</title><link>https://www.demr.jp/pc/{}</link><description>{}'
                                      '</description><pubDate>{} +0900</pubDate></item>'.format(new_data[1],
                                                                                                new_data[0],
                                                                                                new_data[2], rfc_str))
            rss2_str = re.sub(r'<item>.*</item>', ''.join(item_list_2), rss2_str)
        else:
            rss2_str = re.sub(r'<item>.+?</channel>', r'</channel>', rss2_str)
        with open(pd['project_dir'] + '/html_files/' + pd['main_dir'] + 'rss20.xml', 'w', encoding='utf-8') as i:
            i.write(rss2_str)
    # atom
    with open(pd['project_dir'] + '/html_files/' + pd['main_dir'] + 'template/atom.xml', 'r', encoding='utf-8') as j:
        atom_str = j.read()
        if new_file_data:
            atom_str = re.sub(r'</title><updated>.*?</updated><link', '</title><updated>' + now_str + '</updated><link',
                              atom_str)
            item_list_a = re.findall(r'<entry>.+?</entry>', atom_str)
            if len(item_list_a) + len(new_file_data) >= 10:
                item_list_a = item_list_a[:-(len(item_list_a) + len(new_file_data) - 10)]
            for new_data in new_file_data:
                item_list_a.insert(0, "<entry><id>demr.jp/pc/{}</id><title>{}</title><link rel='alternate' "
                                      "type='text/html' href='https://www.demr.jp/pc/{}' /><updated>{}</updated>"
                                      "<summary>{}</summary></entry>".format(new_data[0], new_data[1], new_data[0],
                                                                             now_str, new_data[2]))
            atom_str = re.sub(r'<entry>.*</entry>', ''.join(item_list_a), atom_str)
        else:
            atom_str = re.sub(r'<entry>.*?</entry>', '<entry></entry>', atom_str)
        with open(pd['project_dir'] + '/html_files/' + pd['main_dir'] + 'atom.xml', 'w', encoding='utf-8') as k:
            k.write(atom_str)


def insert_tag_to_upper_anchor(long_str):
    top_str_l = re.findall(r'</h1>.+?<div id="mokujio"', long_str)
    if '<a href="#sc' in top_str_l[0]:
        a_str_l = re.findall(r'<a href="#.+?</a>', top_str_l[0])
        for a_str in a_str_l:
            r_str = a_str
            if 'class=' not in a_str:
                l_text = re.findall(r'>(.+?)<', a_str)[0]
                g_tag = "gtag('event','click',{'event_category':'inner_anchor','event_label':'" + l_text + "'});"
                r_str = re.sub(r'<a href="(.+?)">',
                               r'<a href="\1" class="upper_anchor" onClick="' + g_tag + '">', r_str)
                long_str = long_str.replace(a_str, r_str)
    return long_str


def insert_markdown_anchor(long_str):
    a_str_l = re.findall(r'href="#[^s].+?"', long_str)
    if a_str_l:
        index_str_l = re.findall(r'<nav id="mokuji">.+?</nav>', long_str)
        index_list = [[str_i[1], str_i[0]] for str_i in re.findall(r'<a href="(.+?)">(.+?)</a>', index_str_l[0])]
        for a_str in a_str_l:
            # print(a_str)
            if a_str != 'href="#header"':
                a_text = re.sub(r'href="#(.+?)"', r'\1', a_str)
                r_str = re.sub(r'href="#(.+?)"', 'href="' + [x[1] for x in index_list if x[0] == a_text][0] + '"',
                               a_str)
                long_str = long_str.replace(a_str, r_str)
    return long_str


def top_page_filter(long_str):
    long_str = long_str.replace('"../../"', './')
    long_str = long_str.replace('"../../', '"')
    long_str = long_str.replace('"../', '"../pc/')
    return long_str


def insert_page_card(long_str, pk_dic, pd):
    if '[card]' in long_str:
        card_str_l = re.findall(r'\[card]\(.+?\)', long_str)
        card_str_l = list(set(card_str_l))
        before_replace_str = '../' * (pd['main_dir'].count('/')) + '../../html_files/' + pd['main_dir']
        for card_str in card_str_l:
            card_url = re.findall(r'\((.+?)\)', card_str)[0]
            c_url = card_url.replace(before_replace_str, '')
            for page_id in pk_dic:
                if pk_dic[page_id]['file_path'] == c_url:
                    url_str = card_url.replace('../' * (pd['main_dir'].count('/')) + '../html_files/' + pd['main_dir'],
                                               '')
                    img_str = re.sub(pd['project_dir'] + '/html_files/' + pd['main_dir'] + r'.+?/(.+?).html',
                                     r'../images/art_images/\1_thumb.jpg', c_url)
                    replace_str = '<div class="ar_card"><a href="{}"><div class="ar_in"><div class="ac_img">' \
                                  '<img src="{}" alt="{}" /></div><div class="ac_r"><span class="p_title">{}</span>' \
                                  '<span class="ar_dis">{}</span></div></div></a>' \
                                  '</div>'.format(url_str, img_str, pk_dic[page_id][1], pk_dic[page_id][1],
                                                  pk_dic[page_id][5][:100] + '...')
                    # print(replace_str)
                    long_str = long_str.replace(card_str, replace_str)
    return long_str


def short_cut_filter(long_str, pd, md_file_path):
    if '%pcmax%' in long_str:
        p_str = '[{}]({}html_files/{}{})'.format('PCMAX', '../' * (md_file_path.count('/') - 1), pd['main_dir'],
                                                 pd['sc_url']['PCMAX'])
        long_str = long_str.replace('%pcmax%', p_str)
    for sc in pd['sc_url']:
        if '%' + sc + '%' in long_str:
            l_str = '[{}]({}html_files/{}{})'.format(sc, '../' * (md_file_path.count('/') - 1), pd['main_dir'],
                                                     pd['sc_url'][sc])
            long_str = long_str.replace('%' + sc + '%', l_str)
    return long_str


def import_from_markdown(md_file_list, site_shift, now, pd, mod_flag, first_time_flag, fixed_mod_date):
    upload_list = []
    title_change_id = []
    if pd['site_shift_list']:
        pd['site_shift_list'].remove(site_shift)
    if not os.path.exists(pd['project_dir'] + '/html_files/' + pd['main_dir'] + 'template/main_tmp.html'):
        if not os.path.exists(pd['project_dir'] + '/html_files'):
            os.mkdir(pd['project_dir'] + '/html_files')
        if pd['main_dir']:
            if not os.path.exists(pd['project_dir'] + '/html_files' + pd['main_dir']):
                os.mkdir(pd['project_dir'] + '/html_files' + pd['main_dir'])
        if not os.path.exists(pd['project_dir'] + '/html_files/' + pd['main_dir'] + 'template'):
            os.mkdir(pd['project_dir'] + '/html_files/' + pd['main_dir'] + 'template')
        shutil.copy('template_files/template/main_tmp.html', pd['project_dir'] + '/html_files/' + pd['main_dir']
                    + 'template/main_tmp.html')
    with open(pd['project_dir'] + '/html_files/' + pd['main_dir'] + 'template/main_tmp.html', 'r', encoding='utf-8') \
            as t:
        tmp_str = t.read()
    if os.path.exists(pd['project_dir'] + '/pickle_pot/main_data.pkl'):
        pk_dic = make_article_list.read_pickle_pot('main_data', pd)
    else:
        pk_dic = {}
    # print(make_article_list.read_pickle_pot('main_data', pd))
    # return
    for md_file_path in md_file_list:
        print('start : ' + md_file_path)
        file_name = md_file_path.replace(pd['project_dir'] + '/md_files/' + pd['main_dir'], '').replace('.md', '.html')
        # print('file_name : ' + file_name)
        with open(md_file_path, 'r', encoding='utf-8') as f:
            plain_txt = f.read()
        plain_txt = re.sub(r'recipe_list = {[\s\S]+$', '', plain_txt)
        if '%kanren%' in plain_txt:
            plain_txt = relational_article.collect_md_relation_title_in_str(plain_txt, pk_dic, md_file_path)
        plain_txt = short_cut_filter(plain_txt, pd, md_file_path)
        plain_txt = insert_ds_link(plain_txt, pd)
        md_txt = plain_txt
        # print(md_txt)

        description = re.findall(r'd::(.*?)\n', md_txt)[0]
        if 'p::' in md_txt:
            pub_date = re.findall(r'p::(.*?)\n', md_txt)[0]
        else:
            if fixed_mod_date:
                pub_date = fixed_mod_date
            else:
                pub_date = ''

        if 'l_path = ::' in md_txt:
            keyword_str = re.findall(r'k::(.*?)\n', md_txt)[0]
            if '&' in keyword_str:
                print('There is "&" !')
            keyword = keyword_str.split(' ')
            if '' in keyword:
                keyword.remove('')
        else:
            keyword = ''
        if 'e::' in plain_txt:
            edit_l = re.findall(r'\ne::(.*?)\n', plain_txt)
            if edit_l:
                if 'all' in edit_l:
                    edit_flag = True
                else:
                    edit_flag = False
            else:
                edit_flag = False
        else:
            edit_flag = True
        if pd['project_dir'] == 'konkatsu' or pd['project_dir'] == 'online_marriage':
            if 'a::' in plain_txt:
                ad_flag = int(re.findall(r'a::(\d+?)\n', plain_txt)[0])
            else:
                print('ad_flag error!!!')
                ad_flag = ''
        else:
            ad_flag = ''
        if 'n::' in plain_txt:
            this_id = int(re.findall(r'n::(\d+?)\n', plain_txt)[0])
        else:
            print('no id : ' + md_file_path)
            this_id = len(pk_dic)
            plain_txt = re.sub(r'(d::.*?\n)', r'\1n::' + str(this_id) + r'\n', plain_txt)
        title_str = re.findall(r't::(.+?)\n', md_txt)[0]
        plain_txt = re.sub(r'\n# .+?\n', r'\n# ' + title_str + r'\n', plain_txt)
        md_txt = additional_replace_in_md(md_txt, pd)

        if '%ss' in md_txt:
            ss_flag = True
            for ss_num in pd['site_shift_order']:
                if md_txt.count('%ss' + str(ss_num) + '%') != md_txt.count('%ss' + str(ss_num) + '%'):
                    raise Exception('%ss の数が合っていません！！')
            for shift_num in pd['site_shift_order']:
                if '%ss' + str(shift_num) in md_txt:
                    md_txt = re.sub(r'%ss' + str(shift_num) + r'%\n([\s\S]*?)%ss' + str(shift_num) + r'e%\n', r'\1',
                                    md_txt)
                    md_txt = re.sub(r'%ss\d%\n([\s\S]*?)%ss\de%\n', '', md_txt)
                    break
        else:
            ss_flag = False
        if '%arlist' in md_txt:
            arlist_o_l = re.findall(r'%arlist%\n([\s\S]*?)\n\n', md_txt)
            if arlist_o_l:
                for arlist_o in arlist_o_l:
                    if '%%%' in arlist_o:
                        arlist_l = re.findall(r'- (.*?)\n', arlist_o)
                        for arlist in arlist_l:
                            if '%%%' in arlist:
                                ar_re = re.sub(r'(.+?)%%%', r'<em>\1</em><br />', arlist)
                                md_txt = md_txt.replace(arlist, ar_re)
            md_txt = re.sub(r'%arlist%\n([\s\S]*?)\n\n', r'<!--arlist-->\n\n\n\1\n\n<!--e/arlist-->', md_txt)
            md_txt = re.sub(r'%arlist_b%\n([\s\S]*?)\n\n', r'<!--arlist-b-->\n\n\n\1\n\n<!--e/arlist_b-->', md_txt)
        md_txt = insert_site_banner(md_txt, pd)
        if '%kanren%' in md_txt:
            md_txt = re.sub(r'%kanren%\n([\s\S]*?)\n\n',
                            r'<!--last-section-->\n<!--kanren-->\n\n\n\1\n\n<!--e/kanren-->',
                            md_txt)
        else:
            md_txt = md_txt + '<!--last-section-->'
        # print(md_txt)
        md_txt = re.sub(r'%btnli%\n([\s\S]*?)\n\n', r'<!--btnli-->\n\n\n\1\n\n<!--e/btnli-->', md_txt)
        md_txt = re.sub(r'%point%\n([\s\S]*?)\n\n', r'<!--point-->\n\n\n\1\n\n<!--e/point-->', md_txt)
        md_txt = re.sub(r'%matome%\n([\s\S]*?)\n\n', r'\n<!--matome-->\n\n\n\1\n\n<!--e/matome-->', md_txt)
        md_txt = re.sub(r'%p%\n([\s\S]*?)\n\n', r'<!--point_i-->\n\n\n\1\n\n<!--e/point_i-->', md_txt)
        md_txt = icon_filter(md_txt, pd)

        md_txt = md_txt.replace('%sample%', '<!--sample/s-->')
        md_txt = md_txt.replace('%sample/e%', '<!--sample/e-->')
        md_txt = mail_sample_replace(md_txt)
        md_txt = strong_insert_filter(md_txt)
        # card挿入
        # md_txt = insert_page_card(md_txt, pk_dic) todo: 完成させる
        md_txt = re.sub(r'\(\)\[.*?]\n', '', md_txt)
        md_txt = re.sub(r'\n(<!--.+?-->)\n', r'\n\1', md_txt)
        # md_txt = re.sub(r'>[\s]+?<', '><', md_txt)
        md_txt = md_txt.replace('--><!--', '-->\n<!--')
        if '\n# ' not in md_txt:
            md_txt = re.sub(r'\n[a-zA-Z]::.*?\n', '\n', md_txt)
            md_txt = re.sub(r't::.*?\n', '\n', md_txt)
            md_txt = re.sub(r'n::.*?\n', '\n', md_txt)
            md_txt = re.sub(r'k::.*?\n', '\n', md_txt)
            md_txt = re.sub(r'e::.*?\n', '\n', md_txt)
            md_txt = re.sub(r'a::.*?\n', '\n', md_txt)
            md_txt = re.sub(r'p::.*?\n', '\n', md_txt)
            md_txt = re.sub(r'^[a-zA-Z]::.*?\n', '\n', md_txt)
            md_txt = re.sub(r'^\n*', '', md_txt)
        # print(md_txt)

        print('markdown start!')
        con_str = markdown.markdown(md_txt, extensions=['tables'])
        con_str = con_str.replace('\n', '')
        con_str = re.sub(r'^([\s\S]*)</h1>', '', con_str)
        # print(con_str)
        directory, category = directory_and_category_select(file_name, pd)
        title = re.sub(r'%(.+?)%', r'【\1】', title_str)
        new_str = tmp_str.replace('<!--title-->', title)
        new_str = new_str.replace('<!--h1-->', title)  # titleから()削除しないver.
        new_str = new_str.replace('<!--meta-key-->', ','.join(keyword))
        new_str = new_str.replace('<!--file-path-->', file_name)
        new_str = new_str.replace('<!--category-->', category)
        new_str = new_str.replace('<!--category_str-->', '<!--category_{}-->'.format(category))
        new_str = new_str.replace('<!--main-content-->', con_str)
        new_str = new_str.replace('<!--id_num-->', '<!--id_num_{}-->'.format(str(this_id)))
        new_str = new_str.replace('<h2>', '<!--p-index--><h2>', 1)
        if pd['project_dir'] == 'konkatsu' or pd['project_dir'] == 'online_marriage':
            if ad_flag == 1:
                new_str = new_str.replace('<!--ad-flag-->', '<!--adult_art-->')
            else:
                new_str = new_str.replace('<!--ad-flag-->', '')
        new_str = common_tool.index_maker(new_str)
        new_str = common_tool.section_insert(new_str)
        if '"mokuji"' in new_str:
            new_str = insert_markdown_anchor(new_str)
            new_str = insert_tag_to_upper_anchor(new_str)
        if pd['project_dir'] == 'reibun':
            new_str = change_category_class(new_str, category, pd)
        if fixed_mod_date:
            new_str = new_str.replace('<!--mod-date-->', fixed_mod_date)
            new_str = new_str.replace('<!--mod-date-j-->', fixed_mod_date.replace('-', '/').replace('/0', '/'))
            new_str = new_str.replace('<!--pub-date-->', fixed_mod_date)
            new_str = new_str.replace('<!--pub-date-j-->', fixed_mod_date.replace('-', '/').replace('/0', '/'))
        elif mod_flag or not os.path.exists(pd['project_dir'] + '/html_files/' + pd['main_dir'] + file_name):
            new_str = new_str.replace('<!--mod-date-->', str(now.date()))
            new_str = new_str.replace('<!--mod-date-j-->', str(now.year) + '/' + str(now.month) + '/' + str(now.day))
            if pub_date:
                new_str = new_str.replace('<!--pub-date-->', pub_date)
                if 'T' in pub_date:
                    pub_date_j = re.sub(r'T.*$', '', pub_date)
                else:
                    pub_date_j = pub_date
                new_str = new_str.replace('<!--pub-date-j-->', pub_date_j.replace('-', '/').replace('/0', '/'))
            else:
                new_str = new_str.replace('<!--pub-date-->', str(now.date()))
                pub_date = str(now.date())
                new_str = new_str.replace('<!--pub-date-j-->', str(now.year) + '/' + str(now.month) + '/'
                                          + str(now.day))
        else:
            p_date = pk_dic[this_id]['pub_date']
            m_date = pk_dic[this_id]['mod_date']
            new_str = new_str.replace('<!--mod-date-->', m_date)
            new_str = new_str.replace('<!--mod-date-j-->', m_date.replace('-', '/').replace('/0', '/'))
            new_str = new_str.replace('<!--pub-date-->', p_date)
            new_str = new_str.replace('<!--pub-date-j-->', p_date.replace('-', '/').replace('/0', '/'))

        new_str = new_str.replace('<!--kanren-->', '<section><div class="kanren"><h2>関連記事</h2>')
        new_str = new_str.replace('<!--e/kanren-->', '</div></section>')

        new_str = insert_additional_str(new_str, pd)

        new_str = logical_box_filter(new_str)
        new_str, add_list, plain_txt = img_str_filter(new_str, file_name, plain_txt, pd)
        if pd['project_dir'] == 'reibun':
            new_str = img_filter(new_str, pd)
        new_str = re.sub(r'<p>(<img .+?/>)</p>', r'<div class="center">\1</div>', new_str)

        new_str = new_str.replace('<!--btnli-->', '<div class="btnli">')
        new_str = new_str.replace('<!--e/btnli-->', '</div>')
        new_str = new_str.replace('<!--arlist--><ul>', '<ul class="arlist">')
        new_str = new_str.replace('</ul><!--e/arlist-->', '</ul>')

        new_str = new_str.replace('<!--point-->', '<div id="kijip"><div class="kijoph"><p>この記事のポイント</p>' +
                                  '</div>')
        new_str = new_str.replace('<!--e/point-->', '</div>')
        new_str = new_str.replace('<!--matome-->', '<div id="kijim"><div class="kijoph"><p>この記事のまとめ</p>' +
                                  '</div>')
        new_str = new_str.replace('<!--e/matome-->', '</div>')
        new_str = new_str.replace('<!--point_i-->', '<div class="in_point"><span>ポイント</span>')
        new_str = new_str.replace('<!--e/point_i-->', '</div>')
        new_str = new_str.replace('<ol>', '<ol class="arlist">')
        new_str = new_str.replace('<div class="hidden_show"><ol class="arlist">', '<div class="hidden_show"><ol>')
        new_str = new_str.replace('<br /></p>', '</p>')
        new_str = new_str.replace('。。<br />', '。</p><p>')
        new_str = new_str.replace('。。', '。</p><p>')
        new_str = new_str.replace('）。<br />', '）</p><p>')
        new_str = new_str.replace(')。<br />', ')</p><p>')
        new_str = new_str.replace(')。', ')</p><p>')
        new_str = new_str.replace('）。', '）</p><p>')
        new_str = new_str.replace('？。', '？<br />')
        new_str = new_str.replace('？。。', '？</p><p>')
        new_str = new_str.replace('<!--e/rm--></p>', '</p><!--e/rm-->')
        new_str = re.sub(r'<!--e/rm--><!--rm_(\d)--></p>', r'</p><!--e/rm--><!--rm_\1-->', new_str)
        for lr_str in ['r', 'l']:
            rm_str_l = re.findall(r'<!--' + lr_str + 'm_.+?<!--e/' + lr_str + 'm-->', new_str)
            if rm_str_l:
                for rm_str in rm_str_l:
                    rm_replace = rm_str.replace('。', '。<br />')
                    new_str = new_str.replace(rm_str, rm_replace)
        new_str = re.sub(r'([^>])。([^<])', r'\1。<br />\2', new_str)
        new_str = new_str.replace('。<a ', '。<br /><a ')
        new_str = new_str.replace('。<br />）', '。）')
        new_str = new_str.replace('。<br />)', '。)')
        new_str = new_str.replace('！。<br />', '！<br />')
        new_str = new_str.replace('。<br /></p>', '。</p>')
        new_str = re.sub(r'(件名: .+?)<br />', r'<span class="m_title">\1</span>', new_str)
        new_str = new_str.replace('<table>', '<table class="tb_n">')
        new_str = new_str.replace('<td align="center">', '<td class="al_c">')

        new_str = re.sub(r'<!--lm_(\d)-->',
                         r'<div class="fl1"><div class="icon"><div class="lm_b lm_\1"></div></div>', new_str)
        new_str = new_str.replace('<!--e/lm-->', '</div>')
        new_str = re.sub(r'<!--rm_(\d)-->',
                         r'<div class="fr2"><div class="icon"><div class="rm_b rm_\1"></div></div>', new_str)
        new_str = re.sub(r'<!--rw_(\d)-->',
                         r'<div class="fr2"><div class="icon"><div class="rw_b rw_\1"></div></div>', new_str)
        new_str = re.sub(r'<!--sw-.+?-->', '', new_str)
        new_str = re.sub(r'<!--rs-.+?-->', '', new_str)

        new_str = new_str.replace('<!--e/rm-->', '</div>')
        new_str = new_str.replace('<!--e/rw-->', '</div>')
        if pd['project_dir'] == 'reibun':
            br_str = reibun.main_info.reibun_breadcrumb_maker(category, directory, file_name)
            new_str = new_str.replace('../../../html_files/app', '../../app')
        else:
            br_str = breadcrumb_maker(directory, file_name, pd)
        new_str = new_str.replace('<!--bread-->', br_str)
        new_str = new_str.replace('"../../' + '../' * pd['main_dir'].count('/') + 'html_files/' + pd['main_dir'],
                                  '"../')
        new_str = new_str.replace('<!--sample/s-->', '<div class="sample">')
        new_str = new_str.replace('<!--sample/e-->', '</div>')

        if 'i::' in md_txt:
            t_image_l = re.findall(r'i::(.+?)\n', md_txt)
            t_image = t_image_l[0]
        else:
            if '_1_gr.jpg' in new_str:
                t_img_l = re.findall(r'<div class="alt_img_t"><img src="(.*?/images/' + pd['ar_img_dir'] +
                                     r'/.+?_1_gr\.jpg)"', new_str)
                if t_img_l:
                    t_image = t_img_l[0].replace('../images/', '')
                else:
                    t_image = pd['default_img']
            else:
                t_image = pd['default_img']
        new_str = new_str.replace('<!--t-image-->', t_image)
        new_str = new_str.replace('<!--description-->', description)
        new_str = new_str.replace('.md"', '.html"')
        new_str = new_str.replace('<p>%libut%</p><ul>', '<ul class="libut">')
        # ar_str_l = re.findall(r'<article.+?</article>', new_str)
        # if ar_str_l:
        #     ar_str = ar_str_l[0]
        #     ar_str_c = ar_str.replace('<ul>', '<ul class="libut">')
        #     new_str = new_str.replace(ar_str, ar_str_c)
        new_str = json_img_data_insert(new_str, pd)
        card_br_l = re.findall(r'<span class="ar_dis">.+?</span>', new_str)
        if card_br_l:
            for card_br in card_br_l:
                new_str = new_str.replace(card_br, card_br.replace('<br />', ''))

        upload_list.extend(add_list)
        upload_list.extend(pick_up_same_name_images(file_name, pd))
        if md_file_path == pd['project_dir'] + '/md_files/index.md':
            with open(pd['project_dir'] + '/html_files/index.html', 'r', encoding='utf-8') as h:
                top_long_str = h.read()
                if pd['project_dir'] == 'reibun':
                    mod_log = re.findall(r'<div id="update"><ul class="updli">.+?</ul></div></div>', top_long_str)[0]
                else:
                    mod_log = re.findall(r'<ul class="updli">.+?</ul>', top_long_str)[0]
            top_page_filter(new_str)
            new_str = new_str.replace('</article>',
                                      '<section><div class="tabn"><h2>主な更新履歴</h2>' + mod_log +
                                      '</section></article>')
        str_len = count_main_str_length(new_str, file_name)
        layout_flag = check_page_layout(new_str)
        # print(new_str)
        if mod_flag:
            if os.path.exists(pd['project_dir'] + '/html_files/' + pd['main_dir'] + file_name) and not first_time_flag:
                pub_or_mod = 'mod'
                # print(pk_dic)
                if pk_dic[this_id]['title'] != title_str:
                    update_title_log(file_name, title_str, str(now.date()), str_len, pd)
                    title_change_id.append(this_id)
                    print('title change: ' + file_name)
                elif str_len > pk_dic[this_id]['str_len'] + 300:
                    update_title_log(file_name, title_str, str(now.date()), str_len, pd)
                new_mod_date = str(now.date())
            else:
                update_title_log(file_name, title_str, str(now.date()), str_len, pd)
                new_mod_date = str(now.date())
                pub_or_mod = 'pub'
                title_change_id.append(this_id)
                print('title change: ' + file_name)
        else:
            pub_or_mod = 'mod'
            new_mod_date = pk_dic[this_id]['mod_date']
        if 'T' in pub_date:
            pub_date = pub_date.replace('T', ' ')
        if type(str_len) == int:
            if pd['project_dir'] == 'konkatsu' or pd['project_dir'] == 'online_marriage':
                new_data = {'file_path': file_name, 'title': title, 'pub_date': pub_date, 'mod_date': new_mod_date,
                            'category': category, 'description': description, 'str_len': str_len,
                            'layout_flag': layout_flag, 'shift_flag': ss_flag, 'edit_flag': edit_flag,
                            'ad_flag': ad_flag}
            else:
                new_data = {'file_path': file_name, 'title': title, 'pub_date': pub_date, 'mod_date': new_mod_date,
                            'category': category, 'description': description, 'str_len': str_len,
                            'layout_flag': layout_flag, 'shift_flag': ss_flag, 'edit_flag': edit_flag}
        else:
            print('エラー発生 : ' + str_len)
            raise Exception('md置換ミスがあります')
        if '_test' not in file_name and '_copy' not in file_name:
            pk_dic = add_pickle_dec(pk_dic, new_data, pd, this_id)
        if not os.path.exists(pd['project_dir'] + '/html_files/' + pd['main_dir'] + '/' + directory):
            os.mkdir(pd['project_dir'] + '/html_files/' + pd['main_dir'] + '/' + directory)
        with open(pd['project_dir'] + '/html_files/' + pd['main_dir'] + file_name, 'w', encoding='utf-8') as g:
            g.write(new_str)
            upload_list.append(pd['project_dir'] + '/html_files/' + pd['main_dir'] + file_name)

        add_modify_log(file_name, now.date(), category, title, pub_or_mod, pd)
        # print(plain_txt)
        with open(md_file_path, 'w', encoding='utf-8') as j:
            j.write(plain_txt)
    return upload_list, pk_dic, title_change_id


def insert_ds_link(md_str, pd):
    # pd = joshideai.main_info.info_dict
    used_name = []
    # with open('joshideai/md_files/make_love/sex_30s.md', 'r', encoding='utf-8') as f:
    #     md_str = f.read()
    if 'aff_dir' in pd:
        if pd['aff_dir']['dir'] + '/' not in md_str:
            main_str = re.sub(r'^[\s\S]+?\n## ', '', md_str)
            str_list = main_str.split('\n')
            for key in pd['sc_url']:
                if key not in used_name:
                    for row in str_list:
                        if not row.startswith('#') and not row.startswith('- '):
                            if key in row:
                                if '](' not in row:
                                    i_url = '[{}](../../{}html_files/{}{})'.format(key,
                                                                                   '../' * pd['main_dir'].count('/'),
                                                                                   pd['main_dir'], pd['sc_url'][key])
                                    new_row = row.replace(key, i_url)
                                    md_str = md_str.replace(row, new_row)
                                    print('insert {} link str'.format(key))
                                    used_name.append(key)
                                    break
    return md_str


def img_filter(new_str, pd):
    if pd['project_dir'] == 'reibun':
        new_str = reibun.main_info.reibun_img_filter(new_str)
    return new_str


def insert_additional_str(new_str, pd):
    if pd['project_dir'] == 'reibun':
        new_str = reibun.main_info.reibun_insert_additional_str(new_str)
    return new_str


def change_category_class(new_str, category, pd):
    if pd['project_dir'] == 'reibun':
        new_str = reibun.main_info.reibun_change_category_class(new_str, category)
    return new_str


def icon_filter(md_txt, pd):
    if pd['project_dir'] == 'reibun':
        md_txt = reibun.main_info.reibun_icon_filter(md_txt)
    elif pd['project_dir'] == 'joshideai':
        md_txt = main_info.joshideai_icon_filter(md_txt)
    elif pd['project_dir'] == 'rei_site':
        md_txt = rei_site.main_info.rei_site_icon_filter(md_txt)
    elif pd['project_dir'] == 'konkatsu':
        md_txt = konkatsu.main_info.konkatsu_icon_filter(md_txt)
    else:
        md_txt = reibun.main_info.reibun_icon_filter(md_txt)
    return md_txt


def insert_site_banner(md_txt, pd):
    if pd['project_dir'] == 'reibun':
        md_txt = reibun.main_info.reibun_insert_site_banner(md_txt)
    return md_txt


def additional_replace_in_md(md_txt, pd):
    if pd['project_dir'] == 'reibun':
        md_txt = reibun.main_info.reibun_additional_replace_in_md(md_txt)
    return md_txt


def breadcrumb_maker(directory, file_name, pd):
    result = ''
    if 'index.html' in file_name or directory not in pd['category_data']:
        return result
    else:
        result += '<div itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem" class="b2">' \
                  '<a href="../' + directory + '/" itemprop="item"><span itemprop="name">' + \
                  pd['directory_name'][directory] + '</span></a><meta itemprop="position" content="2" /> &gt;&gt;</div>'
        return result


def json_img_data_insert(long_str, pd):
    img_path = pd['eyec_img']['img_path']
    height = pd['eyec_img']['height']
    width = pd['eyec_img']['width']
    if '<div class="alt_img_t">' in long_str:
        img_l = re.findall(r'<div class="alt_img_t"><img src="\.\./images/(.+?)" alt="', long_str)
        if img_l:
            img_path = img_l[0]
            height = '470'
            width = '760'
    i_str = long_str.replace('<!--jd-img-path-->', img_path)
    i_str = i_str.replace('"<!--jd-height-->"', height)
    i_str = i_str.replace('"<!--jd-width-->"', width)
    return i_str


def logical_box_filter(long_str):
    lg_box_str_l = re.findall(r'<div class="logi_box_e.+?>.+?</div>', long_str)
    if lg_box_str_l:
        for lg_box_str in lg_box_str_l:
            box_str = re.findall(r'>(.*?)<', lg_box_str)[0]
            if '*' in box_str:
                box_str_r = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', box_str)
                box_str_r = re.sub(r'\*(.+?)\*', r'<em>\1</em>', box_str_r)
                long_str = long_str.replace(box_str, box_str_r)
    return long_str


def add_modify_log(mod_file_path, now, category, title, pub_or_mod, pd):
    # mod_log = [[mod_file_path, str(now), category, title, pub_or_mod]]
    if os.path.exists(pd['project_dir'] + '/pickle_pot/modify_log.pkl'):
        mod_log = make_article_list.read_pickle_pot('modify_log', pd)
        today_mod = [x[0] for x in mod_log if x[1] == str(now)]
        if mod_file_path not in today_mod:
            mod_log.append([mod_file_path, str(now), category, title, pub_or_mod])
        else:
            for data in mod_log:
                if data[0] == mod_file_path and data[1] == str(now):
                    mod_log.remove(data)
                    mod_log.append([mod_file_path, str(now), category, title, pub_or_mod])
    else:
        mod_log = [[mod_file_path, str(now), category, title, pub_or_mod]]
    make_article_list.save_data_to_pickle(mod_log, 'modify_log', pd)


def img_str_filter(long_str, file_name, md_str, pd):
    add_list = []
    insert_img_l = re.findall(r'<p><img.+?></p>', long_str)
    if insert_img_l:
        for img_str in insert_img_l:
            print(img_str)
            img_data_l = re.findall(r'alt="(.*?)" src="(.+?)"', img_str)
            if not img_data_l:
                img_data_l = re.findall(r'src="(.+?)".*?alt="(.+?)"', img_str)
                img_data_l = [[x[1], x[0]] for x in img_data_l]
            if not img_data_l:
                img_data_l = re.findall(r'src="(.+?)"', img_str)
                img_data_l = [['', y] for y in img_data_l]
            print(img_data_l)
            if 'insert_image/' in img_data_l[0][1]:
                img_url = img_data_l[0][1]
                new_img_path, add_img = resize_and_rename_image(img_url, file_name, pd)
                new_img_path = '../' + re.sub(r'^.*/images/', 'images/', new_img_path)
                new_str = '<div class="alt_img_t"><img src="{}" alt="{}" width="760" height="470" /></div>' \
                    .format(new_img_path, img_data_l[0][0])
                long_str = long_str.replace(img_str, new_str)
                md_str = md_str.replace(img_url, new_img_path)
                add_list.extend(add_img)
            else:
                img_url = img_data_l[0][1]
                new_str = '<div class="alt_img_t"><img src="{}" alt="{}" width="760" height="470" /></div>' \
                    .format(img_url, img_data_l[0][0])
                long_str = long_str.replace(img_str, new_str)
    return long_str, add_list, md_str


def resize_and_rename_image(img_path, file_path, pd):
    file_name = re.sub(r'^.*/(.+?).html', r'\1', file_path)
    img_dir = '{}/html_files/{}images/{}'.format(pd['project_dir'], pd['main_dir'], pd['ar_img_dir'])
    current_images = os.listdir(img_dir)
    add_img = []
    if file_name + '_1_gr.jpg' in current_images:
        i = 2
        new_name = file_name + '_' + str(i) + '_gr.jpg'
        while new_name in current_images:
            i += 1
            new_name = file_name + '_' + str(i) + '_gr.jpg'
        image_path = re.sub(r'^.*?insert_image/', pd['project_dir'] + '/insert_image/', img_path)
        img = Image.open(image_path)
        img_gr = img.resize((760, 470))
        img_gr.save(img_dir + '/' + new_name)
        add_img.append(img_dir + '/' + new_name)
        if pd['amp_flag']:
            img_gr.save('{}/html_files/amp/images/{}/'.format(pd['project_dir'], pd['ar_img_dir']) + new_name)
            add_img.append('{}/html_files/amp/images/{}/'.format(pd['project_dir'], pd['ar_img_dir']) + new_name)
        img_gr.save(img_dir.replace('/html_files/', '/md_files/') + '/' + new_name)
        img.save(pd['project_dir'] + '/image_stock/' + file_name + '_' + str(i) + '.jpg')
        os.remove(image_path)
    else:
        # print(img_path)
        add_img = make_thumbnail(file_name, pd['project_dir'] + '/' + img_path.replace('../', ''), img_dir, pd)
        new_name = file_name + '_1_gr.jpg'
    return img_dir + '/' + new_name, add_img


def make_thumbnail(file_name, image_path, img_dir, pd):
    amp_dir = img_dir.replace('/pc/', '/amp/')
    md_dir = img_dir.replace('/html_files/', '/md_files/')
    im = Image.open(image_path)
    w, h = im.size
    cut_width = (w - h) / 2
    im_crop = im.crop((cut_width, 0, cut_width + h, h))
    im_resize = im_crop.resize((200, 200))
    im_resize.save(img_dir + '/' + file_name + '_thumb.jpg')
    if pd['amp_flag']:
        im_resize.save(amp_dir + '/' + file_name + '_thumb.jpg')
    im_resize.save(md_dir + '/' + file_name + '_thumb.jpg')
    if h >= w // 1.618:
        gr_h = w // 1.618
        h_a = (h - gr_h) // 2
        im_gr = im.crop((0, h_a, w, gr_h + h_a))
    else:
        gr_w = h + 1.618
        w_a = (w - gr_w) // 2
        im_gr = im.crop((w_a, 0, gr_w + w_a, h))
    im_gr_r = im_gr.resize((760, 470))
    im_gr_r.save(img_dir + '/' + file_name + '_1_gr.jpg')
    if pd['amp_flag']:
        im_gr_r.save(amp_dir + '/' + file_name + '_1_gr.jpg')
    im_gr_r.save(md_dir + '/' + file_name + '_1_gr.jpg')
    im_thumb = im_crop.resize((64, 64))
    im_thumb.save(img_dir + '/' + file_name + '_thumb_s.jpg')
    if pd['amp_flag']:
        im_thumb.save(amp_dir + '/' + file_name + '_thumb_s.jpg')
    im_thumb.save(md_dir + '/' + file_name + '_thumb_s.jpg')
    im.save(pd['project_dir'] + '/image_stock/' + file_name + '_1.jpg')
    os.remove(image_path)
    add_img = [img_dir + '/' + file_name + '_thumb.jpg', img_dir + '/' + file_name + '_1_gr.jpg',
               img_dir + '/' + file_name + '_thumb_s.jpg']
    if pd['amp_flag']:
        add_img.extend([amp_dir + '/' + file_name + '_thumb.jpg', amp_dir + '/' + file_name + '_1_gr.jpg',
                        amp_dir + '/' + file_name + '_thumb_s.jpg'])
    return add_img


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
            f_str = '<div class="sample"><div class="wmail"><p>' + f_mail.replace('\n', '<br />') + '</p></div></div>'
            long_str = long_str.replace('%w%' + f_mail + '\n\n', f_str)
    long_str = long_str.replace('%arr' + '\n\n',
                                '<div class="arr"><img width="17" height="17" src="../images/common/arr.png" alt="↓"></div>')
    cm_mail_l = re.findall(r'%cm%([\s\S]+?)\n\n', long_str)
    if cm_mail_l:
        for cm_mail in cm_mail_l:
            cm_str = '<div class="cm"><p>' + cm_mail.replace('\n', '<br />') + '</p></div></div>'
            long_str = long_str.replace('%cm%' + cm_mail + '\n\n', cm_str)
    if '%%%' in long_str:
        long_str = re.sub(r'%%%([\s\S]+?)%%%', r'<div class="sample">\1</div>', long_str)
    else:
        long_str = long_str.replace('</div></div><div class="arr">', '</div><div class="arr">')
        long_str = long_str.replace('alt="↓"></div><div class="sample"><div class="mail">',
                                    'alt="↓"></div><div class="mail">')
        long_str = long_str.replace('alt="↓"></div><div class="sample"><div class="wmail">',
                                    'alt="↓"></div><div class="wmail">')
        long_str = long_str.replace('</div></div><div class="cm">', '</div><div class="cm">')
        long_str = re.sub(r'<!--km-el-->[\s]*?<div class="sample">', '', long_str)
    return long_str


def strong_insert_filter(long_str):
    if '*' in long_str:
        box_str_r = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', long_str)
        box_str_r = re.sub(r'\*(.+?)\*', r'<em>\1</em>', box_str_r)
        long_str = long_str.replace(long_str, box_str_r)
    return long_str


def add_pickle_dec(pk_dic, new_data, pd, new_data_id):
    path_list = [pk_dic[x]['file_path'] for x in pk_dic]
    if new_data_id or new_data_id == 0:
        pk_dic[new_data_id] = new_data
    else:
        if new_data['file_path'] not in path_list:
            pk_dic[len(pk_dic)] = new_data
        else:
            for i in range(len(path_list)):
                if path_list[i] == new_data['file_path']:
                    pk_dic[i] = new_data
    make_article_list.save_data_to_pickle(pk_dic, 'main_data', pd)
    # print(pk_dic)
    make_article_list.save_text_file(pk_dic, pd)
    return pk_dic


def css_optimize(html_path, css_path):
    with open(css_path, 'r', encoding='utf-8') as f:
        css_str = f.read()
    with open(html_path, 'r', encoding='utf-8') as g:
        html_str = g.read()
    return css_str_optimize(html_str, css_str)


def css_str_optimize(html_str, css_str):
    css_str = css_str.replace('\n', '')
    css_str = css_str.replace('@charset "UTF-8";', '')
    css_str = re.sub(r';[\s]*', ';', css_str)
    css_str = re.sub(r'{[\s]*', '{', css_str)
    css_str = re.sub(r',[\s]*', ',', css_str)
    css_str = re.sub(r':[\s]*', ':', css_str)
    css_str = re.sub(r' {', '{', css_str)
    css_str = re.sub(r'/\*.+?\*/', '', css_str)
    css_str = re.sub(r'@media.*$', '', css_str)
    css_list = css_str.split('}')
    css_list = [c + '}' for c in css_list[:-1]]
    css_sep_list = []
    for line in css_list:
        selector_str_l = re.findall(r'(.+?){', line)
        if ',' in selector_str_l[0]:
            selector_c_list = selector_str_l[0].split(',')
        else:
            selector_c_list = [selector_str_l[0]]
        css_sep_list.append([selector_c_list, re.findall(r'{([\s\S]*)}', line)[0]])
    # print(css_sep_list)

    z_l = [z.split() for z in re.findall(r'class="(.+?)"', html_str)]
    class_list = []
    for z_e in z_l:
        class_list.extend(['.' + q for q in z_e])

    id_list = ['#' + z for z in re.findall(r'id="(.+?)"', html_str)]
    selector_list = class_list + id_list
    selector_list = set(selector_list)
    selector_list = list(selector_list)
    selector_list.sort()
    # print(selector_list)

    tag_list = re.findall('<(.+?)[ |>]', html_str)
    tag_list = [b for b in tag_list if '/' not in b and '!' not in b]
    tag_list = set(tag_list)
    tag_list = list(tag_list)
    new_list = []
    for x in css_sep_list:
        css_selector = []
        for y in x[0]:
            # print(y)
            if '.' in y or '#' in y:
                for z in selector_list:
                    if z in y:
                        css_selector.append(y)
                        break
            else:
                for i in tag_list:
                    if i in y:
                        css_selector.append(y)
                        break
        if css_selector:
            new_list.append([css_selector, x[1]])
    # print(len(new_list))
    # print(new_list)
    str_list = [','.join(a[0]) + '{' + a[1] + '}' for a in new_list]
    new_str = ''.join(str_list)
    # print(new_str)
    return new_str


def modify_relation_list(long_str, title_change_id, pk_dic):
    r_str = re.findall(r'<div class="kanren">(.+?)</div>', long_str)
    if r_str:
        for c_id in title_change_id:
            if pk_dic[c_id]['file_path'] in r_str:
                long_str = re.sub(pk_dic[c_id]['file_path'] + r'">(.+?)</a>',
                                  pk_dic[c_id]['file_path'] + r'">' + pk_dic[c_id]['title'] + '</a>', long_str)
    return long_str


def count_main_str_length(long_str, file_path):
    main_str = re.findall(r'<article itemprop="articleBody mainEntityOfPage">(.+?)</article>', long_str)
    if main_str:
        main_str = re.sub(r'<div class="kanren">.+?</div>', '', main_str[0])
        main_str = re.sub(r'<.+?>', '', main_str)
        # print(main_str)
        str_len = len(main_str)
        # print(str_len)
        per_str = re.findall(r'\D%', main_str)
        if '# ' in main_str or '}(' in main_str or '<' in main_str or '>' in main_str or '](' in main_str:
            print('there is md ! ' + file_path)
        elif per_str:
            print('there is % ! ' + file_path)
            print(per_str)
        return str_len
    else:
        return 'no article !'


def insert_main_length(pd):
    with open(pd['project_dir'] + '/pickle_pot/main_data.pkl', 'rb') as p:
        pk_dic = pickle.load(p)
    for i in pk_dic:
        if 'site/index' not in pk_dic[i]['file_path']:
            file_path = os.path.join(pd['project_dir'] + '/html_files/' + pd['main_dir'], pk_dic[i]['file_path'])
            with open(file_path, 'r', encoding='utf-8') as f:
                long_str = f.read()
                long_str = file_upload.tab_and_line_feed_remove_from_str(long_str)
                str_len = count_main_str_length(long_str, pk_dic[i]['file_path'])
                if type(str_len) == int:
                    pk_dic[i]['str_len'] = str_len
                elif str_len == 'there is md !':
                    print('md : ' + pk_dic[i]['file_path'])
                else:
                    print('error : ' + pk_dic[i]['file_path'])
                    print(str_len)
                flag = check_page_layout(long_str)
                if flag != pk_dic[i]['layout_flag']:
                    print('flag_change : ' + file_path)
                    pk_dic[i]['layout_flag'] = flag
    # print(pk_dic)
    # make_article_list.save_data_to_pickle(pk_dic, 'main_data')


def check_page_layout(long_str):
    new_img = re.findall(r'class="alt_img_t"', long_str)
    rm_str = re.findall(r'class="rm_', long_str)
    rw_str = re.findall(r'class="rw_', long_str)
    if new_img and (rm_str or rw_str):
        flag = True
    else:
        flag = False
    return flag


def check_site_shift(long_str):
    if '%ss' in long_str:
        flag = True
    else:
        flag = False
    return flag


def update_title_log(file_path, title_str, now, str_len, pd):
    if os.path.exists(pd['project_dir'] + '/pickle_pot/title_log.pkl'):
        pk_dic = make_article_list.read_pickle_pot('title_log', pd)
    else:
        pk_dic = {}
    if file_path in pk_dic:
        pk_dic[file_path][now] = [title_str, str_len]
    else:
        pk_dic[file_path] = {now: [title_str, str_len]}
    # print(pk_dic)
    make_article_list.save_data_to_pickle(pk_dic, 'title_log', pd)


def make_1st_title_log(pd):
    pk_dic = make_article_list.read_pickle_pot('main_data', pd)
    new_dec = {'index.html': {'2020/11/10': ['title', 2000]}}
    for p_id in pk_dic:
        new_dec[pk_dic[p_id][0]] = {'2020/11/10': [pk_dic[p_id][1], pk_dic[p_id][6]]}
    # print(new_dec)
    make_article_list.save_data_to_pickle(new_dec, 'title_log', pd)


def directory_and_category_select(file_path, pd):
    # print(file_path)
    directory_l = re.findall(r'^(.+?)/.+$', file_path)
    if directory_l and '/index.html' not in file_path:
        directory = directory_l[0]
        file_name = re.sub(r'^.*/', '', file_path)
        # print('directory: ' + directory)
        if pd['project_dir'] == 'reibun':
            category = reibun.main_info.reibun_search_category(directory, file_name)
        else:
            category = directory
    else:
        directory = 'top'
        category = 'top'
    # print('category : ' + category)
    return directory, category


def all_html_insert():
    all_html_list = glob.glob('reibun/html_files/**/**.html', recursive=True)
    for file_path in all_html_list:
        with open(file_path, 'r', encoding='utf-8') as f:
            long_str = f.read()
            if 'https://www.demr.jp/pc/template/pc_tmp.html' in long_str:
                long_str = long_str.replace('https://www.demr.jp/pc/template/pc_tmp.html',
                                            'https://www.demr.jp/' + file_path.replace('reibun/html_files/', ''))
                # print(long_str)
                with open(file_path, 'w', encoding='utf-8') as g:
                    g.write(long_str)

# if __name__ == '__main__':
#     insert_ds_link('', '')

# pd_dict = reibun.main_info.info_dict
#     main(1, pd_dict)
# site_shift_flag ( 0: normal, 1:no jmail )
# reibun_upload.files_upload(['reibun/index.html'])
# print(make_article_list.read_pickle_pot('modify_log'))
# print(make_article_list.read_pickle_pot('main_data', pd_dict))

# print(make_article_list.read_pickle_pot('title_log'))

# insert_main_length()
# import_from_markdown(['md_files/pc/qa/q3_test.md'])
# t_l = {0: ['']}
# print(make_all_side_bar(t_l))
# insert_to_index_page(t_l)
# xml_site_map_maker(t_l)
# reibun_upload.tab_and_line_feed_remover('reibun/index.html')
# print(markdown.markdown('## h2\n[](あああああ)\n<!--あああああ-->'))
# print([x for x in test_l if x[1] == test_l[-1][1]])
# print(str(datetime.datetime.now())[:-7])
# print(css_optimize('reibun/index.html', 'reibun/pc/css/top1.css'))

# make_rss([])
# reibun_upload.files_upload(['reibun/atom.xml', 'reibun/rss10.xml', 'reibun/rss20.xml'])
# rpd = rei_site.main_info.info_dict
# make_html_dir(rpd)
# all_html_insert()
# first_make_html(rpd)
# insert_to_temp(rpd)
