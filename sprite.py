"""Program containing every sprite"""

import random
import pygame
from pygame.locals import *
from settings import TILESIZE, BOARDWIDTH, PLAYHEIGHT, OLIVE, RED, BLACK

class Player:
    """Class that handles the snake sprite"""
    def __init__(self, screen, x_cord=None, y_cord=None):
        """Initialize settings"""
        self.width = TILESIZE
        self.height = TILESIZE
        self.screen = screen
        self.x_cord, self.y_cord = x_cord, y_cord

    def start(self):
        """Starting position for the snake"""
        start_position = (120, 40)
        self.lst = [start_position]

    def move(self, dx_cord=0, dy_cord=0):
        """Move the snake"""
        #set the last position of the head
        self.x_cord, self.y_cord = self.lst[0]
        #delete the tail
        self.lst.pop()
        #move the head
        self.x_cord += dx_cord * TILESIZE
        self.y_cord += dy_cord * TILESIZE
        #new head
        self.lst.insert(0, (self.x_cord, self.y_cord))

    def is_self_intersecting(self):
        """Check if snake is hitting its body"""
        head = self.lst[0]
        #can't hit the rect directly behind you so 2 instead of 1
        tail_list = self.lst[2:]
        if head in tail_list:
            return True
        return False

    def is_in_play_area(self):
        """Check if snake is within the playing area"""
        j, k = self.lst[0]
        if j >= BOARDWIDTH or k >= PLAYHEIGHT or j < 0 or k < 0:
            return True
        return False

    def eat(self, food):
        """Grow the snake when it touches the apple"""
        self.x_cord, self.y_cord = self.lst[0]
        if self.x_cord >= food.x_cord and self.x_cord+self.width <= food.x_cord+food.width:
            if self.y_cord >= food.y_cord and self.y_cord+self.height <= food.y_cord+food.height:
                #grow the tail by adding last rect
                self.lst.append(self.lst[-1])
                return True
        return False

    def draw(self):
        """Draw the snake"""
        for self.x_cord, self.y_cord in self.lst:
            pygame.draw.rect(self.screen,
                             OLIVE,
                             (self.x_cord, self.y_cord, self.width, self.height))



class Food:
    """Class that handles the food sprite"""
    def __init__(self, screen, player, x_cord=None, y_cord=None):
        """Initialize settings"""
        self.screen = screen
        self.player = player
        self.width = TILESIZE
        self.height = TILESIZE
        self.x_cord, self.y_cord = x_cord, y_cord
        if not self.x_cord or not self.y_cord:
            self.new_position()

    def draw(self):
        """Draw apples"""
        pygame.draw.rect(self.screen, RED, (self.x_cord, self.y_cord, TILESIZE, TILESIZE))

    def new_position(self):
        """Find a position on the board"""
        self.x_cord = random.choice(range(0, BOARDWIDTH, TILESIZE))
        self.y_cord = random.choice(range(0, PLAYHEIGHT, TILESIZE))

class Score:
    """Class that handles the score sprite"""
    def __init__(self, screen, points_per_click=1, click_time_ms=3000):
        """Initialize settings"""
        pygame.font.init()
        self.screen = screen
        self._points_per_click = points_per_click
        self._click_time = click_time_ms
        self._last_time = pygame.time.get_ticks()
        self._score = 0
        self._score_font = pygame.font.SysFont('Arial', 24)

    def add_score(self):
        """Increase score"""
        self._score += 10

    def click(self):
        """Get the time and increase score"""
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self._last_time
        if elapsed > self._click_time:
            self._last_time = current_time
            self._score += self._points_per_click

    def _score_text(self):
        """Display the score"""
        textsurface = self._score_font.render('Score: {}'.format(self._score), False, BLACK)
        self.screen.blit(textsurface, (10, 430))
