import pickle
import random
import re
import difflib


def compare_key_for_relational_art(key_dict, relation_len):
    str_dict = {}
    # print(key_dict)
    result = {x: [] for x in list(range(len(key_dict)))}
    key_list = [
        [x, key_dict[x]['act_noun'], re.sub(r'<!--.*?-->', '', key_dict[x]['title_str']), key_dict[x]['dir_name']]
        for x in key_dict]
    num_list = range(len(key_list))
    for i in num_list:
        for j in num_list[i + 1:]:
            rate = difflib.SequenceMatcher(None, key_list[i][1], key_list[j][1]).ratio() * 100
            result[i].append([j, key_list[j][0], key_list[j][2], rate, key_list[j][1], key_list[j][3]])
            result[j].append([i, key_list[i][0], key_list[i][2], rate, key_list[i][1], key_list[j][3]])
    e_result = {x: sorted(result[x], key=lambda y: y[3], reverse=True) for x in result}
    for ii in e_result:
        str_list = []
        for ind in range(len(e_result[ii])):
            if ind < relation_len:
                this_r = e_result[ii][ind]
                if e_result[ii][ind][3] > 0:
                    str_list.append([this_r[1], this_r[2]])
                else:
                    c_num = relation_len - ind
                    str_list.extend([[x[1], x[2]] for x in random.sample(e_result[ii][ind:], c_num)])
                    break
        # print(len(str_list))
        random.shuffle(str_list)
        str_dict[key_list[ii][0]] = str_list
    out_dict = {y: ''.join('<li><a href="../{}.md">{}</a></li>'.format(x[0], x[1]) for x in str_dict[y]) for y in str_dict}
    # print(out_dict)
    return out_dict


if __name__ == '__main__':
    pj_dir = 'test'
    with open(pj_dir + '/pickle_pot/key_dict.pkl', 'rb') as rk:
        key_dict_t = pickle.load(rk)
    compare_key_for_relational_art(key_dict_t, 10)
