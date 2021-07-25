"""Program that runs the main game"""
# too many branchs and statements at 105 but that's all for controls
import sys
import pickle
import pygame
from pygame.locals import *
from sprite import Player, Food, Score
from settings import TILESIZE, BOARDWIDTH, PLAYHEIGHT, FPS, LIGHTBLUE, BLACK

class Game:
    """Class that handles the game"""
    def __init__(self, screen, direction, is_valid, _win=None):
        pygame.init()
        #get jotstick count
        joystick_count = pygame.joystick.get_count()
        if joystick_count == 0:
            print("Error, I didn't find any joysticks.")
        else:
            p_joystick = pygame.joystick.Joystick(0)
            p_joystick.joystick.init()
        self.screen = screen
        self.direction = direction
        self.is_valid = is_valid
        self._win = _win
        self.clock = pygame.time.Clock()
        self.dt_set = self.clock.tick(FPS)
        pygame.key.set_repeat(500, 100)
        self.player = Player(self.screen)
        self.food = Food(self.screen, self.player)
        self.lst = []
        self.time_left_disabled = 0

    def start(self):
        """Initialize settings"""
        self.direction = 'right'
        self.food.new_position()
        self.player.start()
        self.score = Score(self.screen)
        self.is_valid = True
        self._win = False

    def quit(self):
        """Quit fuction to get out of run loop"""
        self.read()
        #add newest score
        self.lst.append(self.score._score)
        self.lst.sort(reverse=True)
        #write into pickle
        self.write()
        self.is_valid = False

    def write(self):
        """Write to pickle file"""
        with open('Highscores', 'wb') as pickle_open:
            pickle.dump(self.lst, pickle_open)

    def read(self):
        """Read from pickle file"""
        pickle_off = open('Highscores', 'rb')
        self.lst = pickle.load(pickle_off)

    def winning_son(self):
        """Check if player has won"""
        if len(self.player.lst) == 160:
            self._win = True
            return True
        return False

    def run(self):
        """Main loop to run the game"""
        while self.is_valid:
            self.clock.tick(FPS)
            #draw backgrounds
            self.draw()
            #get player movement
            self.events()
            #check all conditions
            self.checklist()
            self.player.draw()
            self.food.draw()
            self.score.click()
            pygame.display.update()

    def checklist(self):
        """Check all conditions for game"""
        #check for touching apple
        if self.player.eat(self.food):
            self.score.add_score()
            #don't allow for the apple to spawn inside the snake
            while (self.food.x_cord, self.food.y_cord) in self.player.lst:
                self.food.new_position()
        if self.player.is_self_intersecting():
            self.quit()
        if self.player.is_in_play_area():
            self.quit()
        if self.winning_son():
            self.quit()

    def draw(self):
        """Draw/ update the game"""
        self.screen.fill(LIGHTBLUE)
        self.drawgrid()
        self.score._score_text()

    def drawgrid(self):
        """Draw the grid"""
        for x_cord in range(0, BOARDWIDTH, TILESIZE):
            for y_cord in range(0, PLAYHEIGHT, TILESIZE):
                rect = pygame.Rect(x_cord, y_cord, TILESIZE, TILESIZE)
                pygame.draw.rect(self.screen, BLACK, rect, 1)

    def events(self):
        """Handles the movement of the snake"""
        for event in pygame.event.get():
            self.update_disabled(self.dt_set)
            if event.type == pygame.QUIT:
                self.quit()
            #keyboard movement
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_UP and self.direction != 'down' and self.is_enabled():
                    self.direction = 'up'
                    self.disable()

                if event.key == K_DOWN and self.direction != 'up' and self.is_enabled():
                    self.direction = 'down'
                    self.disable()

                if event.key == K_LEFT and self.direction != 'right' and self.is_enabled():
                    self.direction = 'left'
                    self.disable()

                if event.key == K_RIGHT and self.direction != 'left' and self.is_enabled():
                    self.direction = 'right'
                    self.disable()

            #mouse movement
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x, pos_y = pygame.mouse.get_pos()
                if (pos_y < self.player.y_cord
                        and self.direction != 'down'
                        and self.direction != 'up'
                        and self.is_enabled()):
                    self.direction = 'up'
                    self.disable()

                if (pos_y > self.player.y_cord
                        and self.direction != 'up'
                        and self.direction != 'down'
                        and self.is_enabled()):
                    self.direction = 'down'
                    self.disable()

                if (pos_x < self.player.x_cord
                        and self.direction != 'right'
                        and self.direction != 'left'
                        and self.is_enabled()):
                    self.direction = 'left'
                    self.disable()

                if (pos_x > self.player.x_cord
                        and self.direction != 'left'
                        and self.direction != 'right'
                        and self.is_enabled()):
                    self.direction = 'right'
                    self.disable()

            #joystick movement
            if event.type == pygame.JOYBUTTONDOWN:
                x_axis = p_joystick.get_axis(0)
                y_axis = p_joystick.get_axis(1)
                if event.key == p_joystick.get_button(7):
                    pygame.quit()
                    sys.exit()
                if y_axis < 0 and self.direction != 'down' and self.is_enabled():
                    self.direction = 'up'
                    self.disable()

                if y_axis > 0 and self.direction != 'up' and self.is_enabled():
                    self.direction = 'down'
                    self.disable()

                if x_axis < 0 and self.direction != 'right' and self.is_enabled():
                    self.direction = 'left'
                    self.disable()

                if x_axis > 0 and self.direction != 'left' and self.is_enabled():
                    self.direction = 'right'
                    self.disable()
        #auto move and wait so snake doesn't fly off
        self.automove()
        pygame.time.wait(250)

    def automove(self):
        """Automatically move the snake at a constant rate"""
        if self.direction == 'up':
            self.player.move(dy_cord=-1)

        if self.direction == 'down':
            self.player.move(dy_cord=1)

        if self.direction == 'left':
            self.player.move(dx_cord=-1)

        if self.direction == 'right':
            self.player.move(dx_cord=1)

    def disable(self):
        """Stop inputs"""
        self.time_left_disabled = 50

    def update_disabled(self, time_taken):
        """Update timer for inputs"""
        self.time_left_disabled = max(self.time_left_disabled - time_taken, 0)

    def is_enabled(self):
        """Allow for inputs"""
        return self.time_left_disabled <= 0
