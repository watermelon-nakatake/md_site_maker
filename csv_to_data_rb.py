# -*- coding: utf-8 -*-
import csv
import os
import re
import io
import urllib.request
import requests
import pickle
from selenium import webdriver
from googletrans import Translator
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# import sys
from html.parser import HTMLParser
# from word_list_rb_sf import main_list
from word_list_rb_sf import keyword_dec_list
from word_list_rb_sf import word_list
from word_list_rb_sf import word_list_fix
from word_list_rb_sf import conjunction_list

# from word_list_rb_sf import illegal_para

str_a = ""
sub_str = ""

remove_list_t = ["出会い", "出会い系", "サイト", "][", "障害", "規定", "支援", "指定", "事業", "福祉", "相談", "当該", "法律", "労働", "厚生", "給付",
                 "支給", "施行", "施設", "省令", "市町村", "介護", "自立", "決定", "改正", '医療', '附則', '特定', '計画', '基準', '生活']


# 記事のスプレッドシートのcsvを読み取って、文字列→リスト変換


def main(file_name):
    big_list = change_csv(file_name)
    print(big_list)
    big_list = change_org_tag(big_list)
    print(big_list)
    return big_list


def change_csv(input_file):
    csv_file = open(input_file, 'r', encoding="utf-8", errors="", newline="")
    f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"',
                   skipinitialspace=True)
    big_list = []
    for row in f:
        while '' in row:
            row.remove('')
        big_list.append(row)
    return big_list


def change_org_tag(str_c):
    str_c = str_c.replace("<p>", "")
    str_c = str_c.replace("</p>", "")
    str_c = str_c.replace("['sc']", "['sc'")
    str_c = str_c.replace(", ['/sc']", "]")
    str_c = str_c.replace("['st']", "['st'")
    str_c = str_c.replace(", ['/st']", "]")
    str_c = str_c.replace("['sh']", "['sh'")
    str_c = str_c.replace(", ['/sh']", "]")
    str_c = str_c.replace("['ch']", "['ch'")
    str_c = str_c.replace(", ['/ch']", "]")
    str_c = str_c.replace("['ps']", "['ps'")
    str_c = str_c.replace("['ps-p']", "['ps-p'")
    str_c = str_c.replace(", ['/ps-p']", "]")
    str_c = str_c.replace("['ps-s']", "['ps-s'")
    str_c = str_c.replace(", ['/ps-s']", "]")
    str_c = str_c.replace("['age-o']", "['age-o'")
    str_c = str_c.replace(", ['/age-o']", "]")
    str_c = str_c.replace("['look']", "['look'")
    str_c = str_c.replace(", ['/look']", "]")
    str_c = str_c.replace("['p']", "'<p>'")
    str_c = str_c.replace("['/p']", "'</p>'")
    str_c = str_c.replace("['co']", "'<comment>'")
    str_c = str_c.replace("['/co']", "'</comment>'")
    # str_c = str_c.replace("['nodata']", "''")
    return str_c


def key_dec_maker(csv_path):
    csv_file = open(csv_path, 'r', encoding="utf-8", errors="", newline="")
    f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"',
                   skipinitialspace=True)
    big_list = []
    for row in f:
        while '' in row:
            row.remove('')
        dec = {'keyword': row[0], 'adj': row[1], 'noun': row[2], 'reason': row[3], 'jaf': row[4], 'ps': row[5],
               'age': row[6], 'look': row[7], 'eng': row[8], 'id': row[9], 'pro': row[10], 'particle': row[11]}
        big_list.append(dec)
    return big_list


def make_list(directory_str, dec_path):
    dec_list = key_dec_maker(dec_path)
    data_list = file_pick_up(directory_str)
    data_list = list_remover(data_list, remove_list_t)
    result = search_and_replace(dec_list, data_list)
    return result


