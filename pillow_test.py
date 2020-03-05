from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from math import sqrt
from textwrap import wrap
import re
import string

COL = {
    "blue":[114,137,218],
    "white":[255,255,255],
    "text":(230,230,230),
    "gray":[153,170,181],
    "dark":[44,47,51],
    "black":[35,39,42],
    "code":(0,200,0)
}
ARC_R = 100
LINE_W = 20
FONT_S = 32
ASPECT = 15
FONT = {
    "n":ImageFont.truetype("Roboto-Light.ttf", 32),
    "i":ImageFont.truetype("Roboto-LightItalic.ttf", 32),
    "b":ImageFont.truetype("Roboto-Regular.ttf", 32),
    "bi":ImageFont.truetype("Roboto-Italic.ttf", 32)
}
REGEX = [
    r"(?<!\\)(\`)[\s\S]*?(?<!\\)\1", # codeblock
    r"(?<!\\)(__|\|\||~~)[\s\S]*?(?<!\\)\1", # unwanted markdowns
    r"(?<!\\)(\*\*)[\s\S]*?(?<!\\)\1", # bold
    r"(?<!\\)([_*])(?!\1| |\n)(?:[^\n](?! \1[^\s\n])|\n(?!\1))+?(?<! |\1|\\)\1" # italic
]
BUBBLE = [
    {"r":50,"w":15},
    {"r":40,"w":13},
    {"r":30,"w":10},
    {"r":20,"w":8},
    {"r":10,"w":5}
]



def draw_box(start,end,col,r,w,draw):
    box_info = [[[
            (start[0],start[1]),
            (start[0]+r*2,start[1]+r*2)
        ],180,270,[
            (start[0]+r,start[1]+w/2-1),
            (end[0]-r,start[1]+w/2-1)
        ]],[[
            (end[0]-r*2,start[1]),
            (end[0],start[1]+r*2)
        ],270,0,[
            (end[0]-w/2,start[1]+r),
            (end[0]-w/2,end[1]-r)
        ]],[[
            (end[0]-r*2,end[1]-r*2),
            (end[0],end[1])
        ],0,90,[
            (end[0]-r,end[1]-w/2+1),
            (start[0]+r,end[1]-w/2+1)
        ]],[[
            (start[0],end[1]-r*2),
            (start[0]+r*2,end[1])
        ],90,180,[
            (start[0]+w/2,end[1]-r),
            (start[0]+w/2,start[1]+r)
        ]]]


    for x in box_info:
        draw.arc(x[0],x[1],x[2],fill=col,width=w)
        draw.line(x[3],fill=col,width=w)

def normal(from_i,to_i,with_i,max_i):
    return (with_i-from_i)*(max_i/(to_i-from_i))

def shade(x,y, size):
    from_col = COL["dark"]
    to_col = COL["black"]

    colour = [0,0,0]
    for i in range(3):
        colour[i] = int((to_col[i]-from_col[i])*y+from_col[i])
    if x < LINE_W/size[0] or x > 1-LINE_W/size[0]:
        return (0)
    elif y < LINE_W/size[1] or y > 1-LINE_W/size[1]:
        return (0)
    

    x = x*size[0]
    y = y*size[1]
    arc_info = [
        {"x":x,"y":y},
        {"x":size[0]-x,"y":y},
        {"x":size[0]-x,"y":size[1]-y},
        {"x":x,"y":size[1]-y}
    ]

    for arc in arc_info:
        x = arc["x"]
        y = arc["y"]
        if x < ARC_R and y < ARC_R:
            if x < ARC_R-sqrt(ARC_R**2-(ARC_R-y)**2):
                return (0)

    return tuple(colour)

def set_markdowns(desc):
    markdowns = []
    new_desc = desc
    for reg in REGEX:
        for x in re.findall(reg, new_desc):
            x = x[0]
            print(x) 
            info = {
                "start":new_desc.find(x),
                "end":new_desc.find(x),
                "type":reg_type(reg)
            } 
            if reg == REGEX[0]:
                info["end"] += len(x[1:-1])
                new_desc.replace(x,"x"*(len(x)-2))
                desc.replace(x,x[1:-1],1)
            elif reg == REGEX[-1]:
                info["end"] += len(x[1:-1])
                new_desc.replace(x,x[1:-1],1)
                desc.replace(x,x[1:-1],1)
            else:
                info["end"] += len(x[2:-2])
                new_desc.replace(x,x[2:-2],1)
                desc.replace(x,x[2:-2],1)
            if reg != REGEX[1]:
                markdowns.append(info)
    #print(new_desc)
    #print(desc)
    return [desc, markdowns]

def reg_type(reg):
    if reg == REGEX[0]: return "null"
    elif reg == REGEX[1]: return "b"
    else: return "i"

def find_width(desc):
    width = 0
    for line in desc.splitlines():
        new_width = sqrt(len(line)/ASPECT)*ASPECT
        if new_width > width:
            width = new_width
    return width

def get_measure_text(desc, width):
    measure_text = ""
    for line in desc.splitlines():
        measure_text += "\n".join(wrap(line, width))
        if line != desc.splitlines()[-1]:
            measure_text += "\n"
    return measure_text

def construct_text(desc, markdowns):
    for mark in markdowns:
        pass


def create_image(task_list):
    # create canvas
    img = Image.new('RGBA', (1000, 1000), (114,137,218,255)) 
    draw = ImageDraw.Draw(img)

    pixels = img.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pixels[x,y] = shade(x/img.size[0],y/img.size[1], img.size)

    draw_box((0,0),img.size,tuple(COL["gray"]),ARC_R,LINE_W,draw)

    # sort tasks
    for task in task_list:
        # get markdowns
        result = set_markdowns(task["task"])
        desc = result[0]
        markdowns = result[1]

        # find width
        width = find_width(desc)

        # measure text
        measure_text = get_measure_text(desc, width)
        
        # apply markdowns
        #task_text = construct_text(desc, markdowns)
        #draw.text((ARC_R/2, ARC_R/2),task_text,COL["text"],font=FONT["n"])
    #print(draw.textsize("R",font=FONT["b"]))
    img.show()





text = [
    {"task":"Hello ***World!\nApples are my favourite food!*** I think you should have some too","sublevel":0}
    #{"task":"Awesome!\nI like apples, I will take 25 please","sublevel":1},
    #{"task":"testing testing","sublevel":0}
]


create_image(text)