#!/bin/env python3
from PIL import Image, ImageDraw
import sys
import argparse
import re

def imgmerge(img):
    trans = createTrans(img.size, 'RGBA')
    transed = Image.blend(img, trans, 0.5)
    return transed

def imgframe(img, frameWidth):
    transed = createTrans((img.size[0] + 2 * frameWidth, img.size[1] + 2 * frameWidth))
    transed.paste(img, (frameWidth, frameWidth))
    return transed

def createTrans(size, mode='RGB'):
    BAR_SIZE = size[1]/5
    transflag = Image.new(mode, size)
    drawer = ImageDraw.Draw(transflag)
    drawer.rectangle([(0,0), size], "#32d7d0")
    drawer.rectangle([(0, BAR_SIZE), (size[0], size[1] - BAR_SIZE)], "#f98bc9")
    drawer.rectangle([(0, 2 * BAR_SIZE), (size[0], size[1] - 2 * BAR_SIZE)], "#ffffff")
    return transflag

def colorToTrans(img, colorRange = 0, color = (255,255,255)):
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
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def pickCommand(img):
    if args.command == 'merge':
        transed = imgmerge(img)
        transed.save('transmerged.png')
    elif args.command == 'frame':
        transed = imgframe(img, args.width)
        transed.save('transframed.png')
    elif args.command == 'color':
        if not re.match('[\da-fA-F]{6}', args.colorhex):
            print("Invalid color")
            return None
        transed = colorToTrans(img, args.threshold, hexToRGB(args.colorhex))
        transed.save('transedcolor.png')

parser = argparse.ArgumentParser(description="Adding trans flag to images in various ways.", prog="imagetranser")
subparser = parser.add_subparsers(dest='command', help='For more help type  imagetranser.py command -h')
merge = subparser.add_parser('merge', help="Merges image with a transgender flag.")
frame = subparser.add_parser('frame', help="Adds a transgender flag frame.")
color = subparser.add_parser('color', help="Change a color within a specified range and turn it into a transgender flag (used mostly for changing the background).")

frame.add_argument("filepath", type=str, help="Path to the image file.", metavar="file")
color.add_argument("filepath", type=str, help="Path to the image file.", metavar="file")
merge.add_argument("filepath", type=str, help="Path to the image file.", metavar="file")

frame.add_argument('-w', "--width", metavar="width", nargs='?', type=int, default=10, help="Specifies width of the frame.")
color.add_argument('-t', '--threshold', type=int, nargs='?', metavar="threshold", default=0, help="Specifies a color threshold.")
color.add_argument('-c', '--colorhex', metavar="colorhex", nargs='?', type=str, default="ffffff", help="Specifies color e.g ff00ff (without #)")

args = parser.parse_args()
img = Image.open(args.filepath)
pickCommand(img)