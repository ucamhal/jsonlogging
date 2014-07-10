from setuptools import setup


def get_version(filename):
    """
    Parse the value of the __version__ var from a Python source file
    without running/importing the file.
    """
    import re
    version_pattern = r"^ *__version__ *= *['\"](\d+\.\d+\.\d+)['\"] *$"
    match = re.search(version_pattern, open(filename).read(), re.MULTILINE)

    assert match, ("No version found in file: {!r} matching pattern: {!r}"
                   .format(filename, version_pattern))

    return match.group(1)

setup(
    name="jsonlogging",
    description="jsonlogging provides structured log output from the "
                "logging module in JSON format",
    author="Hal Blackburn",
    author_email="hwtb2@cam.ac.uk",
    url="https://github.com/ucamhal/ravenpy",
    version=get_version("jsonlogging/__init__.py"),
    packages=["jsonlogging"],
    license="BSD",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: System :: Logging"
    ],
    long_description=open("README.md").read(),
    test_suite="jsonlogging.tests.test_all",
    tests_require="mock >= 1.0.0, < 2.0.0"
)
