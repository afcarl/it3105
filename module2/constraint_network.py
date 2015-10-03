class Constraint:
    """
    name: string
    variables: list
    expression: string
    """
    def __init__(self, name, variables, expression):
        self.name = name
        self.ordered_variables = variables
        self.variables = set(variables)
        self.function = self.make_function(variables, expression)
        self.expression = expression

    def __repr__(self):
        return self.expression

    """
    values: dict(variable: value)
    """
    def is_satisfied(self, *values, **value_map):
        return self.function(*values, **value_map)

    def has_input_variable(self, variable):
        return variable in self.variables

    """
    TODO: this function may be obsolete
    """
    def get_variables_except_focal_variable(self, focal_variable):

        other_variables = []
        for variable in self.ordered_variables:
            if variable != focal_variable:
                other_variables.append(variable)
        return other_variables

    @staticmethod
    def make_function(variables, expression, environment=globals()):
        # http://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html
        # TODO: make this less dangerous by checking the expression before creating the function
        return eval("(lambda " + ', '.join(variables) + ": " + expression + ")", environment)


class ConstraintNetwork:
    def __init__(self, constraints, domains):
        self.constraints = constraints
        self.domains = domains

    def get_constraints_by_variable(self, variable, current_constraint=None):
        """
        current_constraint is excluded from the result
        :param variable:
        :param current_constraint:
        :return:
        """
        constraints = set()
        for constraint_name in self.constraints:
            constraint = self.constraints[constraint_name]
            if constraint != current_constraint and constraint.has_input_variable(variable):
                constraints.add(constraint)
        return constraints
