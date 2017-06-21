from .ParameterGroup import ParameterGroup


class Simulation(object):
    """Simulation object which acts a pipline for different Calculations
    """

    def __init__(self, calculations, parameter_groups, *args, **kwargs):
        self._calculations = self._generate_calculation_pipline(calculations)
        self._params = self._validate_parameter_groups(parameter_groups)

    def _generate_calculation_pipline(self, calculations):
        pass

    def _validate_parameter_groups(self, p_group):
        # check for iterable
        if isinstance(p_group, list) or isinstance(p_group, tuple):
            return [self._validate_parameter_groups(i) for i in p_group]
        else:
            if isinstance(p_group, ParameterGroup):
                return p_group
            else:
                raise Exception('Not a valid parameter Group')
