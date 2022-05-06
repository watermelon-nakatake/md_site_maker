import os

import file_upload
import new_from_md
import sfd.main_info
import sfd_move_up_html
import check_dead_link
import update_md_and_upload_html


if __name__ == '__main__':
    print(os.getcwd())
    update_md_and_upload_html.latest_modify_checker(print_flag=False)
    # up_list = new_from_md.main(1, sfd.main_info.info_dict, mod_date_flag=False, last_mod_flag=False,
    #                            upload_flag=False, first_time_flag=True, fixed_mod_date=False)
    up_list = new_from_md.main(1, sfd.main_info.info_dict, mod_date_flag=True, last_mod_flag=True,
                               upload_flag=False, first_time_flag=False, fixed_mod_date=False)
    sfd_move_up_html.main(up_list)
    check_dead_link.pick_up_inner_dead_link('sfd', 'up_html')
    new_up = []
    for x in up_list:
        if 'index.html' in x or 'sitemap.html' in x:
            new_up.append(x.replace('/html_files/', '/up_html/'))
        else:
            new_up.append(x.replace('/html_files/', '/up_html/').replace('.html', '/index.html'))
    new_up = list(set(new_up))
    print(new_up)
    file_upload.scp_upload(new_up, sfd.main_info.info_dict)
