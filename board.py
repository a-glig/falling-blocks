import pygame

class Board:
    """A class to manage block coniguration on the game board."""

    def __init__(self, bp_game):
        """Initialize board attributes."""
        self.screen = bp_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = bp_game.settings
        self.color_inner = self.settings.board_color
        self.color_outer = self.settings.frame_color
        self.width = self.settings.frame_width

        # Rectangle for actual gameboard
        self.rect = pygame.Rect(0,0, self.settings.board_width, 
            self.settings.board_height)
        self.rect.center = self.screen_rect.center

        # Rectangle for outer frame of gameboard
        self.frame = pygame.Rect(0,0, self.settings.board_width + 2*self.width, 
            self.settings.board_height + 2*self.width)
        self.frame.center = self.screen_rect.center 
        
        self.initialize_grid()

    def draw_board(self):
        """Draw the board and frame to the screen."""
        pygame.draw.rect(self.screen, self.color_inner, self.rect)
        pygame.draw.rect(self.screen, self.color_outer, self.frame, self.width)

    def initialize_grid(self):
        """Initialize empty grid. 0 (1) represents empty (filled) cell."""
        self.grid = [ 
            [0]*self.settings.columns for _ in range(self.settings.rows)
        ]
        # Helper variable to keep track of filled rows
        self.full_rows = [False for _ in range(self.settings.rows)]