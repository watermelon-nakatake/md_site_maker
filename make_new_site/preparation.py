from add_article import make_article_list
import re
import os
import collections
import glob
import shutil
import htaiken.main_info
import file_upload


def make_project_dir_and_pd_file(project_name):
    if not os.path.exists(project_name):
        os.mkdir(project_name)
    if not os.path.exists(project_name + '/' + 'main_info.py'):
        pd_path = project_name + '/' + 'main_info.py'
        shutil.copy('template_files/main_info.py', pd_path)
        with open(pd_path, 'r', encoding='utf-8') as f:
            pd_str = f.read()
            pd_str = pd_str.replace('<!--project-name-->', project_name)
            pd_str = pd_str.replace('rp_project_name', project_name)
            with open(pd_path, 'w', encoding='utf-8') as g:
                g.write(pd_str)
        print('make pd file !')


def preparation_for_new_project(pd):
    make_html_and_md_dir(pd)
    copy_template_files(pd)
    insert_to_temp(pd)
    make_top_page(pd)
    make_sitemap_page(pd)


def change_pk_dic(pd):
    pk_dic = make_article_list.read_pickle_pot('main_data', pd)
    # print(pk_dic)
    pk_dic[144] = pk_dic[146]
    del pk_dic[146]
    print(pk_dic)
    make_article_list.save_data_to_pickle(pk_dic, 'main_data', pd)


def insert_pub_date(pd):
    pk_dic = make_article_list.read_pickle_pot('main_data', pd)
    for id_p in pk_dic:
        print(pk_dic[id_p])
        with open('reibun/html_files/pc/' + pk_dic[id_p]['file_path'], 'r', encoding='utf-8') as f:
            long_str = f.read()
            pub_str_l = re.findall(r'<time itemprop="datePublished" datetime="(.+?)">', long_str)
            if pub_str_l:
                pub_str = pub_str_l[0]
            else:
                raise Exception
            pk_dic[id_p]['pub_date'] = pub_str
    print(pk_dic)
    for id_q in pk_dic:
        print(pk_dic[id_q]['pub_date'])
    # make_article_list.save_data_to_pickle(pk_dic, 'main_data')


def insert_id_and_category_to_html(pd):
    pk_dic = make_article_list.read_pickle_pot('main_data', pd)
    for id_p in pk_dic:
        with open('reibun/html_files/pc/' + pk_dic[id_p]['file_path'], 'r', encoding='utf-8') as f:
            long_str = f.read()
            long_str = long_str.replace('<head><!-- Global site tag (gtag.js) -->',
                                        '<head><!--id_num_' + str(id_p) + '--><!--category_' + pk_dic[id_p]['category']
                                        + '--><!-- Global site tag (gtag.js) -->')
            with open('reibun/html_files/pc/' + pk_dic[id_p]['file_path'], 'w', encoding='utf-8') as g:
                g.write(long_str)


def insert_id_and_category_to_md(pd):
    pk_dic = make_article_list.read_pickle_pot('main_data', pd)
    for id_p in pk_dic:
        md_path = 'reibun/md_files/pc/' + pk_dic[id_p]['file_path'].replace('.html', '.md')
        if os.path.exists(md_path):
            with open(md_path, 'r', encoding='utf-8') as f:
                long_str = f.read()
                long_str = re.sub(r'(d::.*?\n)', r'\1n::' + str(id_p) + r'\n', long_str)
                long_str = long_str.replace('/reibun/pc/', '/html_files/pc/')
                # print(long_str)
                with open(md_path, 'w', encoding='utf-8') as g:
                    g.write(long_str)
        else:
            print('no md_file : ' + pk_dic[id_p]['file_path'])


