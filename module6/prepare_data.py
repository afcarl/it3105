import os
import cPickle as pickle
import sys
from os import path
import h5py
import numpy as np
import gzip

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

        data_set = [board_values, moves]
        # pickle.dump(data_set, open("data_bundle.pickle", "wb"))  # TODO: remove this
        self.create_hdf_file(data_set)
        print 'Done'

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

    @staticmethod
    def create_hdf_file(data_set):
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
        hdf_file = os.path.join('.', '2048.hdf5')
        f = h5py.File(hdf_file, 'w')

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
