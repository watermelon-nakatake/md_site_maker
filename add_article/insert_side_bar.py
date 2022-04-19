import glob
import pathlib
import pickle
import re
import file_upload
import mailsample.main_info


def insert_sb(project_path):
    new_list = [16, 15, 14, 13, 12, 11]
    file_path = glob.glob(project_path + '/**/**.html', recursive=True)
    # file_path = ['mailsample/html_files/index.html']
    pd = mailsample.main_info.info_dict
    # print(pd)
    with open(project_path + '/pickle_pot/main_data.pkl', 'rb') as p:
        pk_dic = pickle.load(p)
    # print(pk_dic)
    imp_str = ''.join(['<li><a href="../{}">{}</a></li>'.format(pk_dic[x]['file_path'], pk_dic[x]['title'])
                       for x in pk_dic if x in pd['side_bar_list']['important']])
    pop_str = ''.join(['<li><a href="../{}">{}</a></li>'.format(pk_dic[x]['file_path'], pk_dic[x]['title'])
                       for x in pk_dic if x in pd['side_bar_list']['pop']])
    new_str = ''.join(['<li><a href="../{}">{}</a></li>'.format(pk_dic[x]['file_path'], pk_dic[x]['title'])
                       for x in pk_dic if x in new_list])
    for h_path in file_path:
        p_data = pathlib.Path(h_path)
        p_str = p_data.read_text()
        # with p_data.open() as f:
        #     p_str = f.read()
        # print(p_str)
        if h_path.count('/') <= 2:
            for lc in [['人気記事', pop_str], ['重要記事', imp_str], ['最近の更新記事', new_str]]:
                p_str = re.sub(r'<div class="sbh">' + lc[0] + '</div><ul>.*?</ul>',
                               '<div class="sbh">{}</div><ul>{}</ul>'.format(lc[0], lc[1].replace('../', '')), p_str)
        else:
            for lc in [['人気記事', pop_str], ['重要記事', imp_str], ['最近の更新記事', new_str]]:
                p_str = re.sub(r'<div class="sbh">' + lc[0] + '</div><ul>.*?</ul>',
                               '<div class="sbh">{}</div><ul>{}</ul>'.format(lc[0], lc[1]), p_str)
        # print(p_str)
        p_data.write_text(p_str)
    file_upload.scp_upload(file_path, pd)


if __name__ == '__main__':
    insert_sb('mailsample')
