class GameStats:
    """Track statistics for the game Block Puzzle."""

    def __init__(self, bp_game):
        """Initialize statistics."""
        self.settings = bp_game.settings
        self.reset_stats()

        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.score = 0
        self.level = 1