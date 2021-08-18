import upload.file_upload
import reibun.main_info
import sfd.main_info
import joshideai.main_info
import rei_site.main_info
import konkatsu.main_info


def reibun_mint_changer(new_url):
    h_str = 'RewriteEngine On\nRewriteRule ^(.*)$ {} [R,L]\nOrder allow,deny\nAllow from all\n'.format(new_url)
    ht_list = ['reibun/html_files/pc/ds/mintj/.htaccess', 'reibun/html_files/amp/ds/mintj/.htaccess',
               'reibun/html_files/app/dsite/mintj/.htaccess']
    for ht_path in ht_list:
        with open(ht_path, 'w', encoding='utf-8') as f:
            f.write(h_str)
    upload.file_upload.scp_upload(ht_list, reibun.main_info.info_dict)


def sf_mint_changer(new_url):
    h_str = 'RewriteEngine On\nRewriteRule ^(.*)$ {} [R,L]\nOrder allow,deny\nAllow from all\n'.format(new_url)
    ht_list = ['sfd/html_files/url/mintj/.htaccess']
    for ht_path in ht_list:
        with open(ht_path, 'w', encoding='utf-8') as f:
            f.write(h_str)
    upload.file_upload.scp_upload(ht_list, sfd.main_info.info_dict)


def ht_changer(project_name, af_site, new_url):
    h_str = 'RewriteEngine On\nRewriteRule ^(.*)$ {} [R,L]\nOrder allow,deny\nAllow from all\n'.format(new_url)
    ht_list_dict = {'reibun': ['reibun/html_files/pc/ds/{}/.htaccess', 'reibun/html_files/amp/ds/{}/.htaccess',
                               'reibun/html_files/app/dsite/{}/.htaccess'],
                    'sfd': ['sfd/html_files/url/{}/.htaccess'],
                    'joshideai': ['joshideai/html_files/site_page/pcmax/.htaccess'],
                    'rei_site': ['rei_site/html_files/pc/site_data/pcmax/.htaccess'],
                    'konkatsu': ['konkatsu/html_files/link/pcmax/.htaccess']}
    pd_dict = {'reibun': reibun.main_info.info_dict, 'sfd': sfd.main_info.info_dict,
               'joshideai': joshideai.main_info.info_dict, 'rei_site': rei_site.main_info.info_dict,
               'konkatsu': konkatsu.main_info.info_dict}
    if project_name == 'all':
        for pj_name in ht_list_dict:
            ht_list = [x.format(af_site) for x in ht_list_dict[pj_name]]
            for ht_path in ht_list:
                with open(ht_path, 'w', encoding='utf-8') as f:
                    f.write(h_str)
            upload.file_upload.scp_upload(ht_list, pd_dict[pj_name])
    else:
        ht_list = [x.format(af_site) for x in ht_list_dict[project_name]]
        for ht_path in ht_list:
            with open(ht_path, 'w', encoding='utf-8') as g:
                g.write(h_str)
        upload.file_upload.scp_upload(ht_list, pd_dict[project_name])


if __name__ == '__main__':
    # reibun_mint_changer('https://track.bannerbridge.net/click.php?APID=169174&affID=50161&siteID=110769')
    # sf_mint_changer('https://track.bannerbridge.net/click.php?APID=169188&affID=50161&siteID=200322')

    ht_changer('all', 'pcmax', 'https://pcmax.jp/lp/?ad_id=rm138751')
