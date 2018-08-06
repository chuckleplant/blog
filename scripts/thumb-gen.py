import glob, os, sys, yaml
from PIL import Image, ExifTags
import math
import piexif
import argparse

cur_path = os.path.dirname(os.path.realpath(__file__))

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
    #print 'would save to '+target_file
    img.save(target_file)


parser = argparse.ArgumentParser()
parser.add_argument('-d','--dir', help='Images folder.', required=True)
parser.add_argument('-o','--out', help='Output folder.', required=True)

args = vars(parser.parse_args())
photo_path = args['dir']
thumbnail_path = args['out']
extensions = ['jpg', 'JPG', 'JPEG', 'png', 'PNG', 'jpeg']

for folder, subs, files in os.walk(photo_path):
    for filename in files:
        abs_file = os.path.join(folder,filename)
        name,ext = os.path.splitext(abs_file)
        if any(filename.endswith(ext) for ext in extensions):
            target_path = thumbnail_path 
            img = Image.open(abs_file)
            exif_dict = piexif.load(abs_file)
            exif_bytes = piexif.dump(exif_dict)
            if piexif.ImageIFD.Orientation in exif_dict["0th"]:
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

            gen_thumb_size(img, 500, thumbnail_path, filename)
            gen_thumb_size(img, 20, thumbnail_path, filename)