import datetime
import json
from typing import Any

import pandas as pd

import anefrost
from anefrost.pipeline.compiler import constants

__all__ = ["Game"]

#Data structure to handle data from a single game.
class Game():
    id: int
    home: int
    away: int
    date: datetime.date
    result: str
    margin: int
    plays: pd.DataFrame
    shootout: pd.DataFrame
    rosters: pd.DataFrame

    def __init__(self, game_id: int):
        with open(anefrost.CLEAN_DIR / f"{game_id}.json", mode = "r", encoding="utf-8") as file:
            pbp_data = json.load(file)

        self.id = game_id
        self.home = pbp_data["homeTeam"]["id"]
        self.away = pbp_data["awayTeam"]["id"]

        if pbp_data["margin"] > 0:
            self.result = pbp_data["gameOutcome"][0] + "H"

        else:
            self.result = pbp_data["gameOutcome"][0] + "A"

        #For better date arithmetic, convert string date to datetime object
        self.date = datetime.datetime.strptime(pbp_data["gameDate"], "%Y-%m-%d")

        self.plays = pd.DataFrame(pbp_data["plays"])
        self.shootout = pd.DataFrame(pbp_data["shootout"])
        self.rosters = pd.DataFrame(pbp_data["rosterSpots"])

    def query_by_team(self, type_code: int, home: bool) -> int:
        """
        Query By Team:
        
        Obtain number of a given event attributed to team in game

        Args:
            df (pd.DataFrame): DataFrame containing all plays in game to check
            typeCode (int): code of event to search for
            home (bool): True to query for home team, False to query for away team

        Returns:
            int: Number of event type attributed to team
            
        Notes:
            Penalties are counted by total minutes, not total penalties given
            typeCode 506 is total shots on goal that are themselves not goals (i.e. saved shots)
            typeCode 605 (and other 6xx type codes) are not NHL official and should not be found in any play-by-play data.
        """
        df = self.plays
        team_id = self.home if home else self.away

        #Querying by number of penalties doesn't make much sense.
        #Instead, if we query for penalties, return the number of penalty minutes
        if type_code == 509:
            #Find all penalties attributed to team
            penalties = df[(df["type"] == type_code) & (df["mainTeam"] == team_id)]["details"]
            #Convert each penalty type to number minutes and sum to get total penalty minutes.
            return sum([constants.PEN_MINUTES[p] for p in penalties])

        #Empty net goals are all goals by our specified team where the listed goalie is null.
        elif type_code == 605:
            return len(df[(df["type"] == 505) & (df["mainTeam"] == team_id) & pd.isnull(df["oppPlayer"])])

        #Awarded goals are scored without a shot being taken; they have no associated details (normally shot type for goals)
        elif type_code == 606:
            return len(df[(df["type"] == 505) & (df["mainTeam"] == team_id) & pd.isnull(df["details"])])

        #Any shots blocked by teammates will have 'teammate-blocked' in details
        elif type_code == 608:
            return len(df[(df["type"] == 508) & (df["mainTeam"] == team_id) & (df["details"] == "teammate-blocked")])

        #Else, return the number of rows (plays) with type_code attributed to the appropriate team
        return len(df[(df["type"] == type_code) & (df["mainTeam"] == team_id)])

    def team_summary(self) -> pd.Series:
        """
        Compute relevant team-level statistics in regulation/overtime of game and return as pandas series.
        
        This function does NOT handle shootout data; shootouts will be analyzed in a separate module.

        Returns:
            pd.Series: Series containing all relevant team-level statistics for game.
            
        Notes:
            The current set of statistics this function compiles are the original parameters NSC uses to build its model.
            The exact collection of statistics this function compiles WILL change as development continues, though this
            original set will likely be set aside to give the option to run the 'legacy version' of this program.
        """

        #Calculate several quantities that will not be in our compiled statline, but will be used to calculate quantities that are.
        #Empty net goals (which don't count against opposing team save percentage)
        home_eng = self.query_by_team(605,True)
        away_eng = self.query_by_team(605,False)

        #Awarded goals (which don't count for team sho percentage)
        home_awg = self.query_by_team(606, True)
        away_awg = self.query_by_team(606, False)

        #Shots blocked by teammates (which don't count for 'normal' blocked shots)
        home_self_blocks = self.query_by_team(608, True)
        away_self_blocks = self.query_by_team(608, False)

        #Compile basic summary data for game.
        statline: dict[str,Any] = {
            "game_id": self.id, #Used as primary key
            "home_team": 68 if self.home == 59 else self.home, #Convert Utah Hockey Club occurrences to Mammoth
            "away_team": 68 if self.away == 59 else self.away,
            "date": self.date,
            "result": self.result
        }

        #Add goal summaries
        statline["home_goals"] =  self.query_by_team(505, True)
        statline["away_goals"] =  self.query_by_team(505, False)
        statline["goal_diff"] = statline["home_goals"] - statline["away_goals"]

        #Add shot summaries; note that total shots on goal are saved shots (506) plus total goals (505) less any awarded goals (606)
        statline["home_shots"] = self.query_by_team(506,True) + statline["home_goals"] - home_awg
        statline["away_shots"] = self.query_by_team(506,False) + statline["away_goals"] - away_awg
        statline["shot_diff"] = statline["home_shots"] - statline["away_shots"]

        #Since awarded goals have no associated shot, shot percentages are nonawarded goals over total shots
        #Though a very extreme case, set shot percentage to 0 if team has no shots.
        statline["home_shot_pct"] = (statline["home_goals"] - home_awg)/statline["home_shots"] if statline["home_shots"] > 0 else 0
        statline["away_shot_pct"] = (statline["away_goals"] - away_awg)/statline["away_shots"] if statline["away_shots"] > 0 else 0

        #Add faceoff summaries
        statline["home_faceoffs"] = self.query_by_team(502,True)
        statline["away_faceoffs"] = self.query_by_team(502,False)
        statline["faceoff_diff"] = statline["home_faceoffs"] - statline["away_faceoffs"]
        #Note that, since every NHL game starts with a faceoff, we do not need to account for unintended division by zero if a game has 0 faceoffs
        statline["faceoff_pct"] = statline["home_faceoffs"]/(statline["home_faceoffs"] + statline["away_faceoffs"])

        #Team save percentages (non empty net goals against over total shots on goal against)
        statline["home_save_pct"] = 1 - (statline["away_goals"] - away_eng)/(statline["away_shots"]-away_eng)
        statline["away_save_pct"] = 1 - (statline["home_goals"] - home_eng)/(statline["home_shots"]-home_eng)

        #Team hit summaries
        statline["home_hits"] = self.query_by_team(503, True)
        statline["away_hits"] = self.query_by_team(503, False)
        statline["hit_diff"] = statline["home_hits"] - statline["away_hits"]

        #Team blocked shots summaries
        #Note that, in the play-by-play data, the team attributed to each blocked shot is the team whose player was blocked
        #We opt to record blocked shots as the number of shots the team blocks (from opposing players)
        #Thus, we take the total shots the opposing team had blocked and subtract those blocked by teammates
        statline["home_blocked"] = self.query_by_team(508, False) - away_self_blocks
        statline["away_blocked"] = self.query_by_team(508, True) - home_self_blocks
        statline["block_diff"] = statline["home_blocked"] - statline["away_blocked"]

        #Additional 'special' metrics
        statline["home_pdo"] = statline["home_shot_pct"] + statline["home_save_pct"]
        statline["away_pdo"] = statline["away_shot_pct"] + statline["away_save_pct"]

        return pd.Series(statline)
