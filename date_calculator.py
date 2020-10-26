from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
import re

TIME_REG = {
    "years": r"(\d+) ?y(?:ear)?s?(?![A-z])",
    "months": r"(\d+) ?m(?:onth)?s?(?![A-z])",
    "weeks": r"(\d+) ?w(?:eak)?s?(?![A-z])",
    "days": r"(\d+) ?d(?:ay)?s?(?![A-z])",
    "hours": r"(\d+) ?h(?:our)?s?(?![A-z])",
    "minutes": r"(\d+) ?min(?:ute)?s?(?![A-z])",
    "seconds": r"(\d+) ?s(?:econd|ec)?s?(?![A-z])"
}

TIME = r"(?:(?:\d+) ?(?:y(?:ear)?|m(?:onth)?|w(?:eek)?|d(?:ay)?|h(?:our)?|min(?:ute)?|s(?:econd|ec)?)s?,?(?: ?and)? ?){1,7}\.?"



def wait(wait_time):
    if not re.fullmatch(TIME, wait_time): return False
    y,m,w,d,h,mi,s = [float(x.group(1)) if x else 0 for x in [re.search(TIME_REG[x], wait_time) for x in TIME_REG]]
    x = datetime.utcnow() + relativedelta(years=y,months=m,weeks=w,days=d,hours=h,minutes=mi,seconds=s)
    return x



def time(time):
    try:
        x = int(time)
        return "Invalid input."
    except ValueError: pass
    x = wait(time)
    if not x:
        try: x = parse(time)
        except: return "Invalid input."
    if x < datetime.utcnow(): return "Cannot assign a date from the past."
    else: return x
