class BaseSimulation(object):
    """simulation object which is meant to be subclassed by different simulations

    enforces structure of code"""

    def __init__(self, *args, **kwargs):
        self.init(*args, **kwargs)

    def run(self, plot=True, *args, **kwargs):
        """function to run simulation

        1. checks parameters are proper 
        2. runs simulation 
        3. plots results if plot true 

        params:
          plot:boolean"""
        res = self.run_simulation(*args, **kwargs)
        if plot:
            self.plot()

    def set_params(self):
        pass

    def plot(self):
        pass

    def init(self):
        pass

    def run_simulation(*args, **kwargs):
        pass


TIME_UNITS = {'ns': 1e-9, 'us': 1e-6, 'ms': 1e-3, 's': 1}


class TimeSimulation(BaseSimulation):
    """simulation which depends only on time"""

    def init(self, func, inital_time, end_time, units):
        assert units in TIME_UNITS, 'Unit must one of {}'.format(
            ",".join(i for i in TIME_UNITS.keys()))
        self._units = units
        self._t_scale = TIME_UNITS[units]
        self._t0 = inital_time
        self._tf = end_time
        self._func = func

    def run_simulation(self):
        """propgate equation through time"""
        pass
