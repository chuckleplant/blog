import glob, os, sys, yaml
import PIL
from PIL import ImageTk, Image, ExifTags
import math

cur_path = os.path.dirname(os.path.realpath(__file__))
yaml_path = os.path.join(cur_path, '../_data/photos')

def get_yaml_path(album_name):
    return os.path.join(yaml_path, album_name) + '.yaml'

def generate_yaml(album_name, album_path):
    print 'Generating YAML'
    photos_in_album = []
    for file in glob.glob(album_path+'/*'):
        photo_title = os.path.splitext(os.path.basename(file))[0]
        photo_img = album_name + '/' + photo_title
        photo_album = album_name
        photo_obj_yaml = dict(
            title = photo_title,
            img = photo_img,
            album = photo_album
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

albums = glob.glob(cur_path+'/../images/photography/*/')
for album_path in albums:
    generate_yaml_for_album(album_path)

max_pix_count = 3000000
photo_path = os.path.join(cur_path,"../images/photography")
thumbnail_path = os.path.join(photo_path,"thumbnails")
extensions = ['jpg', 'JPG', 'JPEG', 'png', 'PNG', 'jpeg']
target_width = 420


for folder, subs, files in os.walk(photo_path):
    for filename in files:
        abs_file = os.path.join(folder,filename)
        if "thumbnails" not in abs_file:
            name,ext = os.path.splitext(abs_file)
            if any(filename.endswith(ext) for ext in extensions):                

                comn_path = os.path.commonprefix([photo_path, abs_file])
                target_path = thumbnail_path + abs_file.replace(comn_path, "")
                img = Image.open(abs_file)
                exif = img.info['exif']
                width, height = img.size
                numpix = width * height
                if numpix > max_pix_count:
                    w, h = res_for_pix_count(width, height, max_pix_count)
                    img.thumbnail((w,h), Image.ANTIALIAS)
                    print 'Resized %s' % filename
                    img.save(abs_file, exif=exif)

                # https://coderwall.com/p/nax6gg/fix-jpeg-s-unexpectedly-rotating-when-saved-with-pil
                if hasattr(img, '_getexif'):
                    orientation = 0x0112
                    exif = img._getexif()
                    if exif is not None:
                        orientation = exif[orientation]
                        rotations = {
                        3: Image.ROTATE_180,
                        6: Image.ROTATE_270,
                        8: Image.ROTATE_90
                        }
                        if orientation in rotations:
                            img = img.transpose(rotations[orientation])

                img.thumbnail((target_width, target_width), PIL.Image.ANTIALIAS)
                target_dir = os.path.dirname(target_path)
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                img.save(target_path)