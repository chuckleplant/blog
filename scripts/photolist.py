import glob, os
import argparse
import Tkinter as tk
from PIL import ImageTk, Image

#fits image inside window
def fitImage(image, window):
    rect.x = 0
    rect.y = 0
    rect.w = 0
    rect.h = 0
    return rect

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
root = tk.Tk()
root.title("Gallery tool")
root.geometry("100x100")
root.configure(background="black")
img = ImageTk.PhotoImage(Image.open(path))
print "%sx%s" % (img.width(), img.height())
panel = tk.Label(root, image = img)
panel.pack(side = "bottom", fill = "both", expand = "no")
root.mainloop()