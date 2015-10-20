class Game(object):
    @staticmethod
    def play_game(start_node, gfx=None, max_num_moves=10000):
        current_node = start_node
        for x in xrange(max_num_moves):
            if gfx is not None:
                gfx.draw(current_node.board.board_values)

            expected_heuristic_value, next_node = current_node.expectimax_max()
            if next_node is None:
                print 'game over'
                print current_node.board
                return x, 'moves'
            else:
                current_node = next_node
            current_node.board.place_new_value_randomly()
