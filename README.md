## Getting Started

Install cookiecutter with `brew install cookiecutter` or `pip install cookiecutter`.

```
cookiecutter gh:prodinit/django-boilerplate
```

## Install requirements
Activate the virtualenv with `source {venv-name}/bin/activate`.

```
poetry install
```

## Add new library
Activate the virtualenv with `source {venv-name}/bin/activate`.

```
poetry add {library-name}
```

## Managing dependencies

### Poetry

To guarantee repeatable installations, all project dependencies are managed using [Poetry](https://python-poetry.org/). The project’s direct dependencies are listed in `pyproject.toml`. Running poetry lock generates poetry.lock which has all versions pinned.

You can install Poetry by using `pip install --pre poetry` or by following the official installation guide [here](https://github.com/python-poetry/poetry#installation).

*Tip:* We recommend that you use this workflow and keep `pyproject.toml` as well as `poetry.lock` under version control to make sure all computers and environments run exactly the same code.

### Other tools

For compatibility, `requirements.txt` and `requirements_dev.txt` can be updated by running

```bash
poetry export --without-hashes -f requirements.txt -o requirements.txt
```
