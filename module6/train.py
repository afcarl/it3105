#!/usr/bin/env python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
import os
import h5py
import argparse
import brainstorm as bs
from brainstorm.data_iterators import Minibatches
import re


class Main(object):
    def __init__(self):

        self.args = None
        self.filename = None
        self.trainer = None
        self.getter_tr = None
        self.getter_va = None
        self.network = None

        self.parse_args()
        print('Running with seed', self.args.seed)
        bs.global_rnd.set_seed(self.args.seed)

        self.calculate_filename()
        self.set_up_iterators()
        self.set_up_network()
        self.set_up_trainer()
        self.train()

    def parse_args(self):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(
            '--seed',
            dest='seed',
            type=int,
            required=False,
            default=1
        )
        arg_parser.add_argument(
            '--accuracy-threshold',
            dest='accuracy_threshold',
            type=float,
            required=False,
            default=1
        )
        arg_parser.add_argument(
            '--max-num-epochs',
            dest='max_num_epochs',
            type=int,
            required=False,
            default=20
        )
        arg_parser.add_argument(
            '--learning-rate',
            dest='learning_rate',
            type=float,
            required=False,
            default=0.1
        )
        arg_parser.add_argument(
            '--momentum',
            dest='momentum',
            type=float,
            required=False,
            default=0.9
        )
        arg_parser.add_argument(
            '--num-hidden-layers',
            dest='num_hidden_layers',
            type=int,
            required=False,
            default=1
        )
        arg_parser.add_argument(
            '--activation-functions',
            dest='activation_functions',
            nargs='+',
            type=str,
            choices=['rel', 'tanh', 'sigmoid', 'linear'],
            required=False,
            default=['rel']
        )
        arg_parser.add_argument(
            '--hidden-layer-sizes',
            dest='hidden_layer_sizes',
            nargs='+',
            type=int,
            required=False,
            default=[40]
        )
        arg_parser.add_argument(
            '--dropout-probabilities',
            dest='dropout_probabilities',
            nargs='+',
            type=float,
            required=False,
            default=[0.2, 0.5]
        )
        arg_parser.add_argument(
            '--minibatch-size',
            dest='minibatch_size',
            type=int,
            required=False,
            choices=range(1, 1200),
            default=100
        )
        arg_parser.add_argument(
            '--patience',
            dest='patience',
            type=int,
            required=False,
            default=10
        )
        arg_parser.add_argument(
            '--disable-saving',
            dest='disable_saving',
            nargs='?',
            const=True,
            required=False,
            help='Add this flag to disable saving of the resulting network',
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
        arg_parser.add_argument(
            '--progress-bar',
            dest='progress_bar',
            nargs='?',
            const=True,
            required=False,
            help='Add this flag to show a progress bar during training',
            default=False
        )
        self.args = arg_parser.parse_args()

        if self.args.num_hidden_layers != len(self.args.activation_functions):
            arg_parser.error('Mismatch detected: num_hidden_layers != len(activation_functions)')

        self.args.activation_functions = map(str, self.args.activation_functions)

        if self.args.num_hidden_layers != len(self.args.hidden_layer_sizes):
            arg_parser.error('Mismatch detected: num_hidden_layers != len(hidden_layer_sizes)')

        for hidden_layer_size in self.args.hidden_layer_sizes:
            if hidden_layer_size < 1:
                arg_parser.error('Integers in hidden_layer_sizes must be >= 1')

        if len(self.args.dropout_probabilities) != self.args.num_hidden_layers + 1:
            arg_parser.error(
                'Mismatch detected: len(dropout_probabilities) != num_hidden_layers + 1'
            )

        for dropout_probability in self.args.dropout_probabilities:
            if dropout_probability < 0 or dropout_probability > 1:
                arg_parser.error('Dropout probabilities must be in the range[0, 1]')

    def calculate_filename(self):
        self.filename = (
            'hl' + str(self.args.num_hidden_layers) +
            '__sizes' + str(self.args.hidden_layer_sizes) +
            '__acfn' + str(self.args.activation_functions) +
            '__dr' + str(self.args.dropout_probabilities) +
            '__lr' + str(self.args.learning_rate) +
            '__mb' + str(self.args.minibatch_size) +
            '__mom' + str(self.args.momentum) +
            '__seed' + str(self.args.seed)
        )
        self.filename = re.sub('[^A-Za-z0-9_.]+', '-', self.filename)
        self.filename += ".hdf5"

    def set_up_iterators(self):
        data_dir = '.'
        data_file = os.path.join(data_dir, '2048.hdf5')
        ds = h5py.File(data_file, 'r')['normalized_split']
        x_tr, y_tr = ds['training']['default'][:], ds['training']['targets'][:]
        x_va, y_va = ds['validation']['default'][:], ds['validation']['targets'][:]

        self.getter_tr = Minibatches(self.args.minibatch_size, default=x_tr, targets=y_tr)
        self.getter_va = Minibatches(self.args.minibatch_size, default=x_va, targets=y_va)

    def set_up_network(self):
        input_shape = (20, 1)
        num_output_classes = 4  # up, right, down, left
        inp, fc = bs.tools.get_in_out_layers(
            'classification',
            input_shape,
            num_output_classes,
            projection_name='FC'
        )

        layer_spec = inp >> bs.layers.Dropout(drop_prob=self.args.dropout_probabilities[0])

        for i in range(self.args.num_hidden_layers):
            layer_name = 'Hid' + str(i + 1)
            activation_function = self.args.activation_functions[i]
            layer_size = self.args.hidden_layer_sizes[i]
            layer_spec = layer_spec >> bs.layers.FullyConnected(
                layer_size,
                name=layer_name,
                activation=activation_function
            )
            dropout_probability = self.args.dropout_probabilities[i + 1]
            layer_spec = layer_spec >> bs.layers.Dropout(drop_prob=dropout_probability)

        layer_spec = layer_spec >> fc

        self.network = bs.Network.from_layer(layer_spec)
        if not self.args.disable_cuda:
            from brainstorm.handlers import PyCudaHandler
            self.network.set_handler(PyCudaHandler())
        self.network.initialize(bs.initializers.Gaussian(0.01))
        self.network.set_weight_modifiers({"FC": bs.value_modifiers.ConstrainL2Norm(1)})

    def set_up_trainer(self):
        self.trainer = bs.Trainer(
            bs.training.MomentumStepper(
                learning_rate=self.args.learning_rate,
                momentum=self.args.momentum
            )
        )
        if self.args.progress_bar:
            self.trainer.add_hook(bs.hooks.ProgressBar())
        self.trainer.add_hook(
            bs.hooks.MonitorScores(
                'valid_getter',
                [bs.scorers.Accuracy(out_name='Output.outputs.predictions')],
                name='validation'
            )
        )
        if not self.args.disable_saving:
            self.trainer.add_hook(
                bs.hooks.SaveBestNetwork(
                    'validation.Accuracy',
                    filename=self.filename,
                    name='best weights',
                    criterion='max'
                )
            )
        self.trainer.add_hook(
            bs.hooks.StopAfterThresholdReached(
                'validation.Accuracy',
                threshold=self.args.accuracy_threshold,
                criterion='max'
            )
        )
        self.trainer.add_hook(
            bs.hooks.EarlyStopper(
                'validation.Accuracy',
                patience=self.args.patience,
                criterion='max'
            )
        )
        self.trainer.add_hook(bs.hooks.StopAfterEpoch(self.args.max_num_epochs))

    def train(self):
        self.trainer.train(self.network, self.getter_tr, valid_getter=self.getter_va)
        print("Best validation accuracy:", max(self.trainer.logs["validation"]["Accuracy"]))


if __name__ == '__main__':
    Main()
