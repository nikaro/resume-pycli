# resume-pycli

CLI tool to build a beautiful resume from a [JSON
Resume](https://jsonresume.org/) file.

This is a Python port of
[resume-cli](https://github.com/jsonresume/resume-cli).

[![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/resume-pycli)](https://libraries.io/pypi/resume-pycli)
[![PyPI Version](https://img.shields.io/pypi/v/resume-pycli?color=4DC71F&logo=python&logoColor=fff)](https://pypi.org/project/resume-pycli/)
[![AUR Version](https://img.shields.io/aur/version/resume-pycli?logo=linux&logoColor=fff)](https://aur.archlinux.org/packages/resume-pycli/)

## Features

* Validate your `resume.json` against schema
* Export your resume to HTML
* Export your resume to PDF
* Customize the theme of your HTML and PDF exports
* Run a local HTTP server to preview the HTML export
* Create an inital `resume.json` with placeholder values to get started

## Installation

With [pipx](https://pipxproject.github.io/pipx/):

```
pipx install resume-pycli
```

With [brew](https://brew.sh/):

```
brew install nikaro/tap/resume-pycli
```

On ArchLinux from the [AUR](https://aur.archlinux.org/packages/resume-pycli/):

```
yay -S resume-pycli

# or without yay
git clone https://aur.archlinux.org/resume-pycli.git
cd resume-pycli/
makepkg -si
```

## Usage

```
Usage: resume [OPTIONS] COMMAND [ARGS]...

  CLI tool to easily setup a new resume.

Options:
  --help  Show this message and exit.

Commands:
  export    Export to HTML and PDF.
  init      Initialize a resume.json file.
  serve     Serve resume.
  validate  Validate resume's schema.
  version   Show application version.
```

Export your resume with a custom theme, for exemple one located in
`./themes/my-beautiful-theme`:

```
resume export --theme my-beautiful-theme
```

If you want to export custom version of your resume, for example a shorter one
located at `./resume.short.json`, to PDF only:

```
resume export --resume resume.short.json --pdf
```

## Themes

You can put your theme in `themes/<name>` next to your `resume.json` file. It
uses [Jinja](https://jinja.palletsprojects.com/en/3.0.x/) as templating engine.
Take a look at the [included
themes](https://github.com/nikaro/resume-pycli/tree/main/resume_pycli/themes/base)
that you can take as example to write your own.

Since it uses Jinja, it is not compatible with ["official" community
themes](https://jsonresume.org/themes/).
