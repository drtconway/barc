import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="barc",
    version="0.1.0",
    author="Thomas Conway",
    author_email="drtomc@gmail.com",
    description="A simple tool for producing sheets of barcode labels",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/drtconway/barc",
    packages=setuptools.find_packages(),
    entry_points = {
        'console_scripts': ['barc=barc.cli:main'],
    },
    install_requires=[
        "docopt",
        "dominate",
        "pyaml",
        "python-barcode",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache 2.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
