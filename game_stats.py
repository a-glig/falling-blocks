class GameStats:
    """Track statistics for the Tetris game."""

    def __init__(self, t_game):
        """Initialize statistics."""
        self.settings = t_game.settings
        self.reset_stats()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.score = 0
        self.level = 1