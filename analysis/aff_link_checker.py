import os
# import pprint
import re
import csv
import google_analytics_access


def check_aff_link_str(long_str, pj_name):
    result = []
    aff_url = {'reibun': {'wk': 'wakuwakumail', 'mt': 'mintj', 'max': 'pcmax', 'hm': 'happymail'},
               'other': {'wk': '550909', 'mt': 'mintj', 'max': 'pcmax', 'hm': 'happymail'}}
    pj_dict = {'reibun': 'sitepage', 'sfd': 'url'}
    pj_code = 'other'
    if pj_name == 'reibun':
        pj_code = 'reibun'
    if pj_name == 'sfd':
        af_list = re.findall(r'/' + pj_dict[pj_name] + r'/.+?/', long_str)
    else:
        af_list = re.findall(r'/' + pj_dict[pj_name] + r'/.+?\.', long_str)
    if af_list:
        # print(af_list)
        for a_id in aff_url[pj_code]:
            if '/{}/{}.'.format(pj_dict[pj_name], aff_url[pj_code][a_id]) in af_list:
                result.append(a_id)
    result = list(set(result))
    # print(result)
    return result


def check_image(long_str, pj_name):
    wp_list = ['sfd', 'shoshin']
    result = False
    if pj_name in wp_list:
        pass
    else:
        if '/images/' in long_str:
            result = True
    return result


def check_aff_for_gsc_data(pj_name, limit_num):
    gsc_data_path = 'gsc_data/{}/p_today.csv'.format(pj_name)
    with open(gsc_data_path, 'r', encoding='utf-8') as p:
        reader_p = csv.reader(p)
        p_list = [x for x in reader_p]
    count_i = 1
    for page in p_list[1:51]:
        if 'https:' in page[4]:
            md_path = pj_name + '/md_files/' + re.sub(r'^https://.+?/', '', page[4]).replace('.html', '.md')
            with open(md_path, 'r', encoding='utf-8') as f:
                md_str = f.read()
            aff_list = check_aff_link_str(md_str, pj_name)
            img_flag = check_image(md_str, pj_name)
            if len(aff_list) <= limit_num or not img_flag:
                print('{} {} : {} {} - {}'.format(count_i, md_path, aff_list, img_flag, page[0]))
            count_i += 1


def mint_checker(pj_name):
    checked_url = []
    gsc_data_path = 'gsc_data/{}/p_today.csv'.format(pj_name)
    with open(gsc_data_path, 'r', encoding='utf-8') as p:
        reader_p = csv.reader(p)
        p_list = [x for x in reader_p]
    # print(p_list)
    counter = 0
    for page in p_list[1:101]:
        if 'https:' in page[4]:
            html_path = page[4]
            if html_path.endswith('/'):
                html_path = html_path + 'index.html'
            elif '.html' not in html_path:
                html_path = html_path + '/index.html'
            md_path = pj_name + '/md_files/' + re.sub(r'^https://.+?/', '', html_path).replace('.html', '.md')
            if os.path.exists(md_path):
                with open(md_path, 'r', encoding='utf-8') as f:
                    md_str = f.read()
                    if '/mintj.' in md_str:
                        print('{} : {}'.format(md_path, page[0]))
                        counter += 1
                    else:
                        checked_url.append(md_path)
    return checked_url


def ga_order_mint_checker(pj_name, start_date, limit):
    checked_url = mint_checker(pj_name)
    ga_data = google_analytics_access.get_ga_data(start_date, limit)
    pc_dict = {}
    rename_data = [[x[0].replace('/amp/', '/pc/'), x[2]] for x in ga_data]
    for row in rename_data:
        if row[0] not in pc_dict:
            pc_dict[row[0]] = int(row[1])
        else:
            pc_dict[row[0]] = pc_dict[row[0]] + int(row[1])
    pc_list = [[x.replace('.html', '.md').replace('/pc/', pj_name + '/md_files/pc/'), pc_dict[x]] for x in pc_dict]
    pc_list = [x for x in pc_list if x[0] not in checked_url]
    pc_list.sort(key=lambda x: x[1], reverse=True)
    for md in pc_list:
        md_path = md[0]
        if md_path not in ['/app/', '/', 'reibun/md_files/pc/']:
            if md_path.endswith('/'):
                md_path = md_path + 'index.md'
            elif '.md' not in md_path:
                md_path = md_path + '/index.md'
            if os.path.exists(md_path):
                with open(md_path, 'r', encoding='utf-8') as f:
                    md_str = f.read()
                    if '/mintj.' in md_str:
                        print('{} : {}'.format(md_path, md[1]))
    # pprint.pprint(pc_list)


if __name__ == '__main__':
    print(os.getcwd())
    # check_aff_for_gsc_data('reibun', 1)
    # mint_checker('reibun')
    ga_order_mint_checker('reibun', start_date='2022-04-01', limit='200')
