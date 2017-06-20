from traitlets import HasTraits, Float, Unicode
import matplotlib.pyplot as plt

class Parameter(HasTraits):
    min = Float()
    max = Float()
    value = Float()
    name = Unicode()
    
    def __init__(self, name, value, min_, max_):
        """Initialize the Parameter object"""
        self.name = name
        self.value = value
        self.min = min_
        self.max = max_
        
    def __str__(self):
        fmt = "Name = {}, Value = {}, Min = {}, Max = {}"
        return fmt.format(self.name, self.value, self.min, self.max)
        
    def __repr__(self):
        return "{} ".format(self.__class__) + self.__str__()
        

class Function(object):
    """pretty class for function to explore in jupyter notebook"""

    def __init__(self, func, independent_var=None, param_dict=None):
        # first run checks for jupyter notebook
        try:
            get_ipython().config
            self._IPYTHON = True
        except NameError:
            self._IPYTHON = False
            
        # assert callable function
        assert hasattr(func, '__call__'), 'Function is not callable'
        
        self._func = func
        self._args, self._ind_var = self._process_function(
            self._func, independent_var)

        self._params = self._prepare_params(param_dict)

        if self._IPYTHON:
            self._setup_widget()
            
    def display(self):
        """function to display a plotting widget in a jupyter notebook"""
        assert self._IPYTHON, """Need jupyter for interactive display"""
        self._setup_widget()
            
    def plot(self, var_):
        """plot this function as a function of var_"""
        fig, ax = plt.subplots()
        ax.plot(var_, self._eval(var_))

    def _prepare_params(self, param_dict):
        if param_dict is None:
            return [Parameter(arg, 1, -10, 10) for arg in self._args]
        else:
            return [Parameter(arg, param_dict.get('value', 1), param_dict.get('min', -10), param_dict.get('max', 10)) for arg in self._args]

    def _setup_widget(self):
        pass
    
    def _eval(self, var_):
        """evaluate function at a single point or list of points"""
        params = {p.name:p.value for p in self._params if p.name != self._ind_var}
        return self._func(var_, **params)

    def _process_function(self, function, independent_var):
        """function to get variables of function
        will assume independent variable is x or t unless explicit
        will be able to change in plotting widget
        """
        import inspect
        args = inspect.getargspec(function)[0]
        assert len(args) > 0, 'Function must have arguments'

        def get_ind_var():
            if 'x' in args:
                ind_var = 'x'
            elif 't' in args:
                ind_var = 'x'
            else:
                ind_var = args[0]
            return ind_var

        if independent_var is not None:
            if independent_var in args:
                ind_var = independent_var
            else:
                ind_var = get_ind_var()
        else:
            ind_var = get_ind_var()

        return args, ind_var