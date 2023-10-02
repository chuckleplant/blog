---
layout: post
title:  "Photo geotagging using your Google location history"
date:   2018-07-23
tags: [google,gps,geotag,python,exif,jpeg,creepy,photography]
comments: true
disqus_identifier: geotagPython
image:
    path: "images/posts/geotag-gphotos.png"
---

> He who controls the past controls the future. He who controls the present controls the past.
>
> -- George Orwell, 1984


[Here](https://github.com/chuckleplant/blog/blob/master/scripts/location-geotag.py)'s a script that runs on Python that can add GPS tags to your photos (jpg) given your Google location history. You have to download the location history from [https://takeout.google.com/](https://takeout.google.com/) and run:

~~~ bash
python location-geotag.py --dir {your photos directory} --json {your location history}
~~~

Do **backup** your photos before doing this, you may lose them.

## Somebody's watching me

I use Google Photos for keeping the thousands if not hundreds of thousands of pictures I've taken over the years. Unlimited storage (I love unlimited stuff) for the price of image compression and probably Google using your photos for machine learning, ads and other orwellian ends.

{% include image.html file="posts/geotag-gphotos.png" description="Google Photos interface showing a map of where the photo was taken." %}

One feature I like is geotagging. Google Photos will use your location history to deduce where the photo was taken. Then they'll show you a nice map when visiting the image and you'll go *'Oh look I've been there!'*

However, I noticed that when exporting the photos out of Google, you don't get the approximate geotag as metadata in your JPEG. This bothers me because the image gallery I'm using also shows you a small map if the image has GPS data in it ([check it out!]({% post_url 2018-07-23-japan-trip %})). 

After some research I found that it's actually not possible to export the geotags from Google Photos. I did find that you can actually download your whole location history, all the location data Google has on you. It's a lot of data depending on how long you've used a smartphone.

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
~~~

Using the [bisect](https://docs.python.org/2/library/bisect.html) python module I could have $$O(\log{}n)$$ search times, which is as good as I can hope for. I had to reverse the locations because Google exports them in descending timestamp order. 

I got the timestamp from my images using PIL black magic `image._getexif()[36867]`. And then it was a matter of finding the location with the closest timestamp to my image. From [SO](https://stackoverflow.com/a/12141511/2628257):

~~~ python
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
~~~

In order to add the GPS information I used the [pexif](https://github.com/bennoleslie/pexif) module at first. But I found that the Exif data written by the module was sometimes broken. I switched to [piexif](https://pypi.org/project/piexif/), which does basically the same. The documentation however was a bit harder to bite, luckily I found [this gist](https://gist.github.com/c060604/8a51f8999be12fc2be498e9ca56adc72) that showed how to embed GPS data via exif.

I also added a time threshold of a couple of hours, any location out of that threshold would be considered inaccurate.

~~~ python
#
# piexif library usage to add GPS info to an image
#
approx_location = find_closest_in_time(my_locations, curr_loc)
hours_away = abs(approx_location.timestamp - time_jpeg_unix) / 3600

if(hours_away < hours_threshold):
    # Google stores these as x-e7
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
~~~

The full script can be found [here](https://github.com/chuckleplant/blog/blob/master/scripts/location-geotag.py). Make sure to make a backup of your images before running the script!

