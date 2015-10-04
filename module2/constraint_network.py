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


class Variable(object):
    """
    Superclass
    """
    def __init__(self, name, domain):
        self.name = name
        self.domain = domain


class VertexColorVariable(Variable):
    """
    Problem-specific (graph coloring) class
    """
    def __init__(self, i, x, y):
        super(VertexColorVariable, self).__init__(name=i, domain=None)
        self.x = x
        self.y = y


class ConstraintNetwork(object):
    """
    Superclass

    constraints: dict {constraint_name: constraint_instance}
    domains: dict {domain_name: set(values)}
    """
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


class VertexColorConstraintNetwork(ConstraintNetwork):
    """
    Problem-specific class
    vertices: list of VertexColorVariable instances
    edges: list of tuples
    initial_domain: list of numbers that shall be put into each domain initially
    """
    def __init__(self, vertices, edges, initial_domain):
        self.edges = edges  # TODO: dunno if needed

        self.vertices = {}
        domains = {}
        for vertex in vertices:
            vertex.domain = set(initial_domain)
            domains[vertex.name] = vertex.domain
            self.vertices[vertex.name] = vertex

        constraints = {}
        for edge in edges:
            expression = str(edge[0]) + " != " + str(edge[1])
            name = str(edge[0]) + "<->" + str(edge[1])
            constraint = Constraint(name=name, variables=edge, expression=expression)
            constraints[name] = constraint

        super(VertexColorConstraintNetwork, self).__init__(constraints=constraints, domains=domains)

    def get_position(self, vertex_name):
        return self.vertices[vertex_name].x, self.vertices[vertex_name].y

    @staticmethod
    def get_color_id(vertex_domain):
        if len(vertex_domain) == 1:
            for color_id in vertex_domain:
                return color_id
        else:
            return -1
