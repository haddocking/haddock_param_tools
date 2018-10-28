import sys
import os
import unittest
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import param_to_json


class Tests(unittest.TestCase):
    def test_haddockparam(self):
        """Test HADDOCKParam class"""
        p = param_to_json.HADDOCKParam()
        self.assertTrue(p.verbose)
        self.assertEqual(p.path, "")
        self.assertEqual(p.params, {})
        self.assertFalse(p.valid)

    def test_load_wrong_path(self):
        p = param_to_json.HADDOCKParam()
        self.assertRaises(FileNotFoundError, p.load, "dummy_path/dummy_file.json")

    def test_load_wrong_format(self):
        p = param_to_json.HADDOCKParam()
        self.assertRaises(param_to_json.HADDOCKParamFormatError, p.load, "test/input/prot-prot-wrong.json")
        with tempfile.TemporaryFile() as fp:
            self.assertRaises(param_to_json.HADDOCKParamFormatError, p.load, fp)

    def test_validate(self):
        p = param_to_json.HADDOCKParam()
        p.load("test/input/prot-prot-em.json")
        with self.assertLogs(level='WARNING') as cm:
            p.params['partners'].pop("2")
            p.validate()
        self.assertEqual(cm.output, ['WARNING:root:Only one partner defined'])
        self.assertEqual(p.nb_partners, 1)
        with self.assertLogs(level='WARNING') as cm:
            p.params['partners'].pop("1")
            p.validate()
        self.assertEqual(cm.output, ['WARNING:root:No partner defined'])
        self.assertEqual(p.nb_partners, 0)

    def test_load(self):
        """Test parameter file loading"""
        p = param_to_json.HADDOCKParam()
        p.load("test/input/prot-prot-em.json")
        self.assertEqual(p.nb_partners, 2)
        self.assertTrue(p.valid)
