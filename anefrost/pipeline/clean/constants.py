#Dictionary keys to be kept in the first step of cleaning. All other keys are 'obsolete' and will be deleted.
#Some keys contain information obtainable from kept keys (e.g. season from first four digits of game_id)
#Others contain information not planned to be used in the model (e.g. startTimeUTC)
KEEP_PBP = ["id", "gameDate", "awayTeam", "homeTeam", "gameOutcome", "plays", "rosterSpots"]
KEEP_TEAM = ["id", "abbrev"]

#Several events in the play-by-play are not intended to be used by the model.
#As such, it is most convenient to remove them.
REMOVED_PLAY_CODES = [516, 520, 521, 523, 524, 535]

#Some keys in the cleaned play-by-data are dependent on event type.
#For example, oppPlayer comes from goalieId for goals, but playerId of winnign player for faceoffs
#Key that should be analyzed for the details key of our cleaned dictionary (by typeCode)
DETAIL_KEYS = {
    505: "shotType",
    506: "shotType",
    507: "shotType",
    508: "reason",
    509: "typeCode"
}

MAIN_PLAYER_KEYS = {
    502: "winningPlayerId",
    503: "hittingPlayerId",
    504: "playerId",
    505: "scoringPlayerId",
    506: "shootingPlayerId",
    507: "shootingPlayerId",
    508: "shootingPlayerId",
    509: "committedByPlayerId",
    525: "playerId"
}

OPP_PLAYER_KEYS = {
    502: "losingPlayerId",
    503: "hitteePlayerId",
    505: "goalieInNetId",
    506: "goalieInNetId",
    507: "goalieInNetId",
    508: "blockingPlayerId",
    509: "drawnByPlayerId"
}

#Testing constants
#Keys that should be present in the cleaned dictionary produced by clean_pbp
CLEAN_MAIN_KEYS = ["id", "gameDate", "awayTeam", "homeTeam", "gameOutcome", "plays", "rosterSpots", "margin", "shootout"]
CLEAN_PLAY_KEYS = ["eventId", "type", "x", "y", "details", "mainPlayer", "oppPlayer", "assist1", "assist2"]
