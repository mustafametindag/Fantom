import re

import cattr

import json

from python_qa.logging.logging import Logging
from pytest_httpserver import HTTPServer

from python_qa.utils.classes import is_attrs_class
from python_qa.utils.wait import wait_for_server_start

logger = Logging.logger


class RespType:
    ONE_SHOT = 1


class BaseServiceStub:
    _port: int = 10071
    _stub: HTTPServer = None

    def start_stub(self, host="localhost", port=None):
        logger.info("Stub starting...")
        if port:
            self._port = port
        self._stub = HTTPServer(host=host, port=self._port)
        self._stub.start()
        wait_for_server_start(f"http://{host}:{self._port}")

    def stop_stub(self):
        logger.info("Stub stopping...")
        if self._stub:
            self._stub.stop()

    def add_rout(
            self, url: str, data: str | dict | bytes = None, status_code: int = 200, resp_type: RespType = RespType.ONE_SHOT
    ):
        logger.info(f"Adding stub: url={url}, data={data}, code={status_code}")
        # cnv = cattrs.Converter()  # ToDo: do!
        request = self._stub.expect_request(re.compile(".*" + url))
        if isinstance(data, list) and is_attrs_class(data[0]):
            list_data = []
            for d in data:
                list_data.append(cattr.unstructure(d))
            data = json.dumps(list_data, default=str)
        if is_attrs_class(data):
            data = json.dumps(cattr.Converter().unstructure_attrs_asdict(data), default=str)
        if isinstance(data, str):
            data = bytes(data, "utf-8")
        if isinstance(data, bytes):
            request.respond_with_data(data, status_code)
        elif isinstance(data, dict | list):
            request.respond_with_json(data, status_code)
