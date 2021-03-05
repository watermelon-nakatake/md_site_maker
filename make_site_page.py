import csv
import re
import datetime
import os
import reibun_upload
from PIL import Image
import make_article_list
import check_mod_date

site_name_list = ['wk', 'hm', 'mt', 'mp', 'max', 'iq']
site_page_dict = {'hm': 'happymail', 'wk': 'wakuwakumail', 'mt': 'mintj', 'max': 'pcmax', 'iq': '194964'}
# 'mp': 'meru-para'
star_category = ['コスト', '使いやすさ', '出会える度', 'ピュア系', 'アダルト系']
site_str = [['ハッピーメール', 'happymail'], ['ワクワクメール', 'wakuwakumail'], ['Jメール', 'mintj'], ['PCMAX', 'pcmax'],
            ['イククル', '194964']]


def main():
    csv_path = 'csv_data/rb_csv.csv'
    star_count, site_dict = make_data(csv_path)
    star_count = make_ranking(star_count)
    insert_data(star_count, site_dict)
    pc_and_amp_site_page_upload()


def insert_mod_log_to_top_page(date_str):
    with open('reibun/index.html', 'r', encoding='utf-8') as f:
        long_str = f.read()
    insert = ''.join(['<li>{} [出会い系サイト情報・<a href="pc/sitepage/{}.html">{}の口コミ情報と詳細データ</a>]を更新</li>'
                     .format(date_str, x[1], x[0]) for x in site_str])
    print(insert)
    long_str = re.sub(r'<div id="update"><ul class="updli">', '<div id="update"><ul class="updli">' + insert, long_str)
    with open('reibun/index.html', 'w', encoding='utf-8') as g:
        g.write(long_str)
    with open('reibun/amp/index.html', 'r', encoding='utf-8') as f:
        long_str_a = f.read()
    insert_a = ''.join(['<li>{} [出会い系サイト情報・<a href="sitepage/{}.html">{}の口コミ情報と詳細データ</a>]を更新</li>'
                       .format(date_str, x[1], x[0]) for x in site_str])
    long_str_a = re.sub(r'<div id="update"><ul class="updli">', '<div id="update"><ul class="updli">' + insert_a,
                        long_str_a)
    with open('reibun/amp/index.html', 'w', encoding='utf-8') as g:
        g.write(long_str_a)
    reibun_upload.ftp_upload(['reibun/index.html', 'reibun/amp/index.html'])


def pc_and_amp_site_page_upload():
    pc_list = ['reibun/pc/sitepage/' + x for x in os.listdir('reibun/pc/sitepage') if '.html' in x and '_test'
               not in x and '_copy' not in x]
    amp_list = ['reibun/amp/sitepage/' + x for x in os.listdir('reibun/amp/sitepage') if '.html' in x and '_test'
                not in x and '_copy' not in x]
    up_list = pc_list + amp_list
    reibun_upload.ftp_upload(up_list)


def site_page_pc_to_amp_changer(amp_path):
    """
    ampに対応できていないcodeをampに対応させて保存
    :param amp_path: ampページのパス
    :return: none
    """
    with open(amp_path, 'r', encoding='utf-8') as f:
        long_str = f.read()
    long_str = pc_to_amp_changer(long_str)
    with open(amp_path, 'w', encoding='utf-8') as g:
        g.write(long_str)


def pc_to_amp_changer(long_str):
    """
    文字列のimgなどをamp対応に変換する。
    :param long_str: ampに対応していない文字列
    :return: ampに対応させた文字列
    """
    long_str = reibun_upload.tab_and_line_feed_remove_from_str(long_str)
    long_str = long_str.replace('<img src="../images/common/site_name_250.png" alt="出会い系メール例文集">',
                                '<amp-img src="../images/common/site_name_400.png" alt="出会い系メール例文集"' +
                                ' width="400" height="59" layout="responsive"></amp-img>')
    long_str = long_str.replace('<img src="../images/common/mod_i.png" alt="更新">',
                                '<amp-img src="../images/common/mod_i.png" width="15" height="15" layout="responsive"' +
                                ' alt="更新"></amp-img>')
    long_str = re.sub(r'<img src="\.\./images/common/(.+?)_sq.png" width="240" height="240" alt="(.+?)">',
                      r'<amp-img src="../images/common/\1_sq.png" width="240" height="240" alt="\2"' +
                      ' layout="responsive"></amp-img>', long_str)
    long_str = re.sub(r'<img src="\.\./images/common/star(.+?)>',
                      r'<amp-img src="../images/common/star\1 width="672" height="110" layout="responsive"></amp-img>',
                      long_str)
    img_str_list = re.findall(r'<img .+?>', long_str)
    img_str_list = set(img_str_list)
    img_str_list = list(img_str_list)
    if img_str_list:
        for img_str in img_str_list:
            if 'width="' in img_str and 'height="' in img_str and 'layout="' in img_str:
                replaced_str = re.sub(r'<img (.+?)>', r'<amp-img \1></amp-img>', img_str)
            elif 'width="' in img_str and 'height="' in img_str and 'layout="' not in img_str:
                replaced_str = re.sub(r'<img (.+?)>', r'<amp-img \1 layout="responsive"></amp-img>', img_str)
            elif 'width="' not in img_str and 'height="' not in img_str:
                print(img_str)
                img_path = re.findall(r'src="(.+?)"', img_str)[0]
                img_path = img_path.replace('../images/', 'reibun/pc/images/')
                im = Image.open(img_path)
                w, h = im.size
                print(w)
                print(h)
                replaced_str = re.sub(r'<img (.+?)>', r'<amp-img \1 width="{}" height="{}"></amp-img>'.format(w, h),
                                      img_str)
                if 'layout="' not in replaced_str:
                    replaced_str = re.sub(r'<amp-img (.+?)>', r'<amp-img \1 layout="responsive">', replaced_str)
            else:
                print('no defect : ' + img_str)
                replaced_str = re.sub(r'<img (.+?)>', r'<amp-img \1 ></amp-img>', img_str)
            if '  ' in replaced_str:
                replaced_str = replaced_str.replace('  ', '')
            if '/ ' in replaced_str:
                replaced_str = replaced_str.replace('/ ', ' ')
            long_str = long_str.replace(img_str, replaced_str)
    return long_str


