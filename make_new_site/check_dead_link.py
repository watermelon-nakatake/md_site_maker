import glob
import os
import pathlib
import re
import sre_parse


def pick_up_inner_dead_link(dir_name, sub_dir):
    all_h_files = glob.glob(dir_name + '/' + sub_dir + '/**/**.html', recursive=True)
    # print(all_h_files)
    under_h_path_list = [x.replace(dir_name + '/' + sub_dir + '/', '') for x in all_h_files]
    # print(under_h_path_list)
    for c_path in all_h_files:
        error_flag = True
        # c_path = 'sfd/up_html/friend-with-benefits/30-something/index.html'
        sp_path = c_path.split('/')
        # print(sp_path)
        p = pathlib.Path(c_path)
        p.open()
        h_str = p.read_text()
        # print(h_str)
        a_str_l = re.findall(r'href="(.*?)"', h_str)
        a_str_l.extend(re.findall(r'src="(.*?)"', h_str))
        id_list = re.findall(r'id="(.+?)"', h_str)
        for a_str in a_str_l:
            if (dir_name in a_str or sub_dir in a_str) and 'sfd.jpg' not in a_str:
                print('error!! dir name in ')
                error_flag = False
            domain_flag = False
            # print('')
            # print(a_str)
            if ('https://' in a_str or 'http://' in a_str) and 'sefure-do.com' not in a_str:
                pass
            elif a_str.startswith('#'):
                if a_str.replace('#', '') not in id_list:
                    print('wrong inner link : {}'.format(a_str))
                    error_flag = False
            elif a_str == '':
                print('error!! empty link')
                error_flag = False
            else:
                if 'sefure-do.com' in a_str:
                    all_t_path = re.sub(r'^.*sefure-do\.com', '', a_str)
                    all_t_path = dir_name + '/' + sub_dir + all_t_path
                    domain_flag = True
                else:
                    b_count = a_str.count('../')
                    all_t_path = '/'.join(sp_path[:(b_count + 1) * -1]) + '/' + a_str.replace('../', '')
                if '.' not in all_t_path or domain_flag:
                    if ('/url/' in all_t_path or '/link/' in all_t_path) and '/index.html' not in all_t_path:
                        if all_t_path.endswith('/'):
                            all_t_path = all_t_path + '.htaccess'
                        else:
                            all_t_path = all_t_path + '/.htaccess'
                    else:
                        if all_t_path.endswith('/'):
                            all_t_path = all_t_path + 'index.html'
                        else:
                            if '/index.html' not in all_t_path:
                                all_t_path = all_t_path + '/index.html'
                # print(all_t_path)
                if not os.path.exists(all_t_path):
                    print('dead link : {} => {}'.format(a_str, all_t_path))
                    error_flag = False
        if not error_flag:
            print('current_file : {}'.format(c_path))
            print('')


if __name__ == '__main__':
    os.chdir('../')
    pick_up_inner_dead_link('sfd', 'up_html')
