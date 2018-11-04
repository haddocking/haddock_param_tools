#!/usr/bin/env python

"""
Replace a parameter in a HADDOCK parameter file (JSON), returns the full parameter file with the modified parameter

usage:
    | $> python haddock_param_replace.py <param_name> <param_new_value> <json file>
example:
    | $> python haddock_param_replace.py amb_cool1 20 job_params.json
    | {
    |   'amb_cool1': 20,
    |   'amb_cool2': 50,
    |   ...
    | }

This script is supposed to work with the new parameter files
used in HADDOCK2.4 (JSON format).
"""

import os
import json
import sys

__author__ = "Mikael Trellet"
__email__ = "mikael.trellet@gmail.com"

USAGE = __doc__


def check_input(args):
    """
    Checks whether to read from stdin/file and validates user input/options.
    :param: args: command-line arguments
    :return: jsonfh: json paramter file as file-object
    """

    if not len(args):
        sys.stderr.write(USAGE)
        sys.exit(1)

    elif len(args) == 2:
        # Pipe?
        if not sys.stdin.isatty():
            jsonfh = sys.stdin
            param = args[0]
            value = args[1]
        else:
            sys.stderr.write(USAGE)
            sys.exit(1)
    elif len(args) == 3:
        if not os.path.isfile(args[2]):
            if args[0] not in ("-h", "--help"):
                sys.stderr.write('File not found: ' + args[2] + '\n')
            sys.stderr.write(USAGE)
            sys.exit(1)
        jsonfh = open(args[2], 'r')
        param = args[0]
        value = args[1]
    else:
        sys.stderr.write(USAGE)
        sys.exit(1)
    return jsonfh, param, value


def replace(jsonfh, param, value):
    params = json.load(jsonfh)
    if param not in params:
        sys.stderr.write(f"ERROR: Parameter {param} not found.\n")
        sys.exit(0)
    elif type(value) != type(params[param]):
        sys.stderr.write(f"WARNING: Type different between old and new values.\n")
    params[param] = value
    return params


def output(params):
    if params:
        sys.stdout.write(json.dumps(params, indent=2, sort_keys=True))
        sys.stdout.write("\n")
        sys.stdout.flush()
    else:
        sys.stderr.write("No parameters generated, aborting...\n")
        sys.exit(0)


if __name__ == '__main__':
    # Check Input
    jsonfh, param, value = check_input(sys.argv[1:])

    try:
        # Do the job
        params = replace(jsonfh, param, value)
        output(params)
    except IOError:
        # This is here to catch Broken Pipes
        # for example to use 'head' or 'tail' without
        # the error message showing up
        pass
    except Exception as e:
        sys.exit(0)
    finally:
        jsonfh.close()

    # last line of the script
    # We can close it even if it is sys.stdin
    jsonfh.close()
    sys.exit(0)
