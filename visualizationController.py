import pygame
from GameVisualizer import *
from diplomacy import Game
from diplomacy.utils.export import to_saved_game_format, load_saved_games_from_disk
import os


class VisualizationController:
    def __init__(self, directory, name):
        self.i = 0
        self.limit = 9

        self.directory = directory
        self.game_name = name

        #self.game = load_saved_games_from_disk(os.path.join(directory, game_name,'frame_' + str(i)+'.json'))[0]
        self.game = load_saved_games_from_disk('frame_' + str(self.i)+'.json')[0]

        self.visualizer = GameVisualizer()
        self.visualizer.paint_map(self.game)

        self.orders_visible = False

    def change_frame(self, change:int):
        self.i = (self.i + change) % self.limit
        self.game = load_saved_games_from_disk('frame_' + str(self.i) + '.json')[0]
        # self.game = load_saved_games_from_disk  \
        # (os.path.join(self.directory, self.game_name,'frame_' + str(self.i)+'.json'))[0]
        self.visualizer.paint_map(self.game)
        if self.orders_visible:
            self.visualizer.paint_orders(self.game)


    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.visualizer.paint_orders(self.game)
                    if event.key == pygame.K_LEFT:
                        self.change_frame(-1)
                    if event.key == pygame.K_RIGHT:
                        self.change_frame(1)

visualization = VisualizationController('/saved_games', 'wwi')
visualization.run()


