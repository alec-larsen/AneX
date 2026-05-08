import anefrost
from anefrost.pipeline.simulate.hsnorm import random_mv_norm

__all__ = ["sim_game"]

def sim_game(home: int, away: int):
    home_gen = anefrost.state.model.predict(random_mv_norm(home, True))
    away_gen = anefrost.state.model.predict(random_mv_norm(away, False))
    return home_gen + away_gen
