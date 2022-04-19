# import pprint
import glob
import pathlib
import pickle
import pprint
import random
import re
import urllib.request
import os
import csv
from PIL import Image
from bs4 import BeautifulSoup
import requests
import words_dict

ok_div = ['<div class="maruck">', '<div class="fr2">', '<div class="alt_img_t">', '<div class="icon">',
          '<div class="fl1">', '<div class="lm_b lm_2">', '<div class="rm_b rm_2">']
ds_list = ['ワクワクメール', 'PCMAX', 'ハッピーメール', 'Jメール']


def read_article_from_sfd_page(page_url, stop_flag, md_remake_flag):
    tag_l = []
    html_path = re.sub(r'https://www\.sefure-do\.com/(.*)/', r'sfd/del_html/\1/index.html', page_url)
    md_path = html_path.replace('/del_html/', '/del_md/').replace('/index.html', '.md')
    if not md_remake_flag and os.path.exists(md_path):
        pass
    else:
        # スクレイピング対象の URL にリクエストを送り HTML を取得する
        print('scrape: ' + page_url)
        res = requests.get(page_url)
        # レスポンスの HTML から BeautifulSoup オブジェクトを作る
        soup = BeautifulSoup(res.text, 'html.parser')
        html_str = str(soup)
        dir_path = html_path.replace('/index.html', '')
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        with open(html_path, 'w', encoding='utf-8') as h:
            h.write(html_str)

        title_text = soup.find('title').get_text().replace(' - セフレ道', '')
        # print(title_text)
        md = soup.find('time', {'class': 'updated'})
        if md:
            mod_time = md.get('datetime')
        else:
            mod_time = ''
        meta_description = soup.find('head').find('meta', {'name': 'description'})
        if meta_description:
            des_str = meta_description['content']
        else:
            des_str = ''
        # print(mod_time)
        main_txt = soup.find_all('div', {'class': 'entry-content'})[0]
        main_str = str(main_txt)
        main_str = re.sub(r'^.*<div class="entry-content">', '', main_str)
        main_str = re.sub(r'<div class="adbox">.*$', '', main_str)
        main_str = re.sub(r'</div></div>$', '', main_str)
        main_str = re.sub(r'<noscript.*?</noscript>', '', main_str)
        dir_name = re.sub(r'https://www\.sefure-do\.com/(.+?)/', r'\1', page_url)
        main_str = main_str.replace('https://www.sefure-do.com/' + dir_name + '/', '../')
        main_str = main_str.replace('https://www.sefure-do.com/' + dir_name, '../')

        md_str, tag_l = html_to_markdown_filter(main_str, page_url, soup)
        if tag_l:
            print('error!! there in tag : {}'.format(tag_l))
            # if stop_flag:
            #     return
        md_head = 't::{}\nd::{}\nn::{}\nm::{}'.format(title_text, des_str, 1, mod_time.replace('+0900', ''))
        md_f = md_head + '\n\n' + md_str
        print(md_f)
        md_path = html_path.replace('/del_html/', '/del_md/').replace('/index.html', '.md')
        with open(md_path, 'w', encoding='utf-8') as m:
            m.write(md_f)
    return tag_l


