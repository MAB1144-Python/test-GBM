import unittest

def minimum_jumps(x):
    k = 0
    total_sum = 0
    mt = [[0]]
    for j in range(1, 10):
        caso = []
        k = k+1
        for i in range(len(mt[-1])):
            caso.append(mt[-1][i]+k)
            caso.append(mt[-1][i]-1)
        mt.append(caso)
        if x in caso:
            # print(f"El número mínimo de saltos necesarios para llegar al punto {x} es: {minimum_jumps(x)}")
            return k

class Test(unittest.TestCase):
    def test_palindromo1(self):
        self.assertEqual(minimum_jumps(1), 1)
    def test_palindromo2(self):
        self.assertEqual(minimum_jumps(2), 3)
    def test_palindromo3(self):
        self.assertEqual(minimum_jumps(3), 2)
    def test_palindromo4(self):
        self.assertEqual(minimum_jumps(4),3)
    def test_palindromo5(self):
        self.assertEqual(minimum_jumps(5), 4)

if __name__ == '__main__':
    unittest.main()