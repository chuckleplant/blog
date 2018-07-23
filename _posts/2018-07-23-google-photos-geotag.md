---
layout: post
title:  "Photo geotagging using your Google location history"
date:   2018-07-23
tags: [google,gps,geotag,python,exif,jpeg,creepy,photography]
comments: true
disqus_identifier: geotagPython
---

> Who controls the past controls the future. Who controls the present controls the past.

## Where I've been

I use Google Photos for keeping the thousands if not hundreds of thousands of pictures I've taken over the years. Unlimited storage (I love unlimited stuff) for the price of image compression and probably Google using your photos for machine learning, ads and other orwellian ends.

{% include image.html file="posts/geotag-gphotos.png" description="Google Photos interface showing a map of where the photo was taken." %}

One feature I like is geotagging. Google Photos will use your location history to deduce where the photo was taken. Then they'll show you a nice map when visiting the image and you'll go *'Oh look I've been there!'*

However, I noticed that when exporting the photos out of Google, you don't get the approximate geotag as metadata in your JPEG. This bothers me because the image gallery I'm using also shows you a small map if the image has GPS data in it.

After some research I found that it's actually not possible to export the geotags. I did find that you can actually download your whole location history, all the location data Google has on you. It's a lot of data depending on how long you've used a smartphone.

{% include image.html file="posts/gdatum.png" description="Get all the data Google has on you from [https://takeout.google.com/](https://takeout.google.com/). The list goes on and on." %}

So I made a small script that adds the GPS information on any photo using your location history as input. It's quite simple but works surprisingly well.

## Script

The script is written in Python. My location history was around 200Mb, so I wanted an efficient way to search through the whole file.

The Google export looks like this:

~~~ json
{
  "locations" : [ {
    "timestampMs" : "1532122858202",
    "latitudeE7" : 48445182,
    "longitudeE7" : 24287419,
    "accuracy" : 13,
    "altitude" : 117,
    "verticalAccuracy" : 2
  }, {
    "timestampMs" : "1532122465164",
    "latitudeE7" : 439445411,
    "longitudeE7" : 26287254,
    "accuracy" : 14,
    "altitude" : 117,
    "verticalAccuracy" : 2
  }, {
    "timestampMs" : "1532122068529",
    "latitudeE7" : 419945411,
    "longitudeE7" : 12287254,
    "accuracy" : 14,
    "altitude" : 117,
    "verticalAccuracy" : 2
  }]
}
~~~

I loaded the JSON and created a custom `Location` class which just registered the GPS info and the timestamp. I converted the timestamps to seconds when loading them. I also defined some operators to be able to sort and search the locations list.

~~~ python
#
# Note I construct directly from the JSON dictionary
#
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
~~~

Using the [bisect](https://docs.python.org/2/library/bisect.html) python module I could have O(log n) search times, which is as good as I can hope for. I had to reverse the locations because Google exports them in descending timestamp order. 

I got the timestamp from my images using PIL black magic `image._getexif()[36867]`. And then it was a matter of finding the location with the closest timestamp to my image. From [SO](https://stackoverflow.com/a/12141511/2628257):

~~~ python
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
~~~

In order to add the GPS information I used the [pexif](https://github.com/bennoleslie/pexif) module. Which was designed with geotagging in mind. I also added a time threshold of a couple of hours, any location out of that threshold would be considered inaccurate.

~~~ python
    if(hours_away < hours_threshold):
        ef = JpegFile.fromFile(image_file)
        ef.set_geo(lat_f, lon_f)
        ef.writeFile(image_file)
    else:
        print 'Time threshold surpassed'
~~~

The full script can be found [here](https://gist.github.com/chuckleplant/84b48f5c2cb743013462b6cb5f598f01). Make sure to make a backup of your images before running the script!

