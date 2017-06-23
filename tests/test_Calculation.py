import unittest 
import os
import time
import h5py
import pandas as pd
from simtools.Calculation import Calculation
from simtools.ParameterGroup import ParameterGroup, Parameter 
import numpy as np

def _f(a, b, c):
    ans = 0
    ans2 = []
    for i in range(1, b*10):
        ans += a+i/c
        ans2.append(a*i + c)
    return {'calc':ans, 'calc2':ans2}

def _f1(calc, calc2):
    return {'mean': np.mean(calc + calc2),'std':np.std(calc+calc2)}

filename = 'test.h5'

class test_Calculation(unittest.TestCase):

    @classmethod
    def setup_class(self):
        self.plist = ParameterGroup([
            Parameter('a', 2, 'linspace', (1, 6, 10)),
            Parameter('b', 30),
            Parameter('c', 2, 'arange', (1, 10, 1))
        ])

    @classmethod
    def teardown_class(self):
        os.remove(filename)


    def test_generate_file(self):
        #make sure no file is there
        if os.path.isfile(filename):
            os.remove(filename)
        calc = Calculation(_f, filename, 0)
        self.assertTrue(os.path.isfile(filename))
    
    def test_overwrite_file(self):
        with h5py.File(filename, 'w') as file_:
            pass
        time1 = os.path.getmtime(filename)
        # sleep so it won't be same
        time.sleep(.01)
        calc = Calculation(_f, filename, 0)
        self.assertNotEqual(time1, os.path.getmtime(filename))
    

    def test_no_overwrite_file(self):
        with h5py.File(filename, 'w') as file_:
            pass
        time1 = os.path.getmtime(filename)
        # sleep so it won't be same
        time.sleep(.01)
        calc = Calculation(_f, filename, 0, overwrite_file=False)
        self.assertEqual(time1, os.path.getmtime(filename))
       

    def test_set_args(self):
        calc = Calculation(_f, filename, 0)
        filepath, _id = calc._filepath, calc._id 
        calc.set_args('test', 2)
        self.assertNotEqual(filepath, calc._filepath)
        self.assertNotEqual(_id, calc,_id)

    def test_process_results(self):
        calc = Calculation(_f, filename, 0)
        calc.add_params(self.plist)
        df = calc.run()
        info_dict = {'_group_number_':0,'a':2,'b':30,'c':2}
        pars = {k:v for k,v in info_dict.items() if k != '_group_number_'}
        test_df = pd.DataFrame([info_dict])
        self.assertTrue(df.equals(test_df))
        #now look at output file
        with h5py.File(filename) as file_:
            groups = {k:v for k,v in file_.items()}
            group = groups['0']
            res = group['0']
            attrs_dict = {k:v for k,v in res.attrs.items()}
            size_group = {k:v for k,v in group.items()}
            _res = {k:np.array(v) for k,v in res.items()}
            
        self.assertEqual(len(groups), 1)
        self.assertEqual(len(size_group), 1)
        self.assertEqual(attrs_dict, pars)
        calculated = _f(**pars)

        self.assertEqual(_res['calc'], calculated['calc'])
        self.assertTrue(np.array_equal(_res['calc2'], calculated['calc2']))


if __name__ == '__main__':
    unittest.main()
