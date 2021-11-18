import re
import csv
import make_article_list
import reibun.main_info


def title_counter(md_path, kw_list, site_shift, pd):
    print(md_path)
    with open(md_path, 'r', encoding='utf-8') as f:
        long_str = f.read()
        title_l = re.findall(r'(t::.+?)\n', long_str)
        if title_l:
            title = title_l[0]
            title = re.sub(r'<!--.*?-->', '', title)
            title_len = len(title.replace('t::', ''))
            print('title : ' + str(title_len))
        des_l = re.findall(r'(d::.+?)\n', long_str)
        if des_l:
            des = des_l[0]
            des = re.sub(r'<!--.*?-->', '', des)
            des_len = len(des.replace('d::', ''))
            print('description : ' + str(des_len))
        main_l = re.findall(r'\n(# [\s\S]*)$', long_str)
        if main_l:
            main = main_l[0]
            if '%ss' in main:
                ss_list = pd['site_shift_list']
                for ss_num in ss_list:
                    if main.count('%ss' + str(ss_num) + '%') != main.count('%ss' + str(ss_num) + '%'):
                        raise Exception('%ss の数が合っていません！！')
                main = re.sub(r'%ss' + str(site_shift) + r'%\n([\s\S]*?)%ss' + str(site_shift) + r'e%\n',
                              r'\1', main)
                ss_list.remove(site_shift)
                for s_num in ss_list:
                    main = re.sub(r'%ss' + str(s_num) + r'%\n([\s\S]*?)%ss' + str(s_num) + r'e%\n', '', main)

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
            print('main(改行なし) : ' + str(len(main.replace('\n', ''))) + '\n')
            keyword_counter(kw_list, main)
            # sc_keyword_counter(main, md_path)


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


def read_this_title_log(md_path, pd):
    target_html = md_path.replace(pd['project_dir'] + '/md_files/' + pd['main_dir'], '').replace('.md', '.html')
    pk = make_article_list.read_pickle_pot('title_log', pd)
    # print(pk)
    for data in pk[target_html]:
        print(data + ' : ' + pk[target_html][data][0])

# todo: ハッピーメール 出会えない セフレ の新記事
# todo: 新記事キーワード : フィーチャーフォン、PC ブラウザ、


if __name__ == '__main__':
    target_md = 'reibun/md_files/pc/majime/m0warikiri.md'
    # query_check_and_make_html.check_single_page_seo(28, target_md, False)
    # read_this_title_log(target_md, reibun.main_info.info_dict)
    key_list = ['長文', 'ハッピーメール']
    title_counter(target_md, key_list, 1, reibun.main_info.info_dict)
