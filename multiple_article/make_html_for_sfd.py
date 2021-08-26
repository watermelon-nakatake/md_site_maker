import markdown
import os
import re


def translate_md_to_html(temp_path, md_path_dir, sub_sex):
    with open(temp_path, 'r', encoding='utf-8') as f:
        temp_str = f.read()
    for md_path in os.listdir(md_path_dir):
        temp = temp_str
        with open(md_path_dir + '/' + md_path, 'r', encoding='utf-8') as m:
            main_str = m.read()
        t_str = re.findall(r't::(.+?)\n', main_str)[0]
        temp = temp.replace('<!--title-->', t_str)
        d_str = re.findall(r'd::(.+?)\n', main_str)[0]
        temp = temp.replace('<!--description-->', d_str)
        n_str = re.findall(r'n::(.+?)\n', main_str)[0]
        temp = temp.replace('#id__num#', '#' + n_str + '#')
        k_str = re.findall(r'k::(.+?)\n', main_str)[0]
        temp = temp.replace('#key__words#', '#' + k_str + '#')
        m_str = re.sub(r'^[\s\S]+?k::.*?\n', '', main_str)
        m_str = re.sub(r'recipe_list = {[\s\S]+$', '', m_str)

        m_str = m_str.replace('%arlist%', '\n')
        m_str = re.sub(r'%l_.+?%([\s\S]+?)\n\n', r'\[st-kaiwa1 r]\1[/st-kaiwa1]\n\n', m_str)
        if sub_sex == 'woman':
            m_str = re.sub(r'%r_.+?%([\s\S]+?)\n\n', r'\[st-kaiwa3]\1[/st-kaiwa3]\n\n', m_str)
            m_str = re.sub(r'%r_\?([\s\S]+?)\n\n', r'\[st-kaiwa3]\1[/st-kaiwa3]\n\n', m_str)
        else:
            m_str = re.sub(r'%r_.+?%([\s\S]+?)\n\n', r'\[st-kaiwa2]\1[/st-kaiwa2]\n\n', m_str)
            m_str = re.sub(r'%r_\?([\s\S]+?)\n\n', r'\[st-kaiwa2]\1[/st-kaiwa2]\n\n', m_str)
        m_str = m_str.replace('[st-kaiwa1 r]\n', '[st-kaiwa1 r]')
        m_str = m_str.replace('[st-kaiwa2]\n', '[st-kaiwa2]')
        m_str = m_str.replace('[st-kaiwa3]\n', '[st-kaiwa3]')
        m_str = re.sub(r'<!--sw-.+?-->', '', m_str)
        m_str = re.sub(r'<!--rs-.+?-->', '', m_str)

        ht_str = markdown.markdown(m_str)
        ht_str = ht_str.replace('。\n', '。<br/>\n')
        temp = temp.replace('<!--main-->', ht_str)

        # print(temp)
        with open('sfd/html_files/up_data/' + md_path.replace('.md', '.html'), 'w', encoding='utf-8') as g:
            g.write(temp)


if __name__ == '__main__':
    translate_md_to_html('sfd/wp_temp.html', 'test/md_files/sf_woman_obj2', 'woman')
