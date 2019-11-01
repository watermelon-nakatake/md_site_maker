# -*- coding: utf-8 -*-
from ftplib import FTP
import os
import time
import re
import datetime
import amp_file_maker
import common_tool
import random


def ftp_upload(up_file_list):
    """
    FTPでファイルをアップロード,ベースはドメイン直下
    :param up_file_list: アップロードするファイルのリスト
    :return: none
    """
    with FTP('blackrhino1.sakura.ne.jp', passwd='k2u5n47ku6') as ftp:
        ftp.login(user='blackrhino1', passwd='k2u5n47ku6')
        ftp.cwd('www')
        for up_file_name in up_file_list:
            with open(str(up_file_name), 'rb') as fp:
                ftp.storbinary("STOR " + up_file_name, fp)
            print('upload: ' + str(up_file_name))
        ftp.close()
    return


def insert_mod_timestamp(main_str):
    today = datetime.date.today()
    main_str = re.sub(r'<time itemprop="dateModified" datetime="(.*?)</time>',
                      '<time itemprop="dateModified" datetime="' + str(today) + '">' + str(today.year) + '年'
                      + str(today.month) + '月' + str(today.day) + '日</time>', main_str)
    return main_str


# ampファイルを作成
def make_amp_total():
    dir_list = ['caption', 'majime', 'qa', 'site', 'policy']
    for directory in dir_list:
        current_path = 'reibun/pc/' + directory
        file_list = os.listdir(current_path)
        now = time.time()
        for file in file_list:
            file_path = current_path + '/' + file
            mod_time = os.path.getmtime(file_path)
            if now - mod_time < 86400:
                amp_file_maker.amp_maker(file_path)
                print('make amp: ' + file_path)


def modified_file_upload():
    upper_dir = ['pc', 'amp']
    dir_list = ['caption', 'majime', 'qa', 'site', 'policy', 'images']
    modified_file = []
    for upper in upper_dir:
        for directory in dir_list:
            current_path = 'reibun/' + upper + '/' + directory
            file_list = os.listdir(current_path)
            now = time.time()
            for file in file_list:
                file_path = current_path + '/' + file
                mod_time = os.path.getmtime(file_path)
                print(file_path)
                print(mod_time)
                print(now)
                if now - mod_time < 86400:
                    modified_file.append(file_path)
    print(modified_file)
    ftp_upload(modified_file)
    # amp_file = [x.replace('/pc/', '/amp/') for x in modified_file]
    # ftp_upload(amp_file)
    ftp_upload(['reibun/index.html'])


def modify_stamp_insert():
    dir_list = ['caption', 'majime', 'qa', 'site', 'policy']
    mod_date_list = {}
    mod_list = []
    for directory in dir_list:
        current_path = 'reibun/pc/' + directory
        file_list = os.listdir(current_path)
        for file in file_list:
            file_path = current_path + '/' + file
            mod_time = os.path.getmtime(file_path)
            mod_date = datetime.date.fromtimestamp(mod_time)
            print(mod_date)
            mod_date_list[directory + '/' + file] = str(mod_date)
            with open(file_path, "r", encoding='utf-8') as f:
                main_str = f.read()
                print(file)
                # print(main_str)
                time_stamp = re.findall('<time itemprop="dateModified" datetime="(.*?)">', main_str)
                print(time_stamp)
                if time_stamp:
                    time_stamp_str = str(time_stamp[0])
                    if time_stamp_str != str(mod_date):
                        print('not same')
                        print(mod_date.day)
                        mod_list.append(file_path)
                        main_str = re.sub(r'<time itemprop="dateModified" datetime="(.*?)</time>',
                                          '<time itemprop="dateModified" datetime="' + str(mod_date)
                                          + '">' + str(mod_date.year) + '年' + str(mod_date.month) + '月'
                                          + str(mod_date.day) + '日</time>', main_str)
                        with open(file_path, "w") as h:
                            h.write(main_str)
    if mod_date_list:
        xml_sitemap_update(mod_date_list)
    return mod_list


def xml_sitemap_update(mod_date_list):
    with open('reibun/p_sitemap.xml', 'r', encoding='utf-8') as g:
        sitemap_str = g.read()
        for page in mod_date_list:
            sitemap_str = re.sub(
                '<loc>https://www.demr.jp/pc/' + page + '</loc><lastmod>(.+?)</lastmod>',
                '<loc>https://www.demr.jp/pc/' + page + '</loc><lastmod>'
                + str(mod_date_list[page]) + '</lastmod>', sitemap_str)
    with open('reibun/p_sitemap.xml', "w") as f:
        f.write(sitemap_str)


