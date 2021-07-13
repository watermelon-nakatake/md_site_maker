import re

project_dir = 'reibun'

site_name = '出会い系メール例文集'
side_bar_list = {'important': [48, 21, 13, 66, 76, 112, 34, 96, 25],
                 'pop': [117, 23, 130, 67, 64, 38, 107, 19, 73]}
category_name = {'policy': ['ポリシー', 'index.html'], 'caption': ['出会い系の予備知識', 'index.html'],
                 'profile': ['プロフィール例文', 'kakikata_p.html'], 'qa': ['出会い系Ｑ＆Ａ', 'index.html'],
                 'site': ['出会い系サイト情報', 'index.html'], 'post': ['掲示板例文', 'kakikata_t.html'],
                 'f_mail': ['ファーストメール例文', 'kakikata_f.html'], 's_mail': ['２通目以降のメール例文', 'majime.html'],
                 'date': ['デートに誘うメール例文', 'date.html'], 'how_to': ['出会い系攻略法', 'kakikata_d.html'],
                 'majime': '出会いメール例文'}
category_data = {'policy': ['ポリシー', 'index.html', 1], 's_mail': ['２通目以降のメール例文', 'majime.html', 41],
                 'caption': ['出会い系の予備知識', 'index.html', 6], 'profile': ['プロフィール例文', 'kakikata_p.html', 17],
                 'qa': ['出会い系Ｑ＆Ａ', 'index.html', 114], 'site': ['出会い系サイト情報', 'index.html', 122],
                 'post': ['掲示板例文', 'kakikata_t.html', 74], 'f_mail': ['ファーストメール例文', 'kakikata_f.html', 107],
                 'date': ['デートに誘うメール例文', 'date.html', 102], 'how_to': ['出会い系攻略法', 'kakikata_d.html', 39],
                 'ap_mail': ['メール例文アプリ情報', 'mail-applicaton.html', 92],
                 'majime': ['出会い系メール例文', 'index.html', 32], 'sitepage': ['出会い系サイト', 'index.html', 122]}
directory_name = {'policy': 'ポリシー', 'caption': '出会い系の予備知識', 'majime': '出会いメール例文',
                  'qa': '出会い系Ｑ＆Ａ', 'site': '出会い系サイト情報', 'sitepage': '出会い系サイト紹介'}
site_shift_list = [0, 1, 2]

add_files = ['reibun/html_files/index.html', 'reibun/html_files/amp/index.html',
             'reibun/html_files/pc/css/base13.css', 'reibun/html_files/pc/css/pc13.css',
             'reibun/html_files/pc/css/phone13.css', 'reibun/html_files/p_sitemap.xml']

main_dir = 'pc/'
article_image_dir = 'art_images'
amp_flag = True
default_img = 'demr_mgirl_1200x630.jpg'
h_sitemap_path = 'reibun/html_files/pc/policy/sitemap.html'
domain_str = 'demr.jp'
ignore_files = ['reibun/html_files/google3d7d16f68a5d3b38.html', 'reibun/html_files/y_key_e2722b15d0cec302.html']
upload_data = {'host_name': 'blackrhino1.sakura.ne.jp', 'password_str': 'k2u5n47ku6', 'user_name': 'blackrhino1',
               'upload_dir': 'reibun'}
sc_url = {'ワクワクメール': 'sitepage/wakuwakumail.html', 'PCMAX': 'sitepage/pcmax.html',
          '口コミランキング': 'sitepage/ranking.html', '口コミ評価ランキング': 'sitepage/ranking.html',
          '出会い系口コミランキング': 'sitepage/ranking.html', 'ハッピーメール': 'sitepage/happymail.html',
          'Jメール': 'sitepage/mintj.html', '出会い系口コミ評価ランキング': 'sitepage/ranking.html',
          '出会い系サイト口コミランキング': 'sitepage/ranking.html'}
eyec_img = {'img_path': 'eyec.jpg', 'height': '464', 'width': '700'}
aff_dir = {'dir': 'sitepage'}

info_dict = {'project_dir': project_dir, 'site_name': site_name, 'side_bar_list': side_bar_list,
             'category_name': category_name, 'category_data': category_data,
             'directory_name': directory_name, 'site_shift_list': site_shift_list, 'add_files': add_files,
             'main_dir': main_dir, 'ar_img_dir': article_image_dir, 'amp_flag': amp_flag,
             'default_img': default_img, 'h_sitemap_path': h_sitemap_path, 'domain_str': domain_str,
             'ignore_files': ignore_files, 'upload_data': upload_data, 'sc_url': sc_url, 'eyec_img': eyec_img,
             'aff_dir': aff_dir}


