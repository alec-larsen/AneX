import anefrost
from anefrost.pipeline.model.linear_regression import core

__all__ = ["team_summary_model"]

def team_summary_model() -> tuple[float, float, int, int]:
    """
    Train linear regression model and return process runtime.

    Returns:
        float: Process runtime (in seconds)
        LinearRegression: Trained linear regression model
        float: R^2 score of model
        int: Total games in data with correct win/loss predicted by model
        int: Total games in dataset that did not go to a shootout
    """
    t, _ = anefrost.time_func(core.train_team_regression)

    x, y = core.load_parameters(anefrost.state.model_params)

    score = anefrost.state.model.score(x,y)

    pred_y = anefrost.state.model.predict(x)

    correct = len([i for i in range(len(y)) if y[i]*pred_y[i] > 0])
    non_so = len([i for i in range(len(y)) if y[i] != 0])

    return (t, score, correct, non_so)
