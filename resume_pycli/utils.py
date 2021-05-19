#!/usr/bin/env python3

import base64
import functools
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import (
    Environment,
    FileSystemLoader,
    select_autoescape,
)
import jsonschema
from pathlib import Path
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


def export_html(resume: dict, theme: str) -> None:
    if "image" in resume["basics"] and resume["basics"]["image"]:
        with open(resume["basics"]["image"], "rb") as image_file:
            resume["basics"]["image"] = base64.b64encode(image_file.read()).decode()
    html = render_html(resume, theme)
    Path("public", "index.html").write_text(html)


def export_pdf(resume: dict, theme: str) -> None:
    options = {
        "quiet": "",
    }
    html = render_html(resume, theme)
    pdfkit.from_string(
        html,
        str(Path("public", "index.pdf")),
        options=options,
    )


def serve(address: str, port: int, path: str) -> None:
    server_address = (address, port)
    ResumeHTTPRequestHandler = functools.partial(
        SimpleHTTPRequestHandler, directory=path
    )
    httpd = HTTPServer(server_address, ResumeHTTPRequestHandler)
    httpd.serve_forever()
