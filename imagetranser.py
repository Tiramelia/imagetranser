#!/bin/env python3
from PIL import Image, ImageDraw
import sys
import argparse
import re


def imgmerge(img, args):
    """Merges an image with a trans flag.
    
    Arguments:
        img {PIL.Image.Image} -- PIL image object
        args {whatever parse_args() returns} -- passed arguments
    
    Returns:
        PIL.Image.Image -- PIL image object
    """
    trans = createTrans(img.size, 'RGBA')
    transed = Image.blend(img, trans, 0.5)
    return transed

def imgframe(img, args):
    """Adds a trans frame to an image.
    
    Arguments:
        img {PIL.Image.Image} -- PIL image object
        args {whatever parse_args() returns} -- passed arguments
    
    Returns:
        PIL.Image.Image -- PIL image object
    """
    frameWidth = args.width
    transed = createTrans((img.size[0] + 2 * frameWidth, img.size[1] + 2 * frameWidth))
    transed.paste(img, (frameWidth, frameWidth))
    return transed

def createTrans(size, mode='RGB'):
    """Creates image object of a trans flag.
    
    Arguments:
        size {tuple} -- A 2-tuple containing width and height.
    
    Keyword Arguments:
        mode {str} -- PIL image object opening mode (default: {'RGB'})
    
    Returns:
        PIL.Image.Image -- PIL image object 
    """
    BAR_SIZE = size[1]/5
    transflag = Image.new(mode, size)
    drawer = ImageDraw.Draw(transflag)
    drawer.rectangle([(0,0), size], "#32d7d0")
    drawer.rectangle([(0, BAR_SIZE), (size[0], size[1] - BAR_SIZE)], "#f98bc9")
    drawer.rectangle([(0, 2 * BAR_SIZE), (size[0], size[1] - 2 * BAR_SIZE)], "#ffffff")
    return transflag

def colorToTrans(img, args):
    """Changes specified colors of an image to trans flag.
    
    Arguments:
        img {PIL.Image.Image} -- PIL image object
        args {whatever parse_args() returns} -- passed arguments
    
    Returns:
        PIL.Image.Image -- PIL image object
    """
    colorRange = args.threshold
    color = hexToRGB(args.colorhex)

    transed = createTrans(img.size)

    pixdata = img.load()
    transpixdata = transed.load()

    width, height = img.size
    for y in range(height):
        for x in range(width):
            transform = True
            for colors in zip(color, pixdata[x,y]):
                if abs(colors[0] - colors[1]) > colorRange:
                    transform = False
            if transform:
                pixdata[x, y] = transpixdata[x, y]
    return img

def hexToRGB(hex):
    """Changes color hex to RGB value.
    
    Arguments:
        hex {str} -- String containing hex number of a color (without #)
    
    Returns:
        tuple -- 3-tuple containing R, G and B values.
    """
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def pickCommand():
    """Takes the passed arguments and choses a function to call.
    """
    args = parser.parse_args()
    img = Image.open(args.filepath)
    switch = {
        'merge' : imgmerge,
        'frame' : imgframe,
        'color' : colorToTrans
    }
    transformFunction = switch.get(args.command)
    result = transformFunction(img, args)
    result.save('transed.png')
    print('Saved as transed.png') 

def colorhex(value):
    """Function for checking if passed argument is in correct format.
    """
    if not re.match('[\da-fA-F]{6}', value):
        raise argparse.ArgumentTypeError("{0} is  an invalid color hex.".format(value))
        return None
    hexToRGB(value)
    return value

parser = argparse.ArgumentParser(description="Adding trans flag to images in various ways.", prog="imagetranser")
subparser = parser.add_subparsers(dest='command', help='For more help type  imagetranser.py command -h', required=True)
merge = subparser.add_parser('merge', help="Merges image with a transgender flag.")
frame = subparser.add_parser('frame', help="Adds a transgender flag frame.")
color = subparser.add_parser('color', help="Change a color within a specified range and turn it into a transgender flag (used mostly for changing the background).")

frame.add_argument("filepath", type=str, help="Path to the image file.", metavar="file")
color.add_argument("filepath", type=str, help="Path to the image file.", metavar="file")
merge.add_argument("filepath", type=str, help="Path to the image file.", metavar="file")

frame.add_argument('-w', "--width", metavar="width", nargs='?', type=int, default=10, help="Width of the frame.")
color.add_argument('-t', '--threshold', type=int, nargs='?', metavar="threshold", default=0, help="Color threshold.")
color.add_argument('-c', '--colorhex', metavar="colorhex", nargs='?', type=colorhex, default="ffffff", help="Color hex e.g ff00ff (without #)")

pickCommand()