def jap_date_insert():
    dir_list = ['caption', 'majime', 'qa', 'site', 'policy']
    for directory in dir_list:
        current_path = 'reibun/pc/' + directory
        file_list = os.listdir(current_path)
        for file in file_list:
            file_path = current_path + '/' + file
            with open(file_path, "r", encoding='utf-8') as f:
                main_str = f.read()
                time_stamp = re.findall('<time itemprop="dateModified" datetime="(.*?)">', main_str)
                if time_stamp:
                    numbers = re.findall(r'(\d+?)-(\d+?)-(\d+?)$', time_stamp[0])
                    main_str = re.sub(r'<time itemprop="dateModified" datetime="(.*?)</time>',
                                      '<time itemprop="dateModified" datetime="' + str(time_stamp[0])
                                      + '">' + str(numbers[0][0]) + '年' + str(int(numbers[0][1])) + '月'
                                      + str(int(numbers[0][2])) + '日</time>', main_str)
            with open(file_path, "w") as h:
                h.write(main_str)


def tab_and_line_feed_remove_from_str(long_str):
    str_list = long_str.splitlines()
    result = ''
    for x in str_list:
        y = x.strip()
        result += y
    result = result.replace('spanclass', 'span class')
    result = result.replace('spanid', 'span id')
    result = result.replace('"alt=', '" alt=')
    result = result.replace('"itemtype', '" itemtype')
    result = result.replace('"datetime=', '" datetime=')
    result = result.replace('imgsrc', 'img src')
    result = result.replace('spanitemprop', 'span itemprop')
    result = result.replace('spanclass', 'span class')
    result = result.replace('ahref', 'a href')
    result = result.replace('timeitemprop', 'time itemprop')
    result = result.replace('description"content="', 'description" content="')
    result = result.replace('"width="', '" width="')
    result = result.replace('"media="', '" media="')
    return result


