import article_modify
import online_marriage.main_info


if __name__ == '__main__':
    article_modify.all_file_to_markdown(before_dir='', after_dir='online_marriage/md_files',
                                        pd=online_marriage.main_info.info_dict, path_remove='', remove_list=[])
