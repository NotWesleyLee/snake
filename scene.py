"""Program to handle levels"""

import sys
import pygame
from pygame.locals import *
from settings import BOARDWIDTH, BLACK, INSTRUCT

class Scene:
    """Main class"""
    def __init__(self, scene_id, screen, background_color):
        self._id = scene_id
        self._screen = screen
        self._background = pygame.Surface(self._screen.get_size())
        self._background.fill(background_color)
        self._is_valid = True
    def draw(self):
        """Draw the background"""
        self._screen.blit(self._background, (0, 0))

    def process_event(self, event):
        """Get events"""
        if event.type == pygame.QUIT:
            print('Good bye!')
            self.set_not_valid()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.set_not_valid()

    def is_valid(self):
        """Check if valid"""
        return self._is_valid

    def set_not_valid(self):
        """Set valid to False"""
        self._is_valid = False
    def update(self):
        """Update screen"""
        pygame.display.update()

    def start_scene(self):
        """Print scene starting"""
        print('starting {}'.format(self))

    def end_scene(self):
        """Print scene ending"""
        print('ending {}'.format(self))

    def __str__(self):
        """Print scene number"""
        return 'Scene {}'.format(self._id)

class TitleScene(Scene):
    """Subclass to handle the title"""
    def __init__(self, scene_id, screen, background_color, title, title_color, title_size):
        super().__init__(scene_id, screen, background_color)
        #set font and size
        title_font = pygame.font.Font(pygame.font.get_default_font(), title_size)
        press_any_key_font = pygame.font.Font(pygame.font.get_default_font(), 18)
        (w_cord, h_cord) = self._screen.get_size()
        #set image text and color
        self._title = title_font.render(title, True, title_color)
        #set image position
        self._title_pos = self._title.get_rect(center=(w_cord/2, h_cord/2))
        self._press_any_key = press_any_key_font.render('Press any key.', True, BLACK)
        self._press_any_key_pos = self._press_any_key.get_rect(center=(w_cord/2, h_cord-80))

    def draw(self):
        """Draw all text"""
        super().draw()
        #draw image with the text
        self._screen.blit(self._title, self._title_pos)
        self._screen.blit(self._press_any_key, self._press_any_key_pos)

    def process_event(self, event):
        """Get events"""
        super().process_event(event)
        if (event.type == pygame.KEYDOWN
                or event.type == pygame.MOUSEBUTTONDOWN
                or event.type == pygame.JOYBUTTONDOWN):
            self.set_not_valid()

class InstructScene(Scene):
    """Subclass to handle the title"""
    def __init__(self, scene_id, screen, background_color, title_size):
        super().__init__(scene_id, screen, background_color)
        (w_cord, h_cord) = self._screen.get_size()
        title_font = pygame.font.Font(pygame.font.get_default_font(), title_size)
        press_any_key_font = pygame.font.Font(pygame.font.get_default_font(), 18)
        self.instructions = []
        self.instructions_pos = []
        self._press_any_key = press_any_key_font.render('Press any key to continue.', True, BLACK)
        self._press_any_key_pos = self._press_any_key.get_rect(center=(w_cord/2, h_cord-80))
        for i in range(len(INSTRUCT)):
            self.instructions.append(title_font.render(INSTRUCT[i], True, BLACK))
            self.instructions_pos.append(self.instructions[i].get_rect(center=(w_cord/2, 140+25*i)))
    def draw(self):
        """Draw all text"""
        super().draw()
        self._screen.blit(self._press_any_key, self._press_any_key_pos)
        for i in range(len(INSTRUCT)):
            self._screen.blit(self.instructions[i], self.instructions_pos[i])

    def process_event(self, event):
        """Get events"""
        super().process_event(event)
        if (event.type == pygame.KEYDOWN
                or event.type == pygame.MOUSEBUTTONDOWN
                or event.type == pygame.JOYBUTTONDOWN):
            self.set_not_valid()

class GameScene(Scene):
    """Subclass to handle the title"""
    def __init__(self, scene_id, screen, background_color, g_snake):
        super().__init__(scene_id, screen, background_color)
        self.g_snake = g_snake
        self.g_snake.start()
        (w_cord, h_cord) = self._screen.get_size()
        press_any_key_font = pygame.font.SysFont('Arial', 16)
        self._press_any_key = press_any_key_font.render('Press any key to continue.', True, BLACK)
        self._press_any_key_pos = self._press_any_key.get_rect(center=(w_cord/2, h_cord-30))

        _lose = pygame.font.SysFont('Arial', 18)
        self.lose = _lose.render("You've lost", True, BLACK)
        _win = pygame.font.SysFont('Arial', 18)
        self.win = _win.render("You've won!", True, BLACK)
        self.win_lose_pos = self.win.get_rect(center=(w_cord/2, h_cord-50))
    def draw(self):
        """Draw all text and start main game loop"""
        self.g_snake.run()
        self._screen.blit(self._press_any_key, self._press_any_key_pos)
        if self.g_snake._win is True:
            self._screen.blit(self.win, self.win_lose_pos)
        else:
            self._screen.blit(self.lose, self.win_lose_pos)

    def process_event(self, event):
        """Get events"""
        super().process_event(event)
        if (event.type == pygame.KEYDOWN
                or event.type == pygame.MOUSEBUTTONDOWN
                or event.type == pygame.JOYBUTTONDOWN):
            self.set_not_valid()


class LeaderScene(Scene):
    """Subclass to handle the title"""
    def __init__(self, scene_id, screen, background_color, title, g_snake):
        super().__init__(scene_id, screen, background_color)
        (w_cord, h_cord) = self._screen.get_size()
        self.highscores = []
        self.highscores_pos = []
        self.g_snake = g_snake
        self.title_font = pygame.font.Font(pygame.font.get_default_font(), 25)
        press_any_key_font = pygame.font.SysFont('Arial', 16)
        self._press_any_key = press_any_key_font.render(
            'Press RETURN to restart or ESC to quit', True, BLACK)
        self._press_any_key_pos = self._press_any_key.get_rect(center=(w_cord/2, h_cord-30))
        self._title = self.title_font.render(title, True, BLACK)
        self._title_pos = self._title.get_rect(center=(w_cord/2, 80))


    def draw(self):
        """Draw all text"""
        super().draw()
        self._screen.blit(self._title, self._title_pos)
        self._screen.blit(self._press_any_key, self._press_any_key_pos)
        for i in range(len(self.highscores)):
            self._screen.blit(self.highscores[i], self.highscores_pos[i])

    def update(self):
        """Draw leaderboard with lastest scores"""
        for i in range(10):
            self.highscores.append(self.title_font.render
                                   ('{}: {}'.format(i + 1, str(self.g_snake.lst[i])), True, BLACK))
            self.highscores_pos.append(self.highscores[i].get_rect(center=(BOARDWIDTH/2, 120+30*i)))
        pygame.display.update()

    def process_event(self, event):
        """Get events and allow players to restart game"""
        super().process_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_RETURN:
                self.set_not_valid()







#l
