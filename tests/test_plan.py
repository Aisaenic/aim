from src.main import main

"""
Examples
self.assertEqual(a, a)
self.assertTrue(a)
self.assertFalse(a)
with self.assertRaises(ValueError):
    pass
"""
"""
def test_invalid_ip(self):

def test_invalid_domain(self):

def test_valid_ip(self):

def test_valid_domain(self):
"""

#python3 main.py 'http://test.com' -in ../tests/test.csv -debug (should only have results from test.csv)
#python3 main.py -in ../tests/test.csv -debug