def area_bbs_filter(main_str, soup):
    st_my_box_l = soup.find_all('div', {'class': 'st-mybox'})
    if st_my_box_l:
        st_mybox_list = []
        for st_my_box in st_my_box_l:
            if 'のおすすめNo.' in str(st_my_box):
                for ds_name in ds_list:
                    if ds_name in str(st_my_box):
                        st_mybox_list.append(ds_name)
                        main_str = main_str.replace(re.sub(r'<noscript.*?</noscript>', '', str(st_my_box)),
                                                    '%st_box_' + ds_name + '%')
                        break
            else:
                st_mybox_list.append([])
                for ds_name in ds_list:
                    if ds_name in str(st_my_box):
                        st_mybox_list[0].append(ds_name)
                main_str = main_str.replace(re.sub(r'<noscript.*?</noscript>', '', str(st_my_box)),
                                            '%st_box_' + '_'.join(st_mybox_list[0]) + '%')
    replace_list = [['st-editor-margin', 'fuk']]
    for rp in replace_list:
        mf_l = soup.find_all('div', {'class': rp[0]})
        if mf_l:
            for mf in mf_l:
                mf_str = str(mf)
                mf_title = mf.text
                if '<noscript>' in mf_str:
                    mf_str = re.sub('<noscript.*?</noscript>', '', mf_str)
                main_str = main_str.replace(mf_str, '%{}_{}%\n'.format(rp[1], mf_title))
    cm_l = soup.find_all('div', {'class': 'clip-memobox'})
    if cm_l:
        for cm in cm_l:
            cm_str = str(cm)
            cm_p_l = re.findall(r'<p>.*</p>', cm_str)
            cm_p = ''
            if cm_p_l:
                cm_p = cm_p_l[0].replace('</p></p>', '</p>')
            if '<noscript>' in cm_str:
                cm_str = re.sub('<noscript.*?</noscript>', '', cm_str)
            main_str = main_str.replace(cm_str, '%clip_memo%\n{}\n'.format(cm_p))
    main_str = main_str.replace('<div class="graybox">', '')
    return main_str