def make_list_from_csv(csv_path):
    with open(csv_path) as f:
        reader = csv.reader(f)
        l_r = [r for r in reader]
        csv_list = [[int(v) if row.index(v) in [4, 5, 6, 7, 8] else v for v in row] for row in l_r[1:]]
        # csv_list = csv_list[1:]
    print(csv_list)
    return csv_list


def make_data(csv_path):
    csv_list = make_list_from_csv(csv_path)
    site_dict = {x: [] for x in site_name_list}
    for row in csv_list:
        site_dict[row[0]].append(row[1:])
    print(site_dict)
    star_count = count_star(site_dict)
    return star_count, site_dict


def star_num_maker(s_num):
    dec_num = s_num * 10
    a_num = dec_num // 10
    b_num = dec_num % 10
    if b_num < 3:
        result = str(int(a_num))
    elif b_num > 7:
        result = str(int(a_num + 1))
    else:
        result = str(int(a_num * 10 + 5)).zfill(2)
    return result


def insert_data(site_data, site_user_data):
    today = datetime.date.today()
    today_str = today.strftime('%Y/%m/%d').replace('/0', '/')
    today_str2 = today.strftime('%F')
    for site_code in site_page_dict:
        print(site_code)
        if site_user_data[site_code]:
            print(site_data[site_code])
            site_page_path = 'reibun/pc/sitepage/' + site_page_dict[site_code] + '.html'
            print(site_page_path)
            with open(site_page_path, 'r', encoding='utf-8') as f:
                long_str = f.read()
            long_str = reibun_upload.tab_and_line_feed_remove_from_str(long_str)
            this_data = site_data[site_code]
            for i in range(len(star_category) + 1):
                # main_i = i + 3
                main_star = star_num_maker(this_data[i])
                long_str = re.sub(r'src="\.\./images/common/star\d+?\.png" alt="星[\d.]+?つ" id="star_i' + str(i + 1) +
                                  r'"></span><span class="ana_i_num"><span>.+?</span></span>',
                                  'src="../images/common/star' + main_star + '.png" alt="星' + str(this_data[i])
                                  + 'つ" id="star_i' + str(i + 1) + '"></span><span class="ana_i_num"><span>' +
                                  str(this_data[i]) + '</span></span>', long_str, 1)
            total_star = star_num_maker(this_data[5])
            long_str = re.sub(r'src="\.\./images/common/star.+?\.png" alt="星.+?つ" id="star_it"></span>' +
                              r'<span class="ana_m_num"><span>.+?</span></span></div></div><!--end-total-->',
                              'src="../images/common/star' + total_star + '.png" alt="星' + total_star
                              + 'つ" id="star_it"></span><span class="ana_m_num"><span>' + str(this_data[5]) +
                              '</span></span></div></div><!--end-total-->', long_str, 1)
            long_str = re.sub(r'5サイト中</a> \d位</div>', '5サイト中</a> {}位</div>'.format(str(this_data[6])), long_str)
            user_data_str = ''
            for user_data in site_user_data[site_code]:
                i_str = '<div class="k_ana_box"><div class="k_data_i"><span class="k_data_name">' + user_data[0] + \
                        'さん</span><span class="k_data_sex">' + user_data[1] + '性</span><span class="k_data_age">' + \
                        user_data[2] + '</span></div><div class="k_ana_i"><span class="k_ana_i_title">コスト</span>' + \
                        '<span class="k_ana_i_star"><img src="../images/common/star' + str(
                    user_data[3]) + '.png" alt="星' \
                        + str(user_data[3]) + 'つ"></span></div><div class="k_ana_i"><span class="k_ana_i_title">' + \
                        '出会える度</span><span class="k_ana_i_star"><img src="../images/common/star' + str(user_data[4]) \
                        + '.png" alt="星' + str(user_data[4]) + 'つ"></span></div><div class="k_ana_i"><span ' + \
                        'class="k_ana_i_title">使いやすさ</span><span class="k_ana_i_star"><img src="../images/common/star' \
                        + str(user_data[5]) + '.png" alt="星' + str(user_data[5]) + 'つ"></span></div>' + \
                        '<div class="k_ana_i"><span class="k_ana_i_title">恋愛</span><span class="k_ana_i_star">' + \
                        '<img src="../images/common/star' + str(user_data[6]) + '.png" alt="星' + str(user_data[6]) + \
                        'つ"></span></div><div class="k_ana_i"><span class="k_ana_i_title">アダルト</span>' + \
                        '<span class="k_ana_i_star"><img src="../images/common/star' + str(
                    user_data[7]) + '.png" alt="星' \
                        + str(user_data[7]) + 'つ"></span></div><div class="k_data_comment"><span class="k_com_c">' + \
                        'コメント</span><span class="k_com_t">' + user_data[8] + '</span></div></div>'
                user_data_str += i_str
            long_str = re.sub(r'<!--kuchi-list-->.*?<!--e/kuchi-list-->',
                              '<!--kuchi-list-->' + user_data_str + '<!--e/kuchi-list-->', long_str)
            long_str = re.sub(r'<time itemprop="dateModified" datetime=".+?</time>',
                              '<time itemprop="dateModified" datetime="{}">{}</time>'.format(today_str2, today_str),
                              long_str)
            with open(site_page_path, 'w', encoding='utf-8') as g:
                g.write(long_str)


