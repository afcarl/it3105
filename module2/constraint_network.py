class Constraint:
    def __init__(self, name, variables, function):
        self.name = name
        self.variables = variables
        self.function = function

    def is_satisfied(self, values):
        return self.function(*values)  # TODO: test/fix this

    def has_input_variable(self, variable):
        return variable in self.variables

    def get_variables_except_focal_variable(self, focal_variable):
        other_variables = set(self.variables)
        other_variables.remove(focal_variable)
        return other_variables


class ConstraintNetwork:
    def __init__(self):
        self.constraints = {
            "c1": lambda x, y, z: x > y,
            "c2": lambda x, y, z: x + y > z
        }  #TODO: use the Constraint class instead
        self.domains = {
            "x": {0, 1, 2, 3},
            "y": {0, 1, 2, 3, 4, 5},
            "z": {4, 5, 6, 7}
        }  # This is test data. TODO: replace with something better

    def get_constraints_by_variable_except_current_constraint(self, variable, current_constraint):
        constraints = set()
        constraints.remove(current_constraint)
        for constraint in self.constraints:
            if constraint.has_input_variable(variable):
                constraints.add(constraint)
        return constraints