def check_html_tag(long_str, h_path):
    body_l = re.findall(r'<body.*?>(.+)</body>', long_str)
    if body_l:
        body = re.sub(r'<script.+?</script>', '', body_l[0])
        body = re.sub(r'<!--.+?-->', '', body)
        tag_str = re.findall(r'<(.+?)[\s>]', body)
        # print(tag_str)
        c_list = collections.Counter(tag_str)
        # print(c_list)
        s_tags = []
        e_tags = []
        for tag in list(set(tag_str)):
            if tag not in ['img', 'br', '/br', 'input', 'meta', 'hr']:
                if '/' in tag:
                    e_tags.append(tag)
                else:
                    s_tags.append(tag)
        for st in s_tags:
            if c_list[st] != c_list['/' + st]:
                print(h_path)
                print('no match : ' + st)
    if '](' in long_str:
        print(h_path + ' : error ](')
    # if '%' in long_str:
    #     t_str = re.findall(r'.{10}%.{10}', long_str)
    #     print(h_path + ' : error %')
    #     for ps in t_str:
    #         print(ps)
    s_str = re.findall(r'#[^shmk"\']', long_str)
    if s_str:
        print(s_str)
        print(h_path + ' : error # in this page')


def check_all_html(target_dir):
    all_files = glob.glob(target_dir + '/**/**.html', recursive=True)
    for h_path in all_files:
        with open(h_path, 'r', encoding='utf-8') as f:
            long_str = f.read()
        check_html_tag(long_str, h_path)


def make_html_and_md_dir(pd):
    with open('template_files/template/index_temp.md', 'r', encoding='utf-8') as f:
        md_temp = f.read()
    if not os.path.exists(pd['project_dir'] + '/pickle_pot'):
        os.mkdir(pd['project_dir'] + '/pickle_pot')
    if not os.path.exists(pd['project_dir'] + '/html_files'):
        os.mkdir(pd['project_dir'] + '/html_files')
    if not os.path.exists(pd['project_dir'] + '/md_files'):
        os.mkdir(pd['project_dir'] + '/md_files')
    for cat_name in pd['category_data']:
        if not os.path.exists(pd['project_dir'] + '/html_files/' + cat_name):
            os.mkdir(pd['project_dir'] + '/html_files/' + cat_name)
        if not os.path.exists(pd['project_dir'] + '/md_files/' + cat_name):
            os.mkdir(pd['project_dir'] + '/md_files/' + cat_name)
            index_md = md_temp
            index_md = index_md.replace('<!--title-->', pd['category_data'][cat_name][0])
            index_md = index_md.replace('<!--id-num-->', str(pd['category_data'][cat_name][2]))
            with open(pd['project_dir'] + '/md_files/' + cat_name + '/' +
                      pd['category_data'][cat_name][1].replace('.html', '.md'), 'w', encoding='utf-8') as g:
                g.write(index_md)
    # todo: トップページとhtmlサイトマップページの自動作成


def make_top_page(pd):
    if not os.path.exists(pd['project_dir'] + '/html_files/index.html'):
        with open('template_files/top_tmp.html', 'r', encoding='utf-8') as f:
            long_str = f.read()
            long_str = file_upload.tab_and_line_feed_remove_from_str(long_str)
            long_str = long_str.replace('<!--site-name-->', pd['site_name'])
            long_str = long_str.replace('<!--main-domain-->', 'https://www.' + pd['domain_str'] + '/')
            long_str = long_str.replace('<!--main-dir-->', pd['main_dir'])
            cat_str = ''.join(['<li><a href="{}/{}">{}</a></li>'
                              .format(x, pd['category_data'][x][1], pd['category_data'][x][0]) for x in
                               pd['category_data']])
            long_str = long_str.replace('<!--temp_category_list-->', cat_str)
            if not pd['default_img']:
                long_str = long_str.replace('<!--t-image-->', 'common/default_img.html')
            else:
                long_str = long_str.replace('<!--t-image-->', pd['default_img'])
            if 'google_id' in pd:
                if pd['google_id']:
                    long_str = long_str.replace('<!--google-id-->', pd['google_id'])
            with open(pd['project_dir'] + '/html_files/index.html', 'w', encoding='utf-8') as g:
                g.write(long_str)


