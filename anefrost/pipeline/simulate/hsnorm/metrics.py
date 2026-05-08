from IPython.display import Markdown
import tabulate
import json

import anefrost
from anefrost.pipeline.simulate import hsnorm

_all__ = ["game_prob", "hth_table"]

def game_prob(home: int, away: int, nsim: int = 10000) -> float:
    """
    For a game between home and away team, calculate probability that home team wins.

    Args:
        home (int): teamID of home team.
        away (int): teamID of away team.
        nsim (int, optional): Number of simulations to run. Defaults to 10000.
        
    Returns:
        float: Proportion of game simulations home team wins.
    """
    #Generate simulated goal differential estimates.
    sims = [hsnorm.sim_game(home,away) for _ in range(nsim)]

    #If the goal differential is positive, the home team won.
    #Count the number of home wins.
    home_wins = len([1 for i in range(len(sims)) if sims[i]>0])

    return home_wins/nsim

def hth_table(nsim: int = 10000) -> tuple[Markdown,Markdown]:
    """
    Calculate head-to-head game probabilities for all teams.

    Returns:
        Markdown: Formatted table for direct insertion into daily reports.
    """
    teams = anefrost.state.teams
    #Sort alphabetically by abbrevations
    teams = sorted(teams, key = lambda team: anefrost.statelookup.TEAM_IDS[team][-1])
    team_abr = {team: anefrost.statelookup.TEAM_IDS[team][-1] for team in teams}
    res1: list[list[str]] = []
    res2: list[list[str]] = []
    hth_lookup: dict[int, dict[int,float]] = {}
    for home in teams:
        row = [hsnorm.game_prob(home,away, nsim) for away in teams]
        hth_lookup[int(home)] = {int(teams[i]): row[i] for i in range(len(teams))}
        row = [f"{w*100:.2f}%" for w in row]
        res1.append([team_abr[home]] + row[0:16])
        res2.append([team_abr[home]] + row[16:])

    col1 = ["Home"] + list(team_abr.values())[0:16]
    col2 = ["Home"] + list(team_abr.values())[16:]
    tbl1 = tabulate.tabulate(res1, headers = col1)
    tbl2 = tabulate.tabulate(res2, headers = col2)

    #Save head-to-head table to state.
    anefrost.state.hth_table = hth_lookup

    #Save head-to-head table into cached data
    with open(anefrost.CACHE_DIR / "hth_table.json", mode = "w", encoding="utf-8") as file:
        json.dump(hth_lookup, file, indent=2)

    return (Markdown(tbl1), Markdown(tbl2))
