from typer.testing import CliRunner
import json
from pathlib import Path
from shutil import copytree

import resume_pycli
from resume_pycli.cli import app


def test_validate():
    runner = CliRunner()
    with runner.isolated_filesystem():
        resume = Path(resume_pycli.__file__).parent.joinpath("resume.json").read_text()
        Path("resume.json").write_text(resume)
        result = runner.invoke(app, ["validate"])
        assert result.exit_code == 0


def test_validate_bad_key():
    runner = CliRunner()
    with runner.isolated_filesystem():
        Path("resume.json").write_text('{"bad_key": "random value"}')
        result = runner.invoke(app, ["validate"])
        assert result.exit_code != 0


def test_export():
    runner = CliRunner()
    with runner.isolated_filesystem():
        resume = Path(resume_pycli.__file__).parent.joinpath("resume.json").read_text()
        Path("resume.json").write_text(resume)
        result = runner.invoke(app, ["export"])
        assert result.exit_code == 0
        assert Path("public", "index.html").exists()
        assert Path("public", "index.pdf").exists()


def test_export_no_html():
    runner = CliRunner()
    with runner.isolated_filesystem():
        resume = Path(resume_pycli.__file__).parent.joinpath("resume.json").read_text()
        Path("resume.json").write_text(resume)
        result = runner.invoke(app, ["export", "--no-html"])
        assert result.exit_code == 0
        assert Path("public", "index.pdf").exists()
        assert not Path("public", "index.html").exists()


def test_export_no_pdf():
    runner = CliRunner()
    with runner.isolated_filesystem():
        resume = Path(resume_pycli.__file__).parent.joinpath("resume.json").read_text()
        Path("resume.json").write_text(resume)
        result = runner.invoke(app, ["export", "--no-pdf"])
        assert result.exit_code == 0
        assert Path("public", "index.html").exists()
        assert not Path("public", "index.pdf").exists()


def test_export_custom_theme():
    runner = CliRunner()
    with runner.isolated_filesystem():
        lib_dir = Path(resume_pycli.__file__).parent
        resume = lib_dir.joinpath("resume.json").read_text()
        copytree(
            lib_dir.joinpath("themes", "base"),
            Path.cwd().joinpath("themes", "custom"),
            dirs_exist_ok=True,
        )
        Path("resume.json").write_text(resume)
        result = runner.invoke(app, ["--theme", "custom", "export"])
        assert result.exit_code == 0
        assert Path("public", "index.html").exists()
        assert Path("public", "index.pdf").exists()


def test_export_with_image():
    runner = CliRunner()
    with runner.isolated_filesystem():
        lib_dir = Path(resume_pycli.__file__).parent
        # create a dummy image and inject it into resume.json
        image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
        with open("image.jpg", "wb") as image_file:
            image_file.write(image.encode())
        resume = json.loads(lib_dir.joinpath("resume.json").read_text())
        resume["basics"]["image"] = "image.jpg"
        Path("resume.json").write_text(json.dumps(resume))
        result = runner.invoke(app, ["export"])
        assert result.exit_code == 0
        assert Path("public", "index.html").exists()
        assert Path("public", "index.pdf").exists()


def test_export_stackoverflow_theme():
    runner = CliRunner()
    with runner.isolated_filesystem():
        lib_dir = Path(resume_pycli.__file__).parent
        resume = lib_dir.joinpath("resume.json").read_text()
        Path("resume.json").write_text(resume)
        result = runner.invoke(app, ["--theme", "stackoverflow", "export"])
        assert result.exit_code == 0
        assert Path("public", "index.html").exists()
        assert Path("public", "index.pdf").exists()
        assert Path("public", "static").is_dir()


def test_export_stackoverflow_theme_with_image():
    runner = CliRunner()
    with runner.isolated_filesystem():
        lib_dir = Path(resume_pycli.__file__).parent
        # create a dummy image and inject it into resume.json
        image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
        with open("image.jpg", "wb") as image_file:
            image_file.write(image.encode())
        resume = json.loads(lib_dir.joinpath("resume.json").read_text())
        resume["basics"]["image"] = "image.jpg"
        Path("resume.json").write_text(json.dumps(resume))
        result = runner.invoke(app, ["--theme", "stackoverflow", "export"])
        assert result.exit_code == 0
        assert Path("public", "index.html").exists()
        assert Path("public", "index.pdf").exists()
        assert Path("public", "static").is_dir()


def test_export_pdf_backend_playwright():
    runner = CliRunner()
    with runner.isolated_filesystem():
        resume = Path(resume_pycli.__file__).parent.joinpath("resume.json").read_text()
        Path("resume.json").write_text(resume)
        result = runner.invoke(
            app, ["export", "--no-html", "--pdf-backend", "playwright"]
        )
        assert result.exit_code == 0
        assert Path("public", "index.pdf").exists()


def fake_pdf(*args, **kwargs):
    Path("public/index.pdf").write_bytes(b"")


def test_export_pdf_backend_weasyprint(mocker):
    mocker.patch("resume_pycli.pdf.export_weasyprint", wraps=fake_pdf)
    runner = CliRunner()
    with runner.isolated_filesystem():
        resume = Path(resume_pycli.__file__).parent.joinpath("resume.json").read_text()
        Path("resume.json").write_text(resume)
        result = runner.invoke(
            app, ["export", "--no-html", "--pdf-backend", "weasyprint"]
        )
        assert result.exit_code == 0
        assert Path("public", "index.pdf").exists()
