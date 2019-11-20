import re
import os
import amp_file_maker
up_dir = ['caption/', 'majime/', 'policy/', 'qa/', 'site/']


def main():
    print('あ')


def all_file_to_markdown():
    change_files = []
    for dir_u in up_dir:
        files = os.listdir('reibun/pc/' + dir_u)
        for file in files:
            change_files.append('reibun/pc/' + dir_u + file)
    for file_c in change_files:
        print(file_c)
        file_to_markdown(file_c)


def file_to_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        long_str = f.read()
        directory = re.sub(r'reibun/pc/(.+?)/.+?.html', r'\1', file_path)
        long_str = amp_file_maker.tab_and_line_feed_remover(long_str)

        title_l = re.findall(r'<title>(.+?)\|出会い系メール例文集</title>', long_str)
        if title_l:
            title = title_l[0]
        else:
            title_l = re.findall(r'<title>(.+?)</title>', long_str)
            if title_l:
                title = title_l[0]
            else:
                print('no title !')
                return
        key_word_l = re.findall(r'<meta name="keywords" content="(.+?)">', long_str)
        if key_word_l:
            key_word = key_word_l[0].split(',')
        else:
            print('no key_word !')
            return
        description_l = re.findall(r'<meta name="description" content="(.+?)">', long_str)
        if description_l:
            description = description_l[0]
        else:
            print('no key_word !')
            return
        key_word_o_l = re.findall(r'<!--kw#(.+?)-->', long_str)
        if key_word_o_l:
            key_word_o = key_word_o_l[0].split('#')
        else:
            key_word_o = ''
        h1_l = re.findall(r'<h1 itemprop="headline alternativeHeadline name">(.+?)</h1>', long_str)
        if h1_l:
            h1 = h1_l[0]
        else:
            print('no h1 !')
            return
        if '</article>' not in long_str:
            long_str = long_str.replace('</section><div class="efooter">', '</section></article><div class="efooter">')
        content_l = re.findall(r'</time></div>(.+?)</article>', long_str)
        if content_l:
            content_str = html_to_markdown(content_l[0], directory)
        else:
            print('no contents !')
            return
        pub_date_l = re.findall(r'<time itemprop="datePublished" datetime="(.+?)">', long_str)
        if pub_date_l:
            pub_date = pub_date_l[0]
        else:
            print('no pub_date !')
            return
        result = 't::' + title + '\n'
        result += 'd::' + description + '\n'
        result += 'f::' + file_path.replace('reibun/pc/', '') + '\n'
        result += 'k::' + ' '.join(key_word)
        if key_word_o:
            result += ' & ' + ' '.join(key_word_o) + '\n'
        else:
            result += '\n'
        result += 'p::' + pub_date + '\n'
        result += '\n#' + h1 + '\n\n'
        result += content_str
        with open(file_path.replace('reibun/', 'md_files/').replace('.html', '.md'), 'w', encoding='utf-8') as g:
            g.write(result)


def html_to_markdown(long_str, directory):
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
    long_str = long_str.replace('<div class="center"><a href="../../app/">'
                                '<img class="app_bn1" src="../images/common/app_bn_f.png" alt="出会い系メール例文アプリ">'
                                '</a></div>', '%app_b%\n\n')
    long_str = re.sub(r'<div class="btnli"><ul>(.+?)</ul></div>', r'%btnli%\n\1\n\n', long_str)
    long_str = re.sub(r'<ul class="btnli">(.+?)</ul>', r'%btnli%\n\1\n\n', long_str)
    long_str = re.sub(r'<ul class="libut">(.+?)</ul>', r'%libut%\n\1\n\n', long_str)
    long_str = re.sub(r'<div class="arlist"><ul>(.+?)</ul></div>', r'%arlist%\n\1\n\n', long_str)
    long_str = re.sub(r'<ul class="arlist">(.+?)</ul>', r'%arlist%\n\1\n\n', long_str)
    long_str = re.sub(r'<li>(.+?)</li>', r'- \1\n', long_str)

    a_str_l = re.findall(r'<a href=".+?">.+?</a>', long_str)
    if a_str_l:
        for a_str in a_str_l:
            a_str_inner_l = re.findall(r'<a href="(.+?)">(.+?)</a>', a_str)
            if a_str_inner_l:
                a_str_inner = a_str_inner_l[0]
                if '#SC' in a_str_inner[0] or '#sc' in a_str_inner[0]:
                    url_str = a_str_inner[0].replace('SC', 'sc')
                elif '/app/' in a_str_inner[0]:
                    url_str = '../../../reibun/app/'
                elif '/ds/' in a_str_inner[0]:
                    url_str = '../../../reibun/pc/' + a_str_inner[0].replace('../ds/', 'ds/')
                elif a_str_inner[0].count('/') == 0:
                    url_str = '../../../reibun/pc/' + directory + '/' + a_str_inner[0]
                elif a_str_inner[0].count('/') == 2:
                    url_str = '../../../reibun/pc/' + a_str_inner[0].replace('../', '')

                elif a_str_inner[0].count('/') == 4:
                    url_str = '../../../reibun/pc/' + a_str_inner[0].replace('../../', '')
                else:
                    url_str = a_str_inner[0]
                    print('unknown link ! : ' + url_str)
                long_str = long_str.replace(a_str, '[' + a_str_inner[1] + '](' + url_str + ')')

    long_str = re.sub(r'<span class="hutoaka">(.+?)</span>', r'**\1**', long_str)
    long_str = re.sub(r'<strong>(.+?)</strong>', r'**\1**', long_str)
    long_str = re.sub(r'<b>(.+?)</b>', r'**\1**', long_str)
    long_str = re.sub(r'<span class="hutokuro">(.+?)</span>', r'*\1*', long_str)
    long_str = re.sub(r'<em>(.+?)</em>', r'*\1*', long_str)

    long_str = re.sub(r'<div class="mail">(.+?)</div>', r'%m%\1\n\n', long_str)
    long_str = re.sub(r'<div class="wmail">(.+?)</div>', r'%w%\1\n\n', long_str)
    long_str = re.sub(r'<div class="cm">(.+?)</div>', r'%cm%\1\n\n', long_str)
    long_str = re.sub(r'<div class="kenmei">(.+?)</div>', r'%k%\1\n\n', long_str)
    long_str = long_str.replace('<div class="arr"><img width="17" height="17" src="../images/arr.png" alt="↓"></div>',
                                '%arr\n\n')
    # long_str = re.sub(r'<div class="sample">([\s\S]+?)</div>', r'%%%\n\n\1%%%\n\n', long_str)
    long_str = re.sub(r'<div class="sample">([\s\S]+?)</div>', r'\1', long_str)
    long_str = re.sub(r'<p>(.+?)</p>', r'\1\n\n', long_str)
    long_str = long_str.replace('<br>', '\n')
    # print(long_str)
    return long_str


if __name__ == '__main__':
    file_to_markdown('reibun/index.html')
    # all_file_to_markdown()
