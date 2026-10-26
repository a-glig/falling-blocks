import pygame.font
from ui_elements import StatisticsBox

class UserInterface:
    """A class to show elements that communicate information to the player."""

    def __init__(self,fb_game):
        """Initialize scorekeeping attributes."""
        self.fb_game = fb_game
        self.screen = fb_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = fb_game.settings
        self.board = fb_game.board
        self.stats = fb_game.stats

        # Prepare the initial score image.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        
        # Import and position image showing control settings
        controls = pygame.image.load('images/controls.png')
        self.controls_scaled = pygame.transform.smoothscale(controls, (250, 150))
        self.position_controls()

    def prep_score(self):
        """Turn the score into a rendered image."""
        label, value = "Score", f"{self.stats.score:,}"
        self.score = StatisticsBox(self.fb_game, label, value)
    
        x = self.board.rect.right + (
                self.screen_rect.right - self.board.rect.right) // 2 
        y = self.board.rect.top 
        self.score.set_position((x,y))

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        label, value = "High score", f"{self.stats.high_score:,}"
        self.high_score = StatisticsBox(self.fb_game, label, value)

        x = self.board.rect.right + (
                self.screen_rect.right - self.board.rect.right) // 2 
        y = self.score.rect.top + 150
        self.high_score.set_position((x,y))

    def prep_level(self):
        """Turn the level into a rendered image."""
        label, value = "Level", str(self.stats.level)
        self.level = StatisticsBox(self.fb_game, label, value)

        x = self.board.rect.right + (
                self.screen_rect.right - self.board.rect.right) // 2 
        y = self.high_score.rect.top + 150
        self.level.set_position((x,y))

    def update_score(self, fb_game):
        """Update player score by checking the number of rows that were filled."""
        if fb_game.full_rows_current > 0:
            row_points = self.settings.points[fb_game.full_rows_current]
            self.stats.score += row_points*self.stats.level 
            self.prep_score()

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        """Draw score to the screen."""
        self.score.draw()
        self.high_score.draw()
        self.level.draw()

    def position_controls(self):
        """Position image showing game controls."""
        self.controls_rect = self.controls_scaled.get_rect()
        self.controls_rect.bottom = self.board.rect.bottom
        controls_x_offset = (self.board.rect.x - self.controls_rect.width)/2
        self.controls_rect.x += controls_x_offset

    def show_controls(self):
        """Draw control settings to the screen."""
        self.screen.blit(self.controls_scaled, self.controls_rect)