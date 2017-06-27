from .ParameterGroup import ParameterGroup
from .Calculation import Calculation
import pandas as pd
import h5py
import numpy as np
import time


def parse_time_diff(x):
    """utility function for parsing a time difference to make it nicely readable

    Parameters
    ----------
    x : float 
        number which will be formatted
    """
    if x >= 60:
        return "{:.2f} min".format(x / 60)
    elif x < .5:
        return "{:.2f} ms".format(x * 1000)
    else:
        return "{:.2f} s".format(x)


class Simulation(object):
    """Simulation object which acts a pipline for different Calculations

    Parameters
    ----------
    filepath : str
        filepath for file storage 
    calculations : list[Calculation]
        list of calculations to perform 
    parameter_groups : list[ParameterGroup]
        list of parameter groups for the calculations (may be only the first one)
    """

    def __init__(self, filepath, calculations, parameter_groups):
        self._filepath = filepath
        self._params = self._validate_parameter_groups(parameter_groups)
        self._calculations = self._generate_calculation_pipline(calculations)

    def _generate_calculation_pipline(self, calculations):
        """check if are already calculations, if not then create calculation
        for calculation after initial caluclation, function arguments may be results from
        previous calculation.  However, all functions MUST have the same argument as first function
        so we will wrap the pipeline function in a utility function which will fetch previuosly calculated
        data and then call the funciton itself
        """
        try:
            ans = []
            for (i, calc) in enumerate(calculations):
                if i == 0:
                    calculation = self._validate_calculation(calc, i)
                    func_args = calculation.get_function_args()
                    ans.append(calculation)
                else:
                    assert func_args

                    def modified_calc(**kwargs):
                        """modified function which can access previous data
                        very slow for now, but will be made faster at some point
                        by indexing the parameters on the index
                        """
                        result_args = {}
                        with h5py.File(self._filepath) as file_:
                            group = file_['/{}'.format(i - 1)]
                            for key in group:
                                param_inputs = {k: v for k,
                                                v in group[key].attrs.items()}
                                if param_inputs == kwargs:
                                    for name, dataset in group[key].items():
                                        d_set = np.array(dataset)
                                        if d_set.shape == ():
                                            result_args[name] = int(d_set)
                                        else:
                                            result_args[name] = d_set
                                    break
                        return calc(**result_args)

                    calculation = self._validate_calculation(modified_calc, i)
                    ans.append(calculation)
            return ans
        except:
            return [self._validate_calculation(calculations, 0)]

    def _validate_calculation(self, calc, index):
        """Check that calculation is proper 

        Parameters
        ----------
        calc : Calculation
            calculation
        index : int 
            index of calculation in list
        """
        if isinstance(calc, Calculation):
            calc.set_args(self._filepath, index)
            return calc
        else:
            return Calculation(calc, self._filepath, index)

    def _validate_parameter_groups(self, p_group):
        # check for iterable
        if isinstance(p_group, list) or isinstance(p_group, tuple):
            return [self._validate_parameter_groups(i) for i in p_group]
        elif isinstance(p_group, ParameterGroup):
            return p_group
        else:
            raise Exception('Not a valid parameter Group')

    def run(self, expansion_type=None, parallel=False, n_jobs=4):
        # TODO Handle the case where its pipelined in the sense that it uses
        # previous results
        _start_calc = time.time()
        df_list = []
        for i, calc in enumerate(self._calculations):
            try:
                calc.add_params(self._params[i])
            except:
                calc.add_params(self._params)
            # make parallel false for now because need serial access to h5 file
            # TODO implement file lock
            parallel = False
            df = calc.run(expansion_type, parallel, n_jobs)
            df['_pipeline_'] = i
            df_list.append(df)
        self._result = pd.concat(df_list)
        self._result_time = time.time() - _start_calc

    def describe_result(self):
        try:
            len_result = len(self._result)
        except AttributeError:
            print('No result computed')
        out_str = 'Output located in {}\n'.format(self._filepath)
        out_str += 'Total number of calculations is {}\n'.format(
            len_result)
        out_str += 'Calculation time is {}\n'.format(
            parse_time_diff(self._result_time))
        out_str += 'Calculation proceeded with {} steps of {} expanded parameter sets each\n'.format(
            len(self._result['_pipeline_'].unique()), len(self._result['_group_number_'].unique()))
        print(out_str)

    def explore_results(self):
        """generate widget to explore results in notebook"""
        try:
            get_ipython().config
            self._IPYTHON = True
        except NameError:
            self._IPYTHON = False

    def _retrive_results(self, pipeline_level, calc_number):
        key = str(calc_number)
        result = {}
        with h5py.File(self._filepath) as file_:
            group = file_['/{}'.format(pipeline_level)]
            params = {k: v for k, v in group[key].attrs.items()}
            for name, dataset in group[key].items():
                d_set = np.array(dataset)
                if d_set.shape == ():
                    result[name] = int(d_set)
                else:
                    result[name] = d_set
        return params, result

    def _retrieve_result_dataframe(self, pipeline_level):
        """generate dataframe for pipeline_level"""
        ans = []
        with h5py.File(self._filepath) as file_:
            group = file_['/{}'.format(pipeline_level)]
            for key in group:
                result = {}
                params = {k: v for k, v in group[key].attrs.items()}
                for name, dataset in group[key].items():
                    d_set = np.array(dataset)
                    if d_set.shape == ():
                        result[name] = int(d_set)
                    else:
                        raise Exception(
                            'Function requires single valued results')
                ans.append({**params, **result})
        return pd.DataFrame(ans).set_index(list(params.keys()))
