import pygame 

class Controls:
    """A visual representation of the game controls."""

    def __init__(self, fb_game):
        self.settings = fb_game.settings
        self.screen = fb_game.screen
        self.screen_rect = self.screen.get_rect()
        self.board_rect = fb_game.board.rect

        self.text_font = pygame.font.SysFont(None, 30)
        self.text_color = (255, 255, 255)

        self.key_font = pygame.font.SysFont("Arial", 30, bold = True)
        self.key_length = 50
        self.key_color = (75, 90, 115)

        self.create_key_up()
        
    def create_key_up(self):
        self.rect_up = pygame.Rect(30, 30, self.key_length, self.key_length)
        self.rect_up.centerx = self.board_rect.right + (
                self.screen_rect.right - self.board_rect.right) // 2 
        self.rect_up.bottom = self.board_rect.bottom
        
        self.arrow_up = self.key_font.render(
            ">", True, self.text_color, self.settings.bg_color)
        self.arrow_up = pygame.transform.rotate(self.arrow_up, 90)
        self.arrow_up_rect = self.arrow_up.get_rect(center = self.rect_up.center)

        self.text_up = self.text_font.render(
            "Rotate", True, self.text_color, self.settings.bg_color)
        self.text_up_rect = self.text_up.get_rect(
            center = (self.rect_up.centerx + 60, self.rect_up.centery))

    def draw(self):
        self.screen.blit(self.arrow_up, self.arrow_up_rect)
        self.screen.blit(self.text_up, self.text_up_rect)
        pygame.draw.rect(self.screen, self.key_color, 
            self.rect_up, width=2, border_radius=10)