def html_to_markdown_filter(main_str, page_url, soup):
    main_str = main_str.replace('<div id="main-content">', '')

    if '/area-bbs/' in page_url:
        main_str = area_bbs_filter(main_str, soup)
    else:
        mt_l = re.findall(r'<div class="st-editor-margin".*?><div class="st-minihukidashi-box".*?>.*?</ul></div></div>',
                          main_str)
        if mt_l:
            for mt_str in mt_l:
                mt_title = re.findall(r'</i>(.+?)</span>', mt_str)[0]
                mt_list = re.findall(r'<ul>.+?</ul>', mt_str)[0]
                main_str = main_str.replace(mt_str, '%matome{}%\n{}'.format(mt_title, mt_list))
    # return

    main_str = main_str.replace('></img>', '/>')
    main_str = main_str.replace('<br/> ', '<br/>')
    main_str = main_str.replace('<p> </p>', '')
    main_str = re.sub(r'<span class="huto".*?>(.+?)</span>', r'**\1**', main_str)
    main_str = re.sub(r'<span class="hutoaka".*?>(.+?)</span>', r'**\1**', main_str)
    main_str = re.sub(r'<strong>(.+?)</strong>', r'**\1**', main_str)
    main_str = re.sub(r'<span class="sfd1">(.+?)</span>', r'*\1*', main_str)
    main_str = re.sub(r'<em>(.+?)</em>', r'*\1*', main_str)
    main_str = re.sub(r'<span class="sfd2">(.+?)</span>', r'*\1*', main_str)
    main_str = re.sub(r'<div class="sdcenter">(.*?)</div>', r'\1', main_str)

    a_list = re.findall(r'<a.*?>.*?</a>', main_str)
    a_list = list(set(a_list))
    for a_str in a_list:
        a_url_l = re.findall(r'href="(.+?)"', a_str)
        if a_url_l:
            a_url = a_url_l[0]
            if 'sefure-do.com' in a_url:
                a_url = re.sub(r'^.+?sefure-do\.com', '', a_url)
            if 'https://' in a_url or 'http://' in a_url:
                ins_url = a_url
            else:
                if '/area-bbs/' in a_url or '/friend-with-benefits/' in a_url or '/url/' in a_url or '/link/' in a_url:
                    ins_url = '..' + a_url
                else:
                    ins_url = a_url
                    ins_url = re.sub(r'^\.\./', '', ins_url)
                if ins_url in ['../area-bbs/', '../friend-with-benefits/']:
                    ins_url = re.sub(r'/$', '', ins_url)
                elif ins_url not in ['../area-bbs', '../friend-with-benefits'] and '/url/' not in ins_url \
                        and '/link/' not in ins_url:
                    ins_url = re.sub(r'/$', '', ins_url)
                    ins_url = ins_url + '.md'
        else:
            ins_url = ''
            print('error!! : no url')

        if 'class="st-cardlink"' in a_str:
            main_str = main_str.replace(a_str, '[card_link](../{})\n'.format(ins_url))
        else:
            a_text_l = re.findall(r'<a .*?>(.+?)</a>', a_str)
            if a_text_l:
                a_text = a_text_l[0]
            else:
                a_text = ''
            main_str = main_str.replace(a_str, '[{}]({})'.format(a_text, ins_url))

    d_list = re.findall(r'<div class="kanren st-cardbox"><dl.*?</dl></div>', main_str)
    for d_str in d_list:
        # print(d_str)
        if 'alt="セフレの作り方"' in d_str:
            main_str = main_str.replace(d_str, '[card_link](../friend-with-benefits)\n')
    #  replace big image
    img_l = re.findall(r'<img .+?/>', main_str)
    for img_str in img_l:
        # print(img_str)
        alt_str = re.findall(r'alt="(.*?)"', img_str)
        if 'data-src="' in img_str:
            img_url = re.findall(r'data-src="(.*?)"', img_str)
        else:
            img_url = re.findall(r'src="(.*?)"', img_str)
        if ('aligncenter' in img_str or 'wp-caption' in main_str) and img_url:
            if '?' in img_url[0]:
                img_url[0] = re.sub(r'\?.*$', '', img_url[0])
            # print(img_url)
            img_path, img_size = image_download(img_url[0])
            if alt_str:
                alt_data = alt_str[0]
            else:
                alt_data = ''
            ins_str = '![{}](../{})'.format(alt_data, img_path)
            # print(ins_str)
            main_str = main_str.replace(img_str, ins_str)
    kw_l = re.findall(r'<div class="st-kaiwa-box.+?</div></div></div>', main_str)
    for kw_str in kw_l:
        # print(kw_str)
        kw_text = re.findall(r'<div class="st-kaiwa-hukidashi.*?">(.+?)</div>', kw_str)[0]
        if '<p>' in kw_text:
            kw_text = kw_text.replace('<p>', '</p><p>')
        kw_text = '<p>{}</p>'.format(kw_text)
        kw_text = kw_text.replace('</p></p>', '</p>')
        # print(kw_text)
        # print('\n')
        if 'kaiwaicon2' in kw_str:
            if '？' in kw_str:
                ins_kw = '%r_?%\n{}\n'.format(kw_text)
            else:
                ins_kw = '%r_!%\n{}\n'.format(kw_text)
        else:
            ins_kw = '%l_parm%\n{}\n'.format(kw_text)
        main_str = main_str.replace(kw_str, ins_kw)
    main_str = re.sub(r'<div class="maruck">(.+?)</div>', r'%arlist%\n\1\n', main_str)
    main_str = re.sub(r'<li .+?>', '<li>', main_str)
    ul_l = re.findall(r'<ul.*?</ul>', main_str)
    if ul_l:
        for ul in ul_l:
            ul_str = ''.join('- {}\n'.format(x) for x in re.findall(r'<li>(.+?)</li>', ul))
            main_str = main_str.replace(ul, ul_str + '\n')

    mk_re_list = [['<p>', ''], ['</p>', '\n\n'], ['<br/>', '\n'], ['<h2>', '\n## '], ['</h2>', '\n\n'],
                  ['<h3>', '\n### '], ['</h3>', '\n\n'], ['<h4>', '\n#### '], ['</h4>', '\n\n'],
                  ['<p class="st-share">', '%share%'], ['(/url/', '(../url/'],
                  ['/)', ')'], ['(https://www.sefure-do.com/friend-with-benefits)', '(../friend-with-benefits)'],
                  ['<section>', ''], ['</section>', ''], ['<b>', '*'], ['</b>', '*']]
    main_str = re.sub(r'<p .+?>', '', main_str)
    main_str = re.sub(r'<div class="wp-caption aligncenter".+?>', '', main_str)
    for mk_re in mk_re_list:
        main_str = main_str.replace(mk_re[0], mk_re[1])
    # print(main_str)
    div_list = list(set(re.findall(r'<div .*?>', main_str)))
    # print(set(div_list))
    for d_row in div_list:
        if d_row not in ok_div:
            print('error!! : new div => {}'.format(d_row))
    main_str = main_str.replace('</div>', '')
    tag_l = list(set(re.findall(r'<.*?>', main_str)))
    return main_str, tag_l


