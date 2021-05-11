#!/usr/bin/env python3

import functools
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import (
    ChoiceLoader,
    Environment,
    FileSystemLoader,
    PackageLoader,
    select_autoescape,
)
import jsonschema
from pathlib import Path
import pdfkit
from shutil import copy


def validate(resume: dict, schema: dict) -> str:
    try:
        jsonschema.validate(instance=resume, schema=schema)
    except jsonschema.ValidationError as err:
        return err.message
    else:
        return ""


def render_html(resume: dict, theme: str) -> str:
    env = Environment(
        loader=ChoiceLoader(
            [
                FileSystemLoader(f"themes/{theme}"),
                PackageLoader("resume_pycli", f"themes/{theme}"),
                PackageLoader("resume_pycli", f"themes/base"),
            ]
        ),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("index.html")
    html = template.render(**resume)

    return html


def export_html(resume: dict, theme: str) -> None:
    html = render_html(resume, theme)
    if "image" in resume["basics"] and resume["basics"]["image"]:
        copy(resume["basics"]["image"], "public")
    Path("public", "index.html").write_text(html)


def export_pdf(resume: dict, theme: str) -> None:
    html = render_html(resume, theme)
    pdfkit.from_string(
        html,
        str(Path("public", "index.pdf")),
    )


def serve(address: str, port: int, path: str) -> None:
    server_address = (address, port)
    ResumeHTTPRequestHandler = functools.partial(
        SimpleHTTPRequestHandler, directory=path
    )
    httpd = HTTPServer(server_address, ResumeHTTPRequestHandler)
    httpd.serve_forever()
