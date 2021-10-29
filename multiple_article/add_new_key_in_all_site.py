import check_site_data
import howto.main_info
import htaiken.main_info
import joshideai.main_info
import koibito.main_info
import konkatsu.main_info
import make_new_article
import new_from_md
import goodbyedt.main_info
import online_marriage.main_info
import rei_site.main_info
import shoshin.main_info
import women.main_info


def add_new_key_in_all_site_and_upload(target_key):
    code_dict = {'obj_m': 'only_obj - man', 'obj_w': 'only_obj - woman',
                 'sub_m': 'only_sub - man', 'sub_w': 'only_sub - woman',
                 'act': 'only_act - man', 'adj_act': 'mix_act - man'}
    info_dict = {'goodbyedt': goodbyedt.main_info.info_dict,
                 'howto': howto.main_info.info_dict,
                 'htaiken': htaiken.main_info.info_dict,
                 'joshideai': joshideai.main_info.info_dict,
                 'koibito': koibito.main_info.info_dict,
                 'konkatsu': konkatsu.main_info.info_dict,
                 'online_marriage': online_marriage.main_info.info_dict,
                 'rei_site': rei_site.main_info.info_dict,
                 'shoshin': shoshin.main_info.info_dict,
                 'women': women.main_info.info_dict}
    site_key_data = check_site_data.check_all_key_data()
    # print(site_key_data)
    add_site = {}
    for project_name in site_key_data:
        if project_name != 'sfd':
            if code_dict[target_key] in site_key_data[project_name]:
                if '- woman' in code_dict[target_key]:
                    add_site[project_name] = 'woman'
                else:
                    add_site[project_name] = 'man'
    print(add_site)
    for project_dir in add_site:
        main_info = info_dict[project_dir]
        make_new_article.make_md_by_project_and_part(project_dir, [], add_site[project_dir], 0, exist_update_flag=False)
        new_from_md.main(0, main_info.info_dict, mod_date_flag=True, last_mod_flag=True, upload_flag=True,
                         first_time_flag=False, fixed_mod_date='')


if __name__ == '__main__':
    add_new_key_in_all_site_and_upload('obj_m')
