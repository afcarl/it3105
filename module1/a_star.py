from priority_set import NodePrioritySet


class AStar(object):
    def __init__(self, draw=None, disable_gfx=False, draw_every=1, print_path=False):
        if draw is None:
            disable_gfx = True
        self.draw = draw
        self.disable_gfx = disable_gfx
        self.draw_every = draw_every
        self.print_path = print_path

    def run(self, start_node):
        """
        Run the A* algorithm
        start_node: must be an instance of a subclass of BaseNode
        """
        open_list = NodePrioritySet()
        closed_list = {}
        start_node.calculate_h()
        start_node.calculate_f()
        open_list.add(start_node, start_node.f)

        def attach_and_eval(parent_node, child_node):
            child_node.set_g(parent_node.g + parent_node.get_arc_cost(child_node))
            child_node.calculate_h()
            child_node.calculate_f()
            child_node.set_parent(parent_node)

        # If the algorithm still hasn't found a solution after the max number of iterations,
        # then the algorithm will stop
        max_num_iterations = 50000000
        for num_iterations in range(max_num_iterations):
            if open_list.is_empty():
                print 'Failed to find a solution'
                return False
            current_node = open_list.pop()
            closed_list[current_node] = current_node
            if not self.disable_gfx and num_iterations % self.draw_every == 0:
                ancestors = current_node.get_ancestors()
                self.draw(current_node, ancestors, closed_list, open_list)  # draw current state
            if current_node.is_solution():
                print "number of nodes created:", len(closed_list) + len(open_list.dict)
                ancestors = current_node.get_ancestors()
                print "path length:", len(ancestors)
                if self.print_path:
                    print "backtracked nodes that led to the solution:"
                    print current_node
                    for ancestor in ancestors:
                        print ancestor
                return current_node
            children = current_node.generate_children()
            for child in children:
                previously_generated = False
                if child in open_list:
                    child = open_list[child]  # re-use previously generated node
                    previously_generated = True
                elif child in closed_list:
                    child = closed_list[child]  # re-use previously generated node
                    previously_generated = True

                if not previously_generated:
                    attach_and_eval(current_node, child)
                    open_list.add(child, child.f)
                elif current_node.g + current_node.get_arc_cost(child) < child.g:
                    attach_and_eval(current_node, child)

        print 'Failed to find a solution within the max number of iterations,', max_num_iterations
        return False
