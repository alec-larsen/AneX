import datetime

__all__ = ["now", "durstr"]

def now() -> str:
    """
    Build timestamp of current local time

    Returns:
        str: formatted timestamp
    """
    t = datetime.datetime.now()
    return f"[{datetime.date.strftime(t, "%H:%M:%S")}]"

def durstr(t: float) -> str:
    """
    Build duration string given number of seconds elapsed

    Args:
        t (float): Runtime of process

    Returns:
        str: Formatted string for elapsed time
    """
    dur = ""
    h = int(t//3600)
    t = t - h*3600
    if h > 0:
        dur += f"{h}h"

    m = int(t//60)
    t = t - m*60
    if m>0 or h>0:
        if h>0:
            dur += f"{m}".zfill(2) + "m"
        else:
            dur += f"{m}m"
    if m > 0 or h > 0:
        dur += f"{round(t)}s"

    else:
        dur += f"{t:.3f}s"

    return dur
