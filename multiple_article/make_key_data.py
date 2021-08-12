import csv


def make_key_dict_from_csv(file_name, new_file_name, common_dict):
    with open('/Users/tnakatake/Downloads/' + file_name) as f:
        reader = csv.reader(f)
        csv_list = [row for row in reader]
    csv_list = [x for x in csv_list if x]
    # print(csv_list)
    new_dict = {}
    for i, row in enumerate(csv_list[1:]):
        if len(csv_list[0]) == len(row):
            insert_dict = {}
            for ii, data_i in enumerate(row):
                if 'eng' in csv_list[0][ii]:
                    insert_dict[csv_list[0][ii]] = data_i.replace(' ', '_')
                else:
                    insert_dict[csv_list[0][ii]] = data_i
            insert_dict.update(common_dict)
            new_dict[i] = insert_dict
    print(new_dict)
    if new_file_name:
        py_str = 'key_dict = ' + str(new_dict)
        with open('multiple_article/key_data/' + new_file_name + '.py', 'w', encoding='utf-8') as g:
            g.write(py_str)


if __name__ == '__main__':
    make_key_dict_from_csv('new_key - sub_m.csv', '', {'type': 'only_sub'})
