import pathlib
from setuptools import setup, find_packages


here = pathlib.Path(__file__).parent


def load_long_description():
    paths = [here, here / 'nsetools']
    for countdown, path in reversed(list(enumerate(paths))):
        try:
            return (path / 'README.md').read_text('utf-8')
        except FileNotFoundError:
            if countdown == 0:
                raise


setup(
    name="nsetools",
    version="1.0.11",
    author="Vivek Jha",
    author_email="vsjha18@gmail.com",
    description="Python library for extracting realtime data from National Stock Exchange",
    license="MIT",
    keywords="nse quote market",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires=">=3",
    install_requires=['six', 'dateutils'],
    url="http://vsjha18.github.com/nsetools",
    packages=find_packages(),
    long_description=load_long_description(),
    long_description_content_type="text/markdown",
)
