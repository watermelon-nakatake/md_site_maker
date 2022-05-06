import new_from_md
import reibun.main_info


if __name__ == '__main__':
    # new_from_md.main(1, reibun.main_info.info_dict, mod_date_flag=True, last_mod_flag=True, upload_flag=True,
    #                  first_time_flag=False, fixed_mod_date=False)
    new_from_md.main(1, reibun.main_info.info_dict, mod_date_flag=False, last_mod_flag=True, upload_flag=True,
                     first_time_flag=True, fixed_mod_date=False)
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
