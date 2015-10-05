from constraint_network import Variable, ConstraintNetwork, Constraint


class VertexColorVariable(Variable):
    """
    Problem-specific (graph coloring) class
    """
    def __init__(self, i, x, y):
        super(VertexColorVariable, self).__init__(name=i, domain=None)
        self.x = x
        self.y = y


class VertexColorConstraintNetwork(ConstraintNetwork):
    """
    Problem-specific class
    vertices: list of VertexColorVariable instances
    edges: list of tuples
    initial_domain: list of numbers that shall be put into each domain initially
    """
    def __init__(self, vertices, edges, initial_domain):
        self.edges = edges

        self.normalize_vertex_positions(vertices)
        self.vertices = {}
        domains = {}
        for vertex in vertices:
            vertex.domain = set(initial_domain)
            domains[vertex.name] = vertex.domain
            vertex.neighbours = set()
            self.vertices[vertex.name] = vertex

        constraints = {}
        for edge in edges:
            expression = str(edge[0]) + " != " + str(edge[1])
            self.vertices[edge[0]].neighbours.add(edge[1])
            self.vertices[edge[1]].neighbours.add(edge[0])
            name = str(edge[0]) + "<->" + str(edge[1])
            constraint = Constraint(name=name, variables=edge, expression=expression)
            constraints[name] = constraint

        super(VertexColorConstraintNetwork, self).__init__(constraints=constraints, domains=domains)

    @staticmethod
    def normalize_vertex_positions(vertices):
        """
        Normalize positions, so that they are all within the range [0, 1]
        This may affect the aspect ratio.
        :param vertices:
        :return:
        """
        min_x, min_y = vertices[0].x, vertices[0].y
        max_x, max_y = vertices[0].x, vertices[0].y
        for vertex in vertices:
            if vertex.x < min_x:
                min_x = vertex.x
            elif vertex.x > max_x:
                max_x = vertex.x
            if vertex.y < min_y:
                min_y = vertex.y
            elif vertex.y > max_y:
                max_y = vertex.y

        max_width = max_x - min_x
        max_height = max_y - min_y
        for vertex in vertices:
            vertex.x -= min_x
            vertex.y -= min_y
            vertex.x /= max_width
            vertex.y /= max_height

    def get_neighbour_names(self, vertex_name):
        return self.vertices[vertex_name].neighbours

    def get_position(self, vertex_name):
        return self.vertices[vertex_name].x, self.vertices[vertex_name].y

    @staticmethod
    def get_color_id(vertex_domain):
        if len(vertex_domain) == 1:
            for color_id in vertex_domain:
                return color_id
        else:
            return -1
