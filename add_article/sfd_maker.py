import file_upload
import new_from_md
import sfd.main_info
import make_html_for_shoshin
import datetime
import sfd_move_up_html
import check_dead_link

import make_new_article

if __name__ == '__main__':
    new_from_md.main(1, sfd.main_info.info_dict, mod_date_flag=True, last_mod_flag=True,
                     upload_flag=False, first_time_flag=True, fixed_mod_date=False)
    sfd_move_up_html.main()
    check_dead_link.pick_up_inner_dead_link('sfd', 'up_html')

    # mod_list = ['sfd/md_files/friend-with-benefits/area-bbs/01-hokkaido.md']
    # now = datetime.datetime.now()
    # pd = sfd.main_info.info_dict
    # new_from_md.import_from_markdown(mod_list, 0, now, pd, mod_flag=True, first_time_flag=True, fixed_mod_date=False)

    # make_new_article.make_md_by_project_and_part('shoshin', [], '', 0)
    # up_files = make_html_for_shoshin.translate_md_to_html('shoshin/html_files/template/wp_temp.html',
    #                                                       [], 'man', pub_flag=False, pub_take_over=True)
    # up_files.append('shoshin/html_files/a_sitemap.xml')
    # file_upload.shoshin_scp_upload(up_files)
