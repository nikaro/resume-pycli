#!/usr/bin/env python3

import click
import json
from pathlib import Path

import resume_pycli
import resume_pycli.utils as u


@click.group()
def cli() -> None:
    """CLI tool to easily setup a new resume."""
    pass


@click.command()
@click.option(
    "--resume",
    default="resume.json",
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
    help="Path to the resume in json format.",
    type=click.File(),
)
@click.option(
    "--schema", help="Path to a custom schema to validate against.", type=click.File()
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
        exit(1)



@click.command()
@click.option("--port", default=4000, help="Serve on a custom port.")
@click.option("--dir", default="public", help="Serve a custom directory.")
@click.option("--silent", is_flag=True, help="Do not open web browser.")
def serve(port, dir, silent) -> None:
    """Serve resume."""
    click.echo(f"Serving on http://localhost:{port}/ ...")
    if not silent:
        click.launch(f"http://localhost:{port}/")
    u.serve("localhost", port, dir)

@click.command()
@click.option(
    "--resume",
    default="resume.json",
    help="Path to the resume in json format.",
    type=click.File(),
)
@click.option("--theme", help="Specify the to used to build the resume.")
@click.option("--pdf", is_flag=True, help="Export to PDF only.")
@click.option("--html", is_flag=True, help="Export to HTML only.")
def export(resume, theme, pdf, html) -> None:
    """Export to HTML and PDF."""
    resume_file = json.load(resume)
    if not theme:
        theme = resume_file["meta"].get("theme", "base")
    Path("public").mkdir(parents=True, exist_ok=True)
    if html or not pdf:
        u.export_html(resume_file, theme)
    if pdf or not html:
        u.export_pdf(resume_file, theme)


@click.command()
def version() -> None:
    """Show application version."""
    click.echo(resume_pycli.__version__)


cli.add_command(version)
cli.add_command(init)
cli.add_command(validate)
cli.add_command(export)
cli.add_command(serve)
