import glob, os, yaml, sys
from PIL import Image
from PIL.Image import Resampling
import math
import piexif
from datetime import datetime

cur_path = os.path.dirname(os.path.realpath(__file__))
yaml_path = os.path.join(cur_path, '../_data/photos')

def decode_usercomment(data):
    # First 8 bytes specify encoding
    encoding_prefix = data[:8]

    # Check the encoding based on prefix and decode accordingly
    if encoding_prefix == b'ASCII\x00\x00\x00':
        return data[8:].decode('ascii')
    elif encoding_prefix == b'UNICODE\x00':
        return data[8:].decode('utf-16')
    elif encoding_prefix == b'\x00\x00\x00\x00\x00\x00\x00\x00':
        return ""
    else:
        # Return raw data if encoding is unknown
        return data[8:]

def get_exif_elem(dict, tag, elem):
    rational_tuple = [piexif.ExifIFD.FNumber, piexif.ExifIFD.FocalLength]
    gps_tuple = [piexif.GPSIFD.GPSLatitude, piexif.GPSIFD.GPSLongitude]
    exif_elem = ''
    if tag in dict:
        if elem in dict[tag]:
            exif_elem = dict[tag][elem]
            if elem is piexif.ExifIFD.ExposureTime:
                return str(exif_elem[0]) + '/' + str(exif_elem[1])
            if elem in rational_tuple:
                return str(float(exif_elem[0]) / float(exif_elem[1]))
            elif elem is piexif.ExifIFD.DateTimeOriginal:
                dt = datetime.strptime(exif_elem.decode('utf-8'), '%Y:%m:%d %H:%M:%S')
                return dt.strftime('%d %B %Y')
            elif elem is piexif.ExifIFD.UserComment:
                decoded_usercomment = decode_usercomment(exif_elem)
                return decoded_usercomment
            elif elem in gps_tuple:
                degrees = float(exif_elem[0][0]) / float(exif_elem[0][1])
                minutes = float(exif_elem[1][0]) / float(exif_elem[1][1])
                seconds = float(exif_elem[2][0]) / float(exif_elem[2][1])
                return degrees + minutes/60 + seconds/3600
            else:
                return exif_elem
    return exif_elem


class BlogPhoto(object):
    def __init__(self, filename, album_name, removeGPS):
        exif_dict = piexif.load(filename)
        im = Image.open(filename)
        width,height = im.size
        self.aspect             = float(width)/float(height)
        self.latitude           = get_exif_elem(exif_dict,"GPS",piexif.GPSIFD.GPSLatitude)
        self.longitude          = get_exif_elem(exif_dict,"GPS",piexif.GPSIFD.GPSLongitude)
        try:
            self.timestamp = datetime.strptime((exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal]).decode('utf-8'), '%Y:%m:%d %H:%M:%S')
            self.date_time_original = get_exif_elem(exif_dict,"Exif",piexif.ExifIFD.DateTimeOriginal)
        except KeyError:
            self.timestamp = datetime.fromtimestamp(os.path.getmtime(filename))
            dt_obj = datetime.fromtimestamp(os.path.getmtime(filename))
            self.date_time_original = dt_obj.strftime('%d %B %Y')
        self.user_comment       = get_exif_elem(exif_dict,"Exif",piexif.ExifIFD.UserComment)
        self.cam_model          = get_exif_elem(exif_dict,"0th",piexif.ImageIFD.Model)
        self.lens_model         = get_exif_elem(exif_dict,"Exif",piexif.ExifIFD.LensModel)
        self.exposure           = get_exif_elem(exif_dict,"Exif",piexif.ExifIFD.ExposureTime)
        self.f_number           = get_exif_elem(exif_dict,"Exif",piexif.ExifIFD.FNumber)
        self.iso                = get_exif_elem(exif_dict,"Exif",piexif.ExifIFD.ISOSpeedRatings)
        self.focal_length       = get_exif_elem(exif_dict,"Exif",piexif.ExifIFD.FocalLength)
        self.photo_title        = os.path.basename(filename)
        self.photo_img          = album_name + '/' + self.photo_title
        self.photo_album        = album_name
        if removeGPS:
            self.latitude = ''
            self.longitude = ''

    def get_yaml(self):
        photo_obj_yaml = dict(
            title = os.path.splitext(os.path.basename(self.photo_title))[0],
            img = self.photo_img,
            album = self.photo_album,
            aspect = self.aspect,
            latitude = self.latitude,
            longitude = self.longitude,
            date_time_original = self.date_time_original,
            user_comment = self.user_comment,
            cam_model = self.cam_model,
            lens_model = self.lens_model,
            exposure = self.exposure,
            f_number = self.f_number,
            iso = self.iso,
            focal_length = self.focal_length
        )
        return photo_obj_yaml

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


def get_yaml_path(album_name):
    return os.path.join(yaml_path, album_name) + '.yaml'
    

