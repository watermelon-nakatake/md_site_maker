import re
import os

put_after_tag = ['ul', 'ol', 'li', 'div', 'span', 'a', 'img', 'p']


def duplicate_class_checker(css_path, html_list, new_css_path):
    html_selector_list = []
    for html_path in html_list:
        with open(html_path, 'r', encoding='utf-8') as g:
            html_str = g.read()
        html_str = tab_and_line_feed_remove_from_str(html_str)
        html_selector_list = pick_up_selector_from_html(html_str, html_selector_list)
        html_selector_list = pick_up_selector_from_js(html_str, html_selector_list)
        html_selector_list = html_selector_list + put_after_tag
        print(html_selector_list)
    with open(css_path, 'r', encoding='utf-8') as f:
        css_str = f.read()
        css_str = move_space_and_indention_from_css(css_str)
        css_str = re.sub(r'^@charset.*?;', '', css_str)
        result = css_str_to_dic(css_str, html_selector_list)
        result = '@charset "utf-8";' + result
    print(result)
    with open(new_css_path, 'w', encoding='utf-8') as h:
        h.write(result)


def duplicated_css_remove(css_path):
    result_str = ''
    target_list = []
    with open(css_path, 'r', encoding='utf-8') as f:
        long_str = f.read()
    long_str = move_space_and_indention_from_css(long_str)
    media_list = re.findall(r'@media all and \(.+?\){(.*?})}', long_str)
    no_media = re.findall(r'^(.+?)@media', long_str)[0]
    target_list.append(css_str_to_dic_simple(no_media))
    for media in media_list:
        target_list.append(css_str_to_dic_simple(media))
    media2 = compare_css_contents(target_list[0], target_list[1])
    # print(media2)
    media3 = compare_css_contents(target_list[0], target_list[2])
    # print(media3)
    media3 = compare_css_contents(media2, media3)
    result_str = add_media_to_str(result_str, target_list[0])
    result_str += '/*for desk top*/@media all and (min-width: 1200px) {'
    result_str = add_media_to_str(result_str, media2)
    result_str += '}/*for tablet*/@media all and (min-width: 670px) and (max-width: 1199px) {'
    result_str = add_media_to_str(result_str, media3)
    result_str += '}'
    print(result_str)
    i = 0
    while os.path.exists(css_path.replace('.css', '_test' + str(i) + '.css')):
        i += 1
    with open(css_path.replace('.css', '_test' + str(i) + '.css'), 'w', encoding='utf-8') as g:
        g.write(result_str)


def add_media_to_str(base_str, media_dict):
    for selector in media_dict:
        base_str += selector + '{' + ';'.join(media_dict[selector]) + '}'
    return base_str


def compare_css_contents(base, target):
    result = {}
    for b in target:
        if b in base:
            b_contents = [x for x in target[b] if x not in base[b]]
            if b_contents:
                result[b] = b_contents
        else:
            result[b] = target[b]
    return result


def css_str_to_dic_simple(css_str):
    result = {}
    used_selector = []
    css_str = re.sub(r'/\*.*?\*/', '', css_str)
    css_list = css_str.split('}')
    for css in css_list:
        selector = re.sub(r'{.*$', '', css)
        inner = re.sub(r'^.+?{', '', css)
        contents_l = inner.split(';')
        # print(selector)
        # print(contents_l)
        if selector:
            if selector not in used_selector:
                result[selector] = contents_l
            else:
                for content in contents_l:
                    if content not in result[selector]:
                        result[selector].append(content)
    return result


def css_str_to_dic(css_str, html_selector_list):
    result = ''
    counter = 5
    while counter > 0:
        if '}' * counter in css_str:
            media_list = re.findall(r'@media all and \(.+?\){.*?' + '}' * counter, css_str)
            no_media = re.sub(r'@media all and \(.+?\){.*' + '}' * counter, '', css_str)
            result += css_str_to_selector_dic(no_media, html_selector_list)
            if media_list:
                for media_str in media_list:
                    media_title_l = re.findall(r'^@media all and \(.+?\)', media_str)
                    if media_title_l:
                        media_title = media_title_l[0]
                        result += media_title + '{'
                        media_content = re.sub(r'^@media all and \(.+?\){(.+?)}$', r'\1', media_str)
                        if '@media all and' in media_content:
                            media_content = css_str_to_dic(media_content, html_selector_list)
                        else:
                            media_content = css_str_to_selector_dic(media_content, html_selector_list)
                        result += media_content + '}'
            break
        counter -= 1
    return result


