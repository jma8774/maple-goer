import pytz
from datetime import datetime

def dtFormat(dt: datetime):
  return dt.astimezone(pytz.timezone('America/New_York')).strftime('%I:%M %p').lstrip('0')

def secondsToDisplay(secs: int):
    hours = int(secs // 3600)
    mins = int((secs % 3600) // 60)
    s = ""
    if hours > 0:
        s += f"{hours} {'hours' if hours > 1 else 'hour'} "
    if mins > 0:
        s += f"{mins} {'minutes' if mins > 1 else 'minute'} "
    return s.strip()