#!/usr/bin/env python
# encoding: utf-8
"""
Knock up a book cover
"""
from __future__ import print_function
import argparse
import random
from PIL import Image, ImageFont, ImageDraw


COLOUR_SCHEMES = [
    ["black", "white"],
    ["#FA6900", "white"],
    ["#AA3939", "white"],
    ["#2D882D", "white"],
]


FONTS = [
    "ANTQUAB.TTF",
    "arial.ttf",
    "BOOKOS.TTF",
    "cour.ttf",
    "calibri.ttf",
]


def largest_font_that_fits(draw, font_file, text, cover_width):
    """ Find the largest-sized font that'll fit this text on this cover  """
    text_x = cover_width + 1
    font_size = 110
    padding = 20
    while(text_x + padding > cover_width):
        font_size -= 10
        font = ImageFont.truetype(font_file, font_size)
        text_x, text_y = draw.textsize(text, font)
    return font


def book_cover(title, author, outfile=None):
    # Last space to newline
    k = title.rfind(" ")
    title = title[:k] + "\n" + title[k+1:]

    colours = random.choice(COLOUR_SCHEMES)
    print(colours)
    # random.shuffle(colours)
    font_file = random.choice(FONTS)
    print(font_file)

    cover_width = 400
    cover_height = 600
    offset = 50

    img = Image.new("RGB", (cover_width, cover_height), color=colours[0])
    draw = ImageDraw.Draw(img)

    # Title
    font = largest_font_that_fits(draw, font_file, title, cover_width)

    text_x, text_y = draw.textsize(title, font)
    x = (cover_width - text_x)/2
    y = offset
    draw.multiline_text((x, y), title, font=font, align="center",
                        fill=colours[1])

    # Author
    font = largest_font_that_fits(draw, font_file, author, cover_width)
    text_x, text_y = draw.textsize(author, font)
    x = (cover_width - text_x)/2
    y = cover_height - text_y - offset
    draw.multiline_text((x, y), author, font=font, align="center",
                        fill=colours[1])
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
