import os
import re
import glob
from upload import file_upload


def main(replace_str_list, sub_str_list, if_replace_str_list, project_dir):
    """
    置換リストにある文字列の置換を行いアップロードまで実行
    :param replace_str_list: [[置換前の文字列, 置換後の文字列], [..., ...], ...] main_file/pc or amp直下のファイルの表記で
    :param if_replace_str_list: 条件付きの置換文字列のリスト（これがなければ置換する）
    :param project_dir: 対象のプロジェクト
    :return: none
    """
    files_dict = pick_up_all_html(project_dir)
    # print(files_dict)
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
                if '<!--GTM-->' not in base_str:
                    long_str = base_str
                    long_str = file_upload.tab_and_line_feed_remove_from_str(long_str)
                    for re_str in replace_list:
                        # print(re_str[0])
                        # print(re_str[1])
                        long_str = long_str.replace(re_str[0], re_str[1])
                    for sub_str in sub_str_list:
                        long_str = re.sub(sub_str[0], sub_str[1], long_str)
                    for if_re_str in if_replace_list:
                        if if_re_str[0] not in long_str:
                            long_str = re.sub(if_re_str[1], if_re_str[2], long_str)
                    if base_str != long_str:
                        print(file_path)
                        # print(long_str)
                        with open(file_path, 'w', encoding='utf-8') as g:
                            g.write(long_str)
                        change_list.append(file_path)
    up_list = [y for y in change_list if '/delete/' not in y and '_test' not in y and '_copy' not in y
               and '/template/' not in y]
    print(up_list)
    # file_upload.auto_scp_upload(up_list)


def pick_up_all_html(project_dir):
    """
    dir_pathにあるhtmlファイルを階層ごとに抽出
    :param project_dir: 大元のディレクトリ
    :return: 階層ごとのファイルパスの辞書
    """
    if project_dir == 'reibun':
        main_dir = '/pc'
    else:
        main_dir = ''
    files_dict = {'t0': [project_dir + '/html_files/index.html'],
                  't1': glob.glob(project_dir + '/html_files' + main_dir + '/*.html', recursive=True),
                  't2': glob.glob(project_dir + '/html_files' + main_dir + '/*/*.html', recursive=True),
                  't3': glob.glob(project_dir + '/html_files' + main_dir + '/*/*/*.html', recursive=True)}
    return files_dict


