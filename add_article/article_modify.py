import re
import os
import glob
import datetime
import shutil
import pickle
from upload import file_upload


# import make_article_list


def make_project_dir(project_name):
    if not os.path.exists(project_name):
        os.mkdir(project_name)
    make_dir = {'md': 'md_files', 'html': 'html_files', 'image_stock': 'image_stock', 'insert_image': 'insert_image',
                'pickle': 'pickle_pot'}
    for dir_name in make_dir:
        dir_path = project_name + '/' + make_dir[dir_name]
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)


def del_note_dir(dir_path):
    all_dir = glob.glob(dir_path + '/**/', recursive=True)
    print(all_dir)
    note_dir = [x for x in all_dir if '/_notes' in x]
    print(note_dir)
    for n_dir in note_dir:
        shutil.rmtree(n_dir)


def insert_canonical(dir_path):
    del_note_dir(dir_path)
    all_files = glob.glob(dir_path + '/**/**.html', recursive=True)
    for file_path in all_files:
        print(file_path)
        with open(file_path, 'r', encoding='Shift_JIS') as f:
            long_str = f.read()
            replace_str = file_upload.tab_and_line_feed_remove_from_str(long_str)
            if '<link rel="canonical"' not in replace_str:
                cn_path = file_path.replace('rei_site/rep_rs/sp/', 'http://www.reibunsite.com/pc/')
                replace_str = re.sub(r'</title>',
                                     r'</title><link rel="canonical" href="' + cn_path + '">',
                                     replace_str)
                replace_str = re.sub(r'<!--yhyo-->.*?<!--yhyo/e-->', '<!--yhyo-->2021<!--yhyo/e-->', replace_str)
                with open(file_path, 'w', encoding='Shift_JIS') as g:
                    g.write(replace_str)


def all_file_to_markdown(before_dir, after_dir, pd, path_remove, remove_list):
    pk_dic = {}
    today = datetime.date.today()
    dir_list = glob.glob(before_dir + '**/**/', recursive=True)
    print(dir_list)
    for n_dir in dir_list:
        n_dir = n_dir.replace(before_dir, after_dir)
        if not os.path.exists(n_dir):
            os.makedirs(n_dir)
    b_files = glob.glob(before_dir + '/**/**.html', recursive=True)
    b_files = [x for x in b_files if 'wp-' not in x and x.count('/') == 3]
    b_files = file_path_order(b_files)
    print(b_files)
    for h_file in b_files:
        print(h_file)
        p_num = len(pk_dic)
        pk_data = file_to_markdown(h_file, before_dir, after_dir, today, path_remove, remove_list, p_num, pd)
        pk_dic[p_num] = pk_data
    print(pk_dic)
    with open('online_marriage/pickle_pot/main_data.pkl', 'wb') as k:
        pickle.dump(pk_dic, k)


def file_path_order(b_files):
    index_files = []
    for h_path in b_files:
        if '/index.html' in h_path:
            index_files.append(h_path)
            b_files.remove(h_path)
    index_files.sort()
    # print(index_files)
    b_files.sort()
    return index_files + b_files