def tab_and_line_feed_remover(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        long_str = f.read()
        result = tab_and_line_feed_remove_from_str(long_str)
        # print(result)
    with open(file_path, 'w', encoding='utf-8') as w:
        w.write(result)


def html_list_maker(dir_list):
    result_list = []
    for directory in dir_list:
        file_list = os.listdir(directory)
        for file_name in file_list:
            result_list.append(directory + '/' + file_name)
    return result_list


def total_update():
    dir_list = ['reibun/pc/caption', 'reibun/pc/majime', 'reibun/pc/qa',
                'reibun/pc/site', 'reibun/pc/policy']
    for file in html_list_maker(dir_list):
        tab_and_line_feed_remover(file)
    mod_list = modify_stamp_insert()
    amp_file_maker.amp_maker(mod_list)
    modified_file_upload()
    ftp_upload(['reibun/p_sitemap.xml', 'reibun/index.html'])


def link_checker(url, target_html_list):
    result_list = []
    for file_path in target_html_list:
        with open(file_path, 'r', encoding='utf-8') as f:
            main_str = f.read()
            if url not in main_str:
                result_list.append(file_path)
    return result_list


def link_check(url):
    pc_dir_list = ['caption', 'majime', 'qa', 'site', 'policy']
    pc_directory = ['reibun/pc/' + x for x in pc_dir_list]
    html_list = html_list_maker(pc_directory)
    result = link_checker(url, html_list)
    print(str(len(result)) + '/' + str(len(html_list)))
    print(result)


def relational_article_insert(title, url, long_str):
    relational_list = re.findall(r'<div class="kanren">.+?</div>', long_str)
    if relational_list:
        if url not in relational_list[0]:
            ch_list = re.findall(r'<li>.+?</li>', relational_list[0])
            ch_list.append('<li><a href="' + url + '">' + title + '</a></li>')
            random.shuffle(ch_list)
            list_str = '<div class="kanren"><h2>関連記事</h2><ul>' + ''.join(ch_list) + '</ul></div>'
            long_str = long_str.replace(relational_list[0], list_str)
            long_str = insert_mod_timestamp(long_str)
    return long_str


def all_file_relational_art_insert(title, url):
    pc_dir_list = ['majime', 'qa', 'site']  # 'caption',
    mod_list = []
    for directory in pc_dir_list:
        file_list = os.listdir('reibun/pc/' + directory)
        for file_name in file_list:
            if '.html' in file_name:
                file_path = 'reibun/pc/' + directory + '/' + file_name
                with open(file_path, 'r', encoding='utf-8') as f:
                    main_str = f.read()
                    if 'class="kanren"' in main_str:
                        main_str = relational_article_insert(title, url, main_str)
                        main_str = insert_mod_timestamp(main_str)
                        main_str = path_directory_adjuster(main_str, file_path)
                        with open(file_path, 'w', encoding='utf-8') as g:
                            g.write(main_str)
                            mod_list.append(file_path)
    amp_file_maker.amp_maker(mod_list)
    ftp_upload(mod_list)
    ftp_upload([x.replace('/pc/', '/amp/') for x in mod_list])


def path_directory_adjuster(long_str, file_path):
    own_directory = re.findall(r'/pc/(.+?)/', file_path)[0]
    long_str = long_str.replace('../../pc/' + own_directory + '/', '')
    long_str = long_str.replace('../' + own_directory + '/', '')
    long_str = long_str.replace('href=""', 'href="../' + own_directory + '/"')
    return long_str


def all_file_rework():
    pc_dir_list = ['caption', 'majime', 'qa', 'site']
    mod_list = []
    for directory in pc_dir_list:
        file_list = os.listdir('reibun/pc/' + directory)
        for file_name in file_list:
            if '.html' in file_name:
                file_path = 'reibun/pc/' + directory + '/' + file_name
                with open(file_path, 'r', encoding='utf-8') as f:
                    main_str = f.read()
                    if 'href=""' in main_str:
                        main_str = main_str.replace('href=""', 'href="../' + directory + '/"')
                        with open(file_path, 'w', encoding='utf-8') as g:
                            g.write(main_str)
                            mod_list.append(file_path)
    amp_file_maker.amp_maker(mod_list)
    ftp_upload(mod_list)
    ftp_upload([x.replace('/pc/', '/amp/') for x in mod_list])


def twitter_card_insert(long_str, file_path):
    img = 'images/mailgirl250w1.jpg'
    title = '出会い系メール例文集'
    desc = '出会い系サイトで役立つメールの例文をご紹介しています。'
    title_l = re.findall(r'<title>(.+?)</title>', long_str)
    if title_l:
        title = title_l[0]
    desc_l = re.findall(r'<meta name="description" content="(.+?)">', long_str)
    if desc_l:
        desc = desc_l[0]
    if 'alt_img_t' in long_str:
        img_l = re.findall(r'<div class="alt_img_t"><img src="(.+?)" alt="', long_str)
        if img_l:
            img = img_l[0]
    elif 'pic25o' in long_str:
        img_l = re.findall(r'<div class="pic250"><img src="(.+?)" width="250"', long_str)
        if img_l:
            img = img_l[0]
            if '"' in img:
                print('pic250 is wrong order! : ' + file_path)
    url = file_path.replace('reibun/pc/', 'https://www.demr.jp/pc/')
    img = img.replace('../images/', '/images/')
    if 'twitter:card' not in long_str:
        card_str = '<meta name="twitter:card" content="summary" />' \
                   '<meta name="twitter:site" content="@goyan_demr" /><meta property="og:url" content="' \
                   + url + '" /><meta property="og:title" content="' + title \
                   + '" /><meta property="og:description" content="' + desc \
                   + '" /><meta property="og:image" content="https://www.demr.jp/pc' + img + '" />'
        long_str = long_str.replace('</head>', card_str + '</head>')
    return long_str


def total_twitter_card_insert():
    pc_dir_list = ['caption', 'majime', 'qa', 'site']
    update_list = []
    for directory in pc_dir_list:
        file_list = os.listdir('reibun/pc/' + directory)
        for file_name in file_list:
            if '.html' in file_name:
                file_path = 'reibun/pc/' + directory + '/' + file_name
                with open(file_path, 'r', encoding='utf-8') as f:
                    main_str = f.read()
                    main_str = twitter_card_insert(main_str, file_path)
                with open(file_path, 'w', encoding='utf-8') as g:
                    g.write(main_str)
                    update_list.append(file_path)
    ftp_upload(update_list)


def insert_index_list(path):
    tab_and_line_feed_remover(path)
    with open(path, 'r', encoding='utf-8') as f:
        new_str = f.read()
        new_str = new_str.replace('<h2>', '<!--p-index--><h2>', 1)
        new_str = common_tool.index_maker(new_str)
        new_str = common_tool.section_insert(new_str)
        print(new_str)
        with open(path, 'w', encoding='utf-8') as g:
            g.write(new_str)


# todo: サイドバーのリンクをpickle使って統一＆自動で作成(タイトル読み取り、整列、自動追加）
# todo: 新規記事追加の省力化　ever note等からのインポートファイルで作成
# todo: ABテストのscript作成

if __name__ == '__main__':
    # total_update()
    # tab_and_line_feed_remover('reibun/pc/majime/mail-applicaton_test.html')
    # link_check('app/')
    # modify_stamp_insert()
    # make_amp_total()
    # modified_file_upload()
    # print(os.listdir('reibun/pc'))
    # jap_date_insert()
    ftp_upload(['reibun/index.html'])
    """ftp_upload(['reibun/p_sitemap.xml', 'reibun/pc/policy/profile.html', 'reibun/pc/policy/index.html',
                'reibun/pc/policy/sitemap.html', 'reibun/pc/policy/log.html',
                'reibun/pc/caption/meaningofwarikiri.html', 'reibun/pc/caption/warikiricheck.html',
                'reibun/pc/caption/index.html', 'reibun/pc/caption/freesite.html', 'reibun/pc/caption/fraud.html',
                'reibun/pc/caption/dealerprofile.html', 'reibun/pc/caption/storyofexperience.html',
                'reibun/pc/caption/fwari.html', 'reibun/pc/caption/jkandjc.html',
                'reibun/pc/caption/tsutsumotase.html', 'reibun/pc/caption/sakura.html',
                'reibun/pc/caption/rapaciousdealer.html', 'reibun/pc/majime/m1remarriage.html',
                'reibun/pc/majime/kakikata_p.html', 'reibun/pc/majime/m2conversation-technic.html',
                'reibun/pc/majime/m2topic.html', 'reibun/pc/majime/m0bigboobs.html', 'reibun/pc/majime/m2lineid.html',
                'reibun/pc/majime/m1netnan-sex.html', 'reibun/pc/majime/m2htalk.html', 'reibun/pc/majime/m0aijin.html',
                'reibun/pc/majime/m2_0_1.html', 'reibun/pc/majime/m1wakuwakumail.html',
                'reibun/pc/majime/m4manual.html', 'reibun/pc/majime/m1_8.html', 'reibun/pc/majime/m2_11.html',
                'reibun/pc/majime/m4virgin.html', 'reibun/pc/majime/m1_9.html', 'reibun/pc/majime/index.html',
                'reibun/pc/majime/m0bbs.html', 'reibun/pc/majime/m0sexfriend.html', 'reibun/pc/majime/m2_2_1.html',
                'reibun/pc/majime/mp_easytocapture.html', 'reibun/pc/majime/m2.html',
                'reibun/pc/majime/mp_sexfriendprofile.html', 'reibun/pc/majime/kakikata_d.html',
                'reibun/pc/majime/mp_enjokousai.html', 'reibun/pc/majime/majime.html',
                'reibun/pc/majime/m1goldenweek.html', 'reibun/pc/majime/m2marriedwomenu.html',
                'reibun/pc/majime/m4application.html', 'reibun/pc/majime/m0marriedman.html',
                'reibun/pc/majime/mail-applicaton_test_c.html', 'reibun/pc/majime/m4honban.html',
                'reibun/pc/majime/m1-adult.html', 'reibun/pc/majime/m3_3.html', 'reibun/pc/majime/m2firstreply.html',
                'reibun/pc/majime/m1middle-aged.html', 'reibun/pc/majime/m0_6.html',
                'reibun/pc/majime/m4personal-data.html', 'reibun/pc/majime/m0sexfriendmw.html',
                'reibun/pc/majime/m0ym.html', 'reibun/pc/majime/m4hitoduma.html',
                'reibun/pc/majime/m1forties-and-fifties.html', 'reibun/pc/majime/m3_2.html',
                'reibun/pc/majime/m2-sympathy.html', 'reibun/pc/majime/m2_1_2.html',
                'reibun/pc/majime/m1marriagehunting.html', 'reibun/pc/majime/mail-applicaton_test.html',
                'reibun/pc/majime/mp_sexy-profile.html', 'reibun/pc/majime/m1sexfriendbun.html',
                'reibun/pc/majime/m0_10.html', 'reibun/pc/majime/m1sexfriendmail.html',
                'reibun/pc/majime/m2conversation.html', 'reibun/pc/majime/m2_1_1.html', 'reibun/pc/majime/m0_8.html',
                'reibun/pc/majime/m0summer.html', 'reibun/pc/majime/m3early.html', 'reibun/pc/majime/m0sexless.html',
                'reibun/pc/majime/m2_9.html', 'reibun/pc/majime/m3first-meeting-sex.html',
                'reibun/pc/majime/m0_4.html', 'reibun/pc/majime/kakikata_t.html', 'reibun/pc/majime/m1-beginner.html',
                'reibun/pc/majime/m2_4.html', 'reibun/pc/majime/m1fixed-phrase.html',
                'reibun/pc/majime/m0warikiri.html', 'reibun/pc/majime/m0mature-lady.html',
                'reibun/pc/majime/m1_1.html', 'reibun/pc/majime/m4netnan-technique.html',
                'reibun/pc/majime/m0virgin.html', 'reibun/pc/majime/m0_12.html', 'reibun/pc/majime/m4rookie.html',
                'reibun/pc/majime/mp_2_1.html', 'reibun/pc/majime/t0_01bbs.html',
                'reibun/pc/majime/m1deaiapplication.html', 'reibun/pc/majime/m2adult-relations.html',
                'reibun/pc/majime/m1_6.html', 'reibun/pc/majime/mp_bad-personality.html',
                'reibun/pc/majime/m0papakatsu_no_sex.html', 'reibun/pc/majime/mail-applicaton.html',
                'reibun/pc/majime/m2papakatsu.html', 'reibun/pc/majime/mp_profile.html',
                'reibun/pc/majime/kakikata_t_test.html', 'reibun/pc/majime/mp_self-introduction.html',
                'reibun/pc/majime/m0happymail.html', 'reibun/pc/majime/m1marriedwoman.html',
                'reibun/pc/majime/m0adultery.html', 'reibun/pc/majime/m1girlfriend.html',
                'reibun/pc/majime/m4yarimokuw.html', 'reibun/pc/majime/m4yarimoku.html', 'reibun/pc/majime/date.html',
                'reibun/pc/majime/m1january.html', 'reibun/pc/majime/m4sexfriend-netonan.html',
                'reibun/pc/majime/m4enderiuraderi.html', 'reibun/pc/majime/m2ngword.html',
                'reibun/pc/majime/kakikata_f.html', 'reibun/pc/majime/m2sexfriend.html', 'reibun/pc/majime/m0_3.html',
                'reibun/pc/majime/m1sexfriendpurpose.html', 'reibun/pc/majime/m1papakatsu.html',
                'reibun/pc/qa/q8.html', 'reibun/pc/qa/q4.html', 'reibun/pc/qa/index.html', 'reibun/pc/qa/q5.html',
                'reibun/pc/qa/q2.html', 'reibun/pc/qa/q3.html', 'reibun/pc/qa/q1.html', 'reibun/pc/qa/q6.html',
                'reibun/pc/qa/q7.html', 'reibun/pc/site/tel.html', 'reibun/pc/site/index.html',
                'reibun/pc/site/jewellive.html', 'reibun/pc/site/news_pcmax.html',
                'reibun/pc/site/registration_pcmax.html', 'reibun/pc/site/point.html',
                'reibun/pc/site/mixisexfriend.html', 'reibun/pc/site/wakuwakutel.html',
                'reibun/pc/site/wakuwakumailadult.html', 'reibun/pc/site/kakaotalksexfriend.html',
                'reibun/pc/site/registration_pcmax_f.html', 'reibun/pc/site/nenrei.html',
                'reibun/pc/site/pcmaxsexfriendlong.html', 'reibun/pc/site/194964_s.html',
                'reibun/pc/site/news_mintj.html', 'reibun/pc/site/yyc_c.html', 'reibun/pc/site/happymailpoint.html',
                'reibun/pc/site/happymail_a.html', 'reibun/pc/site/jmail.html', 'reibun/index.html',
                'reibun/pc/css/base7.css', 'reibun/pc/css/pc7.css', 'reibun/pc/css/phone7.css'])"""
    # all_file_relational_art_insert('出会い系メール自動作成アプリのご紹介', '../majime/mail-applicaton.html')
    # all_file_rework()
    # total_twitter_card_insert()
    # insert_index_list('reibun/pc/majime/mail-applicaton.html')
