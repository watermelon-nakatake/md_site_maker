import os
import glob
import time
import reibun_upload
import make_article_list


def search_update_file():
    last_upload = make_article_list.read_pickle_pot('last_upload')
    all_files = glob.glob('reibun/**/**', recursive=True)
    print(all_files)
    update_files = [x for x in list(set(all_files)) if os.path.getmtime(x) > last_upload and os.path.isfile(x)]
    print(update_files)
    reibun_upload.scp_upload(update_files)
    last_upload = time.time()
    make_article_list.save_data_to_pickle(last_upload, 'last_upload')


if __name__ == '__main__':
    search_update_file()
