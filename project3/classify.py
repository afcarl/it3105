#!/usr/bin/env python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
import argparse
import brainstorm as bs
import img_helper
import numpy as np
import os
import h5py


class Classify(object):
    def __init__(self):
        self.args = None
        self.network_filename = None
        self.network = None
        self.mnist_ds = None
        self.sets = {}

        self.parse_args()
        self.parse_images()
        self.initialize_network()

        for set_name, images in self.sets.iteritems():
            if self.args.print_set_names:
                print(set_name)
            for image in images:
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
            required=False,
            default='',
            help='Name of the png input file. Can also be a file with a list of png file names.'
        )
        arg_parser.add_argument(
            '-a',
            '--print-ascii',
            dest='print_ascii',
            nargs='?',
            const=True,
            required=False,
            help='Print the image in the console in ASCII format',
            default=False
        )
        arg_parser.add_argument(
            '-s',
            '--print-set-names',
            dest='print_set_names',
            nargs='?',
            const=True,
            required=False,
            help='Print the set name before the output for that set',
            default=False
        )
        arg_parser.add_argument(
            '-t',
            '--training',
            dest='training',
            nargs='?',
            const=True,
            required=False,
            help='Run the network on the training set',
            default=False
        )
        arg_parser.add_argument(
            '-v',
            '--validation',
            dest='validation',
            nargs='?',
            const=True,
            required=False,
            help='Run the network on the validation set',
            default=False
        )
        """
        arg_parser.add_argument(
            '-d',
            '--demo',
            dest='demo',
            nargs='?',
            const=True,
            required=False,
            help='Run the network on the demo set',
            default=False
        )
        """

        self.args = arg_parser.parse_args()
        self.network_filename = self.args.network_filename

    def fetch_mnist_data(self):
        if self.mnist_ds is None:
            data_dir = '.'
            data_file = os.path.join(data_dir, 'MNIST.hdf5')
            self.mnist_ds = h5py.File(data_file, 'r')['normalized_split']
        return self.mnist_ds

    def parse_images(self):
        if self.args.training or self.args.validation:
            self.fetch_mnist_data()

        if self.args.training:
            self.sets['training'] = []
            x_tr = self.mnist_ds['training']['default'][:]
            y_tr = self.mnist_ds['training']['targets'][:]
            for x in x_tr[0]:
                self.sets['training'].append(x)
        if self.args.validation:
            self.sets['validation'] = []
            x_va = self.mnist_ds['validation']['default'][:]
            y_va = self.mnist_ds['validation']['targets'][:]
            for x in x_va[0]:
                self.sets['validation'].append(x)

        if self.args.input:
            self.sets['input'] = []
        if self.args.input.endswith('.png'):
            image_array = img_helper.read_image(self.args.input)
            self.sets['input'].append(image_array)
        elif self.args.input:
            f = open(self.args.input)
            lines = []
            for line in f:
                lines.append(line.strip())
            f.close()

            if 'png' in lines[0]:
                for file_name in lines:
                    if file_name.endswith('.png'):
                        image_array = img_helper.read_image(file_name)
                        self.sets['input'].append(image_array)
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