def make_sitemap_page(pd):
    if not os.path.exists(pd['project_dir'] + '/html_files/sitemap.html'):
        with open('template_files/sitemap.html', 'r', encoding='utf-8') as f:
            long_str = f.read()
            long_str = file_upload.tab_and_line_feed_remove_from_str(long_str)
            long_str = long_str.replace('<!--site-name-->', pd['site_name'])
            long_str = long_str.replace('<!--main-domain-->', 'https://www.' + pd['domain_str'] + '/')
            long_str = long_str.replace('<!--main-dir-->', pd['main_dir'])
            cat_str = ''.join(['<li><a href="{}/{}">{}</a></li>'
                              .format(x, pd['category_data'][x][1], pd['category_data'][x][0]) for x in
                               pd['category_data']])
            long_str = long_str.replace('<!--temp_category_list-->', cat_str)
            if not pd['default_img']:
                long_str = long_str.replace('<!--t-image-->', 'common/default_img.html')
            else:
                long_str = long_str.replace('<!--t-image-->', pd['default_img'])
            if 'google_id' in pd:
                if pd['google_id']:
                    long_str = long_str.replace('<!--google-id-->', pd['google_id'])
            with open(pd['project_dir'] + '/html_files/sitemap.html', 'w', encoding='utf-8') as g:
                g.write(long_str)


def make_html_dir(pd):
    print(pd)
    print(glob.glob(pd['project_dir'] + '/md_files/**/', recursive=True))
    all_md_dir = [x.replace('/md_files/', '/html_files/') for x in glob.glob(pd['project_dir'] + '/md_files/**/',
                                                                             recursive=True)]
    # all_md_dir.extend([pd['project_dir'] + '/html_files/' + pd['main_dir'] + 'css',
    #                   pd['project_dir'] + '/html_files/' + pd['main_dir'] + 'images'])
    print(all_md_dir)
    for dir_path in all_md_dir:
        if not os.path.exists(dir_path):
            print('make_dir : ' + dir_path)
            os.makedirs(dir_path)


def copy_template_files(pd):
    copy_list = ['template_files/template', 'template_files/images', 'template_files/css', 'template_files/link']
    if not os.path.exists(pd['project_dir'] + '/html_files/pc/template'):
        for base in copy_list:
            shutil.copytree(base, pd['project_dir'] + '/html_files/' + pd['main_dir'] +
                            base.replace('template_files/', ''))


def insert_to_temp(pd):
    with open(pd['project_dir'] + '/html_files/' + pd['main_dir'] + '/template/main_tmp.html', 'r',
              encoding='utf-8') as f:
        long_str = f.read()
        long_str = file_upload.tab_and_line_feed_remove_from_str(long_str)
        long_str = long_str.replace('<!--site-name-->', pd['site_name'])
        long_str = long_str.replace('<!--main-domain-->', 'https://www.' + pd['domain_str'] + '/')
        long_str = long_str.replace('<!--main-dir-->', pd['main_dir'])
        cat_str = ''.join(['<li><a href="../{}/{}">{}</a></li>'
                          .format(x, pd['category_data'][x][1], pd['category_data'][x][0]) for x in
                           pd['category_data']])
        long_str = long_str.replace('<!--temp_category_list-->', cat_str)
        if 'google_id' in pd:
            if pd['google_id']:
                long_str = long_str.replace('<!--google-id-->', pd['google_id'])
        with open(pd['project_dir'] + '/html_files/' + pd['main_dir'] + '/template/main_tmp.html', 'w',
                  encoding='utf-8') as g:
            g.write(long_str)


if __name__ == '__main__':
    # 新規プロジェクトの１段階
    pj_name = 'htaiken'
    make_project_dir_and_pd_file(pj_name)

    # info_dict.py の作成後実行
    # pd_t = htaiken.main_info.info_dict  # pdをimportに追加、変更
    # preparation_for_new_project(pd_t)
