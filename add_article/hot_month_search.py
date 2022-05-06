import glob
import os
import pathlib
import re

import file_upload
import new_from_md
import htaiken.main_info
import goodbyedt.main_info
import rei_site.main_info
import konkatsu.main_info
import women.main_info
import koibito.main_info
import joshideai.main_info
import howto.main_info
import reibun.main_info
import online_marriage.main_info
import make_html_for_shoshin

num_list = [['0', '０'], ['1', '１'], ['2', '２'], ['3', '３'], ['4', '４'], ['5', '５'], ['6', '６'], ['7', '７'],
            ['8', '８'], ['9', '９']]

mi_dict = {'htaiken': htaiken.main_info.info_dict, 'goodbyedt': goodbyedt.main_info.info_dict,
           'rei_site': rei_site.main_info.info_dict, 'konkatsu': konkatsu.main_info.info_dict,
           'women': women.main_info.info_dict, 'koibito': koibito.main_info.info_dict,
           'joshideai': joshideai.main_info.info_dict, 'howto': howto.main_info.info_dict,
           'reibun': reibun.main_info.info_dict, 'online_marriage': online_marriage.main_info.info_dict}


def make_num_list():
    z_l = '０１２３４５６７８９'
    h_l = '0123456789'
    result = []
    for i in range(10):
        result.append([h_l[i], z_l[i]])
    print(result)


def hot_month_pick_up(hot_month_str):
    md_list = glob.glob('**/**/md_files/', recursive=True)
    counter = 0
    for md_dir in md_list:
        if '_copy' not in md_dir and '_test' not in md_dir and not md_dir.startswith('test'):
            change_list = []
            md_files = glob.glob(md_dir + '/**/**.md', recursive=True)
            for md_path in md_files:
                with open(md_path, 'r', encoding='utf-8') as f:
                    md_str = f.read()
                if hot_month_str in md_str:
                    change_list.append(md_path)
                    counter += 1
            if change_list:
                print(md_dir)
                print(change_list)
    print('{} in {} files'.format(hot_month_str, counter))


def full_num_filter(full_str):
    for row in num_list:
        if row[0] in full_str:
            full_str = full_str.replace(row[0], row[1])
    return full_str


def half_num_filter(half_str):
    for row in num_list:
        if row[1] in half_str:
            half_str = half_str.replace(row[1], row[0])
    return half_str


def rewrite_hot_month(hot_month_str, next_month_str, next_next_str, now_season, next_season, only_season_flag):
    md_list = glob.glob('**/**/md_files/', recursive=True)
    md_list = list(set(md_list))
    md_list = [x for x in md_list if 'mass_production/' not in x]
    counter = 0
    upload_list = []
    up_files = []
    h_hot = half_num_filter(hot_month_str)
    h_next = half_num_filter(next_month_str)
    h_nn = half_num_filter(next_next_str)
    z_hot = full_num_filter(hot_month_str)
    z_next = full_num_filter(next_month_str)
    z_nn = full_num_filter(next_next_str)
    for md_dir in md_list:
        if '_copy' not in md_dir and '_test' not in md_dir and not md_dir.startswith('test') and 'sfd/' not in md_dir:
            change_list = []
            md_files = glob.glob(md_dir + '/**/**.md', recursive=True)
            md_files = [x for x in md_files if '_copy' not in x and '_test' not in x and '_ud' not in x]
            print(md_files)
            if md_dir.startswith('reibun/'):
                md_files.remove('reibun/md_files/pc/majime/m0summer.md')
            for md_path in md_files:
                with open(md_path, 'r', encoding='utf-8') as f:
                    md_str = f.read()
                if h_hot in md_str or z_hot in md_str:
                    if not only_season_flag:
                        md_str = md_str.replace(h_next, h_nn)
                        md_str = md_str.replace(z_next, h_nn)
                        md_str = md_str.replace(h_hot, h_next)
                        md_str = md_str.replace(z_hot, h_next)
                        md_str = md_str.replace(z_nn, h_nn)
                        target_month = h_next
                    else:
                        target_month = h_hot
                    if now_season and next_season:
                        hot_h = re.findall(r'## \S*' + target_month + r'\S*\n', md_str)
                        if hot_h:
                            hot_p = re.findall(r'(' + hot_h[0] + r'[\S\s]+?)\n##', md_str)
                            # print(hot_p)
                            if hot_p:
                                e_hot_p = hot_p[0].replace(now_season, next_season)
                                md_str = md_str.replace(hot_p[0], e_hot_p)
                                # print(e_hot_p)
                    # print(md_str)
                    with open(md_path, 'w', encoding='utf-8') as g:
                        g.write(md_str)
                    change_list.append(md_path)
                    counter += 1
            if change_list:
                # print(md_dir)
                print(change_list)
                upload_list.append(md_dir)
                up_files.extend([x.replace('.md', '.html').replace('/md_files/', '/html_files/') for x in change_list])
                if md_dir.startswith('reibun/'):
                    up_files.append('reibun/html_files/m_sitemap.xml')
                    up_files.extend(
                        [x.replace('.md', '.html').replace('/md_files/', '/html_files/').replace('/pc/', '/amp/')
                         for x in change_list])
                else:
                    sm_path = '{}/html_files/sitemap.xml'.format(md_dir.replace('/md_files/', ''))
                    if os.path.exists(sm_path):
                        up_files.append(sm_path)
                    else:
                        print('no sitemap in : ' + sm_path)
    print('{} in {} files'.format(hot_month_str, counter))
    # print(upload_list)
    # for p in up_files:
    #     print(p)
    return upload_list, up_files


