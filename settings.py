from block_data import block_types, color_types 

class Settings:
    """A class to store all settings for the game Falling Blocks."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        # Board and frame settings.
        self.board_width = 400
        self.board_height = 640
        self.board_color = (230,230,230)
        self.board_x = int((self.screen_width - self.board_width)/2)
        self.board_y = int((self.screen_height - self.board_height)/2)

        self.frame_width = 5
        self.frame_color = (26, 89, 150)

        # Block settings.
        self.square_length = 40
        self.margin_color = (0,0,0)
        self.block_types = block_types
        self.color_types = color_types

        # Number of rows and columns in game board array.
        self.rows = int(self.board_height / self.square_length)
        self.columns = int(self.board_width / self.square_length)

        # Initial time stamps.
        self.last_move_time = 0
        self.last_fall_time = 0

        # Delay for horizontal movement.
        self.move_delay = 250

        # How quickly game speeds by increasing falling speed.
        self.speedup_scale = 0.9

        # Scoring settings. Key: Number of filled rows, value: points.
        self.points= {1:40, 2:100, 3:300, 4:1200}

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.fall_delay = 800
        self.full_rows_total = 0

    