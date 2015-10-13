import random


class Board(object):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __init__(self, size=4):
        self.size = size

        self.board_values = []
        for i in xrange(size):
            self.board_values.append([])
            for j in xrange(size):
                self.board_values[i].append(0)

    def set_board_values(self, board_values):
        self.board_values = board_values

    def get_possible_moves(self):
        moves = []
        if self.can_move_up():
            moves.append(self.UP)
        if self.can_move_right:
            moves.append(self.RIGHT)
        if self.can_move_down():
            moves.append(self.DOWN)
        if self.can_move_left():
            moves.append(self.LEFT)
        return moves

    def can_move(self, direction):
        """
        :param direction: 0, 1, 2 or 3
        :return:
        """
        if direction == self.UP:
            return self.can_move_up()
        elif direction == self.RIGHT:
            return self.can_move_right()
        elif direction == self.DOWN:
            return self.can_move_down()
        elif direction == self.LEFT:
            return self.can_move_left()

    def can_move_up(self):
        for row_index in range(1, self.size):
            for column_index in xrange(self.size):
                if self.board_values[row_index][column_index] > 0 \
                        and self.can_move_tile_up(row_index, column_index):
                    return True
        return False

    def can_move_tile_up(self, row_index, column_index):
        numbers_to_check_for = (0, self.board_values[row_index][column_index])
        for other_row_index in range(row_index - 1, -1, -1):
            if self.board_values[other_row_index][column_index] in numbers_to_check_for:
                return True
        return False

    def can_move_right(self):
        for row_index in xrange(self.size):
            for column_index in xrange(self.size - 1):
                if self.board_values[row_index][column_index] > 0 \
                        and self.can_move_tile_right(row_index, column_index):
                    return True
        return False

    def can_move_tile_right(self, row_index, column_index):
        numbers_to_check_for = (0, self.board_values[row_index][column_index])
        for other_column_index in range(column_index + 1, self.size):
            if self.board_values[row_index][other_column_index] in numbers_to_check_for:
                return True
        return False

    def can_move_down(self):
        for row_index in range(self.size - 1):
            for column_index in xrange(self.size):
                if self.board_values[row_index][column_index] > 0 \
                        and self.can_move_tile_down(row_index, column_index):
                    return True
        return False

    def can_move_tile_down(self, row_index, column_index):
        numbers_to_check_for = (0, self.board_values[row_index][column_index])
        for other_row_index in range(row_index + 1, self.size):
            if self.board_values[other_row_index][column_index] in numbers_to_check_for:
                return True
        return False

    def can_move_left(self):
        for row_index in xrange(self.size):
            for column_index in range(1, self.size):
                if self.board_values[row_index][column_index] > 0 \
                        and self.can_move_tile_left(row_index, column_index):
                    return True
        return False

    def can_move_tile_left(self, row_index, column_index):
        numbers_to_check_for = (0, self.board_values[row_index][column_index])
        for other_column_index in reversed(xrange(column_index)):
            if self.board_values[row_index][other_column_index] in numbers_to_check_for:
                return True
        return False

    def move(self, direction):
        """
        :param direction: 0, 1, 2 or 3
        :return:
        """
        if direction == self.UP:
            return self.move_up()
        elif direction == self.RIGHT:
            return self.move_right()
        elif direction == self.DOWN:
            return self.move_down()
        elif direction == self.LEFT:
            return self.move_left()

    def move_up(self):
        for row_index in range(1, self.size):
            for column_index in xrange(self.size):
                if self.board_values[row_index][column_index] > 0:
                    self.move_tile_up(row_index, column_index)

    def move_tile_up(self, row_index, column_index):
        value = self.board_values[row_index][column_index]
        potential_new_row_index = None
        for other_row_index in reversed(xrange(row_index)):
            other_value = self.board_values[other_row_index][column_index]
            if other_value == value:
                # combine
                self.board_values[other_row_index][column_index] = value + other_value
                self.board_values[row_index][column_index] = 0
                return
            elif other_value == 0:
                potential_new_row_index = other_row_index
            else:
                break
        if potential_new_row_index is not None:
            # move
            self.board_values[row_index][column_index] = 0
            self.board_values[potential_new_row_index][column_index] = value

    def move_right(self):
        for row_index in xrange(self.size):
            for column_index in reversed(xrange(self.size - 1)):
                if self.board_values[row_index][column_index] > 0:
                    self.move_tile_right(row_index, column_index)

    def move_tile_right(self, row_index, column_index):
        value = self.board_values[row_index][column_index]
        potential_new_column_index = None
        for other_column_index in range(column_index + 1, self.size):
            other_value = self.board_values[row_index][other_column_index]
            if other_value == value:
                # combine
                self.board_values[row_index][other_column_index] = value + other_value
                self.board_values[row_index][column_index] = 0
                return
            elif other_value == 0:
                potential_new_column_index = other_column_index
            else:
                break
        if potential_new_column_index is not None:
            # move
            self.board_values[row_index][column_index] = 0
            self.board_values[row_index][potential_new_column_index] = value

    def move_down(self):
        for row_index in reversed(xrange(self.size - 1)):
            for column_index in xrange(self.size):
                if self.board_values[row_index][column_index] > 0:
                    self.move_tile_down(row_index, column_index)

    def move_tile_down(self, row_index, column_index):
        value = self.board_values[row_index][column_index]
        potential_new_row_index = None
        for other_row_index in range(row_index + 1, self.size):
            other_value = self.board_values[other_row_index][column_index]
            if other_value == value:
                # combine
                self.board_values[other_row_index][column_index] = value + other_value
                self.board_values[row_index][column_index] = 0
                return
            elif other_value == 0:
                potential_new_row_index = other_row_index
            else:
                break
        if potential_new_row_index is not None:
            # move
            self.board_values[row_index][column_index] = 0
            self.board_values[potential_new_row_index][column_index] = value

    def move_left(self):
        for row_index in xrange(self.size):
            for column_index in range(1, self.size):
                if self.board_values[row_index][column_index] > 0:
                    self.move_tile_left(row_index, column_index)

    def move_tile_left(self, row_index, column_index):
        value = self.board_values[row_index][column_index]
        potential_new_column_index = None
        for other_column_index in reversed(xrange(column_index)):
            other_value = self.board_values[row_index][other_column_index]
            if other_value == value:
                # combine
                self.board_values[row_index][other_column_index] = value + other_value
                self.board_values[row_index][column_index] = 0
                return
            elif other_value == 0:
                potential_new_column_index = other_column_index
            else:
                break
        if potential_new_column_index is not None:
            # move
            self.board_values[row_index][column_index] = 0
            self.board_values[row_index][potential_new_column_index] = value

    def place_new_value_randomly(self):
        empty_positions = []
        for row_index in xrange(self.size):
            for column_index in range(self.size):
                if self.board_values[row_index][column_index] == 0:
                    empty_positions.append((row_index, column_index))
        if len(empty_positions) > 0:
            row_index, column_index = random.choice(empty_positions)
            if random.random() >= 0.9:
                self.board_values[row_index][column_index] = 4
            else:
                self.board_values[row_index][column_index] = 2

    def __repr__(self):
        result = ''
        for row in self.board_values:
            result += str(row) + "\n"
        return result