def make_list_k(directory_str, dec_list):
    dec_list = keyword_replace(dec_list, 'セフレ', 'セックス')
    for x in dec_list:
        x['kyoki'] = []
    data_list = file_pick_up(directory_str)
    data_list = list_remover(data_list, remove_list_t)
    result = search_and_replace(dec_list, data_list)
    for y in result:
        if y['kyoki'] is []:
            print(str(y['password']) + ': エラー')
    return result


def keyword_replace(key_list_s, main_key, new_key):
    for x in key_list_s:
        x['pro'] = x['pro'].replace(main_key, new_key)
    return key_list_s


# キーワードリストの作成
def file_pick_up(directory_str):
    directory = os.listdir(directory_str)
    result = []
    directory.remove('.DS_Store')
    for file in directory:
        file_path = directory_str + "/" + file
        csv_file = open(file_path, 'r', encoding="shift_jis", errors="", newline="")
        f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"',
                       skipinitialspace=True)
        print(file)
        f_name = re.findall(r'cooccur_(.*?)_', file)
        if f_name[0]:
            key_name = f_name[0]
        else:
            key_name = 'no_name'
        k_list = []
        try:
            for row in f:
                while '' in row:
                    row.remove('')
                # print(row)
                k_list.append(row[0])
            k_list.pop(0)
            dec = {'key': key_name, 'kyoki': k_list}
            result.append(dec)
        except LookupError:
            print("エラー" + f_name[0])
            file_path = directory_str + "/" + file
            csv_file = open(file_path, 'r', encoding="utf-8", errors="", newline="")
            f_e = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"',
                             skipinitialspace=True)
            for row in f_e:
                while '' in row:
                    row.remove('')
                # print(row)
                k_list.append(row[0])
            k_list.pop(0)
            dec = {'key': key_name, 'kyoki': k_list}
            result.append(dec)
    seen = []
    result = [x for x in result if x not in seen and not seen.append(x)]
    return result


def search_and_replace(base_list, insert_list):
    result = []
    for dec in base_list:
        for dec_p in insert_list:
            if dec['pro'] == dec_p['key']:
                dec['kyoki'] = dec_p['kyoki']
                result.append(dec)
    return result


def list_remover(base_list, remove_list):
    for dec in base_list:
        for x in remove_list:
            if x in dec['kyoki']:
                dec['kyoki'].remove(x)
        del dec['kyoki'][30:]
    return base_list


def csv_list_maker(dec_list):
    with open('key_dec2.csv', 'w', newline='') as f:
        w = csv.writer(f, delimiter=",")
        for x in dec_list:
            x["kyoki"].insert(0, x['keyword'])
            # print(x["kyoki"])
            w.writerow(x["kyoki"])


def total_counter(directory_str):
    directory = os.listdir(directory_str)
    counter = {}
    for file in directory:
        file_path = directory_str + "/" + file
        csv_file = open(file_path, 'r', encoding="shift_jis", errors="", newline="")
        f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"',
                       skipinitialspace=True)
        mini_list = []
        for row in f:
            while '' in row:
                row.remove('')
            mini_list.append(row)
            # print(mini_list)
        for y in mini_list[1:]:
            if y[0] in counter:
                counter[y[0]] += int(y[1])
                # print(y)
            else:
                counter[y[0]] = int(y[1])
    result = sorted(counter.items(), key=lambda x: -x[1])
    return result


def name_pick_up(name_list):
    print(len(name_list))
    for x in range(0, len(name_list) - 2):
        for y in range(x, len(name_list) - 1):
            print(str(x) + " " + str(y))
            if name_list[x] == name_list[y]:
                name_list.remove(name_list[y])
    return name_list


def wp_data_pickup(file_path):
    result = []
    with open(file_path, 'r', encoding='utf-8') as f:
        file_str = f.read()
    art_str_list = re.findall(r'<item>(.*?)</item>', file_str)
    for art_str in art_str_list:
        title = re.findall(r'<title>(.*?)</title>', art_str)
        main_str = re.findall(r'<content:encoded><!\[CDATA\[(.*?)\]\]></content:encoded>', art_str)
        link = re.findall(r'<link>https://www.sefure-do.com/friend-with-benefits/(.*?)/</link>', art_str)
        dec = {'title': title[0], 'link': link[0], 'main': main_str[0]}
        result.append(dec)
    return result


