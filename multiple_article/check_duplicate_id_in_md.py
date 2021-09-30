import glob
import re

import make_new_article


def check_duplicate_id(project_dir):
    md_files = glob.glob(project_dir + '/md_files/**/**.md', recursive=True)
    md_files = [x for x in md_files if '_copy' not in x and '_test' not in x]
    print(md_files)
    used_id = []
    for md_path in md_files:
        with open(md_path, 'r', encoding='utf-8') as f:
            long_str = f.read()
        id_str_l = re.findall(r'\nn::(\d*?)\n', long_str)
        # print(id_str_l)
        if id_str_l:
            # print('{} : {}'.format(id_str_l[0], md_path))
            # print(used_id)
            if int(id_str_l[0]) not in used_id:
                used_id.append(int(id_str_l[0]))
            else:
                print('duplicate id : {}  {}'.format(id_str_l[0], md_path))
        else:
            print('no id : {}'.format(md_path))


if __name__ == '__main__':
    target_dir = 'goodbyedt'
    check_duplicate_id(target_dir)
    make_new_article.search_max_id(target_dir)
