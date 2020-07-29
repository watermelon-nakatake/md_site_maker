import glob
import re
import reibun_upload

json_tmp = '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Article",' \
           '"mainEntityOfPage":"https://www.demr.jp/pc/<!--path-->","headline":"<!--title-->",' \
           '"datePublished":"<!--pub-date-->","dateModified":"<!--mod-date-->","description":"<!--description-->",' \
           '"author":{"@type":"Person","name":"ゴーヤン"},"publisher":{"@type":"Organization","name":"出会い系メール例文集",' \
           '"logo":{"@type":"ImageObject","url":"https://www.demr.jp/amp/images/common/site_name_400.png","width":400,' \
           '"height":59}},"image":{"@type":"ImageObject","url":"https://www.demr.jp/pc/images/<!--img-path-->",' \
           '"height":<!--height-->,"width":<!--width-->}}</script>'


def all_html_pick_up(dir_path):
    files = glob.glob(dir_path + '/*.html', recursive=True) + glob.glob(dir_path + '/*/*.html', recursive=True) \
            + glob.glob(dir_path + '/*/*/*.html', recursive=True)
    files = [x for x in files if '_copy' not in x and '_test' not in x]
    return files


def insert_json_to_html(dir_path):
    change_files = []
    # files = all_html_pick_up(dir_path)
    files = ['reibun/index.html']
    for file_path in files:
        print(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            long_str = f.read()
            next_str = insert_json_to_str(file_path, long_str)
            if long_str != next_str:
                with open(file_path, 'w', encoding='utf-8') as g:
                    g.write(next_str)
                change_files.append(change_files)
    # reibun_upload.ftp_upload(change_files)


def insert_json_to_str(file_path, long_str):
    if '<script type="application/ld+json">' not in long_str:
        path = file_path.replace('reibun/pc/', '')
        title = re.findall(r'<title>(.+?)</title>', long_str)[0]
        pub_date = re.findall(r'<time itemprop="datePublished" datetime="(.+?)">', long_str)[0]
        mod_date = re.findall(r'<time itemprop="dateModified" datetime="(.+?)">', long_str)[0]
        description = re.findall(r'<meta name="description" content="(.+?)">', long_str)[0]
        img_path = 'eyec.jpg'
        height = 464
        width = 700
        if '<div class="alt_img_t">' in long_str:
            img_l = re.findall(r'<div class="alt_img_t"><img src="\.\./images/(.+?)" alt="', long_str)
            if img_l:
                img_path = img_l[0]
                height = 470
                width = 760
        i_str = json_tmp.replace('<!--path-->', path)
        i_str = i_str.replace('<!--title-->', title)
        i_str = i_str.replace('<!--pub-date-->', pub_date)
        i_str = i_str.replace('<!--mod-date-->', mod_date)
        i_str = i_str.replace('<!--description-->', description)
        i_str = i_str.replace('<!--img-path-->', img_path)
        i_str = i_str.replace('<!--height-->', str(height))
        i_str = i_str.replace('<!--width-->', str(width))
        long_str = long_str.replace('</body>', i_str + '</body>')
    return long_str


if __name__ == '__main__':
    insert_json_to_html('reibun/pc')
