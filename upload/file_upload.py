# -*- coding: utf-8 -*-
from ftplib import FTP
import os
import time
import re
import datetime

import howto.main_info
import mailsample.main_info
from add_article import amp_file_maker, common_tool
import random
import paramiko
import scp
import reibun.main_info
import online_marriage.main_info
import konkatsu.main_info
import rei_site.main_info
import sfd.main_info
import shoshin.main_info
import htaiken.main_info
import joshideai.main_info
import mailsample.main_info


def scp_upload(up_file_list, pd):
    upload_data = pd['upload_data']
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=upload_data['host_name'], port=22, username=upload_data['user_name'],
                    password=upload_data['password_str'], timeout=600)
        if 'mass_flag' in pd:
            # mkdir を実行する
            stdin, stdout, stderr = ssh.exec_command('mkdir www/{}'.format(pd['project_dir']))
            # 実行結果のstdoutとstderrを読み出す
            for o in stdout:
                print(o)
            for e in stderr:
                print(e)
            for cat_dir in [x for x in pd['category_data']]:
                stdin, stdout, stderr = ssh.exec_command('mkdir www/{}/{}'.format(pd['project_dir'], cat_dir))

                # 実行結果のstdoutとstderrを読み出す
                for o in stdout:
                    print(o)
                for e in stderr:
                    print(e)
        if pd['project_dir'] == 'sfd':
            local_dir = 'up_html'

        else:
            local_dir = 'html_files'
        # ファイルをアップロード
        with scp.SCPClient(ssh.get_transport(), socket_timeout=600) as scpc:
            error_files = []
            for up_file in up_file_list:
                if 'mass_flag' in pd:
                    print('upload: ' + up_file)
                    if '/' in up_file:
                        up_str = up_file.replace('mass_production/' + pd['project_dir'] + '/' + local_dir,
                                                 upload_data['upload_dir'])
                        up_dir = re.findall(r'^(.+)/', up_str)[0]
                    else:
                        up_dir = ''
                else:
                    print('upload: ' + up_file)
                    if '/' in up_file:
                        up_str = up_file.replace(pd['project_dir'] + '/' + local_dir, upload_data['upload_dir'])
                        up_dir = re.findall(r'^(.+)/', up_str)[0]
                    else:
                        up_dir = ''
                try:
                    scpc.put(up_file, 'www/' + up_dir)
                except Exception as e:
                    print(e)
                    error_files.append(up_file)
            if not error_files:
                print('Upload finished !')
            else:
                print('cause error !! upload has not finished')
            return error_files


def shoshin_scp_upload(up_file_list):
    pd = shoshin.main_info.info_dict
    upload_data = pd['upload_data']
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=upload_data['host_name'], port=22, username=upload_data['user_name'],
                    password=upload_data['password_str'])
        # ファイルをアップロード
        with scp.SCPClient(ssh.get_transport()) as scpc:
            error_files = []
            for up_file in up_file_list:
                if up_file in ['.htaccess'] or '/beginner/' in up_file or '/css/' in up_file or '/images/' in up_file \
                        or 'a_sitemap.xml' in up_file or '/means/' in up_file:
                    print('upload: ' + up_file)
                    if '/' in up_file:
                        up_str = up_file.replace(pd['project_dir'] + '/html_files', upload_data['upload_dir'])
                        up_dir = re.findall(r'^(.+)/', up_str)[0]
                    else:
                        up_dir = ''
                    try:
                        scpc.put(up_file, 'www/' + up_dir)
                    except BufferError as e:
                        print(e)
                        error_files.append(up_file)
            print('Upload finished !')
            return error_files


def auto_scp_upload(up_file_list):
    prj_dict = {'howto': howto.main_info.info_dict,
                'joshideai': joshideai.main_info.info_dict,
                'online_marriage': online_marriage.main_info.info_dict,
                'konkatsu': konkatsu.main_info.info_dict,
                'rei_site': rei_site.main_info.info_dict,
                'reibun': reibun.main_info.info_dict,
                'sfd': sfd.main_info.info_dict,
                'shoshin': shoshin.main_info.info_dict,
                'htaiken': htaiken.main_info.info_dict,
                'mailsample': mailsample.main_info.info_dict
                }
    use_dict = {x: [] for x in prj_dict}
    for pro in use_dict:
        for file_path in up_file_list:
            if file_path.startswith(pro):
                use_dict[pro].append(file_path)
    # print(use_dict)
    for dir_name in use_dict:
        if use_dict[dir_name]:
            scp_upload(use_dict[dir_name], prj_dict[dir_name])


