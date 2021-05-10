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


def export(resume: dict, theme: str) -> None:
    # render resume from template
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

    # ensure output directory exists
    Path("public").mkdir(parents=True, exist_ok=True)

    # export to output directory
    if "image" in resume["basics"] and resume["basics"]["image"]:
        copy(resume["basics"]["image"], "public")
    Path("public", "index.html").write_text(html)
    pdfkit.from_file(
        str(Path("public", "index.html")),
        str(Path("public", "index.pdf")),
    )


def serve(address: str, port: int, path: str) -> None:
    server_address = (address, port)
    ResumeHTTPRequestHandler = functools.partial(
        SimpleHTTPRequestHandler, directory=path
    )
    httpd = HTTPServer(server_address, ResumeHTTPRequestHandler)
    httpd.serve_forever()
