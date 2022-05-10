import glob
import os

from PIL import Image


def all_img_to_webp(img_dir, new_width, new_height, new_dir):
    img_files = glob.glob(img_dir + '/**')
    print(img_files)
    for img_path in img_files:
        if '.jpeg' in img_path or '.jpg' in img_path or '.png' in img_path:
            im = Image.open(img_path)
            width, height = im.size
            webp_path = img_path.replace('.jpg', '.webp').replace('.jpeg', '.webp').replace('.png', '.webp')
            if new_dir:
                webp_path = webp_path.replace(new_dir[0], new_dir[1])
            if not new_width and not new_height:
                im.save(webp_path, 'webp')
            else:
                if not new_height:
                    new_height = round(height * new_width / width)
                elif not new_width:
                    new_width = round(width * new_height / height)
                im_resize = im.resize((new_width, new_height), Image.LANCZOS)
                im_resize.save(webp_path, 'webp')


def all_png_resize(img_dir, new_width, new_height):
    img_files = glob.glob(img_dir + '/**.png')
    print(img_files)
    for img_path in img_files:
        im = Image.open(img_path)
        width, height = im.size
        if not new_height:
            new_height = round(height * new_width / width)
        elif not new_width:
            new_width = round(width * new_height / height)
        im_resize = im.resize((new_width, new_height), Image.LANCZOS)
        im_resize.save(img_path)


if __name__ == '__main__':
    os.chdir('../')
    all_img_to_webp('reibun/html_files/pc/images/art_images', 0, 0, ['/art_images/', '/webp/'])
    # all_png_resize('/Users/tnakatake/Downloads/star/convert2', 150, 0)
