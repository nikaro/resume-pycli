from dataclasses import dataclass
from importlib.resources import files
import json
from pathlib import Path

import typer

from . import utils
from . import pdf
from . import html


app = typer.Typer(help="CLI tool to easily setup a new resume.")


@dataclass
class Options:
    """Global options."""

    resume: dict
    theme: Path


@app.callback()
def main(
    resume: Path = typer.Option(
        "resume.json",
        help="Path to the JSON resume.",
    ),
    theme: str = typer.Option(
        "",
        help="Override the theme.",
    ),
) -> None:
    Options.resume = json.loads(resume.read_text())
    Options.theme = utils.find_theme(theme or Options.resume.get("theme", "base"))


@app.command()
def validate(
    schema: Path = typer.Option(
        files("resume_pycli").joinpath("schema.json"),
        exists=True,
        dir_okay=False,
        help="Path to a custom schema to validate against.",
    ),
) -> None:
    """Validate resume's schema."""
    schema_file = json.loads(schema.read_text())
    err = utils.validate(Options.resume, schema_file)
    if err:
        typer.echo(err, err=True)
        raise typer.Exit(code=1)


@app.command()
def serve(
    host: str = typer.Option(
        "localhost",
        help="Bind address.",
    ),
    port: int = typer.Option(
        4000,
        help="Bind port.",
    ),
    browser: bool = typer.Option(
        False,
        help="Open in web browser.",
    ),
    debug: bool = typer.Option(
        False,
        help="Run in debug mode.",
    ),
) -> None:
    """Serve resume."""
    if browser:
        typer.launch(f"http://{host}:{port}/")
    html.serve(
        resume=Options.resume,
        theme=Options.theme,
        host=host,
        port=port,
        debug=debug,
    )


@app.command()
def export(
    to_pdf: bool = typer.Option(
        True,
        "--pdf",
        "--no-pdf",
        help="Export to PDF.",
    ),
    pdf_backend: pdf.Backend = typer.Option(
        "playwright",
        help="Select PDF engine.",
    ),
    to_html: bool = typer.Option(
        True,
        "--html",
        "--no-html",
        help="Export to HTML.",
    ),
    output: Path = typer.Option(
        "public",
        help="Specify the output directory.",
    ),
) -> None:
    """Export to HTML and PDF."""
    output.mkdir(parents=True, exist_ok=True)
    if to_html:
        html.export(
            resume=Options.resume,
            theme=Options.theme,
            output=output,
        )
    if to_pdf:
        pdf.export(
            resume=Options.resume,
            theme=Options.theme,
            output=output,
            engine=pdf_backend,
        )
