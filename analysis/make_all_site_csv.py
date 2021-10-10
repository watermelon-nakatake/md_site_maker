import datetime
import csv
import query_check_and_make_html
import search_console_data


def make_all_site_gsc_csv(start_date):
    result = []
    u_list = []
    head = ['date']
    pj_dict = query_check_and_make_html.project_info
    today = datetime.date.today()
    now = datetime.datetime.now()
    if now.hour > 9:
        day_d = 3
    else:
        day_d = 2
    end_date = str(today - datetime.timedelta(days=day_d))
    print(end_date)
    with open('gsc_data/all_site_data/reibun.csv') as h:
        reader_r = csv.reader(h)
        r_csv = [row for row in reader_r]
        if r_csv[-1][-1] == end_date:
            get_flag = True
        else:
            get_flag = False
    for pj_id in pj_dict:
        if not get_flag:
            search_console_data.make_csv_from_gsc(pj_dict[pj_id]['pj_domain'], start_date, end_date, 'all_site_data',
                                                  pj_id, ['date'])
        with open('gsc_data/all_site_data/' + pj_id + '.csv') as f:
            reader = csv.reader(f)
            csv_list = [row for row in reader]
            r_list = csv_list[1:]
            r_list.reverse()
            # print(r_list)
            u_list.append(r_list)
        head.append(pj_id)
    head.append('sum')
    for i in range(len(u_list[0])):
        j_sum = 0
        a_list = [u_list[0][i][4]]
        for j in u_list:
            # print(j)
            # print(len(j))
            if len(j) > i:
                # print(j[i])
                # print(j[i][0])
                j_sum = j_sum + int(j[i][0])
                # j_sum += int(j[i][0])
                a_list.append(j[i][0])
            else:
                a_list.append(0)
        a_list.append(j_sum)
        # print(a_list)
        # print('sum')
        # print(j_sum)
        # result.append([u_list[0][i][4], j_sum])
        result.append(a_list)
    result.append(head)
    result.reverse()
    print(result)
    with open('gsc_data/all_site_data/sum.csv', 'w', encoding='utf-8') as s:
        writer = csv.writer(s)
        writer.writerows(result)


if __name__ == '__main__':
    start_date_t = '2020-05-01'
    make_all_site_gsc_csv(start_date_t)
