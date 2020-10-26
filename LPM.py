from functions import *


VERSION = "0.0.0"

data = []

open_tasks = {}

### ON READY
@client.event
async def on_ready():
    global data
    with open(SAVEPATH, "r") as f:
        data = json.load(f)
    print(str(datetime.now())[:19]+" --> Bot Online - "+VERSION)
    write_log("Bot connected to Discord - "+VERSION)
    save()


# ---------------------------------------------------



### MAIN CODE
@client.event
async def on_message(message):
    #info
    global data
    user = message.author
    msgtype = str(message.channel.type)
    #info
    if user == client.user: return




# ---- test ---- #

#    x = time(message.content)

#    if isinstance(x, str):
#        if str(time(message.content)) != "Invalid input.":
#            await message.channel.send(x)
#    else:
#        y = chop_microseconds(x - datetime.utcnow())
#        x = x.strftime("%c")
#        await message.channel.send(f"{x} UTC\n{y} left")


# ---- test ---- #


    #await message.channel.send(user.display_name+":", file=discord.File(png(create_bubble(message.clean_content)), "message.png"))
    #await message.delete()
# ---- test ---- #




    return

    if message.content.lower() == "lpm help":
        bot_msg = await message.channel.send(BOT["unavailable"]) # REPLACE LINE
        await bot_msg.delete(delay=5)
        return

    elif message.content.lower() == "tasks":
        user_tasks = fetch_tasks("members", user.id)
        if len(user_tasks) == 0: # send error if user has no tasks
            bot_msg = await message.channel.send(BOT["no_tasks"])
            await bot_msg.delete(delay=5)
            return

        open_tasks[message.channel.id] = user_tasks

        for task in user_tasks:
            task_message = ""
            if task["sublevel"] > 0:
                task_message = f"**Subtask lvl {task['sublevel']}:** "
            task_message += task["task"]
            if task["author"]["id"] != user.id:
                task_message += "\n - " + task["author"]["name"] 
            bot_msg = await message.channel.send(task_message)
            try:
                prev_msg = await message.channel.fetch_message(task["edit"])
                await prev_msg.clear_reactions()
            except: pass
            edit_task(data, task["edit"], "edit", bot_msg.id)

            if task["status"] == "pending":
                await bot_msg.add_reaction(EMOJI["start"])
            elif task["status"] == "started":
                await bot_msg.add_reaction(EMOJI["complete"])
            for x in MINIMAL_SETUP:
                await bot_msg.add_reaction(EMOJI[x])
        return


    elif re.fullmatch(r"task ?\d+", message.content.lower()):
        try:
            len(open_tasks[])


    if msgtype != "text": return
    write_log(message.content)

    if message.content.lower().find("project") == 0:
        #fetch_tasks("guild", message.guild.id)
        await message.channel.send(BOT["unavailable"]) # REPLACE LINE


    elif len(re.findall(r"<@[!&]\d+>(?=\W*?\w)", message.content)) > 0:
        info = task_info_from_message(message.content, message.guild)
        info["edit"] = message.id
        info["author"]["id"] = user.id
        info["author"]["name"] = user.display_name
        data.append(info)
        save()
        await message.add_reaction(EMOJI["start"])
        for x in MINIMAL_SETUP:
            await message.add_reaction(EMOJI[x])



# ---------------------------------------------------



