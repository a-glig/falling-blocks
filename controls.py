import pygame 

class Controls:
    """A visual representation of the game controls."""

    def __init__(self, fb_game):
        self.screen = fb_game.screen
        self.screen_rect = self.screen.get_rect()
        self.board_rect = fb_game.board.rect

        self.key_color = (75, 90, 115)
        self.width = 2
        self.border_radius = 10

        self.key_down = ArrowKey("down")
        self.key_up = ArrowKey("up", "Rotate")
        self.key_left = ArrowKey("left","Left")
        self.key_right = ArrowKey("right", "Right")
        
        self.position_key_down()
        self.position_key_up()
        self.position_key_left()
        self.position_key_right()
    
    def position_key_down(self):
        self.key_down.rect.centerx = self.board_rect.right + (
                self.screen_rect.right - self.board_rect.right) // 2 
        self.key_down.rect.bottom = self.board_rect.bottom
        self.key_down.position_arrow()
    
    def position_key_up(self):
        self.key_up.rect.center = (self.key_down.rect.centerx, 
                self.key_down.rect.centery - 55)
        self.key_up.position_arrow()
        self.key_up.position_text(60)

    def position_key_left(self):
        self.key_left.rect.center = (self.key_down.rect.centerx - 55, 
                self.key_down.rect.centery)
        self.key_left.position_arrow()
        self.key_left.position_text(-60)

    def position_key_right(self):
        self.key_right.rect.center = (self.key_down.rect.centerx + 55, 
                self.key_down.rect.centery)
        self.key_right.position_arrow()
        self.key_right.position_text(60)

    def draw(self):
        for key in (self.key_down, self.key_up, self.key_left, self.key_right):
            self.screen.blit(key.arrow, key.arrow_rect)
            if key.text != None:
                self.screen.blit(key.text, key.text_rect)
            pygame.draw.rect(self.screen, self.key_color, key.rect, 
                self.width, self.border_radius)

class ArrowKey:
    """A visual representation of an arrow key."""

    def __init__(self, dir, text = "None"):
        self.dir = dir
        self.text = text
        
        self.key_font = pygame.font.SysFont("Arial", 30, bold = True)
        self.bg_color = (18,22,32)
        self.key_length = 50

        self.text_font = pygame.font.SysFont(None, 30)
        self.text_color = (255, 255, 255)

        self.rect = pygame.Rect(0, 0, self.key_length, self.key_length)

        self.arrow = self.key_font.render(
                ">", True, self.text_color, self.bg_color)
        self.rotate_arrow(dir)
        self.arrow_rect = self.arrow.get_rect()

        if self.text != None:
            self.text = self.text_font.render(
                text, True, self.text_color, self.bg_color)
            self.text_rect = self.text.get_rect()

    def rotate_arrow(self, dir):
        "Rotate arrow image by an angle depending on the input."
        rotation_angles = {"right" : 0, "up" : 90, "left": 180, "down": 270}
        self.arrow = pygame.transform.rotate(self.arrow, rotation_angles[dir])
        
    def position_arrow(self):
        "Place arrow in the middle of the key."
        self.arrow_rect.center = self.rect.center

    def position_text(self, x_offset):
        "Position text relative to the key."
        self.text_rect.center = (self.rect.centerx + x_offset, self.rect.centery)