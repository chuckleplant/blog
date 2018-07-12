import glob, os
import argparse
from Tkinter import *
from PIL import ImageTk, Image
import yaml

image_layout_width = 1000
image_layout_height = 600
image_layout_aspect = 1000.0/600.0
image_width = 0
image_height = 0

cur_path = os.path.dirname(os.path.realpath(__file__))
yaml_path = os.path.join(cur_path, '../_data/photos')
album_name = ""
album_path = ""



def get_yaml_path():
    return os.path.join(yaml_path, album_name) + '.yaml'

def prevButtonPressed():
    print 'Previous image'

def nextButtonPressed():
    print 'Next image'

def generate_yaml():
    print 'Generating YAML'
    photos_in_album = []
    for file in glob.glob(album_path+'/*'):
        photo_title = os.path.splitext(os.path.basename(file))[0]
        photo_img = album_name + '/' + photo_title
        photo_album = album_name
        photo_obj_yaml = dict(
            title = photo_title,
            img = photo_img,
            album = photo_album
        )
        photos_in_album.append(photo_obj_yaml)
    photo_yaml = dict(
        photos = photos_in_album
    )
    with open(get_yaml_path(), 'w') as outfile:
        yaml.dump(photo_yaml, outfile, default_flow_style=False)


def saveButtonPressed():
    print 'Save'
    generate_yaml()

def discardButtonPressed():
    print 'Discard'

    

def make_input_label(master, w, *args, **kwargs):
    f = Frame(master, width=w)
    f.pack_propagate(0) # don't shrink
    label = Label(f, *args, **kwargs)
    label.pack(side=LEFT,fill=X, expand=1)
    return label

def load_image_resized(path):
    temp_image = Image.open(path)
    aspect = float(temp_image.width) / float(temp_image.height)
    if(aspect > image_layout_aspect):
        image_width = image_layout_width
        image_height = image_width / aspect
    else:
        image_height = image_layout_height
        image_width = image_height * aspect
    temp_image = temp_image.resize((int(image_width),int(image_height)), Image.ANTIALIAS)
    return temp_image



parser = argparse.ArgumentParser(description='Pack images for web deployment')
parser.add_argument('-d', '--dir', help='Folder with the images', required=True)

args = vars(parser.parse_args())
album_path = args['dir']
album_name = os.path.basename(os.path.normpath(album_path))
types = ('*.jpg', '*.png', '*.jpeg', '*.JPG', '*.JPEG')
images = []
for extension in types:
    images.extend(glob.glob(os.path.join(album_path, extension)))
print 'Loaded %s images' % len(images)
print 'From  : ' + album_path
print "Album : " + album_name

if len(images) == 0:
    print 'No images in album'
    exit()

an_image = images[0]
path = an_image





root = Tk()
root.title("Gallery tool")
root.geometry("1280x720")
root.resizable(width=FALSE,height=FALSE)



# Widgets
#
img = ImageTk.PhotoImage(load_image_resized(path))
panel = Label(root, image = img)
#
# Frames
#
main_frame = Frame(root)
image_frame = Frame(main_frame)
input_frame = Frame(main_frame)
title_frame = Frame(input_frame)
album_frame = Frame(input_frame)
bottom_frame = Frame(root)
#
# buttons
#
next_button = Button(bottom_frame, text='Next', command=nextButtonPressed)
prev_button = Button(bottom_frame, text='Previous', command=prevButtonPressed)
save_button = Button(input_frame, text='Save', command=saveButtonPressed)
discard_button = Button(input_frame, text='Discard', command=discardButtonPressed)
#
# Text input
#
title_entry = Entry(title_frame)
album_entry = Entry(album_frame)
#
# Labels
#
image_label = Label(image_frame, image=img)
title_label = Label(title_frame, text="Title")
album_label = Label(album_frame, text="Album")


# Layout
#
main_frame.pack(fill=BOTH, expand=1)
image_frame.pack(side=LEFT, fill=BOTH, expand=1)
input_frame.pack(side=RIGHT)
title_frame.pack()
album_frame.pack()
bottom_frame.pack(side=BOTTOM, fill=BOTH)
#
next_button.pack(side=RIGHT)
prev_button.pack(side=LEFT)
save_button.pack()
discard_button.pack()
#
title_label.pack(side=LEFT)
album_label.pack(side=LEFT)
#
title_entry.pack(side=RIGHT)
album_entry.pack(side=RIGHT)
#
image_label.pack(fill=BOTH,expand=1)




# init values
title_entry.insert(0, 'some text')

# These may be for mac only, bring window to front
#
root.lift()
root.attributes('-topmost',True)
root.after_idle(root.attributes,'-topmost',False)

root.mainloop()