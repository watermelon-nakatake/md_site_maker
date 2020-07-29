import pickle
import re
import csv
import datetime
import make_article_list


def make_mod_date_list():
    seen = []
    mod_list = []
    mod_log = make_article_list.read_pickle_pot('modify_log')
    mod_log.reverse()
    for log in mod_log:
        if log[0] not in seen:
            mod_list.append([log[0], datetime.datetime.strptime(log[1], '%Y-%m-%d'), log[3]])
            seen.append(log[0])
    print(mod_list)
    return mod_list


if __name__ == '__main__':
    print(make_article_list.read_pickle_pot('modify_log'))
    make_mod_date_list()
