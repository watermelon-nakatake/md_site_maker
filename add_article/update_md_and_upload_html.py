import glob
import os
import pickle
import re
import time
import importlib
import make_new_article
import str_counter_md
import monitor_all_sites
import make_html_for_shoshin
import file_upload
import new_from_md


def latest_modify_checker():
    domain_dict = {'reibun': 'demr.jp', 'rei_site': 'reibunsite.com', 'joshideai': 'joshideai.com',
                   'goodbyedt': 'goodbyedt.com', 'howto': 'deaihowto.com', 'htaiken': 'deaihtaiken.com',
                   'koibito': 'koibitodeau.com', 'konkatsu': 'netdekonkatsu.com',
                   'online_marriage': 'lovestrategyguide.com', 'shoshin': 'deaishoshinsha.com',
                   'women': 'deaiwomen.com'}
    rc_list_r = search_edited_md()
    rc_list = [x[0] for x in rc_list_r]
    if rc_list:
        md_file = rc_list[0]
        pj_name = re.sub(r'/.*$', '', md_file)
        info_mod = importlib.import_module(pj_name + '.main_info')
        str_counter_md.title_counter(md_file, [], 1, info_mod.info_dict)
        url_md = re.sub(r'^.+?/md_files/(.+)\.md', r'\1.html', md_file)
        page_url = 'https://www.{}/{}'.format(domain_dict[pj_name], url_md)
        # print(page_url)
        monitor_all_sites.check_gsc_query_data(page_url)


def change_html_and_upload():
    with open('pickle_data/add_last_upload.pkl', 'rb') as n:
        last_mod = pickle.load(n)
    recent_files = search_edited_md()
    print(recent_files)
    pj_name = re.sub(r'/md_files/.+$', '', recent_files[0][0])
    print(pj_name)
    pk_flag = False
    if pj_name == 'shoshin':
        md_files = [x[0] for x in recent_files if x[1] > last_mod and pj_name + '/md_files/' in x[0]]
        print(md_files)
        up_files = make_html_for_shoshin.add_new_article(md_files)
        if up_files:
            file_upload.shoshin_scp_upload(up_files)
            pk_flag = True
    else:
        info_mod = importlib.import_module(pj_name + '.main_info')
        pd = info_mod.info_dict
        new_from_md.main(0, pd, mod_date_flag=True, last_mod_flag=True, upload_flag=True,
                         first_time_flag=False, fixed_mod_date='')
        pk_flag = True
    if pk_flag:
        now = time.time()
        print(now)
        with open('pickle_data/add_last_upload.pkl', 'wb') as p:
            pickle.dump(now, p)


def search_edited_md():
    now = time.time()
    today = now - 60 * 60 * 24
    project_dir = [x for x in make_new_article.dir_dict]
    project_dir.extend(['reibun'])
    project_dir.remove('test')
    project_dir.remove('sfd')
    project_dir.remove('mass')
    all_md = []
    recent_files = []
    for p_dir in project_dir:
        md_files = glob.glob(p_dir + '/md_files/**/**.md', recursive=True)
        all_md.extend(md_files)
    for file in all_md:
        mod_time = os.path.getmtime(file)
        if mod_time > today:
            recent_files.append([file, mod_time])
            # print('{} : {}'.format(file, mod_time))
    if recent_files:
        recent_files.sort(key=lambda x: x[1], reverse=True)
    return recent_files


if __name__ == '__main__':
    # print(search_edited_md())
    change_html_and_upload()
