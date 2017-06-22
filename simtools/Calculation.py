import inspect
import h5py
import os
import numpy as np
import pandas as pd
from .ParameterGroup import ParameterGroup
try:
    from joblib import Parallel, delayed
    _PARALLEL = True
except:
    _PARALLEL = False


class Calculation(object):
    """function should return dictionary"""

    def __init__(self, func, filepath, id_, overwrite_file=True):
        """filepath is where hd5 files are saved"""
        self._func = func
        self._args = inspect.getargspec(func)[0]
        self.set_args(filepath, id_)
        self._prepare_hdf_file(overwrite_file)

    def _prepare_hdf_file(self, overwrite_file):
        """prepare hdf5file"""
        if overwrite_file:
            with h5py.File(self._filepath, 'w') as file_:
                pass
        else:
            # TODO implement check if file exists and raise warning
            pass

    def get_function_args(self):
        return self._args

    def set_args(self, filepath, id_):
        self._filepath = filepath
        self._id = id_

    def add_params(self, params):
        """add ParameterGroup to simulation and validate its inputs"""
        assert isinstance(
            params, ParameterGroup), "Parameters must be of type Parameter group"
        # check if arguments are in parameters (can be extra)
        if self._args != []:
            assert min([i in params.param_names()
                        for i in self._args]) == True, 'Need all of parameters'
        self._params = params

    def _generate_params(self, expansion_type):
        if expansion_type == 'zip':
            param_list = self._params.zip()
        elif expansion_type == 'outer':
            param_list = self._params.outer_product()
        else:
            param_list = self._params.single()

        return param_list

    def run(self, expansion_type=None, parallel=False, n_jobs=4):
        """run the calculation and put into result object"""
        param_list = self._generate_params(expansion_type)
        if parallel and _PARALLEL:
            answer = Parallel(n_jobs=n_jobs)(delayed(self._func)(**i)
                                             for i in param_list)
        else:
            answer = [self._func(**i) for i in param_list]
        return self._process_results(param_list, answer)

    def _process_results(self, params, ans):
        """process results, save to hdf5 file
        build dataframe with parameters and file_paths"""
        d_to_dataframe = []
        with h5py.File(self._filepath) as file_:
            calc_group = file_.create_group(str(self._id))
            for i, (p, r) in enumerate(zip(params, ans)):
                temp = {'_group_number_': i}
                group = calc_group.create_group('{}'.format(i))
                for k, v in p.items():
                    group.attrs[k] = v
                    temp[k] = v
                for k, v in r.items():
                    dataset = group.create_dataset(k, data=np.array(v))
                d_to_dataframe.append(temp)

        return pd.DataFrame(d_to_dataframe)