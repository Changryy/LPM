from PIL import Image, ImageFont, ImageDraw
from string2md import md
from textwrap import wrap
from math import sqrt

# ---------- DISCORD COLOURS ---------- #

COL = {
    "blue":[114,137,218],
    "white":[255,255,255],
    "gray":[153,170,181],
    "dark":[44,47,51],
    "black":[35,39,42],
    "codeblock":(0,0,0),
    "text":(230,230,230),
    "spoiler":(100,100,100),
    "strikethrough":(230,230,230),
    "underline":(230,230,230),
}

# ---------- DISCORD COLOURS ---------- #





# ---------- SETTINGS ---------- #

BORDER = 64
LINE_W = 32
ARC_R = 64
FONT_SIZE = 64
STRIKE_W = 0.05
RATIO = 4

# ---------- SETTINGS ---------- #



# ---------- FONTS ---------- #

FONT = {
    "":ImageFont.truetype("Roboto-Light.ttf", FONT_SIZE),
    "i":ImageFont.truetype("Roboto-LightItalic.ttf", FONT_SIZE),
    "b":ImageFont.truetype("Roboto-Regular.ttf", FONT_SIZE),
    "bi":ImageFont.truetype("Roboto-Italic.ttf", FONT_SIZE)
}

# ---------- FONTS ---------- #




# ---------- LAMBDA FUNCTIONS ---------- #

normal = lambda from_i, to_i, with_i, max_output = 1.0: (with_i - from_i) * (max_output / (to_i - from_i))
interpolate = lambda from_i, to_i, with_i: (to_i - from_i) * with_i + from_i
multilined = lambda line: line["text"].count("\n") > 0

# ---------- LAMBDA FUNCTIONS ---------- #




# ---------- TEXT WRAPPING ---------- #

def ratio(ratio_text):
    img = Image.new('RGBA', (1,1)) 
    draw = ImageDraw.Draw(img)
    w, h = draw.multiline_textsize(ratio_text, font=FONT["b"])
    return w/h

def wrapping_reference(text):
    text = "".join([x["text"] for x in text])

    reference = text

    wp = len(text)
    while ratio(reference) > RATIO:
        wp -= 1
        reference = ""
        for line in text.split("\n"):
            reference += "\n".join(wrap(line,wp,replace_whitespace=False))
            if line != text.split("\n")[-1]: reference += "\n"

    return reference

def wrap_text(text):
    reference = wrapping_reference(text)

    for x in text: x["text"] = x["text"].replace("\n"," ")

    for x in range(reference.count("\n")):
        pos = reference.find("\n")+x
        reference = reference.replace("\n","X",1)

        for x in text:
            if len(x["text"]) >= pos:
                if x is text[-1] and len(x["text"])-1 == pos: break
                x["text"] = x["text"][:pos+1]+"\n"+x["text"][pos+1:]
                break
            pos -= len(x["text"])
        
        if text[-1]["text"][-1] == "\n":
            text[-1]["text"] = text[-1]["text"][:-1]

    return text

# ---------- TEXT WRAPPING ---------- #


def write(text, draw):
    y = draw.textsize("X", font=FONT[""])[1] +4

    position = (BORDER,BORDER/10*8)

    for line in text:

        ###
        font_type = ""
        if "bold" in line["type"]: font_type += "b"
        if "italic" in line["type"]: font_type += "i"
        ###


        line_split = line["text"].split("\n")
        x = draw.textsize(line_split[-1], font=FONT[font_type])[0]



        for a in [("codeblock",y),("spoiler",y),("underline",FONT_SIZE*STRIKE_W),("strikethrough",FONT_SIZE*STRIKE_W)]:

            start = (position[0], position[1] + FONT_SIZE/3*2)
            if a[0] == "underline": start = (start[0], start[1] + FONT_SIZE/3)
            if a[0] in line["type"]:
                for l in line_split:
                    end = (start[0]+draw.textsize(l, font=FONT[font_type])[0], start[1])
                    draw.line((start, end), fill=COL[a[0]], width=int(a[1]))
                    start = (BORDER, start[1] + y)


        ###
        draw.multiline_text(position, line_split[0], font=FONT[font_type], fill=COL["text"], )
        if multilined(line): draw.multiline_text((BORDER, position[1] + y), line["text"][len(line_split[0])+1:], font=FONT[font_type], fill=COL["text"])
        ###


        h = draw.multiline_textsize(line["text"], font=FONT[font_type])[1]


        if multilined(line): position = (BORDER, position[1])
        position = (position[0] + x, position[1] + (h - y + 4))


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


def shade(x,y, size):
    from_col = COL["dark"]
    to_col = COL["black"]

    colour = [0,0,0]
    for i in range(3):
        colour[i] = int(interpolate(from_col[i], to_col[i], y))
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


def create_bubble(text):
    text = wrap_text(md(text))

    img = Image.new('RGBA', (1,1)) 
    draw = ImageDraw.Draw(img)
    size_x, size_y = draw.multiline_textsize("".join([x["text"] for x in text]),font=FONT["b"])
    size = (size_x+BORDER*2,size_y+BORDER*2)

    img = Image.new('RGBA', size)
    draw = ImageDraw.Draw(img)

    pixels = img.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pixels[x,y] = shade(x/img.size[0],y/img.size[1], img.size)

    draw_box((0,0),img.size,tuple(COL["gray"]),ARC_R,LINE_W,draw)

    write(text, draw)

    return img
