import os
import re
from PIL import Image


def copy_from_main_tmp_to_top_and_sm(project_dir):
    with open(project_dir + '/html_files/template/main_tmp.html', 'r', encoding='utf-8') as t:
        tmp_str = t.read()
    with open(project_dir + '/html_files/index.html', 'r', encoding='utf-8') as p:
        p_str = p.read()
    with open(project_dir + '/html_files/sitemap.html', 'r', encoding='utf-8') as s:
        sm_str = s.read()
    for re_str in [r'<ul id="h_nav">.*?</ul>',
                   r'<div class="sbh dtn">メニュー</div><ul>.*?</ul>',
                   r'<div class="sbh">カテゴリー</div><ul>.*?</ul>',
                   r'<nav id="slide_menu"><ul>.*?</ul>',
                   r'<span itemprop="logo".*?</span>',
                   r'<img itemprop="image" src=".*?</span>',
                   r',"author":.*?</script>']:
        m_str_l = re.findall(re_str, tmp_str)
        print(m_str_l)
        if m_str_l:
            m_str = m_str_l[0]
            p_str = re.sub(re_str, m_str.replace('../', ''), p_str)
            sm_str = re.sub(re_str, m_str.replace('../', ''), sm_str)
    print(p_str)
    with open(project_dir + '/html_files/index.html', 'w', encoding='utf-8') as q:
        q.write(p_str)
    with open(project_dir + '/html_files/sitemap.html', 'w', encoding='utf-8') as u:
        u.write(sm_str)


def check_main_temp_for_copy(project_dir):
    with open(project_dir + '/html_files/template/main_tmp.html', 'r', encoding='utf-8') as t:
        tmp_str = t.read()
    if 'site_name_400.png' in tmp_str:
        if os.path.exists('{}/html_files/images/common/site_name_500.png'.format(project_dir)):
            tmp_str = tmp_str.replace('site_name_400.png', 'site_name_500.png')
        else:
            print('change site name image !!')
    if '"width":400,"height":59}}' in tmp_str:
        if os.path.exists('{}/html_files/images/common/site_name_500.png'.format(project_dir)):
            im = Image.open('{}/html_files/images/common/site_name_500.png'.format(project_dir))
            tmp_str = tmp_str.replace('"width":400,"height":59}}', '"width":500,"height":' + str(im.size[1]) + '}}')
    if '<!--t-image-->' in tmp_str:
        if os.path.exists('{}/html_files/images/common/{}_img.jpg'.format(project_dir, project_dir)):
            tmp_str = tmp_str.replace('<!--t-image-->', 'common/{}_img.jpg'.format(project_dir))
        else:
            print('make main image !!')
    if '<!--t-image-->' in tmp_str:
        if os.path.exists('{}/html_files/images/common/{}_img.jpg'.format(project_dir, project_dir)):
            tmp_str = tmp_str.replace('<!--t-image-->', 'common/{}_img.jpg'.format(project_dir))
        else:
            print('make main image !!')
    if 'eyec.jpg' in tmp_str:
        if os.path.exists('{}/html_files/images/common/{}_img.jpg'.format(project_dir, project_dir)):
            tmp_str = tmp_str.replace('eyec.jpg', 'common/{}_img.jpg'.format(project_dir))
        else:
            print('make eye catch image !!')
    if '"height":470,"width":760}}':
        if os.path.exists('{}/html_files/images/common/{}_img.jpg'.format(project_dir, project_dir)):
            tmp_str = tmp_str.replace('"height":470,"width":760}}', '"height":800,"width":1200}}')
            tmp_str = tmp_str.replace('"height":"470","width":"760"}}', '"height":800,"width":1200}}')
    if '"name":"管理人' in tmp_str:
        print('insert author name !!')
    if '<!--jd-' in tmp_str:
        if os.path.exists('{}/html_files/images/common/{}_img.jpg'.format(project_dir, project_dir)):
            tmp_str = tmp_str.replace('<!--jd-img-path-->', 'common/{}_img.jpg'.format(project_dir))
            tmp_str = tmp_str.replace('"<!--jd-height-->"', '800')
            tmp_str = tmp_str.replace('"<!--jd-width-->"', '1200')
    print(tmp_str)
    with open(project_dir + '/html_files/template/main_tmp.html', 'w', encoding='utf-8') as g:
        g.write(tmp_str)

    # s_menu_l = re.findall(r'<div class="sbh dtn">メニュー</div><ul>.*?</ul>', tmp_str)
    # if s_menu_l:
    #     s_menu = s_menu_l[0]
    #     p_str = re.sub(r'<div class="sbh dtn">メニュー</div><ul>.*?</ul>', s_menu.replace('../', ''), p_str)
    #     sm_str = re.sub(r'<div class="sbh dtn">メニュー</div><ul>.*?</ul>', s_menu.replace('../', ''), sm_str)


if __name__ == '__main__':
    target_dir = 'koibito'
    # check_main_temp_for_copy(target_dir)
    copy_from_main_tmp_to_top_and_sm(target_dir)
