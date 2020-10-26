from constants import *



def png(img):
    b = io.BytesIO()
    img.save(b, "PNG")
    b.seek(0)
    return b

def get_key(value, dictionary): # gets key by its value
    for x in dictionary:
        if dictionary[x] == value:
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

def edit_task(all_tasks, task_id, parameter, value):
    for task in all_tasks:
        if task["edit"] == task_id:
            if parameter == "delete":
                del all_tasks[all_tasks.index(task)]
            elif parameter == "fetch":
                return task
            else:
                task[parameter] = value
            return
        if len(task["subtasks"]) > 0:
            return_value = edit_task(task["subtasks"], task_id, parameter, value)
            if return_value != None:
                return return_value
    return

def task_info_from_message(msg, guild):
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
        "working":0,
        "editing":0,
        "edit_status":"",
        "roles":task_roles,
        "author":{"id":0,"name":""},
        "deadline":None,
        "guild":guild.id,
        "pinned":False,
        "locked":False,
        "status":"pending",
        "edit":0,
        "last_edit":0,
        "sublevel":0,
        "subtasks":[]
    }
    return return_dict

def get_type(mention):
    if mention[2] == "!": return "user"
    elif mention[2] == "&": return "role"

def write_log(log_text):
    with open(LOGPATH, "a") as f:
        f.write(str(datetime.now())+" --> "+log_text+"\n")

def chop_microseconds(delta):
    return delta - timedelta(microseconds=delta.microseconds)
