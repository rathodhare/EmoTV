"""
First make sure you have the Python Image libraries installed
   sudo pip install pillow
Down below you will need to define the absolute path to the images see "dir=..."
Run this by entering
    python stitch.py
"""
from PIL import Image
import os

# change this to the director that has your images
dir = "/home/harekrissna/Desktopsss/ITSP"
out_file = "joined_images.jpg"

def getFiles(dir):
    files = []
    for c in os.listdir(dir):
        _, ext = os.path.splitext(c)

        if ext == '.jpg':
            files.append(c)

    return files

def merge_images(dir, file):
    image = Image.open(os.path.join(dir, file))
    base = Image.open(out_file)

    (width1, height1) = image.size
    (width2, height2) = base.size

    result_width = max(width1, width2)
    result_height = height1 + height2

    out = Image.new('RGB', (result_width, result_height))
    out.paste(im=base, box=(0, 0))
    out.paste(im=image, box=(0, height2))

    out.save(out_file,"JPEG")
    return out

def createTarget():
    result = Image.new('RGB', (1, 1))
    result.save(out_file,"JPEG")



ff = getFiles(dir)
createTarget()
for f in ff:
    merge_images(dir, f)

print ("all done")
