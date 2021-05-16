from click.testing import CliRunner
from pathlib import Path
from shutil import copytree

import resume_pycli
from resume_pycli.script import cli


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
