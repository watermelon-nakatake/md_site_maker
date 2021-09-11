import glob
import re


def make_redirect_htaccess_file(project_dir):
    result = []
    old_files = [x.replace(project_dir + '/old_files/', '').replace('index.html', '') for x in
                 glob.glob(project_dir + '/old_files/**/**.html', recursive=True)]
    print(old_files)
    new_md = {}
    md_files = [x.replace(project_dir + '/md_files/', '') for x in
                glob.glob(project_dir + '/md_files/**/**.md', recursive=True)]
    for md_path in md_files:
        if 'object/' in md_path:
            new_name = md_path.replace('object/', 'object-').replace('_dt', '')
        else:
            new_name = re.sub(r'^.+?/', '', md_path)
        new_name = new_name.replace('_', '-').replace('.md', '/')
        # print(new_name)
        new_md[new_name] = md_path
    for md_new in new_md:
        # print(md_new)
        if md_new in old_files:
            ht_str = 'RewriteRule ^{}$ https://www.goodbyedt.com/{} [R=301,L]'.format(md_new,
                                                                                      new_md[md_new].replace('.md',
                                                                                                             '.html'))
            # print(ht_str)
            result.append(ht_str)
    cat = list(set([re.sub(r'/.*$', '', x) for x in md_files]))
    cat_s = ['RewriteRule ^{}/$ https://www.goodbyedt.com/{}/ [R=301,L]'.format(x, x) for x in cat]
    result.extend(cat_s)
    result.sort()
    r_str = '\n'.join(result)
    print(r_str)

    # print(md_files)


if __name__ == '__main__':
    make_redirect_htaccess_file('goodbyedt')
