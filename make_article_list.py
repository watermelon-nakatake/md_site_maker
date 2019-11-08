# -*- coding: utf-8 -*-
import os
import re
import pickle
import common_tool

root_path = '/Users/nakataketetsuhiko/PycharmProjects/reibun_sf/'


def save_data_to_pickle(data, pickle_name):
    with open(root_path + 'pickle_pot/' + pickle_name + '.pkl', 'wb') as p:
        pickle.dump(data, p)


def make_file_data_list():
    dir_list = ['policy', 'caption', 'majime', 'qa', 'site']
    data_list = {}
    for directory in dir_list:
        file_list = os.listdir(root_path + 'reibun/pc/' + directory)
        for file_name in file_list:
            if '.html' in file_name and '_test' not in file_name and '_copy' not in file_name:
                category = common_tool.search_category(directory, file_name)
                with open(root_path + 'reibun/pc/' + directory + '/' + file_name, 'r', encoding='utf-8') as f:
                    long_str = f.read()
                    title_m = re.findall(r'<h1 itemprop="headline alternativeHeadline name">(.+?)</h1>', long_str)
                    if title_m:
                        title = title_m[0]
                    img_m = re.findall(r'<div class="alt_img_t"><img src="(.+?)" alt=', long_str)
                    if img_m:
                        img_path = img_m[0]
                    else:
                        img_path = ''
                    mod_m = re.findall(r'<time itemprop="dateModified" datetime="(.+?)">', long_str)
                    if mod_m:
                        mod_time = mod_m[0]
                    data_list[directory + '/' + file_name] = [title, img_path, mod_time, category]
    return data_list


def make_current_file_list():
    new_data_list = make_file_data_list()
    # print(new_data_list)
    # old_data_list = {}
    old_data_list = read_pickle_pot('title_img_list')
    old_path_list = [old_data_list[x][0] for x in old_data_list]
    for new_path in new_data_list:
        for old_id in old_data_list:
            if old_data_list[old_id][0] == new_path:
                old_data_list[old_id] = [new_path, new_data_list[new_path][0], new_data_list[new_path][1],
                                         new_data_list[new_path][2], new_data_list[new_path][3]]
                break
        if new_path not in old_path_list:
            old_data_list[len(old_data_list)] = [new_path, new_data_list[new_path][0], new_data_list[new_path][1],
                                                 new_data_list[new_path][2], new_data_list[new_path][3]]
            # print(str(len(old_data_list)) + ': ' + new_path, new_data_list[new_path][0] + new_data_list[new_path][1]
            #      + new_data_list[new_path][2] + new_data_list[new_path][3])
    print(old_data_list)
    save_data_to_pickle(old_data_list, 'title_img_list')
    save_text_file(old_data_list)


def save_text_file(data_dec):
    result_str = ''
    for data_id in data_dec:
        result_str += str(data_id) + '  ' + ' '.join(data_dec[data_id]) + '\n'
    with open(root_path + 'pickle_pot/title_img_list.txt', 'w', encoding='utf-8') as f:
        f.write(result_str)


def read_pickle_pot(pkl_name):
    with open(root_path + 'pickle_pot/' + pkl_name + '.pkl', 'rb') as f:
        pk_dec = pickle.load(f)
    # print(pk_dec)
    return pk_dec


def change_pickle(file_name, num_str, new_data):
    pk_data = read_pickle_pot(file_name)
    print(pk_data)
    print(pk_data[num_str])
    if new_data == 'delete':
        del pk_data[num_str]
    else:
        pk_data[num_str] = new_data
    print(pk_data)
    save_data_to_pickle(pk_data, file_name)


def add_to_pk_list():
    pk_dec = read_pickle_pot('title_img_list')
    for p_id in pk_dec:
        with open('reibun/pc/' + pk_dec[p_id][0], 'r', encoding='utf-8') as f:
            long_str = f.read()
            desc_l = re.findall('<meta name="description" content="(.*?)">', long_str)
            if desc_l:
                desc_str = desc_l[0]
            else:
                desc_str = ''
            pk_dec[p_id].append(desc_str)
            if len(pk_dec[p_id]) < 6:
                print('error : ' + pk_dec[p_id][0])
    print(pk_dec)
    save_data_to_pickle(pk_dec, 'title_img_list')


if __name__ == '__main__':
    # make_current_file_list()
    # add_to_pk_list()
    print(read_pickle_pot('title_img_list'))
    print(read_pickle_pot('modify_log'))
    # change_pickle('title_img_list', 140, 'delete')
