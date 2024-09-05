import time
import typing

import requests

from python_qa.logging.logging import Logging

logger = Logging.logger


def wait_for_condition(
        func: typing.Callable,
        expected_condition: typing.Callable[[object], bool],
        wait_time: int = 10,
        step_time: int = 0.5,
):
    res = None
    end_time = time.time() + wait_time
    while time.time() < end_time:
        time.sleep(step_time)
        try:
            res = func()
            if expected_condition(res):
                return res
        except Exception as e:
            logger.warning(f"An error: {e} occurred while waiting\nContinue waiting ...")
    return res


wait = wait_for_condition


def wait_for_status(
        func: typing.Callable, status: int = 200, wait_iter: int = 5, wait_step: int = 0.5
):
    iter = 0
    res = None
    while iter < wait_iter:
        res = func()
        if res.status_code == status:
            return res
        iter += 1
        time.sleep(wait_step)
    return res


wfs = wait_for_status


def wait_for(fn: typing.Callable, wait_time: int = 15, wait_step: float = 0.2):
    start_time = time.time()
    res = fn()
    while not res and start_time + wait_time >= time.time():
        time.sleep(wait_step)
        res = fn()
    return res


def wait_for_server_start(url: str, wait_time: int = 5, wait_step: float = 0.2):
    resp = None
    start_time = time.time()
    while not resp and start_time + wait_time >= time.time():
        logger.info("waiting for the server to start ...")
        try:
            resp = requests.get(url)
            return
        except Exception:
            time.sleep(wait_step)
    raise Exception(f"Failed to connect to server: {url}")


wait_start = wait_for_server_start
