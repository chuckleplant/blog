import glob, os
import argparse
from Tkinter import *
from PIL import ImageTk, Image

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
#root.resizable(width=FALSE,height=FALSE)

img = ImageTk.PhotoImage(Image.open(path))
print "%sx%s" % (img.width(), img.height())

# widgets
panel = Label(root, image = img)
#
# Frames
#
main_frame = Frame(root)
image_frame = Frame(main_frame)
input_frame = Frame(main_frame)
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
title_input = Entry(input_frame)
country_input = Entry(input_frame)
album_input = Entry(input_frame)
#
# Labels
#
image_label = Label(image_frame, text="Image", bg="green", fg="white")


main_frame.pack(fill=BOTH, expand=1)
image_frame.pack(side=LEFT, fill=BOTH, expand=1)
input_frame.pack(side=RIGHT)
bottom_frame.pack(side=BOTTOM, fill=BOTH)

next_button.pack(side=RIGHT)
prev_button.pack(side=LEFT)
save_button.pack()
discard_button.pack()
title_input.pack()
country_input.pack()
album_input.pack()
image_label.pack(fill=BOTH,expand=1)

#save_button.pack()
#right_frame.pack(fill=Y)
#title_input.pack()
#bottom_frame.pack(fill=X)
#country_input.pack()
#album_input.pack()


#bottom_frame.pack(side=BOTTOM, fill=HORIZONTAL)
#right_frame.pack(side=RIGHT)
#next_button.pack()
#prev_button.pack()
#save_button.pack()
#discard_button.pack()




# init values
title_input.insert(0, 'some text')
country_input.insert(0, 'Spain')
root.mainloop()