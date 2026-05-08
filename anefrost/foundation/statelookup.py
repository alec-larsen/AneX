__all__ = ["get_params", "TEAM_IDS"]

#Parameter Set Types
PARAM_SETS = {
    "Alpha": ["home_shots", "away_shots", "home_shot_pct", "away_shot_pct",
               "home_faceoffs", "away_faceoffs", "home_save_pct",
               "away_save_pct", "home_hits", "away_hits", "home_blocked", "away_blocked"],
    "Goal-Agnostic": ["home_shots", "away_shots", "home_faceoffs", "away_faceoffs", "home_hits",
                      "away_hits", "home_blocked", "away_blocked"],
    "Goal-Centric": ["home_shot_pct", "away_shot_pct", "home_save_pct", "away_save_pct",
                     "home_pdo", "away_pdo"]
}

def get_params(param_set: str) -> list[str]:
    """
    Retrieve set of parameters to be used when training model

    Args:
        param_set (str): Key used to retrieve parameter set

    Returns:
        list[str]: Set of parameters.
    """
    return PARAM_SETS[param_set]

#Accepted names for users to refer to each team with given id by (case insensitive)
#Generally, each team has three accepted names; full, team/symbol, and abbreviation
#Some teams may have two nicknames (e.g. Canadiens/Habs, Maple Leafs/Leafs)
TEAM_IDS = {
    1: ["New Jersey Devils", "Devils", "NJD"],
    2: ["New York Islanders", "Islanders", "NYI"],
    3: ["New York Rangers", "Rangers", "NYR"],
    4: ["Philadelphia Flyers", "Flyers", "PHL"],
    5: ["Pittsburgh Penguins", "Penguins", "PIT"],
    6: ["Boston Bruins", "Bruins", "BOS"],
    7: ["Buffalo Sabres", "Sabres", "BUF"],
    8: ["Montreal Canadiens", "Canadiens", "Habs", "MTL"],
    9: ["Ottawa Senators", "Senators", "OTT"],
    10: ["Toronto Maple Leafs", "Maple Leafs", "Leafs", "TOR"],
    12: ["Carolina Hurricanes", "Hurricanes", "CAR"],
    13: ["Florida Panthers", "Panthers", "FLA"],
    14: ["Tampa Bay Lightning", "Lightning", "TBL"],
    15: ["Washington Capitals", "Capitals", "WSH"],
    16: ["Chicago Blackhawks", "Blackhawks", "CHI"],
    17: ["Detroit Red Wings", "Red Wings", "DET"],
    18: ["Nashville Predators", "Predators", "NSH"],
    19: ["St. Louis Blues", "Blues", "STL"],
    20: ["Calgary Flames", "Flames", "CGY"],
    21: ["Colorado Avalanche", "Avalanche", "COL"],
    22: ["Edmonton Oilers", "Oilers", "EDM"],
    23: ["Vancouver Canucks", "Canucks", "VAN"],
    24: ["Anaheim Ducks", "Ducks", "ANA"],
    25: ["Dallas Stars", "Stars", "DAL"],
    26: ["Los Angeles Kings", "Kings", "LAK"],
    28: ["San Jose Sharks", "Sharks", "SJS"],
    29: ["Columbus Blue Jackets", "Blue Jackets", "Jackets", "CBJ"],
    30: ["Minnesota Wild", "Wild", "MIN"],
    52: ["Winnipeg Jets", "Jets", "WPG"],
    54: ["Vegas Golden Knights", "Golden Knights", "VGK"],
    55: ["Seattle Kraken", "Kraken", "SEA"],
    68: ["Utah Mammoth", "Mammoth", "UTA"]
}

MODEL_TYPES = 0

#Information for generation algorithm types.
#Keys leading with capital letters are intended for external printing. All other keys are for data internal to the model.
GENERATION_TYPES = {
    "hsnorm": {
        "Game data generation method": "Multivariate normal distribution",
        "details": {
            "Parameter covariances": "All Game Data",
            "Parameter variances": "By Team",
            "Parameter means": "By Team, Home/Away"
        },
    },
    "discrete_pick": {
        "Game data generation method": "Discrete selection",
        "details": {
            "Home/Away Agnostic"
        }
    }
}
