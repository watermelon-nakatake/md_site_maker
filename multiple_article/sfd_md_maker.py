import re
import os
import shutil

import make_new_article
import source_data
import make_html_for_sfd


def sfd_md_maker_by_key_list(dir_name, part_code, start_num, end_num, start_id, subject_sex, pub_start):
    key_dict = make_new_article.key_source_dict[part_code]
    if not end_num:
        end_num = list(key_dict.keys())[-1]
    use_id = [x for x in key_dict if start_num <= x <= end_num]
    print(use_id)
    if part_code != 'adj_act':
        part_code_e = re.sub(r'_.', '', part_code)
    else:
        part_code_e = part_code
    make_new_article.make_new_pages_to_md_from_key_list('sfd', dir_name, source_data, 'sf', use_id,
                                                        make_new_article.key_source_dict[part_code], recipe_flag=True,
                                                        subject_sex=subject_sex, start_id=start_id, insert_pub_date=pub_start,
                                                        part_code=part_code_e, copy_pub_flag=False,
                                                        exist_update_flag=True)
    if os.path.exists('sfd/html_files/' + dir_name):
        shutil.rmtree('sfd/html_files/' + dir_name)
        os.mkdir('sfd/html_files/' + dir_name)
    make_html_for_sfd.translate_md_to_html('sfd/wp_temp.html', 'sfd/md_files/' + dir_name, subject_sex,
                                           pub_flag=True, pub_take_over=True, html_dir=dir_name)


if __name__ == '__main__':
    sfd_md_maker_by_key_list('adj_act', 'adj_act', 0, '', 580, 'man', '2021-10-01T18:22:12')