def auto_update(project_list):
    for prj in [x.replace('/md_files/', '') for x in project_list]:
        if prj not in ['sfd', 'shoshin']:
            new_from_md.main(0, mi_dict[prj], mod_date_flag=True, last_mod_flag=True, upload_flag=False,
                             fixed_mod_date=False, first_time_flag=False)
            print('update : {}'.format(prj))


def make_next_month_str(month_num):
    if month_num == 12:
        next_num = 1
    else:
        next_num = month_num + 1
    return '{}月'.format(next_num)


def auto_month_update(old_month_str, now_season, next_season, only_season_flag):
    old_num = int(half_num_filter(old_month_str).replace('月', ''))
    # print(old_num)
    # print(type(old_num))
    next_month_str = make_next_month_str(old_num)
    print('next_month_str : {}'.format(next_month_str))
    next_next_str = make_next_month_str(int(next_month_str.replace('月', '')))
    print('next_next_month_str = {}'.format(next_next_str))
    upload_list, up_files = rewrite_hot_month(old_month_str, next_month_str, next_next_str, now_season, next_season,
                                              only_season_flag)
    print('up_files = {}'.format(up_files))
    print('len of up_files : '.format(len(list(set(up_files)))))
    # print(len(up_files))
    # shoshin_up = [x.replace('/html_files/', '/md_files/').replace('.html', '.md') for x in up_files if 'shoshin/' in x]
    # if shoshin_up:
    #     up_files = make_html_for_shoshin.add_new_article(shoshin_up)
    #     if up_files:
    #         file_upload.shoshin_scp_upload(up_files)
    auto_update(upload_list)
    file_upload.auto_scp_upload(up_files)
    # print(up_files)


def simple_month_filter(target_dir, replace_list):
    md_files = glob.glob(target_dir + '/md_files/**/**.md', recursive=True)
    md_files = [x for x in md_files if '/area-bbs/' not in x]
    # print(md_files)
    for md_path in md_files:
        p = pathlib.Path(md_path)
        p.open()
        m_str = p.read_text()
        e_str = m_str
        for row in replace_list:
            if row[0] in e_str:
                e_str = e_str.replace(row[0], row[1])
        if m_str != e_str:
            # print(e_str)
            # break
            p.open(mode='w')
            p.write_text(e_str)


if __name__ == '__main__':
    # auto_month_update('3月', '冬', '春', only_season_flag=False)  # 現在の月を記入 not 新しい月
    # ul = rewrite_hot_month('９月', '１０月', '１１月')
    # auto_update(ul)
    # hot_month_pick_up('11月')
    # make_num_list()
    simple_month_filter('sfd', [['4月', '<!--hot-month-->5月<!--e/hot-month-->']])
