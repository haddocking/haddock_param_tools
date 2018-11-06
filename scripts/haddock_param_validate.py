#!/usr/bin/env python

"""
Validate a HADDOCK parameter file (JSON) and returns any WARNING/ERRORS found.

usage:
    | $> python haddock_param_validate.py [-v/--verbose] <json file>
example:
    | $> python haddock_param_validate.py job_params.json
    | WARNING: No partner detected
    | ERROR: Wrong type for parameter 'amb_cool2'
    |   ...

This script is supposed to work with the new parameter files
used in HADDOCK2.4 (JSON format).
"""

import os
import json
import sys
import logging

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


def check_input(args):
    """
    Checks whether to read from stdin/file and validates user input/options.
    :param: args: command-line arguments
    :return: jsonfh: json parameter file as file-object
    """

    if not sys.stdin.isatty():
        if not len(args):
            jsonfh = sys.stdin
            verbose = False
        elif len(args) == 1 and args[0] in ("-v", "--verbose"):
            jsonfh = sys.stdin
            verbose = True
        else:
            sys.stderr.write(USAGE)
            sys.exit(1)
    else:
        if not len(args):
            sys.stderr.write(USAGE)
            sys.exit(1)
        if len(args) == 1:
            if not os.path.isfile(args[0]):
                sys.stderr.write('File not found: ' + args[0] + '\n')
                sys.stderr.write(USAGE)
                sys.exit(1)
            jsonfh = open(args[0], 'r')
            verbose = False
        elif len(args) == 2 and args[1] in ("-v", "--verbose"):
            jsonfh = open(args[0], 'r')
            verbose = True
        else:
            sys.stderr.write(USAGE)
            sys.exit(1)

    return jsonfh, verbose


def validate(jsonfh, verbose):
    params = json.load(jsonfh)
    for k, v in key_types.items():
        if k not in params:
            logging.error(f"Key missing: {k}")
        elif type(params[k]).__name__ != v:
            logging.error(f"Wrong format for param {param}: {type(params[k]).__name__} instead of {v}")

    nb_partners = len(params['partners'])
    if verbose:
        if not nb_partners:
            logging.warning("No partner defined")
        elif nb_partners < 2:
            logging.warning("Only one partner defined")
        elif nb_partners > 20:
            logging.warning("More than 20 partners defined, HADDOCK currently supports up to 20 partners")


if __name__ == '__main__':
    # Check Input
    jsonfh, verbose = check_input(sys.argv[1:])

    try:
        # Do the job
        validate(jsonfh, verbose)
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