def ftp_upload(up_file_list, pd):
    """
    FTPでファイルをアップロード,ベースはドメイン直下
    :param up_file_list: アップロードするファイルのリスト
    :param pd
    :return: none
    """
    host_name = pd['upload_data']['host_name']
    password_str = pd['upload_data']['password_str']
    user_name = pd['upload_data']['user_name']
    with FTP(host_name, passwd=password_str) as ftp:
        ftp.login(user=user_name, passwd=password_str)
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
def make_amp_total(pd):
    dir_list = ['caption', 'majime', 'qa', 'site', 'policy']
    for directory in dir_list:
        current_path = 'reibun/pc/' + directory
        file_list = os.listdir(current_path)
        now = time.time()
        for file in file_list:
            file_path = current_path + '/' + file
            mod_time = os.path.getmtime(file_path)
            if now - mod_time < 86400:
                amp_file_maker.amp_maker(file_path, pd)
                print('make amp: ' + file_path)


def modified_file_upload(pd):
    upper_dir = ['pc', 'amp']
    dir_list = ['caption', 'majime', 'qa', 'site', 'policy', 'images', 'sitepage', 'css']
    modified_file = []
    now = time.time()
    for upper in upper_dir:
        for directory in dir_list:
            current_path = 'reibun/' + upper + '/' + directory
            if os.path.exists(current_path):
                file_list = os.listdir(current_path)
                for file in file_list:
                    file_path = current_path + '/' + file
                    mod_time = os.path.getmtime(file_path)
                    if now - mod_time < 8640:
                        print(file_path)
                        modified_file.append(file_path)
    # print(modified_file)
    scp_upload(modified_file, pd)
    # amp_file = [x.replace('/pc/', '/amp/') for x in modified_file]
    # ftp_upload(amp_file)
    # ftp_upload(['reibun/index.html'])


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
    result = result.replace('"src', '" src')
    result = result.replace('"title="', '" title="')
    result = result.replace('"itemscope=', '" itemscope=')
    result = result.replace('"itemprop=', '" itemprop=')
    result = result.replace('imgitemprop=', 'img itemprop=')
    result = result.replace('imgwidth', 'img width')
    result = result.replace('"layout=', '" layout=')
    result = result.replace('"class=', '" class=')
    result = result.replace('"height="', '" height="')
    result = result.replace('"id="', '" id="')
    result = result.replace('"id="', '" id="')
    result = result.replace('"onclick="', '" onclick="')
    result = result.replace('"id="', '" id="')
    result = result.replace('"target="', '" target="')
    result = result.replace(', ', ',')
    result = css_minify(result)
    return result


def css_minify(long_str):
    css_str_l = re.findall(r'<style.*?>(.+?)</style>', long_str)
    if css_str_l:
        for css_str in css_str_l:
            css_str_r = css_str.replace(': ', ':')
            css_str_r = css_str_r.replace(' {', '{')
            long_str = long_str.replace(css_str, css_str_r)
    return long_str


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


def total_update(pd):
    dir_list = ['reibun/pc/caption', 'reibun/pc/majime', 'reibun/pc/qa',
                'reibun/pc/site', 'reibun/pc/policy']
    for file in html_list_maker(dir_list):
        tab_and_line_feed_remover(file)
    mod_list = modify_stamp_insert()
    amp_file_maker.amp_maker(mod_list, pd)
    modified_file_upload(pd)
    ftp_upload(['reibun/p_sitemap.xml', 'reibun/index.html'], pd)


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


def all_file_relational_art_insert(title, url, pd):
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
    amp_file_maker.amp_maker(mod_list, pd)
    ftp_upload(mod_list, pd)
    ftp_upload([x.replace('/pc/', '/amp/') for x in mod_list], pd)


def path_directory_adjuster(long_str, file_path):
    own_directory = re.findall(r'/pc/(.+?)/', file_path)[0]
    long_str = long_str.replace('../../pc/' + own_directory + '/', '')
    long_str = long_str.replace('../' + own_directory + '/', '')
    long_str = long_str.replace('href=""', 'href="../' + own_directory + '/"')
    return long_str


