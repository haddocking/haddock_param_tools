[![Build Status](https://travis-ci.com/mtrellet/haddock_param_tools.svg?branch=master)](https://travis-ci.com/mtrellet/haddock_param_tools)
[![codecov](https://codecov.io/gh/mtrellet/haddock_param_tools/branch/master/graph/badge.svg)](https://codecov.io/gh/mtrellet/haddock_param_tools)
[![Documentation Status](https://readthedocs.org/projects/haddock-param-tools/badge/?version=latest)](https://haddock-param-tools.readthedocs.io/en/latest/?badge=latest)

# haddock_param_tools
Python scripts and API to manipulate HADDOCK2.4 parameter files (*.json).

This repository is split between scripts that can be used at the command-line level
and a API allowing to use those functions in any python script.

Tested with:

    - Python3.6 
    - Python3.7

# Scripts

The scripts contained in the [scripts](scripts/) directory can be used as commands in any terminal.
They accept both file path or stream from the standard output as input. This allows for piping them
one after each other in order to perform different operations at once.

## Summary

```bash
$> python haddock_param_summary.py job_params.json
it0	1000
it1	20
itw	20
Partner1: Protein
Partner2: Protein
clust_meth: FCC
clust_cutoff: 0.6
```

## Get input PDB files

```bash
$> python haddock_param_extract_pdb.py job_params.json
partner1.pdb created
partner2.pdb created
```

# API

This [API](param_to_json) allows access to most operations on a parameter file at the python level. 
It is based on a HADDOCKParam object that encapsulates the JSON dictionary and exposes different 
information and operations to edit/change the parameters. Any change can be dumped to a new parameter 
file using the `dumper` function.

## Documentation

See more information here: https://haddock-param-tools.readthedocs.io/

## Installation

- Build

```bash
$> python setup.py build
```
- Optional - Test
```bash
$> python setup.py test
```

- Install
```bash
$> python setup.py install
```

## Usage

### Load a parameter file

```python
from param_to_json import HADDOCKParam

params = HADDOCKParam()
params.load('test/input/prot-prot-em.json')
print(params.nb_partners)
```

# License

Apache (see [LICENSE](LICENSE))