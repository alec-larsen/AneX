import anefrost
from anefrost.pipeline import compiler

def team_summaries() -> float:
    """
    Compile all cleaned play-by-play data on system into team-level statistical summaries
    and print process runtime.
    """
    t, _ = anefrost.time_func(compiler.compile_team_summaries)

    return t

def game_slates():
    """
    Partition data for last 41 home and away games for each team. Print process runtime.

    Returns:
        float: Process runtime (seconds)
    """
    t, _ = anefrost.time_func(compiler.recent_games)
    return t
