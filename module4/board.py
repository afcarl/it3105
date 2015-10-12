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
        for other_column_index in range(column_index - 1, -1, -1):
            if self.board_values[row_index][other_column_index] in numbers_to_check_for:
                return True
        return False

    def move(self, direction):
        pass  # TODO
