#
# Geotagging using Google location history.
#
# Input parameters:
# 
#   -j JSON, --json JSON  The JSON file containing your location history.
#   -d DIR, --dir DIR     Images folder.
#   -t TIME, --time TIME  Hours of tolerance.

import os
import glob
import argparse
import json
import datetime
import time
from bisect import bisect_left, bisect_right
from PIL import Image
from pexif import JpegFile
import math

class Location(object):
    def __init__(self, d={}):
        for key in d:
            if key == 'timestampMs':
                self.timestamp = int(d[key]) / 1000
            elif key == 'latitudeE7':
                self.latitude = d[key]
            elif key == 'longitudeE7':
                self.longitude = d[key]

    def __eq__( self, other ):
        return self.timestamp == other.timestamp
    def __lt__( self, other ):
        return self.timestamp < other.timestamp
    def __le__( self, other ):
        return self.timestamp <= other.timestamp
    def __gt__( self, other ):
        return self.timestamp > other.timestamp
    def __ge__( self, other ):
        return self.timestamp >= other.timestamp
    def __ne__( self, other ):
        return self.timestamp != other.timestamp

def find_closest_in_time(locations, a_location):
    pos = bisect_left(locations, a_location)
    if pos == 0:
        return locations[0]
    if pos == len(locations):
        return locations[-1]
    
    before = locations[pos - 1]
    after = locations[pos]
    if after.timestamp - a_location.timestamp < a_location.timestamp - before.timestamp:
       return after
    else:
       return before

def res_for_pix_count(width, height, pixcount):
    aspect = float(width) / float(height)
    h = math.sqrt(float(pixcount) / aspect)
    w = aspect * h
    return int(w), int(h)

parser = argparse.ArgumentParser()
parser.add_argument('-d','--dir', help='Images folder.', required=True)
args = vars(parser.parse_args())
image_dir = args['dir']

max_pix_count = 2500000

included_extenstions = ['jpg', 'JPG', 'jpeg', 'JPEG']
file_names = [fn for fn in os.listdir(image_dir) if any(fn.endswith(ext) for ext in included_extenstions)]

for image_file in file_names:
    image_file = os.path.join(image_dir, image_file)
    image = Image.open(image_file)
    exif = image.info['exif']

    width, height = image.size
    numpix = width * height

    if numpix > max_pix_count:
        w, h = res_for_pix_count(width, height, max_pix_count)
        image.thumbnail((w,h), Image.ANTIALIAS)
        image.save(image_file, exif=exif)
        print 'saved %s' % image_file
    