# def html_to_html_filter(main_str):
#     main_str = re.sub(r'<span class="huto".*?>(.+?)</span>', r'<strong>\1</strong>', main_str)
#     main_str = main_str.replace('></img>', '/>')
#     main_str = main_str.replace('<br/> ', '<br/>')
#     a_list = re.findall(r'<a.*?>.*?</a>', main_str)
#     for a_str in a_list:
#         if 'class="st-cardlink"' in a_str:
#             a_url = re.findall(r'href="https://www.sefure-do.com/(.*?)"', a_str)[0]
#             main_str = main_str.replace(a_str, '<a href="{}" class="ar-card">card_link</a>'.format(a_url))
#
#     d_list = re.findall(r'<div class="kanren st-cardbox"><dl.*?</dl></div>', main_str)
#     for d_str in d_list:
#         # print(d_str)
#         if 'alt="セフレの作り方"' in d_str:
#             main_str = main_str.replace(d_str, '<a href="friend-with-benefits/index.html" class="sf-card">セフレの作り方</a>')
#     #  replace big image
#     img_l = re.findall(r'<img .+?/>', main_str)
#     for img_str in img_l:
#         # print(img_str)
#         alt_str = re.findall(r'alt="(.*?)"', img_str)
#         img_url = re.findall(r'data-src="(.*?)"', img_str)
#         if 'aligncenter' in img_str and img_url:
#             # print(img_url)
#             img_path, img_size = image_download(img_url[0])
#             if alt_str:
#                 alt_data = alt_str[0]
#             else:
#                 alt_data = ''
#             ins_str = '<div class="alt_img_t"><img src="../{}" alt="{}" width="{}" height="{}" />' \
#                       '</div>'.format(img_path, alt_data, img_size[0], img_size[1])
#             # print(ins_str)
#             main_str = main_str.replace(img_str, ins_str)
#     kw_l = re.findall(r'<div class="st-kaiwa-box.+?</div></div></div>', main_str)
#     for kw_str in kw_l:
#         # print(kw_str)
#         kw_text = re.findall(r'<div class="st-kaiwa-hukidashi.*?">(.+?)</div>', kw_str)[0]
#         if '<p>' in kw_text:
#             kw_text = kw_text.replace('<p>', '</p><p>')
#         kw_text = '<p>{}</p>'.format(kw_text)
#         kw_text = kw_text.replace('</p></p>', '</p>')
#         # print(kw_text)
#         # print('\n')
#         if 'kaiwaicon2' in kw_str:
#             ins_kw = '<div class="fr2"><div class="icon"><div class="rm_b rm_2"></div></div>{}</div>'.format(kw_text)
#         else:
#             ins_kw = '<div class="fl1"><div class="icon"><div class="lm_b lm_2"></div></div>{}</div>'.format(kw_text)
#         main_str = main_str.replace(kw_str, ins_kw)
#
#     main_str = re.sub(r'<p><div class="alt_img_t">(.+?)</div></p>', r'<div class="alt_img_t">\1</div>', main_str)
#     print(main_str)
#     div_list = re.findall(r'<div .*?>', main_str)
#     # print(set(div_list))
#     for d_row in div_list:
#         if d_row not in ok_div:
#             print('error!! : new div => {}'.format(d_row))
#     return main_str


