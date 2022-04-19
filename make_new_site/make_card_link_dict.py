import glob
import pickle
import pprint
import re

import new_from_md


def main(project_dir):
    cl_dic = {}
    md_list = glob.glob(project_dir + '/md_files/**/**.md', recursive=True)
    for md_path in md_list:
        print(md_path)
        with open(md_path, 'r', encoding='utf-8') as f:
            md_str = f.read()
        title = re.findall(r't::(.+?)\n', md_str)[0]
        title = re.sub(r'<!--.*?-->', '', title)
        url = re.sub(r'^.*/md_files/', '', md_path)
        url = url.replace('.md', '.html')
        md_main = re.sub(r'^[\s\S]*::.*?\n', '', md_str)
        md_main = re.sub(r'%\S+\n', '', md_main)
        start_str = new_from_md.make_start_str(md_main)
        if '![' in md_str:
            img_str = re.findall(r'!\[.*?]\((.*?)\)\n', md_str)[0]
            img_str = re.sub(r'^.*/images/', 'images/', img_str)
            img_str = re.sub(r'-\d*x\d*\.', '.', img_str)
            img_str = img_str.replace('.', '-150x150.')
        else:
            img_str = ''
        cl_dic[url] = {'title': title, 'start_str': start_str, 'img_path': img_str}
    pprint.pprint(cl_dic)
    with open(project_dir + '/pickle_pot/card_data.pkl', 'wb') as p:
        pickle.dump(cl_dic, p)


if __name__ == '__main__':
    main('sfd')
    # with open('sfd/pickle_pot/card_data.pkl', 'rb') as f:
    #     data = pickle.load(f)
    # pprint.pprint(data)

