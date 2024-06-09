import unittest
import unicodedata


def es_palindromo(palabra):
    palabra = ''.join((c for c in unicodedata.normalize('NFD', palabra) if unicodedata.category(c) != 'Mn'))
    palabra = ''.join((c for c in palabra.lower() if c.isalpha()))
    palabra = list(palabra)
    return palabra == palabra[::-1]

class Testpalindromo(unittest.TestCase):
    def test_palindromo1(self):
        self.assertEqual(es_palindromo("ana"), True)
    def test_palindromo2(self):
        self.assertEqual(es_palindromo("anita lava la tina"), True)
    def test_palindromo3(self):
        self.assertEqual(es_palindromo("Aman a Panamá"), True)
    def test_palindromo4(self):
        self.assertEqual(es_palindromo("A mamá Roma le aviva el amor a papá y a papá Roma le aviva el amor a mamá"), True)
    def test_palindromo5(self):
        self.assertEqual(es_palindromo("A la torre, derrótala"), True)

if __name__ == '__main__':
    unittest.main()