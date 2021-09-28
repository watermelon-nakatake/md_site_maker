import glob
import re


def html_link_check(project_dir):
    html_files = glob.glob(project_dir + '/html_files/**/**.html', recursive=True)
    # print(html_files)
    other_files = glob.glob(project_dir + '/html_files/**/**', recursive=True)
    dir_list = glob.glob(project_dir + '/html_files/**/', recursive=True)
    # print(dir_list)
    exist_link = html_files + dir_list + other_files
    exist_link = list(set(exist_link))
    exist_link.sort()
    # print(exist_link)
    for path_str in html_files:
        with open(path_str, 'r', encoding='utf-8') as f:
            str_h = f.read()
            link_str_l = re.findall(r'href="(.*?)"', str_h)
            id_list = re.findall(r'id="(.*?)"', str_h)
            src_link = re.findall(r'src="(.*?)"', str_h)
            link_str_l = link_str_l + src_link
            # print(link_str_l)
            make_absolute_path(link_str_l, path_str, exist_link, id_list)


def make_absolute_path(relative_path_list, path_str, exist_link, id_list):
    split_path = path_str.split('/')
    # print(split_path)
    for link_str in relative_path_list:
        if not link_str:
            print('empty link in  {}'.format(path_str))
        elif link_str.startswith('#'):
            if link_str.replace('#', '') not in id_list:
                print('there is no id : ' + link_str)
        elif 'https://' in link_str:
            pass
        else:
            back_count = link_str.count('../')
            # print(back_count)
            add_path = split_path[:-1 * (back_count + 1)]
            ab_path = '/'.join(add_path) + '/' + link_str.replace('../', '').replace('./', '')
            # print(ab_path)
            if ab_path not in exist_link:
                print('poor link [{}]   in   [{}]'.format(link_str, path_str))


if __name__ == '__main__':
    html_link_check('joshideai')
