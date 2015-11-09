#!/usr/bin/env python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
import argparse
import brainstorm as bs
import img_helper
import numpy as np


class Classify(object):
    def __init__(self):
        self.args = None
        self.network_filename = None
        self.input_array = None

        self.parse_args()
        self.parse_png()
        if self.args.print_ascii:
            self.print_ascii()
        self.activate()

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
            '-i',
            '--input',
            dest='input_filename',
            type=str,
            required=True,
            help='Name of the png input file. Must be 28x28.'
        )
        arg_parser.add_argument(
            '-p',
            '--print-ascii',
            dest='print_ascii',
            nargs='?',
            const=True,
            required=False,
            help='Print the image in the console in ASCII format',
            default=False
        )

        self.args = arg_parser.parse_args()
        self.network_filename = self.args.network_filename

    def parse_png(self):
        self.input_array = img_helper.read_image(self.args.input_filename)

    def print_ascii(self):
        chars = ' ░▒▓█'
        for row in self.input_array:
            r = ''
            for x in row:
                idx = int(round(x * (len(chars) - 1)))
                r += chars[idx] + chars[idx]
            print(r)

    def activate(self):
        network = bs.Network.from_hdf5(self.network_filename)
        data = np.zeros(shape=(1, 1, 28, 28, 1))
        adapted_input_array = np.array(self.input_array)
        adapted_input_array.shape = (28, 28, 1)
        data[0][0] = adapted_input_array
        network.provide_external_data({
            'default': data,
            'targets': np.zeros(shape=(1, 1, 1))
        })
        network.forward_pass()
        outputs = network.get('FC.outputs.default')
        max_output_index = np.argmax(outputs[0][0])
        print('That looks like', max_output_index)


if __name__ == '__main__':
    Classify()