def generate_yaml(album_name, album_path, image_paths):
    print ('Generating YAML for ' + album_name)
    reverse = False
    removeGPS = False
    options_path = os.path.join(album_path,"options.yaml")
    if os.path.isfile(options_path):
        with open(options_path, 'r') as options_file:
            options = yaml.load(options_file, Loader=yaml.FullLoader)
            if 'reverse' in options:
                reverse = options['reverse']
            if 'removeGPS' in options:
                removeGPS = options['removeGPS']


    photos_in_album = []
    blog_photos = []

    for file in image_paths:
        blog_photo = BlogPhoto(file, album_name, removeGPS)
        blog_photos.append(blog_photo)

    blog_photos.sort(reverse=reverse)
    for bp in blog_photos:
        photos_in_album.append(bp.get_yaml())

    photo_yaml = dict(
        photos = photos_in_album
    )
    with open(get_yaml_path(album_name), 'w') as outfile:
        yaml.dump(photo_yaml, outfile, default_flow_style=False)

def generate_yaml_for_album(album_path):
    images = []
    types = ('*.jpg', '*.png', '*.jpeg')
    if sys.platform != "win32":
        types += ('*.JPG', '*.PNG', '*.JPEG')
    for extension in types:
        images.extend(glob.glob(os.path.join(album_path, extension)))
    if len(images) == 0:
        print ('No images in album , ' + album_path)
        return
    elif "thumbnails" in album_path:
        print ('not this one')
        return
    album_name = os.path.basename(os.path.normpath(album_path))
    generate_yaml(album_name, album_path, images)

def res_for_pix_count(width, height, pixcount):
    aspect = float(width) / float(height)
    h = math.sqrt(float(pixcount) / aspect)
    w = aspect * h
    return int(w), int(h)


def res_for_height(width, height, desired_height):
    aspect = float(width)/float(height)
    new_width = aspect * desired_height
    return int(new_width), desired_height

def gen_thumb_size(img, thumbheight, thumbdir, album, fname):
    tw, th = res_for_height(img.width, img.height, thumbheight)
    img.thumbnail((tw,th), Resampling.LANCZOS)
    target_dir = os.path.join(thumbnail_path, str(thumbheight), album)
    target_file = os.path.join(target_dir, fname)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    img.save(target_file)


def process_blog_images(workspace_root='.'):
    """
    Process and resize images for a Jekyll blog.
    """
    # Get list of all the blog post files
    posts_directory = os.path.join(workspace_root, '_posts')
    posts = [f for f in os.listdir(posts_directory) if f.endswith('.md')]

    for post in posts:
        post_path = os.path.join(posts_directory, post)
        with open(post_path, 'r', encoding='utf-8') as file:
            # Extract the front matter (content between two '---' lines)
            lines = file.readlines()
            front_matter = ''.join(lines[1:lines.index('---\n', 1)])
            data = yaml.safe_load(front_matter)
            image_path = data.get('image', {}).get('path')

            if image_path:
                # Ensure that the image exists
                absolute_image_path = os.path.join(workspace_root, image_path)
                
                # Check if the resized image already exists in the img/600 folder
                resized_image_folder = os.path.join(workspace_root, 'img/600')
                output_path = os.path.join(resized_image_folder, os.path.basename(image_path))
                if os.path.exists(output_path):
                    print(f"Resized image for {post} already exists at {output_path}. Skipping.")
                    continue

                if os.path.exists(absolute_image_path):
                    # Resize the image
                    with Image.open(absolute_image_path) as img:
                        width_percent = (600 / float(img.size[0]))
                        new_height = int((float(img.size[1]) * float(width_percent)))
                        img_resized = img.resize((600, new_height), Image.ANTIALIAS)

                        # Save the resized image
                        os.makedirs(resized_image_folder, exist_ok=True)
                        img_resized.save(output_path)
                        print(f"Saved resized image for {post} to {output_path}")
                else:
                    print(f"Image path {absolute_image_path} does not exist for post {post}")
            else:
                print(f"{post_path} did not specify an image.")

process_blog_images(os.path.join(cur_path, ".."))
exit()

albums = glob.glob(cur_path+'/../img/albums/*/')
for album_path in albums:
    generate_yaml_for_album(album_path)

max_pix_count = 3000000
photo_path = os.path.join(cur_path,"../img/albums")
thumbnail_path = os.path.join(cur_path,"../img")
extensions = ['jpg', 'JPG', 'JPEG', 'png', 'PNG', 'jpeg']


for folder, subs, files in os.walk(photo_path):
    for filename in files:
        abs_file = os.path.join(folder,filename)
        name,ext = os.path.splitext(abs_file)
        if any(filename.endswith(ext) for ext in extensions):       
            album_name = os.path.basename(os.path.dirname(abs_file))
            img = Image.open(abs_file)

            touched = False

            exif_dict = piexif.load(abs_file)
            exif_bytes = piexif.dump(exif_dict)
            if piexif.ImageIFD.Orientation in exif_dict["0th"]:    
                touched = True
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

            width, height = img.size
            numpix = width * height
            if numpix > max_pix_count:
                w, h = res_for_pix_count(width, height, max_pix_count)
                img.thumbnail((w,h), Image.ANTIALIAS)
                print ('Resized %s' % filename)
                touched = True

            if touched:
                img.save(abs_file, exif=exif_bytes)
            # https://coderwall.com/p/nax6gg/fix-jpeg-s-unexpectedly-rotating-when-saved-with-pil

            gen_thumb_size(img, 250, thumbnail_path, album_name, filename)
            gen_thumb_size(img, 20, thumbnail_path, album_name, filename)