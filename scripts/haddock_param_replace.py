#!/usr/bin/env python

"""
Replace a parameter in a HADDOCK parameter file (JSON), returns the full parameter file with the modified parameter.
Parameter must be int, float, string or boolean

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
import re

__author__ = "Mikael Trellet"
__email__ = "mikael.trellet@gmail.com"

USAGE = __doc__

key_types = {'amb_cool1': 'float', 'amb_cool2': 'float', 'amb_cool3': 'float', 'amb_firstit': 'int',
             'amb_hot': 'float', 'amb_lastit': 'int', 'anastruc_1': 'int', 'c2sym': 'list', 'c3sym': 'list',
             'c4sym': 'list', 'c5sym': 'list', 'centroid_kscale': 'float', 'centroid_rest': 'bool',
             'centroids': 'dict', 'clust_cutoff': 'float', 'clust_meth': 'str', 'clust_size': 'int',
             'cmrest': 'bool', 'cool1_steps': 'int', 'cool2_steps': 'int', 'cool3_steps': 'int',
             'create_narestraints': 'bool', 'crossdock': 'bool', 'dan': 'list', 'db_method': 'str',
             'delenph': 'bool', 'dielec': 'str', 'dihedrals_cool1': 'float', 'dihedrals_cool2': 'float',
             'dihedrals_cool3': 'float', 'dihedrals_hot': 'float', 'dihedrals_on': 'bool', 'dist_hb': 'float',
             'dist_nb': 'float', 'dnap_water_tokeep': 'float', 'dnarest_on': 'bool', 'elecflag_0': 'bool',
             'elecflag_1': 'bool', 'em_it0': 'bool', 'em_it1': 'bool', 'em_itw': 'bool', 'em_kscale': 'int',
             'em_resolution': 'float', 'em_rest': 'bool', 'emstepstrans': 'int', 'ensemble_multiply': 'bool',
             'epsilon': 'float', 'error_dih': 'int', 'fcc_ignc': 'bool', 'fileroot': 'str', 'fin_cool2': 'float',
             'fin_cool3': 'float', 'fin_rigid': 'float', 'firstwater': 'str', 'fully_flex': 'dict',
             'haddock_dir': 'str', 'hbond_cool1': 'float', 'hbond_cool2': 'float', 'hbond_cool3': 'float',
             'hbond_firstit': 'int', 'hbond_hot': 'float', 'hbond_lastit': 'int', 'hbonds_on': 'bool',
             'his_patch': 'dict', 'iniseed': 'int', 'init_cool2': 'float', 'init_cool3': 'float',
             'init_rigid': 'float', 'initiosteps': 'int', 'inter_mat': 'list', 'inter_rigid': 'float',
             'kcont': 'float', 'keepwater': 'bool', 'kncs': 'float', 'krg_cool1': 'float', 'krg_cool2': 'float',
             'krg_cool3': 'float', 'krg_hot': 'float', 'ksurf': 'float', 'ksym': 'float', 'kzres': 'float',
             'ncs': 'list', 'ncs_on': 'bool', 'ncvpart': 'float', 'noecv': 'bool', 'ntrials': 'int',
             'numc2sym': 'int', 'numc3sym': 'int', 'numc4sym': 'int', 'numc5sym': 'int', 'numncs': 'int',
             'nums3sym': 'int', 'numzres': 'int', 'par_nonbonded': 'str', 'partners': 'dict', 'pcs': 'list',
             'queues': 'list', 'ranair': 'bool', 'randorien': 'bool', 'rdc': 'list', 'rebuildcplx': 'bool',
             'rgrest': 'bool', 'rgsele': 'str', 'rgtarg': 'float', 'rigidmini': 'bool', 'rigidtrans': 'bool',
             'rotate180_0': 'bool', 'rotate180_1': 'bool', 'run_dir': 'str', 'runana': 'str', 'runname': 'str',
             's3sym': 'list', 'semi_flex': 'dict', 'skip_struc': 'int', 'solvate_method': 'str', 'solvent': 'str',
             'solvshell': 'bool', 'ssdihed': 'str', 'structures_0': 'int', 'structures_1': 'int',
             'surfrest': 'bool', 'sym_on': 'bool', 'tadfactor': 'int', 'tadfinal1_t': 'int', 'tadfinal2_t': 'int',
             'tadfinal3_t': 'int', 'tadhigh_t': 'int', 'tadinit1_t': 'int', 'tadinit2_t': 'int',
             'tadinit3_t': 'int', 'temptrash_dir': 'str', 'timestep': 'float', 'transwater': 'bool',
             'unamb_cool1': 'float', 'unamb_cool2': 'float', 'unamb_cool3': 'float', 'unamb_firstit': 'int',
             'unamb_hot': 'float', 'unamb_lastit': 'int', 'voxels_dim': 'list', 'voxels_num': 'list',
             'water_analysis': 'bool', 'water_randfrac': 'float', 'water_restraint_cutoff': 'float',
             'water_restraint_initial': 'float', 'water_restraint_scale': 'float', 'water_surfcutoff': 'float',
             'water_tokeep': 'float', 'watercoolsteps': 'int', 'waterdock': 'bool', 'waterensemble': 'int',
             'waterheatsteps': 'int', 'waterrefine': 'int', 'watersteps': 'int', 'weights': 'dict', 'zres': 'dict',
             'zres_on': 'bool', 'zresmax': 'float', 'zresmin': 'float'}


def cast_args(arg_param, arg_value):
    """
    Check whether the param exists and value has a proper type
    :param str arg_param: parameter to be replaced
    :param str arg_value: new parameter value to be assigned
    :return value: new value with parameter type
    :rtype value: int, float, str, bool
    """
    if arg_param not in key_types:
        sys.stderr.write(f"ERROR: Parameter {arg_param} not found.\n")
        sys.exit(1)
    if key_types[arg_param] in ('list', 'dict'):
        sys.stderr.write(f"ERROR: For parameters of types list and dict, please consider using param_to_json API.\n"
                         f"Aborting\n")
        sys.exit(1)
    if key_types[arg_param] == 'str':
        return arg_value
    elif key_types[arg_param] == 'int':
        if not re.match(r'-?(?<![\d.])[0-9]+(?![\d.])', arg_value):
            sys.stderr.write(f"ERROR: Wrong value {arg_value} for parameter {arg_param} ({key_types[arg_param]}).\n"
                             f"Check type.\n")
            sys.exit(1)
        else:
            return int(arg_value)
    elif key_types[arg_param] == 'float':
        if not re.match(r'-?[0-9]+\.[0-9]+', arg_value):
            sys.stderr.write(f"ERROR: Wrong value {arg_value} for parameter {arg_param} ({key_types[arg_param]}).\n"
                             f"Check type.\n")
            sys.exit(1)
        else:
            return float(arg_value)
    elif key_types[arg_param] == 'bool':
        if not re.match(r'[tT]rue|[Ff]alse|0|1', arg_value):
            sys.stderr.write(f"ERROR: Wrong value {arg_value} for parameter {arg_param} ({key_types[arg_param]}).\n"
                             f"Check type.\n")
            sys.exit(1)
        elif re.match(r'[Tt]rue|1', arg_value):
            return True
        elif re.match(r'[Ff]alse|0', arg_value):
            return False
        else:
            sys.stderr.write(f"ERROR: Processing of boolean value failed.\n")
            sys.exit(1)


def check_input(args):
    """
    Checks whether to read from stdin/file and validates user input/options.
    :param: args: command-line arguments
    :return: jsonfh: json parameter file as file-object
    """

    if not len(args):
        sys.stderr.write(USAGE)
        sys.exit(1)

    elif len(args) == 2:
        # Pipe?
        if not sys.stdin.isatty():
            jsonfh = sys.stdin
            value = cast_args(args[0], args[1])
            param = args[0]
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
        value = cast_args(args[0], args[1])
        param = args[0]
    else:
        sys.stderr.write(USAGE)
        sys.exit(1)
    return jsonfh, param, value


def replace(jsonfh, param, value):
    params = json.load(jsonfh)
    if param not in params:
        sys.stderr.write(f"ERROR: Parameter {param} not found.\n")
        sys.exit(0)
    elif isinstance(value, type(params[param])):
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
