from enum import Enum
import os
from pathlib import Path
import subprocess

from .utils import serve_bg


class Backend(str, Enum):
    # https://playwright.dev/python/
    playwright = "playwright"
    # https://doc.courtbouillon.org/weasyprint/stable/
    weasyprint = "weasyprint"
    # https://pdfshift.io/
    # pdfshift = "pdfshift"
    # https://docraptor.com/
    # docraptor = "docraptor"


def export(*, resume: dict, theme: Path, output: Path, engine: Backend) -> None:
    if engine == Backend.playwright:
        export_playwright(resume=resume, theme=theme, output=output)
    elif engine == Backend.weasyprint:
        export_weasyprint(resume=resume, theme=theme, output=output)
    else:
        raise Exception("unsupported pdf engine")


def export_playwright(*, resume: dict, theme: Path, output: Path) -> None:
    from playwright.sync_api import sync_playwright

    port = serve_bg(resume=resume, theme=theme)
    # enable playwright debug output
    os.environ["DEBUG"] = "pw:api"
    with sync_playwright() as p:
        chromium = p.chromium
        if not Path(chromium.executable_path).exists():
            subprocess.run(["playwright", "install", "chromium"], check=True)
        browser = chromium.launch()
        page = browser.new_page()
        page.goto(url=f"http://localhost:{port}")
        page.pdf(path=str(output / "index.pdf"), format="A4")
        browser.close()


def export_weasyprint(*, resume: dict, theme: Path, output: Path) -> None:
    from weasyprint import CSS, HTML  # type: ignore

    port = serve_bg(resume=resume, theme=theme)
    styles = [CSS(string="@page { size: A4 }")]
    HTML(f"http://localhost:{port}").write_pdf(output / "index.pdf", stylesheets=styles)
