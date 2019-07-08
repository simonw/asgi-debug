from setuptools import setup
import os

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="asgi-debug",
    description="ASGI middleware for debugging ASGI applications",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/asgi-debug",
    license="Apache License, Version 2.0",
    version=VERSION,
    py_modules=["asgi_debug"],
    extras_require={"test": ["pytest", "pytest-asyncio", "asgiref==3.1.2"]},
    setup_requires=["pytest-runner"],
)
