import datetime
from typing import Any

import anefrost

__all__ = ["ALL_GAME_IDS"]

def _gtd(today: datetime.date = datetime.date.today()) -> int:
    """
    Find number of games up to, but not including, today for the current season.

    Returns:
        int: Number of games that have occurred so far in the NHL regular season.
    """
    date = today - datetime.timedelta(days=1)
    sched_json: dict[str, Any] = {"gameWeek": []}
    while True:
        day = str(date) #Start with yesterday's date to check for games
        week = [d["date"] for d in sched_json["gameWeek"]]

        #Only pull new game week from NHL API when needed (when day falls out of range of current week)
        if day not in week:
            #This gives us a dictionary of the week of games containing day.
            sched_json = anefrost.request_json(f"https://api-web.nhle.com/v1/schedule/{day}")

        #Obtain only the game data for the specified day.
        #List comprehension generates a list with one element, so we take [0] to access it.
        day_data = [d for d in sched_json["gameWeek"] if d["date"] == day][0]

        #Get all regular season games that were played on day
        #Our regular season games to date will all have '02' as their middle two digits.
        #[id] // 10000 yields the first six digits and taking this result modulo 100 leaves us the middle two
        regular_games = [game for game in day_data["games"] if (game["id"] // 10000) % 100 == 2]

        #Verify that at least one regular season game occurred on day.
        #Provided this is true, games to date can be derived from the maximum game_id for the day.
        if regular_games:
            #Since last four digits of game_id represent regular season order, largest game_id is most recent game.
            #Find maximum game_id in day's game data (for only regular season games)
            max_game_id = max([game["id"] for game in regular_games])

            #Last four digits of maximum game_id yield number of games that have happened so far in the regular season.
            return max_game_id % 10000

        #If the game list was empty, move to the previous day to check for games.
        date = date - datetime.timedelta(days=1)

#Set of all game ids that should be present in any game data set.
ALL_GAME_IDS = list(range(2024020001,2024021313)) + list(range(2025020001,2025020001+_gtd()))
