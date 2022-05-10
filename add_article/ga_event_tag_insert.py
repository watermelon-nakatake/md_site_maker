import glob
import os
import pathlib
import re


def event_tag_insert(project_dir):
    name_dic = {'550909': 'waku', 'pcmax': 'max', 'mintj': 'mintj', 'happymail': 'happy'}
    reibun_name_dic = {'wakuwakumail': 'waku', 'pcmax': 'max', 'mintj': 'mintj', 'jmail': 'mintj', 'happymail': 'happy',
                       'ranking': 'rank'}
    main_dir = ''
    if project_dir == 'reibun':
        main_dir = 'pc/'
        name_dic = reibun_name_dic
    all_files = glob.glob(project_dir + '/html_files/' + main_dir + '**/**.html', recursive=True)
    all_files = [x for x in all_files if '_copy' not in x and '_ud' not in x]
    all_files = ['reibun/html_files/pc/caption/fwari.html']
    print(all_files)
    for file_path in all_files:
        p = pathlib.Path(file_path)
        p.open()
        base_str = p.read_text()
        ar_str = re.findall(r'<article.+?</article>', base_str)
        if ar_str:
            new_str = base_str
            tr_str = re.sub(r'<div class="only_mob teisite">.*$', '', ar_str[0])

            a_list = re.findall(r'<a .+?>', tr_str)
            a_list = list(set(a_list))
            for a_str in a_list:
                if '/sitepage/' in a_str and 'gtag' not in a_str:
                    for s_name in name_dic:
                        if '/sitepage/' + s_name in a_str:
                            if 'class="' not in a_str:
                                c_str = ' class="{}-atxil"'.format(name_dic[s_name])
                            else:
                                c_str_l = re.findall(r'class="(.+?)"', a_str)
                                if c_str_l:
                                    c_str = ' class="{}-atxil {}"'.format(name_dic[s_name], c_str_l[0])
                                else:
                                    c_str = ' class="{}-atxil"'.format(name_dic[s_name])
                            tag_str = ' onclick="gtag' + "('event','click',{'event_category':'access','event_label':'"\
                                      + name_dic[s_name] + "-txil'}" + ');"'
                            ins_a = a_str.replace('>', c_str + tag_str + '>')
                            ins_a = ins_a.replace('  ', ' ')
                            new_str = new_str.replace(a_str, ins_a)


            if new_str != base_str:
                print(new_str)


if __name__ == '__main__':
    os.chdir('../')
    event_tag_insert('reibun')
