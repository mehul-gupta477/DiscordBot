import nox


@nox.session
def tests(session: nox.Session) -> None:
    """Run the test suite with coverage."""
    session.install("-r", "requirements.txt")
    session.install("coverage[toml]")

    # Run tests with coverage
    session.run(
        "coverage",
        "run",
        "-m",
        "unittest",
        "discover",
        "-s",
        "tests",
        "-p",test",
        "discover",
        "-s",
        "tests",
        "-p",
        # We use *_test.py pattern for our tests
        "*_test.py",
    )

    # Generate coverage report
    session.run("coverage", "report", "--fail-under=90")

    # Generate XML report for Codecov
    session.run("coverage", "xml")

    # Generate HTML report for local viewing
    session.run("coverage", "html")


@nox.session
def format(session: nox.Session) -> None:
    """Format te HTML report for local viewing
    session.run("coverage", "html")


@nox.session
def format(session: nox.Session) -> None:
    """Format code with black."""
    session.install("black")
    session.run("black", ".")


@nox.session
def lint(session: nox.Session) -> None:
    """Run linting checks."""
    session.install("ruff")
    session.run("ruff", "check", "--fix", ".")
on.install("ruff")
    session.run("ruff", "check", "--fix", ".")
