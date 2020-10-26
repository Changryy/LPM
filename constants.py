from imports import *



# ---------- DISCORD ---------- #
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
client = discord.Client()
# ---------- DISCORD ---------- #



# ---------- SYSTEM ---------- #
ROOT = sys.argv[0][:sys.argv[0].find("LPM.py")]

SAVEPATH = ROOT+"save.json"
LOGPATH = ROOT+"log.txt"
# ---------- SYSTEM ---------- #



# ---------- REACTION SETUP ---------- #
MINIMAL_SETUP = ["edit","add_subtask"]
NORMAL_SETUP = ["edit","change_deadline","add_subtask","help"]
MAXIMUM_SETUP = ["edit","change_deadline","add_subtask","pin","lock","info","help"]
QUESTION_SETUP = ["complete","cancel"]
EDIT_SETUP = ["edit","change_deadline","delete","cancel"]
# ---------- REACTION SETUP ---------- #



# ---------- REACTION COMMANDS ---------- #
EMOJI = {
    "help":"❔",
    "delete":"🗑️",
    "cancel":"❎",
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
# ---------- REACTION COMMANDS ---------- #




# ---------- MESSAGES ---------- #
BOT = {
    "delete":"**Are you sure you want to delete this task?**",
    "deleted":"*The task has been deleted.*",
    "authority":"*You are not authorised to use this function.*",
    "no_tasks":"*You do not have any tasks.*",
    "dedication":"*This task is not dedicated to you.*",
    "worker":"*You are not working on this task.*",
    "unavailable":"*This feature is unavailable at the moment.*",
    "complete":"**Are you sure this task has been completed?**",
    "completed":"*Task completed!*",
    "started":"*Task assigned.*",
    "edit":"**What would you like to edit?**\n"+EMOJI["edit"]+" - Text\n"+EMOJI["change_deadline"]+" - Deadline\n"+EMOJI["delete"]+" - Delete Task\n"+EMOJI["cancel"]+" - Cancel",
    "time":"**How much time will you spend on this task?** (Update this often for better recommendations)",
    "deadline":"**When should this task be finished?**",
    "text":"**Write the new task text:**",
    "subtask":"**Write what the new subtask should be:**",
    "nonexistent":"*Could not find any task by that number.*"
}
# ---------- MESSAGES ---------- #



# ---------- SETTINGS ---------- #
PERMS = {
    "member":["add_subtask","change_deadline","start","edit"],
    "author":["delete","change_deadline","add_subtask","pin","unlock","lock","edit"]
}
# ---------- SETTINGS ---------- #
