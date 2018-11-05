import setuptools
import os
import shutil

if not os.path.exists('build/_scripts'):
    os.makedirs('build/_scripts')
shutil.copyfile('scripts/haddock_param_extract_pdb.py', 'build/_scripts/hp_extract_pdb')
shutil.copyfile('scripts/haddock_param_summary.py', 'build/_scripts/hp_summary')
shutil.copyfile('scripts/haddock_param_replace.py', 'build/_scripts/hp_replace')
shutil.copyfile('scripts/haddock_param_validate.py', 'build/_scripts/hp_validate')

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
    scripts=['build/_scripts/hp_extract_pdb', 'build/_scripts/hp_summary', 'build/_scripts/hp_replace',
             'build/_scripts/hp_validate'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
    ],
)
