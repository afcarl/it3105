class BoardPrinter(object):
    """
    An alternative to Gfx. Just prints the board to the console.
    """
    def draw(self, board_values):
        print
        for row in board_values:
            print row
