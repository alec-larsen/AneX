import time

__all__ = ["DOORS", "exit_door"]

#Custom exception to denote intended exit of program
#Will be useful if/when logging is added for extra documentation of runtime
class _ControlledExit(Exception):
    def __init__(self):
        super().__init__("Program exited without error.")

#Callable to cleanly leave program
def exit_door():
    time.sleep(3)
    raise _ControlledExit

DOORS = _ControlledExit
