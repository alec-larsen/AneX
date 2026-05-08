from pathlib import Path
import sys

__all__ = ["RAW_DIR", "CLEAN_DIR", "COMPILED_DIR", "CACHE_DIR", "DATA_DIRECTORIES"]

#Root directory in source tree
_DEV_ROOT = Path(__file__).resolve().parents[1]

#Root directory of application:
#Use executable directory when frozen
if getattr(sys, "frozen", False):
    _ROOT_DIRECTORY = Path(sys.executable).parent

#Else, use the source root during development
else:
    _ROOT_DIRECTORY = _DEV_ROOT # type: ignore

#All required data directories
RAW_DIR = _ROOT_DIRECTORY / "data" / "puck" / "raw"
CLEAN_DIR = _ROOT_DIRECTORY / "data" / "puck" / "clean"
COMPILED_DIR = _ROOT_DIRECTORY / "data" / "puck" / "compiled"
CACHE_DIR = _ROOT_DIRECTORY / "data" / "puck" / "cached"

#Set of all required data directories
DATA_DIRECTORIES = [
    RAW_DIR,
    CLEAN_DIR,
    COMPILED_DIR,
    CACHE_DIR
]
