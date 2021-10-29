import csv
import key_data.key_source
from googletrans import Translator
import difflib
import key_data.key_obj_man
import key_data.key_obj_woman
import key_data.key_adj_act
import key_data.key_sub_man
import key_data.key_adj


def make_key_dict_from_csv(file_name, new_file_name, common_dict, start_num, start_row):
    with open('/Users/tnakatake/Downloads/' + file_name) as f:
        reader = csv.reader(f)
        csv_list = [row for row in reader]
    csv_list = [x for x in csv_list if x]
    # print(csv_list)
    new_dict = {}
    used_key = []
    used_eng = []
    if 'eng' in csv_list[0]:
        eng_num = csv_list[0].index('eng')
    else:
        eng_num = 0
    if start_row:
        slice_num = start_row - 1
    else:
        slice_num = 1
    for i, row in enumerate(csv_list[slice_num:]):
        if row[0]:
            if len(csv_list[0]) == len(row):
                if row[0] not in used_key:
                    insert_dict = {}
                    for ii, data_i in enumerate(row):
                        if ii == 0 and data_i not in used_key:
                            used_key.append(data_i)
                        if eng_num != 0 and ii == eng_num:
                            if data_i not in used_eng:
                                if not data_i.isascii():
                                    print('ascii error {}'.format(row))
                                insert_dict['eng'] = data_i.replace(' ', '_').replace('-', '_')
                                used_eng.append(data_i.replace(' ', '_').replace('-', '_'))
                            elif not data_i:
                                insert_dict['eng'] = ''
                            else:
                                print('error! : {} in eng list !!'.format(data_i))
                        elif data_i == 'FALSE':
                            insert_dict[csv_list[0][ii]] = False
                        elif data_i == 'TRUE':
                            insert_dict[csv_list[0][ii]] = True
                        elif data_i in ['0', '1', '3']:
                            insert_dict[csv_list[0][ii]] = int(data_i)
                        else:
                            insert_dict[csv_list[0][ii]] = data_i
                        if 'act' in file_name:
                            if ii == 6 and not data_i:
                                insert_dict[csv_list[0][ii]] = 'a'
                            if ii == 7:
                                if data_i:
                                    insert_dict[csv_list[0][ii]] = [data_i]
                                else:
                                    insert_dict[csv_list[0][ii]] = [data_i]
                            if ii == 8 and not data_i:
                                insert_dict[csv_list[0][ii]] = 'と'
                            if ii == 9:
                                insert_dict[csv_list[0][ii]] = False
                            if ii == 12:
                                insert_dict[csv_list[0][ii]] = int(insert_dict[csv_list[0][ii]])
                    insert_dict.update(common_dict)
                    new_dict[i + start_num] = insert_dict
                else:
                    print('{} : {} already in list !'.format(i + 2, row[0]))
    print(new_dict)
    if new_file_name:
        py_str = 'key_dict = ' + str(new_dict)
        with open('multiple_article/key_data/' + new_file_name + '.py', 'w', encoding='utf-8') as g:
            g.write(py_str)
    return new_dict


def import_english_str(insert_list, reference_dict, target_key):
    result = {}
    used_eng = [reference_dict[y]['eng'] for y in reference_dict]
    r_dict = {reference_dict[x][target_key]: reference_dict[x]['eng'] for x in reference_dict}
    # print(r_dict)
    translator = Translator()
    for row_i in insert_list:
        row = insert_list[row_i]
        if not row['eng']:
            if row[target_key] in r_dict:
                row['eng'] = r_dict[row[target_key]].lower().replace(' ', '_')
                # print('{} :  {}'.format(row[target_key], row['eng']))
            else:
                row['eng'] = translator.translate(row[target_key], src="ja", dest="en").text.lower().replace(' ', '_')
                print('{} :  {}'.format(row[target_key], row['eng']))
        elif ' ' in row['eng']:
            row['eng'] = row['eng'].replace(' ', '_')
        elif '-' in row['eng']:
            row['eng'] = row['eng'].replace('-', '_')
        if row['eng'] not in used_eng:
            used_eng.append(row['eng'])
        else:
            if row['eng'] + '2' not in used_eng:
                row['eng'] = row['eng'] + '2'
                used_eng.append(row['eng'])
            elif row['eng'] + '3' not in used_eng:
                row['eng'] = row['eng'] + '3'
                used_eng.append(row['eng'])
            else:
                print('error!!')
        if not row['eng'].isascii():
            print('eng error!! {}'.format(row))
        result[row_i] = row
    return result


def write_csv_file(t_dict, file_path):
    t_list = [[t_dict[x][y] for y in t_dict[x]] for x in t_dict]
    with open(file_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(t_list)


def translate_ja_to_eng():
    translator = Translator()
    result = translator.translate('みかん', src="ja", dest="en")
    print(result.text)
    r2 = translator.translate('りんご', src="ja", dest="en")
    print(r2.text)


def match_list():
    a_dict = key_data.key_obj_man.keyword_dict
    b_dict = key_data.key_obj_man.keyword_dict
    for i_num in a_dict:
        a_dict[i_num]['eng'] = b_dict[i_num]['eng']
        a_dict[i_num]['o_adj'] = b_dict[i_num]['adj']
    print(a_dict)


def check_duplicate_keyword(new_dict, existing_dict):
    result = {}
    used_list = [existing_dict[x]['all_key'] for x in existing_dict]
    n_num = len(existing_dict)
    for n_id in new_dict:
        if new_dict[n_id]['all_key'] in used_list:
            print('same key : ' + new_dict[n_id]['all_key'])
        else:
            for e_id in existing_dict:
                if new_dict[n_id]['all_key'] in existing_dict[e_id]['all_key']:
                    print(new_dict[n_id]['all_key'] + '  in  ' + existing_dict[e_id]['all_key'])
                elif existing_dict[e_id]['all_key'] in new_dict[n_id]['all_key']:
                    print(existing_dict[e_id]['all_key'] + '  in  ' + new_dict[n_id]['all_key'])
                r = difflib.SequenceMatcher(None, new_dict[n_id]['all_key'], existing_dict[e_id]['all_key']).ratio()
                if r > 0.5:
                    print('near : {} and {}'.format(new_dict[n_id]['all_key'], existing_dict[e_id]['all_key']))
            result[n_num] = new_dict[n_id]
            used_list.append(new_dict[n_id]['all_key'])
            n_num += 1
    print(result)


if __name__ == '__main__':
    i_dict = make_key_dict_from_csv('new_key - obj_m.csv', '', {'type': 'only_obj'}, 321, start_row=114)
    check_duplicate_keyword(i_dict, key_data.key_obj_woman.keyword_dict)
    # o_dict = import_english_str(i_dict, key_data.key_obj_woman.keyword_dict, 'all_key')
    # write_csv_file(o_dict, 'multiple_article/key_data/key_obj_m2.csv')