def image_download(img_url):
    save_dir = 'sfd/del_md/'
    save_path = save_dir + 'images/art_images/' + re.sub(r'^.+/', '', img_url)
    if not os.path.exists(save_path):
        print('download: {}'.format(save_path))
        urllib.request.urlretrieve(img_url, save_path)
    im = Image.open(save_path)
    return save_path.replace(save_dir, ''), im.size


def get_all_url_list(csv_path):
    with open(csv_path) as f:
        reader = csv.reader(f)
        csv_list = [row for row in reader]
    result = [x[csv_list[0].index('URLs')] for x in csv_list[1:]]
    # print(len(result))
    return result


def make_all_md_file(all_url_csv, stop_flag, md_remake_flag):
    no_display_list = ['https://www.sefure-do.com/friend-with-benefits/boys-love/',
                       'https://www.sefure-do.com/friend-with-benefits/idol/',
                       'https://www.sefure-do.com/friend-with-benefits/gal/',
                       'https://www.sefure-do.com/friend-with-benefits/glamorous-girl/',
                       'https://www.sefure-do.com/friend-with-benefits/flight-attendant/',
                       'https://www.sefure-do.com/friend-with-benefits/second-virgin/',
                       'https://www.sefure-do.com/friend-with-benefits/prostitution/',
                       'https://www.sefure-do.com/friend-with-benefits/lolita/',
                       'https://www.sefure-do.com/friend-with-benefits/childcare-worker/',
                       'https://www.sefure-do.com/friend-with-benefits/sales-lady/',
                       'https://www.sefure-do.com/friend-with-benefits/area-bbs/11-saitama/',
                       'https://www.sefure-do.com/friend-with-benefits/taking-children/',
                       'https://www.sefure-do.com/friend-with-benefits/legal-lolita/',
                       'https://www.sefure-do.com/friend-with-benefits/plump-and-ugly/',
                       'https://www.sefure-do.com/friend-with-benefits/erotic/',
                       'https://www.sefure-do.com/friend-with-benefits/amateur/',
                       'https://www.sefure-do.com/friend-with-benefits/area-bbs/08-ibaraki/',
                       'https://www.sefure-do.com/friend-with-benefits/area-bbs/02-aomori/']
    no_use_url = ['https://www.sefure-do.com/sitemap/']
    ng_tag = []
    t_list = get_all_url_list(all_url_csv)
    a_list = get_all_url_list('sfd/all-urls.csv')
    url_list = [x for x in t_list if x not in a_list]
    url_list = [x for x in url_list if x not in no_use_url and '?' not in x and '/top/' not in x]
    print(url_list)
    print(len(url_list))
    # return
    for page_url in url_list:
        tag_l = read_article_from_sfd_page(page_url, stop_flag, md_remake_flag)
        if tag_l:
            ng_tag.extend(tag_l)
    # print(list(set(ng_tag)))


def change_webp_image(img_path):
    im = Image.open(img_path)
    width, height = im.size
    webp_path = img_path.replace('.jpeg', '.webp').replace('.jpg', '.webp').replace('/art_images/', '/webp/')
    if width != 760:
        new_height = round(760 * height / width)
        im_resize = im.resize((760, new_height), Image.LANCZOS)
        im_resize.save(webp_path, 'webp')
        im_resize.save(img_path)
    else:
        im.save(webp_path, 'webp')


def change_webp_by_dir(target_dir):
    img_list = glob.glob(target_dir + '/**.**', recursive=True)
    # print(img_list)
    for im_path in img_list:
        change_webp_image(im_path)


def make_sq_webp_img(origin_path, move_dir):
    im = Image.open(origin_path)
    width, height = im.size
    if width == 150 and height == 150:
        webp_path = move_dir + re.sub(r'^.*/', '', origin_path).replace('.jpeg', '.webp').replace('.jpg', '.webp')
        im.save(webp_path, 'webp')
    else:
        print('error!! : {}'.format(origin_path))


