import make_article_list
import reibun.main_info


def make_new_main_data_pkl(pd):
    old_pkl = make_article_list.read_pickle_pot('main_data', pd)
    print(old_pkl)
    new_pkl = {}
    for x in old_pkl:
        new_pkl[x] = {'file_path': old_pkl[x][0],
                      'title': old_pkl[x][1],
                      'pub_date': old_pkl[x][2],
                      'mod_date': old_pkl[x][3],
                      'category': old_pkl[x][4],
                      'description': old_pkl[x][5],
                      'str_len': old_pkl[x][6],
                      'layout_flag': old_pkl[x][7],
                      'shift_flag': old_pkl[x][8]}
    make_article_list.save_data_to_pickle(new_pkl, 'main_data', pd)
    print(new_pkl)


if __name__ == '__main__':
    # make_new_main_data_pkl()
    # change_pk_dic()
    print(make_article_list.read_pickle_pot('main_data', reibun.main_info.info_dict))
