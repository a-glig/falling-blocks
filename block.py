import pygame
from pygame.sprite import Sprite

class Block(Sprite):
    """A class to manage a block that the player controls."""

    def __init__ (self, t_game, type):
        """Create a block at the top of the board."""
        super().__init__()
        self.screen = t_game.screen
        self.screen_rect = t_game.screen.get_rect()
        self.settings= t_game.settings
        self.board = t_game.board
        self.all_blocks = t_game.all_blocks

        # Block settings
        self.type = type
        self.length = self.settings.square_length
        self.color = self.settings.color_types[self.type]
        self.margin_color = self.settings.margin_color
        self.angle = 0

        self.rects = [
            pygame.Rect(x*self.length + self.settings.board_x,
            y*self.length + self.settings.board_y, self.length, self.length) 
            for x,y in self.settings.block_types[self.type][0]
        ]
        
        # Reference rectangle for checking collisions
        self.rect = self.rects[0].unionall(self.rects[1:])
        self.longest_side = max(self.rect.width, self.rect.height)

        # Reference rectangle for performing rotations
        self.box = pygame.Rect(0,0,self.longest_side, self.longest_side)
        self.box.topleft = t_game.board.rect.topleft

        self._adjust_horizontal_position()
        self._adjust_vertical_position()

        # Movement flags; start with block that's not moving horizontally, 
        # but does fall vertically
        self.moving_right = False
        self.moving_left = False
        self.moving_down = True

    def draw_block(self):
        """Draw entire block to the screen."""
        for rect in self.rects:
            pygame.draw.rect(self.screen, self.margin_color, rect) 
            pygame.draw.rect(self.screen, self.color, rect.inflate(-2,-2))

    def draw_single(self, s):
        """Draw a single square to the screen."""
        pygame.draw.rect(self.screen, self.margin_color, s)
        pygame.draw.rect(self.screen, s.color, s.rect.inflate(-2,-2))

    def _adjust_horizontal_position(self):
        """Each block starts at the center of the board."""
        incr = 4 if self.type == 'yellow' else 3
        for r in self.rects:
            r.x += incr*self.length
        self.rect.x += incr*self.length
        self.box.x += incr*self.length
    
    def _adjust_vertical_position(self):
        """Make sure that all blocks are created in the top layer."""
        while self.rect.top > self.board.rect.top:
            for r in self.rects:
                r.y -= self.length
            self.rect.y -= self.length
            self.box.y -= self.length

    def update_horizontal(self,t_game):
        """Update the block's horizontal position based on movement flags."""
        if  (t_game.current_time - self.settings.last_move_time > 
                self.settings.move_delay) and self.moving_down:
            if self.rect.right < self.board.rect.right and self.moving_right:
                self._move_horizontal(1)
                self.settings.last_move_time = t_game.current_time
            if self.rect.left > self.board.rect.left and self.moving_left:
                self._move_horizontal(-1)
                self.settings.last_move_time = t_game.current_time

    def _move_horizontal(self, dir):
        """Move block by one block length to the left/right."""
        for square in self.rects:
            square.x += dir*self.length
        self.rect.x += dir*self.length
        self.box.x += dir*self.length
        
    def update_vertical(self,t_game):
        """Update the block's vertical position at constant rate."""
        if (t_game.current_time - self.settings.last_fall_time >
                self.settings.fall_delay) and self.moving_down:  
            if self.rect.bottom < self.board.rect.bottom:
                self.move_vertical(1)
                self.settings.last_fall_time = t_game.current_time
        if self.rect.bottom >= self.board.rect.bottom:
            self.moving_down = False

    def move_vertical(self, dir):
        """Move block down by one block length and update time."""
        for square in self.rects:
            square.y += dir*self.length
        self.rect.y += dir*self.length
        self.box.y += dir*self.length
        

    def move_to_bottom(self,t_game):
        """Pushes block down to lowest unoccupied space."""
        while self.moving_down == True:
            for square in self.rects:
                square.y += self.length
            self.rect.y += self.length
            self.check_collisions_vertical()
            if self.rect.bottom == self.board.rect.bottom:
                self.moving_down = False

    def check_collisions_horizontal(self):
        """Disable horizontal movement if collision is detected."""
        if self.collides_with_group():
            if self.moving_right:
                self._move_horizontal(-1)
            if self.moving_left:
                self._move_horizontal(+1)
                
    def check_collisions_vertical(self):
        """Disable vertical movement if collision is detected."""
        if self.collides_with_group():
            self.move_vertical(-1)
            self.moving_down = False

    def collides_with_group(self):
        """Check if current block collides with any other object."""
        if pygame.sprite.spritecollide(self, self.all_blocks, False):
            for r in self.rects:
                for s in self.all_blocks:
                    if r.colliderect(s.rect):
                        return True
        return False

    def rotate(self, type):
        """Rotate current block by 90 degrees in right direction."""
        if self.angle == 0:
            self._update_block_position(90, type)
        elif self.angle == 90:
            self._update_block_position(180, type)
        elif self.angle == 180:
            self._update_block_position(270, type)
        else:
            self._update_block_position(0, type)
    
    def _update_block_position(self, angle, type):
        """Update positions of individual squares and the collision box."""
        x0,y0 = self.box.topleft[0], self.box.topleft[1]
        self.new_rects = [
            pygame.Rect(x*self.length + x0,y*self.length + y0, self.length, 
            self.length) for x,y in self.settings.block_types[type][angle]
        ]
        self.new_rect = self.new_rects[0].unionall(self.new_rects[1:])
        
        if self._rotation_allowed():
            self.rects = self.new_rects
            self.rect = self.new_rect    
            self._update_angle()   

    def _rotation_allowed(self):
        """Check if there is space for a rotation."""
        # First check collision of self.box.
        for s in self.all_blocks:
            if self.box.colliderect(s.rect):
                return False
        # Check collision of individual squares.
        for r in self.rects:
            for s in self.all_blocks:
                if r.colliderect(s.rect):
                    return False
        # Check if a rotation would make the block leave the board.
        if (self.box.left < self.board.rect.left or 
                self.box.right > self.board.rect.right or 
                self.box.top < self.board.rect.top):
            return False
        
        return True
    
    def _update_angle(self):
        """Increase angle by 90 degrees.""" 
        if self.angle in (0,90,180):
            self.angle += 90
        else:
            self.angle = 0 



 

        

    