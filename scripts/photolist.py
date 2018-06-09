import glob, os
import argparse
from Tkinter import *
from PIL import ImageTk, Image


image_layout_width = 1000
image_layout_height = 600
image_layout_aspect = 1000.0/600.0
image_width = 0
image_height = 0



#fits image inside window
def fitImage(image, window):
    rect.x = 0
    rect.y = 0
    rect.w = 0
    rect.h = 0
    return rect

def prevButtonPressed():
    print 'Previous image'

def nextButtonPressed():
    print 'Next image'

def saveButtonPressed():
    print 'Save'

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



parser = argparse.ArgumentParser(description='Pack images for web deployment')
parser.add_argument('-d', '--dir', help='Folder with the images', required=True)
parser.add_argument('-o', '--output', help='Output YAML file', required=True)

args = vars(parser.parse_args())
img_dir = args['dir']
out_fil = args['output']
types = ('*.jpg', '*.png', '*.jpeg')
images = []
for extension in types:
    images.extend(glob.glob(os.path.join(img_dir, extension)))
print 'Loaded %s images' % len(images)


an_image = images[0]
print an_image
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
country_frame = Frame(input_frame)
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
country_entry = Entry(country_frame)
album_entry = Entry(album_frame)
#
# Labels
#
image_label = Label(image_frame, image=img)
title_label = Label(title_frame, text="Title")
country_label = Label(country_frame, text="Country")
album_label = Label(album_frame, text="Album")


# Layout
#
main_frame.pack(fill=BOTH, expand=1)
image_frame.pack(side=LEFT, fill=BOTH, expand=1)
input_frame.pack(side=RIGHT)
title_frame.pack()
country_frame.pack()
album_frame.pack()
bottom_frame.pack(side=BOTTOM, fill=BOTH)
#
next_button.pack(side=RIGHT)
prev_button.pack(side=LEFT)
save_button.pack()
discard_button.pack()
#
title_label.pack(side=LEFT)
country_label.pack(side=LEFT)
album_label.pack(side=LEFT)
#
title_entry.pack(side=RIGHT)
country_entry.pack(side=RIGHT)
album_entry.pack(side=RIGHT)
#
image_label.pack(fill=BOTH,expand=1)




# init values
title_entry.insert(0, 'some text')
country_entry.insert(0, 'Spain')
root.mainloop()