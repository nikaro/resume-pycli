#!/usr/bin/env python3

import json
from pathlib import Path
import sys

import click

import resume_pycli
import resume_pycli.utils as u


@click.group()
def cli() -> None:
    """CLI tool to easily setup a new resume."""


@click.command()
@click.option(
    "--resume",
    default="resume.json",
    metavar="PATH",
    help="Path to the resume in json format.",
    type=click.File("x"),
)
def init(resume) -> None:
    """Initialize a resume.json file."""
    source = Path(__file__).parent.joinpath("resume.json").read_text()
    resume.write(source)
    click.echo("resume.json created")


@click.command()
@click.option(
    "--resume",
    default="resume.json",
    metavar="PATH",
    help="Path to the resume in json format.",
    type=click.File(),
)
@click.option(
    "--schema", metavar="PATH", help="Path to a custom schema to validate against.", type=click.File()
)
def validate(resume, schema) -> None:
    """Validate resume's schema."""
    resume_file = json.load(resume)
    if not schema:
        schema = Path(__file__).parent.joinpath("schema.json").open()
    schema_file = json.load(schema)
    err = u.validate(resume_file, schema_file)
    if err:
        click.echo(err, err=True)
        sys.exit(1)


@click.command()
@click.option("--bind", default="localhost", metavar="ADDR", help="Specify alternate bind address")
@click.option("--port", default=4000, metavar="PORT", help="Serve on a custom port.")
@click.option("--path", default="public", metavar="PATH", help="Serve a custom directory.")
@click.option("--silent", is_flag=True, help="Do not open web browser.")
def serve(bind, port, path, silent) -> None:
    """Serve resume."""
    click.echo(f"Serving on http://{bind}:{port}/ ...")
    if not silent:
        click.launch(f"http://{bind}:{port}/")
    u.serve(bind, port, path, silent)


@click.command()
@click.option(
    "--resume",
    default="resume.json",
    metavar="PATH",
    help="Path to the resume in json format.",
    type=click.File(),
)
@click.option("--theme", metavar="NAME", help="Specify the to used to build the resume.")
@click.option("--pdf", is_flag=True, help="Export to PDF only.")
@click.option(
    "--pdf-options",
    metavar="OPTS",
    help='Pass options as quoted Python dict to wkhtmltopdf (ex: \'{"page-size": "A4"}\').',
    default="{}",
    callback=u.cb_pdf_options,
)
@click.option("--html", is_flag=True, help="Export to HTML only.")
@click.option("--output", metavar="PATH", help="Specify the output directory.", default="public")
def export(resume, theme, pdf, pdf_options, html, output) -> None:
    """Export to HTML and PDF."""
    resume_file = json.load(resume)
    if not theme:
        theme = resume_file["meta"].get("theme", "base")
    Path("public").mkdir(parents=True, exist_ok=True)
    if html or not pdf:
        u.export_html(resume_file, theme, output)
    if pdf or not html:
        u.export_pdf(resume_file, theme, output, pdf_options)


@click.command()
def version() -> None:
    """Show application version."""
    click.echo(resume_pycli.__version__)


cli.add_command(version)
cli.add_command(init)
cli.add_command(validate)
cli.add_command(export)
cli.add_command(serve)
