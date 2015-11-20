#!/usr/bin/env python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
import argparse
import brainstorm as bs
import numpy as np
import os
import h5py
import sys
from os import path
from prepare_data import PrepareData
from collections import Counter

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from module4.board import Board


class Play(object):
    def __init__(self, init=True):
        self.args = None
        self.network_filename = None
        self.network = None
        self.max_tile_value = None

        if init:
            self.parse_args()
            self.initialize_network()
            self.run()

    def parse_args(self):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(
            '-n',
            '--network',
            dest='network_filename',
            type=str,
            required=True,
            help='Name of the input hdf5 file with the neural network'
        )

        arg_parser.add_argument(
            '-st',
            '--stats',
            dest='stats',
            nargs='?',
            const=True,
            required=False,
            help='Show accuracy stats',
            default=False
        )
        arg_parser.add_argument(
            '-r',
            '--print-results',
            dest='print_results',
            nargs='?',
            const=True,
            required=False,
            help='Show every board state',
            default=False
        )
        arg_parser.add_argument(
            '--disable-cuda',
            dest='disable_cuda',
            nargs='?',
            const=True,
            required=False,
            help='Add this flag to use the CPU instead of the GPU',
            default=False
        )

        self.args = arg_parser.parse_args()
        self.network_filename = self.args.network_filename

    def initialize_network(self):
        self.network = bs.Network.from_hdf5(self.network_filename)
        if not self.args.disable_cuda:
            from brainstorm.handlers import PyCudaHandler
            self.network.set_handler(PyCudaHandler())

    def choose_direction(self, board_values_2d):
        data = np.zeros(shape=(1, 1, 20, 1))
        processed_input = PrepareData.pre_process(board_values_2d)
        adapted_input_array = np.array(processed_input)
        adapted_input_array.shape = (20, 1)
        data[0][0] = adapted_input_array
        self.network.provide_external_data({
            'default': data,
            'targets': np.zeros(shape=(1, 1, 1))
        })
        self.network.forward_pass()
        outputs = self.network.get('FC.outputs.default')
        prioritized_directions = outputs[0][0].argsort()[-4:][::-1]
        return prioritized_directions

    def run(self):
        board = Board(size=4)
        board.place_new_value_randomly()

        for i in xrange(2000):
            if self.args.print_results:
                print('iteration', i)
                print(board)
            directions = self.choose_direction(board.board_values)
            has_moved = False
            for direction in directions:
                if board.can_move(direction):
                    board.move(direction)
                    has_moved = True
                    break
            if not has_moved:
                num_empty_tiles, max_tile_value, tile_sum = board.get_tile_stats()
                print(max_tile_value)
                self.max_tile_value = max_tile_value
                break
            board.place_new_value_randomly()

if __name__ == '__main__':
    max_tile_values = []
    for i in xrange(50):
        p = Play()
        max_tile_values.append(p.max_tile_value)

    # random play

    max_tile_value_counts = Counter(max_tile_values)
    print('stats:', max_tile_value_counts)

    #p = scipy.stats.ttest_ind([MY RESULTS], [RANDOM PLAYER RESULTS]).pvalue
    #num_points = max(0,min(7, ceiling(-log(p,10))))
