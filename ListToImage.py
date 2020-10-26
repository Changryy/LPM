from PIL import Image, ImageDraw, ImageFont
from math import sqrt

COL = {  # Discord colours
    "blue": (114, 137, 218),
    "white": (255, 255, 255),
    "text": (240, 245, 255),
    "gray": (153, 170, 181), 
    "dark": (54, 57, 63),
    "black": (35, 39, 42)
}

def draw_box(start, end, col, r, w, draw):
    box_info = [[[
        (start[0], start[1]),
        (start[0] + r * 2, start[1] + r * 2)
    ], 180, 270, [
        (start[0] + r, start[1] + w / 2 - 1),
        (end[0] - r, start[1] + w / 2 - 1)
    ]], [[
        (end[0] - r * 2, start[1]),
        (end[0], start[1] + r * 2)
    ], 270, 0, [
        (end[0] - w / 2, start[1] + r),
        (end[0] - w / 2, end[1] - r)
    ]], [[
        (end[0] - r * 2, end[1] - r * 2),
        (end[0], end[1])
    ], 0, 90, [
        (end[0] - r, end[1] - w / 2 + 1),
        (start[0] + r, end[1] - w / 2 + 1)
    ]], [[
        (start[0], end[1] - r * 2),
        (start[0] + r * 2, end[1])
    ], 90, 180, [
        (start[0] + w / 2, end[1] - r),
        (start[0] + w / 2, start[1] + r)
    ]]]

    for x in box_info:
        draw.arc(x[0], x[1], x[2], fill=col, width=w)
        draw.line(x[3], fill=col, width=w)

interpolate = lambda from_i, to_i, with_i: (to_i - from_i) * with_i + from_i

def shade(x, y, size, outline_width, corner_radius):
    from_col = COL["dark"]
    to_col = COL["black"]

    colour = [0, 0, 0]
    for i in range(3):
        colour[i] = int(interpolate(from_col[i], to_col[i], y))
    if x < outline_width / size[0] or x > 1 - outline_width / size[0]:
        return (0)
    elif y < outline_width / size[1] or y > 1 - outline_width / size[1]:
        return (0)

    x = x * size[0]
    y = y * size[1]
    arc_info = [
        {"x": x, "y": y},
        {"x": size[0] - x, "y": y},
        {"x": size[0] - x, "y": size[1] - y},
        {"x": x, "y": size[1] - y}
    ]

    for arc in arc_info:
        x = arc["x"]
        y = arc["y"]
        if x < corner_radius and y < corner_radius:
            if x < corner_radius - sqrt(corner_radius ** 2 - (corner_radius - y) ** 2):
                return (0)

    return tuple(colour)


def create_background(size, outline_width, corner_radius):
    img = Image.new('RGBA', size, 0)
    draw = ImageDraw.Draw(img)

    pixels = img.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pixels[x, y] = shade(x / img.size[0], y / img.size[1], img.size, outline_width, corner_radius)

    draw_box((0, 0), img.size, tuple(COL["blue"]), corner_radius, outline_width, draw)

    return img

def image_from_list(task_list, text_font, image_name, margin = 5, outline_width = 10, corner_radius = 30, spacing = 5, indent_space = 4, text_size = 15, text_color = (0,0,0), bg_image = None):
    writing_list = []
    image_min_size = [0,0]

    font = ImageFont.truetype(text_font, text_size) #Sets the font

    for task in task_list:
        task_string = "" #Will contain the line to print
        for indent in range(0,task["sublevel"]): #Loop for each indentation
            for space in range(0, indent_space): #Loop for each amount of spaces per indentation
                task_string += " " #Add space to the string
        if task["sublevel"] > 0: #Add circle in beggining if task is a sublevel
            task_string += "○"
        task_string += task["task"] #Add the name of the task to the string
        writing_list.append(task_string) #Append it to a list with all the tasks strings
        line_size = font.getsize(task_string) #Get the size of the line
        width = line_size[0]
        image_min_size[1] += line_size[1] + spacing #Add to the vertical image size
        if width > image_min_size[0]: #Check to get the widest line which will be the images width
            image_min_size[0] = width

    image_size = (image_min_size[0] + (outline_width+ margin)*2, image_min_size[1] + (outline_width+ margin)*2)
    img = create_background(image_size, outline_width, corner_radius)
    draw = ImageDraw.Draw(img)

    y_pos = outline_width + margin
    vertical_separation = image_min_size[1]/len(writing_list)
    for line in writing_list: #Draw each line
        draw.text((outline_width + margin, y_pos), line, font = font, fill = text_color)
        y_pos += vertical_separation

    return img
    #img.save(image_name)

#Test list#
tasks_test = [
    {"task": "Clean up", "sublevel": 0},
    {"task": "Bedroom", "sublevel": 1},
    {"task": "Livingroom", "sublevel": 1},
    {"task": "Study", "sublevel": 0},
    {"task": "Math", "sublevel": 1},
    {"task": "Caclulus", "sublevel": 2},
    {"task": "Algebra", "sublevel": 2},
    {"task": "Physics", "sublevel": 1},
    {"task": "Optics", "sublevel": 2},
    {"task": "Nuclear Physics", "sublevel": 2},
]

#Actual code
image_from_list(tasks_test, "Encryption.ttf", "TestImage.png", text_size = 30, text_color = COL["text"]).show()