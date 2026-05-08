import json
import os
from typing import Any

import anefrost
from anefrost.pipeline.clean import constants

__all__ = ["clean_all_pbp"]

def clean_play_list(plays: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Flatten each play dictionary in list of plays, leaving only key information.

    Args:
        plays (list[dict[str, Any]]): List of plays from game to be cleaned

    Returns:
        list[dict[str, Any]]: Cleaned list of plays; Pandas dataframe compatible
    """

    plays = [{
        "eventId": play["eventId"],
        "type": play["typeCode"],
        "x": -play["details"]["xCoord"] if play["homeTeamDefendingSide"] == "Right" else play["details"]["xCoord"], #Modifed such that home team always shoots on positive x-coordinate net.
        "y": play["details"]["yCoord"],
        #Not every event type has/needs additional details. Assign all details of events without a specified details field to None
        "details": (play["details"][constants.DETAIL_KEYS[play["typeCode"]]] if constants.DETAIL_KEYS.get(play["typeCode"]) is not None and 
                    play["details"].get(constants.DETAIL_KEYS.get(play["typeCode"])) is not None else None),
        #Consolidate all fields involving main player in given play into one key.
        #Some plays may not have main players.
        #Bench minor penalties are not listed as committed by a single player (rather they're served by a specific player). We do not count these against said player.
        "mainPlayer": (play["details"][constants.MAIN_PLAYER_KEYS[play["typeCode"]]] if constants.MAIN_PLAYER_KEYS.get(play["typeCode"]) is not None and
                       play["details"].get(constants.MAIN_PLAYER_KEYS.get(play["typeCode"])) is not None else None),
        "mainTeam": play["details"]["eventOwnerTeamId"],
        #Not every event involves an opposing player. Assign oppPlayer of any event without an opposing player to None.
        #Note: some play types that usually have opposing players may not in certain situations (e.g. empty net goals have no listed goalie.)
        "oppPlayer": (play["details"][constants.OPP_PLAYER_KEYS[play["typeCode"]]] if constants.OPP_PLAYER_KEYS.get(play["typeCode"]) is not None and
                      play["details"].get(constants.OPP_PLAYER_KEYS.get(play["typeCode"])) is not None else None),
        "assist1": play["details"]["assist1PlayerId"] if play["typeCode"] == 505 and play["details"].get("assist1PlayerId") is not None else None,
        "assist2": play["details"]["assist2PlayerId"] if play["typeCode"] == 505 and play["details"].get("assist2PlayerId") is not None else None
    } for play in plays]

    return plays

def clean_pbp(pbp_json: dict[str, Any]) -> dict[str, Any]:
    """
    Clean raw play-by-play data from NHL API into more concise format.

    Args:
        pbp_json (dict): Raw play-by-play data from NHL API, as Python dictionary.
    """
    #Keep only required keys, all others in raw data will not be used in the model.
    pbp_json = {k: pbp_json[k] for k in constants.KEEP_PBP}

    #Add margin of victory; positive for home win, negative for away win.
    pbp_json["margin"] = pbp_json["homeTeam"]["score"] - pbp_json["awayTeam"]["score"]

    #Reduce team desciptions to only keys listed in KEEP_TEAM.
    pbp_json["homeTeam"] = {k: pbp_json["homeTeam"][k] for k in constants.KEEP_TEAM}
    pbp_json["awayTeam"] = {k: pbp_json["awayTeam"][k] for k in constants.KEEP_TEAM}

    #Flatten gameOutcome; will be used to note whether game went to overtime or shootout
    pbp_json["gameOutcome"] = pbp_json["gameOutcome"]["lastPeriodType"]

    #Flatten rosterSpots; remove unneccesary keys
    pbp_json["rosterSpots"] = [{
        "teamId": player["teamId"],
        "playerId": player["playerId"],
        "name": player["firstName"]["default"] + " " + player["lastName"]["default"],
        "position": player["positionCode"]
    } for player in pbp_json["rosterSpots"]]

    #Get rid of period start and stoppage announcements
    pbp_json["plays"] = [play for play in pbp_json["plays"] if play["typeCode"] not in constants.REMOVED_PLAY_CODES]

    plays = [play for play in pbp_json["plays"] if play["periodDescriptor"]["periodType"] != "SO"]
    shootout = [play for play in pbp_json["plays"] if play["periodDescriptor"]["periodType"] == "SO"]

    pbp_json["plays"] = clean_play_list(plays)
    pbp_json["shootout"] = clean_play_list(shootout)

    return pbp_json

def clean_all_pbp() -> None:
    """
    Clean all raw data collected (including previously cleaned data).
    """
    #Get list of all files in data/raw/
    raw_files = os.listdir(anefrost.RAW_DIR)

    for f in raw_files:
        #Get first file in raw/ but not in clean/; load respective JSON data to clean
        with open(anefrost.RAW_DIR / f"{f}", mode="r", encoding="utf-8") as file:
            pbp_json = json.load(file)
        #Clean data from this game
        pbp_json = clean_pbp(pbp_json)
        #Write cleaned data into clean/
        with open(anefrost.CLEAN_DIR /f"{f}", mode = "w", encoding="utf-8") as file:
            json.dump(pbp_json, file, indent=2)
