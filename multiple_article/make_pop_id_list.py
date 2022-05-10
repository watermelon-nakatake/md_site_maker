import csv
import pickle
import pprint


def make_click_list():
    with open('sfd/page.csv') as f:
        reader = csv.reader(f)
        csv_list = [row for row in reader]
    # print(csv_list)
    pop_list = [x[0].replace('https://www.sefure-do.com/', '') for x in csv_list[1:]]
    # print(pop_list)
    with open('sfd/pickle_pot/main_data.pkl', 'rb') as p:
        p_dict = pickle.load(p)
    # print(p_dict)
    name_dict = {p_dict[x]['file_path'].replace('.html', '/'): x for x in p_dict}
    # pprint.pprint(name_dict)
    result = [[name_dict[x], x] for x in pop_list if x in name_dict]
    pprint.pprint(result)
    pop = [x[0] for x in result[:10]]
    imp = [x[0] for x in result[10:20]]
    print(pop)
    print(imp)


if __name__ == '__main__':
    make_click_list()

