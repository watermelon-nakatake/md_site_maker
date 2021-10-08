import re


def delete_no_use_selector(css_path, html_path):
    result = ''
    with open(html_path, 'r', encoding='utf-8') as h:
        html_str = h.read()
    id_list = list(set(re.findall(r'<.+? id="(.+?)"', html_str)))
    id_list = ['#{}'.format(x) for x in id_list]
    print(id_list)
    class_list = list(set(re.findall(r'<.+? class="(.+?)"', html_str)))
    class_list = ['.{}'.format(x) for x in class_list]
    class_list_e = []
    for y in class_list:
        if ' ' in y:
            class_list_e.extend(y.split())
        else:
            class_list_e.append(y)
    print(class_list_e)
    tag_list = list(set([x for x in re.findall(r'<(.+?)[ |>]', html_str) if not x.startswith('/')]))
    print(tag_list)
    all_list = id_list + class_list_e + tag_list

    with open(css_path, 'r', encoding='utf-8') as f:
        css_str = f.read()
    css_str = css_filter(css_str)
    media_list = css_str.split('@media')
    new_list = []
    for m_str in media_list:
        if 'charset' in m_str:
            o_str = re.sub(r'^.+?;', '', m_str)
        else:
            o_str = re.sub(r'^.+?\{', '', m_str)
            o_str = re.sub(r'}$', '', o_str)
        new_list.append(o_str)
    # print(new_list)
    for row in new_list:
        m_result = []
        r_list = row.split('}')
        for r in r_list:
            u_flag = False
            # print(r)
            s_str = re.sub(r'\{.*$', '', r)
            selector_l = s_str.split()
            selector_l = [x.replace(',', '') if ',' in x else x for x in selector_l]
            selector_l = [re.sub(r':.*$', '', x) if ':' in x else x for x in selector_l]
            # print(selector_l)
            for s in selector_l:
                if ('.' in s or '#' in s) and s in all_list:
                    u_flag = True
                    break
                elif len(selector_l) == 1 and s in all_list:
                    u_flag = True
                    break
            if u_flag:
                m_result.append(r + '}')
        m_r_str = '\n'.join(m_result)
        # print(m_r_str)
        result += '@media {\n' + m_r_str + '\n}\n\n'
    print(result)


def css_filter(css_str):
    css_str = re.sub(r'/\*.+?\*/', '', css_str)
    css_str = re.sub(r'}\s*', '}', css_str)
    css_str = re.sub(r'\s*}', '}', css_str)
    css_str = re.sub(r'\{\s*', '{', css_str)
    css_str = re.sub(r'\s*\{', '{', css_str)
    css_str = re.sub(r';\s*', ';', css_str)
    # print(css_str)
    return css_str


if __name__ == '__main__':
    delete_no_use_selector('rei_site/html_files/css/main.css', 'shoshin/html_files/contents.html')
