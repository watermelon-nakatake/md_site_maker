import glob
import re


def insert_id_to_imported_md_files(project_dir):
    sorted_list = []
    index_list = []
    other_list = []
    plus_num = 1
    md_files = glob.glob(project_dir + '/md_files/**/**.md')
    md_files.sort()
    for md_path in md_files:
        if 'md_files/index.md' in md_path:
            sorted_list.append(md_path)
            plus_num = 0
        elif '/index.md' in md_path:
            index_list.append(md_path)
        else:
            other_list.append(md_path)
    sorted_list = sorted_list + index_list + other_list
    print(sorted_list)
    i = plus_num
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


if __name__ == '__main__':
    target_dir = 'mailsample'
    insert_id_to_imported_md_files(target_dir)