def convert_all_sq_image_to_webp(target_dir, project_dir):
    with open(project_dir + '/pickle_pot/card_data.pkl', 'rb') as p:
        cl_dic = pickle.load(p)
    # print(cl_dic)
    img_list = [re.sub(r'^.*/', '', cl_dic[x]['img_path']) for x in cl_dic if cl_dic[x]['img_path']]
    img_list = [re.sub(r'-\d*x\d*-150x150\.', r'-150x150.', x).replace('.webp', '.jpg') for x in img_list]
    # print(len(img_list))
    # print(img_list)
    sq_img_list = glob.glob(target_dir + '/**/*-150x150.*', recursive=True)
    sq_name_list = [re.sub(r'^.*/', '', x) for x in sq_img_list]
    sq_name_dict = {re.sub(r'^.*/', '', x): x for x in sq_img_list}
    # print(sq_name_dict)
    # use_img_list = [x for x in img_list if x in sq_name_list]
    for img in img_list:
        make_sq_webp_img(sq_name_dict[img], 'sfd/html_files/images/sq/')
    # print(no_img_list)
    # print(len(no_img_list))
    # print(len(sq_img_list))


def all_jpg_to_webp(img_dir):
    img_files = glob.glob(img_dir + '/**.jpeg')
    print(img_files)
    img_num = 1
    for img_path in img_files:
        im = Image.open(img_path)
        width, height = im.size
        if width == 150 and height == 150:
            webp_path = img_dir + '/rdm_sq' + str(img_num).zfill(2) + '.webp'
            im.save(webp_path, 'webp')
            img_num += 1
        else:
            print('error!! : {}'.format(img_path))


def insert_pub_date():
    html_list = glob.glob('sfd/wp_html/**/**.html', recursive=True)
    for html_path in html_list:
        if 'sitemap' not in html_path:
            print(html_path)
            pub_date = ''
            html_p = pathlib.Path(html_path)
            html_p.open()
            h_str = html_p.read_text()
            meta_l = re.findall(r'<meta .*?>', h_str)
            for meta in meta_l:
                if 'property="article:published_time"' in meta:
                    pub_date = re.sub(r'^.+content="(.+?)\+\d\d:\d\d".*$', r'\1', meta)
                    print(pub_date)
            if pub_date:
                md_path = html_path.replace('/wp_html/', '/md_files/').replace('/index.html', '.md')
                m = pathlib.Path(md_path)
                m.open()
                md_str = m.read_text()
                if 'p::' not in md_str:
                    md_str = re.sub(r'(\nn::\d*?)\n', r'\1\np::' + pub_date + '\n', md_str)
                    print(md_str)
                    m.open(mode='w')
                    m.write_text(md_str)


def hide_no_use_page():
    no_use_list = ['friend-with-benefits/boys-love/',
                   'friend-with-benefits/idol/',
                   'friend-with-benefits/gal/',
                   'friend-with-benefits/glamorous-girl/',
                   'friend-with-benefits/flight-attendant/',
                   'friend-with-benefits/second-virgin/',
                   'friend-with-benefits/prostitution/',
                   'friend-with-benefits/lolita/',
                   'friend-with-benefits/childcare-worker/',
                   'friend-with-benefits/sales-lady/',
                   'friend-with-benefits/area-bbs/11-saitama/',
                   'friend-with-benefits/taking-children/',
                   'friend-with-benefits/legal-lolita/',
                   'friend-with-benefits/plump-and-ugly/',
                   'friend-with-benefits/erotic/',
                   'friend-with-benefits/amateur/',
                   'friend-with-benefits/area-bbs/08-ibaraki/',
                   'friend-with-benefits/area-bbs/02-aomori/']
    no_use_md = [re.sub(r'^.*/(.+)/', r'\1', x) + '.md' for x in no_use_list]
    print(no_use_md)
    # return
    md_list = glob.glob('sfd/md_files/**/**.md', recursive=True)
    for md_path in md_list:
        if 'sitemap' not in md_path:
            # print(md_path)
            md_p = pathlib.Path(md_path)
            md_p.open()
            m_str_p = md_p.read_text()
            m_str = m_str_p
            a_str_l = re.findall(r'\[.*?]\(.*?\)', m_str)
            for a_str in a_str_l:
                a_url = re.findall(r']\((.*?)\)', a_str)
                if a_url:
                    url = a_url[0]
                    for nu in no_use_md:
                        if nu in url:
                            print('no use : {} in {}'.format(nu, md_path))
                            a_text_l = re.findall(r'\[(.*?)]', a_str)
                            if a_text_l:
                                a_text = a_text_l[0]
                                ins_str = a_text + '<!--dead_link_' + a_str + '-->'
                                print(ins_str)
                                m_str = m_str.replace(a_str, ins_str)
                                # print(m_str)
                            break
            if m_str != m_str_p:
                md_p.open(mode='w')
                md_p.write_text(m_str)


