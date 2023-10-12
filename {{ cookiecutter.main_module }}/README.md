{{ cookiecutter.project_name }}
==============================

__Version:__ {{ cookiecutter.version }}

{{ cookiecutter.project_description }}

## Features
- Django Rest Framework Project Setup
- Authentication and Authorization
    > /api/login: This API takes email, password and returns jwt token

    > /api/signup: This API takes email, password and sends and sends an account activation email 

    > /api/activate?token=: This is the account activation email link

    > /api/logout: This API logs out the current user

    > /api/password_change: This API takes new_password of a logged in user and updates the current password

    > /api/password_reset: This API takes the email of user and sends an email with the instructions ot reset the password

    > /api/password_reset_confirm: This API takees the new_password and confirms the reset password with a reset password token in the query params

- Google Auth
- Payment gateway module setup
- Celery setup
    > To run Celery: `celery -A {{ cookiecutter.main_module }} worker -l info`

    > To run Celery Beat: `celery -A {{ cookiecutter.main_module }} beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler`
- AWS clients and util functions
- Pytest setup
- Github Actions
    > spell_check

    > black_check
    
    > pydoc_check
    
    > password_check
    
    > test_cases
    
    > terraform_validate
- Dockerfile.django for backend
- Dockerfile.nginx for reverse proxy

## Getting up and running

Minimum requirements: **pip, python3.9, poetry, redis & [PostgreSQL 11][install-postgres]**, setup is tested on Mac OSX only.

```
brew install python3 poetry libmagic postgres
```

[install-postgres]: http://www.gotealeaf.com/blog/how-to-install-postgresql-on-a-mac

### Poetry

To guarantee repeatable installations, all project dependencies are managed using [Poetry](https://python-poetry.org/). The project’s direct dependencies are listed in `pyproject.toml`.
Running `poetry lock` generates `poetry.lock` which has all versions pinned.

You can install Poetry by using `pip install --pre poetry` or by following the official installation guide [here](https://github.com/python-poetry/poetry#installation).

*Tip:* We recommend that you use this workflow and keep `pyproject.toml` as well as `poetry.lock` under version control to make sure all computers and environments run exactly the same code.

### Celery
To run Celery
`celery -A {{ cookiecutter.main_module }} worker -l info`

To run Celery Beat:
`celery -A {{ cookiecutter.main_module }} beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler`

### Other tools

For compatibility, `requirements.txt` and `requirements_dev.txt` can be updated by running

```bash
poetry export --without-hashes -f requirements.txt -o requirements.txt
```

and

```bash
poetry export --without-hashes -f requirements.txt -o requirements_dev.txt --with dev
```

, respectively.

## Contributing

Golden Rule:

> Anything in **main** is always **deployable**.

Avoid working on `main` branch, create a new branch with meaningful name, send pull request asap. Be vocal!
