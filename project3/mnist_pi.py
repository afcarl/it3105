#!/usr/bin/env python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
import os
import h5py
import argparse
import brainstorm as bs
from brainstorm.data_iterators import Minibatches
from brainstorm.handlers import PyCudaHandler


class Main(object):
    def __init__(self):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(
            '--seed',
            dest='seed',
            type=int,
            required=False,
            default=42
        )
        arg_parser.add_argument(
            '--accuracy-threshold',
            dest='accuracy_threshold',
            type=float,
            required=False,
            default=0.96
        )
        arg_parser.add_argument(
            '--max-num-epochs',
            dest='max_num_epochs',
            type=int,
            required=False,
            default=500
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

        self.args = arg_parser.parse_args()

        bs.global_rnd.set_seed(self.args.seed)

        self.trainer = None
        self.getter_tr = None
        self.getter_va = None
        self.network = None

        self.set_up_iterators()
        self.set_up_network()
        self.set_up_trainer()
        self.train()

    def set_up_iterators(self):
        data_dir = os.environ.get('BRAINSTORM_DATA_DIR', '../data')
        data_file = os.path.join(data_dir, 'MNIST.hdf5')
        ds = h5py.File(data_file, 'r')['normalized_split']
        x_tr, y_tr = ds['training']['default'][:], ds['training']['targets'][:]
        x_va, y_va = ds['validation']['default'][:], ds['validation']['targets'][:]

        self.getter_tr = Minibatches(100, default=x_tr, targets=y_tr)
        self.getter_va = Minibatches(100, default=x_va, targets=y_va)

    def set_up_network(self):
        inp, fc = bs.tools.get_in_out_layers('classification', (28, 28, 1), 10,
                                             projection_name='FC')
        self.network = bs.Network.from_layer(
            inp >>
            bs.layers.Dropout(drop_prob=0.2) >>
            bs.layers.FullyConnected(1200, name='Hid1', activation='rel') >>  # rel = rectified linear
            bs.layers.Dropout(drop_prob=0.5) >>
            bs.layers.FullyConnected(1200, name='Hid2', activation='rel') >>
            bs.layers.Dropout(drop_prob=0.5) >>
            fc
        )

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
        self.trainer.add_hook(bs.hooks.ProgressBar())
        scorers = [bs.scorers.Accuracy(out_name='Output.outputs.predictions')]
        self.trainer.add_hook(bs.hooks.MonitorScores('valid_getter', scorers,
                                                     name='validation'))
        self.trainer.add_hook(bs.hooks.SaveBestNetwork('validation.Accuracy',
                                                       filename='mnist_pi_best.hdf5',
                                                       name='best weights',
                                                       criterion='max'))
        self.trainer.add_hook(
            bs.hooks.StopAfterThresholdReached(
                'validation.Accuracy',
                threshold=self.args.accuracy_threshold,
                criterion='at_least'
            )
        )
        self.trainer.add_hook(bs.hooks.StopAfterEpoch(self.args.max_num_epochs))

    def train(self):
        self.trainer.train(self.network, self.getter_tr, valid_getter=self.getter_va)
        print("Best validation accuracy:", max(self.trainer.logs["validation"]["Accuracy"]))


if __name__ == '__main__':
    Main()
