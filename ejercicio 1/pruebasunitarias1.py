import unittest

def suma(a, b):
    return a + b

class TestSuma(unittest.TestCase):
    def test_suma(self):
        self.assertEqual(suma(3, 4), 7)

if __name__ == '__main__':
    unittest.main()