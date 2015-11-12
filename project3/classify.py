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
        self.network = None
        self.images = []

        self.parse_args()
        self.parse_images()
        self.initialize_network()
        for image in self.images:
            self.classify(image)

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
            dest='input',
            type=str,
            required=True,
            help='Name of the png input file. Can also be a file with a list of png file names.'
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
        arg_parser.add_argument(
            '-m',
            '--mode',
            dest='mode',
            choices=['one', 'many'],
            required=False,
            default='one'
        )

        self.args = arg_parser.parse_args()
        self.network_filename = self.args.network_filename

    def parse_images(self):
        if self.args.input.endswith('.png'):
            image_array = img_helper.read_image(self.args.input)
            self.images.append(image_array)
        else:
            f = open(self.args.input)
            lines = []
            for line in f:
                lines.append(line.strip())
            f.close()

            if 'png' in lines[0]:
                for file_name in lines:
                    if file_name.endswith('.png'):
                        image_array = img_helper.read_image(file_name)
                        self.images.append(image_array)
            else:
                pass
                # TODO: parse text file with one image for each line

    @staticmethod
    def print_ascii(image):
        chars = ' ░▒▓█'
        for row in image:
            r = ''
            for x in row:
                idx = int(round(x * (len(chars) - 1)))
                r += chars[idx] + chars[idx]
            print(r)

    def initialize_network(self):
        self.network = bs.Network.from_hdf5(self.network_filename)

    def classify(self, image):
        if self.args.print_ascii:
            self.print_ascii(image)
        data = np.zeros(shape=(1, 1, 28, 28, 1))
        adapted_input_array = np.array(image)
        adapted_input_array.shape = (28, 28, 1)
        data[0][0] = adapted_input_array
        self.network.provide_external_data({
            'default': data,
            'targets': np.zeros(shape=(1, 1, 1))
        })
        self.network.forward_pass()
        outputs = self.network.get('FC.outputs.default')
        max_output_index = np.argmax(outputs[0][0])
        print(max_output_index)


if __name__ == '__main__':
    Classify()
