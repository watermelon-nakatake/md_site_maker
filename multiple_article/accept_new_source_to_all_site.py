import glob
import os
import pickle
import time
import make_new_article
import new_from_md
import make_html_for_shoshin
import file_upload
import importlib
import now_upload


def accept_source_for_md_in_all_site_and_upload(select_pj, upload_flag):
    all_up_flag = True
    if select_pj:
        pj_list = select_pj
    else:
        pj_list = [x for x in make_new_article.dir_dict if x not in ['sfd', 'test', 'mass']][4:]
    for pj_name in pj_list:
        recent_files = make_new_article.make_md_from_exist_keywords(pj_name)
        pk_flag = False
        if pj_name == 'shoshin':
            if all_up_flag:
                md_files = [x for x in glob.glob('shoshin/md_files/**/**.md') if '/beginner/' in x or '/means/' in x]
            else:
                md_files = recent_files
            up_files = make_html_for_shoshin.shoshin_md_to_html(md_files, mod_flag=False)
            if up_files and upload_flag:
                up_files.append('shoshin/html_files/a_sitemap.xml')
                file_upload.shoshin_scp_upload(up_files)
                pk_flag = True
        else:
            info_mod = importlib.import_module(pj_name + '.main_info')
            pd = info_mod.info_dict
            if upload_flag:
                new_from_md.main(0, pd, mod_date_flag=True, last_mod_flag=True, upload_flag=True,
                                 first_time_flag=False, fixed_mod_date='')
                pk_flag = True
            else:
                new_from_md.main(0, pd, mod_date_flag=True, last_mod_flag=True, upload_flag=False,
                                 first_time_flag=False, fixed_mod_date='')
        if pk_flag:
            now = time.time()
            # print(now)
            with open('pickle_data/add_last_upload.pkl', 'wb') as p:
                pickle.dump(now, p)


def all_update_and_safety_upload():
    accept_source_for_md_in_all_site_and_upload([], False)
    now_upload.upload_in_order([])


if __name__ == '__main__':
    # accept_source_for_md_in_all_site_and_upload(['shoshin'], True)
    all_update_and_safety_upload()
