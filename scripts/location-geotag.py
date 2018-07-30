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
import piexif
from fractions import Fraction


# Exif copyright data, modify it here and it'll be written to every picture
#
#

class Location(object):
    def __init__(self, d={}):
        self.timestamp = None
        self.latitude = None
        self.longitude = None
        self.altitude = 0

        for key in d:
            if key == 'timestampMs':
                self.timestamp = int(d[key]) / 1000
            elif key == 'latitudeE7':
                self.latitude = d[key]
            elif key == 'longitudeE7':
                self.longitude = d[key]
            elif key == 'altitude':
                self.altitude = d[key]

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


# https://gist.github.com/c060604/8a51f8999be12fc2be498e9ca56adc72

def to_deg(value, loc):
    """convert decimal coordinates into degrees, munutes and seconds tuple
    Keyword arguments: value is float gps-value, loc is direction list ["S", "N"] or ["W", "E"]
    return: tuple like (25, 13, 48.343 ,'N')
    """
    if value < 0:
        loc_value = loc[0]
    elif value > 0:
        loc_value = loc[1]
    else:
        loc_value = ""
    abs_value = abs(value)
    deg =  int(abs_value)
    t1 = (abs_value-deg)*60
    min = int(t1)
    sec = round((t1 - min)* 60, 5)
    return (deg, min, sec, loc_value)


def change_to_rational(number):
    """convert a number to rantional
    Keyword arguments: number
    return: tuple like (1, 2), (numerator, denominator)
    """
    f = Fraction(str(number))
    return (f.numerator, f.denominator)



parser = argparse.ArgumentParser()
parser.add_argument('-j','--json', help='The JSON file containing your location history.', required=True)
parser.add_argument('-d','--dir', help='Images folder.', required=True)
parser.add_argument('-t','--time', help='Hours of tolerance.', default=1, required=False)
args = vars(parser.parse_args())
locations_file = args['json']
image_dir = args['dir']
hours_threshold = int(args['time'])

print 'Loading data (takes a while)...'
with open(locations_file) as f:
    location_data = json.load(f)

location_array = location_data['locations']
print 'Found %s locations' % len(location_array)

my_locations = []
for location in location_array:
    a_location = Location(location)
    my_locations.append(a_location)

print 'Reversing locations list'
my_locations = list(reversed(my_locations))

included_extenstions = ['jpg', 'JPG', 'jpeg', 'JPEG']
file_names = [fn for fn in os.listdir(image_dir) if any(fn.endswith(ext) for ext in included_extenstions)]

for image_file in file_names:
    image_file = os.path.join(image_dir, image_file)
    image = Image.open(image_file)
    time_exif = image._getexif()[36867]
    time_jpeg_unix = time.mktime(datetime.datetime.strptime(time_exif, "%Y:%m:%d %H:%M:%S").timetuple())
    curr_loc = Location()
    curr_loc.timestamp = int(time_jpeg_unix)
    approx_location = find_closest_in_time(my_locations, curr_loc)
    hours_away = abs(approx_location.timestamp - time_jpeg_unix) / 3600

    if(hours_away < hours_threshold):
        lat_f = float(approx_location.latitude) / 10000000.0
        lon_f = float(approx_location.longitude) / 10000000.0
        
        exif_dict = piexif.load(image_file)        
        exif_dict["GPS"][piexif.GPSIFD.GPSVersionID] = (2, 0, 0, 0)
        exif_dict["GPS"][piexif.GPSIFD.GPSAltitudeRef] = 0 if approx_location.altitude > 0 else 1        
        exif_dict["GPS"][piexif.GPSIFD.GPSAltitude] = change_to_rational(abs(approx_location.altitude))
        exif_dict["GPS"][piexif.GPSIFD.GPSLatitudeRef] = 'S' if lat_f < 0 else 'N'
        exif_dict["GPS"][piexif.GPSIFD.GPSLongitudeRef] = 'W' if lon_f < 0 else 'E'

        lat_deg = to_deg(lat_f, ["S", "N"])
        lng_deg = to_deg(lon_f, ["W", "E"])
        exiv_lat = (change_to_rational(lat_deg[0]), change_to_rational(lat_deg[1]), change_to_rational(lat_deg[2]))
        exiv_lng = (change_to_rational(lng_deg[0]), change_to_rational(lng_deg[1]), change_to_rational(lng_deg[2]))
        exif_dict["GPS"][piexif.GPSIFD.GPSLatitude] = exiv_lat
        exif_dict["GPS"][piexif.GPSIFD.GPSLongitude] = exiv_lng
        
        exif_bytes = piexif.dump(exif_dict)
        image.save(image_file, exif=exif_bytes)
    else:
        print 'Time threshold surpassed'