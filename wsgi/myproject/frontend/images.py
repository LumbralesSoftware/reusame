import os
from PIL import Image, ImageOps, ImageDraw

from django.conf import settings

def create_thumb(item, width):
    #path to original image and file split
    original_file = os.path.join(settings.MEDIA_ROOT, item.image.name)
    filehead, filetail = os.path.split(original_file)

    #check if image path exists otherwise create it
    image_path = os.path.join(settings.IMAGE_ON_DEMAND_DIR, width)
    if not os.path.exists(image_path):
        os.mkdir(image_path)

    #create image path. note, width SHOULD be a string otherwise os.path.join fails
    image_file = os.path.join(settings.IMAGE_ON_DEMAND_DIR, width, filetail)

    # we need te calculate the new height based on the ratio of the original image, create integers
    ratio = float(float(item.image.width) / float(item.image.height))
    height = int(float(width) / ratio)
    iwidth = int(width)


    # check if file exists and the original file hasn't updated in between
    if os.path.exists(image_file) and os.path.getmtime(original_file) > os.path.getmtime(image_file):
            os.unlink(image_file)

    # if the image wasn't already resized, resize it.Maybe I should rewrite it to do this directly with PythonMagick
    # taken from snippet http://www.djangosnippets.org/snippets/453/

    if not os.path.exists(image_file):
        image = Image.open(original_file)
        #assert False
        image.thumbnail([iwidth, height], Image.ANTIALIAS)
        format = 'png' # conver to PNG to be able to set the transparent mask

        bigsize = (image.size[0] * 3, image.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(image.size, Image.ANTIALIAS)
        image.putalpha(mask)

        #optional unsharp mask using snippet http://www.djangosnippets.org/snippets/1267/
        #image = usm(image,settings.RADIUS,settings.SIGMA,settings.AMOUNT,settings.THRESHOLD)

        try:
            image.save(image_file, format, quality=90, optimize=1)
        except:
            image.save(image_file, format, quality=90)

    return filetail
