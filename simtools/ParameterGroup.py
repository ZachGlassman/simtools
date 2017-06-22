"""This module exposes an object ParameterGroup which contains a set of Parameter objects
Each parameter group carries information about expansion which is carried out during the simulation.
"""
from itertools import product
import numpy as np


class ExpansionFunction(object):
    """Expansion object which allows naming of an expansion"""

    def __init__(self, name, function):
        self.name = name
        self._func = function

    def __call__(self, *args):
        return self._func(*args)


_EXPANSIONS = {
    'linspace': ExpansionFunction('linspace', np.linspace),
    'arange': ExpansionFunction('arange', np.arange),
    'list': ExpansionFunction('list', list)
}


class Parameter(object):
    """represents a single parameter in a model carries information about possible expansion
    responsible for evaluating expansion during the simulation.

    Parameters
        ----------
        name : str
            name of parameter
    """

    def __init__(self, name, value, expansion=None, args=None):
        self.name = name
        self.value = value
        if expansion is not None:
            try:
                self.expansion = _EXPANSIONS[expansion]
            except KeyError:
                print('Need to use valid expansion\n' +
                      ''.join(i + '\n' for i in _EXPANSIONS.keys()))
            self.args = args
        else:
            def _func(*args):
                return [self.value]
            self.expansion = _func
            self.args = ()

    def eval_expr(self):
        """Evaluate the expansion
        
        Returns
        -------
        expansion : any
            expansion of variables
        """
        return self.expansion(*self.args)


class ParameterGroup(object):
    """represents a set of parameters and possible expansions of those parameters
    
    Parameters
    ---------
    params : list 
         list of Parameter objects
    """

    def __init__(self, params=None):
        self._params = []
        if params is not None:
            for i in params:
                self.add_parameter(i)

    def param_names(self):
        """Get the names of all the parameters
        

        Returns
        -------
        names : list 
            list of parameter names
        """
        return [i.name for i in self._params]

    def add_parameter(self, param):
        assert isinstance(
            param, Parameter), "cannot make ParameterGroup of type not Parameter"
        self._params.append(param)

    def outer_product(self):
        """return a list of dictionaries of arguments with outer product expansion
        every value will be expanded by every other value
        len(list) = PI(len(expansion)) where PI is multiplicative"""
        expanded_params = [i.eval_expr() for i in self._params]
        names = [i.name for i in self._params]
        n_pars = len(self._params)
        return [{names[i]:tup[i] for i in range(n_pars)} for tup in product(*tuple(expanded_params))]

    def zip(self):
        """return list of dictionaries of arguments zipped
        we will truncate the zip to the minimum length of parameter expansions greater than 1
        singular parameter expansions will be treated as constant
        """
        expanded_params = {i.name: i.eval_expr() for i in self._params}
        min_len = min([j for j in [len(i)
                                   for i in expanded_params.values()] if j > 1])
        for k, v in expanded_params.items():
            if len(v) < 2:
                expanded_params[k] = np.array([v[0] for _ in range(min_len)])
            else:
                expanded_params[k] = np.array(v[:min_len])
        return [{k: v[i] for k, v in expanded_params.items()} for i in range(min_len)]

    def single(self):
        """return list with single element with only the value of each parameter"""
        return [{i.name: i.value for i in self._params}]
