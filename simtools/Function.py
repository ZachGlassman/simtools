class Function(object):
    """pretty class for function to explore in jupyter notebook"""

    def __init__(self, func, independent_var=None):
        try:
            get_ipython().config
        except:
            print('must run in Jupyter notebook for now')
        assert hasattr(func, '__call__')
        self._func = func
        print(type(func))
        self._args, self._ind_var = self._process_function(
            self._func, independent_var)

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
