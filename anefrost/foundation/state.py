from typing import Any

from anefrost.foundation import statelookup

__all__ = ["state"]

TBA = object() #To Be Assigned

class State():
    def __init__(self, model_type: str = "Alpha"):
        self.model_params = statelookup.get_params(model_type)         
        self.generator_params: dict[int, Any] = {}
        self.teams = statelookup.TEAM_IDS
        self.model: Any = TBA
        self.hth_table = {}

    def set_model(self, model_type: str|list[str]):
        if isinstance(model_type, str):
            self.model_params = statelookup.get_params(model_type)

        else:
            self.model_params = model_type

state = State("Alpha")
