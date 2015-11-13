#!/usr/bin/env python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
import argparse
import brainstorm as bs
from brainstorm.handlers import PyCudaHandler
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
            '-c',
            '--compare',
            dest='compare',
            nargs='?',
            const=True,
            required=False,
            help='For every classification, show whether or not it is correct',
            default=False
        )
        arg_parser.add_argument(
            '-tr',
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
        arg_parser.add_argument(
            '-te',
            '--test',
            dest='test',
            nargs='?',
            const=True,
            required=False,
            help='Run the network on the test set',
            default=False
        )
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
            help='Show every resulting integer',
            default=False
        )

        self.args = arg_parser.parse_args()
        self.network_filename = self.args.network_filename

    def fetch_mnist_data(self):
        if self.mnist_ds is None:
            data_dir = '.'
            data_file = os.path.join(data_dir, 'MNIST.hdf5')
            self.mnist_ds = h5py.File(data_file, 'r')['normalized_split']
        return self.mnist_ds

    def parse_images(self):
        if self.args.training or self.args.validation or self.args.test:
            self.fetch_mnist_data()

        if self.args.training:
            self.sets['training'] = {'images': [], 'correct_answers': []}
            x_training = self.mnist_ds['training']['default'][:]
            y_training = self.mnist_ds['training']['targets'][:]
            for x in x_training[0]:
                self.sets['training']['images'].append(x)
            for y in y_training[0]:
                self.sets['training']['correct_answers'].append(y[0])
        if self.args.validation:
            self.sets['validation'] = {'images': [], 'correct_answers': []}
            x_validation = self.mnist_ds['validation']['default'][:]
            y_validation = self.mnist_ds['validation']['targets'][:]
            for x in x_validation[0]:
                self.sets['validation']['images'].append(x)
            for y in y_validation[0]:
                self.sets['validation']['correct_answers'].append(y[0])
        if self.args.test:
            self.sets['test'] = {'images': [], 'correct_answers': []}
            x_test = self.mnist_ds['test']['default'][:]
            y_test = self.mnist_ds['test']['targets'][:]
            for x in x_test[0]:
                self.sets['test']['images'].append(x)
            for y in y_test[0]:
                self.sets['test']['correct_answers'].append(y[0])
        if self.args.demo:
            import pickle
            demo_set_filename = 'demo_python2'
            demo_set = pickle.load(open(demo_set_filename, "rb"))

            for i in range(len(demo_set[0])):
                demo_set[0][i] = map(lambda value: value / 255.0, demo_set[0][i])
                adapted_image_array = []
                for row_idx in range(28):
                    adapted_image_array.append([])
                    for col_idx in range(28):
                        adapted_image_array[row_idx].append(demo_set[0][i][row_idx * 28 + col_idx])
                demo_set[0][i] = adapted_image_array

            x_demo = demo_set[0]
            y_demo = map(int, demo_set[1])
            self.sets['demo'] = {'images': x_demo, 'correct_answers': y_demo}

        if self.args.input:
            self.sets['input'] = {'images': []}
        if self.args.input.endswith('.png'):
            image_array = img_helper.read_image(self.args.input)
            self.sets['input']['images'].append(image_array)
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
                        self.sets['input']['images'].append(image_array)
            else:
                print('Failed to parse custom input')

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
        self.network.set_handler(PyCudaHandler())

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
        if self.args.print_results:
            print(max_output_index)
        return max_output_index

    def run(self):
        for set_name, set_dict in self.sets.iteritems():
            set_dict['num_correct'] = 0
            set_dict['num_wrong'] = 0
            if self.args.print_set_names:
                print(set_name)
            for i in range(len(set_dict['images'])):
                image = set_dict['images'][i]
                answer = self.classify(image)
                if 'correct_answers' in set_dict:
                    correct_answer = set_dict['correct_answers'][i]
                    if answer == correct_answer:
                        set_dict['num_correct'] += 1
                        if self.args.compare:
                            print('correct')
                    else:
                        set_dict['num_wrong'] += 1
                        if self.args.compare:
                            print('wrong! should be {}'.format(correct_answer))
            if self.args.stats:
                num_total = (set_dict['num_correct'] + set_dict['num_wrong'])
                if num_total > 0:
                    accuracy = set_dict['num_correct'] / num_total
                    print('Accuracy', accuracy)
                else:
                    print('Accuracy could not be determined')

if __name__ == '__main__':
    Classify()
