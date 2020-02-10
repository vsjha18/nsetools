from setuptools import setup, find_packages

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
    long_description=pathlib.Path('README.md').read_text('utf-8'),
    long_description_content_type="text/markdown",
)
