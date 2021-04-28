import make_article_list
import re
import os
import collections
import glob
import reibun.main_info


def preparation_for_new_project(pd):
    change_pk_dic(pd)


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


if __name__ == '__main__':
    # make_new_main_data_pkl()
    # change_pk_dic()
    # insert_pub_date()
    # insert_id_and_category_to_html()
    # print(make_article_list.read_pickle_pot('main_data', reibun.main_info.info_dict))
    # insert_id_and_category_to_md(reibun.main_info.info_dict)
    check_all_html('reibun/html_files/pc')
