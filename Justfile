package := 'casualcms'
default_test_suite := 'tests/unittests'
default_functest_suite := 'tests/functionals/'

fmt: black

test: flake8 mypy pytest functest


flake8:
    poetry run flake8 && echo "$(tput setaf 10)Success: no lint issue$(tput setaf 7)"

mypy:
    poetry run mypy src/ tests/

black:
    poetry run isort .
    poetry run black .

pytest test_suite=default_test_suite:
    poetry run pytest -sxv {{test_suite}}

lf:
    poetry run pytest -sxvvv --lf

buildcss:
    poetry run tailwindcss -i ./src/todolist/ui/assets/styles/main.css -o ./src/todolist/ui/static/css/main.css

cov test_suite=default_test_suite:
    rm -f .coverage
    rm -rf htmlcov
    poetry run pytest --cov-report=html --cov={{package}} {{test_suite}}
    xdg-open htmlcov/index.html

functest test_suite=default_functest_suite:
    poetry run behave --tags=-dev --no-capture {{test_suite}}

funcdevtest: buildcss
    poetry run behave --tags=dev --no-capture tests/functionals/

servetest:
    poetry run python tests/functionals/fixtures.py

install:
    poetry install