def reibun_additional_replace_in_md(md_str):
    md_str = md_str.replace(r'%app_b%', '<div class="center"><a href="../../app/"><img class="app_bn1" '
                                        'src="../images/common/app_bn_f.png" alt="出会い系メール例文アプリ">'
                                        '</a></div>')
    return md_str


def reibun_insert_site_banner(long_str):
    b_dict = {'hm': '<a href="../ds/happymail/" target="_blank" rel="nofollow" class="happy-otherb"'
                    ' onclick="gtag(' + "'event', 'click', {'event_category': 'access','event_label': 'happy-otherb'}" +
                    ');"><img src="../images/hm234x60_1214.gif" width="234" height="60" alt="ハッピーメール"></a>',
              'mt': '<a href="../ds/mintj/" target="_blank" class="mintj-otherb" onclick="gtag' +
                    "('event', 'click', {'event_category': 'access','event_label': 'mintj-otherb'})" +
                    ';"><img width="234" height="60" alt="Jメール" src="../images/mt234x60blue.gif"></a>',
              'hm2': '<a href="../ds/happymail2/" target="_blank" rel="nofollow" '
                     'class="happy2-otherb" onclick="gtag(' +
                     "'event', 'click', {'event_category': 'access','event_label': 'happy2-otherb'})" +
                     ';"><img src="../images/happymail50p200x150.gif" width="200" height="150" alt="ハッピーメール"></a>',
              'max': '<a href="../ds/pcmax" target="_blank" rel="nofollow" class="max1-otherb" onclick="gtag' +
                     "('event', 'click', {'event_category': 'access','event_label': 'max1-otherb'})" +
                     ';"><img width="240" height="90" src="../images/pm240x90_02.gif" alt="PCMAX"></a>',
              'wk': '<a href="../ds/550909" target="_blank" rel="nofollow" class="waku-otherb"' +
                    ' onclick="gtag' + "('event', 'click', {'event_category': 'access','event_label': 'waku-otherb'})"
                    + ';"><img width="236" height="80" src="../images/wk236-80_2.png" alt="ワクワクメール"></a>'
              }
    for site_code in b_dict:
        long_str = long_str.replace('%bn_' + site_code + '%', '<div class="center">' + b_dict[site_code] + '</div>')
    return long_str


def reibun_icon_filter(long_str):
    long_str = long_str.replace('%l_normal%', '%lm_1%')
    long_str = long_str.replace('%l_!%', '%lm_2%')
    long_str = long_str.replace('%l_?%', '%lm_5%')
    long_str = long_str.replace('%l_good%', '%lm_6%')
    long_str = long_str.replace('%l_angry%', '%lm_4%')
    long_str = long_str.replace('%l_palm%', '%lm_3%')
    long_str = long_str.replace('%l_normal%', '%lm_1%')
    long_str = long_str.replace('%l_!', '%lm_2%')
    long_str = long_str.replace('%l_?', '%lm_5%')
    long_str = long_str.replace('%l_good', '%lm_6%')
    long_str = long_str.replace('%l_angry', '%lm_4%')
    long_str = long_str.replace('%l_palm', '%lm_3%')
    long_str = long_str.replace('%l_normal', '%lm_1%')

    long_str = long_str.replace('%r_normal%', '%rm_1%')
    long_str = long_str.replace('%r_!%', '%rm_3%')
    long_str = long_str.replace('%r_?%', '%rm_2%')
    long_str = long_str.replace('%r_good%', '%rm_4%')
    long_str = long_str.replace('%r_angry%', '%rm_5%')
    long_str = long_str.replace('%r_palm%', '%rm_6%')
    long_str = long_str.replace('%r_normal', '%rm_1%')
    long_str = long_str.replace('%r_!', '%rm_3%')
    long_str = long_str.replace('%r_?', '%rm_2%')
    long_str = long_str.replace('%r_good', '%rm_4%')
    long_str = long_str.replace('%r_angry', '%rm_5%')
    long_str = long_str.replace('%r_palm', '%rm_6%')
    long_str = long_str.replace('%rw_?%', '%rw_1%')
    long_str = long_str.replace('%rw_!%', '%rw_2%')
    long_str = long_str.replace('%rw_?', '%rw_1%')
    long_str = long_str.replace('%rw_!', '%rw_2%')
    if '%r_' in long_str or '%l_' in long_str:
        print('There is wrong icon tag !')
        return
    long_str = re.sub(r'%rm_(\d)%([\s\S]+?)\n\n', r'<!--rm_\1-->\n\n\2\n\n<!--e/rm-->\n\n\n', long_str)
    long_str = re.sub(r'%lm_(\d)%([\s\S]+?)\n\n',
                      r'<!--lm_\1-->\n\n\2\n\n<!--e/lm-->\n\n\n', long_str)
    long_str = re.sub(r'%rw_(\d)%([\s\S]+?)\n\n',
                      r'<!--rw_\1-->\n\n\2\n\n<!--e/rw-->\n\n\n', long_str)
    return long_str


