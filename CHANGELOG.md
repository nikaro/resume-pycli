## Unreleased


## v4.1.0 - 2023-02-13

### Build

- deps-dev: bump ruff from 0.0.244 to 0.0.246
- deps-dev: bump ruff from 0.0.243 to 0.0.244
- deps-dev: bump ruff from 0.0.241 to 0.0.243
- deps-dev: bump types-jsonschema from 4.17.0.3 to 4.17.0.4
- deps-dev: bump ruff from 0.0.239 to 0.0.241
- deps-dev: bump black from 22.12.0 to 23.1.0
- deps-dev: bump ruff from 0.0.238 to 0.0.239
- deps-dev: bump types-beautifulsoup4 from 4.11.6.4 to 4.11.6.5

### Features

- pdf: add multiple pdf engine choices

### Refactor

- split utils to pdf and html libs
- html: export and serve content through flask


## v4.0.0 - 2023-02-01

### Build

- deps-dev: bump ruff from 0.0.237 to 0.0.238

### Refactor

- replace __file__ by importlib.resources
- replace lib click by typer


## v3.0.1 - 2023-01-29

### Bug Fixes

- do not auto-install playwright dependencies


## v3.0.0 - 2023-01-29

### Build

- python 3.8 minimum version
- deps: bump jsonschema from 4.4.0 to 4.17.3
- deps: bump beautifulsoup4 from 4.10.0 to 4.11.1
- deps: bump jinja2 from 3.0.3 to 3.1.2
- deps: bump click from 8.0.4 to 8.1.3
- deps-dev: bump pytest from 7.1.1 to 7.2.1

### Refactor

- replace pdfkit by playwright


## v2.0.0 - 2022-03-24

### Build

- update deps versions and set min python to 3.7


## v1.3.4 - 2021-07-04

### Build

- set min python version to 3.6

### Features

- add flag to pass bind address for serve command


## v1.3.3 - 2021-06-06

### Bug Fixes

- suppress server output with silent flag
- remove debug print


## v1.3.2 - 2021-06-06

### Bug Fixes

- copy themes assets into output folder
- serve themes assets locally


## v1.3.1 - 2021-06-05

### Bug Fixes

- pdf not rendering css and images correctly

### Features

- allow to pass options to wkhtmltopdf


## v1.3.0 - 2021-06-01

### Bug Fixes

- suppress wkhtmltopdf output
- give more control over profile icon

### Build

- update dependencies

### Features

- add flat theme


## v1.2.0 - 2021-05-18

### Bug Fixes

- cannot export pdf resume with image

### Features

- add version command
- add stackoverflow theme


## v1.1.3 - 2021-05-16

### Bug Fixes

- package could not be imported


## v1.1.2 - 2021-05-16

### Bug Fixes

- export: allow usage of custom themes

### Build

- include tests into package


## v1.1.1 - 2021-05-15

### Build

- update dependencies


## v1.1.0 - 2021-05-11

### Features

- add flags to build pdf-only or html-only


## v1.0.0 - 2021-05-11

