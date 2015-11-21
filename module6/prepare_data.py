import os
import cPickle as pickle
import sys
from os import path
import h5py
import numpy as np
import math
import argparse

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from module4.board import Board


class PrepareData(object):
    def __init__(self):
        self.args = None
        self.data_set = None
        self.preprocessing_method = None

        self.parse_args()
        self.read_pickle()
        self.create_hdf_file(self.data_set)
        print 'Done'

    def parse_args(self):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(
            '-p',
            '--preprocessing-method',
            dest='preprocessing_method',
            type=int,
            required=False,
            choices=[1, 2],
            default=1
        )
        self.args = arg_parser.parse_args()

        if self.args.preprocessing_method == 1:
            self.preprocessing_method = self.pre_process1
        else:
            self.preprocessing_method = self.pre_process2

    def read_pickle(self):
        board_values = []
        moves = []
        file_names = next(os.walk('./runs'))[2]
        for file_name in file_names:
            if file_name.startswith('run_') and file_name.endswith('.pickle'):
                arr = pickle.load(open('./runs/' + file_name, "rb"))  # [board_states, moves]

                processed_x_vectors = []
                for board_state in arr[0]:
                    processed_x = self.preprocessing_method(board_state)
                    processed_x_vectors.append(processed_x)
                board_values += processed_x_vectors
                moves += arr[1]
                print file_name

        self.data_set = [board_values, moves]

    @staticmethod
    def pre_process1(board_values_2d):
        board = Board(size=4, board_values=board_values_2d)
        possible_moves = board.get_possible_moves()
        num_empty_tiles, max_tile_value, tile_sum = board.get_tile_stats()

        x_vector = []

        # flat board state
        for row in board_values_2d:
            x_vector += row
        # normalized "linear" tile values
        x_vector = map(lambda y: float(y) / max_tile_value, x_vector)

        # possible moves
        for i in range(4):
            x_vector.append(1 if i in possible_moves else 0)

        return x_vector

    @staticmethod
    def pre_process2(board_values_2d):
        board = Board(size=4, board_values=board_values_2d)
        possible_moves = board.get_possible_moves()
        num_empty_tiles, max_tile_value, tile_sum = board.get_tile_stats()
        max_tile_value_log2 = float(math.log(max_tile_value, 2))

        x_vector = []

        # board state
        for row in board_values_2d:
            x_vector += row
        # normalized log_2 representation
        x_vector = map(lambda y: 0 if y == 0 else math.log(y, 2) / max_tile_value_log2, x_vector)

        # possible moves
        for i in range(4):
            x_vector.append(1 if i in possible_moves else 0)

        # number of empty tiles
        x_vector.append(math.tanh(num_empty_tiles / 8))

        # tile sum
        x_vector.append(math.tanh(tile_sum / 2048))

        # indicate mergeable tiles
        for i in range(board.size):
            for j in range(board.size):
                current_tile = board_values_2d[i][j]
                has_matching_neighbour = \
                    (i - 1 >= 0 and board_values_2d[i - 1][j] == current_tile) \
                    or (i + 1 <= 3 and board_values_2d[i + 1][j] == current_tile) \
                    or (j - 1 >= 0 and board_values_2d[i][j - 1] == current_tile) \
                    or (j + 1 <= 3 and board_values_2d[i][j + 1] == current_tile)
                x_vector.append(1 if has_matching_neighbour else 0)

        # is max tile in corner
        is_max_tile_in_corner = False
        for i in range(board.size):
            for j in range(board.size):
                current_tile = board_values_2d[i][j]
                if current_tile == max_tile_value:
                    if i in (0, 3) and j in (0, 3):
                        is_max_tile_in_corner = True
        x_vector.append(1 if is_max_tile_in_corner else 0)

        return x_vector

    def create_hdf_file(self, data_set):
        num_entries = len(data_set[1])
        num_training_entries = int(num_entries * 0.8)
        num_validation_entries = num_entries - num_training_entries
        print('num_entries', num_entries)
        print('num_training_entries', num_training_entries)
        print('num_validation_entries', num_validation_entries)
        x_vector_size = len(data_set[0][0])
        print('x_vector_size', x_vector_size)

        training_inputs = np.array(data_set[0][:num_training_entries]).reshape(
            (1, num_training_entries, x_vector_size, 1)
        )
        training_targets = np.array(data_set[1][:num_training_entries]).reshape(
            (1, num_training_entries, 1)
        )
        validation_inputs = np.array(data_set[0][num_training_entries:]).reshape(
            (1, num_validation_entries, x_vector_size, 1)
        )
        validation_targets = np.array(data_set[1][num_training_entries:]).reshape(
            (1, num_validation_entries, 1)
        )

        print("Creating HDF5 data set")
        file_name = '2048_{0}.hdf5'.format(self.args.preprocessing_method)
        hdf_file_path = os.path.join('.', file_name)
        f = h5py.File(hdf_file_path, 'w')

        variant = f.create_group('normalized_split')
        training_group = variant.create_group('training')
        training_group.create_dataset(name='default', data=training_inputs, compression='gzip')
        training_group.create_dataset(name='targets', data=training_targets, compression='gzip')

        validation_group = variant.create_group('validation')
        validation_group.create_dataset(name='default', data=validation_inputs, compression='gzip')
        validation_group.create_dataset(name='targets', data=validation_targets, compression='gzip')

        f.close()


if __name__ == '__main__':
    PrepareData()
