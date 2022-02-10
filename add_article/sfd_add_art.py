import markdown
import re


def translate_md_to_html(md_path, sub_sex):
    with open(md_path, 'r', encoding='utf-8') as m:
        main_str = m.read()
    m_str = main_str
    print('text len : {}'.format(len(m_str.replace('\n', '').replace('## ', '').replace('### ', ''))))
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
    m_str = m_str.replace('/link/', '/url/')
    m_str = m_str.replace('../area-bbs/', '/area-bbs/')
    m_str = m_str.replace('../../html_files/url/', '../url/')
    m_str = m_str.replace('../url/', '/url/')
    fb_link_l = re.findall(r']\((.+?)\)', m_str)
    if fb_link_l:
        for fb_link in fb_link_l:
            if '/' not in fb_link:
                m_str = m_str.replace('](' + fb_link + ')', '](/friend-with-benefits/' + fb_link + ')')
    m_str = re.sub(r'<!--sw-.+?-->', '', m_str)
    m_str = re.sub(r'<!--rs-.+?-->', '', m_str)
    # print(m_str)

    ht_str = markdown.markdown(m_str)
    ht_str = insert_section_tag(ht_str)
    ht_str = ht_str.replace('。\n', '。<br/>\n')
    with open(md_path.replace('.md', '.html'), 'w', encoding='utf-8') as g:
        g.write(ht_str)


def insert_section_tag(long_str):
    h_list = re.findall(r'<h\d>.+?</h\d>', long_str)
    # print(h_list)
    for i, h in enumerate(h_list):
        if i == 0:
            long_str = long_str.replace(h, '<section>' + h)
        else:
            if (h.startswith('<h2') and h_list[i - 1].startswith('<h2')) or (h.startswith('<h3') and h_list[i - 1].startswith('<h3')):
                long_str = long_str.replace(h, '</section>\n<section>\n' + h)
            elif (h.startswith('<h2') and h_list[i - 1].startswith('<h3')) or (h.startswith('<h3') and h_list[i - 1].startswith('<h4')):
                long_str = long_str.replace(h, '</section>\n</section>\n<section>\n' + h)
            elif (h.startswith('<h3') and h_list[i - 1].startswith('<h2')) or (h.startswith('<h4') and h_list[i - 1].startswith('<h3')):
                long_str = long_str.replace(h, '<section>\n' + h)
    if h_list[-1].startswith('<h2'):
        long_str = long_str + '\n</section>'
    elif h_list[-1].startswith('<h3'):
        long_str = long_str + '\n</section>\n</section>'

    return long_str


if __name__ == '__main__':
    translate_md_to_html('sfd/md_files/original/fwb.md', 'man')
