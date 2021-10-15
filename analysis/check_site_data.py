import os
import pickle
import make_new_article


def check_all_key_data():
    counter = {}
    project_dict = make_new_article.dir_dict
    for pj in project_dict:
        print(pj)
        if os.path.exists(pj + '/pickle_pot/key_dict.pkl'):
            with open(pj + '/pickle_pot/key_dict.pkl', 'rb') as f:
                key_dict = pickle.load(f)
            # print(key_dict)
            if pj not in counter:
                counter[pj] = {}
            for page_name in key_dict:
                if key_dict[page_name]['type'] not in counter[pj]:
                    counter[pj][key_dict[page_name]['type']] = {'sub': [], 'obj': [], 'a_adj': [], 'act': []}
                for k in ['sub', 'obj', 'a_adj', 'act']:
                    if key_dict[page_name][k] not in counter[pj][key_dict[page_name]['type']][k]:
                        counter[pj][key_dict[page_name]['type']][k].append(key_dict[page_name][k])
                page_data = {'type': key_dict[page_name]['type'], 'sub': key_dict[page_name]['sub_key'],
                             'obj': key_dict[page_name]['obj_key'], 'a_adj': key_dict[page_name]['a_adj'],
                             'act': key_dict[page_name]['act']}
                # print(page_data)
            # print(len(key_dict))
    # print(counter)
    for pj_c in counter:
        for c_c in counter[pj_c]:
            print('\n{} : {}'.format(pj_c, c_c))
            # print(counter[pj_c][c_c])
            for k_c in counter[pj_c][c_c]:
                # print(counter[pj_c][c_c][k_c])
                if counter[pj_c][c_c][k_c]:
                    if len(counter[pj_c][c_c][k_c]) < 10:
                        print('    {}: {} - {}'.format(k_c, len(counter[pj_c][c_c][k_c]), str(counter[pj_c][c_c][k_c])))
                    else:
                        print('    {}: {} - {}'.format(k_c, len(counter[pj_c][c_c][k_c]),
                                                       str(counter[pj_c][c_c][k_c][:10]) + ' etc.'))

    # print(counter)


if __name__ == '__main__':
    check_all_key_data()
