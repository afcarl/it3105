import os
import cPickle as pickle
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from module4.board import Board


class PrepareData(object):
    def __init__(self):
        board_values = []
        moves = []
        file_names = next(os.walk('./runs'))[2]
        for file_name in file_names:
            if file_name.startswith('run_') and file_name.endswith('.pickle'):
                arr = pickle.load(open('./runs/' + file_name, "rb"))  # [board_states, moves]

                processed_x_vectors = []
                for board_state in arr[0]:
                    processed_x = self.pre_process(board_state)
                    processed_x_vectors.append(processed_x)
                board_values += processed_x_vectors
                moves += arr[1]
                print file_name

        pickle.dump([board_values, moves], open("data_bundle.pickle", "wb"))
        print 'done'

    @staticmethod
    def pre_process(board_values_2d):
        board = Board(size=4, board_values=board_values_2d)
        possible_moves = board.get_possible_moves()
        num_empty_tiles, max_tile_value, tile_sum = board.get_tile_stats()

        x_vector = []
        for row in board_values_2d:
            x_vector += row
        x_vector = map(lambda y: float(y) / max_tile_value, x_vector)

        for i in range(4):
            x_vector.append(1 if i in possible_moves else 0)
        return x_vector


if __name__ == '__main__':
    PrepareData()
