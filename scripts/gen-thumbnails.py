# The image resizing bit of this code is based on: https://opensource.com/life/15/2/resize-images-python
# This script is hence released with license Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
# Original author is: Dayo Ntwari
# This script was written by: Sergio Basurco
#
# This script creates thumbnails for a set of image file extensions. It grabs all images recursively from
# photo_path and places the thumbnails at photo_path/thumbnails.

import os, sys
import PIL
from PIL import Image

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
                wpercent = target_width / float(img.size[0])
                hsize = int((float(img.size[1]) * float(wpercent)))
                img = img.resize((target_width, hsize), PIL.Image.ANTIALIAS)
                target_dir = os.path.dirname(target_path)
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                img.save(target_path)
   