def css_str_to_selector_dic(css_str, html_selector_list):
    result = ''
    css_list2 = []
    reset = ''
    clear_fix = ''
    # print('start')
    # print(css_str)
    css_list = css_str.split('}')
    for c_str in css_list:
        if c_str:
            selector_list = []
            if '/*reset css*/' in c_str:
                selector_list = [x for x in split_selector(c_str) if x in html_selector_list]
                reset = '/*reset css*/' + ','.join(selector_list) + c_str[c_str.find('{'):] + '}'
            elif '/*clear fix*/' in c_str:
                selector_list = [x + ':after' for x in split_selector(c_str) if x in html_selector_list]
                clear_fix = '/*clear fix*/' + ','.join(selector_list) + c_str[c_str.find('{'):] + '}'
            elif ',' in c_str[:c_str.find('{')]:
                # print('=> ' + c_str)
                selector_list = [split_selector_block(x) for x in c_str.split('{')[0].split(',')]
                # print(selector_list)
                css_list2.append([selector_list, c_str + '}'])
            else:
                css_list2.append([split_selector(c_str), c_str + '}'])
    print('css_list2')
    print(css_list2)
    # for p in css_list2:
    #     print(p)
    #     print('\n')
    if '@keyframes' in css_str:
        for css in css_list2:
            if '@keyframes' in css[0]:
                k_num = css_list2.index(css)
                key_plus = 1
                remove_list = []
                key_str = css_list2[k_num][1]
                while '%' in css_list2[k_num + key_plus][0][0]:
                    remove_list.append(css_list2[k_num + key_plus])
                    key_str += css_list2[k_num + key_plus][1]
                    key_plus += 1
                css_list2[k_num - 1] = [css_list2[k_num - 1][0], css_list2[k_num - 1][1] + key_str + '}']
                for remove in remove_list:
                    css_list2.remove(remove)
    for selector in html_selector_list:
        print('!! selector')
        print(selector)
        move_list = []
        much_selector_list = []
        for style in css_list2:
            if type(style[0][0]) != str:
                a_list = []
                new_str = []
                for y in style[0]:
                    a_list.extend(y)
                if selector in a_list:
                    if set(a_list).issubset(html_selector_list):
                        top_selector = []
                        for sub_selector in style[0]:
                            if selector in sub_selector:
                                top_selector = sub_selector
                                break
                        much_selector_list.append([top_selector, style[1]])
                        move_list.append(style)
                    else:
                        # print('there is no use selector!')
                        # print(style[1])
                        sp_str = style[1].split('{')
                        c_sp_str_list = [re.sub(r'^ ', '', x) for x in sp_str[0].split(',')]
                        for c in range(len(style[0])):
                            if set(style[0][c]).issubset(html_selector_list):
                                new_str.append(c_sp_str_list[c])
                                # print('there')
                                # print(style[0][c])
                                # print(c_sp_str_list[c])
                        # print(new_str)
                        if new_str:
                            much_selector_list.append([[selector], ','.join(new_str) + '{' + sp_str[1]])
                        move_list.append(style)
                        # print(','.join(new_str) + '{' + sp_str[1])
            else:
                if selector in style[0]:
                    if set(style[0]).issubset(html_selector_list):
                        much_selector_list.append(style)
                        move_list.append(style)
        if selector == put_after_tag[0]:
            result += '/*base tag start*/'
        if len(much_selector_list) == 1:
            result += much_selector_list[0][1]
        elif len(much_selector_list) > 1:
            list_len = 1
            while much_selector_list:
                use_list = [x for x in much_selector_list if len(x[0]) == list_len]
                use_list = sorted(use_list, key=lambda a: a[0].index(selector))
                result += ''.join([x[1] for x in use_list])
                for use in use_list:
                    much_selector_list.remove(use)
                list_len += 1
        for move in move_list:
            css_list2.remove(move)
    if '/*base tag start*/' in result:
        split_result = result.split('/*base tag start*/')
        result = split_result[1] + split_result[0]
    return reset + result + clear_fix


def split_selector(c_str):
    selector_list = re.sub(r'/\*.*?\*/', '', c_str[:c_str.find('{')]).replace('.', ' .').replace(',', ' ') \
        .replace('  ', ' ').split(' ')
    selector_list = [re.sub(r':.+$', '', x) for x in selector_list if x]
    return selector_list


