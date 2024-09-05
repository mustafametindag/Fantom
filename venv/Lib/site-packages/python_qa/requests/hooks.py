import json

from python_qa.logging.logging import Logging
import logging


class BaseLogging:
    log_level = logging.NOTSET
    log_format = None

    def log(self, data):
        try:
            content = json.dumps(data.json(), indent=4, ensure_ascii=False, sort_keys=True)
        except ValueError:
            content = data.text if len(data.text) < 1000 else f"\tPart of the big response data is:\n{data.text[:100]}\n..."
        if isinstance(data.request.body, str):
            try:
                body = json.dumps(json.loads(data.request.body), indent=4, ensure_ascii=False, sort_keys=True)
            except json.decoder.JSONDecodeError:
                body = data.request.body
        elif isinstance(data.request.body, bytes) and len(data.request.body) < 100000:
            try:
                body = json.dumps(json.loads(data.request.body.decode('UTF-8')), indent=4, ensure_ascii=False, sort_keys=True)
            except ValueError:
                body = "*** Request data has to big or non text content in the body for logging ***"
        else:
            body = "-"
        Logging.logger.log(
            self.log_level, self.log_format.format(data=data, body=body, content=content)
        )


class LoggingResponseInfo(BaseLogging):
    log_format = (
        "\nRequest: {data.request.method} {data.url} "
        "headers {data.request.headers}\n"
        "Request body:\n{body}\n\n"
        "Response: {data.status_code}\n"
        "{content}"
    )
    log_level = logging.INFO

    def run(self, response, *args, **kwargs):
        self.log(response)
