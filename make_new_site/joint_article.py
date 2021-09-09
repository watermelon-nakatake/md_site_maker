import difflib
import glob
import re


def check_md_files(project_dir):
    md_files = glob.glob(project_dir + '/md_files/**/**.md', recursive=True)
    # print(md_files)
    short_md = []
    for md_path in md_files:
        with open(md_path, 'r', encoding='utf-8') as f:
            md_str = f.read()
        len_s = len(md_str)
        if len_s < 2000:
            short_md.append(md_path)
            print('{} : {}'.format(md_path, len_s))
        else:
            # print(md_path)
            pass


def check_diff_in_md_files(project_dir):
    result = []
    md_files = glob.glob(project_dir + '/md_files/**/**.md', recursive=True)
    for i in list(range(len(md_files))):
        x = md_files[i]
        with open(x, 'r', encoding='utf-8') as f:
            x_str = f.read()
            for y in md_files[i + 1:]:
                with open(y, 'r', encoding='utf-8') as g:
                    y_str = g.read()
                dif_r = difflib.SequenceMatcher(None, x_str, y_str).ratio()
                if dif_r > 0.3 and 'pref' not in x:
                    result.append([x, y, dif_r])
                    print([x, y, dif_r])
    result.sort(key=lambda z: z[2], reverse=True)
    print(result)


def insert_ad_key_to_md(project_dir, insert_ad):
    md_files = glob.glob(project_dir + '/md_files/**/**.md', recursive=True)
    # print(md_files)
    for md_path in md_files:
        with open(md_path, 'r', encoding='utf-8') as f:
            md_str = f.read()
        if not re.search(r'\na::\d+', md_str):
            md_str = md_str.replace('\nk::', '\na::{}\nk::'.format(insert_ad))
            print(md_str)
            with open(md_path, 'w', encoding='utf-8') as g:
                g.write(md_str)


if __name__ == '__main__':
    # check_md_files('women')
    # check_diff_in_md_files('women')
    insert_ad_key_to_md('women', '3')