def file_to_markdown(file_path, before_dir, after_dir, today, path_remove, remove_list, p_num, pd):
    new_path = file_path.replace(before_dir + '/', '').replace(path_remove, '').replace('.html', '.md')
    md_path = file_path.replace(before_dir, after_dir).replace('.html', '.md')
    # md_path = file_path.replace(before_dir, after_dir + '/experiences').replace('/index.html', '.md')
    category = file_path.split('/')[-1]
    with open(file_path, 'r', encoding='utf-8') as f:
        long_str = f.read()
    long_str = file_upload.tab_and_line_feed_remove_from_str(long_str)
    title_l = re.findall(r'<title>(.+?)</title>', long_str)
    if title_l:
        if '|' not in title_l[0]:
            title = title_l[0]
        else:
            title = re.sub(r'\|.*$', '', title_l[0])
    else:
        title = 'no_title'
        print('no title !')
    key_word_l = re.findall(r'<meta name="Keywords" content="(.+?)"', long_str)
    if key_word_l:
        key_word = key_word_l[0].split(',')
    else:
        print('no key_word !')
        key_word = 'n_a'
    description_l = re.findall(r'<meta name="description" content="(.*?)"', long_str)
    if description_l:
        description = description_l[0]
    else:
        print('no key_word !')
        description = 'n_a'
    h1_l = re.findall(r'<h1.*?>(.+?)</h1>', long_str)
    if h1_l:
        h1 = h1_l[0]
    else:
        print('no h1 !')
        h1 = 'n_a'
    # メインコンテンツ抽出
    # main_start = '<div class="entry-content">'
    # main_end = '</div><!-- コピー禁止エリアここまで -->'
    main_start = '<div class="contents">'
    main_end = '<div class="postdate">'
    remove_str = []
    main_srt_l = re.findall(main_start + r'(.*?)' + main_end, long_str)
    if main_srt_l:
        main_str = main_srt_l[0]
    else:
        print('no contents !')
        main_str = ''
    for r_str in remove_str:
        if r_str in main_str:
            main_str.replace(r_str, '')
    if '<h4>関連記事' in main_str:
        main_str = re.sub(r'<h4>関連記事.*$', '', main_str)
    if '/wp-content/uploads/' in main_str:
        img_l = re.findall(r'<img .+?>', main_str)
        for i, img_str in enumerate(img_l):
            # print(img_str)
            f_img_l = re.findall(r'alt="(.*?)".+?static/wp-content/uploads/(.+?\.jpg)', img_str)
            print(f_img_l)
            if f_img_l:
                old_img = 'htaiken/old_files/wp-content/uploads/' + f_img_l[0][1]
                new_img = file_path.replace('/old_files/', '/md_files/images/art_images/') \
                    .replace('/index.html', '_{}.jpg'.format(str(i + 1)))
                shutil.copy(old_img, new_img)
                # print(new_img)
                insert_str = '<img src="{}" alt="{}">'.format(new_img.replace('htaiken/md_files', '..'),
                                                              f_img_l[0][0])
                main_str = main_str.replace(img_str, insert_str)
            else:
                print('image_error!! {}'.format(file_path))

    # pub_date_l = re.findall(r'<time class="updated" datetime="(.+?)T', long_str)
    pub_date_l = re.findall(r'<time class="entry-time" itemprop="datePublished" datetime="(.+?)">', long_str)
    if pub_date_l:
        pub_date = pub_date_l[0]
        pub_date = pub_date.replace('年', '-').replace('月', '-').replace('日', '-')
    else:
        print('no pub_date !')
        pub_date = '2017-10-11'

    result = 't::' + title + '\n'
    result += 'd::' + description + '\n'
    result += 'n::' + str(p_num) + '\n'
    if key_word == 'n_a':
        result += 'k::\n'
    else:
        result += 'k::' + ' '.join(key_word) + '\n'
    result += 'f::' + new_path + '\n'
    result += 'p::' + pub_date + '\n'
    result += '\n# ' + h1 + '\n\n'
    result += html_to_markdown(main_str, remove_list, md_path, pd).replace('</div>', '') \
        .replace('<div class="redbox">', '## ').replace('&nbsp;', '').replace('<div id="kanren">', '')
    naked_str = re.sub(r'<.+?>', '', result + h1)
    str_len = len(naked_str)
    pk_data = {'file_path': file_path,
               'title': title,
               'pub_date': pub_date,
               'mod_date': today,
               'category': category,
               'description': description,
               'str_len': str_len,
               'layout_flag': True,
               'shift_flag': False}
    with open(md_path, 'w', encoding='utf-8') as g:
        g.write(result)
    return pk_data


def relative_path_maker(link_str, md_path):
    link_back = link_str.count('../')
    html_path = re.sub(r'^.*md_files/', 'html_files/', md_path)
    path_spl = html_path.split('/')
    target_path = '/'.join(path_spl[:-(link_back + 1)]) + '/' + re.sub(r'^.*\./', '', link_str)
    num_back = target_path.count('/')
    return '../' * num_back + re.sub(r'/$', '', target_path)


