import article_modify
import htaiken.main_info


if __name__ == '__main__':
    target_dir = 'htaiken'
    pd_dict = htaiken.main_info.info_dict
    article_modify.all_file_to_markdown(before_dir=target_dir + '/old_files', after_dir=target_dir + '/md_files',
                                        pd=pd_dict, path_remove='', remove_list=[])
