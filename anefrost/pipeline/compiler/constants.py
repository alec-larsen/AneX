#Reference tables to convert numerical ids to string descriptions.
#Primarily used to allow end-users to easily type queries by team/event name

EVENT_TYPES = {
    502: "Faceoff",
    503: "Hit",
    504: "Giveaway",
    505: "Goal",
    506: "Shot on Goal",
    507: "Missed Shot",
    508: "Blocked Shot",
    509: "Penalty",
    525: "Takeaway",
    #All 6xx type codes are added for ease of querying and should no be found in any play-by-play data
    605: "Empty Net Goal",
    606: "Awarded Goal",
    608: "Teammate Blocked Shot"
}

#Penalty codes to number of minutes
PEN_MINUTES = {
    "MIN": 2,
    "BEN": 2,
    "MAJ": 5,
    "GAM": 10
}
