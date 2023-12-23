from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.readlines()

setup(
    name="guitoolbox",
    version="0.0.2",
    description="GUI for toolboxes",
    packages=find_packages(),
    install_requires=requirements,
    # Currently there is a bug that makes the GUI toolbox crash with a different python version
    python_requires="~=3.9",
)
