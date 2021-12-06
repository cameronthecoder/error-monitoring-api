import itertools
import platform
import sys
import traceback
import requests
import threading
import json
import os
from datetime import date, timedelta

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
        print(data)
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
        print(file)
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

    def send_exception(self, exception, type, req_data: dict, env_data: dict):
        # Not sure if this is a good way to parse exceptions but it works for now /shrug
        if exception.__traceback__:
            tb = traceback.extract_tb(exception.__traceback__)
        else:
            tb = traceback.extract_tb(sys.exc_info())
        frames = []
        environment = {}
        for frame in tb:
            f = {
                "file_name": frame[0],
                "line_number": frame[1],
                "method_name": frame[2],
                "line": frame[3],
                "code": self._get_code_window(frame[0], frame[1]),
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
            "error_name": f"{type.__name__}: {str(exception)}",
            "request": req_data,
            "environment": environment,
        }
        issue_json = json.dumps(issue, indent=2, cls=CustomJSONEncoder)

        threading.Thread(target=self._send, args=(issue_json,)).start()