def split_selector_block(c_str):
    selector_list = re.sub(r'/\*.*?\*/', '', c_str).replace('.', ' .').replace(',', ' ') \
        .replace('  ', ' ').split(' ')
    selector_list = [re.sub(r':.+$', '', x) for x in selector_list if x]
    return selector_list


def pick_up_selector_from_html(html_str, selector_list):
    str_list = re.findall(r'<([^>/ ]*?)[ >]|id="(.+?)"|class="(.+?)"', html_str)
    remove_tag = ['link', 'html', 'head', 'meta', 'title']
    for s_str in str_list:
        s_list = []
        if s_str[0]:
            if '!' not in s_str[0] and s_str[0] not in remove_tag:
                s_list = [s_str[0]]
        elif s_str[1]:
            if ' ' in s_str[1]:
                s_list = ['#' + x for x in s_str[1].split() if x != '' or x != ' ']
            else:
                s_list = ['#' + s_str[1]]
        elif s_str[2]:
            if ' ' in s_str[2]:
                s_list = ['.' + x for x in s_str[2].split() if x != '' or x != ' ']
            else:
                s_list = ['.' + s_str[2]]
        for selector in s_list:
            if selector not in selector_list and selector not in put_after_tag:
                selector_list.append(selector)
    return selector_list


def pick_up_selector_from_js(html_str, selector_list):
    js_str_list = re.findall(r'<script.+?</script>', html_str)
    if js_str_list:
        for js_str in js_str_list:
            add_str_l = re.findall(r'classList\.add\(\'(.+?)\'\)|classList\.add\("(.+?)"\)|'
                                   r'classList\.remove\(\'(.+?)\'\)|classList\.remove\("(.+?)"\)', js_str)
            if add_str_l:
                for add_str in add_str_l:
                    if add_str:
                        for add_s in add_str:
                            if add_s and '.' + add_s not in selector_list:
                                selector_list.append('.' + add_s)
    return selector_list


def tab_and_line_feed_remove_from_str(long_str):
    str_list = long_str.splitlines()
    result = ''
    for x in str_list:
        y = x.strip()
        result += y
    result = result.replace('spanclass', 'span class')
    result = result.replace('spanid', 'span id')
    result = result.replace('"alt=', '" alt=')
    result = result.replace('"itemtype', '" itemtype')
    result = result.replace('"datetime=', '" datetime=')
    result = result.replace('imgsrc', 'img src')
    result = result.replace('spanitemprop', 'span itemprop')
    result = result.replace('spanclass', 'span class')
    result = result.replace('ahref', 'a href')
    result = result.replace('timeitemprop', 'time itemprop')
    result = result.replace('description"content="', 'description" content="')
    result = result.replace('"width="', '" width="')
    result = result.replace('"media="', '" media="')
    result = result.replace('"src', '" src')
    result = result.replace('"itemscope=', '" itemscope=')
    result = result.replace('"itemprop=', '" itemprop=')
    result = result.replace('imgitemprop=', 'img itemprop=')
    result = result.replace('"layout=', '" layout=')
    result = result.replace('"class=', '" class=')
    result = result.replace('"height="', '" height="')
    result = result.replace('"id="', '" id="')
    result = result.replace('"id="', '" id="')
    result = result.replace('"onclick="', '" onclick="')
    result = result.replace('"id="', '" id="')
    result = result.replace('"target="', '" target="')
    result = result.replace('blockquotecite', 'blockquote cite')
    result = result.replace('<br/>', '<br>')
    result = result.replace(', ', ',')
    result = css_minify(result)
    return result


def css_minify(long_str):
    css_str_l = re.findall(r'<style.*?>(.+?)</style>', long_str)
    if css_str_l:
        for css_str in css_str_l:
            css_str_r = css_str.replace(': ', ':')
            css_str_r = css_str_r.replace(' {', '{')
            long_str = long_str.replace(css_str, css_str_r)
    return long_str


def move_space_and_indention_from_css(css_str):
    css_str = css_str.replace('\n', '').replace('\t', '').replace('    ', '').replace(', ', ',').replace('} ', '}'). \
        replace(' {', '{').replace('/* ', '/*').replace(' */', '*/')
    return css_str


if __name__ == '__main__':
    # duplicate_class_checker('new/css/style26.css', ['new/company/fryer.html'],
    #                         'new/test/test7.css')
    duplicated_css_remove('template_files/css/main.css')
