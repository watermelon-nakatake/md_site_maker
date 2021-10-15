import key_data.key_act

act_dict_s = key_data.key_act.act_dict_s
adj_dict_one = {
    0: {'a_adj': ''}
}

adj_dict_s = adj_dict_one
#     {
#     0: {'a_adj': 'ワクワクメールで', 'site': 'wk'},
#     1: {'a_adj': 'ハッピーメールで', 'site': 'hm'},
#     2: {'a_adj': 'PCMAXで', 'site': 'pc'},
#     3: {'a_adj': 'Jメールで', 'site': 'mj'}
# }

act_dict = act_dict_s
# act_dict = {x: act_dict[x] for x in act_dict if 'sf' not in act_dict[x]['ignore_a']}

repeat_num = 1
key_list = [y for y in adj_dict_s]
for n in range(repeat_num):
    pop_n = key_list.pop(0)
    key_list.append(pop_n)
adj_dict = {i: adj_dict_s[y] for i, y in enumerate(key_list)}
if len(act_dict) >= len(adj_dict):
    key_data1 = act_dict_s
    key_data2 = adj_dict
    ud_flag = ['key_a', 'key_b']
else:
    key_data1 = adj_dict_s
    key_data2 = act_dict
    ud_flag = ['key_b', 'key_a']
result_list = {}
used_list = []
i = 0
for id1 in key_data1:
    if i < len(key_data2):
        pass
    else:
        i = 0
    result_list[id1] = key_data1[id1] | key_data2[i] | {'type': 'mix_act',
                                                        'all_key': key_data2[i]['a_adj'] + key_data1[id1]['act']}
    used_list.append(['{}_{}'.format(ud_flag[0], id1), '{}_{}'.format(ud_flag[1], i)])
    i += 1
key_dict = result_list

# print(result_list)
# print(used_list)
