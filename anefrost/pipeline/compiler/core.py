import json
import os

import pandas as pd

import anefrost
from anefrost.pipeline.compiler.game import Game

__all__ = ["compile_team_summaries", "recent_games"]

def compile_team_summaries() -> None:
    """
    Compile team-level statistics for all games in dataset into a single dataframe.
    
    Returns:
        pd.DataFrame: Final dataframe of compiled summaries.
    
    Notes:
        This function will assume that all cleaned data has been checked for valid structure (namely non-empty list of plays)
    """

    #Get list of ids for all games present in cleaned data.
    game_ids = os.listdir(anefrost.CLEAN_DIR)

    #Build Game wrappers for each game_id
    games = [Game(int(game_id[:-5])) for game_id in game_ids]

    #Compile team-level summary stats for each game and package list of series into a dataframe
    df = pd.DataFrame([game.team_summary() for game in games])

    path = anefrost.COMPILED_DIR /"team_statistics.json"

    df.to_json(path, date_format = 'iso', date_unit='s', compression = None, indent=2) #type: ignore - Pylance cannot recognize that this should always return None

def recent_games() -> None:
    with open(anefrost.COMPILED_DIR / "team_statistics.json", mode="r", encoding="utf-8") as file:
        data = json.load(file)
        data = pd.DataFrame(data)

    anefrost.state.teams = data["home_team"].unique()

    for team in anefrost.state.teams:
        home_games: pd.DataFrame = data[data["home_team"] == team] #type: ignore
        away_games: pd.DataFrame = data[data["away_team"] == team] #type: ignore
        home_games = home_games.nlargest(41, "game_id")[anefrost.state.model_params] #type: ignore
        away_games = away_games.nlargest(41, "game_id")[anefrost.state.model_params] #type: ignore

        path = anefrost.COMPILED_DIR

        home_games.to_json(path/f"{team}h.json", date_format = 'iso', date_unit='s', compression = None, indent=2) #type: ignore
        away_games.to_json(path/f"{team}a.json", date_format = 'iso', date_unit='s', compression = None, indent=2) #type: ignore
