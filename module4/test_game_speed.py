import unittest
from board import Board
from game import Game
from node import Node
import time
from datetime import datetime


class TestGameSpeed(unittest.TestCase):
    def test_speed(self):
        size = 4

        start_time = time.time()

        for i in xrange(2000):
            board = Board(size=size)
            board.place_new_value_randomly()
            board.place_new_value_randomly()
            start_node = Node(board=board)
            Game.play_game_randomly(
                start_node=start_node,
                max_num_moves=25
            )

        with open("game_speed_log.txt", "a") as log:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            execution_time = "%s sec" % (time.time() - start_time)
            line = "\n" + now + ": " + execution_time
            print line
            log.write(line)


if __name__ == '__main__':
    unittest.main()
