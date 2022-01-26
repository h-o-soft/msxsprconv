#!/usr/bin/env python3
import sys
import argparse
from PIL import Image

used_colors = []
color_index = [-1] * 16
msx_palette = [
    (0,0,0),
    (0,0,0),
    (0x3e, 0xb8, 0x49),
    (0x74, 0xd0, 0x7d),
    (0x59, 0x55, 0xe0),
    (0x80, 0x76, 0xf1),
    (0xb9, 0x5e, 0x51),
    (0x65, 0xdb, 0xef),
    (0xdb, 0x65, 0x59),
    (0xff, 0x89, 0x7d),
    (0xcc, 0xc3, 0x5e),
    (0xde, 0xd0, 0x87),
    (0x3a, 0xa2, 0x41),
    (0xb7, 0x66, 0xb5),
    (0xcc, 0xcc, 0xcc),
    (0xff, 0xff, 0xff)
    ]

def get_color_index(col):
    diff_sum = 256 * 3
    idx = 1
    cnt = 0
    for c in msx_palette:
        sum = abs(col[0] - c[0]) + abs(col[1] - c[1]) + abs(col[2] - c[2])
        if sum <= diff_sum:
            idx = cnt
            diff_sum = sum
        cnt = cnt + 1
    return idx

def count_color(img):
    color_count = 0
    width, height = img.size

    for y in range(height):
        for x in range(width):
            col = img.getpixel((x,y))
            if col[3] != 0:
                exists = False
                for c in used_colors:
                    if c[0] == col[0] and c[1] == col[1] and c[2] == col[2]:
                        exists = True
                        break
                if not exists:
                    used_colors.append(tuple(col))
    
    idx = 0
    for col in used_colors:
        guess_idx = get_color_index(col)
        color_index[guess_idx] = idx
        idx = idx + 1

    return len(used_colors)

def create_sprite_data(img, sz, x, y, cidx, midx):
    target_col = used_colors[cidx]

    vram_data = bytearray()
    get_ofs = []
    if sz == 16:
        get_ofs = [(0,0), (0,8), (8,0), (8,8)]
    else:
        get_ofs = [(0,0)]

    for ofs in get_ofs:
        gx = x * sz + ofs[0]
        gy = y * sz + ofs[1]
        for oy in range(8):
            dat = 0
            for ox in range(8):
                col = img.getpixel((gx + ox,gy + oy))
                if col[3] != 0 and col[0] == target_col[0] and col[1] == target_col[1] and col[2] == target_col[2]:
                    dat = dat | (1 << (7 - ox))
            vram_data.append(dat)
    
    idx = 0
    for val in vram_data:
        if output_format == "txt":
            if (idx % 8) == 0:
                sys.stdout.write("\tDB ")
        if output_format == "txt":
            sys.stdout.write("$" + format(val, '02x'))
        else:
            sys.stdout.buffer.write(val.to_bytes(1, 'little'))
        if output_format == "txt":
            if (idx % 8) != 7:
                sys.stdout.write(",")
            else:
                if args.comment:
                    sys.stdout.write("\n")
                else:
                    sys.stdout.write(" ; " + str(x) + "," + str(y) + " " + str(midx) + "\n")
        idx = idx + 1

parser = argparse.ArgumentParser(description='MSX Sprite Converter Version 0.2.0 Copyright 2022 H.O SOFT Inc.')
parser.add_argument('path', help='image path')
parser.add_argument('-s', '--size', help='Sprite Size ( 8 or 16 ) [default = 16]', type=int, default=16)
parser.add_argument('-l', '--label', help='Assembler Label [default = "_sprite"]', default="_sprites")
parser.add_argument("-o", '--output', help='Directs the output to a name of your choice')
parser.add_argument('-f', '--format', choices=['txt', 'bin'], help='Output format text or binary [default= "txt"]', default="txt")
parser.add_argument('-c', '--comment', help='Add long information comment (only txt format)', action='store_true')

args = parser.parse_args()

if args.output != None:
    sys.stdout = open(args.output, 'w+')

output_format = args.format
spr_size = args.size

im = Image.open(args.path)
im_rgba = im.convert('RGBA')
width, height = im.size

col_count = count_color(im_rgba)

x_count = width  // spr_size
y_count = height // spr_size

if output_format == "txt":
    sys.stdout.write("; Sprite : " + args.path + " / size " + str(spr_size) + " / Count " + str(x_count * y_count) + "\n")
    sys.stdout.write(args.label + ":\n")

for y in range(y_count):
    for x in range(x_count):
        # for idx in range(col_count):
        for i, idx in enumerate(color_index):
            if idx >= 0:
                if output_format == "txt" and args.comment:
                    sys.stdout.write("; " + str(x) + "," + str(y) + " COL " + str(i) + " : (" + str(used_colors[idx][0]) + ","+ str(used_colors[idx][1]) + ","+ str(used_colors[idx][2]) + ")\n")
                create_sprite_data(im_rgba, spr_size, x, y, idx, i)

sys.stdout = sys.__stdout__
sys.exit(0)
