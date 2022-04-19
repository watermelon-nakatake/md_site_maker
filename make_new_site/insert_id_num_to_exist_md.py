import glob
import pprint
import re
import sfd.main_info


def insert_id_to_imported_md_files(project_dir):
    sorted_list = []
    top_list = []
    index_list = []
    other_list = []
    plus_num = 1
    md_files = glob.glob(project_dir + '/md_files/**/**.md')
    md_files.sort()
    for md_path in md_files:
        if 'md_files/index.md' in md_path:
            top_list.append(md_path)
        elif '/index.md' in md_path:
            index_list.append(md_path)
        else:
            other_list.append(md_path)
    sorted_list = other_list
    sorted_list.sort()
    pprint.pprint(sorted_list)
    # return
    i = 3
    for md_p in sorted_list:
        with open(md_p, 'r', encoding='utf-8') as f:
            md_str = f.read()
        if '\nn::' in md_str:
            md_str = re.sub(r'\nn::\d*?\n', '\nn::{}\n'.format(i), md_str)
        else:
            md_str = re.sub(r'\nk::', '\nn::{}\nk::'.format(i), md_str)
        i += 1
        # print(md_str)
        with open(md_p, 'w', encoding='utf-8') as g:
            g.write(md_str)
    print('next id : {}'.format(i))


def insert_id_to_no_display_md(sorted_list, start_num):
    i = start_num
    sorted_list.sort()
    for md_p in sorted_list:
        # md_p = md_p.replace('https://www.sefure-do.com/', 'sfd/del_md/')
        md_p = re.sub(r'https://www.sefure-do.com/(.+)/', r'sfd/del_md/\1.md', md_p)
        with open(md_p, 'r', encoding='utf-8') as f:
            md_str = f.read()
        if '\nn::' in md_str:
            md_str = re.sub(r'\nn::\d*?\n', '\nn::{}\n'.format(i), md_str)
        else:
            md_str = re.sub(r'\nk::', '\nn::{}\nk::'.format(i), md_str)
        i += 1
        # print(md_str)
        print(md_p)
        with open(md_p, 'w', encoding='utf-8') as g:
            g.write(md_str)
    print('next id : {}'.format(i))


if __name__ == '__main__':
    no_dsp_list = ['https://www.sefure-do.com/friend-with-benefits/boys-love/',
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
    # target_dir = 'sfd'
    # insert_id_to_imported_md_files(target_dir)
    insert_id_to_no_display_md(no_dsp_list, 791)
