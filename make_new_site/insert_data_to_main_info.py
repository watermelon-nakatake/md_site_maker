import glob
import re


def insert_new_data_to_all_main_info(insert_name, insert_str, ignore_project):
    info_list = glob.glob('**/main_info.py')
    print(info_list)
    for info_path in info_list:
        if info_path.replace('/main_info.py', '') not in ignore_project:
            with open(info_path, 'r', encoding='utf-8') as f:
                long_str = f.read()
            if insert_name not in long_str:
                long_str = long_str.replace('info_dict = {',
                                            insert_name + " = '" + insert_str + "'\n\ninfo_dict = {")
                long_str = re.sub(r"(info_dict = {[\s\S]+?)}", r"\1" + ", '" + insert_name + "': " + insert_name + '}',
                                  long_str)
                print(long_str)
                with open(info_path, 'w', encoding='utf-8') as g:
                    g.write(long_str)


def check_temp_file(target_str, ignore_list):
    temp_list = glob.glob('**/html_files/template/main_tmp.html')
    print(temp_list)
    for tmp_path in temp_list:
        if tmp_path.replace('/html_files/template/main_tmp.html', '') not in ignore_list:
            with open(tmp_path, 'r', encoding='utf-8') as f:
                long_str = f.read()
                if target_str not in long_str:
                    print('no str in : {}'.format(tmp_path))


if __name__ == '__main__':
    # insert_new_data_to_all_main_info('relation_str',
    #                                  '<section><h2><!--keyword-main-noun-->の関連記事</h2><ul>{}</ul></section>',
    #                                  ['reibun', 'sfd'])
    check_temp_file('<!--relation-list-->', ['reibun'])
