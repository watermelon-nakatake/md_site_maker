import key_data.key_act

project_name = 'rei_site'

a_adj_data = {'joshideai': {'adj_dict': 'site_name', 'slide_num': 1},
              'rei_site': {'adj_dict': 'site_name', 'slide_num': 0}}
adj_dict = {
    'site_name': {
        0: {'a_adj': 'ワクワクメールで', 'site': 'wk'},
        1: {'a_adj': 'ハッピーメールで', 'site': 'hm'},
        2: {'a_adj': 'PCMAXで', 'site': 'pc'},
        3: {'a_adj': 'Jメールで', 'site': 'mj'}
    },
    'none': {0: {'a_adj': ''}},
    'make_sf_and': {0: {'a_adj': 'セフレを作って'}}
}

act_dict = key_data.key_act.act_dict_s
adj_dict_s = adj_dict[a_adj_data[project_name]['adj_dict']]
if project_name == 'sfd':
    act_dict = {x: act_dict[x] for x in act_dict if 'sf' not in act_dict[x]['ignore_a']}

if len(adj_dict[a_adj_data[project_name]['adj_dict']]) > 1:
    slide_num = a_adj_data[project_name]['slide_num']
    key_list = [y for y in adj_dict_s]
    if slide_num > 0:
        for n in range(slide_num):
            pop_n = key_list.pop(0)
            key_list.append(pop_n)
    adj_dict = {i: adj_dict_s[y] for i, y in enumerate(key_list)}
    if len(act_dict) >= len(adj_dict):
        key_data1 = act_dict
        key_data2 = adj_dict
        ud_flag = ['key_a', 'key_b']
    else:
        key_data1 = adj_dict
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
else:
    key_dict = {x: act_dict[x].update(adj_dict_s) for x in act_dict}

# print(key_dict)
# print(result_list)
# print(used_list)
