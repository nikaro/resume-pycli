from click.testing import CliRunner
import json
from pathlib import Path
import re
from shutil import copytree
import tomli

import resume_pycli
from resume_pycli.script import cli


def test_version():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["version"])
        assert result.exit_code == 0
        assert re.match(r"^(:?\d+)\.(:?\d+)\.(:?\d+)", result.output.strip())


def test_version_match_pyproject():
    with Path(__file__).parent.parent.joinpath("pyproject.toml").open(mode="rb") as f:
        pyproject = tomli.load(f)
    major, minor, patch, pre, _ = re.match(
        r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$",
        pyproject["tool"]["poetry"]["version"],
    ).groups()
    pyproject_version = f"{major}.{minor}.{patch}"
    if pre:
        pyproject_version = f"{pyproject_version}{pre[:1]}{pre.split('.')[-1]}"
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["version"])
        cli_version = result.output.strip()
        assert cli_version == pyproject_version


def test_init():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["init"])
        assert result.exit_code == 0
        assert Path("resume.json").exists()
        assert result.output == "resume.json created\n"


def test_init_already_exists():
    runner = CliRunner()
    with runner.isolated_filesystem():
        Path("resume.json").touch()
        result = runner.invoke(cli, ["init"])
        assert result.exit_code == 2


def test_validate():
    runner = CliRunner()
    with runner.isolated_filesystem():
        resume = Path(resume_pycli.__file__).parent.joinpath("resume.json").read_text()
        Path("resume.json").write_text(resume)
        result = runner.invoke(cli, ["validate"])
        assert result.exit_code == 0


def test_validate_bad_key():
    runner = CliRunner()
    with runner.isolated_filesystem():
        Path("resume.json").write_text('{"bad_key": "random value"}')
        result = runner.invoke(cli, ["validate"])
        assert result.exit_code == 1


def test_export():
    runner = CliRunner()
    with runner.isolated_filesystem():
        resume = Path(resume_pycli.__file__).parent.joinpath("resume.json").read_text()
        Path("resume.json").write_text(resume)
        result = runner.invoke(cli, ["export"])
        assert result.exit_code == 0
        assert Path("public", "index.html").exists()
        assert Path("public", "index.pdf").exists()


def test_export_pdf_only():
    runner = CliRunner()
    with runner.isolated_filesystem():
        resume = Path(resume_pycli.__file__).parent.joinpath("resume.json").read_text()
        Path("resume.json").write_text(resume)
        result = runner.invoke(cli, ["export", "--pdf"])
        assert result.exit_code == 0
        assert Path("public", "index.pdf").exists()
        assert not Path("public", "index.html").exists()


def test_export_pdf_options():
    runner = CliRunner()
    with runner.isolated_filesystem():
        resume = Path(resume_pycli.__file__).parent.joinpath("resume.json").read_text()
        Path("resume.json").write_text(resume)
        result = runner.invoke(
            cli, ["export", "--pdf", "--pdf-options", "{'page-size': 'A4'}"]
        )
        assert result.exit_code == 0
        assert Path("public", "index.pdf").exists()
        assert not Path("public", "index.html").exists()


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
        result = runner.invoke(cli, ["export", "--theme", "custom"])
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
        result = runner.invoke(cli, ["export"])
        assert result.exit_code == 0
        assert Path("public", "index.html").exists()
        assert Path("public", "index.pdf").exists()


def test_export_stackoverflow_theme():
    runner = CliRunner()
    with runner.isolated_filesystem():
        lib_dir = Path(resume_pycli.__file__).parent
        resume = lib_dir.joinpath("resume.json").read_text()
        Path("resume.json").write_text(resume)
        result = runner.invoke(cli, ["export", "--theme", "stackoverflow"])
        assert result.exit_code == 0
        assert Path("public", "index.html").exists()
        assert Path("public", "index.pdf").exists()
        assert Path("public", "assets").is_dir()


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
        result = runner.invoke(cli, ["export", "--theme", "stackoverflow"])
        assert result.exit_code == 0
        assert Path("public", "index.html").exists()
        assert Path("public", "index.pdf").exists()
        assert Path("public", "assets").is_dir()