if __name__ == '__main__':
    os.chdir('../')
    print(os.getcwd())
    pj_dir = 'reibun'
    re_list = [['requestAnimationFrame(loop)}})})})</script>',
                'requestAnimationFrame(loop)}})})});function lazyAnalyticsScript(){let scrollFirstTime=1;window.addEventListener("scroll",oneTimeFunction,false);window.addEventListener("mousemove",oneTimeFunction,false);function oneTimeFunction(){if(scrollFirstTime===1){scrollFirstTime=0;let adScript=document.createElement("script");adScript.src=\'https://www.googletagmanager.com/gtag/js?id=UA-15766143-9\';document.body.appendChild(adScript);let adScript2=document.createElement("script");adScript2.innerHTML=\'window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","UA-15766143-9");\';document.body.appendChild(adScript2);window.removeEventListener("scroll",oneTimeFunction,false);window.removeEventListener("mousemove",oneTimeFunction,false);}}}lazyAnalyticsScript();</script>'],
               ['rg/WebPage"><div id="header"',
                'rg/WebPage"><!--GTM(noscript)--><noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-PR45XTQ" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript><!--End GTM(noscript)--><div id="header"'],
               ['<div id="navop"><div id="gnav">', '<div id="gnav">'],
               ['</ul></div></div><div class="hd_m" id="m_button">',
                '</ul></div><div class="hd_m" id="m_button">'],
               ['/sitepage/ranking.html" class="hd_m"', '/sitepage/ranking.html" class="hd_rank_link"'],
               ["'event_label':'rank-topil'})", "'event_label':'hd-rank-link'})"],
               ['<div class="efooter mobnone"><div class="eft3"><div class="eft2"><span class="eft1">',
                '<div class="efooter mobnone"><div class="eft">'],
               ['</span></span></a></span><span class="eft1"><span class="imgnon" itemprop="publisher"',
                '</span></span></a><span class="no_dis" itemprop="publisher"'],
               ['"></span></span></div></div><div id="bread"',
                '" loading="lazy" class="no_dis"></div><div id="bread"'],
               ['<span itemprop="logo" itemscope="itemscope" itemtype="https://schema.org/ImageObject"><span itemprop="url">https://www.demr.jp/pc/images/logo2.png</span></span></span><span class="imgnon"><img ',
                '<span itemprop="logo" itemscope="itemscope" itemtype="https://schema.org/ImageObject"><span itemprop="url">https://www.demr.jp/pc/images/common/site_name_400.png</span></span></span><img '],
               ['<span itemprop="logo" itemscope="itemscope" itemtype="https://schema.org/ImageObject"><span itemprop="url">https://www.demr.jp/pc/images/common/site_name_400.png</span></span></span><span class="imgnon"><img ',
                   '<span itemprop="logo" itemscope="itemscope" itemtype="https://schema.org/ImageObject"><span itemprop="url">https://www.demr.jp/pc/images/common/site_name_400.png</span></span></span><img '],
               ['</ul></div></div></div><div id="footer"><div id="f_wrap"><div id="fnav"><div class="fnav_i ud">MENU</div><ul><li class="fnav00"><a href="../../">TOPページ</a></li><li class="fnav01"><a href="../majime/kakikata_p.html">プロフィール例文</a></li><li class="fnav02"><a href="../majime/kakikata_t.html">掲示板書き込み例文</a></li><li class="fnav03"><a href="../majime/kakikata_f.html">ファーストメール</a></li><li class="fnav04"><a href="../majime/majime.html">２通目以降の例文</a></li><li class="fnav05"><a href="../majime/date.html">デートに誘うメール例文</a></li><li class="fnav06"><a href="../majime/kakikata_d.html">出会い系攻略法</a></li><li class="fnav07"><a href="../site/">サイト情報と攻略法</a></li><li class="fnav08"><a href="../caption/">出会いの予備知識</a></li><li class="fnav09"><a href="../qa/">出会い系Q＆A</a></li></ul></div><div class="snsb"><div class="snsb1"><a href="../../atom.xml"><img src="../images/rss_004_c-trans.png" width="24" height="24" alt="RSS購読する"></a></div></div></div><div id="pnav"><ul><li><a href="../policy/">サイトポリシー</a></li><li class="mobnone"><a href="../policy/sitemap.html">サイトマップ</a></li><li class="mobnone"><a href="../policy/log.html">更新履歴</a></li><li class="mobnone"><a href="../mailform/mail.html">お問い合わせ</a></li></ul></div><div id="footer2">出会い系サイトは18禁です。<br/>18歳未満の方は出会い系サイトの利用及び当サイトの閲覧が一切禁止されています。</div><div id="footer1">&copy; 出会い系メール例文集 2009-<span id="cp_year"></span></div></div>',
                '</ul></div><div class="leftnav s_line"><div class="sbh">MENU</div><ul><li class="fnav00"><a href="../../">TOPページ</a></li><li><a href="../majime/">出会い系メール例文</a></li><li><a href="../../app/">出会い系メール作成アプリ</a></li><li><a href="../majime/kakikata_p.html">プロフィール例文</a></li><li><a href="../majime/kakikata_t.html">出会い系掲示板投稿例文</a></li><li><a href="../majime/kakikata_f.html">ファーストメール例文</a></li><li><a href="../majime/majime.html">２通目以降のメール例文</a></li><li><a href="../majime/date.html">デートに誘うメール例文</a></li><li><a href="../majime/kakikata_d.html">出会いの方法とコツ</a></li><li><a href="../site/">サイト情報と攻略法</a></li><li><a href="../caption/">出会いの予備知識</a></li><li><a href="../qa/">出会い系Q＆A</a></li><li><a href="../policy/">サイトポリシー</a></li></ul></div></aside></div><div id="footer"><div id="footer2">出会い系サイトは18禁です。<br />18歳未満の方は出会い系サイトの利用及び当サイトの閲覧が一切禁止されています。</div><div id="footer1">&copy; 出会い系メール例文集 2009-<span id="cp_year"></span></div></div>'],
               ['<div id="con3"><main itemscope="itemscope" itemtype="http://schema.org/Article" itemprop="mainEntityOfPage">',
                '<main itemscope="itemscope" itemtype="http://schema.org/Article" itemprop="mainEntityOfPage" id="con3">'],
               ]
    sub_list = [[r'<!-- Global site tag \(gtag\.js\) -->.*?<!--e/gtag-->',
                "<!--GTM--><script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','GTM-PR45XTQ');</script><!--End GTM-->"],
                [r'<link rel="amphtml" href="https://www\.demr\.jp/amp.*?">',
                 ''],
                [r'<div class="leftnav s_line tabn"><div class="sbh">カテゴリー</div>.*?<div class="leftnav nkkj"><div class="sbh">重要記事</div>',
                 '<div class="leftnav nkkj"><div class="sbh">重要記事</div>']]
    if_re_list = []
    main(re_list, sub_list, if_re_list, pj_dir)