def aff_link_filter(long_str, pd):
    if 'track.bannerbridge.net' in long_str:
        bn_str_l = re.findall(r'<a href="http://track\.bannerbridge\.net/.+?>.+?</a>', long_str)
        if bn_str_l:
            for bn_str in bn_str_l:
                if '<img' not in bn_str:
                    if 'ハッピーメール' in bn_str:
                        af_text = 'ハッピーメール'
                        af_link = pd['aff_dir'] + '/happymail'
                    elif 'ミント' in bn_str:
                        af_text = 'Jメール'
                        af_link = pd['aff_dir'] + '/mintj'
                    elif 'メルパラ' in bn_str:
                        af_text = 'メルパラ'
                        af_link = pd['aff_dir'] + '/meru-para'
                    elif 'PCMAX' in bn_str:
                        af_text = 'PCMAX'
                        af_link = pd['aff_dir'] + '/pcmax'
                    elif 'ワイワイシー' in bn_str or 'YYC' in bn_str or 'yyc' in bn_str:
                        af_text = 'YYC'
                        af_link = pd['aff_dir'] + '/yyc'
                    else:
                        print('unknown link')
                        af_text = re.findall(r'<a href="http://track\.bannerbridge\.net/.+?>(.+?)</a>', bn_str)[0]
                        af_link = 'uk_link'
                    long_str = re.sub(bn_str + r'<img.+?>', '[{}](../../../html_files/{})'.format(af_text, af_link),
                                      long_str)
                    long_str = long_str.replace(bn_str, '[{}](../../../html_files/{})'.format(af_text, af_link))
        bn_img_l = re.findall(r'<img src="http://track\.bannerbridge\.net/.+?>', long_str)
        if bn_img_l:
            for bn_img in bn_img_l:
                if 'width="1" height="1"' in bn_img:
                    long_str = long_str.replace(bn_img, '')
    return long_str


def html_to_markdown(long_str, remove_list, md_path, pd):
    for r_str in remove_list:
        long_str = long_str.replace(r_str, '')
    long_str = re.sub(r'<div id="mokujio">.+?</nav></div>', '', long_str)
    long_str = re.sub(r'<div class="kanren"><h2>関連記事</h2><ul>(.+?)</ul></div>', r'%kanren%\n\1\n\n', long_str)
    long_str = re.sub(r'<h2><span id="sc\d+">(.+?)</span></h2>', r'##\1\n\n', long_str)
    long_str = re.sub(r'<h3><span id="sc\d+">(.+?)</span></h3>', r'###\1\n\n', long_str)
    long_str = re.sub(r'<h4><span id="sc\d+">(.+?)</span></h4>', r'####\1\n\n', long_str)
    long_str = re.sub(r'<h5><span id="sc\d+">(.+?)</span></h5>', r'#####\1\n\n', long_str)
    long_str = re.sub(r'<h2>(.+?)</h2>', r'## \1\n\n', long_str)
    long_str = re.sub(r'<h3>(.+?)</h3>', r'### \1\n\n', long_str)
    long_str = re.sub(r'<h4>(.+?)</h4>', r'#### \1\n\n', long_str)
    long_str = re.sub(r'<h5>(.+?)</h5>', r'##### \1\n\n', long_str)
    long_str = long_str.replace('<section>', '')
    long_str = long_str.replace('</section>', '')
    long_str = re.sub(r'<div class="btnli"><ul>(.+?)</ul></div>', r'%btnli\n\n\1\n\n', long_str)
    long_str = re.sub(r'<ul class="btnli">(.+?)</ul>', r'%btnli\n\n\1\n\n', long_str)
    long_str = re.sub(r'<ul class="libut">(.+?)</ul>', r'%libut\n\n\1\n\n', long_str)
    long_str = re.sub(r'<div class="arlist"><ul>(.+?)</ul></div>', r'%arlist\n\n\1\n\n', long_str)
    long_str = re.sub(r'<ul class="arlist">(.+?)</ul>', r'%arlist\n\n\1\n\n', long_str)
    long_str = re.sub(r'<ul>(.+?)</ul>', r'%arlist%\n\n\1\n\n', long_str)
    long_str = re.sub(r'<li>(.+?)</li>', r'- \1\n', long_str)
    long_str = aff_link_filter(long_str, pd)
    a_str_l = re.findall(r'<a href=".+?".*?>.+?</a>', long_str)
    if a_str_l:
        for a_str in a_str_l:
            a_str_inner_l = re.findall(r'<a href="(.+?)".*?>(.+?)</a>', a_str)
            if a_str_inner_l:
                a_str_inner = a_str_inner_l[0]
                if '#SC' in a_str_inner[0] or '#sc' in a_str_inner[0]:
                    url_str = a_str_inner[0].replace('SC', 'sc')
                # elif '/app/' in a_str_inner[0]:
                #     url_str = '../../../reibun/app/'
                # elif '/ds/' in a_str_inner[0]:
                #     url_str = '../../../reibun/pc/' + a_str_inner[0].replace('../ds/', 'ds/')
                elif 'http://' in a_str_inner[0] or 'https://' in a_str_inner[0]:
                    url_str = a_str_inner[0]
                else:
                    url_str = relative_path_maker(a_str_inner[0], md_path)
                    print('relative_link: ' + url_str)
                long_str = long_str.replace(a_str, '[' + a_str_inner[1] + '](' + url_str + ')')

    long_str = re.sub(r'<span class="hutoaka">(.+?)</span>', r'**\1**', long_str)
    long_str = re.sub(r'<strong>(.+?)</strong>', r'**\1**', long_str)
    long_str = re.sub(r'<b>(.+?)</b>', r'**\1**', long_str)
    long_str = re.sub(r'<span class="hutokuro">(.+?)</span>', r'*\1*', long_str)
    long_str = re.sub(r'<em>(.+?)</em>', r'*\1*', long_str)

    long_str = re.sub(r'<div class="mail">(.+?)</div>', r'%m%\1\n\n', long_str)
    long_str = re.sub(r'<div class="wmail">(.+?)</div>', r'%w%\1\n\n', long_str)
    long_str = re.sub(r'<div class="cm">(.+?)</div>', r'\n\1\n\n', long_str)
    long_str = re.sub(r'<div class="comment">(.+?)</div>', r'\n\1\n\n', long_str)
    long_str = re.sub(r'<div class="kenmei">(.+?)</div>', r'%k%\1\n\n', long_str)
    long_str = long_str.replace('<div class="arr"><img width="17" height="17" src="../images/arr.png" alt="↓"></div>',
                                '%arr\n\n')
    # long_str = re.sub(r'<div class="sample">([\s\S]+?)</div>', r'%%%\n\n\1%%%\n\n', long_str)
    long_str = re.sub(r'<div class="sample">([\s\S]+?)</div>', r'\1', long_str)
    long_str = re.sub(r'<p>(.+?)</p>', r'\1\n\n', long_str)
    long_str = long_str.replace('<br>', '\n')
    long_str = long_str.replace('<br />', '\n')
    long_str = long_str.replace('<br/>', '\n')
    # print(long_str)
    return long_str


