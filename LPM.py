import os
import random
import math
import re
import requests
import emoji
import json
import sys
from datetime import datetime, timedelta
import string

import discord
from dotenv import load_dotenv
from textwrap import wrap

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
client = discord.Client()


VERSION = "0.0.0"



SAVEPATH = sys.argv[0][:sys.argv[0].find("LPM.py")]+"save.json"
LOGPATH = sys.argv[0][:sys.argv[0].find("LPM.py")]+"log.txt"



REACTION_SETUP = ["edit","change_deadline","delete","add_subtask","help"]
EMOJI = {
    "help":"❔",
    "delete":"❌",
    "edit":"✏️",
    "add_subtask":"📎",
    "change_deadline":"⌛",
    "complete":"✅",
    "lock":"🔒",
    "unlock":"🔓",
    "pin":"📌",
    "start":"▶️",
    "info":"ℹ️"
}
data = []




### ON READY
@client.event
async def on_ready():
    global data
    with open(SAVEPATH, "r") as f:
        data = json.load(f)
    print(str(datetime.now())[:19]+" --> Bot Online - "+VERSION)
    write_log("Bot connected to Discord - "+VERSION)
    save()




### MAIN CODE
@client.event
async def on_message(message):
    #info
    global data
    user = message.author
    msgtype = str(message.channel.type)
    #info
    if user == client.user:
        
        return


    if message.content.lower() == "lpm help":
        pass

    elif message.content.lower() == "tasks":
        for task in fetch_tasks("members", user.id):
            task_index = data.index(task)
            task_message = ""
            if task["sublevel"] > 0:
                task_message = f"**Subtask lvl {task['sublevel']}:** "
            task_message += task["task"]
            if task["author"]["id"] != user.id:
                task_message += "\n - " + task["author"]["name"]
            bot_msg = await message.channel.send(task_message)
            data[task_index]["edit"] = bot_msg.id
            
            if task["status"] == "ongoing":
                await bot_msg.add_reaction(EMOJI["start"])
            elif task["status"] == "started":
                await bot_msg.add_reaction(EMOJI["complete"])
            for x in REACTION_SETUP:
                await bot_msg.add_reaction(EMOJI[x])




    if msgtype != "text": return
    write_log(message.content)

    if message.content.lower().find("project") == 0:
        #fetch_tasks("guild", message.guild.id)
        pass

    elif len(re.findall(r"<@[!&]\d+>(?=\W*?\w)", message.content)) > 0:
        info = get_task_info(message.content, message.guild)
        info["edit"] = message.id
        info["author"]["id"] = user.id
        info["author"]["name"] = user.display_name
        data.append(info)
        save()
        for x in REACTION_SETUP:
            await message.add_reaction(EMOJI[x])




@client.event
async def on_reaction_add(reaction, user):
    if user == client.user: return
    command = get_input(reaction.emoji)

    if command == "delete":
        pass # make commands and the "edit_task(task, parameter, edit)" function



def get_input(input_emoji):
    for x in EMOJI:
        if EMOJI[x] == input_emoji:
            return x

def extract_subtasks(all_tasks):
    done = True
    new_tasks = all_tasks

    for task in all_tasks:
        if task["subtasks"] != []:
            done = False
            for x in task["subtasks"]:
                x_index = task["subtasks"].index(x)
                del task["subtasks"][x_index]
                new_tasks.insert(all_tasks.index(task)+1, x)

    if done: return new_tasks
    else: return extract_subtasks(new_tasks)


def fetch_tasks(search_type, search_id):
    global data
    tasks = []
    for task in extract_subtasks(data):
        if search_type == "members":
            if search_id in task[search_type]:
                tasks.append(task)
        elif search_type == "guild" and task[search_type] == search_id:
            tasks.append(task)
    return tasks


def get_task_info(msg, guild):
    task_members = []
    all_mentions = re.findall(r"<@[!&]\d+>", msg)
    new_msg = msg
    task_roles = []
    for mention in all_mentions:
        mention_type = get_type(mention)
        mention_id = int(mention[3:len(mention)-1])
        separation = new_msg[:new_msg.find(mention)]
        if len(re.findall(r"\w+", separation)) > 1: break
        if mention_type == "user":
            if not mention_id in task_members:
                task_members.append(mention_id)
        elif mention_type == "role":
            if mention_id in task_roles: continue
            task_roles.append(mention_id)
            for user in guild.get_role(mention_id).members:
                if not mention_id in task_members:
                    task_members.append(user.id)
        new_msg = new_msg[len(separation)+len(mention):]

    return_dict = {
        "task":re.findall(r"\w[\s\S]*", new_msg)[0],
        "members":task_members,
        "roles":task_roles,
        "author":{"id":0,"name":""},
        "deadline":None,
        "guild":guild.id,
        "pinned":False,
        "locked":False,
        "status":"ongoing",
        "edit":0,
        "sublevel":0,
        "subtasks":[]
    }
    return return_dict

def get_type(mention):
    if mention[2] == "!": return "user"
    elif mention[2] == "&": return "role"

def save():
    global data
    json_data = "[\n"
    for task in data:
        json_data += "   {\n"
        for key in task:
            json_data += '      "'+key+'":'
            #if type(task[key]) is str:
            #    json_data += '"'+str(task[key])+'"'
            #else:
            json_data += str(json.dumps(task[key]))
            json_data += ",\n"
        json_data = json_data[:len(json_data)-2]+"\n    }"
        if task != data[-1]:
            json_data += ",\n"
    json_data += "\n]"
    with open(SAVEPATH, "w") as f:
        f.write(json_data)
    write_log("Updated Save File")

def write_log(log_text):
    with open(LOGPATH, "a") as f:
        f.write(str(datetime.now())+" --> "+log_text+"\n")


client.run(token)