def duplicate_pref_filter():
    pref_dict = {
        x: '[{}](area-bbs/{}-{}.md)'.format(words_dict.area_link_list[x]['ari'], str(x).zfill(2),
                                            words_dict.area_link_list[x]['alpha']) for x in words_dict.area_link_list}
    pref_list = [x for x in pref_dict]
    for rem in [2, 8]:
        pref_list.remove(rem)
    # print(pref_list)
    md_list = glob.glob('sfd/md_files/**/**.md', recursive=True)
    for md_path in md_list:
        if 'sitemap' not in md_path:
            md_p = pathlib.Path(md_path)
            md_p.open()
            m_str = md_p.read_text()
            m_str_e = m_str
            a_str_l = re.findall(r'\[[^]]*?]\([^)]*?\)\S{1,2}\[.*?]\(.*?\)', m_str)
            for a_str in a_str_l:
                a_inner_l = re.findall(r'(\[[^]]*?]\([^)]*?\))(\S{1,2})(\[.*?]\(.*?\))', a_str)
                if a_inner_l[0][0] == a_inner_l[0][2]:
                    print(md_path)
                    print(a_inner_l)
                    if 'area-bbs/' in a_inner_l[0][2]:
                        ch_id = random.choice(pref_list)
                        while str(ch_id).zfill(2) in a_inner_l[0][2] or str(ch_id).zfill(2) in md_path:
                            ch_id = random.choice(pref_list)
                        ins_str = a_inner_l[0][0] + a_inner_l[0][1] + pref_dict[ch_id]
                        print(md_path)
                        print(a_str)
                        print(ins_str)
                        print('')
                        m_str_e = m_str_e.replace(a_str, ins_str)
                    elif '/url/' in a_inner_l[0][2]:
                        if 'pcmax' not in a_inner_l[0][0]:
                            ins_s = '[PCMAX](../url/pcmax)'
                        else:
                            ins_s = '[ハッピーメール](../url/happymail)'
                        ins_str = a_inner_l[0][0] + a_inner_l[0][1] + ins_s
                        print(ins_str)
                        print('')
                        m_str_e = m_str_e.replace(a_str, ins_str)
            # if m_str_e != m_str:
            #     md_p.open(mode='w')
            #     md_p.write_text(m_str_e)


