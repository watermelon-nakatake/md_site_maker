import pickle
import pprint


def main(pj_name):
    with open(pj_name + '/pickle_pot/main_data.pkl', 'rb') as p:
        pk_dict = pickle.load(p)
        pprint.pprint(pk_dict)


if __name__ == '__main__':
    main('rei_site')