def make_category_data_str(project_dir, main_dir):
    result = {}
    all_md_files = glob.glob(project_dir + '/md_files/**/**.md', recursive=True)
    print(all_md_files)
    dir_list = [re.sub(project_dir + r'/md_files/' + main_dir + r'(.+)/.*$', r'\1', x) for x in all_md_files]
    dir_list = list(set(dir_list))
    print(dir_list)
    dir_list = [x for x in dir_list if '.md' not in x]
    for d_path in dir_list:
        dir_index = project_dir + '/md_files/' + main_dir + '/' + d_path + '/index.md'
        if os.path.exists(dir_index):
            with open(dir_index, 'r', encoding='utf-8') as f:
                long_str = f.read()
                m_id = re.findall(r'n::(\d+?)\n', long_str)[0]
                m_title = re.findall(r't::(.+?)\n', long_str)[0]
                result[d_path] = [m_title, 'index.html', int(m_id)]
        else:
            result[d_path] = ['na', 'na', 'na']
    print(result)
    return result


if __name__ == '__main__':
    p_d = {'project_dir': 'rei_site', 'site_name': '出会い系メールの例文サイト', 'main_dir': 'pc/', 'aff_dir': 'http'}
    all_file_to_markdown('../rei_site/old_files/pc', 'rei_site/md_files/pc', p_d, 'pc/',
                         ['<div id="back"><a href="#top"><img src="../stylesheet/back.png" width="100" height="25"'
                          ' border="0" alt="ページTOPに戻る"></a></div></div>'])
    # del_note_dir('rei_site/old_files')
    # insert_canonical('rei_site/rep_rs/sp')
    # make_project_dir('rei_site')
    # print(relative_path_maker('../option/howtouse.html', 'rei_site/md_files/adult/a1.md'))
    make_category_data_str('../rei_site', 'pc/')
