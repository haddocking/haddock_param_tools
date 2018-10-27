import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import param_to_json


class Tests(unittest.TestCase):
    def test_haddockparam(self):
        """Test HADDOCKParam class"""
        p = param_to_json.HADDOCKParam()
        self.assertTrue(p.verbose)
        self.assertEqual(p.nb_partners, 0)
        self.assertEqual(p.path, "")
        self.assertEqual(p.params, {})
        self.assertFalse(p.valid)

    def test_load_wrong_path(self):
        p = param_to_json.HADDOCKParam()
        self.assertRaises(FileNotFoundError, p.load, "dummy_path/dummy_file.json")

    def test_load_wrong_format(self):
        p = param_to_json.HADDOCKParam()
        self.assertRaises(param_to_json.HADDOCKParamFormatError, p.load, "test/input/prot-prot-wrong.json")

    def test_load_warning(self):
        p = param_to_json.HADDOCKParam()
        with self.assertLogs(level='WARNING') as cm:
            p.load("test/input/prot-prot-no-partner.json")
        self.assertEqual(cm.output, ['WARNING:root:No partner defined'])
        p.params['partners'][1] = []
        with self.assertLogs(level='WARNING') as cm:
            p._validate()
        self.assertEqual(cm.output, ['WARNING:root:Only one partner defined'])

    def test_load(self):
        """Test parameter file loading"""
        p = param_to_json.HADDOCKParam()
        p.load("test/input/prot-prot-em.json")
        self.assertEqual(p.nb_partners, 2)
        self.assertTrue(p.valid)
