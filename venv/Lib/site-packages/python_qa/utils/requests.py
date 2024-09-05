import inspect
from typing import Union, List

from requests import Response

from python_qa.logging.logging import Logging


def verify_response(
        resp: Response,
        ok_status: Union[int, List[int]] = 200,
        fail_text: str = "",
) -> Response:
    func = inspect.stack()[1][4][0].strip()
    if isinstance(ok_status, int):
        ok_status = [ok_status]
    if resp.status_code not in ok_status:
        raise ValueError(
            f"Verified response: function {func} failed:"
            f"\nResponse code: {resp.status_code}, expected: {ok_status}"
            f"\nResponse data: {resp.content}"
            f"\n{fail_text}"
        )
    else:
        Logging.logger.info(
            f"Verified response: function {func} code {resp.status_code}"
        )
    return resp


vr = verify_response
