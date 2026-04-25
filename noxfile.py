import nox


@nox.session(python=["3.10", "3.11", "3.12", "3.13"])
def tests(session: nox.Session) -> None:
    session.run("python", "-m", "pip", "install", "--upgrade", "pip")
    session.install(".")
    session.install(
        "pytest",
        "coverage",
        "freezegun",
        "pytest-asyncio",
    )
    session.run("python", "-c", "import sys; print(sys.executable); print(sys.version)")
    session.run("pytest")
