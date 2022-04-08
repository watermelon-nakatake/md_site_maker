import pprint
import re
import urllib.request
import os
import csv
from PIL import Image
from bs4 import BeautifulSoup
import requests

ok_div = ['<div class="maruck">', '<div class="fr2">', '<div class="alt_img_t">', '<div class="icon">',
          '<div class="fl1">', '<div class="lm_b lm_2">', '<div class="rm_b rm_2">']
ds_list = ['ワクワクメール', 'PCMAX', 'ハッピーメール', 'Jメール']


def read_article_from_sfd_page(page_url, stop_flag, md_remake_flag):
    tag_l = []
    html_path = re.sub(r'https://www\.sefure-do\.com/(.*)/', r'sfd/wp_html/\1/index.html', page_url)
    md_path = html_path.replace('/wp_html/', '/new_md/').replace('/index.html', '.md')
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
        main_txt = soup.find_all('div', {'class': 'mainbox'})[0]
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
            if stop_flag:
                return
        md_head = 't::{}\nd::{}\nn::{}\nm::{}'.format(title_text, des_str, 1, mod_time.replace('+0900', ''))
        md_f = md_head + '\n\n' + md_str
        # print(md_f)
        md_path = html_path.replace('/wp_html/', '/new_md/').replace('/index.html', '.md')
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
                ins_url = re.sub(r'^.+?sefure-do\.com', '', a_url)
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
    save_dir = 'sfd/new_md/'
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
    ng_tag = []
    url_list = get_all_url_list(all_url_csv)
    for page_url in url_list:
        tag_l = read_article_from_sfd_page(page_url, stop_flag, md_remake_flag)
        if tag_l:
            ng_tag.extend(tag_l)
    print(list(set(ng_tag)))


def change_webp_image(img_path):
    im = Image.open(img_path)
    im.save(img_path.replace('.jpeg', '.webp').replace('.jpg', '.webp'), 'webp')


if __name__ == '__main__':
    make_all_md_file('sfd/all-urls.csv', stop_flag=True, md_remake_flag=False)
    # change_webp_image('sfd/new_md/images/art_images/woman_in_bed40.jpg')
    # read_article_from_sfd_page('https://www.sefure-do.com/friend-with-benefits/area-bbs/24-mie/',
    #                            stop_flag=False, md_remake_flag=True)
    # pprint.pprint(get_all_url_list('sfd/all-urls.csv'))
