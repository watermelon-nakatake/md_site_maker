from goodbyedt import main_info
import new_from_md

if __name__ == '__main__':
    new_from_md.main(0, main_info.info_dict, mod_date_flag=True, last_mod_flag=True, upload_flag=False,
                     first_time_flag=True, fixed_mod_date='')
    # change_file_upload.search_update_file(joshideai.main_info.info_dict)
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
