import glob

import new_from_md


def main(project_dir):
    md_list = glob.glob(project_dir + '/**/**.md', recursive=True)
    print(md_list)


if __name__ == '__main__':
    main('sfd')


