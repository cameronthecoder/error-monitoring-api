import itertools
import platform
import sys
import traceback
import quart
import requests
import threading
import json


class Client(object):
    def __init__(self, api_key: str, server_host: str) -> None:
        self.api_key = api_key
        self.server_host = server_host

    def _send(self, data):
        try:
            response = requests.post(
                self.server_host + "/api/projects/issues/",
                headers={
                    "API-Key": self.api_key,
                    "Content-Type": "application/json",
                    "User-Agent": "error-monitoring",
                },
                data=data,
                timeout=10,
            )
            return response.json()
        except Exception as e:
            print(e)

    def _get_code_window(self, file, line_number) -> str:
        with open(file) as _file:
            code = ""
            iteration = 0
            for line in itertools.islice(_file, (line_number - 10), line_number + 10):
                iteration += 1
                code += line
            return code

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
                "file": frame[0],
                "line_number": frame[1],
                "method_name": frame[2],
                "line": frame[3],
                "code": self._get_code_window(frame[0], frame[1]),
            }
            frames.append(f)

        for key, value in env_data.items():
            environment[key] = str(value)
        
        environment["QUART_VER"] = quart.__version__
        environment["PYTHON_VER"] = platform.python_version()

        issue = {
            "frames": frames,
            "error": {"name": f"{type.__name__}: {str(exception)}"},
            "request": req_data,
            "environment": environment
        }
        print(issue)
        
        threading.Thread(target=self._send, args=(json.dumps(issue),)).start()
