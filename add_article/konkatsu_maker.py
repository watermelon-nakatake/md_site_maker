import new_from_md
import konkatsu.main_info
# import make_new_article


if __name__ == '__main__':
    # make_new_article.make_md_by_project_and_part('online_marriage', [], '', 0)
    new_from_md.main(1, konkatsu.main_info.info_dict, mod_date_flag=True, last_mod_flag=True, upload_flag=True,
                     first_time_flag=False, fixed_mod_date='')
    """
    新規markdownファイルやファイル更新でサイト全体とアップデートしてアップロード
    :param site_shift: サイトの表示に関するフラグ
    :param pd: projectのデータ
    :param mod_date_flag: mod_dateを更新するかのフラグ
    :param last_mod_flag: last_modを更新するか否か
    :param upload_flag: アップロードするか否か
    :param first_time_flag: 初回作成か否か
    :return: none
    """