def html_pickup(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        file_str = f.read()
    title = re.findall(r'<title>(.*?)</title>', file_str)
    main_str = re.findall(r'<main>(.*?)</main>', file_str)
    dec = {'title': title[0], 'main': main_str[0]}
    return dec


def str_checker(str_x, str_y):
    dec = {}
    if str_x['title'] is not str_y['title']:
        dec['title'] = str_x['title']
    if str_x['main'] is not str_y['main']:
        dec['main'] = str_x['main']
    if dec is {}:
        result = 'none'
    else:
        result = dec
    return result


def circle_slicer(str_checked):
    """
    「。」で文字列をスライスして文字列のリストを返す
    :param str_checked: 大きな文字列
    :return: スライスされてキーワードを取り除いたリスト
    """
    list_r = []
    while '。' in str_checked:
        index = str_checked.find('。') + 1
        str_sliced = str_checked[0:index]
        list_r.append(str_sliced)
        str_checked = str_checked[index:]
    return list_r


class MyHtmlStripper(HTMLParser):
    def error(self, message):
        pass

    def __init__(self, s):
        super().__init__()
        self.sio = io.StringIO()
        self.feed(s)

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        self.sio.write(data)

    @property
    def value(self):
        return self.sio.getvalue()


def directory_to_list(path):
    directory = os.listdir(path)
    result = []
    for file in directory:
        file_path = path + "/" + file
        result.append(file_path)
    return result


def update_checker(directory_path, file_path):
    wp_list = wp_data_pickup(file_path)
    directory = os.listdir(directory_path)
    result = []
    for file in directory:
        dec = {}
        if '.html' in file:
            html_path = directory_path + "/" + file
            html_dec = html_pickup(html_path)
            file_name = file.replace('.html', '')
            for y in wp_list:
                # print(str(y['link']) + ':vs:' + str(file_name))
                if file_name == y['link']:
                    # print('スタート' + str(y['link']) + ':vs:' + str(file_name))
                    # dec['match'] = []
                    # print(html_dec['main'])
                    # main_str_list = circle_slicer(MyHtmlStripper(html_dec['main']).value)
                    # y_str = MyHtmlStripper(y['main']).value
                    if html_dec['title'] != y['title']:
                        dec['title'] = y['title']
                    if '<img' in y['main']:
                        image = re.findall(r'<img.*?/>', y['main'])
                        if image:
                            dec['image'] = image[0]
                    # for x in main_str_list:
                    #     if x not in y_str:
                    #         dec['match'].append(x)
                    if 'image' in dec:
                        dec['link'] = file_name
                    if 'title' in dec:
                        dec['link'] = file_name
                    # else:
                    #     del dec['match']
        if dec is not {}:
            result.append(dec)
    while {} in result:
        result.remove({})
    return result


def code_insert(list_str_c):
    line_num = 544  # 現時点でのコードの最大値
    result = sentence_code_insert(list_str_c, 'ch', line_num)
    result = sentence_code_insert(result[0], 'h2', result[1])
    result = sentence_code_insert(result[0], 'h3', result[1])
    result = sentence_code_insert(result[0], 'ja', result[1])
    result = sentence_code_insert(result[0], 'ps', result[1])
    print(result[1])
    return result[0]


def sentence_code_insert(list_str_s, char, line_num):
    match_list = re.findall(r"\['" + char + r"', '.*?\]", list_str_s)
    for match in match_list:
        # print('start')
        # print(match)
        if "['ch', '<!--insert-para-->']" not in match:
            line_num += 1
            str_num = 0
            # print("分解")
            inner_str_list = re.findall(r"'.*?'", match)
            for inner_str in inner_str_list:
                if "'" + char + "'" not in inner_str and "nodata" not in inner_str and "<!--insert" not in inner_str:
                    str_num += 1
                    # print(inner_str)
                    list_str_s = list_str_s.replace(inner_str,
                                                    inner_str + "<!--|" + str(line_num) + "-" + str(str_num) + "|-->'",
                                                    1)
                    list_str_s = list_str_s.replace("'<!--|", "<!--|")

    return list_str_s, line_num


def long_str_search(long_str):
    match_list = re.findall(r'-->[亜-熙ぁ-んァ-ヶ。、]*?<!--', long_str)
    result = [""]
    for match in match_list:
        if len(match) > 20:
            print(match)
            result.append(match)
    match_list_a = re.findall(r"'[亜-熙ぁ-んァ-ヶ。、]*?<!-", long_str)
    for match_a in match_list_a:
        if len(match_a) > 20:
            print(match_a)
            result.append(match_a)
    match_list_b = re.findall(r"-->[亜-熙ぁ-んァ-ヶ。、]*?'", long_str)
    for match_b in match_list_b:
        if len(match_b) > 20:
            print(match_b)
            result.append(match_b)
    match_list_c = re.findall(r"'[亜-熙ぁ-んァ-ヶ。、]*?'", long_str)
    for match_c in match_list_c:
        if len(match_c) > 20:
            print(match_c)
            result.append(match_c)

    match_list_d = re.findall(r"-->[^<]*?<!-", long_str)
    for match_d in match_list_d:
        if len(match_d) > 20:
            print(match_d)
            result.append(match_d)
    result.sort()
    return result


def file_download(path_list):
    user = 'kirishima3260@yahoo.co.jp'
    password = 'snhrtv3ef04dl8'

    session = requests.session()

    login_info = {
        "mail": user,
        "pw": password,
        "btnSubmit": ""
    }

    url_login = 'https://user.sakurasaku-labo.jp/users/login/'
    res = session.post(url_login, data=login_info)
    res.raise_for_status()

    print(res.text)

    res = session.get('https://user.sakurasaku-labo.jp/tools/cooccur')
    res.raise_for_status()

    print(res.text)
    for path in path_list:
        file_name = re.findall(r'/([^/]*?)$', path)[0]
        urllib.request.urlretrieve(path, "download.csv")
        print(file_name)
    return res.text


def selenium_ctr():
    driver = webdriver.Safari()
    driver.get('https://user.sakurasaku-labo.jp/users/login')

    driver.find_element_by_id('mail').send_keys('kirishima3260@yahoo.co.jp')
    driver.find_element_by_id('pw').send_keys('snhrtv3ef04dl8')
    element = driver.find_element_by_partial_link_text('ログイン')
    driver.execute_script("arguments[0].click();", element)

    print(driver.find_elements_by_css_selector('body').text)

    driver.find_elements_by_link_text('共起語を探す')

    print(driver.find_elements_by_css_selector('body').text)

    text = driver.find_element_by_id('datatable').text
    print(text)


def kyoki_list(num):
    for x in keyword_dec_list[num:]:
        print(str(x['keyword'] + ': ' + str(x['kyoki'])))
    return


def keyword_duplicate_check(c_list):
    pickup_list = []
    eng_list = []
    for key in c_list:
        keyword = key['keyword']
        for key_l in pickup_list:
            if keyword in key_l:
                print('重複しています : ' + str(keyword) + '-' + str(key['id']))
        pickup_list.append(keyword)
        eng = key['eng']
        if eng in eng_list:
            print('engが重複 : ' + str(eng))
        eng_list.append(eng)


def word_translation(k_list):
    translator = Translator()
    for key in k_list:
        keyword_j = key['keyword']
        keyword_e = translator.translate(keyword_j)
        keyword_e = keyword_e.text
        keyword_e = keyword_e.lower()
        eng_text = keyword_e.replace(' ', '-')
        print(str(keyword_j) + ': ' + str(eng_text))


def word_list_duplicate_checker(w_list):
    result = []
    for x in range(len(w_list) - 1):
        for y in range(x + 1, len(w_list)):
            for x_str in w_list[x]['after']:
                for y_str in w_list[y]['after']:
                    if x_str in y_str:
                        asw = {w_list[x]['before']: x_str, w_list[y]['before']: y_str}
                        result.append(asw)
                        print(asw)
    return result


def sentence_list_maker(list_str):
    w_list = word_list_fix + word_list + conjunction_list
    for f_word in w_list:
        if f_word['after'][0] in list_str:
            list_str = list_str.replace(f_word['after'][0], f_word['before'])
    for words in w_list:
        for c_word in words['after']:
            if c_word in list_str:
                list_str = list_str.replace(c_word, words['before'])
    print(list_str)
    for r_word in w_list:
        if r_word['before'] in list_str:
            list_str = list_str.replace(r_word['before'], '<' + str(r_word['after'][0]) + '>')
    print('*******************************')
    print(list_str)
    list_str = list_str.replace("','", "', '")
    result = code_insert(list_str)
    print('*******************************')
    print(result)


def url_and_title_list_maker(path, pkl_name):
    file_list = os.listdir(path)
    title_list = {}
    for file in file_list:
        if '.html' in file:
            print(file)
            with open(path + '/' + file, "r", encoding='utf-8') as f:
                str_x = f.read()
                title = re.findall(r'<h1 .*?>(.*?)</h1>', str_x)
                if '<!--data#key#' in str_x:
                    l_key = re.findall(r'<!--data#key#(.*?)#.*?#-->', str_x)[0]
                    id_n = int(re.findall(r'<!--data#key#.*?#(.*?)#-->', str_x)[0])
                    dec = {'title': title[0], 'url': file, 'key': l_key}
                    title_list[id_n] = dec
    print(title_list)
    with open('pickle_data/' + pkl_name + '.pkl', 'wb') as p:
        pickle.dump(title_list, p)


def make_str_to_list(name_str):
    actor_list = []
    actors = re.findall(r'\d+位：(.+?)\n', name_str)
    for x in actors:
        actor_list.append(x)
    print(actor_list)


def random_adj_list_maker(csv_path, key_list):
    # 13 - 24
    csv_list = change_csv(csv_path)
    for x in range(0, len(csv_list)):
        adj_list = []
        for y in range(12, 37):
            if csv_list[x][y] == '0':
                adj_list.append(y - 12)
                print(adj_list)
        key_list[x]['rdm_adj'] = adj_list
    print(key_list)


if __name__ == '__main__':
    # ランダム形容詞の除外リスト作成
    random_adj_list_maker('list_csv.csv', keyword_dec_list)

    # ①csvファイルをリストに置換
    # print(change_csv('illegal.csv'))

    # ②出力されたリストを文字列として記入
    # list_str_m = "[['st', '<p>', ['ch', 'そんな気持ちで<!--google--><!--search-->をして<!--there-->にたどり着いた<!--reader-->も<!--exist-->ことでしょう。', 'そんな感じで、世の中には<!--hな--><!--keyword-h-->との<!--sex-->を希望して<!--exist--><!--reader-->も多い<!--think-->。', 'そういう<!--ya#2#疑問#願望#ya-->を持って<!--exist--><!--reader-->も<!--exist--><!--think-->。'], '</p>', '<p>',['ch', '<!--c-逆接-->、残念ながら<!--japan-->では<!--keyword-il--><!--like--><!--R18--><!--woman-y-->と<!--making-love-->などをするのは<!--illegal-->です。', '<!--c-逆接-->、<!--japan-->の法律では<!--keyword-il--><!--like--><!--R18--><!--woman-y-->と淫らな行為をすることは禁じられています。', '<!--c-逆接-->、<!--japan-->の法律では<!--keyword-il-->を含む<!--R18--><!--woman-y-->（児童）と<!--sex-->など淫らな行為（淫行）をするのは<!--illegal-->で許されません。'],['ch', '<!--absolutely-->やってはいけません。', 'もしやってしまうと、<!--ya#2#児童ポルノ法#淫行条例違反#ya-->で逮捕されることになります。', 'もし気の迷いで<!--ya#2#JK#JC#ya--><!--like--><!--R18--><!--woman-y-->と<!--sex-->したりすると、警察に逮捕されます。'],['ch', '<!--c-並列-->、<!--real2--><!--keyword-il-->を装った美人局の場合もあるので<!--well-->危険です。', 'nodata'], ['ch', '<!--c-順接-->、もしも<!--deaikei2--><!--site-->で監視の目をくぐり抜けて利用している<!--keyword-il-->を<!--find2-->も、<!--absolutely--><!--mail-->を送ったりしてはいけません。', '<!--c-順接-->、万が一不正をして<!--deaikei2--><!--site-->を使っている<!--keyword-il-->を<!--find2-->も、<!--mail-->したりしないで<!--c-対比-->通報してください。', '<!--c-順接-->、<!--deaikei2--><!--site-->を利用していて、年齢を偽って<!--entry-->している<!--keyword-il-->を見つけたら、<!--mail-->しないで<!--whore-->に通報しましょう。'],['ch', '<!--absolutely-->会って<!--sex-->しようとしてはいけません。', '<!--sex-->しようなんて考えないでください。', 'nodata'],'</p>', '<p>', ['ch', '<!--c-逆接-前提-->、<!--deaikei2--><!--site-->を使えば「<!--keyword-h-->」<!--woman-y-->となら出会うことが<!--s-can-->。', '<!--c-逆接-前提-->、<!--real2--><!--keyword-il-->ではなくて、合法な「<!--keyword-h--><!--woman-y-->」であれば、<!--deaikei2--><!--site-->で出会って<!--sex-->することが<!--s-can-->。', 'どうしても<!--keyword-il-->と<!--sex-->したい<!--reader-->は、<!--real2--><!--keyword-il-->ではなく18歳以上の「<!--keyword-h--><!--woman-y-->」と<!--deaikei2-->で出会って制服<!--sex-->しましょう。'],['ch', '高校を卒業した18歳以上の<!--woman-y-->であれば、出会おうが<!--sex-->しようが自由です。', 'nodata'], ['ch', '<!--deaikei2-->には<!--various-->タイプの<!--woman-y-->がいるので、その中には高校を卒業したばかりの若い未成年の<!--woman-y-->もいます。', '特に大手の<!--deaikei2--><!--site-->は<!--woman-->利用者が多いので、高校を卒業したばかりの若い<!--woman-y-->から熟女まで、<!--various--><!--woman-->が<!--entry-->しています。', '大手の、ファッション誌などに広告を出している<!--deaikei2--><!--site-->には18歳から20歳までの若い<!--woman-y-->が多いです。'],['ch', '<!--c-当然-->、<!--ya#2#中学#高校#ya-->の制服を持っている<!--keyword-h-->もいる<!--think2-->。', '<!--deaikei2--><!--site-->の<!--b-bbs-->や<!--profile-->の<!--photo-->を見ると、<!--keyword-h-->若い<!--look-->の<!--woman-y-->も<!--many-->見つかります。', 'その中には、一見<!--keyword-il-->にしか見えない<!--woman-y-->もいます。'],['ch', 'そういう<!--keyword-h-->合法の<!--woman-y-->であれば、問題なく出会って<!--sex-->することが<!--s-can-->。', 'その中から、<!--me-->が求める<!--keyword-h--><!--look-->の<!--woman-y-->を<!--find2-->、出会えばいいんです。', 'そういう<!--keyword-h--><!--look-->の<!--woman-y-->を狙って出会って、<!--sex-->すれば<!--good-->んです。'], ['ch', '若くて<!--keyword-h--><!--look-->の<!--woman-y-->と制服<!--sex-->すれば、<!--keyword-il-->と<!--sex-->する気分は十分味わえます。', 'nodata', '<!--R18--><!--real2--><!--keyword-il-->も、18歳の<!--keyword-h-->かわいい<!--woman-y-->も、<!--sex-->の気持ち良さは変わりません。'],'</p>', '<p>', ['ch', '<!--c-解説-->、<!--there-->では<!--keyword-h--><!--woman-y-->と<!--deaikei2--><!--site-->で出会って<!--how-to-sex-->について<!--description-->していきます。', '<!--c-解説-->、<!--there-->では<!--keyword-il-->と出会って<!--how-to-sex-->ではなく、<!--keyword-h--><!--woman-y-->と出会って<!--how-to-sex-->を<!--description-->します。', '以下では、<!--real2--><!--keyword-il-->ではなく、合法な<!--keyword-h--><!--woman-y-->と<!--surely-->出会える<!--way-->を<!--description-->します。'],'</p>'], ['st', '<p>', ['ch', '<!--crucial-->なことなので、最後にもう一回<!--ya#1#釘を刺して#念を押して#注意して#ya-->おきます。', '<!--at-first-->の<!--reader-->で書きましたが、念のためもう一度<!--ya#1#釘を刺して#念を押して#注意して#ya-->おきます。', '最後にもう一度<!--ya#1#釘を刺して#念を押して#注意して#ya-->おきます。'], ['ch', '<!--keyword-il-->と出会いたい<!--reader-->も<!--exist-->かもしれませんが、<!--R18-->児童と<!--h-2-->なことをするのは<!--illegal-->です。', '<!--keyword-il-->と出会いたくてこの<!--page-->にたどり着いた<!--man-->も多い<!--think-->が、<!--keyword-il-->と<!--sex-->すると警察に逮捕されます。', '「<!--keyword-il--> <!--sex-->」などでgoogle<!--search-->して<!--there-->を読んでいる<!--reader-->も<!--exist--><!--think-->が、<!--real2--><!--keyword-il-->と<!--sex-->するのは<!--illegal-->です。'],['ch', '<!--absolutely--><!--keyword-il-->とは<!--sex-->しないようにしてください。', '<!--c-順接-->、決して<!--real2--><!--keyword-il-->を<!--find2-->も手を出してはいけません。'],['ch', 'これは<!--certainly-->厳守してください。', 'nodata'], ['ch', 'その代わり、18歳以上の<!--keyword-h-->合法の<!--woman-y-->と<!--deaikei2-->で出会って、<!--sex-->を楽しんでください。', '本物ではなく18歳以上の<!--keyword-h-->若い<!--woman-y-->と出会って<!--sex-->して、安全に<!--sex-->を楽しんでください。', 'それよりも、<!--keyword-h-->18歳以上の<!--woman-y-->と出会って、安心して<!--sex-->を楽しみましょう。'],'</p>']]"

    # ③文字列中の特定ワードを置換用タグに置き換え
    # ④出力された文字列を文字列として保存
    # ⑤文字列のタグ等を置換、階層構造のリスト風文字列にする
    # ⑥sentence codeの挿入
    # sentence_list_maker(change_org_tag(list_str))
    # ⑦完成した文字列をリストとしてword_list_rbファイルに記入、保存

    # キーワードの英訳
    # word_translation(keyword_dec_list)

    # 新規キーワードのキーワードリスト作成
    # print(make_list("/Users/nakataketetsuhiko/PycharmProjects/reibun_sf/cvs_d",
    #                "/Users/nakataketetsuhiko/PycharmProjects/reibun_sf/csv20190518.csv"))

    # キーワードの共起語を表示
    # kyoki_list(193)

    # keyword_dec_listのキーワード重複チェック
    # keyword_duplicate_check(keyword_dec_list)

    # print(len(keyword_dec_list))

    # 関連記事用のリスト作成 ピックル保存
    # url_and_title_list_maker('files_sf', 'sex_m')

    # 文章から名前などを抽出
    # sample_str = ''
    # make_str_to_list(sample_str)
