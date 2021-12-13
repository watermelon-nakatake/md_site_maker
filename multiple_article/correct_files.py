import pickle


def delete_pk_dict(pj_name, del_num):
    with open(pj_name + '/pickle_pot/key_dict.pkl', 'rb') as f:
        key_dict = pickle.load(f)
        key_dict = {x: key_dict[x] for x in key_dict if key_dict[x]['page_id'] < del_num}
        print(key_dict)
        with open(pj_name + '/pickle_pot/key_dict.pkl', 'wb') as g:
            pickle.dump(key_dict, g)
    with open(pj_name + '/pickle_pot/main_data.pkl', 'rb') as h:
        main_dict = pickle.load(h)
        main_dict = {x: main_dict[x] for x in main_dict if x < del_num}
        print(main_dict)
        with open(pj_name + '/pickle_pot/main_data.pkl', 'wb') as i:
            pickle.dump(main_dict, i)


if __name__ == '__main__':
    delete_pk_dict('howto', 481)
