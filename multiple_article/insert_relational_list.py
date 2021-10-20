import pickle
import random
import re
import difflib


def compare_key_for_relational_art(key_dict, relation_len):
    str_dict = {}
    # print(key_dict)
    title_dict = {x: re.sub(r'<!--.*?-->', '', key_dict[x]['title_str'])
                  for x in key_dict}
    count_dict = {x: 0 for x in key_dict}
    # print(title_dict)
    result = {x: [] for x in key_dict}
    key_list = [[x, key_dict[x]['act_noun']] for x in key_dict]
    # print(key_list)
    num_list = range(len(key_list))
    for i in num_list:
        for j in num_list[i + 1:]:
            rate = difflib.SequenceMatcher(None, key_list[i][1], key_list[j][1]).ratio() * 100
            result[key_list[i][0]].append([key_list[j][0], rate])
            result[key_list[j][0]].append([key_list[i][0], rate])
    e_result = {x: sorted(result[x], key=lambda y: y[1], reverse=True) for x in result}
    # print(e_result)
    er_name_list = [x for x in e_result]
    random.shuffle(er_name_list)
    # print(er_name_list)
    for p_name in er_name_list:
        str_list = []
        for ind in range(relation_len):
            if e_result[p_name][ind][1] > 0 and count_dict[e_result[p_name][ind][0]] < relation_len + 5:
                str_list.append([e_result[p_name][ind][0], title_dict[e_result[p_name][ind][0]]])
                count_dict[e_result[p_name][ind][0]] += 1
        str_dict[p_name] = str_list
    # print(str_dict)
    # print(count_dict)
    minor_list = [x for x in count_dict if count_dict[x] < 10]
    # print(minor_list)
    # count_list = [[x, count_dict[x]] for x in count_dict]
    # count_list.sort(key=lambda x: x[1], reverse=True)
    # print(count_list)
    for row in str_dict:
        if len(str_dict[row]) < 15:
            str_dict[row].extend([[x, title_dict[x]] for x in random.sample(minor_list, 15 - len(str_dict[row]))])
        # print(len(str_dict[row]))
    # print(str_dict)
    # minor_counter(key_dict, str_dict)
    out_dict = {y: ''.join(['<li><a href="../{}.md">{}</a></li>'.format(x[0], x[1]) for x in str_dict[y]]) for y in str_dict}
    # print(out_dict)
    return out_dict


def minor_counter(key_dict, target_dict):
    counter_dict = {x: 0 for x in key_dict}
    for row in target_dict:
        for t in target_dict[row]:
            counter_dict[t[0]] += 1
    # print(counter_dict)
    counter_list = [[x, counter_dict[x]] for x in counter_dict]
    counter_list.sort(key=lambda x: x[1], reverse=True)
    print(counter_list)


if __name__ == '__main__':
    pj_dir = 'test'
    with open(pj_dir + '/pickle_pot/key_dict.pkl', 'rb') as rk:
        key_dict_t = pickle.load(rk)
    # print(len(key_dict_t))
    compare_key_for_relational_art(key_dict_t, 15)
