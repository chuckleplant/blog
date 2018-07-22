import os
from subprocess import call
import argparse
import json
from pprint import pprint
import datetime
import bisect
from bisect import bisect_left, bisect_right

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


def takeClosest(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    
    before = myList[pos - 1]
    after = myList[pos]
    if after.timestamp - myNumber.timestamp < myNumber.timestamp - before.timestamp:
       return after
    else:
       return before

            
parser = argparse.ArgumentParser()
parser.add_argument('-j','--json', help='The JSON file containing your location history.', required=True)

args = vars(parser.parse_args())
locations_file = args['json']

print 'Loading data...'
with open(locations_file) as f:
    location_data = json.load(f)

location_array = location_data['locations']
print 'Found %s locations' % len(location_array)

my_locations = []
for location in location_array:
    timestamp = int(location['timestampMs']) / 1000

    print (datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S --- ' + str(timestamp)))
    a_location = Location(location)
    #my_locations.append(a_location)
    bisect.insort(my_locations, a_location)



custom_ts = 1532122067 #would be second element
input_location = Location()
input_location.timestamp = custom_ts

print takeClosest(my_locations, input_location).timestamp