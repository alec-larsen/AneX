import anefrost
from anefrost.pipeline import clean

__all__ = ["clean_pbp"]

def clean_pbp() -> float:
    """
    Clean all raw play-by-play data on system and print process runtime.
    """
    #Get time (in seconds) for [rep] calls of this function.
    t, _ = anefrost.time_func(clean.clean_all_pbp)
    return t
