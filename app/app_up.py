from ftplib import FTP


def ftp_upload(up_file_name, remote_dir):
    """
    FTPでファイルをアップロード,ベースはドメイン直下
    :param up_file_name: アップロードするファイル名
    :param remote_dir: アップロードするディレクトリ
    :return: none
    """
    if remote_dir:
        up_dir_and_file = str(remote_dir) + '/' + str(up_file_name)
    else:
        up_dir_and_file = up_file_name
    with FTP('blackrhino1.sakura.ne.jp', passwd='k2u5n47ku6') as ftp:
        ftp.login(user='blackrhino1', passwd='k2u5n47ku6')
        ftp.cwd('www/reibun')
        with open(str(up_file_name), 'rb') as fp:
            ftp.storbinary("STOR " + up_dir_and_file, fp)
        print('upload: ' + str(up_file_name))
        ftp.close()
    return


def app_upload():
    upload_list = ['index.html', 'app13.css', 'main_v10151323.js', 'manifest.json', 'offline.html', 'service-worker.js']
    for up_file in upload_list:
        ftp_upload(up_file, 'app')


def test_upload():
    upload_list = ['index.html', 'app13.css', 'main_v10151323.js', 'manifest.json', 'offline.html', 'service-worker.js']
    for up_file in upload_list:
        ftp_upload(up_file, 'test_app')


# 以下実行
#app_upload()
test_upload()
