#Custom class of exception to handle errors raised by verification functions.
class VerificationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

#Custom class of exception to handle errors created by network connectivity issues.
class NetworkError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

#Custom class of exception to handle timeout-adjacent errors in reasonably expected sections of the program.
class ExcessDelayError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

#Set of custom exceptions that stem from runtime error
RUNTIME_ERROR_FLAGS = (VerificationError, NetworkError, ExcessDelayError)
