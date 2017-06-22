import unittest 
from simtools.ParameterGroup import ParameterGroup, Parameter 

class test_Parameter(unittest.TestCase):

    def test_build(self):
        p = Parameter('test_param',2)
        self.assertEqual(p.name, 'test_param')
        self.assertEqual(p.value, 2)
    
    def test_linspace(self):
        import numpy as np
        p = Parameter('test_para',2,'linspace', (1,10,20))
        self.assertEqual(p.eval_expr().tolist(), np.linspace(1,10,20).tolist())

    def test_arange(self):
        import numpy as np
        p = Parameter('test_para',2,'arange', (1,100,2))
        self.assertEqual(p.eval_expr().tolist(), np.arange(1,100,2).tolist())

class testParameterGroup(unittest.TestCase):
    @classmethod
    def setup_class(self):
        self.plist = [
            Parameter('a',2,'linspace',(1,6,10)),
            Parameter('b',30),
            Parameter('c',2,'arange',(1,10,1))
        ]

        
    def test_build(self):
        params = ParameterGroup(self.plist)

if __name__ == '__main__':
    unittest.main()