from collections.abc import Callable
import time
from typing import Any

import requests

import anefrost

__all__ = ["request_json", "time_func"]

def request_json(url: str, code: int = 200) -> dict[str,Any]:
    """
    Summary

    Args:
        url (str): URL to attempt to request json data from
        code (int): Status code expected from general response; defaults to 200

    Raises:
        anestat.exceptions.NetworkError: Raised if response from get request is unable to be received or is received with an unexpected status code.
        anestat.exceptions.ExcessDelayError: Raised if get request takes excessively long to return any response

    Returns:
        dict[str,Any]: JSON data obtained from request, formatted as a Python dictionary
    """
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != code:
            raise anefrost.exceptions.NetworkError(f"\033[91mCall should yield status code {code}, obtained status code {response.status_code} instead.\033[0m")
        return response.json()

    except requests.exceptions.ConnectionError as exc:
        raise anefrost.exceptions.NetworkError("\033[91mResponse unable to be received from target. Please check internet connection.\033[0m") from exc

    except requests.exceptions.Timeout as exc:
        raise anefrost.exceptions.ExcessDelayError("\033[91mResponse not received for call within 10 seconds. Please check internet connection.\033[0m") from exc

def time_func(func: Callable[...,Any], n: int = 1) -> tuple[float,Any]:
    """
    Measure runtime for function call.

    Args:
        func (function): Function to measure runtime of.
        n (int): Number of times to run function. Defaults to 1.

    Returns:
        float: Final runtime (in seconds).
        Any: Any return values that 
    """
    start_time = time.perf_counter()

    for _ in range(n):
        val = func()

    end_time = time.perf_counter()

    return (end_time - start_time, val) #type: ignore - I know this isn't unbound
