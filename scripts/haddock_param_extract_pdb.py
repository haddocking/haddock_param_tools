#!/usr/bin/env python

"""
Extract the PDB input files from a job parameter file (JSON)
in the current directory

usage:
    | $> python haddock_param_summary.py <json file>
example:
    | $> python haddock_param_summary.py job_params.json
    | partner1.pdb created
    | partner2.pdb created

This script is supposed to work with the new parameter files
used in HADDOCK2.4 (JSON format).
"""

import os
import json
import sys

__author__ = "Mikael Trellet"
__email__ = "mikael.trellet@gmail.com"

USAGE = __doc__.format(__author__, __email__)


def check_input(args):
    """
    Checks whether to read from stdin/file and validates user input/options.
    :param: args: command-line arguments
    :return: jsonfh: json paramter file as file-object
    """

    if not len(args):
        # No chain, from pipe
        if not sys.stdin.isatty():
            jsonfh = sys.stdin
        else:
            sys.stderr.write(USAGE)
            sys.exit(1)
    elif len(args) == 1:
        if not os.path.isfile(args[0]):
            if args[0] not in ("-h", "--help"):
                sys.stderr.write('File not found: ' + args[0] + '\n')
            sys.stderr.write(USAGE)
            sys.exit(1)
        jsonfh = open(args[0], 'rU')
    else:
        sys.stderr.write(USAGE)
        sys.exit(1)

    return jsonfh


def extract_pdbs(jsonfh):
    """
    Write PDB files found in HADDOCK parameter file
    :param: jsonfh: json paramter file as file-object
    """
    try:
        params = json.load(jsonfh)
        for p, pdb in params['partners'].items():
            with open(f'partner{p}.pdb', 'w') as o:
                o.write(pdb['raw_pdb'])
            sys.stdout.write(f'partner{p}.pdb created\n')
        sys.stdout.flush()
    except Exception as e:
        sys.stderr.write(f'Error: {e}\n')
        raise


if __name__ == '__main__':
    # Check Input
    jsonfh = check_input(sys.argv[1:])

    try:
        # Do the job
        extract_pdbs(jsonfh)
    except IOError:
        # This is here to catch Broken Pipes
        # for example to use 'head' or 'tail' without
        # the error message showing up
        pass
    except Exception as e:
        sys.exit(0)

    # last line of the script
    # We can close it even if it is sys.stdin
    jsonfh.close()
    sys.exit(0)
