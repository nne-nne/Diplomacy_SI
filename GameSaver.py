from diplomacy import Game
from diplomacy.utils.export import to_saved_game_format, load_saved_games_from_disk
from GameVisualizer import *
import os

class GameSaver:
    def __init__(self):
        self.save_frame = 0
        self.read_frame = 0
        self.visualizer = None
        self.game = None

    def save_game(self, game:Game, name):
        #to_saved_game_format(game, output_path = os.path.join('/saved_games',name,'frame_' + str(self.save_frame) + '.json'))
        to_saved_game_format(game, output_path = './frames/frame_' + str(self.save_frame) + '.json',output_mode='w')
        self.save_frame += 1


