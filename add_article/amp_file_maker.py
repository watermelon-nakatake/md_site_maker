# -*- coding: utf-8 -*-
import re
import os
import shutil
from upload import file_upload
import new_from_md
from PIL import Image


def relation_file_upload(amp_str):
    src_list = re.findall('img src="(.+?).jpg"', amp_str)
    copy_file = []
    if src_list:
        for src_str in src_list:
            if '/images/' in src_str:
                if not os.path.isfile(src_str + '.jpg'):
                    file_name = re.sub(r'^.*?/images/', '/images/', src_str)
                    if os.path.isfile('reibun/html_files/pc' + file_name):
                        shutil.copyfile('reibun/html_files/pc' + file_name, 'reibun/html_files/amp' + file_name)
                        copy_file.append('reibun/html_files/amp' + file_name)
    # reibun_upload.ftp_upload(copy_file)


def a_tag_filter(main_str):
    match_list = re.findall(r'<a href=.+?>', main_str)
    if match_list:
        for a_str in match_list:
            element_order = []
            inner_str = a_str.replace('<a ', '')
            inner_str = inner_str.replace('">', '')
            a_element_list = inner_str.split('" ')
            element_words = ['href=', 'class=', 'onclick=', 'rel=']
            for e_word in element_words:
                for a_element in a_element_list:
                    if e_word == 'onclick=':
                        pass
                    elif e_word in a_element:
                        element_order.append(a_element + '"')
            if '/ds/' in a_str:
                if 'rel=' not in a_str:
                    element_order.append('rel="sponsored"')
            jointed_a = '<a ' + ' '.join(element_order) + '>'
            main_str = main_str.replace(a_str, jointed_a)
    return main_str


def g_tag_insert(content_str):
    insert_str = ''
    g_tag_list = ['waku-otherb', 'mintj-otherb', 'happy-otherb', 'max1-otherb', 'merupa-otherb', 'iku-otherb']
    for i in range(len(g_tag_list)):
        if g_tag_list[i] in content_str:
            event_label = g_tag_list[i].replace('-', '-amp')
            insert_str += ',"trackAncorClicks' + str(i + 1) + '":{"on":"click","selector":".' + g_tag_list[i] \
                          + '","request":"event","vars":{"eventCategory":"access","eventAction":"click","eventLabel":"' \
                          + event_label + '"}}'
    return insert_str


def tab_and_line_feed_remover(long_str):
    str_list = long_str.splitlines()
    result = ''
    for x in str_list:
        y = x.strip()
        result += y
    result = result.replace('spanclass', 'span class')
    result = result.replace('"itemtype', '" itemtype')
    result = result.replace('"datetime=', '" datetime=')
    result = result.replace('imgsrc', 'img src')
    result = result.replace('spanitemprop', 'span itemprop')
    result = result.replace('spanclass', 'span class')
    result = result.replace('ahref', 'a href')
    result = result.replace('timeitemprop', 'time itemprop')
    result = result.replace('\\t', '')
    return result


