import sys

import nox


@nox.session
def lint(session):
    session.run("black", "--check", ".")
    session.run("flake8", ".")
    session.run("isort", "-q", ".")


@nox.session
@nox.parametrize("django", ["3.2", "4.0", "main"])
def test(session, django):
    if django == "main":
        session.install("https://github.com/django/django/archive/main.tar.gz")  # noqa E501
    else:
        session.install(f"django=={django}")
    session.run("coverage", "run", "-m", "pytest", "tests")
    session.run("coverage", "report")
    session.run("coverage", "xml")
