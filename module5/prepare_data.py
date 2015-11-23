#!/usr/bin/env python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
import h5py
import os
from demo import load_flat_text_cases
import numpy as np

"""
This python file reads the flat mnist txt files, preprocesses it and finally saves it in a format
that the training module can read
"""

data_dir = '.'
mnist_training_file_path = os.path.join(data_dir, 'all_flat_mnist_training_cases_text.txt')
mnist_validation_file_path = os.path.join(data_dir, 'all_flat_mnist_testing_cases_text.txt')
hdf_file = os.path.join(data_dir, 'MNIST.hdf5')

print("Extracting and preprocessing MNIST data...")
training_inputs, training_targets = load_flat_text_cases(mnist_training_file_path)
for i in range(len(training_inputs)):
    training_inputs[i] = map(lambda value: value / 255.0, training_inputs[i])  # normalize
training_inputs = np.array(training_inputs).reshape((1, 60000, 28, 28, 1))
training_targets = np.array(training_targets).reshape((1, 60000, 1))

validation_inputs, validation_targets = load_flat_text_cases(mnist_validation_file_path)
for i in range(len(validation_inputs)):
    validation_inputs[i] = map(lambda value: value / 255.0, validation_inputs[i])  # normalize
validation_inputs = np.array(validation_inputs).reshape((1, 10000, 28, 28, 1))
validation_targets = np.array(validation_targets).reshape((1, 10000, 1))


print("Creating HDF5 dataset...")
f = h5py.File(hdf_file, 'w')

variant = f.create_group('normalized_split')
group = variant.create_group('training')
group.create_dataset(name='default', data=training_inputs, compression='gzip')
group.create_dataset(name='targets', data=training_targets, compression='gzip')

group = variant.create_group('validation')
group.create_dataset(name='default', data=validation_inputs, compression='gzip')
group.create_dataset(name='targets', data=validation_targets, compression='gzip')

f.close()
print("Done")