def css_insert(long_str):
    css_str = ''
    if 'lm_b' in long_str:
        css_str += '.lm_b{width:4pc;height:77px;background-repeat:no-repeat;background-image:' \
                   'url(../images/common/icon_ml_m.png)}.lm_1{background-position:0 0}' \
                   '.lm_2{background-position:-4pc 0}.lm_3{background-position:-8pc 0}' \
                   '.lm_4{background-position:0 -77px}.lm_5{background-position:-4pc -77px}' \
                   '.lm_6{background-position:-8pc -77px}.fl1{width:67%;position:relative;' \
                   'padding:20px 5%;border-radius:10px;background-color:#dcdcdc;margin:40px 0 40px 70px}' \
                   '.fl1 .icon{position:absolute;left:-70px;top:0}.fl1:before{content:'';position:absolute;' \
                   'display:block;width:0;height:0;left:-15px;top:20px;border-right:15px solid #dcdcdc;' \
                   'border-top:15px solid transparent;border-bottom:15px solid transparent}'
    if 'rm_b' in long_str:
        css_str += '.rm_b{width:4pc;height:77px;background-repeat:no-repeat;' \
                   'background-image:url(../images/common/icon_mr_m.png)}.rm_1{background-position:0 0}' \
                   '.rm_2{background-position:-4pc 0}.rm_3{background-position:-8pc 0}' \
                   '.rm_4{background-position:0 -77px}.rm_5{background-position:-4pc -77px}.' \
                   'rm_6{background-position:-8pc -77px}.fr2{width:67%;position:relative;padding:20px 5%;' \
                   'border-radius:10px;background-color:#7fffd4;margin:40px 70px 40px 3%}' \
                   '.fr2 .icon{position:absolute;right:-70px;top:0}.fr2:before{content:'';position:absolute;' \
                   'display:block;width:0;height:0;right:-15px;top:20px;border-left:15px solid #7fffd4;' \
                   'border-top:15px solid transparent;border-bottom:15px solid transparent}'
    if 'rw_b' in long_str:
        css_str += '.rw_b{width:4pc;height:64px;background-repeat:no-repeat}.rw_1{background-image:' \
                   'url(../images/common/icon_wr_1_m.png)}.rw_2{background-image:url(../images/common/icon_wr_2_m.png)}' \
                   '.fr2{width:67%;position:relative;padding:20px 5%;' \
                   'border-radius:10px;background-color:#7fffd4;margin:40px 70px 40px 3%}' \
                   '.fr2 .icon{position:absolute;right:-70px;top:0}.fr2:before{content:'';position:absolute;' \
                   'display:block;width:0;height:0;right:-15px;top:20px;border-left:15px solid #7fffd4;' \
                   'border-top:15px solid transparent;border-bottom:15px solid transparent}'
    long_str = long_str.replace('</style><style amp-boilerplate>', css_str + '</style><style amp-boilerplate>')
    return long_str


def make_amp_top_page():
    with open('../reibun/html_files/index.html', "r", encoding='utf-8') as f:
        pc_top = f.read()
    with open('../reibun/html_files/amp/index.html', "r", encoding='utf-8') as g:
        amp_top = g.read()
    new_str = re.findall(r'<h2>主な更新履歴</h2>.+?</article>', pc_top)[0]
    new_str = new_str.replace('"pc/', '"')
    amp_top = re.sub(r'<h2>主な更新履歴</h2>.+?</article>', new_str, amp_top)
    mod_date = re.findall(r'<time itemprop="dateModified" datetime=".+?">(.+?)</time>', pc_top)[0]
    amp_top = re.sub(r'<!--mod-->.+?<!--e/mod-->', '<!--mod-->{}<!--e/mod-->'.format(mod_date), amp_top)
    with open('../reibun/html_files/amp/index.html', "w", encoding='utf-8') as h:
        h.write(amp_top)


