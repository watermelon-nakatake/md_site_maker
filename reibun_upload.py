from ftplib import FTP
import os
import time
import re
import datetime
from article_maker_rb import amp_maker
from amp_file_maker import amp_maker


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
                with open('file_other/amp_tp.html', "r", encoding='utf-8') as g:
                    tmp_str = g.read()
                    amp_maker(file_path, file_path.replace('/pc/', '/amp/'), tmp_str)
                print('make amp: ' + file_path)


def modified_file_upload():
    upper_dir = ['pc', 'amp']
    dir_list = ['caption', 'majime', 'qa', 'site', 'policy']
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
            mod_date_list[file] = str(mod_date)
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
            with open('reibun/p_sitemap.xml', encoding='utf-8') as g:
                sitemap_str = g.read()
                for page in mod_date_list:
                    sitemap_str = re.sub(
                        '<loc>https://www.demr.jp/pc/' + directory + '/' + page + '</loc><lastmod>(.+?)</lastmod>',
                        '<loc>https://www.demr.jp/pc/' + directory + '/' + page + '</loc><lastmod>'
                        + mod_date_list[page] + '</lastmod>', sitemap_str)
    return mod_list


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


def tab_and_line_feed_remover(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        long_str = f.read()
        str_list = long_str.splitlines()
        print(str_list)
        result = ''
        for x in str_list:
            y = x.strip()
            result += y
        result = result.replace('span class', 'span class')
        result = result.replace('img src', 'img src')
        result = result.replace('span itemprop', 'span itemprop')
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
    amp_maker(mod_list)
    modified_file_upload()
    ftp_upload(['reibun/p_sitemap.xml'])


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


if __name__ == '__main__':
    total_update()
    # tab_and_line_feed_remover('reibun/pc/majime/m0_2_1_test.html')
    # link_check('app/')
    # modify_stamp_insert()
    # make_amp_total()
    # modified_file_upload()
    # print(os.listdir('reibun/pc'))
    # jap_date_insert()
    # ftp_upload(['reibun/index.html'])
