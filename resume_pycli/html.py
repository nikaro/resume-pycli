from base64 import b64encode
from importlib.resources import as_file
from importlib.resources import files
from pathlib import Path
from shutil import copytree

from bs4 import BeautifulSoup
from jinja2 import (
    Environment,
    FileSystemLoader,
    select_autoescape,
)


def render(resume: dict, theme: str) -> str:
    lib_dir = files("resume_pycli")
    env = Environment(
        loader=FileSystemLoader(
            [
                str(Path.cwd().joinpath("themes").joinpath(theme)),
                str(lib_dir.joinpath("themes").joinpath(theme)),
            ]
        ),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("index.html")
    html = template.render(**resume)

    return html


def export(resume: dict, theme: str, output: Path) -> None:
    if "image" in resume["basics"] and resume["basics"]["image"]:
        with open(resume["basics"]["image"], "rb") as image_file:
            resume["basics"]["image_b64"] = b64encode(image_file.read()).decode()
    html = render(resume, theme)
    output.joinpath("index.html").write_text(html)
    # find theme directory
    if (cwd_theme := Path.cwd().joinpath("themes").joinpath(theme)).is_dir():
        theme_dir = cwd_theme
    elif (
        lib_theme := files("resume_pycli").joinpath("themes").joinpath(theme)
    ).is_dir():
        with as_file(lib_theme) as lib_theme_p:
            theme_dir = lib_theme_p
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
    assets_uniq = set(assets)
    for asset in assets_uniq:
        copytree(
            Path.joinpath(theme_dir, asset),
            output.joinpath(asset),
            dirs_exist_ok=True,
        )
