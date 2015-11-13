"""
The purpose of this module is to convert the pickled file to a python 2-friendly format
It must be run in python 3
"""

import pickle
import argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
    '-i',
    dest='filename',
    type=str,
    required=False,
    help='Name of the pickled file to be converted',
    default='demo'
)
args = arg_parser.parse_args()

demo_prep_set = pickle.load(open(args.filename, "rb"))

filename_converted = args.filename + "_python2"
pickle.dump(demo_prep_set, open(filename_converted, "wb"), protocol=0)
print('{0} converted to {1}'.format(args.filename, filename_converted))
