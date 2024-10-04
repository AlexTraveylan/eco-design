"""
This file is the setup script for the package.
"""

from setuptools import find_packages, setup

with open("requirements.txt", mode="r", encoding="utf-8") as f:
    requirements = f.readlines()

setup(
    name="ecodesign",
    version="0.1",
    packages=find_packages(),
    install_requires=[lib.strip() for lib in requirements],
)
