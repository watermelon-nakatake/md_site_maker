import csv
import pprint
import re
import pickle
import sd_check_mod_date


def pick_up_all_article():
    with open('sfd/all_urls.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        c_list_b = [x for x in reader]
        c_list_b[0][0] = c_list_b[0][0].replace('\ufeff', '')
    c_list_b.sort(key=lambda x: int(x[0]))
    c_list = [['/' + re.sub(r'https://www\.sefure-do.com/.+?/', '', x[2]), int(x[0]), x[1], x[2]] if '/area-bbs/' not in x[2]
              else ['/' + re.sub(r'https://www\.sefure-do.com/.+?/area-bbs/', '', x[2]), int(x[0]), x[1], x[2]] for x in c_list_b]
    # print(c_list)
    with open('sfd/pickle_pot/scrape_data.pkl', 'rb') as q:
        scr_dict = pickle.load(q)
    irregular_img = [x for x in scr_dict if not scr_dict[x]['img_pos']]
    irregular_img = ['/' + re.sub(r'https://www\.sefure-do.com/.+?/', '', x) for x in irregular_img]
    # print(irregular_img)
    with open('sfd/page_data.csv', 'r', encoding='utf-8') as p:
        reader_p = csv.reader(p)
        p_list = [x for x in reader_p]
    # pprint.pprint(p_list)
    page_dict = {}
    for p_data in p_list[1:]:
        p_str = re.sub(r'^.+/(.+)/', r'/\1/', p_data[0])
        if not p_str.endswith('/'):
            p_str = p_str.replace('/friend-with-benefits', '') + '/'
        if p_str == '/www.sefure-do.com/':
            p_str = '/'
        if p_str not in page_dict:
            page_dict[p_str] = [int(p_data[2]), int(p_data[1])]
        else:
            page_dict[p_str] = [int(p_data[2]) + page_dict[p_str][0], int(p_data[1]) + page_dict[p_str][1]]
    # pprint.pprint(page_dict)
    # no_dis_list = [x[0] for x in c_list if x[0] not in page_dict and x[1] < 3440]
    # for p_str in no_dis_list:
    #     print('https://www.sefure-do.com/friend-with-benefits' + p_str)
    # pprint.pprint(no_dis_list)
    # pages = [[re.sub(r'^.+/(.+)/', r'/\1/', x[0]), x[2]] for x in p_list[1:]]
    # print(pages)
    # click = [x[0] for x in p_list[1:] if int(x[1]) > 0]
    # no_dis = [x for x in c_list if x not in pages and int(x[0]) < 3440]
    # pprint.pprint(no_dis)
    # print(len(no_dis))
    # new_dis = [x[2] for x in c_list if x[2] not in click and int(x[0]) >= 3440]
    # pprint.pprint(new_dis)
    # print(len(new_dis))

    long_title = [[x[1], x[2], len(x[1])] for x in c_list_b if len(x[1]) > 30]
    long_title.sort(key=lambda x: x[2], reverse=True)
    # pprint.pprint(long_title)

    page_list = [[x, page_dict[x][0], page_dict[x][1]] for x in page_dict]
    o_page_list = sorted(page_list, key=lambda x: int(x[2]), reverse=True)
    # pprint.pprint(o_page_list)

    with open('gsc_data/sfd/month2022-02-05.csv', 'r', encoding='utf-8') as g:
        q_read = csv.reader(g)
        q_list = [x for x in q_read]
    # pprint.pprint(q_list)
    # lq_list = [[re.sub(r'^.*(/.*/)', r'\1', x[5]), x[4], x[0], x[1]] for x in q_list]
    # pprint.pprint(lq_list)
    lq_dict = {}
    for q in q_list[1:]:
        # print(q)
        lq_str = re.sub(r'^.*(/.*/)', r'\1', q[5])
        if int(q[0]) > 0 or int(q[1]) > 50:
            if lq_str not in lq_dict:
                lq_dict[lq_str] = [[q[4], int(q[0]), int(q[1])]]
            else:
                lq_dict[lq_str].append([q[4], int(q[0]), int(q[1])])

    # pprint.pprint(lq_dict)
    # return

    for o_p in o_page_list:
        for t_p in c_list:
            if (o_p[0] == t_p[0] and (len(t_p[2]) > 30 or len(t_p[2]) < 28) and o_p[2] >= 5) or\
                    (o_p[0] == t_p[0] and o_p[0] in irregular_img and o_p[2] >= 5):
                # if o_p[0][1:3].isdecimal():
                #     dir_str = 'area-bbs'
                # else:
                #     dir_str = 'friend-with-benefits'
                scrape_data = sd_check_mod_date.read_sd_page(t_p[3], log_flag=True)
                if not scrape_data['img_pos']:
                    edit_s = 'https://www.sefure-do.com/wp-admin/post.php?post={}&action=edit'.format(t_p[1])
                    print('{} {} : {} - {}'.format(edit_s, t_p[2], o_p[2], len(t_p[2])))
                    if o_p[0] in lq_dict:
                        pprint.pprint(sorted(lq_dict[o_p[0]], key=lambda x: x[2], reverse=True))
                    # print(o_p)
                    # print(t_p)
                    # print('-------------')
                else:
                    scr_dict[t_p[3]]['img_pos'] = True
                break
    with open('sfd/pickle_pot/scrape_data.pkl', 'wb') as r:
        pickle.dump(scr_dict, r)


def make_image_pos_list(url_list, change_flag, first_flag):
    ignore_url = ['https://www.sefure-do.com/sitemap/', 'https://www.sefure-do.com/contact-form/']
    with open('sfd/pickle_pot/scrape_data.pkl', 'rb') as p:
        load_data = pickle.load(p)
    if first_flag:
        url_list = [x[2] for x in url_list if ('img_pos' not in load_data[x[2]] or not load_data[x[2]]['img_pos']) and
                    x[2] not in ignore_url]
        if url_list:
            if change_flag:
                mod_dict = {x: sd_check_mod_date.read_sd_page(x, log_flag=False) for x in url_list}
                with open('sfd/pickle_pot/scrape_data.pkl', 'wb') as q:
                    pickle.dump(mod_dict, q)
            else:
                mod_dict = load_data
            irregular_img = [x for x in mod_dict if not mod_dict[x]['img_pos']]
        else:
            irregular_img = []
    else:
        irregular_img = [x for x in load_data if not load_data[x]['img_pos'] and x not in ignore_url]
    return irregular_img


if __name__ == '__main__':
    pick_up_all_article()
