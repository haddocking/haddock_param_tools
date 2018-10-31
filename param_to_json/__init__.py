"""
Representation of a HADDOCK parameter file as a Python object.

This library allows to create, load, modify and write HADDOCK
parameter files in JSON format.

Several functions are made available and are based on a common
structure HADDOCKParam that needs to be initialized prior to
doing anything.
"""

import json
import logging
from json import JSONDecodeError

__author__ = 'Mikael Trellet'
__version__ = '0.1'

logging.basicConfig()


class HADDOCKParamError(Exception):
    """Exception class related to any error within the HADDOCKParam class"""

    def __init__(self, message):
        # Call base class constructor
        Exception.__init__(self, message)


class HADDOCKParamFormatError(Exception):
    """Exception class related to any format error within the HADDOCKParam
    class"""

    def __init__(self, message, param=None):
        full_message = f'{message}\n'
        if param:
            full_message += f'Parameter: "{param}"'

        # Call base class constructor
        Exception.__init__(self, full_message)


class HADDOCKParam(object):
    """
    Top-level class representing a complete HADDOCK parameter file.

    :param bool verbose: Get validation details and warnings
    """

    key_types = {'amb_cool1': 'int', 'amb_cool2': 'int', 'amb_cool3': 'int', 'amb_firstit': 'int', 'amb_hot': 'int',
                 'amb_lastit': 'int', 'anastruc_1': 'int', 'c2sym': 'list', 'c3sym': 'list', 'c4sym': 'list',
                 'c5sym': 'list', 'centroid_kscale': 'float', 'centroid_rest': 'bool', 'centroids': 'dict',
                 'clust_cutoff': 'float', 'clust_meth': 'str', 'clust_size': 'int', 'cmrest': 'bool',
                 'cool1_steps': 'int', 'cool2_steps': 'int', 'cool3_steps': 'int', 'create_narestraints': 'bool',
                 'crossdock': 'bool', 'dan': 'list', 'db_method': 'str', 'delenph': 'bool', 'dielec': 'str',
                 'dihedrals_cool1': 'int', 'dihedrals_cool2': 'int', 'dihedrals_cool3': 'int', 'dihedrals_hot': 'int',
                 'dihedrals_on': 'bool', 'dist_hb': 'float', 'dist_nb': 'float', 'dnap_water_tokeep': 'float',
                 'dnarest_on': 'bool', 'elecflag_0': 'bool', 'elecflag_1': 'bool', 'em_it0': 'bool', 'em_it1': 'bool',
                 'em_itw': 'bool', 'em_kscale': 'int', 'em_resolution': 'float', 'em_rest': 'bool',
                 'emstepstrans': 'int', 'ensemble_multiply': 'bool', 'epsilon': 'float', 'error_dih': 'int',
                 'fcc_ignc': 'bool', 'fileroot': 'str', 'fin_cool2': 'float', 'fin_cool3': 'float',
                 'fin_rigid': 'float', 'firstwater': 'str', 'fully_flex': 'dict', 'haddock_dir': 'str',
                 'hbond_cool1': 'int', 'hbond_cool2': 'int', 'hbond_cool3': 'int', 'hbond_firstit': 'int',
                 'hbond_hot': 'int', 'hbond_lastit': 'int', 'hbonds_on': 'bool', 'his_patch': 'dict', 'iniseed': 'int',
                 'init_cool2': 'float', 'init_cool3': 'float', 'init_rigid': 'float', 'initiosteps': 'int',
                 'inter_mat': 'list', 'inter_rigid': 'float', 'kcont': 'float', 'keepwater': 'bool', 'kncs': 'float',
                 'krg_cool1': 'int', 'krg_cool2': 'int', 'krg_cool3': 'int', 'krg_hot': 'int', 'ksurf': 'float',
                 'ksym': 'float', 'kzres': 'float', 'n': 'int', 'nb_mol_max': 'int', 'ncs': 'list', 'ncs_on': 'bool',
                 'ncvpart': 'float', 'noecv': 'bool', 'ntrials': 'int', 'numc2sym': 'int', 'numc3sym': 'int',
                 'numc4sym': 'int', 'numc5sym': 'int', 'numncs': 'int', 'nums3sym': 'int', 'numzres': 'int',
                 'par_nonbonded': 'str', 'partners': 'dict', 'pcs': 'list', 'queues': 'list', 'ranair': 'bool',
                 'randorien': 'bool', 'rdc': 'list', 'rebuildcplx': 'bool', 'rgrest': 'bool', 'rgsele': 'str',
                 'rgtarg': 'float', 'rigidmini': 'bool', 'rigidtrans': 'bool', 'rotate180_0': 'bool',
                 'rotate180_1': 'bool', 'run_dir': 'str', 'runana': 'str', 'runname': 'str', 's3sym': 'list',
                 'semi_flex': 'dict', 'skip_struc': 'int', 'solvate_method': 'str', 'solvent': 'str',
                 'solvshell': 'bool', 'ssdihed': 'str', 'structures_0': 'int', 'structures_1': 'int',
                 'surfrest': 'bool', 'sym_on': 'bool', 'tadfactor': 'int', 'tadfinal1_t': 'int', 'tadfinal2_t': 'int',
                 'tadfinal3_t': 'int', 'tadhigh_t': 'int', 'tadinit1_t': 'int', 'tadinit2_t': 'int',
                 'tadinit3_t': 'int', 'temptrash_dir': 'str', 'timestep': 'float', 'transwater': 'bool',
                 'unamb_cool1': 'int', 'unamb_cool2': 'int', 'unamb_cool3': 'int', 'unamb_firstit': 'int',
                 'unamb_hot': 'int', 'unamb_lastit': 'int', 'voxels_dim': 'list', 'voxels_num': 'list',
                 'water_analysis': 'bool', 'water_randfrac': 'float', 'water_restraint_cutoff': 'float',
                 'water_restraint_initial': 'float', 'water_restraint_scale': 'float', 'water_surfcutoff': 'float',
                 'water_tokeep': 'float', 'watercoolsteps': 'int', 'waterdock': 'bool', 'waterensemble': 'int',
                 'waterheatsteps': 'int', 'waterrefine': 'int', 'watersteps': 'int', 'weights': 'dict', 'zres': 'dict',
                 'zres_on': 'bool', 'zresmax': 'float', 'zresmin': 'float'}

    def __init__(self, verbose=True):
        self.verbose = verbose
        self.path = ""
        self.params = {}
        self.valid = False
        self.nb_partners = 0

    @property
    def nb_partners(self):
        return self.__nb_partners

    @nb_partners.setter
    def nb_partners(self, val):
        if val < 0:
            self.__nb_partners = 0
            logging.warning("Number of partners cannot be less than 0")
        elif val > 20:
            self.__nb_partners = 20
            logging.warning("Currently HADDOCK supports up to 20 molecules")
        else:
            self.__nb_partners = val

    @nb_partners.getter
    def nb_partners(self):
        if not self.params:
            raise HADDOCKParamError("No parameters found, please load a file")
        elif "partners" not in self.params:
            raise HADDOCKParamFormatError("No partners found in parameter set, wrong format")
        else:
            return len(self.params["partners"])

    def _load(self, jsonfh, skip_validation):
        try:
            self.params = json.load(jsonfh)
            if not skip_validation:
                self.valid = self.validate()
        except JSONDecodeError as e:
            raise HADDOCKParamFormatError(f"Error while loading JSON file: {e}")
        except HADDOCKParamFormatError:
            raise

    def validate(self):
        """
        Validation of parameter file format and keys

        :return: True/False
        :rtype: bool
        :raise: HADDOCKParamFormatError
        """
        # Check that all required keys are present and have proper value type
        # TODO Clean non required keys, by default all are required
        for k, v in self.key_types.items():
            if k not in self.params:
                raise HADDOCKParamFormatError("Key missing.", param=k)
            elif type(self.params[k]).__name__ != v:
                raise HADDOCKParamFormatError(f"Wrong format: {type(self.params[k]).__name__} instead of {v}", param=k)

        self.nb_partners = len(self.params['partners'])
        if self.verbose:
            if not self.nb_partners:
                logging.warning("No partner defined")
                return False
            elif self.nb_partners < 2:
                logging.warning("Only one partner defined")
                return False
        return True

    def load(self, input, skip_validation=False):
        """Load the parameter file in a HADDOCKParam object

        :param input: JSON file path or file-object
        :param skip_validation: Flag to skip or not the validation step
        :type input: str, file
        :type skip_validation: bool
        """
        if isinstance(input, str):
            with open(input, 'r') as jsonfh:
                self._load(jsonfh, skip_validation)
        else:
            self._load(input, skip_validation)

