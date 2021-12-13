import pickle
import pprint


def main(pj_name, file_id):
    file_list = ['main_data', 'key_dict']
    file_name = file_list[file_id]
    with open('{}/pickle_pot/{}.pkl'.format(pj_name, file_name), 'rb') as p:
        pk_dict = pickle.load(p)
        pprint.pprint(pk_dict)
    # pprint.pprint([[pk_dict[x]['title'], pk_dict[x]['file_path']] for x in pk_dict])
    # pprint.pprint([pk_dict[x]['title'] for x in pk_dict])


if __name__ == '__main__':
    main('shoshin', 1)
