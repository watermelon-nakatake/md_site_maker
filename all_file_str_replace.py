import re
import glob
import reibun_upload


def main(replace_str_list, if_replace_str_list):
    """
    置換リストにある文字列の置換を行いアップロードまで実行
    :param replace_str_list: [[置換前の文字列, 置換後の文字列], [..., ...], ...] main_file/pc or amp直下のファイルの表記で
    :param if_replace_str_list: 条件付きの置換文字列のリスト（これがなければ置換する）
    :return: none
    """
    files_dict = pick_up_all_html('reibun/pc')
    change_list = []
    for files_name in files_dict:
        if files_name == 't2':
            replace_list = [[re.sub(r'href="(.+?)"', r'href="../\1"', x[0]),
                             re.sub(r'href="(.+?)"', r'href="../\1"', x[1])] for x in replace_str_list]
            replace_list = [[re.sub(r'src="(.+?)"', r'src="../\1"', x[0]),
                             re.sub(r'src="(.+?)"', r'src="../\1"', x[1])] for x in replace_list]
            if_replace_list = [[re.sub(r'href="(.+?)"', r'href="../\1"', x[0]),
                                re.sub(r'href="(.+?)"', r'href="../\1"', x[1]),
                                re.sub(r'href="(.+?)"', r'href="../\1"', x[2])] for x in if_replace_str_list]
            if_replace_list = [[re.sub(r'src="(.+?)"', r'src="../\1"', x[0]),
                                re.sub(r'src="(.+?)"', r'src="../\1"', x[1]),
                                re.sub(r'src="(.+?)"', r'src="../\1"', x[2])] for x in if_replace_list]
        elif files_name == 't3':
            replace_list = [[re.sub(r'href="(.+?)"', r'href="../../\1"', x[0]),
                             re.sub(r'href="(.+?)"', r'href="../../\1"', x[1])] for x in replace_str_list]
            replace_list = [[re.sub(r'src="(.+?)"', r'src="../../\1"', x[0]),
                             re.sub(r'src="(.+?)"', r'src="../../\1"', x[1])] for x in replace_list]
            if_replace_list = [[re.sub(r'href="(.+?)"', r'href="../../\1"', x[0]),
                                re.sub(r'href="(.+?)"', r'href="../../\1"', x[1]),
                                re.sub(r'href="(.+?)"', r'href="../../\1"', x[2])] for x in if_replace_str_list]
            if_replace_list = [[re.sub(r'src="(.+?)"', r'src="../../\1"', x[0]),
                                re.sub(r'src="(.+?)"', r'src="../../\1"', x[1]),
                                re.sub(r'src="(.+?)"', r'src="../../\1"', x[2])] for x in if_replace_list]
        elif files_name == 't0':
            replace_list = [[re.sub(r'href="(.+?)"', r'href="pc/\1"', z) for z in x] for x in replace_str_list]
            replace_list = [[re.sub(r'src="(.+?)"', r'src="pc/\1"', z) for z in x] for x in replace_list]
            if_replace_list = [[re.sub(r'href="(.+?)"', r'href="pc/\1"', z) for z in x] for x in if_replace_str_list]
            if_replace_list = [[re.sub(r'src="(.+?)"', r'src="pc/\1"', z) for z in x] for x in if_replace_list]
        else:
            replace_list = replace_str_list
            if_replace_list = if_replace_str_list
        for file_path in files_dict[files_name]:
            with open(file_path, 'r', encoding='utf-8') as f:
                base_str = f.read()
                long_str = base_str
                long_str = reibun_upload.tab_and_line_feed_remove_from_str(long_str)
                for re_str in replace_list:
                    long_str = re.sub(re_str[0], re_str[1], long_str)
                for if_re_str in if_replace_list:
                    if if_re_str[0] not in long_str:
                        long_str = re.sub(if_re_str[1], if_re_str[2], long_str)
                if base_str != long_str:
                    with open(file_path, 'w', encoding='utf-8') as g:
                        g.write(long_str)
                    change_list.append(file_path)
    up_list = [y for y in change_list if '/delete/' not in y and '_test' not in y and '_copy' not in y
               and '/template/' not in y]
    print(up_list)
    # reibun_upload.scp_upload(up_list)


def pick_up_all_html(dir_path):
    """
    dir_pathにあるhtmlファイルを階層ごとに抽出
    :param dir_path: 大元のディレクトリ
    :return: 階層ごとのファイルパスの辞書
    """
    files_dict = {'t0': ['reibun/index.html'],
                  't1': glob.glob(dir_path + '/*.html', recursive=True),
                  't2': glob.glob(dir_path + '/*/*.html', recursive=True),
                  't3': glob.glob(dir_path + '/*/*/*.html', recursive=True)}
    return files_dict


if __name__ == '__main__':
    re_list = [['<div class="center">[<img class="app_bn1" src="../images/common/app_bn_f.png" alt="出会い系メール例文アプリ">](../../../reibun/app/)',
                '<div class="center">[<img class="app_bn1" src="../images/common/app_bn_f.png" alt="出会い系メール例文アプリ">](../../../reibun/app/)']]
    if_re_list = []
    main(re_list, if_re_list)
