import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

import anefrost

__all__ = ["load_parameters", "train_team_regression"]

def load_parameters(params: list[str], data: pd.DataFrame|None = None) -> tuple[np.typing.NDArray[np.float64], np.typing.NDArray[np.float64]]:
    if data is None:
        #Load previously compiled data
        with open(anefrost.COMPILED_DIR / "team_statistics.json", mode="r", encoding="utf-8") as file:
            data = json.load(file)
            data = pd.DataFrame(data)

    #Partition compiled data into dependent and target data
    x = data[params].to_numpy()
    y = data["goal_diff"].to_numpy()
    return (x,y)

def train_team_regression() -> None:
    """
    Train model to project home goal differential based on on basic team-level statistics.

    Saves generated model directly to state.
    """
    x, y = load_parameters(anefrost.state.model_params)

    anefrost.state.model = LinearRegression().fit(x,y) #type: ignore