def all_file_rework(pd):
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
    amp_file_maker.amp_maker(mod_list, pd)
    ftp_upload(mod_list, pd)
    ftp_upload([x.replace('/pc/', '/amp/') for x in mod_list], pd)


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


def total_twitter_card_insert(pd):
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
    ftp_upload(update_list, pd)


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


def relational_file_pick_up(target_file):
    with open(target_file, 'r', encoding='utf-8') as f:
        long_str = f.read()
        relational_list = ['reibun/pc/css/base13.css', 'reibun/pc/css/pc13.css', 'reibun/pc/css/phone13.css',
                           'reibun/p_sitemap.xml',
                           target_file]  # 'reibun/atom.xml', 'reibun/rss10.xml', 'reibun/rss20.xml',
        p_time = 60 * 60 * 24 * 1
        now = time.time()
        img_list = re.findall(r'src="(.+?)"', long_str)
        if img_list:
            for img_path in img_list:
                if 'http://' not in img_path and 'https://' not in img_path:
                    if 'reibun/index.html' in target_file:
                        img_path = img_path.replace('pc/', 'reibun/pc/')
                    elif 'reibun/amp/index.html' == target_file:
                        img_path = re.sub(r'^images/', '../reibun/html_files/amp/images/', img_path)
                    elif 'reibun/amp/' in target_file:
                        img_path = img_path.replace('../images/', 'reibun/amp/images/')
                    else:
                        img_path = img_path.replace('../images/', 'reibun/pc/images/')
                    relational_list.append(img_path)
        mod_list = [r_path for r_path in relational_list if now - os.path.getmtime(r_path) < p_time]
        return mod_list


def files_upload(upload_file_list, pd):
    modify_list = []
    for file in upload_file_list:
        tab_and_line_feed_remover(file)
        add_files = relational_file_pick_up(file)
        modify_list.extend(add_files)
    modify_list = set(modify_list)
    modify_list = list(modify_list)
    ftp_upload(modify_list, pd)


def all_pc_file_upload(pd):
    up_dir = ['caption', 'majime', 'policy', 'qa', 'site', 'sitepage', 'reviews']
    html_list = ['reibun/index.html']
    for directory in up_dir:
        f_list = ['reibun/pc/' + directory + '/' + x for x in os.listdir('reibun/pc/' + directory)
                  if '.html' in x and '_test' not in x and '_copy' not in x]
        html_list.extend(f_list)
    ftp_upload(html_list, pd)


def all_amp_file_upload(pd):
    up_dir = ['caption', 'majime', 'policy', 'qa', 'site', 'sitepage']
    html_list = ['reibun/amp/index.html']
    for directory in up_dir:
        f_list = ['reibun/amp/' + directory + '/' + x for x in os.listdir('reibun/amp/' + directory)
                  if '.html' in x and '_test' not in x and '_copy' not in x]
        html_list.extend(f_list)
    ftp_upload(html_list, pd)


# todo: ABテストのscript作成

if __name__ == '__main__':
    os.chdir('../')
    print(os.getcwd())
    # target = ['reibun/pc/caption/fwari.html']
    # files_upload(target)

    # all_amp_file_upload()
    # all_pc_file_upload()

    # tab_and_line_feed_remover(target)
    # ftp_upload([target])
    # link_check('app/')
    # modify_stamp_insert()
    # make_amp_total()
    # modified_file_upload()
    # print(os.listdir('reibun/pc'))
    # jap_date_insert()
    # all_file_relational_art_insert('出会い系メール自動作成アプリのご紹介', '../majime/mail-applicaton.html')
    # all_file_rework()
    # total_twitter_card_insert()
    # insert_index_list('reibun/pc/majime/mail-applicaton.html')
    # total_update()

    up_files = ['reibun/html_files/pc/sitepage/ranking.html']
    auto_scp_upload(up_files)

    # ftp_upload(up_files)

    # scp_upload(['reibun/html_files/pc/images/common/site_name_250.png',
    #             'reibun/html_files/pc/images/common/site_name_250.png'], reibun.main_info.info_dict)
