from howto import main_info
import new_from_md
import make_new_article

if __name__ == '__main__':
    # make_new_article.make_md_by_project_and_part('howto', [], '', 0)
    new_from_md.main(0, main_info.info_dict, mod_date_flag=True, last_mod_flag=True, upload_flag=True,
                     first_time_flag=True, fixed_mod_date='')
    # change_file_upload.search_update_file(howto.main_info.info_dict)
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
