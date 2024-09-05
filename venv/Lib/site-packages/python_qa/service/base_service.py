import os
import multiprocess
from multiprocessing import current_process
from subprocess import Popen, PIPE, STDOUT
from python_qa.logging.logging import Logging


class BaseService:
    _name: str = "base-service"
    _binary_path: str = None
    _custom_config: dict = {}
    _config: dict = {}
    _config_arg: str = None
    _config_path: str = None
    _port: int = None
    _proc: Popen = None

    def __init__(
            self,
            binary_path: str,
            config_path: str = None,
            config_arg: str = "-config"
    ):
        self._binary_path = binary_path
        self._config_path = config_path
        self._config_arg = config_arg

    def _start_service(self):
        def log_stdout(stdout):
            t = current_process()
            while getattr(t, "do_run", True):
                for line in stdout:
                    data = line.decode("utf-8").strip()
                    if data:
                        Logging.logger.info(f"{self._name}: " + data)
        args = [self._binary_path, f"{self._config_arg}={self._config_path}"]
        self._proc = Popen(
            args,
            stdout=PIPE,
            stderr=STDOUT,
            env={"APP_NAME": self._name, **os.environ}
        )
        # ToDo: multiprocessing
        self._log_proc = multiprocess.Process(
            target=log_stdout, args=[self._proc.stdout]
        )
        self._log_proc.start()

    def _stop_service(self):
        if self._proc:
            if self._proc.poll() is None:
                self._proc.kill()
            if self._log_proc.is_alive():
                self._log_proc.do_run = False
                self._log_proc.terminate()
