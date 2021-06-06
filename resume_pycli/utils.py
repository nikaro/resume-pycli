#!/usr/bin/env python3

import ast
from base64 import b64encode
from bs4 import BeautifulSoup
import functools
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from shutil import copytree
import socket
from tempfile import TemporaryDirectory
import threading

from jinja2 import (
    Environment,
    FileSystemLoader,
    select_autoescape,
)
import jsonschema
import pdfkit


def validate(resume: dict, schema: dict) -> str:
    try:
        jsonschema.validate(instance=resume, schema=schema)
    except jsonschema.ValidationError as err:
        return err.message
    else:
        return ""


def render_html(resume: dict, theme: str) -> str:
    lib_dir = Path(__file__).parent
    env = Environment(
        loader=FileSystemLoader(
            [
                str(Path.cwd().joinpath("themes", theme)),
                str(lib_dir.joinpath("themes", theme)),
            ]
        ),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("index.html")
    html = template.render(**resume)

    return html


def export_html(resume: dict, theme: str, output: str) -> None:
    if "image" in resume["basics"] and resume["basics"]["image"]:
        with open(resume["basics"]["image"], "rb") as image_file:
            resume["basics"]["image_b64"] = b64encode(image_file.read()).decode()
    html = render_html(resume, theme)
    Path(output, "index.html").write_text(html)
    # find theme directory
    if (cwd_theme := Path.cwd().joinpath("themes", theme)).is_dir():
        theme_dir = cwd_theme
    elif (lib_theme := Path(__file__).parent.joinpath("themes", theme)).is_dir():
        theme_dir = lib_theme
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
    assets = set(assets)
    for asset in assets:
        copytree(
            Path.joinpath(theme_dir, asset),
            Path(output).joinpath(asset),
            dirs_exist_ok=True,
        )


def cb_pdf_options(ctx, params, value) -> dict:
    return ast.literal_eval(value)


def check_port(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0


def export_pdf(resume: dict, theme: str, output: str, pdf_options: dict) -> None:
    # export html in a random temporary directory
    tmpdir = TemporaryDirectory()
    export_html(resume, theme, tmpdir.name)
    # increment port if already in use
    port = 4001
    while check_port(port):
        port += 1
    # run server in background
    daemon = threading.Thread(
        target=serve, args=("localhost", port, tmpdir.name, True), daemon=True
    )
    daemon.start()
    options = {
        "quiet": "",
    }
    options.update(pdf_options)
    pdfkit.from_url(
        f"http://localhost:{port}",
        str(Path(output, "index.pdf")),
        options=options,
    )


class SilentHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


def serve(address: str, port: int, path: str, silent: bool) -> None:
    server_address = (address, port)
    handler = SilentHandler if silent else SimpleHTTPRequestHandler
    resume_handler = functools.partial(handler, directory=path)
    httpd = HTTPServer(server_address, resume_handler)
    httpd.serve_forever()
