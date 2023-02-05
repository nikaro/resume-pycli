from pathlib import Path
from shutil import copytree

from flask import Flask
from flask import render_template


def export(resume: dict, theme: Path, output: Path) -> None:
    # render resume to html
    app = Flask(
        import_name="resume_pycli",
        template_folder=f"{theme}",
        static_folder=f"{theme.joinpath('static')}",
    )
    with app.app_context():
        html = render_template("index.html", **resume)
    # copy assets into ourput directory
    if (static := theme.joinpath("static")).is_dir():
        copytree(static, output.joinpath("static"), dirs_exist_ok=True)
    # write html output
    output.joinpath("index.html").write_text(html)


def serve(
    *,
    resume: dict,
    theme: Path,
    host: str = "localhost",
    port: int = 4000,
    debug: bool = False,
) -> None:
    app = Flask(
        import_name="resume_pycli",
        template_folder=f"{theme}",
        static_folder=f"{theme.joinpath('static')}",
    )

    @app.route("/")
    def index():
        return render_template("index.html", **resume)

    app.run(host=host, port=port, debug=debug)
