import re

project_dir = 'konkatsu'

site_name = 'ネット婚活で結婚相手探し'
side_bar_list = {'important': [],
                 'pop': []}
category_data = {'partner': ['結婚相手を探す', 'index.html', 1],
                 'best-way-to-matchmaking': ['婚活のやり方', 'index.html', 2]}
category_name = {x: [category_data[x][0], category_data[x][1]] for x in category_data}
directory_name = {x: category_data[x][0] for x in category_data}
site_shift_list = []
site_shift_order = []

add_files = []

main_dir = ''
article_image_dir = 'art_images'
amp_flag = False
default_img = 'konkatsu/html_files/images/common/konkatsu_img.jpeg'
h_sitemap_path = 'konkatsu/html_files/sitemap.html'
domain_str = 'netdekonkatsu.com'
ignore_files = ['konkatsu/html_files/google3d7d16f68a5d3b38.html']
upload_data = {'host_name': 'wmelon01.sakura.ne.jp', 'password_str': '4tmy3uap6y', 'user_name': 'wmelon01',
               'upload_dir': 'konkatsu'}
sc_url = {'ワクワクメール': 'link/550909', 'PCMAX': 'link/pcmax',
          'ハッピーメール': 'link/happymail', 'Jメール': 'link/mintj'}
eyec_img = {'img_path': 'eyec.jpg', 'height': '464', 'width': '700'}
aff_dir = {'dir': 'link'}

info_dict = {'project_dir': project_dir, 'site_name': site_name, 'side_bar_list': side_bar_list,
             'category_name': category_name, 'category_data': category_data,
             'directory_name': directory_name, 'site_shift_list': site_shift_list, 'add_files': add_files,
             'main_dir': main_dir, 'ar_img_dir': article_image_dir, 'amp_flag': amp_flag,
             'default_img': default_img, 'h_sitemap_path': h_sitemap_path, 'domain_str': domain_str,
             'ignore_files': ignore_files, 'upload_data': upload_data, 'sc_url': sc_url, 'eyec_img': eyec_img,
             'aff_dir': aff_dir}


def konkatsu_insert_site_banner(long_str):
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


def konkatsu_icon_filter(long_str):
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


def konkatsu_insert_additional_str(new_str):
    new_str = new_str.replace('</section><section><div class="kanren">',
                              '</section><div class="only_mob teisite"><div class="sbh">出会系口コミランキング</div>'
                              '<ul class="slu"><li><a href="../link/wakuwakumail.html"><div class="sli">'
                              '<span class="sl_num">1</span><img src="../images/common/wkwk_sq.gif" '
                              'alt="ワクワクメール"><div class="slr"><span class="slsn">ワクワクメール</span>'
                              '<span class="slsd">利用者が多くコスパ抜群</span></div></div></a></li><li><a href="../link/happymail.html"><div class="sli">'
                              '<span class="sl_num">2</span><img src="../images/common/hm_sq.png" '
                              'alt="ハッピーメール"><div class="slr"><span class="slsn">ハッピーメール</span>'
                              '<span class="slsd">真面目な出会いに強い</span></div></div></a></li><li>'
                              '<a href="../link/pcmax.html"><div class="sli"><span class="sl_num">3</span>'
                              '<img src="../images/common/max_sq.gif" alt="PCMAX"><div class="slr">'
                              '<span class="slsn">PCMAX</span><span class="slsd">初心者でも使いやすい</span></div>'
                              '</div></a></li></ul>'
                              '<div class="center"><a href="../link/ranking.html">口コミ評価ランキング</a>'
                              '</div></div><section><div class="kanren">')
    new_str = new_str.replace('<!--arlist_b--><ul>', '<ul class="arlist" id="deaikei">')
    new_str = new_str.replace('</ul><!--e/arlist_b-->', '</ul>')
    return new_str


def konkatsu_img_filter(new_str):
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


def konkatsu_breadcrumb_maker(category, directory, file_name):
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
