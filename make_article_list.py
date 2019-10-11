# -*- coding: utf-8 -*-
import os
import re
import pickle
import csv
root_path = '/Users/nakataketetsuhiko/PycharmProjects/reibun_sf/'


def save_data_to_pickle(data, pickle_name):
    with open(root_path + 'pickle_pot/' + pickle_name + '.pkl', 'wb') as p:
        pickle.dump(data, p)


def make_file_data_list():
    dir_list = ['caption', 'majime', 'qa', 'site']
    data_list = []
    for directory in dir_list:
        file_list = os.listdir(root_path + 'reibun/pc/' + directory)
        for file_name in file_list:
            if '.html' in file_name:
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
                    data_list.append([directory + '/' + file_name, title, img_path])
    return data_list


def make_current_file_list():
    data_list = make_file_data_list()
    save_data_to_pickle(data_list, 'title_img_list')
    with open(root_path + 'pickle_pot/' + 'title_img_list.csv', 'w') as c:
        writer = csv.writer(c)
        for x in data_list:
            writer.writerow(x)


def read_pickle_pot(pkl_name):
    with open(root_path + 'pickle_pot/' + pkl_name, 'rb') as f:
        pk_dec = pickle.load(f)
    # print(pk_dec)
    return pk_dec


if __name__ == '__main__':
    make_current_file_list()
    # read_pickle_pot('title_img_list.pkl')
