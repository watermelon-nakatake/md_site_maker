import glob
import pickle
import pprint
import importlib
import file_upload
import make_new_article


def upload_in_order(select_pj):
    error_files = {}
    upload_file = {}
    # with open('pickle_data/upload_leak.pkl', 'rb') as rp:
    #     upload_file = pickle.load(rp)
    if not upload_file:
        upload_file = {}
        if select_pj:
            pj_list = select_pj
        else:
            pj_list = [x for x in make_new_article.dir_dict if x not in ['sfd', 'test', 'mass']][4:]
        for pj_name in pj_list:
            upload_file[pj_name] = [x for x in glob.glob(pj_name + '/html_files/**/**.html', recursive=True) if
                                    '_test' not in x and '_copy' not in x]
    for u_pj in upload_file:
        if u_pj == 'shoshin':
            er_files = file_upload.shoshin_scp_upload(upload_file['shoshin'])
        else:
            info_mod = importlib.import_module(u_pj + '.main_info')
            pd = info_mod.info_dict
            er_files = file_upload.scp_upload(upload_file[u_pj], pd)
        if er_files:
            error_files[u_pj] = er_files
    if error_files:
        pprint.pprint(error_files)
        with open('pickle_data/upload_leak.pkl', 'wb') as p:
            pickle.dump(error_files, p)


if __name__ == '__main__':
    upload_in_order([])
