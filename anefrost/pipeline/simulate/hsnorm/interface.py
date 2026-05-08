import anefrost
from anefrost.pipeline.simulate import hsnorm

def state_generator() -> float:
    """
    Compute all required values for team statline generation and measure process runtime.
    
    All computed parameters are saved to state.

    Returns:
        float: Total required time to compute all generation parameters.
    """
    t1, _ = anefrost.time_func(hsnorm.global_cor)
    t2, _ = anefrost.time_func(hsnorm.team_parameters)

    return t1+t2

def hth_results():
    t, (md1, md2) = anefrost.time_func(hsnorm.hth_table)
    return (t, md1, md2)
