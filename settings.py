from block_data import block_types as b_types, color_types as b_colors

class Settings:
    """A class to store all settings for Tetris."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        # Board and frame settings
        self.board_width = 500
        self.board_height = 600
        self.board_color = (230,230,230)
        self.board_x = int((self.screen_width - self.board_width)/2)
        self.board_y = int((self.screen_height - self.board_height)/2)

        self.frame_width = 5
        self.frame_color = (26, 89, 150)
        
        # Block settings
        self.square_length = 50
        self.margin_color = (0,0,0)
        self.block_types = b_types
        self.color_types = b_colors

        # Number of rows and columns in game board array
        self.rows = int(self.board_height / self.square_length)
        self.columns = int(self.board_width / self.square_length)

        # Time settings
        self.move_delay = 300
        self.fall_delay = 800
        self.last_move_time = 0
        self.last_fall_time = 0

    