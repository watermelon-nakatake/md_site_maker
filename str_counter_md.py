import re


def title_counter(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        long_str = f.read()
        title_l = re.findall(r'(t::.+?)\n', long_str)
        if title_l:
            title = title_l[0]
            title_len = len(title.replace('t::', ''))
            print('title : ' + str(title_len))
        des_l = re.findall(r'(d::.+?)\n', long_str)
        if des_l:
            des = des_l[0]
            des_len = len(des.replace('d::', ''))
            print('description : ' + str(des_len))
        main_l = re.findall(r'\n(# [\s\S]*)$', long_str)
        if main_l:
            main = main_l[0]
            main = re.sub(r'\n#* ', '\n', main)
            main = re.sub(r'\]\(.+?\)', ']', main)
            main = re.sub(r'%.+?%', '', main)
            main = re.sub(r'!\[.+?\]', '', main)
            main = re.sub(r'\[(.+?)\]', r'\1', main)
            main = re.sub(r'<.+?>', '', main)
            main = re.sub(r'\n- ', r'\n', main)
            main_len = len(main)
            print('main : ' + str(main_len))
            print('main(改行なし) : ' + str(len(main.replace('\n', ''))))


if __name__ == '__main__':
    title_counter('md_files/pc/majime/m1_9.md')
