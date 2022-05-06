import glob
import os
import pathlib
import re


def move_up_html(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html_str = f.read()
    if '/index.html' not in html_path and 'sitemap.html' not in html_path and '_copy' not in html_path:
        a_str_l = re.findall(r'<a .+?>.+?<', html_str)
        for a_str in a_str_l:
            if 'http' not in a_str and '//' not in a_str and '#' not in a_str:
                ins_str = a_str.replace('href="', 'href="../')
                if 'index.html' not in a_str and 'sitemap.html' not in a_str:
                    ins_str = ins_str.replace('.html', '/')
                html_str = html_str.replace(a_str, ins_str)
        s_str_l = re.findall(r'src=".*?"', html_str)
        for s_str in s_str_l:
            if 'http' not in s_str and '//' not in s_str:
                ins_s = s_str.replace('src="', 'src="../')
                html_str = html_str.replace(s_str, ins_s)
        html_str = html_str.replace('<link href="', '<link href="../')

        new_path = html_path.replace('/html_files/', '/up_html/').replace('.html', '/index.html')
        this_dir = new_path.replace('/index.html', '')
        file_name = re.sub(r'^.*/', '', html_path)
        new_file_name = file_name.replace('.html', '/')
        html_str = html_str.replace(file_name, new_file_name)
        if not os.path.exists(this_dir):
            os.mkdir(this_dir)
    else:
        a_str_l = re.findall(r'<a .+?>.+?<', html_str)
        for a_str in a_str_l:
            if 'http' not in a_str and '//' not in a_str and '#' not in a_str and 'sitemap.html' not in a_str:
                ins_str = a_str
                if 'index.html' not in a_str:
                    ins_str = ins_str.replace('.html', '/')
                html_str = html_str.replace(a_str, ins_str)
        new_path = html_path.replace('/html_files/', '/up_html/')
    with open(new_path, 'w', encoding='utf-8') as g:
        g.write(html_str)


def img_move_after_h2_in_md():
    all_md_files = glob.glob('sfd/md_files/**/**.md', recursive=True)
    counter = 1
    for md_path in all_md_files:
        # md_path = 'sfd/md_files/friend-with-benefits/difference-between-sefure-and-lover.md'
        p = pathlib.Path(md_path)
        p.open()
        md_str = p.read_text()
        h_l = re.findall(r'\n## .+?\n', md_str)
        b_h_s = re.sub(r'^([\S\s]+?\n)## ', r'\1', md_str)
        i_l = re.findall(r'\n!\[.*?]\(.+?\)', b_h_s)
        if i_l and h_l:
            print('{} {}'.format(counter, md_path))
            md_str = md_str.replace(i_l[0], '').replace(h_l[0], h_l[0] + i_l[0] + '\n')
            # print(md_str)
            # break
            p.open(mode='w')
            p.write_text(md_str)
            counter += 1


def main(update_files):
    all_html_files = glob.glob('sfd/html_files/**/**.html', recursive=True)
    # print(all_html_files)
    # all_html_files = ['sfd/html_files/index.html', 'sfd/html_files/sitemap.html']
    for html_file_path in update_files:
        if '/template/' not in html_file_path and '_copy' not in html_file_path and '.html' in html_file_path:
            move_up_html(html_file_path)


if __name__ == '__main__':
    main(['sfd/html_files/index.html', 'sfd/html_files/sitemap.html'])
    # img_move_after_h2_in_md()
