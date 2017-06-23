import unittest 
from simtools.Calculation import Calculation

def _f(a, b, c):
    ans = 0
    ans2 = []
    for i in range(1, b*10):
        ans += a+i/c
        ans2.append(a*i + c)
    return {'calc':ans, 'calc2':ans2}

def _f1(calc, calc2):
    return {'mean': np.mean(calc + calc2),'std':np.std(calc+calc2)}

class test_Calculation(unittest.TestCase):

    @classmethod
    def setup_class(self):
        self.plist = [
            Parameter('a', 2, 'linspace', (1, 6, 10)),
            Parameter('b', 30),
            Parameter('c', 2, 'arange', (1, 10, 1))
        ]
        
            


if __name__ == '__main__':
    unittest.main()
