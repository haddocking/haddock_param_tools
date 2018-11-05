.. HADDOCK2.4 param file scripts documentation master file, created by
   sphinx-quickstart on Mon Sep 17 00:27:13 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

HADDOCK2.4 parameter file tools documentation
=========================================================
This document aims to provide some usage and info about the
different ways provided by the CSB team to manipulate or
visualise HADDOCK2.4 new parameter files.
Those new parameter files are associated with all your HADDOCK
runs performed with the portal and are named by default `job_params.json`.

The tools are split in two categories:

- **scripts** 
Standalone scripts that can be used at the command-line level and
piped together to perform actions on a parameter file. They usually take a JSON
parameter file as input and output the same file with the change required.

- **API - param_to_json**
This API lets you manipulate HADDOCK2.4 parameter files at
the Python level. It allows you to perform changes on your parameters within your
own Python scripts. It encapsulates the parameter file ito a HADDOCKParam python
class that ensures for the validity and integrity of your parameters.

API Reference
=============

.. toctree::
   :maxdepth: 1

   main

Scripts
=======

- **haddock_param_summary.py**
.. automodule:: haddock_param_summary

- **haddock_param_extract_pdb.py**
.. automodule:: haddock_param_extract_pdb

- **haddock_param_replace.py**
.. automodule:: haddock_param_replace


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
