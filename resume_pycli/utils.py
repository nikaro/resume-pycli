from importlib.resources import as_file
from importlib.resources import files
from pathlib import Path
import socket
import threading
from typing import Optional

import jsonschema

from .html import serve


def validate(resume: dict, schema: dict) -> Optional[str]:
    try:
        jsonschema.validate(instance=resume, schema=schema)
    except jsonschema.ValidationError as err:
        return err.message

    return None


def check_port(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0


def find_theme(name: str) -> Path:
    """Find theme directory either in current directory or in package directory."""
    cwd_theme = Path.cwd().joinpath("themes").joinpath(name)
    lib_theme = files("resume_pycli").joinpath("themes").joinpath(name)
    if cwd_theme.is_dir():
        return cwd_theme
    elif lib_theme.is_dir():
        with as_file(lib_theme) as lib_theme_p:
            return lib_theme_p
    else:
        raise Exception("cannot find theme")


def serve_bg(*, resume: dict, theme: Path) -> int:
    port = 4001
    while check_port(port):
        port += 1
    # run server in background
    daemon = threading.Thread(
        target=serve,
        kwargs={"resume": resume, "theme": theme, "port": port},
        daemon=True,
    )
    daemon.start()
    return port
