import sys
from os import path
from copy import deepcopy
from uuid import uuid4
import cPickle as pickle

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from module4.board import Board
from module4.board_printer import BoardPrinter


class Main(object):
    def __init__(self):
        self.gfx = BoardPrinter()
        self.board_states = []
        self.moves = []
        self.run()

    @staticmethod
    def get_next_state(current_state, force_down=None):
        if force_down:
            return 5
        elif current_state == 0:
            return 2
        elif current_state == 1:
            return 3
        elif current_state == 2:
            return 1
        elif current_state == 3:
            return 0
        elif current_state == 4:
            return 1
        elif current_state == 5:
            return 4

    def run(self):
        board = Board(size=4)
        board.place_new_value_randomly()

        states = [
            [0],  # move up after having moved left
            [0],  # move up after having moved right
            [1],  # move right
            [3],  # move left
            [1, 3],  # move right after having moved down
            [2]  # move down
        ]
        state = 0

        num_consecutive_ignores = 0
        for x in xrange(1000):
            # self.gfx.draw(board.board_values)
            moved = False
            for direction in states[state]:
                if board.can_move(direction):
                    board_values_copy = deepcopy(board.board_values)
                    self.board_states.append(board_values_copy)
                    self.moves.append(direction)

                    board.move(direction)
                    moved = True
                    break

            if moved:
                state = self.get_next_state(state)
                board.place_new_value_randomly()
                num_consecutive_ignores = 0
            else:
                # print 'ignored move'
                num_consecutive_ignores += 1
                state = self.get_next_state(state, force_down=num_consecutive_ignores >= 3)
            if len(board.get_possible_moves()) == 0:
                # print
                # print 'game over'
                break
        # print x + 1, 'moves'
        # print len(self.board_states), len(self.moves)
        filename = "run_" + str(uuid4()) + ".pickle"
        pickle.dump([self.board_states, self.moves], open('runs/' + filename, "wb"))


if __name__ == '__main__':
    for i in xrange(100):
        Main()
