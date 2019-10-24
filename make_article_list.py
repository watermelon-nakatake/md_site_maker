# -*- coding: utf-8 -*-
import os
import re
import pickle

root_path = '/Users/nakataketetsuhiko/PycharmProjects/reibun_sf/'


def save_data_to_pickle(data, pickle_name):
    with open(root_path + 'pickle_pot/' + pickle_name + '.pkl', 'wb') as p:
        pickle.dump(data, p)


def search_category(directory, file_name):
    if directory != 'majime':
        category = directory
    else:
        if 'm0' in file_name:
            category = 'post'
        elif 'mp_' in file_name:
            category = 'profile'
        elif 'm1' in file_name:
            category = 'f_mail'
        elif 'm2' in file_name:
            category = 's_mail'
        elif 'm3' in file_name:
            category = 'date'
        elif 'm4' in file_name:
            category = 'how_to'
        elif 't0_' in file_name:
            category = 'post'
        else:
            category = 'majime'
    return category


def make_file_data_list():
    dir_list = ['policy', 'caption', 'majime', 'qa', 'site']
    data_list = {}
    for directory in dir_list:
        file_list = os.listdir(root_path + 'reibun/pc/' + directory)
        for file_name in file_list:
            if '.html' in file_name and '_test' not in file_name and '_copy' not in file_name:
                category = search_category(directory, file_name)
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


if __name__ == '__main__':
    # make_current_file_list()
    print(read_pickle_pot('title_img_list'))
