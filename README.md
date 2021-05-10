# resume-pycli

CLI tool to build a beautiful resume from a [JSON Resume](https://jsonresume.org/) file.

This is a Python port of [resume-cli](https://github.com/jsonresume/resume-cli).

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
```

## Themes

You can put your theme in `themes/<name>` next to your `resume.json` file. It uses [Jinja2](https://jinja2docs.readthedocs.io/en/stable/) as templating engine. Take a look at the [small demo](https://git.sr.ht/~nka/resume-pycli/tree/main/item/src/resume_pycli/themes/base/) that you can take as example to write your own.

It is not compatible with ["official" community themes](https://jsonresume.org/themes/) and at the moment i have not included a beautiful one.
