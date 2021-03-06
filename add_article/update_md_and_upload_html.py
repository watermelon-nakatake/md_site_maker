import glob
import os
import pickle
import pprint
import re
import time
import importlib
from PIL import Image
import make_new_article
import str_counter_md
import monitor_all_sites
import make_html_for_shoshin
import file_upload
import new_from_md

replace_words = {'pcmax': 'PCMAX'}

def latest_modify_checker(print_flag):
    domain_dict = {'reibun': 'demr.jp', 'rei_site': 'reibunsite.com', 'joshideai': 'joshideai.com',
                   'goodbyedt': 'goodbyedt.com', 'howto': 'deaihowto.com', 'htaiken': 'deaihtaiken.com',
                   'koibito': 'koibitodeau.com', 'konkatsu': 'netdekonkatsu.com',
                   'online_marriage': 'lovestrategyguide.com', 'shoshin': 'deaishoshinsha.com',
                   'women': 'deaiwomen.com', 'mailsample': 'mailsample.jp', 'sfd': 'sefure-do.com'}
    rc_list_r = search_edited_md(print_flag)
    rc_list = [x[0] for x in rc_list_r]
    if rc_list:
        md_file = rc_list[0]
        pj_name = re.sub(r'/.*$', '', md_file)
        info_mod = importlib.import_module(pj_name + '.main_info')
        str_counter_md.title_counter(md_file, [], 1, info_mod.info_dict)
        url_md = re.sub(r'^.+?/md_files/(.+)\.md', r'\1.html', md_file)
        page_url = 'https://www.{}/{}'.format(domain_dict[pj_name], url_md)
        # print(page_url)
        with open(md_file, 'r', encoding='utf-8') as f:
            md_str = f.read()
        main_str = re.sub(r'^[\s\S]+k::.*?\n', '', md_str)
        main_str = re.sub(r'recipe_list = [\s\S]*$', '', main_str)
        main_str = re.sub(r'<!--.*?-->', '', main_str)
        print('str_len : {}'.format(len(main_str.replace('\n', ''))))
        gs_list = monitor_all_sites.check_gsc_query_data(page_url)
        if gs_list:
            pprint.pprint(gs_list[:20])
        if gs_list:
            set_dict = []
            for row in gs_list:
                str_s = row[4].split(' ')
                for p_str in str_s:
                    if p_str not in set_dict:
                        set_dict.append(p_str)
            for word in set_dict[:20]:
                if word in replace_words:
                    word_r = replace_words[word]
                else:
                    word_r = word
                print('{} : {}'.format(word_r, main_str.count(word_r)))


def change_html_and_upload():
    with open('pickle_data/add_last_upload.pkl', 'rb') as n:
        last_mod = pickle.load(n)
    recent_files = search_edited_md(print_flag=True)
    recent_files = [x for x in recent_files if x[1] > last_mod]
    print(recent_files)
    if recent_files:
        pj_name = re.sub(r'/md_files/.+$', '', recent_files[0][0])
    else:
        return
    print(pj_name)
    pk_flag = False
    if pj_name == 'shoshin':
        md_files = [x[0] for x in recent_files if x[1] > last_mod and pj_name + '/md_files/' in x[0]]
        print(md_files)
        up_files = make_html_for_shoshin.shoshin_md_to_html(md_files, mod_flag=True)
        for md_path in md_files:
            up_files.extend(insert_image_str_and_resize(md_path))
        up_files = css_uploader(pj_name, last_mod, up_files)
        if up_files:
            file_upload.shoshin_scp_upload(up_files)
            pk_flag = True
    else:
        md_files = [x[0] for x in recent_files if x[1] > last_mod and pj_name + '/md_files/' in x[0]]
        up_files = []
        for md_path in md_files:
            up_files.extend(insert_image_str_and_resize(md_path))
        info_mod = importlib.import_module(pj_name + '.main_info')
        pd = info_mod.info_dict
        new_from_md.main(0, pd, mod_date_flag=True, last_mod_flag=True, upload_flag=True,
                         first_time_flag=False, fixed_mod_date='')
        up_files = css_uploader(pj_name, last_mod, up_files)
        if up_files:
            file_upload.scp_upload(up_files, pd)
        pk_flag = True
    if pk_flag:
        now = time.time()
        print(now)
        with open('pickle_data/add_last_upload.pkl', 'wb') as p:
            pickle.dump(now, p)


def css_uploader(pj_name, last_mod, up_files):
    css_path = pj_name + '/html_files/css/main.css'
    if css_path not in up_files and os.path.isfile(css_path):
        css_mod = os.path.getmtime(css_path)
        if css_mod > last_mod:
            up_files.append(css_path)
    return up_files


def search_edited_md(print_flag):
    now = time.time()
    today = now - 60 * 60 * 24
    project_dir = [x for x in make_new_article.dir_dict]
    project_dir.extend(['reibun'])
    project_dir.extend(['mailsample'])
    project_dir.remove('test')
    # project_dir.remove('sfd')
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
            if print_flag:
                print('{} : {}'.format(file, mod_time))
    if recent_files:
        recent_files.sort(key=lambda x: x[1], reverse=True)
    return recent_files


def insert_image_str_and_resize(md_path):
    up_img = []
    image_files = glob.glob('image_insert/**/**', recursive=True)
    image_files.remove('image_insert/')
    if image_files:
        print(image_files)
    else:
        print('there is no image')
    if image_files:
        with open('pickle_data/used_img.pkl', 'rb') as n:
            used_img = pickle.load(n)
        img_name = re.sub(r'^.*/(.+)$', r'\1', image_files[0])
        if img_name in used_img:
            print('this image has used !!')
            used_flag = True
        else:
            used_flag = False
        with open(md_path, 'r', encoding='utf-8') as f:
            md_str = f.read()
        # print(img_name)
        if 'html_files/images/art_images/' not in md_str:
            first_h2 = re.findall(r'\n## .+?\n', md_str)[0]
            pj_dir = re.sub(r'^(.+?)/.*$', r'\1', md_path)
            md_name = re.sub(r'^.*/md_files/(.+?).md', r'\1', md_path)
            image_path = '{}/html_files/images/art_images/{}.jpg'.format(pj_dir, md_name.replace('/', '_'))
            act_noun_l = re.findall(r"'act_noun': '(.+?)'", md_str)
            if act_noun_l:
                act_noun = act_noun_l[0]
            else:
                key_str = re.findall(r'\nk::(.+?)\n', md_str)[0]
                act_noun = key_str.split()[0]
            image_tag = '![{}](../../html_files/images/art_images/{}.jpg)'.format(act_noun, md_name.replace('/', '_'))
            md_str = md_str.replace(first_h2, first_h2 + '\n' + image_tag + '\n')
            # print(md_str)
            with open(md_path, 'w', encoding='utf-8') as g:
                g.write(md_str)
            img = Image.open(image_files[0])
            img_gr = img.resize((760, 470))
            img_gr.save(image_path)
            up_img.append(image_path)
            if not used_flag:
                used_img.append(img_name)
                with open('pickle_data/used_img.pkl', 'wb') as p:
                    pickle.dump(used_img, p)
            os.remove(image_files[0])
    return up_img


if __name__ == '__main__':
    # print(search_edited_md())
    change_html_and_upload()
