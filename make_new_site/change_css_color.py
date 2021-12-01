import glob
import importlib
import re
import make_new_article
import file_upload


def change_css(project_dir, color_dict):
    with open(project_dir + '/html_files/css/main_copy.css', 'r', encoding='utf-8') as f:
        css_str = f.read()
    css_str = re.sub(r'(\n\s*)', '', css_str)
    css_str = css_str.replace(', ', ',').replace(': ', ':').replace('; ', ';').replace(' {', '{').replace(';}', '}') \
        .replace('. ', '.')
    # main
    css_str = re.sub(r'(}h2,\.sbh{.*?background-color:)\S+?;(.*?})', r'\1{};\2'.format(c_dict['main']), css_str)

    css_str = re.sub(r'(}h2{.*?background-color:)\S+?;(.*?})', r'\1{};\2'.format(c_dict['main']), css_str)

    css_str = re.sub(r'(}#cpr{.*?background-color:)\S+?;(.*?})', r'\1{};\2'.format(c_dict['main']), css_str)

    css_str = re.sub(r'(}\.kijoph{.*?color:)\S+?;(.*?})', r'\1{};\2'.format(c_dict['main']), css_str)

    css_str = re.sub(r'(}\.lb_c_b{.*?background-color:)\S+?;(.*?})', r'\1{};\2'.format(c_dict['main']), css_str)

    css_str = re.sub(r'(}h1{.*?border-bottom:2px solid )\S+?;(.*?})', r'\1{};\2'.format(c_dict['main']), css_str)

    css_str = re.sub(r'(}h3{.*?color:)\S+?;(.*?})', r'\1{};\2'.format(c_dict['h3']), css_str)

    css_str = re.sub(r'(}\.fr2{.*?background-color:)\S+?;(.*?})', r'\1{};\2'.format(c_dict['balloon']), css_str)

    css_str = re.sub(r'(}\.fr2::before{.*?border-left:15px solid )\S+?;(.*?})', r'\1{};\2'.format(c_dict['balloon']), css_str)

    css_str = re.sub(r'(}\.sbh{.*?background:url\("\.\./images/common/)\S+?(".*?})',
                     r'\1{}\2'.format(c_dict['icon']), css_str)

    # print(css_str)
    with open(project_dir + '/html_files/css/main.css', 'w', encoding='utf-8') as g:
        g.write(css_str)


def insert_star_to_css_and_html(project_dir):
    html_files = glob.glob(project_dir + '/html_files/**/**.html', recursive=True)
    print(html_files)
    for h_path in html_files:
        with open(h_path, 'r', encoding='utf-8') as f:
            long_str = f.read()
        sbh_list = re.findall(r'<div class="sbh">(.+?)</div>', long_str)
        for sbh_str in sbh_list:
            if '<span class="ball">' not in sbh_str:
                long_str = re.sub(r'<div class="sbh">' + sbh_str + '</div>',
                                  '<div class="sbh"><span class="ball"></span>' + sbh_str + '</div>', long_str)
        print(long_str)


def insert_all_css(before, after, check_str, c_count):
    # project_dir = [x for x in make_new_article.dir_dict]
    # project_dir.extend(['reibun'])
    # project_dir.remove('test')
    # project_dir.remove('sfd')
    # project_dir.remove('mass')
    # project_dir.remove('shoshin')
    project_dir = ['test']
    for pj in project_dir:
        pj_css = pj + '/html_files/css/main.css'
        with open(pj_css, 'r', encoding='utf-8') as f:
            css_str = f.read()
        if css_str.count(check_str) < c_count:
            new_str = css_str.replace(before, after)
            if new_str != css_str:
                with open(pj_css, 'w', encoding='utf-8') as g:
                    g.write(new_str)
                info_mod = importlib.import_module(pj + '.main_info')
                # file_upload.scp_upload([pj_css], info_mod.info_dict)


if __name__ == '__main__':
    # c_dict = {'main': '#EF8E3E',
    #           'h3': '#EF8E3E',
    #           'h4': '#000000',
    #           'balloon': '#A5E1FF',
    #           'icon': 'mail_or.png'}
    # change_css('joshideai', c_dict)
    # insert_star_to_css_and_html('joshideai')

    insert_all_css('/*for desk top*/',
                   '.alt_img_t img {width: 90%;margin-top: 10px;margin-left: 5%;margin-bottom: 5px;height: auto;}'
                   '/*for desk top*/',
                   '.alt_img_t img', 1)
