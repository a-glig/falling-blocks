import sys

import pygame
import random

from settings import Settings

from block import Block
from board import Board
from game_stats import GameStats
from user_interface import UserInterface
from button import Button

class FallingBlocks:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Falling Blocks")
        
        self.stats = GameStats(self)
        self.board = Board(self)
        self.ui = UserInterface(self)
        
        # Sprite group contains all blocks that have landed.
        self.all_blocks = pygame.sprite.Group()
        self.choice = self._random_block()
        self.current_block = Block(self, self.choice)

        self.game_active = False
        self.first_game = True

        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop of the game."""
        while True:
            self._check_events()
            
            if self.game_active:
                self.current_block.update_horizontal(self)
                self.current_block.check_collisions_horizontal()
                self.current_block.update_vertical(self)
                self.current_block.check_collisions_vertical()
                if self.current_block.moving_down == False:
                    self._register_block()
                    self._update_grid()
                    self.ui.update_score(self)
                    self.ui.check_high_score()
                    self._update_level()
                    self._switch_block()
            
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypasses and mouse events."""
        self.current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.stats.reset_stats()
            self.ui.prep_score()
            self.ui.prep_level()
            
            self.settings.initialize_dynamic_settings()
            self.all_blocks.empty()
            self.board.initialize_grid()
            self.game_active = True

            if not self.first_game:
                self.choice = self._random_block()
                self.current_block = Block(self, self.choice)
                self.current_block.move_vertical(-1)

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)
        
    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.current_block.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.current_block.moving_left = True
        elif event.key == pygame.K_SPACE:
            if self.game_active:
                self.current_block.move_to_bottom()
        elif event.key == pygame.K_UP:
            if self.game_active:
                self.current_block.rotate(self.choice)

    def _check_keyup_events(self, event):    
        if event.key == pygame.K_RIGHT:
            self.current_block.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.current_block.moving_left = False

    def _register_block(self):
        """
        If block is no longer moving, add it to the sprites group and register
        it in the grid.
        """
        for square in self.current_block.rects:
            s = pygame.sprite.Sprite()
            s.rect = square
            s.color = self.current_block.color
            self.all_blocks.add(s)
            (pos_x,pos_y) = self._get_grid_position(square)
            self.board.grid[pos_y][pos_x] = 1

    def _get_grid_position(self, r):
        """Determine (x,y)-position of a block in the grid."""
        return (
            int((r.x - self.board.rect.x)/self.settings.square_length),
            int((r.y - self.board.rect.y)/self.settings.square_length)
        )

    def _update_grid(self):
        """Update grid if full rows appear and shift blocks accordingly."""
        self.full_rows_current = 0
        current_row = self.settings.rows - 1
        while current_row >= 0:
            if all(entry == 1 for entry in self.board.grid[current_row]):
                # Delete full row and add insert row at the top.
                del self.board.grid[current_row]
                new_row = [0 for _ in range(self.settings.columns)]
                self.board.grid.insert(0,new_row)
                self._update_blocks(current_row)
                
                # Update row count.
                self.settings.full_rows_total += 1
                self.full_rows_current += 1

            else:
                current_row -=1

    def _update_level(self):
        """Increase level and speed of the falling blocks."""
        # Level increases each time 10 full rows have been detected.
        if (self.settings.full_rows_total%10 ==0 and 
                self.settings.full_rows_total > (self.stats.level-1)*10):
            self.stats.level += 1
            self.ui.prep_level()
            self.settings.fall_delay *= self.settings.speedup_scale

    def _update_blocks(self,row):
        """Delete blocks in a full line and move all higher blocks down."""
        for s in self.all_blocks.copy():
            pos_y = self._get_grid_position(s.rect)[1]
            if pos_y == row:
                self.all_blocks.remove(s)
            if pos_y < row:
                s.rect.y += self.settings.square_length

    def _switch_block(self):
        """Create new block to start a new turn."""
        self.choice = self._random_block() 
        self.current_block = Block(self, self.choice)
        if self.current_block.collides_with_group():
            self._register_block()
            self.game_active = False
            self.first_game = False
            pygame.mouse.set_visible(True)

    def _random_block(self):
        """Choose random block, identified by its color."""
        return random.choice(list(self.settings.block_types.keys()))

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.board.draw_board()
        for square in self.all_blocks.sprites():
            self.current_block.draw_single(square)   
        self.current_block.draw_block()
        
        self.ui.show_controls()
        self.ui.show_score()
        
        if not self.game_active:
            self.play_button.draw_button()
        
        pygame.display.flip()
    
if __name__ == '__main__':
    # Make a game instance, and run the game.
    fb = FallingBlocks()
    fb.run_game()