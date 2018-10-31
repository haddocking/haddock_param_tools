import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import param_to_json


class Tests(unittest.TestCase):
    def test_get_wrong_param(self):
        """Test HADDOCKParam get function"""
        p = param_to_json.HADDOCKParam()
        p.load("test/input/prot-prot-em.json")
        self.assertRaises(param_to_json.HADDOCKParamError, p.get, "dummy_param")

    def test_get_param(self):
        """Test HADDOCKParam get function with non-existing param"""
        p = param_to_json.HADDOCKParam()
        p.load("test/input/prot-prot-em.json")
        self.assertEqual(p.get("amb_cool1"), 10)
        self.assertEqual(p.get("centroid_kscale"), 50.0)
        self.assertEqual(p.get("clust_meth"), "FCC")

    def test_set_wrong_param(self):
        """Test HADDOCKParam set function with non-existing param"""
        p = param_to_json.HADDOCKParam()
        p.load("test/input/prot-prot-em.json")
        self.assertRaises(param_to_json.HADDOCKParamError, p.set, "dummy_param", "dummy_value")

    def test_set_wrong_param_format(self):
        """Test HADDOCKParam set function with wrong parameter format"""
        p = param_to_json.HADDOCKParam()
        p.load("test/input/prot-prot-em.json")
        self.assertRaises(param_to_json.HADDOCKParamFormatError, p.set, "amb_cool1", 10.1)

    def test_set_param(self):
        """Test HADDOCKParam set function"""
        p = param_to_json.HADDOCKParam()
        p.load("test/input/prot-prot-em.json")
        p.set("amb_cool1", 20)
        self.assertEqual(p.get("amb_cool1"), 20)
