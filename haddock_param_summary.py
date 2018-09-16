#!/usr/bin/env python3

"""
Get a quick summary of the job parameter file (JSON)

usage: 
    $> python haddock_param_summary.py <json file>
example: 
    $> python haddock_param_summary.py job_params.json
    it0 1000
    it1 20
    itw 20
    Partner1: Protein
    Partner2: Protein
    clust_meth: FCC
    clust_cutoff: 0.6

Author: {0} ({1})

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

def print_summary(jsonfh):
    try:
        params = json.load(jsonfh)
        # Number of models
        sys.stdout.write(f"it0\t{params['structures_0']}\nit1\t{params['structures_1']}\nitw\t{params['waterrefine']}\n")
        # Number of partners + type
        for i, p in params['partners'].items():
            sys.stdout.write('Partner{}: {}\n'.format(i, p['moleculetype']))
        # Clustering method
        sys.stdout.write(f"clust_meth: {params['clust_meth']}\n")
        sys.stdout.write(f"clust_cutoff: {params['clust_cutoff']}\n")
        sys.stdout.flush()
    except Exception as e:
        sys.stderr.write(f'Error: {e}\n')
        raise


if __name__ == '__main__':
    # Check Input
    jsonfh = check_input(sys.argv[1:])

    try:
        # Do the job
        print_summary(jsonfh)
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