def reibun_search_category(directory, file_name):
    if directory != 'majime':
        category = directory
    else:
        if 'm0' in file_name:
            category = 'post'
        elif 'mp_' in file_name:
            category = 'profile'
        elif 'm1' in file_name:
            category = 'f_mail'
        elif 'm2' in file_name:
            category = 's_mail'
        elif 'm3' in file_name:
            category = 'date'
        elif 'm4' in file_name:
            category = 'how_to'
        elif 't0_' in file_name:
            category = 'post'
        else:
            category = 'majime'
    return category


def reibun_change_category_class(new_str, category):
    if category != 'majime':
        new_str = new_str.replace('<!--sb-category-->', '<div class="leftnav"><div class="sbh cat-i"></div>'
                                                        '<ul></ul></div>')
    else:
        new_str = new_str.replace('<!--sb-category-->', '')
    return new_str


def reibun_insert_additional_str(new_str):
    new_str = new_str.replace('</section><section><div class="kanren">',
                              '</section><div class="only_mob teisite"><div class="sbh">出会系口コミランキング</div>'
                              '<ul class="slu"><li><a href="../sitepage/wakuwakumail.html"><div class="sli">'
                              '<span class="sl_num">1</span><img src="../images/common/wkwk_sq.gif" '
                              'alt="ワクワクメール"><div class="slr"><span class="slsn">ワクワクメール</span>'
                              '<span class="slsd">利用者が多くコスパ抜群</span></div></div></a></li><li><a href="../sitepage/happymail.html"><div class="sli">'
                              '<span class="sl_num">2</span><img src="../images/common/hm_sq.png" '
                              'alt="ハッピーメール"><div class="slr"><span class="slsn">ハッピーメール</span>'
                              '<span class="slsd">真面目な出会いに強い</span></div></div></a></li><li>'
                              '<a href="../sitepage/pcmax.html"><div class="sli"><span class="sl_num">3</span>'
                              '<img src="../images/common/max_sq.gif" alt="PCMAX"><div class="slr">'
                              '<span class="slsn">PCMAX</span><span class="slsd">初心者でも使いやすい</span></div>'
                              '</div></a></li></ul>'
                              '<div class="center"><a href="../sitepage/ranking.html">口コミ評価ランキング</a>'
                              '</div></div><section><div class="kanren">')
    new_str = new_str.replace('<!--arlist_b--><ul>', '<ul class="arlist" id="deaikei">')
    new_str = new_str.replace('</ul><!--e/arlist_b-->', '</ul>')
    return new_str


def reibun_img_filter(new_str):
    p_img_str_l = re.findall(r'<p><img .+?/></p>', new_str)
    if p_img_str_l:
        for p_img_str in p_img_str_l:
            if '/w_500/' in p_img_str and 'width="' not in p_img_str:
                p_img_r = re.sub(r'<p>(.+?)/></p>', r'<div class="w_500">\1 width="500" height="375"/></div>',
                                 p_img_str)
            else:
                p_img_r = re.sub(r'<p>(.+?)/></p>', r'<div class="center">\1 /></div>', p_img_str)
            new_str = new_str.replace(p_img_str, p_img_r)
    return new_str


def reibun_breadcrumb_maker(category, directory, file_name):
    result = ''
    if 'index.html' in file_name:
        return result
    else:
        result += '<div itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem" class="brd2">' \
                  '<a href="../' + directory + '/" itemprop="item"><span itemprop="name">' + directory_name[directory] \
                  + '</span></a><meta itemprop="position" content="2" /> &gt;&gt;</div>'
        if directory == 'majime' and category != 'majime':
            result += '<div itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem" class="brd2">' \
                      '<a href="../' + directory + '/' + category_name[category][1] + \
                      '" itemprop="item"><span itemprop="name">' + \
                      category_name[category][
                          0] + '</span></a><meta itemprop="position" content="3" /> &gt;&gt;&gt;</div>'
        return result
