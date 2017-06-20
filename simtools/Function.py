from traitlets import HasTraits, Float, Unicode
import matplotlib.pyplot as plt
import ipywidgets
import IPython
import numpy as np
from ipykernel.pylab.backend_inline import flush_figures


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

    def to_widget_dict(self):
        """make a dict for float slider"""
        return {'value': self.value,
                'min': self.min,
                'max': self.max,
                'description': self.name,
                'step': abs(self.max - self.min) / 20}


def int_ceil(x):
    """return ceiling of value should be an integer"""
    _int = int(x)
    if _int < x:
        return int(x + 1)
    else:
        return _int


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

    def _setup_params_widget(self, params):
        """break into groups of 3"""
        num_rows = int_ceil(len(params) / 3)
        return ipywidgets.VBox([ipywidgets.HBox(params[3 * i:3 * (i + 1)]) for i in range(num_rows)])

    def _setup_widget(self):
        """create widget which will have parameters and range for x axis as well"""
        params = [ipywidgets.BoundedFloatText(
            **param.to_widget_dict()) for param in self._params if param.name != self._ind_var]
        param_widget = self._setup_params_widget(params)
        ind_var = [i for i in self._params if i.name == self._ind_var][0]
        x_min = ipywidgets.FloatText(description='x_min', value=ind_var.min)
        x_max = ipywidgets.FloatText(description='x_max', value=ind_var.max)

        submit_button = ipywidgets.Button(description='Plot')
        clear_button = ipywidgets.Button(description='Clear Plots')
        clear_check = ipywidgets.Checkbox(description='Fresh Plot')
        self._fig, self._ax = plt.subplots()
        _xx = np.linspace(x_min.value, x_max.value)
        self._ax.plot(_xx, self._func(
            _xx, **{param.description: param.value for param in params}))
        self._layout = ipywidgets.VBox(
            [param_widget,
             ipywidgets.HBox([x_min, x_max, clear_check]),
             ipywidgets.HBox([submit_button, clear_button])
             ])

        def _on_button_clicked(b):
            xx = np.linspace(x_min.value, x_max.value)
            # update parameters
            param_dict = {param.description: param.value for param in params}
            IPython.display.clear_output(wait=True)
            if clear_check.value:
                self._ax.cla()
            self._ax.plot(xx, self._func(xx, **param_dict))
            self._fig.canvas.draw()
            IPython.display.display(self._ax.figure)

        def _on_clear_button_clicked(b):
            IPython.display.clear_output(wait=True)
            self._ax.cla()
            self._fig.canvas.draw()
            IPython.display.display(self._ax.figure)

        submit_button.on_click(_on_button_clicked)
        clear_button.on_click(_on_clear_button_clicked)
        IPython.display.display(self._layout)

    def _eval(self, var_):
        """evaluate function at a single point or list of points"""
        params = {p.name: p.value for p in self._params if p.name != self._ind_var}
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
