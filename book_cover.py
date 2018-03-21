#!/usr/bin/env python
# encoding: utf-8
"""
Knock up a book cover
"""
from __future__ import print_function
import argparse
import hashlib
import random
import struct
from PIL import Image, ImageFont, ImageDraw


FONTS = [
    "ANTQUAB.TTF",
    "arial.ttf",
    "arialbd.ttf",
    "BOOKOS.TTF",
    "BOOKOSB.TTF",
    "calibri.ttf",
    "calibrib.ttf",
    "times.ttf",
    "cour.ttf",
    "courbd.ttf",
    "georgia.ttf",
    "georgiab.ttf",
    "timesbd.ttf",
]


def dopplr(name):
    """
    Take the MD5 digest of a name,
    convert it to hex and take the
    first 6 characters as an RGB value.
    """
    return "#" + hashlib.sha224(name).hexdigest()[:6]


def foreground_colour(background_colour):
    """
    For a given background colour, return black or white for the text
    http://stackoverflow.com/a/946734/724176
    """
    # Get RGB values
    background_colour = background_colour.lstrip("#")
    background_colour = struct.unpack('BBB', background_colour.decode('hex'))
    r = background_colour[0]
    g = background_colour[1]
    b = background_colour[2]
    print(r, g, b)

    # The perceived brightness of the individual primaries red, green, and blue
    # are not identical. The quickest advice I can give is to use the
    # traditional formula to convert RGB to gray - R*0.299 + G*0.587 + B*0.114.
    # There are lots of other formulas.
    grey = r*0.299 + g*0.587 + b*0.144

    # The gamma curve applied to displays makes the middle gray value higher
    # than you'd expect. This is easily solved by using 186 as the middle value
    # rather than 128. Anything less than 186 should use white text, anything
    # greater than 186 should use black text.
    print(grey)
    if grey < 186:
        return "white"
    else:
        return "black"


def largest_font_that_fits(draw, font_file, text, cover_width):
    """ Find the largest-sized font that'll fit this text on this cover  """
    text_w = cover_width + 1
    font_size = 110
    padding = 20
    while(text_w + padding > cover_width):
        font_size -= 10
        font = ImageFont.truetype(font_file, font_size)
        text_w, text_h = draw.textsize(text, font)
    return font


def get_an_image(text):
    """ Get some public domain image for text """

    # Get the second or fourth word
    index = random.choice([1, 3])
    text = text.split()[index]
    print(text)
    sort = random.choice(["relevance", "interestingness-desc"])
    print(sort)

    from flickr_search_downloadr import flickr_search_downloadr

    filename = flickr_search_downloadr(text,
                                       tags=None,
                                       user_id="internetarchivebookimages",
                                       sort=sort,
                                       quantity=1,
                                       number=None,
                                       size="m",
                                       title=None,
                                       noclobber=True,
                                       outdir="E:/stufftodelete")
    img = Image.open(filename[0])
    return img


def book_cover(title, author, outfile=None):
    # Last space to newline
    k = title.rfind(" ")
    title = title[:k] + "\n" + title[k+1:]

    # 50% chance to capitalise
    if random.randrange(2):
        title = title.upper()
        author = author.upper()

    font_file = random.choice(FONTS)
    print(font_file)

    cover_width = 400
    cover_height = 600
    offset = 50

    bg_colour = dopplr(title)
    fg_colour = foreground_colour(bg_colour)
    print(bg_colour, fg_colour)

    img = Image.new("RGB", (cover_width, cover_height), color=bg_colour)
    draw = ImageDraw.Draw(img)

    # Title
    font = largest_font_that_fits(draw, font_file, title, cover_width)

    text_w, text_h = draw.textsize(title, font)
    x = (cover_width - text_w)/2
    y = offset
    draw.multiline_text((x, y), title, font=font, align="center",
                        fill=fg_colour)
    bottom_of_top_text = y + text_h

    # Author
    font = largest_font_that_fits(draw, font_file, author, cover_width)
    text_w, text_h = draw.textsize(author, font)
    x = (cover_width - text_w)/2
    y = cover_height - text_h - offset
    draw.multiline_text((x, y), author, font=font, align="center",
                        fill=fg_colour)
    top_of_bottom_text = y

    try:
        img2 = get_an_image(title)
        w, h = img2.size
        x = cover_width/2 - w/2
        y_gap = top_of_bottom_text - bottom_of_top_text
        y = bottom_of_top_text + y_gap/2 - h/2
        img.paste(img2, (x, y))
    except Exception as e:
        print(str(e))

    # img.show()
    if outfile:
        img.save(outfile)
    return img


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Knock up a book cover",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-t', '--title',
        help="Book title")
    parser.add_argument(
        '-a', '--author',
        help="Book author")
    parser.add_argument(
        '-o', '--outfile', default="book_cover.png",
        help="Output image filename")
    args = parser.parse_args()

    img = book_cover(args.title, args.author, args.outfile)
    img.show()


# End of file
