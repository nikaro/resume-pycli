from http.server import HTTPServer, SimpleHTTPRequestHandler
import functools
from pathlib import Path
import socket
from typing import Optional

import jsonschema


def validate(resume: dict, schema: dict) -> Optional[str]:
    try:
        jsonschema.validate(instance=resume, schema=schema)
    except jsonschema.ValidationError as err:
        return err.message

    return None


def check_port(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0


class SilentHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


def serve(address: str, port: int, path: Path, silent: bool) -> None:
    server_address = (address, port)
    handler = SilentHandler if silent else SimpleHTTPRequestHandler
    resume_handler = functools.partial(handler, directory=path)
    httpd = HTTPServer(server_address, resume_handler)
    httpd.serve_forever()
