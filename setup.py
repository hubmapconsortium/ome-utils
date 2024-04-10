from pathlib import Path

from setuptools import find_packages, setup

here = Path(__file__).parent.absolute()

with open(here / "README.rst", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="hubmap-ome-utils",
    version="0.2.5",
    description="OME-XML utility functions for HuBMAP computational pipelines",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/hubmapconsortium/ome-utils",
    author="Matt Ruffalo",
    author_email="mruffalo@cs.cmu.edu",
    license="GPLv3",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="ometiff",
    packages=find_packages(),
    install_requires=["pint"],
    python_requires=">=3.9",
)
