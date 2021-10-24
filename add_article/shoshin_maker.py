import file_upload
import new_from_md
import shoshin.main_info
import make_html_for_shoshin

# import make_new_article

if __name__ == '__main__':
    # make_new_article.make_md_by_project_and_part('shoshin', [], '', 0)
    up_files = make_html_for_shoshin.translate_md_to_html('shoshin/html_files/template/wp_temp.html',
                                                          'shoshin/md_files/beginner', 'man', pub_flag=False,
                                                          pub_take_over=False, html_dir='beginner')
    file_upload.shoshin_scp_upload(up_files)