def correct_wrong_dead_link_comment():
    md_list = glob.glob('sfd/md_files/**/**.md', recursive=True)
    for md_path in md_list:
        if 'sitemap' not in md_path:
            md_p = pathlib.Path(md_path)
            md_p.open()
            m_str = md_p.read_text()
            m_str_e = m_str
            dl_l = re.findall(r'<!--dead_link_.+?<!--dead_link_\[.+?]\(.+?\)-->-->', m_str_e)
            if dl_l:
                print(md_path)
                # print(dl_l)
                for dl in dl_l:
                    print(dl)
                    u_count = dl.count('_')
                    k_count = dl.count('[')
                    e_count = dl.count('>')
                    # print(count)
                    if u_count == 4 and k_count == 1 and e_count == 2:
                        ed_str = re.sub(r'^<!--dead_link_.+?(<!--dead_link_\[.+?]\(.+?\)-->)-->$', r'\1', dl)
                        if '(/' in ed_str:
                            ed_str = ed_str.replace('(/', '(')
                        print(ed_str)
                        m_str_e = m_str_e.replace(dl, ed_str)
                    else:
                        print('error!!')
                print('')
                # if m_str_e != m_str:
                #     md_p.open(mode='w')
                #     md_p.write_text(m_str_e)


def correct_wrong_pref_link():
    pref_dict = {
        x: '[{}](area-bbs/{}-{}.md)'.format(words_dict.area_link_list[x]['ari'], str(x).zfill(2),
                                            words_dict.area_link_list[x]['alpha']) for x in words_dict.area_link_list}
    # pprint.pprint(pref_dict)
    # wrong_list = [[pref_dict[x].replace('area-bbs/0', 'area-bbs/'), pref_dict[x]] for x in pref_dict if x < 10]
    # print(wrong_list)
    wrong_list = [['[北海道](area-bbs/1-hokkaido.md)', '[北海道](area-bbs/01-hokkaido.md)'],
                  ['[青森県](area-bbs/2-aomori.md)', '青森県<!--dead_link_[青森県](area-bbs/02-aomori.md)-->'],
                  ['[岩手県](area-bbs/3-iwate.md)', '[岩手県](area-bbs/03-iwate.md)'],
                  ['[宮城県](area-bbs/4-miyagi.md)', '[宮城県](area-bbs/04-miyagi.md)'],
                  ['[秋田県](area-bbs/5-akita.md)', '[秋田県](area-bbs/05-akita.md)'],
                  ['[山形県](area-bbs/6-yamagata.md)', '[山形県](area-bbs/06-yamagata.md)'],
                  ['[福島県](area-bbs/7-fukushima.md)', '[福島県](area-bbs/07-fukushima.md)'],
                  ['[茨城県](area-bbs/8-ibaraki.md)', '茨城県<!--dead_link_[茨城県](area-bbs/08-ibaraki.md)-->'],
                  ['[栃木県](area-bbs/9-tochigi.md)', '[栃木県](area-bbs/09-tochigi.md)']]
    md_list = glob.glob('sfd/md_files/**/**.md', recursive=True)
    for md_path in md_list:
        if 'sitemap' not in md_path:
            md_p = pathlib.Path(md_path)
            md_p.open()
            m_str = md_p.read_text()
            m_str_e = m_str
            for wa in wrong_list:
                if wa[0] in m_str_e:
                    m_str_e = m_str_e.replace(wa[0], wa[1])
            if m_str_e != m_str:
                print(m_str_e)
                print('\n')
                # md_p.open(mode='w')
                # md_p.write_text(m_str_e)


if __name__ == '__main__':
    correct_wrong_pref_link()
    # hide_no_use_page()
    # duplicate_pref_filter()
    # insert_pub_date()
    # make_all_md_file('sfd/true-all.csv', stop_flag=False, md_remake_flag=False)
    # change_webp_image('sfd/md_files/images/art_images/woman_in_bed40.jpg')
    # change_webp_by_dir('sfd/html_files/images/art_images')
    # convert_all_sq_image_to_webp('/Users/tnakatake/会社データ/change_server20220324/wp_down/sefuredo/wp-content/uploads',
    #                              'sfd')
    # all_jpg_to_webp('/Users/tnakatake/images/sex/sqr')
    # read_article_from_sfd_page('https://www.sefure-do.com/friend-with-benefits/',
    #                            stop_flag=False, md_remake_flag=True)
    # pprint.pprint(get_all_url_list('sfd/all-urls.csv'))
