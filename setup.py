import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="param_to_json",
    version="0.1",
    author="Mikael Trellet",
    author_email="mikael.trellet@gmail.com",
    description="HADDOCK2.4 parameter file tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mtrellet/haddock_param_tools",
    packages=setuptools.find_packages(),
    test_suite='nose.collector',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
    ],
)
