#!/usr/bin/env python3

from importlib.resources import files
import json
from pathlib import Path

import typer

from resume_pycli import __version__
from resume_pycli import utils


app = typer.Typer(help="CLI tool to easily setup a new resume.")


@app.command()
def init(
    resume: typer.FileTextWrite = typer.Option(
        "resume.json",
        mode="x",
        help="Path to the resume in json format.",
    )
) -> None:
    """Initialize a resume.json file."""
    source = files("resume_pycli").joinpath("resume.json").read_text()
    resume.write(source)
    typer.echo("resume.json created")


@app.command()
def validate(
    resume: Path = typer.Option(
        Path("resume.json"),
        exists=True,
        dir_okay=False,
        help="Path to the resume in json format.",
    ),
    schema: Path = typer.Option(
        files("resume_pycli").joinpath("schema.json"),
        exists=True,
        dir_okay=False,
        help="Path to a custom schema to validate against.",
    ),
) -> None:
    """Validate resume's schema."""
    resume_file = json.loads(resume.read_text())
    schema_file = json.loads(schema.read_text())
    err = utils.validate(resume_file, schema_file)
    if err:
        typer.echo(err, err=True)
        raise typer.Exit(code=1)


@app.command()
def serve(
    host: str = typer.Option(
        "localhost",
        help="Specify alternate bind address",
    ),
    port: int = typer.Option(
        4000,
        help="Serve on a custom port.",
    ),
    path: Path = typer.Option(
        Path("public"),
        exists=True,
        file_okay=False,
        help="Serve a custom directory.",
    ),
    silent: bool = typer.Option(False, help="Do not open web browser."),
) -> None:
    """Serve resume."""
    typer.echo(f"Serving on http://{host}:{port}/ ...")
    if not silent:
        typer.launch(f"http://{host}:{port}/")
    utils.serve(host, port, path, silent)


@app.command()
def export(
    resume: Path = typer.Option(
        Path("resume.json"),
        help="Path to the resume in json format.",
    ),
    theme: str = typer.Option(
        "",
        help="Specify the to used to build the resume.",
    ),
    pdf: bool = typer.Option(
        True,
        help="Export to PDF.",
    ),
    html: bool = typer.Option(
        True,
        help="Export to HTML.",
    ),
    output: Path = typer.Option(
        "public",
        help="Specify the output directory.",
    ),
) -> None:
    """Export to HTML and PDF."""
    resume_file = json.loads(resume.read_text())
    if not theme:
        theme = resume_file["meta"].get("theme", "base")
    output.mkdir(parents=True, exist_ok=True)
    if html:
        utils.export_html(resume_file, theme, output)
    if pdf:
        utils.export_pdf(resume_file, theme, output)


@app.command()
def version() -> None:
    """Show application version."""
    typer.echo(__version__)
