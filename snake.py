#!/usr/bin/env python3
""" Snake game written in Python3 using pygame"""

import pygame
from game import Game
from scene import TitleScene, InstructScene, GameScene, LeaderScene
from settings import *

__author__ = 'Wesley Lee'
__email__ = 'shotun123@csu.fullerton.edu'
__maintainer__ = 'shotun123'


def main():
    """Main function to loop the program"""

    screen = pygame.display.set_mode((BOARDWIDTH, BOARDHEIGHT))
    pygame.display.set_caption("Snake game")
    clock = pygame.time.Clock()
    g_snake = Game(screen, 'right', True)

    while True:
        #list of levels the game goes through
        scene_list = [TitleScene(1, screen, PINK, INTRO, BLACK, 40),
                      InstructScene(2, screen, PINK, 30),
                      GameScene(3, screen, LIGHTBLUE, g_snake),
                      LeaderScene(4, screen, LIGHTGREY, LEADER, g_snake)]

        for scene in scene_list:
            scene.start_scene()
            while scene.is_valid():
                clock.tick(FPS)
                for event in pygame.event.get():
                    scene.process_event(event)
                scene.update()
                scene.draw()
            scene.end_scene()



if __name__ == '__main__':
    main()
