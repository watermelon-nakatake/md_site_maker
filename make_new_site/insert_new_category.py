import glob
import re


def insert_category_to_template_and_normal_html(project_dir, new_cat_dict):
    with open(project_dir + '/html_files/template/main_tmp.html', 'r', encoding='utf-8') as f:
        temp_str = f.read()
    h_str = re.findall(r'<ul id="h_nav">(.*?)</ul>', temp_str)[0]
    h_str = h_str.replace('/index.html', '').replace('/"', '"')
    print(h_str)
    m_str = re.findall(r'<div class="sbh dtn">メニュー</div><ul>(.*?)</ul>', temp_str)[0]
    m_str = m_str.replace('/index.html', '').replace('/"', '"')
    print(m_str)
    s_str = re.findall(r'<nav id="slide_menu"><ul>(.*?)</ul>', temp_str)[0]
    s_str = s_str.replace('/index.html', '').replace('/"', '"')
    print(s_str)
    h_list = re.findall(r'<li.*?><a href="(.*?)">(.*?)</a></li>', h_str)
    print(h_list)
    h_dict = {}
    for h_li in h_list:
        h_dict[h_li[0].replace('../', '')] = h_li[1]
    target_str = ''.join(['<li><a href="../{}">{}</a></li>'.format(x, h_dict[x]) for x in h_dict])
    print(target_str)
    h_dict.update(new_cat_dict)
    print(h_dict)
    new_str = ''.join(['<li><a href="../{}">{}</a></li>'.format(x, h_dict[x]) for x in h_dict])
    print(new_str)
    new_m = m_str.replace(target_str, new_str)
    print(new_m)
    new_s = s_str.replace(target_str, new_str)
    temp_str = re.sub(r'<ul id="h_nav">.*?</ul>', '<ul id="h_nav">{}</ul>'.format(new_str), temp_str)
    temp_str = re.sub(r'<div class="sbh dtn">メニュー</div><ul>.*?</ul>',
                      '<div class="sbh dtn">メニュー</div><ul>{}</ul>'.format(new_m), temp_str)
    temp_str = re.sub(r'<nav id="slide_menu"><ul>.*?</ul>', '<nav id="slide_menu"><ul>{}</ul>'.format(new_s), temp_str)

    with open(project_dir + '/html_files/template/main_tmp.html', 'w', encoding='utf-8') as g:
        g.write(temp_str)

    html_files = glob.glob(project_dir + '/html_files/**/**.html', recursive=True)
    print(html_files)
    for file_path in html_files:
        s_num = file_path.count('/')
        if s_num > 2:
            with open(file_path, 'r', encoding='utf-8') as h:
                long_str = h.read()
            long_str = re.sub(r'<ul id="h_nav">.*?</ul>', '<ul id="h_nav">{}</ul>'.format(new_str), long_str)
            long_str = re.sub(r'<div class="sbh dtn">メニュー</div><ul>.*?</ul>',
                              '<div class="sbh dtn">メニュー</div><ul>{}</ul>'.format(new_m), long_str)
            long_str = re.sub(r'<nav id="slide_menu"><ul>.*?</ul>', '<nav id="slide_menu"><ul>{}</ul>'.format(new_s),
                              long_str)
            with open(file_path, 'w', encoding='utf-8') as j:
                j.write(long_str)
        elif s_num == 2:
            with open(file_path, 'r', encoding='utf-8') as k:
                long_str = k.read()
            long_str = re.sub(r'<ul id="h_nav">.*?</ul>', '<ul id="h_nav">{}</ul>'.format(new_str).replace('../', ''),
                              long_str)
            long_str = re.sub(r'<div class="sbh dtn">メニュー</div><ul>.*?</ul>',
                              '<div class="sbh dtn">メニュー</div><ul>{}</ul>'.format(new_m).replace('../', ''),
                              long_str)
            long_str = re.sub(r'<nav id="slide_menu"><ul>.*?</ul>',
                              '<nav id="slide_menu"><ul>{}</ul>'.format(new_s).replace('../', ''),
                              long_str)
            with open(file_path, 'w', encoding='utf-8') as l:
                l.write(long_str)


if __name__ == '__main__':
    insert_category_to_template_and_normal_html('joshideai', {'website': '出会い系で出会う'})
