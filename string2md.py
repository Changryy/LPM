import re
import string
from copy import deepcopy

REGEX = [ # Just read "type" if you wonder what these regex patterns search for
    {"type": "codeblock", "re": r"((?<!\\)(\`)[\s\S]*?(?<!\\)\2)"},
    {"type": "strikethrough", "re": r"((?<!\\)(~~)[\s\S]*?(?<!\\)\2)"},
    {"type": "spoiler", "re": r"((?<!\\)(\|\|)[\s\S]*?(?<!\\)\2)"},
    {"type": "underline", "re": r"((?<!\\)(__)[\s\S]*?(?<!\\)\2)"},
    {"type": "bold", "re": r"((?<!\\)(\*\*)[\s\S]*?(?<!\\)\2)"}, # the one under this one took a lot of time to make
    {"type": "italic", "re": r"((?<!\\)([_*])(?!\2| |\n)(?:[^\n](?! \2[^\s\n])|\n(?!\2))+?(?<! |\2|\\)\2)"} # yet it still isnt perfect
]


def md(text): # Converts string to a list with a "Markdown Document"-like format
    full_text = text # stores input string for later uses
    stamps = [] # stores result of the first phase
    converted_text = [] # stores the end result

    # Phase 1: Find Special Text
    for i in range(len(REGEX)): # go through every type of markdown
        for match in re.findall(REGEX[i]["re"], text): # find every line with that markdown
            line = match[0] # of course "line" doesnt have to be a line, it can be a sentence or perhaps a word
            span = (text.find(line), text.find(line)+len(line))
            k = len(match[1]) # number of key markdown characters (will just be called k from now on)

            if i == 0: # if codeblock: replace line
                text = text.replace(line, "x"*len(line), 1)
            else: # else: replace key markdown characters
                text = text.replace(line, "x"*k+line[k:-k]+"x"*k, 1)

            stamps.append({"span": span, "type": REGEX[i]["type"], "k": k})



    # Phase 2: Re-assemble Text

    span = [0, len(full_text)] # span of the new_item["text"] based on full_text
    new_item = {"text": full_text, "type": []} # converted_text item template
    current_stamps = [] # stamps used for the current item (in the loop below)

    while True:
        ending_stamp = {"k":0} # template for the "ending_stamp" (if there is any)
        new_item["type"] = [] # default item type
        span[1] = len(full_text) # default item end position

        if len(current_stamps) > 0:
            new_item["type"] = [x["type"] for x in current_stamps] # assign types for the item
            ending_stamp = min(current_stamps, key=lambda x: x["span"][1]) # set "ending_stamp" as the stamp that ends first
            span[1] = ending_stamp["span"][1] # set the item end as the "endings_stamp" end



        ending = True # will be set to False if a new stamp is introduced
        if len(stamps) > 0: # if there are any stamps that havent been introduced yet:
            next_stamp = min(stamps, key=lambda x: x["span"][0]) # set "next_stamp" to the stamp that gets introduced next

            if next_stamp["span"][0] < span[1]: # if the "next_stamp" starts before the current ends:
                current_stamps.append(next_stamp.copy()) # append "next_stamp" to "current_stamps"
                span[1] = next_stamp["span"][0] # set the new item end as the "next_stamp" start
                del stamps[stamps.index(next_stamp)] # delete "next_stamp" from "stamps" as it now has been moved to "current_stamps"
                ending = False # told you it would be set to False

        new_item["text"] = full_text[span[0]:span[1]] # assign the item text

        if ending: # if a stamp is ending:
            if len(current_stamps) > 0:
                del current_stamps[current_stamps.index(ending_stamp)] # delete "ending_stamp" from "current_stamps"
            if ending_stamp["k"] > 0:
                new_item["text"] = new_item["text"][0:-ending_stamp["k"]] # set the ending offset to ending_stamp["k"]

        
        if len(new_item["text"]) > 0: converted_text.append(deepcopy(new_item)) # append the item to "converted_text" unless its empty

        span[0] = span[1] # set the next item start as the current end
        if not ending: span[0] += next_stamp["k"] # if no stamp is ending, add next_stamp["k"] to the next item start

        if span[1] == len(full_text)-ending_stamp["k"]: break # end loop if the span ends at the same position as the "full_text" ends
    
    return converted_text # Im tired of all the commenting...