@client.event
async def on_reaction_add(reaction, user):
    command = get_key(reaction.emoji, EMOJI)
    msg = reaction.message
    task = edit_task(data, msg.id, "fetch", 0)
    topic = get_key(msg.content, BOT)
    remap = False

    if task == None or command == None or user == client.user: return
    await msg.clear_reactions()


    # bot questions
    if topic != None and user.id == task["editing"] and task["edit_status"] == "menu":
        edit_task(data, msg.id, "edit_status", "")
        
        if topic == "delete":
            if command == "complete":
                edit_task(data, msg.id, "delete", 0)
                bot_msg = await msg.channel.send(BOT["deleted"])
                await msg.delete()
                try:
                    last_msg = await msg.channel.fetch_message(task["last_edit"])
                    await last_msg.delete()
                except: pass
                await bot_msg.delete(delay=5)
                save()
                return
            elif command == "cancel":
                edit_task(data, msg.id, "edit", task["last_edit"])
                remap = True
                await msg.delete()

        elif topic == "complete":
            if command == "complete":
                edit_task(data, msg.id, "status", "completed")
                bot_msg = await msg.channel.send(BOT["completed"])
                await msg.delete()
                try:
                    last_msg = await msg.channel.fetch_message(task["last_edit"])
                    await last_msg.delete()
                except: pass
                await bot_msg.delete(delay=5)
                save()
                return
            elif command == "cancel":
                edit_task(data, msg.id, "edit", task["last_edit"])
                remap = True
                await msg.delete()

        elif topic == "edit":
            if command == "edit":
                remap = True
                edit_task(data, msg.id, "edit", task["last_edit"])
                await msg.delete()
                bot_msg = await msg.channel.send(BOT["unavailable"]) # REPLACE LINE
                await bot_msg.delete(delay=5)
            elif command == "change_deadline":
                remap = True
                edit_task(data, msg.id, "edit", task["last_edit"])
                await msg.delete()
                bot_msg = await msg.channel.send(BOT["unavailable"]) # REPLACE LINE
                await bot_msg.delete(delay=5)
            elif command == "delete":
                await msg.delete()
                bot_msg = await msg.channel.send(BOT[command])
                edit_task(data, msg.id, "edit_status", "menu")
                edit_task(data, msg.id, "edit", bot_msg.id)
                for x in QUESTION_SETUP:
                    await bot_msg.add_reaction(EMOJI[x])
                save()
                return
            elif command == "cancel":
                edit_task(data, msg.id, "edit", task["last_edit"])
                remap = True
                await msg.delete()
    #elif topic != None and task["edit_status"] == "menu":


    # commands for everyone
    if not remap:
        if command == "help":
            remap = True
            bot_msg = await msg.channel.send(BOT["unavailable"]) # REPLACE LINE
            await bot_msg.delete(delay=5)

        elif command == "info":
            remap = True
            bot_msg = await msg.channel.send(BOT["unavailable"]) # REPLACE LINE
            await bot_msg.delete(delay=5)

    # check if participant
    participating = False
    for role in task["roles"]:
        for user_role in user.roles:
            if user_role.id == role:
                participating = True
    for member in task["members"]:
        if user.id == member:
            participating = True

    if not participating:
        if command in PERMS["member"]:
            remap = True
            bot_msg = await msg.channel.send(BOT["dedication"])
            await bot_msg.delete(delay=5)


    # Commands for the participant
    elif not remap:
        if command == "start" and task["status"] == "pending":
            remap = True
            edit_task(data, msg.id, "working", user.id)
            edit_task(data, msg.id, "status", "started")
            bot_msg = await msg.channel.send(BOT["started"])
            await bot_msg.delete(delay=5)

        elif command == "complete" and task["status"] == "started":
            if user.id == task["working"]:
                bot_msg = await msg.channel.send(BOT[command])
                edit_task(data, msg.id, "edit_status", "menu")
                edit_task(data, msg.id, "editing", user.id)
                edit_task(data, msg.id, "last_edit", task["edit"])
                edit_task(data, msg.id, "edit", bot_msg.id)
                for x in QUESTION_SETUP:
                    await bot_msg.add_reaction(EMOJI[x])
                save()
                return

            else:
                remap = True
                bot_msg = await msg.channel.send(BOT["worker"])
                await bot_msg.delete(delay=5)
        
        elif command == "edit":
            if user.id == task["working"] or user.id == task["author"]["id"]:
                bot_msg = await msg.channel.send(BOT["edit"])
                
                edit_task(data, msg.id, "edit_status", "menu")
                edit_task(data, msg.id, "last_edit", msg.id)
                edit_task(data, msg.id, "editing", user.id)
                edit_task(data, msg.id, "edit", bot_msg.id)
                for x in EDIT_SETUP:
                    await bot_msg.add_reaction(EMOJI[x])
                return
            else:
                remap = True
                bot_msg = await msg.channel.send(BOT["worker"])
                await bot_msg.delete(delay=5)


    # commands for the task managers
    if (user.id == task["author"]["id"] or participating) and not remap:
        if command == "add_subtask":
            remap = True
            #bot_msg = await msg.channel.send(BOT["subtask"])
            #edit_task(data, msg.id, "edit_status", "menu")
            #edit_task(data, msg.id, "last_edit", msg.id)
            #edit_task(data, msg.id, "e", user.id)
            bot_msg = await msg.channel.send(BOT["unavailable"]) # REPLACE LINE
            await bot_msg.delete(delay=5)

        elif command == "change_deadline":
            remap = True
            bot_msg = await msg.channel.send(BOT["unavailable"]) # REPLACE LINE
            await bot_msg.delete(delay=5)


    # check if author
    if user.id != task["author"]["id"] and not remap:
        if command in PERMS["author"]:
            remap = True
            bot_msg = await msg.channel.send(BOT["authority"])
            await bot_msg.delete(delay=5)


    # Commands for the task author
    elif not remap:

        if command == "edit":
            bot_msg = await msg.channel.send(BOT["edit"])
            edit_task(data, msg.id, "edit_status", "menu")
            edit_task(data, msg.id, "last_edit", msg.id)
            edit_task(data, msg.id, "editing", user.id)
            edit_task(data, msg.id, "edit", bot_msg.id)
            for x in EDIT_SETUP:
                await bot_msg.add_reaction(EMOJI[x])
            return


    if remap:
        try:
            if topic != None:
                msg = await msg.channel.fetch_message(task["edit"])
            await msg.clear_reactions()
            if task["status"] == "pending":
                await msg.add_reaction(EMOJI["start"])
            elif task["status"] == "started":
                await msg.add_reaction(EMOJI["complete"])
            for x in MINIMAL_SETUP:
                await msg.add_reaction(EMOJI[x])
        except: pass
    save()



# ---------------------------------------------------

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



client.run(token)