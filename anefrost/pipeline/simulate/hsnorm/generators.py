import numpy as np
import pandas as pd
import json
import random

import anefrost

__all__ = ["global_cor", "team_parameters", "random_mv_norm"]

def global_cor():
    """
    Produce correlation matrix from all data in dataset.

    Returns:
        NDArray: Correlation matrix for all NHL data
    """
    x, _ = anefrost.pipeline.model.linear_regression.load_parameters(anefrost.state.model_params)
    anefrost.state.generator_params[0] =  np.corrcoef(x,rowvar=False) #type: ignore

def team_parameters():
    for team in anefrost.state.teams: #type: ignore - The teams attribute will be assigned whenever this function is run
        with open(anefrost.COMPILED_DIR / f"{team}h.json", mode="r", encoding="utf-8") as file:
            data = json.load(file)
            home_data = pd.DataFrame(data).to_numpy()

        with open(anefrost.COMPILED_DIR / f"{team}a.json", mode="r", encoding="utf-8") as file:
            data = json.load(file)
            away_data = pd.DataFrame(data).to_numpy()

        all_data = np.vstack([home_data, away_data])

        team_dist = {
            "std": np.std(all_data,0),
            "home_mu": home_data.mean(0),
            "away_mu": away_data.mean(0)
        }

        anefrost.state.generator_params[team] = team_dist

def random_mv_norm(team: int, home: bool = True):
    cor = anefrost.state.generator_params[0]
    team_params = anefrost.state.generator_params[team]
    mu = team_params["home_mu"] if home else team_params["away_mu"]

    #Produce diagonal standard deviation matrix
    d = np.diag(team_params["std"])

    #Using correlation from leaguewide data and variance from specific team, construct covariance matrix
    #We use the Cholesky decomposition (lower triangular factor), A, to sample from our random multivariate normal distribution
    a = np.linalg.cholesky(d @ cor @ d)

    #Generate a random vector, z, consisting of N independent univariate standard normal variables.
    z = np.array([random.normalvariate() for _ in range(len(mu))])

    #The transform Q = mu + Az produces a value drawn from the desired multivariate normal distribution.
    q =  mu + (a @ z.T)
    return q.reshape(1,-1)
