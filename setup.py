from distutils.core import setup

from jsonlogging import __version__

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
    version=get_version("jsonlogging/__init__.py"),
    packages=["jsonlogging"],
    license="BSD",
    long_description=open("README.md").read()
)
