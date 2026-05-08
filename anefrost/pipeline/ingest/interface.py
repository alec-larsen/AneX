import anefrost
from anefrost.pipeline import ingest

__all__ = ["ingest_pbp"]

def ingest_pbp() -> tuple[int, float]:
    """
    Ingest 100 play-by-plays from the NHL API, if at least 100 are required to write.
    
    If there are less than 100 play-by-plays remaining to write, ingest all remaing play-by-plays.
    
    Print total runtime for process.
    """
    #Get number of games left to write before 100 attempted writing calls
    initial_unwritten_games = len(ingest.core.unwritten_games())

    #Get time (in seconds) for set of ingestion calls
    t, _ = anefrost.time_func(ingest.write_batch_pbp)

    #Get number of games left to write before 100 attempted writing calls
    final_unwritten_games = len(ingest.unwritten_games())

    #If we had 100 or less play-by-plays left to write, this function wrote the last of the required data.
    n = initial_unwritten_games-final_unwritten_games
    return (n,t)
