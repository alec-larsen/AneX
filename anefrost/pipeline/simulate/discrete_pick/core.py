import json
import pandas as pd

import anefrost

def sim_game(home: int, away: int) -> float:
    with open(anefrost.COMPILED_DIR / f"{home}h.json", mode="r", encoding="utf-8") as file:
        data = json.load(file)
        home_data = pd.DataFrame(data).to_numpy()

    with open(anefrost.COMPILED_DIR / f"{away}a.json", mode="r", encoding="utf-8") as file:
        data = json.load(file)
        away_data = pd.DataFrame(data).to_numpy()
        
    home_wins = 0
    
    for i in range(41):
        for j in range(41):
            diff = anefrost.state.model.predict(home_data[i]) + anefrost.state.model.predict(away_data[j])
            
            if diff > 0:
                home_wins += 1
    
    return home_wins/1681