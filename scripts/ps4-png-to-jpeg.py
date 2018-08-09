# PS4 screenshots are saved as PNG files, we need JPEGs and we also need to maintain order
# for some reason PS4 images have the same creation date. So they're sorted by title alone.
# I want them sorted by the date of picture taken.
# last 14 characters are date of pic

import os
import glob
import argparse
import json
from datetime import datetime
import time
from bisect import bisect_left, bisect_right
from PIL import Image
from pexif import JpegFile
import piexif
import pprint


parser = argparse.ArgumentParser()
parser.add_argument('-d','--dir', help='Images folder.', required=True)
args = vars(parser.parse_args())
image_dir = args['dir']

png_files = glob.glob(os.path.join(image_dir, '*.png'))
for png_file in png_files:
    filename = os.path.splitext(os.path.basename(png_file))[0]
    datestring = filename[-14:]
    timestamp = datetime.strptime(datestring,'%Y%m%d%H%M%S')
    jpg_filename = os.path.join(image_dir,'converted',filename+'.jpg')
    png_img = Image.open(png_file)
    width,height = png_img.size

    exif_dict = {   '0th': {   }, '1st': {   }, 'Exif': {   }, 'GPS': {   }, 'Interop': {   }, 'thumbnail': None}
    exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = timestamp.strftime('%Y:%m:%d %H:%M:%S')
    exif_dict["0th"][piexif.ImageIFD.Model] = 'Playstation(R)4'
    exif_dict["Exif"][piexif.ExifIFD.PixelXDimension] = width
    exif_dict["Exif"][piexif.ExifIFD.PixelYDimension] = height
    exif_bytes = piexif.dump(exif_dict)

    rgb_img = png_img.convert('RGB')
    rgb_img.save(jpg_filename, exif=exif_bytes)