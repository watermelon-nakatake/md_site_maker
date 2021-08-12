import csv


def read_keyword_csv(csv_path, remove_list):
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.reader(f)
        csv_list = [row for row in reader]
    # print(csv_list)
    vol_list = [[x[0], x[2]] for x in csv_list]
    vol_list.sort(key=lambda y: int(y[1]), reverse=True)
    # print(vol_list)
    for row in vol_list:
        sp_l = row[0].split(' ')
        for r_str in remove_list:
            if r_str in sp_l:
                sp_l.remove(r_str)
        if sp_l:
            print(sp_l)


if __name__ == '__main__':
    read_keyword_csv('/Users/tnakatake/Downloads/deaik.csv',
                     ['出会い系', '出会い', '系', '出逢い系', 'ふれ'])