def make_ranking(star_count):
    data_list = [[x, star_count[x][5]] for x in star_count]
    data_list.sort(key=lambda y: y[1], reverse=True)
    rank_dict = {z[0]: data_list.index(z) + 1 for z in data_list}
    result = {y: star_count[y] + [rank_dict[y]] for y in star_count}
    return result


def count_star(site_dict):
    result_dict = {}
    for site_name in site_dict:
        if site_dict[site_name]:
            cost = 0
            meet = 0
            use = 0
            pure = 0
            adult = 0
            for doc in site_dict[site_name]:
                cost += doc[3]
                meet += doc[4]
                use += doc[5]
                pure += doc[6]
                adult += doc[7]
            result_dict[site_name] = [round(cost / len(site_dict[site_name]), 1),
                                      round(meet / len(site_dict[site_name]), 1),
                                      round(use / len(site_dict[site_name]), 1),
                                      round(pure / len(site_dict[site_name]), 1),
                                      round(adult / len(site_dict[site_name]), 1),
                                      round((cost + meet + use + pure + adult) / 5 / len(site_dict[site_name]), 1)]
    print(result_dict)
    return result_dict


def star_size_list():
    star = 275
    margin = 70
    result = 0
    for i in range(12):
        if i % 2 == 1:
            result += margin
        else:
            result += star
        print(result)


def manual_add_modify_log(mod_file_path_list):
    mod_log = make_article_list.read_pickle_pot('modify_log')
    now = datetime.date.today()
    today_mod = [x[0] for x in mod_log if x[1] == str(now)]
    for mod_file_path in mod_file_path_list:
        with open(mod_file_path, 'r', encoding='utf-8') as f:
            long_str = f.read()
        title = re.findall(r'<title>(.+?)\|出会い系メール例文集</title>', long_str)[0]
        if mod_file_path not in today_mod:
            mod_log.append([mod_file_path, str(now), 'sitepage', title, 'mod'])
        else:
            for data in mod_log:
                if data[0] == mod_file_path and data[1] == str(now):
                    mod_log.remove(data)
                    mod_log.append([mod_file_path, str(now), 'sitepage', title, 'mod'])
    make_article_list.save_data_to_pickle(mod_log, 'modify_log')
    check_mod_date.make_mod_date_list()


if __name__ == '__main__':
    # make_list_from_csv('csv_data/test_rb_csv.csv')
    # make_data('csv_data/test_rb_csv.csv')
    # star_size_list()

    # reibun_upload.tab_and_line_feed_remover('reibun/amp/site/index.html')
    # reibun_upload.tab_and_line_feed_remover('reibun/amp/sitepage/194964.html')

    # reibun_upload.tab_and_line_feed_remover('reibun/pc/sitepage_test/happymail.html')
    # reibun_upload.tab_and_line_feed_remover('reibun/pc/sitepage_test/194964.html')

    # site_page_pc_to_amp_changer('reibun/amp/sitepage/194964.html')

    # pc_and_amp_site_page_upload()

    # reibun_upload.ftp_upload(['reibun/pc/site/index.html'])

    main()

    manual_add_modify_log(['reibun/pc/sitepage/{}.html'.format(x[1]) for x in site_str])
    print(make_article_list.read_pickle_pot('modify_log'))
    print(make_article_list.read_pickle_pot('mod_date_list'))
    # print(make_article_list.read_pickle_pot('title_img_list'))
    # insert_mod_log_to_top_page('2020/8/5')
