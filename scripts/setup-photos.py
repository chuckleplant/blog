import glob, os, sys, yaml
from PIL import Image, ExifTags
import math
import piexif

cur_path = os.path.dirname(os.path.realpath(__file__))
yaml_path = os.path.join(cur_path, '../_data/photos')

def get_yaml_path(album_name):
    return os.path.join(yaml_path, album_name) + '.yaml'

def generate_yaml(album_name, album_path):
    print 'Generating YAML'
    photos_in_album = []
    for file in sorted(glob.glob(album_path+'/*')):
        im = Image.open(file)
        width,height = im.size
        photo_aspect = float(width)/float(height)

        photo_title = os.path.basename(file)
        photo_img = album_name + '/' + photo_title
        photo_album = album_name
        photo_obj_yaml = dict(
            title = os.path.splitext(os.path.basename(photo_title))[0],
            img = photo_img,
            album = photo_album,
            aspect = photo_aspect
        )
        photos_in_album.append(photo_obj_yaml)
    photo_yaml = dict(
        photos = photos_in_album
    )
    with open(get_yaml_path(album_name), 'w') as outfile:
        yaml.dump(photo_yaml, outfile, default_flow_style=False)

def generate_yaml_for_album(album_path):
    images = []
    types = ('*.jpg', '*.png', '*.jpeg', '*.JPG', '*.JPEG')
    for extension in types:
        images.extend(glob.glob(os.path.join(album_path, extension)))
    if len(images) == 0:
        print 'No images in album , ' + album_path
        return
    elif "thumbnails" in album_path:
        print 'not this one'
        return
    album_name = os.path.basename(os.path.normpath(album_path))
    types = ('*.jpg', '*.png', '*.jpeg', '*.JPG', '*.JPEG')
    generate_yaml(album_name, album_path)

def res_for_pix_count(width, height, pixcount):
    aspect = float(width) / float(height)
    h = math.sqrt(float(pixcount) / aspect)
    w = aspect * h
    return int(w), int(h)


def res_for_height(width, height, desired_height):
    aspect = float(width)/float(height)
    new_width = aspect * desired_height
    return int(new_width), desired_height

def gen_thumb_size(img, thumbheight, thumbdir, fname):
    tw, th = res_for_height(img.width, img.height, thumbheight)
    img.thumbnail((tw,th), Image.ANTIALIAS)
    target_dir = os.path.join(thumbnail_path, str(thumbheight))
    target_file = os.path.join(target_dir, fname)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    img.save(target_file)


albums = glob.glob(cur_path+'/../images/photography/*/')
for album_path in albums:
    generate_yaml_for_album(album_path)

max_pix_count = 3000000
photo_path = os.path.join(cur_path,"../img/albums")
thumbnail_path = os.path.join(cur_path,"../img")
#thumbnail_path = os.path.join(photo_path,"thumbnails")
extensions = ['jpg', 'JPG', 'JPEG', 'png', 'PNG', 'jpeg']
target_width = 420


for folder, subs, files in os.walk(photo_path):
    for filename in files:
        abs_file = os.path.join(folder,filename)
        name,ext = os.path.splitext(abs_file)
        if any(filename.endswith(ext) for ext in extensions):       
            comn_path = os.path.commonprefix([photo_path, abs_file])
            target_path = thumbnail_path + abs_file.replace(comn_path, "")
            img = Image.open(abs_file)

            touched = False

            exif_dict = piexif.load(abs_file)
            exif_bytes = piexif.dump(exif_dict)
            if piexif.ImageIFD.Orientation in exif_dict["0th"]:    
                touched = True
                orientation = exif_dict["0th"].pop(piexif.ImageIFD.Orientation)
                exif_bytes = piexif.dump(exif_dict)
                if orientation == 2:
                    img = img.transpose(Image.FLIP_LEFT_RIGHT)
                elif orientation == 3:
                    img = img.rotate(180)
                elif orientation == 4:
                    img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
                elif orientation == 5:
                    img = img.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
                elif orientation == 6:
                    img = img.rotate(-90, expand=True)
                elif orientation == 7:
                    img = img.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
                elif orientation == 8:
                    img = img.rotate(90, expand=True)

            width, height = img.size
            numpix = width * height
            if numpix > max_pix_count:
                w, h = res_for_pix_count(width, height, max_pix_count)
                img.thumbnail((w,h), Image.ANTIALIAS)
                print 'Resized %s' % filename
                touched = True

            if touched:
                img.save(abs_file, exif=exif_bytes)
            # https://coderwall.com/p/nax6gg/fix-jpeg-s-unexpectedly-rotating-when-saved-with-pil

            gen_thumb_size(img, 200, thumbnail_path, filename)
            gen_thumb_size(img, 20, thumbnail_path, filename)