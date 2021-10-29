import os
import pickle
import pprint

import make_new_article


def check_all_key_data():
    counter = {}
    project_dict = make_new_article.dir_dict
    del project_dict['test']
    for pj in project_dict:
        # print(pj)
        if os.path.exists(pj + '/pickle_pot/key_dict.pkl'):
            with open(pj + '/pickle_pot/key_dict.pkl', 'rb') as f:
                key_dict = pickle.load(f)
            # print(key_dict)
            if pj not in counter:
                counter[pj] = {}
            for page_name in key_dict:
                this_sex = key_dict[page_name]['sub_sex']
                this_type = key_dict[page_name]['type']
                if this_type not in counter[pj]:
                    counter[pj][this_type] = {}
                if this_sex not in counter[pj][this_type]:
                    counter[pj][this_type][this_sex] = {'sub': [], 'obj': [], 'a_adj': [], 'act': []}
                for k in ['sub', 'obj', 'a_adj', 'act']:
                    if key_dict[page_name][k] not in counter[pj][this_type][this_sex][k]:
                        counter[pj][this_type][this_sex][k].append(key_dict[page_name][k])
                # page_data = {'type': key_dict[page_name]['type'], 'sub': key_dict[page_name]['sub_key'],
                #              'obj': key_dict[page_name]['obj_key'], 'a_adj': key_dict[page_name]['a_adj'],
                #              'act': key_dict[page_name]['act']}
                # print(page_data)
            # print(len(key_dict))
    # print(counter)
    summary = {}
    for pj_c in counter:
        if pj_c not in summary:
            summary[pj_c] = {}
        for c_c in counter[pj_c]:
            for s_c in counter[pj_c][c_c]:
                num_counter = []
                print('\n{} : {} - {}'.format(pj_c, c_c, s_c))
                # print(counter[pj_c][c_c])
                for k_c in counter[pj_c][c_c][s_c]:
                    # print(counter[pj_c][c_c][s_c][k_c])
                    if counter[pj_c][c_c][s_c][k_c]:
                        if len(counter[pj_c][c_c][s_c][k_c]) < 10:
                            print('    {}: {} - {}'.format(k_c, len(counter[pj_c][c_c][s_c][k_c]),
                                                           str(counter[pj_c][c_c][s_c][k_c])))
                        else:
                            print('    {}: {} - {}'.format(k_c, len(counter[pj_c][c_c][s_c][k_c]),
                                                           str(counter[pj_c][c_c][s_c][k_c][:10]) + ' etc.'))
                        num_counter.append(len(counter[pj_c][c_c][s_c][k_c]))
                summary[pj_c]['{} - {}'.format(c_c, s_c)] = max(num_counter)
        summary[pj_c]['sum'] = sum([summary[pj_c][x] for x in summary[pj_c]])
    print('\n')
    pprint.pprint(summary, width=40)
    return summary


if __name__ == '__main__':
    check_all_key_data()
