import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

import anefrost

def load_data(params: list[str], data: pd.DataFrame|None = None):
    """
    Load play-by-play data and convert goal differentials to binary win/loss target variable.
    """
    if data is None:
        #Load previously compiled data
        with open(anefrost.COMPILED_DIR / "team_statistics.json", mode="r", encoding="utf-8") as file:
            data = json.load(file)
            data = pd.DataFrame(data)

    #Partition compiled data into dependent and target data
    x = data[params].to_numpy()
    #Convert goal differentials to win/loss; 1 if home team wins game (excluding SO), 0.5 if game is tied into SO, 0 otherwise.
    y = np.array([1 if gd > 0 else 0.5 if gd == 0 else 0 for gd in data["goal_diff"]])
    return (x,y)

def build_model():
    x,y = load_data(anefrost.state.model_params)
    LogisticRegression().fit(x,y)
