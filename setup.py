import setuptools
from distutils.core import setup
import versioneer

## base requirements
install_requires = open("requirements.txt").read().strip().split("\n")
dev_requires = open("requirements.dev.txt").read().strip().split("\n")

extras = {"dev": dev_requires}

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    name="nugflow",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    install_requires=install_requires,
    packages=setuptools.find_packages(),
    license="Having no license, this work is under exclusive copyright by default.",
    long_description=readme,
)
