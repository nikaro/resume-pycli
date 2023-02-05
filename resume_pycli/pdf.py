from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import threading

from playwright.sync_api import sync_playwright

from . import html
from . import utils


def export(resume: dict, theme: Path, output: Path) -> None:
    # export html in a random temporary directory
    tmpdir = TemporaryDirectory()
    html.export(resume, theme, Path(tmpdir.name))
    # increment port if already in use
    port = 4001
    while utils.check_port(port):
        port += 1
    # run server in background
    daemon = threading.Thread(
        target=html.serve, args=("localhost", port, False, resume, theme), daemon=True
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
