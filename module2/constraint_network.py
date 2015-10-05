class Constraint(object):
    """
    name: string
    variables: list or tuple
    expression: string
    """
    def __init__(self, name, variables, expression):
        self.name = name
        self.ordered_variables = list(variables)
        self.variables = set(variables)
        self.function = self.make_function(self.ordered_variables, expression)
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

    @staticmethod
    def make_function(variables, expression, environment=globals()):
        # http://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html
        # TODO: make this less dangerous by checking the expression before creating the function
        return eval("(lambda " + ', '.join(variables) + ": " + expression + ")", environment)


class Variable(object):
    """
    Superclass
    """
    def __init__(self, name, domain):
        self.name = name
        self.domain = domain


class ConstraintNetwork(object):
    """
    Superclass

    constraints: dict {constraint_name: constraint_instance}
    domains: dict {domain_name: set(values)}
    """
    def __init__(self, constraints, domains):
        self.constraints = constraints
        self.domains = domains
        self.variable_constraints_cache = {}

    def get_constraints_by_variable(self, variable, current_constraint=None):
        """
        current_constraint is excluded from the result
        :param variable:
        :param current_constraint:
        :return:
        """
        hash_key = hash(
            variable +
            ('' if current_constraint is None else "__" + current_constraint.expression)
        )
        if hash_key in self.variable_constraints_cache:
            return self.variable_constraints_cache[hash_key]

        constraints = set()
        for constraint_name in self.constraints:
            constraint = self.constraints[constraint_name]
            if constraint != current_constraint and constraint.has_input_variable(variable):
                constraints.add(constraint)

        self.variable_constraints_cache[hash_key] = constraints
        return constraints


