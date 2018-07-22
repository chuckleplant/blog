import os
from subprocess import call
import argparse
import json
from pprint import pprint
import datetime
import time
import bisect
from bisect import bisect_left, bisect_right
from PIL import Image
from json import JSONEncoder
from pexif import JpegFile

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
    print 'Finding closest element'
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

parser = argparse.ArgumentParser()
parser.add_argument('-j','--json', help='The JSON file containing your location history.', required=True)
parser.add_argument('-p','--photo', help='The image file.', required=True)
args = vars(parser.parse_args())
locations_file = args['json']
image_file = args['photo']

print 'Loading data...'
with open(locations_file) as f:
    location_data = json.load(f)

location_array = location_data['locations']
print 'Found %s locations' % len(location_array)

print 'Creating sorted list of objects'
my_locations = []
for location in location_array:
    a_location = Location(location)
    my_locations.append(a_location)

my_locations = list(reversed(my_locations))

image = Image.open(image_file)
time_exif = image._getexif()[36867]
time_jpeg_unix = time.mktime(datetime.datetime.strptime(time_exif, "%Y:%m:%d %H:%M:%S").timetuple())

curr_loc = Location()
curr_loc.timestamp = int(time_jpeg_unix)
aprox_location = find_closest_in_time(my_locations, curr_loc)

lat_f = float(aprox_location.latitude) / 10000000.0
lon_f = float(aprox_location.longitude) / 10000000.0
hours_away = abs(aprox_location.timestamp - time_jpeg_unix) / 3600

print 'Found approximate location, %s hours away' % hours_away

if(hours_away < 4):
    #
    # Add exif gps data while keeping all other data
    #
    ef = JpegFile.fromFile(image_file)
    ef.set_geo(lat_f, lon_f)
    ef.writeFile(image_file)
else:
    print 'Location confidence too low'