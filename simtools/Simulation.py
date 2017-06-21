from .ParameterGroup import ParameterGroup
from .Calculation import Calculation
import pandas as pd


class Simulation(object):
    """Simulation object which acts a pipline for different Calculations
    """

    def __init__(self, filepath, calculations, parameter_groups):
        self._filepath = filepath
        self._calculations = self._generate_calculation_pipline(calculations)
        self._params = self._validate_parameter_groups(parameter_groups)

    def _generate_calculation_pipline(self, calculations):
        """check if are already calculations, if not then create calculation"""
        try:
            return [self._validate_calculation(calc, i)
                    for (i, calc) in enumerate(calculations)]
        except:
            return [self._validate_calculation(calculations, 0)]

    def _validate_calculation(self, calc, index):
        if isinstance(calc, Calculation):
            calc.set_args(self._filepath, index)
            return calc
        else:
            return Calculation(calc, self._filepath, index)

    def _validate_parameter_groups(self, p_group):
        # check for iterable
        if isinstance(p_group, list) or isinstance(p_group, tuple):
            return [self._validate_parameter_groups(i) for i in p_group]
        else:
            if isinstance(p_group, ParameterGroup):
                return p_group
            else:
                raise Exception('Not a valid parameter Group')

    def run(self, expansion_type=None, parallel=False, n_jobs=4):
        # TODO Handle the case where its pipelined in the sense that it uses
        # previous results
        df_list = []
        for i, calc in enumerate(self._calculations):
            try:
                calc.add_params(self._params[i])
            except:
                calc.add_params(self._params)
                df = calc.run(expansion_type, parallel, n_jobs)
                df['_pipeline_'] = i
            df_list.append(df)
        return pd.concat(df_list)
