import sys
import pygame

pygame.display.init()
pygame.font.init()


class Gfx(object):
    """
    This class takes care of drawing the state of the search to a window using pygame
    """
    size = width, height = 540, 540
    WHITE = 255, 255, 255
    FOREGROUND_SMALL = (119, 110, 101)
    FOREGROUND_LARGER = (249, 246, 242)
    COLORS = {
        0: (158, 148, 138),
        2: (238, 228, 218),
        4: (237, 224, 200),
        8: (242, 177, 121),
        16: (245, 149, 99),
        32: (246, 124, 95),
        64: (246, 94, 59),
        128: (237, 207, 114),
        256: (237, 204, 97),
        512: (237, 200, 80),
        1024: (237, 197, 63),
        2048: (255, 174, 0),
        "other": (130, 122, 39)
    }

    def __init__(self, grid_width, grid_height, fps):
        self.grid_width = grid_width
        self.grid_height = grid_height

        self.GU_X = self.width / float(grid_width)
        self.GU_Y = self.height / float(grid_height)

        self.screen = pygame.display.set_mode(self.size)

        self.clock = pygame.time.Clock()  # used for limiting the fps, so one can see each step
        self.fps = fps

        self.font = pygame.font.SysFont("monospace", 36)

    def get_color(self, number):
        if number in self.COLORS:
            return self.COLORS[number]
        return self.COLORS["other"]

    def draw_tile(self, x, y, color, number):
        # draw colored tile
        rect = pygame.Rect(
            x * self.GU_X + 1,
            y * self.GU_Y + 1,
            self.GU_X - 2,
            self.GU_Y - 2
        )
        pygame.draw.rect(self.screen, color, rect)

        # draw number on tile
        if number != 0:
            color = self.FOREGROUND_SMALL if number < 8 else self.FOREGROUND_LARGER
            number_str = str(number)
            label = self.font.render(str(number), 1, color)
            label_position = (
                (x + (0.5 - 0.08 * len(number_str))) * self.GU_X,
                (y + 0.35) * self.GU_Y
            )
            self.screen.blit(label, label_position)

    def draw_rows(self, board_values):
        for i in xrange(len(board_values)):
            for j in xrange(len(board_values[i])):
                number = board_values[i][j]
                color = self.get_color(number)
                self.draw_tile(j, i, color, number)

    def draw(self, board_values):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.fps /= 2  # halve the fps
                    if self.fps < 0.5:
                        self.fps = 0.5
                if event.key == pygame.K_UP:
                    self.fps *= 2  # double the fps
                    if self.fps > 256.0:
                        self.fps = 256.0

        self.clock.tick(self.fps)

        self.screen.fill(self.WHITE)

        self.draw_rows(board_values)

        pygame.display.flip()
