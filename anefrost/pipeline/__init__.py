#Add all main modules to namespace by default
from . import clean #type: ignore
from . import compiler #type: ignore
from . import ingest #type: ignore
from .model import linear_regression #type: ignore

#Add all interface functions directly to pipeline API
from .clean.interface import *
from .compiler.interface import *
from .ingest.interface import *
from .model.linear_regression.interface import *
from .simulate.hsnorm.interface import *

from .ingest.core import unwritten_games #type: ignore
