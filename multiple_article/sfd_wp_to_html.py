import re
import urllib.request
import os
from PIL import Image
from bs4 import BeautifulSoup
import requests

ok_div = ['<div class="maruck">', '<div class="fr2">', '<div class="alt_img_t">', '<div class="icon">',
          '<div class="fl1">', '<div class="lm_b lm_2">', '<div class="rm_b rm_2">']


def read_article_from_sfd_page(page_url):
    down_files = []
    # スクレイピング対象の URL にリクエストを送り HTML を取得する
    print('scrape: ' + page_url)
    res = requests.get(page_url)
    # レスポンスの HTML から BeautifulSoup オブジェクトを作る
    soup = BeautifulSoup(res.text, 'html.parser')
    title_text = soup.find('title').get_text().replace(' - セフレ道', '')
    print(title_text)
    md = soup.find('time', {'class': 'updated'})
    if md:
        mod_time = md.get('datetime')
    else:
        mod_time = ''
    # print(mod_time)
    main_txt = soup.find_all('div', {'class': 'mainbox'})[0]
    main_str = str(main_txt)
    main_str = re.sub(r'^.*<div class="entry-content">', '', main_str)
    main_str = re.sub(r'<div class="adbox">.*$', '', main_str)
    main_str = re.sub(r'</div></div>$', '', main_str)
    main_str = re.sub(r'<noscript.*?</noscript>', '', main_str)
    main_str = re.sub(r'<span class="huto".*?>(.+?)</span>', r'<strong>\1</strong>', main_str)
    main_str = main_str.replace('></img>', '/>')
    main_str = main_str.replace('<br/> ', '<br/>')
    a_list = re.findall(r'<a.*?>.*?</a>', main_str)
    for a_str in a_list:
        if 'class="st-cardlink"' in a_str:
            a_url = re.findall(r'href="https://www.sefure-do.com/(.*?)"', a_str)[0]
            main_str = main_str.replace(a_str, '<a href="{}" class="ar-card">card_link</a>'.format(a_url))

    d_list = re.findall(r'<div class="kanren st-cardbox"><dl.*?</dl></div>', main_str)
    for d_str in d_list:
        # print(d_str)
        if 'alt="セフレの作り方"' in d_str:
            main_str = main_str.replace(d_str, '<a href="friend-with-benefits/index.html" class="sf-card">セフレの作り方</a>')
    #  replace big image
    img_l = re.findall(r'<img .+?/>', main_str)
    for img_str in img_l:
        # print(img_str)
        alt_str = re.findall(r'alt="(.*?)"', img_str)
        img_url = re.findall(r'data-src="(.*?)"', img_str)
        if 'aligncenter' in img_str and img_url:
            # print(img_url)
            img_path, img_size = image_download(img_url[0])
            if alt_str:
                alt_data = alt_str[0]
            else:
                alt_data = ''
            ins_str = '<div class="alt_img_t"><img src="../{}" alt="{}" width="{}" height="{}" />' \
                      '</div>'.format(img_path, alt_data, img_size[0], img_size[1])
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
            ins_kw = '<div class="fr2"><div class="icon"><div class="rm_b rm_2"></div></div>{}</div>'.format(kw_text)
        else:
            ins_kw = '<div class="fl1"><div class="icon"><div class="lm_b lm_2"></div></div>{}</div>'.format(kw_text)
        main_str = main_str.replace(kw_str, ins_kw)

    main_str = re.sub(r'<p><div class="alt_img_t">(.+?)</div></p>', r'<div class="alt_img_t">\1</div>', main_str)
    print(main_str)
    div_list = re.findall(r'<div .*?>', main_str)
    # print(set(div_list))
    for d_row in div_list:
        if d_row not in ok_div:
            print('error!! : new div => {}'.format(d_row))


def image_download(img_url):
    save_path = 'sfd/move/images/art_images/' + re.sub(r'^.+/', '', img_url)
    if not os.path.exists(save_path):
        print('download: {}'.format(save_path))
        urllib.request.urlretrieve(img_url, save_path)
    im = Image.open(save_path)
    return save_path.replace('sfd/move/', ''), im.size


if __name__ == '__main__':
    read_article_from_sfd_page('https://www.sefure-do.com/friend-with-benefits/serious-woman/')
