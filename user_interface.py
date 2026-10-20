import pygame.font

class UserInterface:
    """A class to show elements that communicate information to the player."""

    def __init__(self,fb_game):
        """Initialize scorekeeping attributes."""
        self.screen = fb_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = fb_game.settings
        self.board = fb_game.board
        self.stats = fb_game.stats

        # Settings for scoring information.
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

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
        score_str = "Score: " + f"{self.stats.score:,}"
        self.score_image = self.font.render(score_str, True, 
            self.text_color, self.settings.bg_color)
    
        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score_str = "High score: " + f"{self.stats.high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True, 
            self.text_color, self.settings.bg_color)
        
        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = "Level: " + str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
            self.text_color, self.settings.bg_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

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
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)

    def position_controls(self):
        """Position image showing game controls."""
        self.controls_rect = self.controls_scaled.get_rect()
        self.controls_rect.bottom = self.board.rect.bottom
        controls_x_offset = (self.board.rect.x - self.controls_rect.width)/2
        self.controls_rect.x += controls_x_offset

    def show_controls(self):
        """Draw control settings to the screen."""
        self.screen.blit(self.controls_scaled, self.controls_rect)