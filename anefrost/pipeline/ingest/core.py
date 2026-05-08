import json
import datetime
import os

import anefrost

__all__ = ["write_batch_pbp", "unwritten_games"]

def unwritten_games() -> list[int]:
    """
    Obtain list of required games' play-by-plays that have yet to be written into raw data.

    Returns:
        list[int]: List of all game_ids of unwritten play-by-plays
    """
    #Get list of all files in data/raw/
    current_files = os.listdir(anefrost.RAW_DIR)

    #Cut off '.json' extension and cast to int to get game_id
    current_files = [int(file[:-5]) for file in current_files]

    #Find lowest game_id whose play-by-play we want for the model that isn't already in our raw dataset.
    return [code for code in anefrost.ALL_GAME_IDS if code not in current_files]

def write_play_by_play(game_id: int) -> bool:
    """
    Pull play-by-play data from NHL API and write data to local system in JSON format.

    Args:
        game_id (int): id of game to pull play-by-play of
        
    Returns:
        bool: True if game was successfully written to raw data, False otherwise.
    """
    pbp_json = anefrost.request_json(f"https://api-web.nhle.com/v1/gamecenter/{game_id}/play-by-play")

    #Verify that the game in question has not been postponed.
    #If the recorded date of the game is before today, this game has occurred; write as intended.
    if datetime.datetime.strptime(pbp_json["gameDate"], '%Y-%m-%d') < datetime.datetime.now():
        with open(anefrost.RAW_DIR /f"{game_id}.json", mode = "w", encoding="utf-8") as file:
            json.dump(pbp_json, file, indent=2)
        return True

    #If this game has been rescheduled and has yet to be played, return False to signify writing cannot be done.
    else:
        return False

def write_next_pbp() -> bool:
    """
    Write oldest play-by-play data not yet in data/raw/ to JSON.
    
    Returns:
        bool: True if this function wrote into raw data, False otherwise
    """
    for game in unwritten_games():
        #Attempt to write this new play-by-play into our dataset
        success = write_play_by_play(game)

        #If writing was successful, return True to signify a successful write.
        if success:
            return True

        #If writing failed, we move to the next game in the list.

    #If every remaining game was not written, return False to signify this function did not change the data.
    return False

def write_batch_pbp() -> None:
    """
    Write 100 play-by-plays into raw data.
    
    If there are less than 100 play-by-plays missing from the raw dataset, write all remaining play-by-plays.
    """

    #Attempt to write the next play-by-play missing from raw data 100 times.
    for _ in range(100):
        #If we fail to write the next play-by-play, all required data has been written already.
        if not write_next_pbp():
            break
