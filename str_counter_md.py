import re
import csv


def title_counter(md_path, kw_list):
    print(md_path)
    with open(md_path, 'r', encoding='utf-8') as f:
        long_str = f.read()
        title_l = re.findall(r'(t::.+?)\n', long_str)
        if title_l:
            title = title_l[0]
            title_len = len(title.replace('t::', ''))
            print('title : ' + str(title_len))
        des_l = re.findall(r'(d::.+?)\n', long_str)
        if des_l:
            des = des_l[0]
            des_len = len(des.replace('d::', ''))
            print('description : ' + str(des_len))
        main_l = re.findall(r'\n(# [\s\S]*)$', long_str)
        if main_l:
            main = main_l[0]
            main = re.sub(r'\n#* ', '\n', main)
            main = re.sub(r'^# ', '', main)
            main = re.sub(r']\(.+?\)', ']', main)
            main = re.sub(r'%.+?%', '', main)
            main = re.sub(r'!\[.+?]', '', main)
            main = re.sub(r'\[(.+?)]', r'\1', main)
            main = re.sub(r'<.+?>', '', main)
            main = re.sub(r'\n- ', r'\n', main)
            main = re.sub(r'\*', r'', main)
            main_len = len(main)
            print('main : ' + str(main_len))
            print('main(改行なし) : ' + str(len(main.replace('\n', ''))))
            print('\n')
            keyword_counter(kw_list, main)
            print('\n')
            sc_keyword_counter(main, md_path)


def keyword_counter(kw_list, long_str):
    for word in kw_list:
        if word:
            print(word + ' : ' + str(long_str.count(word)))


def sc_keyword_counter(long_str, md_path):
    with open('/Users/nakataketetsuhiko/Downloads/https___www-2/ページ.csv') as g:
        reader_p = csv.reader(g)
        csv_list_p = [row_p for row_p in reader_p]
    if md_path.replace('md_files/pc/', '').replace('.md', '.html').replace('index.html', '') in csv_list_p[1][0]:
        with open('/Users/nakataketetsuhiko/Downloads/https___www-2/クエリ.csv') as f:
            reader = csv.reader(f)
            csv_list = [row for row in reader]
        c_list = [y[0] for y in csv_list[1:] if int(y[2]) > check_number_of_days_q()]
        words = []
        for x in c_list:
            row_words = x.split(' ')
            for z in row_words:
                if z not in words and len(z) < 11:
                    words.append(z)
                    print(z + ' : ' + str(long_str.count(z)))


def check_number_of_days_q():
    with open('/Users/nakataketetsuhiko/Downloads/https___www-2/日付.csv') as f:
        reader = csv.reader(f)
        csv_list = [row for row in reader]
    result = len(csv_list) - 1
    return result


if __name__ == '__main__':
    key_list = ['出会い系', '掲示板', '書き方', 'PCMAX', 'テンプレ', '例文', '書き込み', '最初']
    title_counter('md_files/pc/majime/kakikata_t.md', key_list)
