import re
import csv


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


if __name__ == '__main__':
    check_aff_for_gsc_data('reibun', 1)
