import os
import glob
import time
import file_upload
import make_article_list
import reibun.main_info


def search_update_file(pd):
    last_upload = make_article_list.read_pickle_pot('last_md_mod', pd)
    all_files = [x for x in glob.glob(pd['project_dir'] + '/html_files/**/**', recursive=True) if '_copy' not in x
                 and '_test' not in x and '/template' not in x and '.cgi' not in x]
    update_files = [x for x in list(set(all_files)) if os.path.getmtime(x) > last_upload and os.path.isfile(x)]
    print(update_files)
    file_upload.scp_upload(update_files, pd)


if __name__ == '__main__':
    p_d = reibun.main_info.info_dict
    search_update_file(p_d)
