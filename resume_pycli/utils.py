#!/usr/bin/env python3

from base64 import b64encode
from bs4 import BeautifulSoup
import functools
from http.server import HTTPServer, SimpleHTTPRequestHandler
from importlib.resources import as_file
from importlib.resources import files
from pathlib import Path
from shutil import copytree
import socket
import subprocess
from tempfile import TemporaryDirectory
import threading
from typing import Optional

from jinja2 import (
    Environment,
    FileSystemLoader,
    select_autoescape,
)
import jsonschema
from playwright.sync_api import sync_playwright


def validate(resume: dict, schema: dict) -> Optional[str]:
    try:
        jsonschema.validate(instance=resume, schema=schema)
    except jsonschema.ValidationError as err:
        return err.message

    return None


def render_html(resume: dict, theme: str) -> str:
    lib_dir = files("resume_pycli")
    env = Environment(
        loader=FileSystemLoader(
            [
                str(Path.cwd().joinpath("themes").joinpath(theme)),
                str(lib_dir.joinpath("themes").joinpath(theme)),
            ]
        ),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("index.html")
    html = template.render(**resume)

    return html


def export_html(resume: dict, theme: str, output: Path) -> None:
    if "image" in resume["basics"] and resume["basics"]["image"]:
        with open(resume["basics"]["image"], "rb") as image_file:
            resume["basics"]["image_b64"] = b64encode(image_file.read()).decode()
    html = render_html(resume, theme)
    output.joinpath("index.html").write_text(html)
    # find theme directory
    if (cwd_theme := Path.cwd().joinpath("themes").joinpath(theme)).is_dir():
        theme_dir = cwd_theme
    elif (
        lib_theme := files("resume_pycli").joinpath("themes").joinpath(theme)
    ).is_dir():
        with as_file(lib_theme) as lib_theme_p:
            theme_dir = lib_theme_p
    else:
        raise Exception("cannot find theme")
    # copy theme assets in output directory
    soup = BeautifulSoup(html, "html.parser")
    assets = [
        link.get("href").split("/")[1]
        for link in soup.find_all("link")
        if link.get("href").startswith("/")
    ]
    assets += [
        script.get("src").split("/")[1]
        for script in soup.find_all("script")
        if script.get("src").startswith("/")
    ]
    assets_uniq = set(assets)
    for asset in assets_uniq:
        copytree(
            Path.joinpath(theme_dir, asset),
            output.joinpath(asset),
            dirs_exist_ok=True,
        )


def check_port(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0


def export_pdf(resume: dict, theme: str, output: Path) -> None:
    # export html in a random temporary directory
    tmpdir = TemporaryDirectory()
    export_html(resume, theme, Path(tmpdir.name))
    # increment port if already in use
    port = 4001
    while check_port(port):
        port += 1
    # run server in background
    daemon = threading.Thread(
        target=serve, args=("localhost", port, tmpdir.name, True), daemon=True
    )
    daemon.start()
    with sync_playwright() as p:
        chromium = p.chromium
        if not Path(chromium.executable_path).exists():
            subprocess.run(["playwright", "install", "chromium"], check=True)
        browser = chromium.launch()
        page = browser.new_page()
        page.goto(url=f"http://localhost:{port}")
        page.pdf(path=str(output.joinpath("index.pdf")), format="A4")
        browser.close()


class SilentHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


def serve(address: str, port: int, path: Path, silent: bool) -> None:
    server_address = (address, port)
    handler = SilentHandler if silent else SimpleHTTPRequestHandler
    resume_handler = functools.partial(handler, directory=path)
    httpd = HTTPServer(server_address, resume_handler)
    httpd.serve_forever()
