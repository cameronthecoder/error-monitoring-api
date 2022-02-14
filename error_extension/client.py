import itertools
import platform
import sys
import traceback
import requests
import threading
import json
import os
from datetime import timedelta
from importlib.metadata import version


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, timedelta):
                return str(obj)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return json.JSONEncoder.default(self, obj)


class Client(object):
    def __init__(
        self, api_key: str, server_host: str, excluded_keys: list = []
    ) -> None:
        self.api_key = api_key
        self.server_host = server_host
        self.excluded_keys = excluded_keys

    def _send(self, data):
        try:
            response = requests.post(
                self.server_host + "/api/issues/",
                headers={
                    "API-Key": self.api_key,
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "User-Agent": "error-monitoring",
                },
                data=data,
                timeout=10,
            )
            json = response.json()
            return json
        except Exception as e:
            print(e)

    def set_api_key(self, key: str) -> None:
        self.api_key = key

    def _get_code_window(self, file, line_number) -> str:
        if file != "<string>" and os.path.exists(file):
            with open(file) as _file:
                code = ""
                for line in itertools.islice(
                    _file, (line_number - 10), line_number + 10
                ):
                    code += line
                return code
        else:
            return ""

    def send_exception(
        self, req_data: dict = {}, env_data: dict = {}, exc_info=None, exception: Exception = None
    ):
        # Copied some code from https://github.com/MindscapeHQ/raygun4py/blob/2bf646157d2eb169fcbd9342d9fcc3447855f189/python3/raygun4py/raygunprovider.py#L80
        # This allows for sending an exception without passing an exception object

        if exc_info is None:
            exc_info = sys.exc_info()

        exc_type, exc_value, exc_traceback = exc_info

        error_name = None
        if exception is not None:
            error_name = f"{type(exception).__name__}: {str(exception)}"
            tb = traceback.extract_tb(exception.__traceback__)
        else:
            error_name = f"{exc_type.__name__}: {str(exc_value)}"
            tb = traceback.extract_tb(exc_traceback)

        frames = []
        environment = {}

        for frame in tb:
            file_name, line_number, method_name, line = frame
            f = {
                "file_name": file_name,
                "line_number": line_number,
                "method_name": method_name,
                "line": line,
                "code": self._get_code_window(file_name, line_number),
            }
            frames.append(f)

        for key, value in env_data.items():
            if key in self.excluded_keys:
                environment[key] = "******"
            elif value is not None:
                environment[key] = value

        environment["QUART_VER"] = version("quart")
        environment["PYTHON_VER"] = platform.python_version()

        issue = {
            "frames": frames,
            "error_name": error_name,
            "request": req_data,
            "environment": environment,
        }
        issue_json = json.dumps(issue, indent=2, cls=CustomJSONEncoder)

        threading.Thread(target=self._send, args=(issue_json,)).start()
