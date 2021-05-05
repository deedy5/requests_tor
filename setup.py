from setuptools import setup
from requests_tor import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="requests_tor",
    version=__version__,
    author="deedy5",
    description="Multithreading requests via TOR with automatic TOR new identity",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deedy5/requests_tor",
    license="MIT",
    py_modules=["requests_tor"],
    install_requires=["requests>=2.25.0", "stem>=1.8.0"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",       
    ],
    python_requires=">=3.6",
    zip_safe=False,
)
