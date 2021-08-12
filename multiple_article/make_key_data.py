import csv
import key_data.key_source
from googletrans import Translator


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
    return new_dict


def import_english_str(insert_list, reference_dict):
    r_dict = {reference_dict[x]['obj_key']: reference_dict[x]['eng'] for x in reference_dict}
    # print(r_dict)
    translator = Translator()
    for row_i in insert_list:
        row = insert_list[row_i]
        if not row['eng'] and row['obj_key'] in r_dict:
            row['eng'] = r_dict[row['obj_key']]
            # print('{} :  {}'.format(row['obj_key'], row['eng']))
        if not row['eng']:
            row['eng'] = translator.translate(row['obj_key'], src="ja", dest="en").text
            print('{} :  {}'.format(row['obj_key'], row['eng']))


def translate_ja_to_eng():
    translator = Translator()
    result = translator.translate('みかん', src="ja", dest="en")
    print(result.text)
    r2 = translator.translate('りんご', src="ja", dest="en")
    print(r2.text)


if __name__ == '__main__':
    i_dict = make_key_dict_from_csv('new_key - obj_w.csv', '', {'type': 'only_sub'})
    import_english_str(i_dict, key_data.key_source.keyword_dict)
