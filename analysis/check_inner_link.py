import glob
import pathlib
import re


def make_link_list(md_path):
    pj_dir = re.sub(r'^(.+?)/md_files/.*$', r'\1', md_path)
    same_dir = re.sub(r'^(.+)/.*$', r'\1', md_path)
    print(same_dir)
    last_dir = re.sub(r'^.*/(.+)/.*$', r'\1', md_path)
    file_name = re.sub(r'^.+/', '', md_path)
    m_two_path = last_dir + '/' + file_name
    h_two_path = m_two_path.replace('.md', '.html')
    print(m_two_path)
    # print(last_dir)
    if '/pc/' in md_path:
        remove_path = pj_dir + '/md_files/pc/'
    else:
        remove_path = pj_dir + '/md_files/'
    md_list = [x for x in glob.glob(pj_dir + '/md_files/**/**.md', recursive=True) if '_test.' not in x
               and '_copy.' not in x and '_ud.' not in x]
    for o_path in md_list:
        with open(o_path, 'r', encoding='utf-8') as f:
            long_str = f.read()
            link_list = re.findall(r'\[(.+?)]\((.+?)\)', long_str)
            for link in link_list:
                if m_two_path in link[1] or h_two_path in link[1]:
                    print('{} as {}'.format(o_path.replace(remove_path, ''), link[0]))
                elif same_dir in o_path and link[1] == file_name:
                    print('{} as {} !!'.format(o_path.replace(remove_path, ''), link[0]))

    # print(md_list)


if __name__ == '__main__':
    make_link_list('reibun/md_files/pc/majime/m1sexfriendmail.md')