def amp_maker(pc_path_list, pd):
    up_list = []
    with open('reibun/html_files/amp/template/amp_tmp_2.html', "r", encoding='utf-8') as g:
        tmp_str = g.read()
    for pc_path in pc_path_list:
        if 'reibun/html_files/index.html' == pc_path:
            make_amp_top_page()
            continue
        if '.html' in pc_path and '/sitepage/' not in pc_path and '/reviews/' not in pc_path:
            with open(pc_path, "r", encoding='utf-8') as f:
                print('amp maker: ' + pc_path)
                str_x = f.read()
                str_x = tab_and_line_feed_remover(str_x)
                title = re.findall(r'<h1 itemprop="headline alternativeHeadline name">(.*?)</h1>', str_x)[0]
                content = re.findall(r'</time></div>(.*?)</article>', str_x)[0]
                """top_images = re.findall(r'<div class="alt_img_t">.+?</div>', content)
                if top_images:
                    for top_img in top_images:
                        insert_str = top_img.replace('.jpg" alt="',
                                                     '.jpg" width="759" height="506" layout="responsive" alt="')
                        insert_str = insert_str.replace('<img', '<amp-img')
                        insert_str = insert_str.replace('"></div>', '"></amp-img></div>')
                        content = content.replace(top_img, insert_str)
                        img_path = re.findall(r'src="(.+?)"', top_img)
                        if img_path:
                            tmp_str = tmp_str.replace(
                                '"url": "https://www.demr.jp/pc/images/eyec.jpg","height": 464,"width": 700',
                                '"url": "' + str(img_path[0]) + '","height": 506,"width": 759')"""
                k_str = re.findall(r'<section><div class="kanren">.+$', content)
                if k_str:
                    kr_str = k_str[0].replace('<section>', '').replace('</section>', '')
                else:
                    kr_str = ''
                content = re.sub(r'<div class="only_mob teisite">.+$', '', content)
                content = re.sub(r'<section><div class="kanren">.+$', '', content)
                content = a_tag_filter(content)
                content = content.replace(' target="_blank"', '')
                content = re.sub(r'<img(.+?)>', r'<amp-img\1></amp-img>', content)
                content = amp_image_filter(content, pd)
                content = re.sub(r'<a href="\.\./ds/(.+?)" class="(.+?)" onclick="gtag\(.+?}\);" rel="nofollow">',
                                 r'<a href="../ds/\1" class="\2" rel="sponsored">', content)
                pub_date = re.findall(r'itemprop="datePublished" datetime="(.*?)">', str_x)[0]
                mod_date = re.findall(r'itemprop="dateModified" datetime="(.*?)">', str_x)[0]
                description = re.findall(r'<meta name="description" content="(.*?)">', str_x)[0]
                h1_str = re.findall(r'<h1 itemprop="headline alternativeHeadline name">(.*?)</h1>', str_x)[0]
                date_data = re.findall(r'(\d{4})-(\d{2})-(\d{2})', str_x)
                new_date = date_data[0][0] + '年' + date_data[0][1] + '月' + date_data[0][2] + '日'

                amp_data = tmp_str.replace('<!--title-->', title)
                amp_data = amp_data.replace('<!--h1-->', h1_str)
                amp_data = amp_data.replace('<!--content-->', content)
                amp_data = amp_data.replace('<!--pub-date-->', str(pub_date))
                amp_data = amp_data.replace('<!--mod-date-->', str(mod_date))
                amp_data = amp_data.replace('<!--description-->', description)
                amp_data = amp_data.replace('<!--i-kanren-->', kr_str)
                if pc_path == 'reibun/html_files/index.html':
                    amp_path = '../reibun/html_files/amp/index.html'
                else:
                    amp_path = pc_path.replace('/pc/', '/amp/')
                amp_data = amp_data.replace('<!--path-->', amp_path.replace('reibun/html_files/amp/', ''))
                amp_data = amp_data.replace('<!--new-date-->', new_date)
                amp_data = amp_data.replace('<amp-img class="app_bn1" src="../images/common/app_bn_f.png" ' +
                                            'alt="出会い系メール例文アプリ">',
                                            '<amp-img class="app_bn1" src="../images/common/app_bn_f.png" width="336" ' +
                                            'height="280"  layout="responsive" alt="出会い系メール例文アプリ">')
                side_bar_list = [['人気記事', 'pop-a'], ['重要記事', 'imp-a'], ['最近の更新記事', 'new-a']]
                for x in side_bar_list:
                    match_str_list = re.findall(r'<div class="sbh">' + x[0] + r'</div>.+?</ul>', str_x)
                    if match_str_list:
                        amp_data = amp_data.replace('<!--' + x[1] + '-->', match_str_list[0])
                relative_art = re.findall(r'<!--otherart-->(.+?)<!--otherart/end-->', str_x)
                if relative_art:
                    amp_data = amp_data.replace('<!--other-a-->', match_str_list[0])
                gtag_i = g_tag_insert(content)
                if gtag_i:
                    amp_data = amp_data.replace('{"trackPageview": {"on": "visible","request": "pageview"}}}',
                                                '{"trackPageview": {"on": "visible","request": "pageview"}' +
                                                gtag_i + '}}')
                if pc_path == 'reibun/html_files/index.html':
                    amp_data = amp_data.replace('"pc/', '"')
                    amp_data = amp_data.replace('demr.jp/index.html', 'demr.jp/')
                if '<span class="pc_none">' in amp_data:
                    amp_data = re.sub(r'<span class="pc_none">(.+?)</span>', r'\1', amp_data)
                    amp_data = re.sub(r'<span class="mob_none">.+?</span>', '', amp_data)
                html_str = re.findall(r'(<body.*?>[\s\S]+?</body>)', amp_data)[0]
                css_str = re.findall(r'<style amp-custom>([\s\S]+?)</style>', amp_data)[0]
                new_css = new_from_md.css_str_optimize(html_str, css_str)
                amp_data = amp_data.replace(css_str, new_css)
                main_image = re.findall(r'<img itemprop="image" src="(.+?)"', str_x)[0]
                if 'images/eyec.jpg' not in main_image:
                    mi_w, mi_h = search_image_size(main_image, pd)
                    main_image = main_image.replace('../images/', '/images/').replace('pc/image/', '/images/')
                    amp_data = re.sub(r'"image":{"@type":.+</body>',
                                      '"image":{"@type":"ImageObject","url":"https://www.demr.jp/pc/' + main_image +
                                      '","height":' + str(mi_h) + ',"width":' + str(mi_w) + '}}</script></body>',
                                      amp_data)
                amp_data = amp_data.replace('<div id="other-a" class="as_li"><!--other-a--></div>', '')
                amp_data = amp_data.replace('mailform/review.html', 'mailform/')
            with open(amp_path, "w") as h:
                h.write(amp_data)
            up_list.append(amp_path)
            # relation_file_upload(amp_data)
    return up_list


