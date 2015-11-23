#!/usr/bin/env python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
import os
import argparse
from ast import literal_eval
from os import path
import sys

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from module4.gfx import Gfx
import pygame


class Main(object):
    """
    This visualizer can show a run of the 2048 game played by the AI. Optionally, it can also store
    each frame as a PNG image file.
    """

    def __init__(self):
        self.args = None
        self.board_states = None
        self.gfx = Gfx(grid_width=4, grid_height=4, fps=16.0)

        self.parse_args()
        self.read()
        self.visualize()

    def parse_args(self):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(
            '-i',
            '--input',
            dest='input_filename',
            type=str,
            required=True
        )
        arg_parser.add_argument(
            '-s',
            '--store-screenshots',
            dest='store_screenshots',
            nargs='?',
            const=True,
            required=False,
            help='Add this flag to store every frame as an image file (PNG)',
            default=False
        )
        self.args = arg_parser.parse_args()

    def read(self):
        f = open(self.args.input_filename)
        lines = []
        for line in f:
            lines.append(line.strip())
        f.close()

        self.board_states = []
        for line in lines:
            board_values = literal_eval(line)
            self.board_states.append(board_values)

    def visualize(self):
        for i in range(len(self.board_states)):
            board_values = self.board_states[i]
            self.gfx.draw(board_values)
            if self.args.store_screenshots:
                file_name = '{0}_{1}.png'.format(self.args.input_filename, i)
                pygame.image.save(self.gfx.screen, file_name)


if __name__ == '__main__':
    Main()
