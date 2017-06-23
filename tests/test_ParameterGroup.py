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
        d = Parameter('d',30)
        params.add_parameter(d) 
        self.assertNotEqual(params._params, 
                            ParameterGroup(self.plist)._params)

    def test_param_names(self):
        params = ParameterGroup(self.plist)
        names = params.param_names()
        self.assertEqual(['a','b','c'], names)

    def test_zip(self):
        import numpy as np
        params = ParameterGroup(self.plist)
        a = np.linspace(1,6,10)
        c = np.arange(1,10,1)
        zipped = [dict(a=a[i],b=30,c=c[i]) for i in range(min(len(c), len(a)))]
        self.assertEqual(zipped, params.zip())

    def test_outer_product(self):
        import numpy as np
        from itertools import product

        params = ParameterGroup(self.plist)
        tuple_ = (np.linspace(1,6,10), [30], np.arange(1,10,1))
        names = ['a','b','c']
        exp = [{names[i]:tup[i] for i in range(3)} for tup in product(*tuple_)]
        self.assertEqual(exp, params.outer_product())

    def test_single(self):
        params = ParameterGroup(self.plist)
        single = [dict(a=2,b=30,c=2)]
        self.assertEqual(single, params.single())

        
if __name__ == '__main__':
    unittest.main()