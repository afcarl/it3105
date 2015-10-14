import random


class Game(object):
    @staticmethod
    def play_game(start_node, gfx=None, play_randomly=False, max_num_moves=10000):
        if play_randomly:
            sorting_function = lambda child: random.random()
        else:
            sorting_function = lambda child: child.get_heuristic()

        current_node = start_node
        for x in xrange(max_num_moves):
            if gfx is not None:
                gfx.draw(current_node.board.board_values)

            children = current_node.generate_children()
            if len(children) == 0:
                print 'game over'
                print current_node.board
                return x

            sorted_children = sorted(
                children,
                key=sorting_function,
                reverse=True
            )
            current_node = sorted_children[0]
            current_node.board.place_new_value_randomly()

    @staticmethod
    def play_game_randomly(start_node, max_num_moves=10000):
        current_node = start_node
        for x in xrange(max_num_moves):
            directions = range(4)
            random.shuffle(directions)
            moved = False
            for direction in directions:
                if current_node.board.can_move(direction):
                    current_node.board.move(direction)
                    moved = True
                    break

            if not moved:
                return x  # game over

            current_node.board.place_new_value_randomly()
