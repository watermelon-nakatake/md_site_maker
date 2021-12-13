import file_upload
import new_from_md
import shoshin.main_info
import make_html_for_shoshin

import make_new_article

if __name__ == '__main__':
    make_new_article.make_md_by_project_and_part('shoshin', [], '', 0)
    up_files = make_html_for_shoshin.translate_md_to_html('shoshin/html_files/template/wp_temp.html',
                                                          [], 'man', pub_flag=False, pub_take_over=True)
    up_files.append('shoshin/html_files/a_sitemap.xml')
    file_upload.shoshin_scp_upload(up_files)
