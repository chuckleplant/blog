# Author: Sergio Basurco
#
# This script creates thumbnails for a set of image file extensions. It grabs all images recursively from
# photo_path and places the thumbnails at photo_path/thumbnails.

import os, sys
import PIL
from PIL import Image
from PIL import ExifTags



cur_path = os.path.dirname(os.path.realpath(__file__))
photo_path = os.path.join(cur_path,"../images/photography")
thumbnail_path = os.path.join(photo_path,"thumbnails")
extensions = ['jpg', 'JPG', 'JPEG', 'png', 'PNG', 'jpeg']
target_width = 500


for folder, subs, files in os.walk(photo_path):
    for filename in files:
        abs_file = os.path.join(folder,filename)
        if "thumbnails" not in abs_file:
            name,ext = os.path.splitext(abs_file)
            if any(filename.endswith(ext) for ext in extensions):
                comn_path = os.path.commonprefix([photo_path, abs_file])
                target_path = thumbnail_path + abs_file.replace(comn_path, "")
                img = Image.open(abs_file)
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
   