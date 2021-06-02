from add_article import make_article_list
import re


def preparation_for_new_project():
    change_pk_dic()


def change_pk_dic():
    pk_dic = make_article_list.read_pickle_pot('main_data')
    # print(pk_dic)
    pk_dic[144] = pk_dic[146]
    del pk_dic[146]
    print(pk_dic)
    make_article_list.save_data_to_pickle(pk_dic, 'main_data')


def insert_pub_date():
    pk_dic = make_article_list.read_pickle_pot('main_data')
    for id_p in pk_dic:
        print(pk_dic[id_p])
        with open('reibun/html_files/pc/' + pk_dic[id_p]['file_path'], 'r', encoding='utf-8') as f:
            long_str = f.read()
            pub_str_l = re.findall(r'<time itemprop="datePublished" datetime="(.+?)">', long_str)
            if pub_str_l:
                pub_str = pub_str_l[0]
            else:
                raise Exception
            pk_dic[id_p]['pub_date'] = pub_str
    print(pk_dic)
    for id_q in pk_dic:
        print(pk_dic[id_q]['pub_date'])
    # make_article_list.save_data_to_pickle(pk_dic, 'main_data')


def insert_id_and_category_to_html():
    pk_dic = make_article_list.read_pickle_pot('main_data')
    for id_p in pk_dic:
        with open('reibun/html_files/pc/' + pk_dic[id_p]['file_path'], 'r', encoding='utf-8') as f:
            long_str = f.read()
            long_str = long_str.replace('<head><!-- Global site tag (gtag.js) -->',
                                        '<head><!--id_num_' + str(id_p) + '--><!--category_' + pk_dic[id_p]['category']
                                        + '--><!-- Global site tag (gtag.js) -->')
            with open('reibun/html_files/pc/' + pk_dic[id_p]['file_path'], 'w', encoding='utf-8') as g:
                g.write(long_str)


if __name__ == '__main__':
    # make_new_main_data_pkl()
    # change_pk_dic()
    # insert_pub_date()
    insert_id_and_category_to_html()
    print(make_article_list.read_pickle_pot('main_data'))
