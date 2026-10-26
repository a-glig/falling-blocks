import pygame

class StatisticsBox:
    """A class to display current game statistics in a box."""

    def __init__(self, fb_game, label, value):
        """Initialize components of the box."""
        self.screen = fb_game.screen
        self.settings = fb_game.settings
        
        self.width, self.height = 300, 100
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 58)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        
        self.label_img = self.font.render(label, True, 
            self.text_color, self.settings.bg_color)
        self.value_img = self.font.render(value, True, 
            self.text_color, self.settings.bg_color)

        self.label_rect = self.label_img.get_rect(
            center = (self.rect.centerx, self.rect.top + 30)
        )
        self.value_rect = self.value_img.get_rect(
            center = (self.rect.centerx, self.rect.top + 70)
        )

    def draw(self):
        self.screen.blit(self.label_img, self.label_rect)
        self.screen.blit(self.value_img, self.value_rect)
        pygame.draw.rect(self.screen, (75, 90, 115), self.rect, width=5)