def add_amp_file(pc_path, pd):
    file_name = pc_path.replace('reibun/html_files/pc/', '')
    amp_maker(['reibun/html_files/pc/' + file_name], pd)
    file_upload.ftp_upload(['reibun/html_files/amp/' + file_name], pd)


def search_image_size(img_str, pd):
    # print(img_str)
    if '../images/' in img_str:
        img_path = img_str.replace('../images/', 'reibun/html_files/pc/images/')
    else:
        img_path = re.sub(r'^images/', pd['project_dir'] + '/html_files/' + pd['main_dir'] + 'images/', img_str)
    im = Image.open(img_path)
    w, h = im.size
    return w, h


def amp_image_filter(long_str, pd):
    img_str_l = re.findall(r'<amp-img.+?>', long_str)
    if img_str_l:
        for img_str in img_str_l:
            if '/>' in img_str:
                img_str_r = img_str.replace('/>', '>')
            else:
                img_str_r = img_str
            if 'width=' not in img_str or 'height=' not in img_str:
                # print(long_str)
                img_path_str = re.findall(r'src="(.+?)"', img_str)[0]
                w, h = search_image_size(img_path_str, pd)
                if 'width=' not in img_str:
                    img_str_r = img_str_r.replace('>', ' width="{}">'.format(str(w)))
                if 'height=' not in img_str:
                    img_str_r = img_str_r.replace('>', ' height="{}">'.format(str(h)))
            if 'layout=' not in img_str:
                img_str_r = img_str_r.replace('>', ' layout="responsive">')
                img_str_r = img_str_r.replace('  ', ' ')
            long_str = long_str.replace(img_str, img_str_r)
    return long_str


def img_insert_size(file_path, pd):
    with open(file_path, 'r', encoding='utf-8') as f:
        long_str = f.read()
        long_str = tab_and_line_feed_remover(long_str)
        long_str = amp_image_filter(long_str, pd)
        with open(file_path, 'w', encoding='utf-8') as g:
            g.write(long_str)


def all_amp_change_and_upload(pd):
    up_dir = ['caption/', 'majime/', 'policy/', 'qa/', 'site/']
    up_files = []
    for directory in up_dir:
        dir_str = 'reibun/html_files/pc/' + directory
        files = [dir_str + x for x in os.listdir(dir_str) if '_test' not in x and '_copy' not in x]
        up_files.extend(files)
    # print(up_files)
    amp_maker(up_files, pd)
    file_upload.ftp_upload([y.replace('/pc/', '/amp/') for y in up_files], pd)


# if __name__ == '__main__':
#     # img_insert_size('reibun/html_files/amp/index.html')
#     # new_file = 'majime/mail-applicaton.html'
#     # amp_maker(['reibun/html_files/pc/majime/kakikata_t.html'])
#     # reibun_upload.ftp_upload(['reibun/html_files/pc/' + new_file])
#     # reibun_upload.ftp_upload(['reibun/html_files/amp/' + new_file])
#     # amp_maker(['reibun/html_files/pc/sitepage/index.html'], )
#     # all_amp_change_and_upload()
#     print('amp')
